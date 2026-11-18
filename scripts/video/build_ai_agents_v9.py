"""Build the approved AI Agents three-roll review cut from the November originals."""
from pathlib import Path
import json
import subprocess

import cv2
import numpy as np

from editspec_build import Build, FPS, H, W, Reader, fr, sha
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px, smoothstep

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/ai-agents-build-2026-11-18-v9'
REVIEW = ROOT / 'video-audit/ai-agents-rolls-1-3-2026-11-18'
DEST = ROOT / 'Prompts/ai-agents-v9.mp4'
RAW = {i: ROOT / f'Prompts/ai-agents-{i}.mp4' for i in (1, 2, 3)}
ASSET = ROOT / 'course-assets/ai-agents'
ASSETS = {k: ASSET / f'ai-agents-{k}.jpg' for k in ('uses', 'agent-loop', 'close')}
COLORS = ['#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a', '#6e51ff', '#6e51ff']
CARDS = [(40,127,784,799), (816,127,1560,799), (40,831,784,1503), (816,831,1560,1503)]
FLOW = [(72,169,389,584), (452,169,769,584), (832,169,1149,584), (1212,169,1529,584),
        (586,619,1395,733), (40,802,1560,890)]

# Cuts fall inside measured quiet intervals. The worker-question splice keeps 0.75s.
PARTS = [
    (3,0,66.60,'Opening and course story',0),
    (1,100.37,155.97,'Four applications',0.85),
    (3,85.35,105.60,'Busywork and open question',0),
    (3,115.97,120.27,'How does it work?',0),
    (2,156.03,203.77,'Goal, plan, act, check, loop and outcomes',0.74),
    (3,145.40,148.35,'Your name',0),
    (3,154.73,160.80,'You make it better',0),
]


def prepare():
    for source in json.loads((REVIEW/'sources.json').read_text()):
        assert sha(ROOT/source['file']) == source['sha256']
    b = Build(ROOT, RAW[3], AUDIT, DEST, [RAW[1], RAW[2], *ASSETS.values(), ASSET/'ai-agents.mp4'])
    b.load_audio([(105.12,105.76),(66.27,66.90)])
    starts = []
    for i,(roll,a,z,label,gain) in enumerate(PARTS):
        starts.append(b.cursor)
        if i == 5:
            b.mark_close_start()
        if roll == 3:
            b.keep(fr(a),fr(z),label)
        else:
            b.graft(RAW[roll],fr(a),fr(z),label,f'roll-{roll}',picture_from=fr(a),gain_db=gain)
    b.finish_audio()
    b.make_close('agents')
    return b, starts


class Picture:
    def __init__(self, build, starts):
        self.b = build
        self.starts = starts
        self.readers = {}
        self.mask = glyph_mask()
        self.boards = {}
        for key in ('uses','agent-loop'):
            path,cw,ch,ox,oy = build.compose(ASSETS[key],key)
            self.boards[key] = (cv2.imread(str(path)),np.array([cw/2-ox,ch/2-oy,cw]),ox,oy)
        self.last_state = None
        self.cached = None

    def native(self, roll, source_time):
        target = fr(source_time)
        reader = self.readers.get(roll)
        if reader is None or target < reader.n:
            if reader:
                reader.c.release()
            reader = self.readers[roll] = Reader(RAW[roll])
        return clean_frame(reader.at(target),self.mask)[0]

    def board(self, key, idx=None, camera=None):
        board,full,ox,oy = self.boards[key]
        cx,cy,width = full if camera is None else camera
        state = (key,idx,cx,cy,width)
        if state == self.last_state:
            return self.cached
        scale = W/width
        left,top = cx-width/2, cy-H/(2*scale)
        transform = np.float32([[1/scale,0,left+ox],[0,1/scale,top+oy]])
        frame = cv2.warpAffine(board,transform,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_REPLICATE)
        if idx is not None:
            rect = (CARDS if key=='uses' else FLOW)[idx]
            x,y,r,z = rect
            draw_ring(frame,(x-left)*scale,(y-top)*scale,(r-left)*scale,(z-top)*scale,
                      hex_bgr(COLORS[idx].lstrip('#')),max(4,14*scale),ring_px(H))
        self.last_state,self.cached = state,frame
        return frame

    def scene(self, f):
        t = f/FPS
        starts = self.starts
        uses_start = starts[1]
        flow_start = starts[4]
        # Establish current canonical boards on the introductory lines.
        if f < uses_start-fr(3.2):
            if t < 7:
                return self.native(3,7.15+0.86*t),'authors'
            if t < 13.8:
                return self.native(1,19.5+t-7),'agent task sequence'
            if t < 19.8:
                return self.native(1,28.0+t-13.8),'course design'
            if 27.9 <= t < 42.5:
                return self.native(2,36.4+(t-27.9)*0.774),'request, file and tests'
            if 42.5 <= t < 48.6:
                return self.native(2,48.2+(t-42.5)),'human review'
            return self.native(3,t),'course story'
        if f < starts[2]:
            s = (f-uses_start+fr(PARTS[1][1]))/FPS
            cues = [100.68,111.18,127.60,143.66]
            idx = sum(s >= cue for cue in cues)-1
            full = self.boards['uses'][1]
            if idx < 0:
                return self.board('uses'),'applications overview'
            def card_camera(i):
                x,y,r,z = CARDS[i]
                return np.array([(x+r)/2,(y+z)/2,self.b.fit_w(r-x,z-y)])
            current = card_camera(idx)
            before = full if idx==0 else card_camera(idx-1)
            move_seconds = 4.0 if idx == 2 else 2.4
            progress = np.clip((s-cues[idx])/move_seconds,0,1)
            if idx==2:
                # Pull out across the row change, then settle on the lower-left card.
                camera = (before+(full-before)*smoothstep(min(1,progress*2)) if progress<0.5 else
                          full+(current-full)*smoothstep(2*progress-1))
            else:
                camera = before+(current-before)*smoothstep(progress)
            return self.board('uses',idx,camera),f'applications card {idx+1}'
        if f < starts[3]:
            source = (f-starts[2]+fr(PARTS[2][1]))/FPS
            return self.native(3,max(86.0,source)),'busywork and workers'
        if f < flow_start-fr(3):
            return self.native(3,116.4+(f-starts[3])/FPS),'transition'
        if f < starts[5]:
            s = (f-flow_start+fr(PARTS[4][1]))/FPS
            if 179.70 <= s < 183.25:
                return self.native(2,44.05+(s-179.70)),'verification example'
            cues = [156.34,162.44,170.32,177.22,185.04,194.48]
            idx = sum(s >= cue for cue in cues)-1
            return self.board('agent-loop',None if idx<0 else idx),f'loop state {idx+1}'
        age = f-starts[5]
        zoom = 1+.2*smoothstep(np.clip((age-48)/149,0,1))
        h,w = self.b.close_img.shape[:2]
        size = w/zoom
        trans = np.float32([[size/W,0,(w-size)/2],[0,size/W,(h-size*H/W)/2]])
        return cv2.warpAffine(self.b.close_img,trans,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_CUBIC),'close'


def main():
    if DEST.exists():
        raise SystemExit(f'Candidate already exists: {DEST}')
    cv2.setNumThreads(2)
    b,starts = prepare()
    picture = Picture(b,starts)
    temp = AUDIT/'render.tmp.mp4'
    boundaries = {f:row['label'] for f,row in zip(starts[1:],b.rows[1:])}
    previous = None
    cmd = [b.ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30',
           '-i','pipe:0','-i',str(AUDIT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264',
           '-vf','scale=out_range=full:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int',
           '-color_range','pc','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
           '-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
           '-movflags','+faststart',str(temp)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for f in range(b.total):
            frame,label = picture.scene(f)
            if label != previous:
                if f:
                    boundaries[f] = label
                print(f'{f/FPS:.2f}s {label}',flush=True)
            previous = label
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait():
            raise RuntimeError('Video encoding failed')
    for reader in picture.readers.values():
        reader.c.release()
    assert all(sha(path)==original for path,original in b.hashes.items())
    manifest = b.manifest(dict(parts=PARTS,
                    card_rects=CARDS,loop_rects=FLOW,render_sha256=sha(temp),
                    gain_basis_lufs={'base':-19.35,'applications':-20.20,'loop':-20.09}))
    manifest['boundaries'] = [dict(frame=f,label=l) for f,l in sorted(boundaries.items())]
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    temp.rename(DEST)
    print(DEST, b.total/FPS,flush=True)


if __name__ == '__main__':
    main()
