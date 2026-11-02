#!/usr/bin/env python3
"""Shorter narration; unchanged canonical boards and teaching examples. Review only."""
from pathlib import Path
import json,subprocess,wave,copy
import av,cv2,numpy as np
import build_next_level_moves_v3 as base
import next_level_moves_zoom as zoom
from editspec_build import Build
from ken_burns_path import draw_ring,ring_px,hex_bgr
ROOT=base.ROOT
OUT=ROOT/'video-audit/next-level-moves-shortening-2026-11-02/build-v5'
SOURCE=ROOT/'Prompts/next-level-moves-v4.mp4'
DEST=ROOT/'Prompts/next-level-moves-v5.mp4'
EXPECTED='e11bc8d471d161b922a39a7302ade3d7d9ac2be20f6cfcbc05cb90cdd9d7d4bb'
FPS=30;SR=48000
# Each endpoint is in a measured source silence. No time stretching or added pauses.
CUTS=[
 (1908,2029,'summer-filler','The AI answers, absolutely. Let’s start with where you are.'),
 (2300,2393,'summer-logistics','I can get around my neighborhood, and I have afternoons free.'),
 (2735,2854,'summer-banner','Repeated takeaway banner.'),
 (3895,4067,'profit-background','Three friends available part-time; definition of sales.'),
 (4448,4546,'profit-multiplication','Suppose your crew mows ten lawns at thirty dollars each.'),
 (4602,4836,'profit-expense-detail','Individual labor and supply amounts; keep total costs and profit.'),
 (5107,5240,'profit-banner','Repeated takeaway banner.'),
 (6228,6311,'college-filler','The AI answers, let’s start with the goal.'),
 (6491,6618,'college-banner','Repeated takeaway banner.'),
 (8586,8876,'iteration-questions-and-banner','Last two questions and repeated takeaway banner.'),
]
TOTAL=9206-sum(b-a for a,b,_,_ in CUTS)
SPANS={**zoom.SPANS,'pr':(3704,5265),'co':(5910,6636)}
ASSETS={**zoom.ASSET,'pr':'profit','co':'college'}
def mapped(f):return f-sum(max(0,min(f,b)-a) for a,b,_,_ in CUTS if f>a)
def removed(f):return any(a<=f<b for a,b,_,_ in CUTS)
def pieces():
 start=0;result=[]
 for a,b,_,_ in CUTS:
  result.append((start,a));start=b
 result.append((start,9206));return result

class Board:
 def __init__(self,key):
  self.key=key;sa,sb=SPANS[key];self.start=mapped(sa);self.end=mapped(sb)
  dummy=object.__new__(Build);dummy.out=OUT
  p,self.cw,self.ch,_,_=dummy.compose(ROOT/f'course-assets/next-level-moves/next-level-moves-{ASSETS[key]}.jpg',key)
  self.image=cv2.imread(str(p));self.full=np.array([self.cw/2,self.ch/2,self.cw],dtype=float)
  spec=json.loads((zoom.OLD/f'leg-{key}.json').read_text())
  self.rings=[]
  for r in spec['rings'][:-1]:
   rr=copy.deepcopy(r);rr['start']=mapped(sa+r['start'])-self.start;rr['end']=mapped(sa+r['end'])-self.start;self.rings.append(rr)
  self.moves=[]
  if key in ['sb','it']:
   targets=[np.array([r['rect'][0]+r['rect'][2]/2,r['rect'][1]+r['rect'][3]/2-18,1120.]) for r in self.rings]
   first=self.rings[0]['start'];self.moves.append((first,first+24,self.full,targets[0]))
   for i,r in enumerate(self.rings[1:],1):self.moves.append((r['start']-24,r['start'],targets[i-1],targets[i]))
   end=self.end-self.start-3;self.moves.append((end-24,end,targets[-1],self.full))
   self.rings[-1]['end']=end-24
  else:
   # Same small full-board push, continuous across speech cuts.
   last=spec['beats'][-1]['to'];self.moves=[(0,self.end-self.start,self.full,np.array(last,dtype=float))]
  self.log={'source_span':[sa,sb],'output_span':[self.start,self.end],'rings':self.rings,'moves':[{'start':a,'end':b,'from':s.tolist(),'to':d.tolist()} for a,b,s,d in self.moves]}
 def render(self,n):
  q=n-self.start;cam=self.full;moving=False
  for a,b,src,dst in self.moves:
   if q<a:break
   if q<b:
    cam=src+(dst-src)*base.ease((q-a)/(b-a));moving=True;break
   cam=dst
  cx,cy,w=cam;h=w*720/1280
  cx=np.clip(cx,w/2,self.cw-w/2);cy=np.clip(cy,h/2,self.ch-h/2);x=cx-w/2;y=cy-h/2
  im=cv2.warpAffine(self.image,np.float32([[w/1280,0,x],[0,h/720,y]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  ring=next((r for r in self.rings if r['start']<=q<r['end']),None)
  first=self.moves[0][0]<=q<self.moves[0][1]
  if ring and (self.key not in ['sb','it'] or not moving or first):
   rx,ry,rw,rh=ring['rect'];scale=1280/w;t=ring_px(720);half=t/2
   coords=((rx-x)*scale-half,(ry-y)*scale-half,(rx+rw-x)*scale+half,(ry+rh-y)*scale+half)
   assert min(coords[:2])>=0 and coords[2]<1280 and coords[3]<720,(self.key,n,coords)
   draw_ring(im,*coords,hex_bgr(ring['color']),ring['radius']*scale+half,t)
  return im

def main():
 cv2.setNumThreads(2);OUT.mkdir(parents=True,exist_ok=True)
 assert not DEST.exists(),'Never overwrite a review candidate'
 assert base.sha(SOURCE)==EXPECTED
 protected={str(p):base.sha(p) for p in [SOURCE,ROOT/'course-assets/next-level-moves/next-level-moves.mp4',ROOT/'lessons/next-level-moves.md',*sorted((ROOT/'course-assets/next-level-moves').glob('*.jpg'))]}
 subprocess.run([base.FF,'-v','error','-y','-i',str(SOURCE),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'source.wav')],check=True)
 with wave.open(str(OUT/'source.wav')) as f:
  assert f.getframerate()==SR and f.getnchannels()==1
  pcm=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)
 chunks=[];fade=240
 for i,(a,b) in enumerate(pieces()):
  p=pcm[a*1600:b*1600].copy()
  if i:p[:fade]*=np.linspace(0,1,fade)
  if i<len(pieces())-1:p[-fade:]*=np.linspace(1,0,fade)
  chunks.append(p)
 audio=np.concatenate(chunks);assert len(audio)==TOTAL*1600
 with wave.open(str(OUT/'edited.wav'),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(np.round(audio).astype('<i2').tobytes())
 boards={k:Board(k) for k in SPANS}
 bounds={mapped(a):label for a,b,label,_ in CUTS}
 for k,(a,b) in SPANS.items():bounds.update({mapped(a):k+'-in',mapped(b):k+'-out'})
 for k,(a,b) in base.SPANS.items():bounds.update({mapped(a):k+'-illustration-in',mapped(b):k+'-illustration-out'})
 (OUT/'camera-plan.json').write_text(json.dumps({k:b.log for k,b in boards.items()},indent=2)+'\n')
 proc=subprocess.Popen([base.FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','15','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 count=0
 with av.open(str(SOURCE)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for n,f in enumerate(c.decode(video=0)):
   if removed(n):continue
   raw=f.to_ndarray(format='yuv420p')
   key=next((k for k,(a,b) in SPANS.items() if a<=n<b),None)
   cutaway=any(a<=n<b for a,b in base.SPANS.values())
   if key and not cutaway:raw=av.VideoFrame.from_ndarray(boards[key].render(count),format='bgr24').to_ndarray(format='yuv420p')
   proc.stdin.write(raw.tobytes());count+=1
   if count%1500==0:print(f'Rendered {count}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0 and count==TOTAL
 assert all(base.sha(p)==h for p,h in protected.items())
 m={'source':str(SOURCE),'source_sha256':EXPECTED,'candidate':str(DEST),'candidate_sha256':base.sha(DEST),'fps':FPS,'frames':TOTAL,'duration':TOTAL/FPS,'seconds_removed':(9206-TOTAL)/FPS,'cuts':[{'source_frames':[a,b],'source_seconds':[a/30,b/30],'output_join':mapped(a),'label':l,'removed':s} for a,b,l,s in CUTS],'retained_source_spans':pieces(),'boundaries':[{'frame':f,'label':l} for f,l in sorted(bounds.items())], 'scope':'Approved option 3: shorten spoken chats and remove spoken banners; preserve existing canonical boards, teaching, analogies and closing.', 'source_note':'Verified live-matching v4 is the narrow-edit baseline; raw rolls retained. One video and one audio encode. Original graphic cutaways retained; chat cameras and highlights retimed.', 'audio_join_fades_ms':5,'speed_change':False,'added_pauses':[],'protected_hashes':protected,'protected_files_unchanged':True,'listening':'Not auditioned by the agent; transcript, signal and visual verification performed separately.','status':'Review candidate; not installed or published'}
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(json.dumps({'candidate':str(DEST),'seconds':TOTAL/30,'saved':(9206-TOTAL)/30}),flush=True)
if __name__=='__main__':main()
