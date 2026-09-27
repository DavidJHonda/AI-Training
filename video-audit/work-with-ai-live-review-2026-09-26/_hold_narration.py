import json, sys, os
OUT="video-audit/work-with-ai-live-review-2026-09-26"
def st(t): m,s=divmod(t,60); return f"{int(m)}:{s:05.2f}"
for s in sys.argv[1:]:
    tp=f"{OUT}/_transcripts/{s}.json"
    if not os.path.exists(tp): print(f"== {s}: no transcript yet"); continue
    words=json.load(open(tp))["words"]; spans=[x for x in json.load(open(f"{OUT}/{s}/board-spans.json"))["spans"] if x["length"]>=3]
    print(f"== {s}")
    for x in spans:
        w=[q for q in words if q["end"]>x["start"] and q["start"]<x["end"]]
        if not w: txt="(silent)"; first=last=""
        else:
            first=" ".join(q["word"] for q in w[:9]); last=" ".join(q["word"] for q in w[-7:])
        # silence tail: last word end vs span end
        tail=(x["end"]-w[-1]["end"]) if w else x["length"]
        head=(w[0]["start"]-x["start"]) if w else 0
        flag="LONG" if x["length"]>20 and not x["board"].endswith("-close") else "ok"
        print(f"  {x['board'].replace(s+'-',''):28s} {st(x['start'])}-{st(x['end'])} {x['length']:5.1f}s {flag:4s} lead-in {head:4.1f}s tail {tail:4.1f}s | \"{first} … {last}\"")
