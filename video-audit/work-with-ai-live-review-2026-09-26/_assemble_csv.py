import csv, os, sys
OUT="video-audit/work-with-ai-live-review-2026-09-26"
order=["work-with-ai-opener","ai-is-different","where-ai-works-best","your-home-base","questions-matter","art-of-prompting","context-window","evaluate-the-results","critical-thinking"]
SUM="lesson,video,candidate,duration,verdict,why,points_total,rich,taught,thin,missing,wrong,hard_met,hard_total,hard_missed,errors,source_qa,additions,repair_feasible,reroll_needs,listening_limits".split(",")
PTS="lesson,video,kind,n,point,rating,timestamp,spoken_or_note".split(",")
summ=[]; pts=[]; problems=[]
for s in order:
    a=f"{OUT}/{s}/narration-summary.csv"; b=f"{OUT}/{s}/narration-points.csv"
    for p,hdr,dest in ((a,SUM,summ),(b,PTS,pts)):
        if not os.path.exists(p): problems.append(f"missing {p}"); continue
        with open(p,newline="",encoding="utf-8") as fh:
            r=csv.DictReader(fh)
            if [h.strip() for h in r.fieldnames]!=hdr: problems.append(f"header mismatch {p}: {r.fieldnames}")
            for row in r:
                row={k.strip():(v or "").replace("\n"," / ").strip() for k,v in row.items() if k}
                row["lesson"]=s; dest.append(row)
def write(path,hdr,rows):
    with open(path,"w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=hdr,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
write(f"{OUT}/narration-review-summary.csv",SUM,summ)
write(f"{OUT}/narration-review-points.csv",PTS,pts)
print(f"summary rows {len(summ)}, point rows {len(pts)}")
for p in problems: print("PROBLEM:",p)
for r in summ: print(f"  {r['lesson']:22s} {r['verdict']:7s} pts {r['points_total']:>3} R{r['rich']:>2} T{r['taught']:>2} Th{r['thin']:>2} M{r['missing']:>2} W{r['wrong']:>2}  hard {r['hard_met']}/{r['hard_total']}")
