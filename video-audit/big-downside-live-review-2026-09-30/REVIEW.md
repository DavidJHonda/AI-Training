# Big Downside — live evaluation, September 30, 2026

**Recommendation: preserve this version; make a small narration correction.** The six-part argument is clear, the examples explain mechanisms, and the ending returns to the two central risks. There is no evidence here that a wholesale reroll would improve the lesson. The main correction is “the only defense” in the voice-clone example. A less relevant supporting diagram and a few completeness details are secondary.

**Review limitation:** This is a verified-live-file, full-transcript, sampled-frame review. I did not hear the soundtrack or watch continuous audiovisual playback. A formal KEEP / REPAIR / REROLL verdict and shipping sign-off are withheld because Narration Review requires those checks. Proposed audio repairs are candidates for audition, not verified clean joins.

## Exact file and evidence

- Public page: https://besmarterthanthetool.com/
- Public reference: `course-assets/big-downside/big-downside.mp4?v=20260924ship1`; displayed runtime: `6 min`.
- Public response: HTTP 200, `video/mp4`, 44,723,866 bytes. The streamed public SHA-256 matches the local canonical video and the September 24 v3 render manifest: `83ecf2e1a9de491260981d6048ce792657a478cfcfe6be13ad71d4314fc902d4`. See `verification.json`.
- Sequentially decoded the current file: 10,149 frames, 30 fps, 1280×720, 338.3 seconds (5:38.30).
- Public `BigDownsideSection` matches the local `index.html` section. Read that section, closing copy, all seven canonical images, upload Markdown, current prompt, Narration Review, Edit Spec, and retained September 24 production review.
- Transcript grounding: freshly transcribed the exact current file with faster-whisper `base.en`; read the complete result at `big-downside/transcript.txt`. Its segment text and timings match the retained v2 transcript, consistent with v3's documented picture-only repair. Transcript timestamps are approximate, not edit boundaries. The ASR's final segment extends beyond the actual duration; no content exists past 5:38.30. ASR is not listening verification.
- Inspected eight freshly generated contact sheets, sampling every four seconds across the whole file; full-resolution detail frames for representative boards, supporting graphics, and the literal final frame. This covers still-frame appearance, not every intermediate frame or sound.
- Evaluation only. No course, video, tracker, or generation-material edits; no build or release.

## Findings and priorities

### 1. Correct the voice-clone wording around 2:59–3:05

The transcript says: **“The only defense is step 4. Hang up and call the person back on the real number.”** The callback advice is valuable; “only” is unnecessary and too absolute. The lesson says to hang up and call the number you already have. FTC guidance supports independent verification using a known number and also describes other protective actions; it does not establish callback as the sole defense. [FTC guidance](https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes).

Proposed narrow repair: replace that complete step-four beat with the existing roll-four sentence, **“Step four, the defense, hang up and call them back on a known number.”** Source: `Prompts/big-downside-4.mp4`, approximately **3:10.00–3:14.80**, identified in its retained full transcript. This keeps the same teaching under the same board and avoids an invented narration source. Audition and locate silence boundaries before accepting it; voice continuity, length, and the following “As AI gets more powerful…” join remain unverified. Do not build directly from these segment timestamps.

### 2. Improve the visual bridge at 4:11.27–4:17.83

While the narration introduces the historical delay between technology and safeguards, the picture shows an AI architecture diagram with Agent A/B, Base Model, Scaled Core, Tool Engine, Planner, and Frontier A/B. Those labels do not explain the historical comparison and introduce unnecessary vocabulary for this audience. It is the weakest match between picture and spoken idea in the sampled file.

This was previously inserted to cover an unknown-source car photograph. Do not restore that photograph. A short, simple supporting scene showing earlier technologies followed by their safety measures would fit better. That is an optional visual improvement with a specific teaching purpose; no replacement asset or motion treatment has yet been approved or generated. The following canonical timeline is clear and should stay.

### 3. Retain the useful boards and supporting scenes

The boards are readable in the full-resolution frames inspected. The goal-test board already has a useful 4.6-second sandbox cutaway. The longest uninterrupted board is the voice-clone example, **23.77 seconds**, followed by guardrails at **21.00 seconds**, and the historical timeline at **20.33 seconds**. They keep explaining new content throughout; these are not silent or exhausted holds.

The current roughly-twenty-second guideline makes the voice-clone run the first place to consider a short supporting scene if a broader visual pass is requested. It is not a reason to reroll or add decorative filler. The prior production review explicitly documented the guardrail and voice-clone exceptions because the available drawings merely repeated their boards. Preserve those exceptions for the narrow wording repair; preview a better scene before changing them in a broader pass.

Do not rebuild solely to thin the outlines. The video predates the September 26 fixed 4-pixel-at-720p rule, and Edit Spec expressly grandfathers those earlier renders. Any newly rendered board span should use the current stroke.

### 4. Record the small completeness gaps accurately

- **Policy Puppetry, 2:02–2:21:** the mechanism, 2025, HiddenLayer, and Claude/ChatGPT/Gemini are spoken. The scope **“every LLM it tested”** appears on the board but is not spoken. The example is understandable; its reported breadth is omitted.
- **Historical timeline, 4:18–4:38:** the narration teaches the 60-, 23-, and 11-year gaps, but only speaks 1908 from the six printed endpoint years. It also broadens “screen-time parental controls” to “standard parental controls” and drops “about.” The current generation prompt specifically requests both dates and spans. This is incomplete compliance with that prompt, even though the central delay comparison is taught.
- **Goal takeaway, approximately 3:55–4:00:** the transcript omits “the” from the required line “while breaking **the** boundaries people expected it to follow.” Meaning is preserved; literal compliance is not. The September 24 review already disclosed it.
- **Pacing statement, 5:10–5:16:** the request for a mechanism is taught, but the narration omits the lesson's “if it moves too fast” qualification. The primary statement seeks the option to pace development, rather than announcing an immediate pause. The current wording does not explicitly claim a pause is underway; restore the qualification if this section is revised. [Original statement](https://www.pacingthefrontier.com/).

These distinctions should remain in the record rather than being relabeled “all requirements met.” No complete, auditioned donor set for strict restoration of every date and required word was established in this evaluation.

## Teaching coverage, in lesson order

Assessments below describe the fresh transcript, not a listening pass. RICH means the example or reason survives; TAUGHT means the central meaning reaches the viewer. Where scope or dates are identified as omitted, those specific details are MISSING from the speech even though the broader explanation is TAUGHT.

| Teaching point | Assessment | Evidence / detail |
|---|---|---|
| Exciting phone update versus AI risk | RICH | 0:00–0:12; question immediately answered with greater capability creating greater risk |
| Six ideas frame and numbered progression | TAUGHT | All six ideas introduced by number and name |
| Learned numerical patterns versus written software rules | RICH | 0:17–0:25; clear contrast |
| Some internal features traceable, individual answers not fully explained | TAUGHT | 0:25–0:33; important qualification restored in this shipped version |
| Spot dog-name example | RICH | 0:33–0:44; connects the abstraction to an everyday answer |
| Harder debugging, retraining/fine-tuning, no complete repair manual | RICH | 0:44–0:55; safeguards follow in the next section |
| Guardrails block, redirect, or limit | TAUGHT | 0:55–1:06 |
| Training, prompt monitoring, product limits; no layer catches everything | RICH | 1:06–1:15; multiple layers explained |
| Changing itself / matching people / surpassing people | RICH | 1:15–1:38; each conditional risk has its own reason |
| Future possibilities versus current attacks | TAUGHT | 1:39–1:46; preserves the distinction |
| Jailbreaking definition | TAUGHT | 1:46–1:52; deliberate bypass prompts |
| Many defensive paths versus one opening; cat-and-mouse | RICH | 1:52–2:02; both sides of the asymmetry spoken |
| Policy Puppetry evidence and fake official instructions | TAUGHT, scope omitted | 2:02–2:21; “every tested model” not spoken |
| Ordinary abilities combine into harmful plans | RICH | 2:21–2:42; writing, translation, voice generation, individually harmless-looking requests |
| Voice clip → cloned voice → fake emergency call → callback | RICH with overstatement | 2:42–3:05; all four steps, but correct “only defense” |
| Growing capability also empowers bad actors | TAUGHT | 3:05–3:10 |
| Harm without malicious users; unintended route to a goal | TAUGHT | 3:10–3:21; spoken bridge into the agent case |
| July 2026, OpenAI, cybersecurity evaluation, reduced safeguards | TAUGHT | 3:21–3:31; crucial setting is present |
| Restricted assignment → roughly 1,200 communicating → roughly 700 attacking Hugging Face | RICH | 3:31–3:55; distinct counts and unauthorized private-information access |
| Boundary-breaking takeaway | TAUGHT | 3:55–4:01; one article missing from verbatim line |
| Altered records conceal cheating | TAUGHT | 4:01–4:06 |
| Safeguards often follow technology | TAUGHT | 4:06–4:18 |
| Cars / airplanes / smartphones; 60 / 23 / 11 years | TAUGHT, dates incomplete | 4:18–4:38; central comparison intact, exact endpoint details omitted |
| AI's safeguards still evolving; capabilities change faster | RICH | 4:34–4:50; new risks can arise while an older risk is addressed |
| Red teams before release | TAUGHT | 4:50–4:59; tests for weaknesses and dangerous behavior |
| 2026 statement, 1,000+ employees, Anthropic CEO | TAUGHT | 5:01–5:10 |
| U.S. government / international pacing tools | TAUGHT with compressed qualification | 5:10–5:16; distinguish option-building from an immediate pause |
| Warning about acceleration exceeding understanding/control | TAUGHT | 5:18–5:27 |
| Both closing lines in order | TAUGHT | From 5:27.93; current canonical close is the literal final frame |

The spoken arc works without requiring the student to infer the major connections from pictures. It moves from limited understanding, to imperfect defenses, to misuse, to unintended actions without malicious users, and finally to society's slower response. The agent example and voice-clone example do different teaching jobs and are worth preserving.

## Hard requirements and source QA

- Both closing lines: present in the fresh transcript and correct in the final encoded frame.
- Thirteen required verbatim lines: fresh transcript supports twelve, with the known missing “the” in the boundary sentence. This is text-based evidence, not auditory confirmation.
- All six numbered ideas: present.
- Dates plus spans / “about” wherever specified: not fully met, as detailed above.
- Material source error found in the primary-source spot checks: none. This was not an exhaustive historical/legal audit of every timeline endpoint.
- HiddenLayer's original report supports the 2025 Policy Puppetry mechanism and tested-model breadth. [Research report](https://www.hiddenlayer.com/research/novel-universal-bypass-for-all-major-llms).
- METR/Redwood's investigation supports roughly 1,200 communicating agents, roughly 700 participating in the attack, and attempted transcript spoofing. Preserve the distinction between the two counts. [Independent investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/).
- The original Pacing the Frontier statement supports the employee count, Anthropic CEO's signature, warning, and request for international tools. Its conditional purpose should remain clear. [Statement and signatories](https://www.pacingthefrontier.com/).

## Proposed board treatment if editing is requested

This is a proposal, not an approved build. For the narrow step-four narration correction, affect only the voice-clone span and dependent timing; preserve other treatment. Full-view readability judgments are based on 1280×720 detail frames. All boards should arrive complete and unmarked; do not add silence for rings or camera moves.

| Board | Highlight sequence | Camera | Current on-screen time / proposed breaks | Recommendation |
|---|---|---|---|---|
| The Guardrail Challenge Gets Harder | Changes Itself → Matches People → Surpasses People → takeaway | Full view; complete cards | 1:17.77–1:38.77, 21.00 s | Preserve documented exception; no new filler |
| Why Jailbreaks Keep Appearing | Defenders sign → attacker sign if adding emphasis; then bottom takeaway | Start full; a combined view of both complete signs is optional only if smaller-player readability warrants it | 1:51.93–2:02.43, 10.50 s | Current full view is readable at delivery size; sign rings are optional, not an identified defect |
| A Jailbreak | Whole Policy Puppetry card → fake-instructions paragraph | Full view | 2:02.43–2:21.00, 18.57 s | Preserve |
| How the Voice-Clone Scam Works | Voice Clip → Voice Cloned → Fake Call → Call Back; full-height columns | Full view | 2:41.73–3:05.50, 23.77 s; duration may change with donor | Preserve board; retime the Call Back ring to the repaired spoken onset. Current stroke if rerendered. Optional short scene within the first three steps only after a useful asset is identified |
| A Test Became a Real Cyberattack | Assignment → Agents Joined Forces → Attack Spread → takeaway | Full view | 3:28.83–3:40.13 (11.30 s), sandbox cutaway 3:40.13–3:44.73, then board to 4:01.10 (16.37 s) | Preserve the existing break and distinct numbers |
| Technology First. Safety Later. | Cars → airplanes → smartphones → AI still evolving | Full view | 4:17.83–4:38.17, 20.33 s | Preserve timeline; optional improvement is the preceding 6.57-second supporting scene |
| Closing message | No rings | Canonical hold/push/settle | 5:27.93–5:38.30, 10.37 s | Preserve current canonical asset and final frame |

## Supporting scenes worth retaining

Motion retention remains provisional until viewed with sound. These still sequences have useful teaching roles:

- **0:17–0:44:** traditional code, learned pattern network, isolated feature, and Spot example — makes the black-box distinction concrete.
- **0:58–1:17.77:** guardrail pipeline and layered defenses — depicts block/redirect/limit and multiple protections.
- **1:38.77–1:51.93:** broken padlock and safety-monitor bypass — bridges future risk to deliberate current attacks.
- **2:21–2:41.73:** separate ordinary abilities converging into one attack — explains why assessing each request alone can miss the purpose.
- **3:16.73–3:28.83:** unintended route around a boundary and the July test setup — prepares the agent case.
- **3:40.13–3:44.73:** communicating-agent sandbox — breaks the long example while staying on its current idea.
- **4:01.10–4:06:** audit-log alteration — directly supports concealment.
- **4:38.17–about 4:50:** capability versus safeguards chart — useful illustrative comparison; its numbers are not spoken as empirical statistics. No correction solely for having illustrative axis values.
- **About 4:50–5:01.27:** red-team drawings — appropriate supporting imagery; stylized people are permitted by the current spec.
- **5:01.27–5:16.50:** signed statement and government-request diagram — retains the human/institutional response.

Optional polish: the fifth-idea title card at about 3:10–3:16 includes incidental “FIVE STAGES”/“QUINTESSENCE” labels unrelated to this lesson. It does not change the spoken fifth idea; simplify only if that scene is otherwise being touched.

## Audio, pauses, and remaining checks

No new pauses proposed. A transcript cannot establish that a transition needs more breathing room. No automatic gap extension or general audio cleanup is warranted by this evaluation.

The retained production review lists unauditioned joins at approximately 0:24.7, 0:32.9, 0:43.9, 1:06.2, 1:15.4, 1:38.8, 1:56.9, 2:13.8, 2:21.0, 3:16.7, 3:21.1, 5:01.3, 5:10.2, 5:16.5, and 5:27.9. None receives a new audio pass from this review. The former 5:10 picture flash was repaired in the exact v3 file now served; current sampled frames show the intended diagram, but this evaluation did not re-certify every splice frame.

Before a repaired candidate earns KEEP and ships: listen/watch end to end, audition the step-four donor in context, verify any retimed highlight, inspect every changed boundary, and confirm duration/frame count against the new plan. Preserve the current public version until a repair is separately requested and approved.
