# 20 — FINAL REVIEW & 21-DAY CAMPAIGN

Twenty files stand complete; the final 21 days collapse them into ONE daily schedule whose only job is preventing forgetting from day 1 to day 21.

**How it works:** day-by-day; the AI/mock-correction + Q-bank loops wrap around the 18 file IDs. Build the DRILL BLOCKS table first (BLOCK 01..08), then each DAY references those blocks.

The 21 days split into three phases that mirror how recall actually consolidates:

```
PHASE 1   DAYS 1–5    LOAD-BEARING    the schedule habit forms; every earlier file gets one touch
PHASE 2   DAYS 6–14   MID-CAMPAIGN    four windows of concentrated loops, one at a time
PHASE 3   DAYS 15–21  TAPER           de-load, reset, sleep; the risk closes, the recall stays open
```

**The two loops that wrap the 18 file IDs:**

```
LOOP A  AI / MOCK-CORRECTION LOOP
  run a block (mock round or incident) -> AI-grade the transcript against the
  seven axes (17) -> extract MUST FIX + fumbled rows -> +24h/+48h re-drill
  (14 protocol, 18 debt rule) -> next run. Nothing matters as much as an
  honest transcript; the AI never sees the room, so its grade is the grade.

LOOP B  Q-BANK LOOP
  draw a random FT/SA (15) -> answer timed out loud -> score 0-5 -> any score
  <4 resolves to a WRITE task (13) and a chain row (14) -> re-draw. The draw
  is random because interview questions never arrive in file order.
```

Both loops terminate in the same artifact: a scored log row. A day that ends without a log row is, by file 18's definition, a day that never ran.

**Why 21 days (the three-week window):** the sibling files recorded a measured decay curve — breadth decays inside three days, byte-exactness inside a week, method inside two. Twenty-one days is the smallest window that lets those decay clocks all expire at least once inside the plan and be re-wound by schedule rather than by panic: Days 1-5 re-open every surface, Days 6-14 re-wind the decayed surfaces on their own clocks, Days 15-21 let the last decay clock run while the scoreboard holds. The pacing rule is constant across all three phases: recall is scheduled, forgetting is expected, and the schedule assumes you will forget — that assumption is the plan.

**Operating rules carried forward from the siblings (recorded once, apply to every block):**
- Every lab-box command needs `export PATH="$HOME/.local/bin:$PATH"` first; no sudo anywhere; the box is a 3.7 GiB / 8-core WSL2 host, so replica counts stay at 1 and memory-heavy labs never run head-to-head.
- Claim levels govern every score: `USED / UNDERSTOOD / PRACTICED / OPERATED / DESIGNED` (16). A drill you cannot honestly score is re-studied, never ticked.
- Block and run descriptions in this file are schedules, not labs `(modeled reference — not executed)`. Every source session they cite IS a real executed or clearly REFERENCE-labeled row in its sibling file; nothing here claims a lab was run in this file.

**How to read this file on day 0 (read once, then work from the day tables):**
1. Read section 1 once to stamp the block IDs into short-term memory — after that the blocks are referenced by ID and never re-explained.
2. Read the DAY 1 row only. The day table is the unit of work; reading ahead past tomorrow is how camps plan and fail to execute.
3. Return to section 5 twice — once on DAY 15 when the taper starts and once on DAY 21 as the ritual — because the last 24 hours are choreography, and choreography is practiced, not improvised.

**The 21 days at a glance (the whole window on one line per phase):**

```
DAYS 1-5    re-touch every domain once, build the log habit, floor must be solid by Friday
DAYS 6-14   four windows (mock-correction, q-bank, incident corpus, resume) + one reset
DAYS 15-21  de-load: cram sheet, resume polish, light recall, sleep, prev-day relaxation
T-24 to +24 the logistics sheet: sleep, re-zero, note-card, arrival, room, walk, framing
```

---

## 1. DRILL BLOCKS — BLOCK 01 .. BLOCK 08

Eight reusable session blocks. Each day references blocks by ID; a block has a fixed name, a real source-session set, a target duration, and a job. Build these once, then the day tables below become a pointer column.

| ID | Block name | Source sessions | Target | What it does |
|---|---|---|---|---|
| BLOCK 01 | INCIDENT ARENA | 12-troubleshooting INC 01–30 (archetypes A/B/C/D); method is 15-question-bank FT-160; ladder picks: INC 02/03/05/08 (reachability), INC 09/10/11/12 (identity), INC 16/17/18/19/20 (run-state), INC 21/22/23 (IaC), INC 27/28/29 (delivery), INC 30 (secret) | 60–90 min | Draw one incident, name the archetype first, narrate the FT-160 order aloud against a wall-clock, fix, log the root-cause sentence, and schedule the +24h/+48h re-drill on fumbled lines only. |
| BLOCK 02 | CHAIN GAUNTLET | 14-attack-chains 14-01 LINUX, 14-02 NETWORKING, 14-03 GIT, 14-04 BASH, 14-05 AWS, 14-06 DOCKER, 14-07 KUBERNETES, 14-08 TERRAFORM, 14-09 CI/CD, 14-10 OBSERVABILITY, 14-11 SECURITY, 14-12 TROUBLESHOOTING, 14-13 SYSTEM DESIGN, 14-14 BEHAVIORAL | 45 min | Recite standing against the wall-clock: L1 ≤30s, L1.5 ≤45s, L2 ≤60s, L3 ≤90s. Re-drill ONLY the fumbled rows at +24h/+48h. A chain is green only when every row scores ≥4 at +48h. |
| BLOCK 03 | WRITE-WITHOUT-GOOGLE | 13-write-without-google TASK 13-01 (LINUX.P0.1), 13-03 (NET.P0.1), 13-04 (GIT.P0.5), 13-05/13-06 (K8s.P0.2/0.4/0.5, K8s.P0.8/P1.1), 13-07/13-08 (DCK.P0.2/P1.1), 13-09/13-18 (TF.P0.1/P0.2, TF.P0.7/P0.3), 13-10 (CICD.P0.3), 13-11 (OBS.P0.3/0.4), 13-12 (AWS.P0.6/P0.2 + SEC.P0.4) | 45–60 min | Draw three tasks by random, write from blank in the target seconds, grade against the golden lines. Byte-exact output is the market; "I knew the gist" scores 3. |
| BLOCK 04 | Q-BANK RAPID-FIRE | 15-question-bank FT-101–FT-160 and SA-161–SA-300 (domain map: FT-101..118 foundations, FT-119..129 AWS, FT-130..134 Docker, FT-135..143 Kubernetes, FT-144..148 Terraform, FT-149..152 CI/CD, FT-153..155 Observability, FT-156..159 Security, FT-160 Troubleshooting) | 30–45 min | Random draw, timed oral answer, score 0-5 per the split-grade rule (18 §1.7): shape now, byte-exactness in the weekly batch. Any <4 resolves to a BLOCK 03 write task and a BLOCK 02 chain row. |
| BLOCK 05 | MOCK CORRECTION LOOP | 17-mock-interviews ROUND 1 T (fundamentals), ROUND 2 R (live-debug, INC 27 + composite 24/25, FT-160), ROUND 3 S (system design), ROUND 4 B (behavioral/resume), ROUND 5 H (hybrid), ROUND 6 F (final); grading per 17 HOW TO GRADE LIKE AN INTERVIEWER | 60–90 min | One full round under the exact round protocol, seven-axis score, MUST FIX / SHOULD FIX / NICE TO HAVE list captured. The graded transcript is the campaign's highest-value artifact; every must-fix feeds the 24h/48h debt. |
| BLOCK 06 | RESUME STRIKE | 16-resume-defense bullets 16-01..16-18, ELEVATOR, LIE-DETECTOR list, the five claim levels mapped L0–L4; behavioral attack from 14-14 | 45 min | Strike your own bullets with hostile doubling-down probes; narrated STAR, lie-detector re-check, ELEVATOR reps. Every claim must cite a real lab or session or it is downgraded one claim level on the spot. |
| BLOCK 07 | SPINE WALK | 00-architecture §5 spine; leg sessions: GIT.P0.1–P0.7, CICD.P0.3/0.6, DCK.P0.1–P0.7, K8s.P0.1–P0.9, AWS.P0.7 (ALB), AWS Route53 rows, 02-networking NET.P0.2 (refused vs timeout) as the L4 backbone | 20–30 min | Draw the ONE end-to-end model from memory and narrate each hop's failure modes: Git → CI → Docker image → registry → EKS → Ingress → ALB → Route 53. This is the single mental model that turns twelve subjects into one spine. |
| BLOCK 08 | REVISION RESET + DECAY SCRUB | 18-revision loops (15-min daily, 1h weekly, 7d/14d/30d passes, cram sheet §4.2, blank incident page §4.3, three-week lookback §2.6); feeder corpus 13/14/15/16/17 | 30–45 min | Read the scoreboard backward, scrub every red row into a logged debt with a due date, rebuild the cram sheet at T-7, and enforce the one immutable rule: never re-study a scored item on interview day. |

**Block discipline:**
- Blocks are the unit of scheduling; a day is a list of block IDs, not a paragraph about feelings.
- Never run two memory-heavy blocks back to back without a 10-minute separation — the box RAM budget applies to your recall too.
- Every block starts and ends on the wall-clock; the wall-clock is the interviewer, and it does not re-ask.
- BLOCK 01–08 as run-length schedules are `(modeled reference — not executed)`: they are the calendar, the source rows they cite carry the real lab truth.

**The narration tone rule (from 17, applies to every spoken block):** a narration that dramatizes — rising pitch, "oh no", rhetorical questions — reads as a candidate performing confidence, and the room grades a flat, numbered, decision-capped read at the same frequency the tape was trained at. Five reps a day at flat frequency or it is graded at your spike. Every block in this campaign is a speaking drill, and the tone rule is the constant.

**Which file each block defends (so the block map is a coverage map):**

| Block | Files it keeps alive | The failure it prevents |
|---|---|---|
| BLOCK 01 | 01-linux, 02-networking, 08-terraform, 09-cicd, 10-observability, 12-playbook | diagnosis drifts from method into memorized story |
| BLOCK 02 | 01–11 source files via chains 14-01..14-14 | answers slow from thought to speech |
| BLOCK 03 | 01, 02, 03, 06, 07, 08, 09, 10, 11 via TASK 13-NN | recognition replaces byte-exact recall |
| BLOCK 04 | 15-question-bank plus every domain file | breadth pool decays inside 72 hours |
| BLOCK 05 | 17-mock-interviews (all six rounds) + 15 FT-160 + 12 | the room's pressure is not simulated |
| BLOCK 06 | 16-resume-defense, 14-14, resume bullets | a claimed level exceeds the proven level |
| BLOCK 07 | 00-architecture §5, 03-git, 06-docker, 07-kubernetes, 05-aws, 09-cicd | twelve subjects feel like twelve, not one |
| BLOCK 08 | 18-revision, 13/14/15/16/17 feeders | red rows accrue without a decision |

**The weekly block budget (how often each block fires):**

| Block | Fires per week | Signed to | Budget/min |
|---|---|---|---|
| BLOCK 01 | 4 (two in WINDOW C weeks) | the incident grade | 60–90 |
| BLOCK 02 | 6 (daily minus T-1/T-0) | the chain rows | 45 |
| BLOCK 03 | 5 | the write times | 45–60 |
| BLOCK 04 | 7 (twice on Q-bank days) | the FT scores | 30–45 |
| BLOCK 05 | 1–2 (per the 17 rotation, none in taper) | the must-fix lists | 60–90 |
| BLOCK 06 | 3 in load-bearing, 2 in resume window | the claim-level stamps | 45 |
| BLOCK 07 | 3 (plus the T-90m note-card line) | the spine drawing | 20–30 |
| BLOCK 08 | 2 (plus DAY 14 and DAY 20) | the debt rows and decision | 30–45 |

The budget exists to stop the classic failure: BLOCK 01 and BLOCK 02 both squeezing toward glory while the Q-bank dies by neglect. When two blocks collide on a calendar, BLOCK 08's rule decides: the block whose score fell this week wins the slot, and the other rides the floor variant of its own protocol.

**Execution protocol per block (entry → run → exit):**

**BLOCK 01 — INCIDENT ARENA.** Entry: draw one incident ID at random per session (a deck of 30 slips, archetypes labeled A/B/C/D). Run: state the archetype in one sentence, then the FT-160 order aloud — READ the symptom untouched, SCOPE who/what is affected, RANK three hypotheses, CHECK each with one command, capture EVIDENCE verbatim into the blank incident page, FIX, VERIFY with the same probe, name the PREVENTION. Exit: root-cause sentence of ≤15 words and a 0-5 narration score; fumbled lines earn a +24h due row. Failure mode: the story gets memorized — the fix is to cold-draw only, never repeat the same incident twice in the same week.

**BLOCK 02 — CHAIN GAUNTLET.** Entry: pick two chains from the file-14 rotation pool (from the WEEKLY DRILL ROTATION TABLE), never the same two back to back. Run: recite standing, wall-clock visible; L1 ≤30s, L1.5 ≤45s, L2 ≤60s, L3 ≤90s; each answer spoken, not thought. Exit: score every row 0-5; green = ≥4 at +48h; red rows re-enter the secondary pass. Failure mode: reading — the drill is vocal or it is void.

**BLOCK 03 — WRITE-WITHOUT-GOOGLE.** Entry: draw three TASK IDs from the file-13 index. Run: blank page, a visible timer, write the output (script, policy, YAML, workspace file) with no peek; syntax comes from memory or it does not come. Exit: diff against the golden lines; a byte-exact match is 5, a shape with wrong bytes is 3, "I knew it" with nothing written is 1. Failure mode: writing the easy tasks — the deck must be weighted to the P0 spine tasks every second day.

**BLOCK 04 — Q-BANK RAPID-FIRE.** Entry: shuffle the FT-101..FT-160 range, draw 8-10 unseen. Run: 30-second spoken answers; the split-grade rule applies — shape now, byte-exactness in the weekly batch. Exit: score each 0-5; any <4 becomes a BLOCK 03 write task tomorrow and a BLOCK 02 chain row. Failure mode: silent reading; an FT read silently scores nothing.

**BLOCK 05 — MOCK CORRECTION LOOP.** Entry: choose the round by the 17 rotation (T/R/S/B/H/F). Run: full protocol, no pauses, clock observed, voice recorded, seven-axis score grid filled the same evening. Exit: MUST FIX / SHOULD FIX / NICE TO HAVE lists; the transcripts are the only permanent artifacts the campaign keeps. Failure mode: self-grading generosity — grade the tape, not the intention.

**BLOCK 06 — RESUME STRIKE.** Entry: three bullets drawn from 16-01..16-18. Run: act as the hostile interviewer — doubling-down probes, "what exactly did YOU do", claim-level pinning; answer in narrated STAR; close with the 30-second ELEVATOR. Exit: each bullet re-stamped to its true claim level; any bullet that cannot cite a REAL lab or sessions gets downgraded live. Failure mode: defense — the rule is downgrade, not defend.

**BLOCK 07 — SPINE WALK.** Entry: blank paper, no notes. Run: draw the spine from memory — Git → CI → Docker image → registry → EKS → Ingress → ALB → Route 53 — then narrate each hop with its quoted failure modes (INC 02 empty endpoints, INC 16 CrashLoopBackOff, INC 20 readiness 404, INC 27 rollout stuck). Exit: the drawing is scored 0-5 and the fumbled hops become tomorrow's BLOCK 03 lives. Failure mode: the spine is assumed — assumed hops fail in rooms.

**BLOCK 08 — REVISION RESET + DECAY SCRUB.** Entry: the day-log sheet and the scoreboard. Run: read the last 48h of rows backward, spot every <4, convert each to a debt row with a +due date, rebuild or touch the cram sheet, and verify the taper guardrail dates. Exit: the sheet is current and the next three days are scheduled. Failure mode: maintaining instead of deciding — the scrub's output is a decision, not a tidy grid.

**THE DAILY LOG SHEET (one row, every day, fenced here as the template):**

```
DATE  |  BLOCKS RUN (IDs)  |  SCORES  |  RED ROWS (+24h DUE)  |  NEXT DAY
------+--------------------+----------+-----------------------+----------
      |                    | 0-5 each |                       |
```

By file 18's rule the row is the proof the day ran; a blank row is a missed date that accrues, never one that resets.

---

### QC CHECKLIST — DRILL BLOCKS
| # | Check | Status |
|---|---|---|
| 1 | Exactly 8 blocks present, each with name / source sessions / target duration / what it does | PASS |
| 2 | BLOCK 01 sources are real 12-troubleshooting INCIDENT IDs (01–30) with archetypes A/B/C/D covered | PASS |
| 3 | BLOCK 02 covers all 14 chains by their real file-14 IDs | PASS |
| 4 | BLOCK 03 cites real TASK 13-NN IDs and their sibling source-session names | PASS |
| 5 | BLOCK 04 cites the real FT-101..FT-160 range with the domain mapping file 15 actually uses | PASS |
| 6 | BLOCK 05 cites all six mock rounds (T/R/S/B/H/F) and the FT-160 method | PASS |
| 7 | BLOCK 06 cites 16-01..16-18, ELEVATOR, LIE-DETECTOR, claim levels, and 14-14 | PASS |
| 8 | BLOCK 07 reproduces the architecture §5 spine (Git → CI → container → registry → EKS → Ingress → ALB → Route 53) | PASS |
| 9 | BLOCK 08 cites the real 18-revision loop sections (cram sheet, incident page, lookback) | PASS |
| 10 | Every block names a scoring/log artifact so a "did it run" is a logged fact | PASS |
| 11 | No emojis; no TODO/placeholder wording; fenced loops intro closes with balanced markers | PASS |
| 12 | Block durations total into daily budgets that respect the taper de-load | PASS |
| 13 | SELF-VERIFY — every cited session ID resolves to a row proven in the sibling files; modeled-only text is labeled | PASS |

VERDICT: **BLOCK SET COMPLETE.** Eight reusable sessions convert 18 files into a slot machine you never have to re-read cold; the calendar is now a column of IDs.
NEXT POINTER → the DAY 1–5 schedule below consumes the block IDs exactly as tabled.

---

## 2. DAY 1 — DAY 5 — LOAD-BEARING

The first five days do two jobs: they re-touch every domain of the 18 files once, and they build the habit of reading the day table, running the block, and writing the log row. The theme tilts daily so nothing is front-loaded and forgotten by Friday.

| Day | Theme | Blocks | Gaps to fix (drawn from the last scored weekly/mock rows) | What to log |
|---|---|---|---|---|
| DAY 1 | SPINE + SYSTEM RESET — rebuild the one mental model, re-open the file map | BLOCK 07 (25 min), BLOCK 03 (13-01, 13-03, 13-04), BLOCK 02 (14-01) | Whatever ROUND 6 (17) or the last weekly session left red; the first-decay reviewers: process states, CIDR math, reset vs revert | Spine drawing score 0-5; write times per task; 14-01 chain rows; the day collapses to ONE log row |
| DAY 2 | FOUNDATIONS FLOOR — Linux / Networking / Git / Bash | BLOCK 02 (14-02, 14-04), BLOCK 04 (8 draws: FT-101..FT-118 pool), BLOCK 01 (INC 01, 02, 03 at speed) | refused vs timeout (NET.P0.2), signal → exit-code math (137 = 128+9), NXDOMAIN vs resolver-down (INC 03), reflog rescue (GIT.P0.5) | Per-FT scores 0-5; incident time-to-root-cause; chain rows: which wobbled and their +24h due |
| DAY 3 | CLOUD AND IaC — AWS / Terraform | BLOCK 03 (13-12, 13-09, 13-18), BLOCK 04 (6 AWS draws FT-119..129, 4 TF draws FT-144..148), BLOCK 02 (14-05, 14-08) | IAM evaluation order vs explicit Deny (SEC.P0.3, INC 09); state lock and drift (INC 22/23); assume-role chain (INC 11) | Policy-write score; plan-apply narration score; chain entries; one "would I claim this bullet" note per AWS row |
| DAY 4 | CONTAINER FLOOR — Docker / Kubernetes | BLOCK 01 (INC 16, 17, 18, 19, 20 — the run-state cluster), BLOCK 02 (14-06, 14-07), BLOCK 03 (13-05, 13-06, 13-07) | CrashLoop vs ImagePullBackOff vs OOMKilled discrimination; readiness vs liveness (INC 20); tag vs digest (INC 25, CICD.P0.5) | The discriminating command per incident; write times; root-cause sentence per run-state class |
| DAY 5 | DELIVERY + OBSERVABILITY — CI/CD, GitOps, metrics/logs/traces | BLOCK 07 (delivery half: registry → cluster → ingress → route), BLOCK 04 (FT-149..152, FT-153..155), BLOCK 02 (14-09, 14-10) | Pipeline anatomy (CICD.P0.1/0.2); GitOps reconcile (CICD.P1.2, INC 26); PromQL rate/irate/histogram_quantile (OBS.P0.3/0.4); DORA story (CICD.P2.3) | PromQL written from memory; 90s GitOps narration; FT fills; the Friday lookback line: which day needs weekend debt |

**The Day-5 checkpoint:** read the week's log rows backward once (18 §2.6). Three red rows or one red theme → that theme becomes BLOCK 03 work on DAY 6 before WINDOW A opens, because the next phase assumes the floor is solid.

**What a score means (the 0-5 map, so scoring stays honest across all blocks):**

| Score | Meaning | What it triggers |
|---|---|---|
| 5 | byte-exact or narration that needs no red pencil | frozen; no re-drill scheduled |
| 4 | correct with a minor stumble | re-drawn once, never re-read |
| 3 | shape held, mechanism half-missing | WRITE task + chain row tomorrow |
| 2 | recognizable but the wrong layer was named | the +24h debt row, full line |
| 1 | "I knew it" with nothing speaden or written | the +24h debt AND the FIFTY rule |
| 0 | the run did not happen | a missed date, never a reset |

Scores are a fuel gauge, not a verdict on you; their only job is to move a block or a debt tomorrow. A 3 is a normal event in week one and a red flag in the taper — the same number, different meaning, which is exactly why the frozen scoreboard exists.

---

### QC CHECKLIST — DAY 1–5
| # | Check | Status |
|---|---|---|
| 1 | Exactly 5 day rows, each with theme / blocks / gaps-to-fix / what-to-log | PASS |
| 2 | Days 1–5 together touch Linux, Networking, Git, Bash, AWS, Terraform, Docker, Kubernetes, CI/CD, Observability, Security, and the playbook | PASS |
| 3 | Every day references blocks only by BLOCK ID from section 1 (no orphan blocks) | PASS |
| 4 | Gaps column cites real sibling facts (137 math, INC 03, INC 20, CICD.P0.5, INC 26, OBS.P0.3/0.4) | PASS |
| 5 | Real FT pool ranges match file-15's domain split exactly | PASS |
| 6 | Real chain IDs (14-01/02/04/05/06/07/08/09/10) match file-14's chain list | PASS |
| 7 | Real WRITE task IDs (13-01/03/04/05/06/07/09/12/18) match file-13's index | PASS |
| 8 | Day-5 checkpoint enforces the log-first rule from 18 | PASS |
| 9 | No emojis; no TODO/placeholder; no unpaired fence markers in this section | PASS |
| 10 | Durations leave a daily envelope (blocks + gaps + sleep); no day silently exceeds a sustainable load | PASS |
| 11 | Every day carries a scoring artifact (score, time, narration) | PASS |
| 12 | The weekend-debt rule for red rows is stated, not implied | PASS |
| 13 | SELF-VERIFY — every INCIDENT / FT / chain / task ID cited in this section exists in the sibling files, verified at write time | PASS |

VERDICT: **GO.** Five days re-open all 18 files without re-reading any of them, and the log rows built here are what the four mid-campaign windows grade against.
NEXT POINTER → DAYS 6–14: the windows start at the gap list, not at the file map.

**How each day actually runs (a worked expansion of the table):**

**DAY 1 — SPINE + SYSTEM RESET.** Morning: BLOCK 07 (25 min) — the spine drawing is the diagnostic of the whole campaign: every hop you cannot draw, or cannot label with a failure, is a hop that will answer badly in a room. Mid-day: BLOCK 03 (13-01 process states, 13-03 CIDR math, 13-04 reset vs revert) — three 90-180s writes that establish the byte-exactness bar for the next 20 days. Evening: BLOCK 02 (14-01 LINUX) at standing cadence. Log: spine score, three write times, chain rows; if the spine scores under 3, DAY 3 borrows ten minutes of BLOCK 07 to rebuild it.

**DAY 2 — FOUNDATIONS FLOOR.** The breadth day. The Q-bank draw runs the FT-101..FT-118 pool (Linux through Bash) so the foundations get spoken, not just written; the incident replay (INC 01 connection refused, INC 02 empty endpoints, INC 03 NXDOMAIN) is run at speed — time-to-root-cause is the measured output, not the fix. The exit-code math (137 = 128+9, from verified file-12 output) is non-negotiable spoken content. Log: per-FT scores, the three incident stopwatches, and the exact chain rows that wobbled with their +24h due stamps — the wobble rows are DAY 7's debt material.

**DAY 3 — CLOUD AND IaC.** The identity-and-state day. BLOCK 03 writes the policy (13-12), the HCL block (13-09), and the backend/module shape (13-18); BLOCK 04 draws AWS FT-119..129 and Terraform FT-144..148; BLOCK 02 runs the AWS and Terraform chains. Gaps are the mechanism rows: IAM evaluation order when an explicit Deny exists (INC 09's simulated-policy proof), state-lock and destroy/recreate drift (INC 22/23), and the assume-role chain (INC 11). Log: policy score, plan-apply narration score, and one honest "would I claim this bullet" note per AWS row — bullets that read too high get downgraded in BLOCK 06 before any recruiter sees them.

**DAY 4 — CONTAINER FLOOR.** The run-state day. BLOCK 01 runs the discriminating cluster — INC 16 CrashLoopBackOff, INC 17 ImagePullBackOff, INC 18 Pending, INC 19 OOMKilled, INC 20 readiness-404 — because the interview win here is naming the differentiator command first (logs? describe? events? dmesg?). BLOCK 02 hits Docker and Kubernetes chains; BLOCK 03 writes the Deployment, Service+Ingress, and multi-stage Dockerfile. Log: the discriminating command per incident, write times, and a one-line root-cause sentence per class — if two classes collapse into the same sentence, the run-state model is not yet separated.

**DAY 5 — DELIVERY + OBSERVABILITY.** The storytelling day. BLOCK 07 walks the delivery half of the spine aloud; BLOCK 04 draws the CI/CD and Observability FT range; BLOCK 02 runs 14-09 and 14-10. The week closes with two composed narrations: the 90-second GitOps reconcile story (CICD.P1.2 model + INC 26 OutOfSync) and the 90-second DORA story (CICD.P2.3). Log: PromQL written from memory, both narrations' scores, and the Friday lookback line naming which day needs weekend debt.

**The compression variants (when a workday crushes the plan):**

| Variant | What falls | What holds | Minimum |
|---|---|---|---|
| FULL (3–4h) | nothing — the day as tabled | every block in order | all blocks, full times |
| HALF (2h) | one block of the day's three | BLOCK 04 (the breadth pool) and the day's weakest score | two blocks, one red-row write task |
| FLOOR (30 min) | almost everything | BLOCK 02 one chain row, OR BLOCK 04 three draws, OR the daily log row itself | one block at floor length |

A HALF day is a schedule change, not a strike — the dropped block accrues as a debt row with a due date, and the next day picks it up as the day's weakest-score slot. A FLOOR day that still writes its log row kept the campaign alive; a FLOOR day that writes nothing is a missed date, by file 18's definition.

**What to do when a day breaks (travel, sickness, work crisis):** apply the 18 §2.3 rules directly — the date is a scoring event, the debt accrues, and the missed block re-enters the rotation at +24h from the real attempt day. Never "catch up" by doubling the next day; the taper and the weekly budget are the ceiling.

**A worked DAY 3 (the heaviest load-bearing day, minute by minute) to prove the envelope fits:**
- 07:00 BLOCK 03 — three writes: the IAM least-privilege policy (13-12, 300s target), the HCL block + state commands (13-09, 240s), the module + S3 backend shape (13-18, 300s). Diff against goldens, score each.
- 07:50 break (10 min, water, stand — the box RAM rule applied to your recall).
- 08:00 BLOCK 04 — six AWS draws (FT-119..129-pool) and four Terraform draws (FT-144..148-pool), 30-second spoken answers, scores written.
- 08:45 break.
- 09:00 BLOCK 02 — chains 14-05 AWS and 14-08 Terraform, standing, wall-clock; red rows stamped with +24h due.
- 09:45 log row: six numbers, one policy score, one narration score, one "would I claim this bullet" note. Day ends at 09:50.
The envelope proves a heavy theme day fits in under three hours with two breaks — there is no excuse for a load-bearing day to die to a work schedule.

**What a good log row looks like (read once, then never re-read):**
Good: "DAY 3 — blocks 03/04/02 — 13-12=4 13-09=3 13-18=4 ; FT pool 34/40 ; 14-05 needed +24h on the STS row ; plan-apply narration 4 ; would I claim the IAM bullet: no yet". Bad: "DAY 3 — did policy stuff, felt better". The good row is uglier and useful: every number is a decision input for DAY 7 and DAY 14; the bad row is a feeling, and a feeling cannot be scored, scheduled, or defended. If a row cannot be written, the day's scoring was skipped, not the day.

---

## 3. DAYS 6–14 — THE MID-CAMPAIGN WINDOWS

Nine days, four windows, then one diagnostic reset. Each window is ONE loop run at saturation; spreading them would dilute the loop, and dilution is how forgetting wins a war room.

| Window | Days | Blocks | Focus | Guardrails |
|---|---|---|---|---|
| WINDOW A — first mock-correction cycle | DAY 6 | BLOCK 05 (ROUND 2 R live-debug, INC 27 + composite 24/25, FT-160 method) | Narration order: symptom → scope → hypotheses → checks → evidence → root cause → fix → verify → escalate → prevent, with no 60s silence | AI-grade the FULL transcript tonight; the MUST FIX list is the only plan for DAY 7 — nothing new gets added |
| WINDOW A — the +24h debt | DAY 7 | BLOCK 01 (the exact fumbled incident lines), BLOCK 04 (only the FT rows that cost points on DAY 6) | Re-drill the fumbled nodes at full speed with no notes, per the 14 protocol | The debt is narrow by design: re-drilling everything is dilution; re-drilling nothing is fantasy |
| WINDOW B — Q-bank saturation | DAYS 8–9 | BLOCK 04 twice daily (2× ~15 draws to cross all 60 FT), BLOCK 03 for every FT scored <4, BLOCK 02 secondary chains | Split-grade rule (18 §1.7): shape every answer, then byte-exactness in the weekly batch; the <4 write tasks are the batch | A 4/5 FT is re-drawn, not re-read; volume is the point, silence is the enemy |
| WINDOW C — incident corpus | DAYS 10–11 | BLOCK 01 over the four archetypes: DAY 10 = one narrated pass per archetype (A reachability, B identity, C state, D delivery); DAY 11 = cold draws, name the archetype first, then the FT-160 run | Pattern recognition beats memorized story; the archetype call is the first scored move | Every incident ends with a one-line prevention statement (12 house style); the blank incident page (18 §4.3) is the scratch tool |
| WINDOW D — resume + behavioral + design | DAYS 12–13 | BLOCK 06 (ROUND 4 B strike), BLOCK 02 (14-14, 14-13), BLOCK 05 (ROUND 3 S design or ROUND 5 H hybrid), ELEVATOR five reps per day | Hostile doubling-down probes; claim-level honesty under fire; system design narrated with the spine as the frame | LIE-DETECTOR pass on every bullet that surfaced in rounds — a claim that cannot cite a real session is downgraded, not defended |
| MID-POINT RESET — diagnostics | DAY 14 | BLOCK 05 (ROUND 1 T gauntlet under protocol), BLOCK 08 (scoreboard read-back) | Read all nine days' log rows backward; pick the taper intensity: which windows worked, which red rows carried | The midpoint score is a decision input, not a grade on you — it sets the DAYS 15–21 variants and nothing else |

**Window rules:**
- Windows run one at a time. Starting WINDOW B on DAY 8 while DAY 6's debt is still open is the single most common campaign failure — close the loop, then move.
- A window that fails its focus is a scoring event, never a reset: the window is re-armed at +24h on DAY 14 if needed, per 18 §6.4.
- Special missions (section 7), if activated, slot into the windows they map to — they never earn their own window at the taper's cost.

---

### QC CHECKLIST — DAYS 6–14
| # | Check | Status |
|---|---|---|
| 1 | Nine days covered in six table rows (four windows, the +24h debt day, one reset) | PASS |
| 2 | Each window names ONE loop run at saturation, per the load-bearing principle | PASS |
| 3 | WINDOW A uses ROUND 2 R's real incident set (INC 27 + composite 24/25) and the FT-160 method | PASS |
| 4 | The +24h debt day re-drills ONLY fumbled rows (14 protocol, 18 debt rule) | PASS |
| 5 | WINDOW B covers the full FT-101..FT-160 range through random draws | PASS |
| 6 | WINDOW C uses all four incident archetypes with the archetype-first rule | PASS |
| 7 | WINDOW D cites rounds 3/4/5, chains 14-13/14-14, ELEVATOR, and the LIE-DETECTOR | PASS |
| 8 | DAY 14 is a diagnostic (ROUND 1 T + scoreboard read-back), not a new study day | PASS |
| 9 | Window rules close the open-debt failure mode explicitly | PASS |
| 10 | No emojis; no TODO/placeholder phrase; fencing in this section balanced or absent | PASS |
| 11 | Every row names a scoring/log artifact returned to the day log | PASS |
| 12 | The mid-point score is framed as a taper-intensity input, matching 18's decision logic | PASS |
| 13 | SELF-VERIFY — ROUND 1/2/3/5 IDs, INC 24/25/27, FT-160, and chains 14-13/14-14 all resolve to real sibling rows | PASS |

VERDICT: **GO.** Nine days burn the loops at saturation in the order the war room already proved, and DAY 14 turns nine log rows into a taper decision.
NEXT POINTER → DAYS 15–21: the taper de-loads what the mid-campaign loaded.

**What each window is really graded on:**

**WINDOW A (DAYS 6–7) — the first mock-correction cycle.** DAY 6 is ROUND 2 R, the live-debug simulation: INC 27's rollout-stuck incident with the FT-160 method, graded on narration first and diagnosis second. The AI-grade happens the same night; the scorer's job is to find where the FT-160 order broke, because a broken order is a fixable knob and a wrong fact is a bigger one. DAY 7 is narrow by design — only the fumbled lines are re-drilled: the same incident excerpt, no notes, full speed. The window's pass condition is not a score, it is a narrower DAY 7 than DAY 6: the debt must shrink every cycle or the loop is not correcting.

**WINDOW B (DAYS 8–9) — Q-bank saturation.** Two days of volume to cross all 60 FT entries at least once and to hit the SA range by draw. The split-grade rule is the discipline: every answer is shaped out loud within the minute, then the byte-exactness pass lands in the weekly batch, not in the flow of the draw. Every FT scored under 4 writes itself into BLOCK 03 the following day — the conversion rule is what makes volume actually stick. The block discipline: a 4/5 answer is re-drawn, never re-read; re-reading is the passive trap.

**What the WINDOW B batch looks like (a worked three-row slice of the tracking sheet):**

```
FT ID   SCORE   WRITE TASK (BLOCK 03 TOMORROW)      CHAIN ROW (+24h)
FT-107  3/5     refused-vs-timeout TCP states      14-02 timeout rows
FT-125  4/5     re-draw only, no write              none
FT-150  3/5     pipeline stage graph from memory    14-09 pipeline rows
```

The batch proves the conversion rule is mechanical: a score is never argued with, only converted. Three rows like this per day is the campaign's entire WINDOW B deliverable.

**The glass-box run (WINDOW A only, once):** one narration performed while a person or the recording is watching the clock, not the answer. The single thing this run measures is whether the FT-160 order survives the presence of an audience: the sequence is the grade, the silence between steps is the leak, and the run's result decides whether DAY 7's re-drill is method-shaped or fact-shaped. If the order collapsed with the audience, re-drill the order itself — facts were never the failing layer.

**WINDOW C (DAYS 10–11) — incident corpus.** DAY 10 narrates one pass per archetype, so the four failure families cement: reachability (A), identity/authorization (B), orchestration/state (C), delivery (D) — the archetype call is the scored move because it is the scope move. DAY 11 is the cold draw: any of the 30, archetype first, FT-160 order second, prevention line last. The blank incident page (18 §4.3) is the scratch tool for every narration. Pass condition: the candidate-voice stays on the method even when the incident is unfamiliar — recognition, not memorized story.

**WINDOW D (DAYS 12–13) — resume + behavioral + design.** BLOCK 06 with ROUND 4 B's hostile strike across all 18 bullets, the LIE-DETECTOR pass on anything that wobbled, the ELEVATOR five reps a day, chain 14-14 every day, and 14-13 system design narrated with the spine as the frame on DAY 12 or DAY 13. Pass condition: every claim spoken at exactly its earned claim level — a bullet that survives hostile probing at PRACTICED is stronger than one that bloats to DESIGNED and breaks on the follow-up.

**DAY 14 — MID-POINT RESET.** ROUND 1 T under protocol gives the breadth snapshot; BLOCK 08 reads nine log rows backward. The output is a two-line decision: which two red rows ride into the taper, and which taper variant (normal / light / heavy) DAY 15 starts from. The midpoint score decides the taper; it never re-opens a window.

**The AI-grading prompt (the fixed rubric fed to the grader after every mock run):**

```
Grade this transcript on the seven axes of 17-mock-interviews, hard:
knowledge, structure, narration/cadence, claim honesty, recovery, speed,
and listening.
For every axis: a 0-5 score, one sentence of evidence QUOTED from the
transcript, and exactly one MUST FIX in the shape of a drill, not a
feeling. The MUST FIX must name the sibling file and session ID it maps
to (12 INC NN, 15 FT-NNN, 14-0N, 13-NN, 16-NN, or round 1-6).
Score the tape verbatim. Never credit intent. A claim of a lab that did
not run in the transcript is a claim-level violation: stamp it LIE and
route it to the 16-resume-defense downgrade rule.
```

The rubric is fixed because the grading has to stay one shape across all 21 days; a moving rubric is a moving target, and a moving target cannot be beaten. Every MUST FIX that names a session ID is exactly the input DAY 7, DAY 8, and the taper need.

**The incident deck (how the 30 INCIDENT slips are built for BLOCK 01):**

| Archetype | Slips in the deck | The discrimination each deck-slot tests |
|---|---|---|
| A — Reachability | INC 01 conn refused, INC 02 timeouts/empty endpoints, INC 03 NXDOMAIN, INC 05 expired cert, INC 08 ingress 404 | refused vs timeout; NXDOMAIN vs resolver down; probe path vs workload health |
| B — Identity/Authorization | INC 09 S3 deny, INC 10 Forbidden, INC 11 assume-role, INC 12 secret mount, INC 14 ECR push | explicit Deny vs allow; role chain; secrets-path vs creds-path |
| C — Orchestration/State | INC 16 CrashLoop, INC 17 ImagePull, INC 18 Pending, INC 19 OOMKilled, INC 20 readiness 404, INC 21 PVC, INC 22 state lock, INC 23 drift | run-state discriminator; scheduling vs image vs storage vs IaC state |
| D — Delivery | INC 24 CI-vs-local, INC 25 stale layers, INC 27 rollout stuck, INC 28 rollback, INC 29 same-tag, INC 30 leaked secret | artifact identity; tag vs digest; rollback vs forward-fix; secret hygiene |

Deck construction is fixed once at DAY 1 and never edited mid-campaign — editing the deck is how memorized-by-accident happens. Cold draws pull one slip per archetype in WINDOW C and one slip total otherwise.

**A worked Q-bank conversion (LOOP B end to end, so the debt shape is clear):**
1. DAY 8 draw: FT-107 (Networking, L2, refused vs timeout). Answer starts clean, then stalls on the timeout half.
2. Score 3 — shape held, mechanism half-missing. The 0-5 is the event; the stall is the fact.
3. Conversion per the rule: tomorrow's BLOCK 03 gains the write task "the refused-vs-timeout TCP state diagram from memory" (sourced to NET.P0.2), and tomorrow's BLOCK 02 carries chain 14-02's timeout rows in the secondary pass.
4. Re-draw on DAY 9: answered clean, score 5. The +24h row closes. The loop is complete when the score, the write, and the re-draw all moved — a re-draw that repeats the score is a debt that keeps its date.

---

## 4. DAYS 15–21 — THE TAPER

Reset, light recall, resume polish, sleep, prev-day relaxation. The taper's spine (18 §4): risk closes before the room opens. From DAY 15 the only artifact allowed near your eyes is the cram sheet and the note-card — the entire 20-file system shrinks to two pages, on purpose.

| Day | T-minus | Theme | Blocks | Guardrails |
|---|---|---|---|---|
| DAY 15 | T-7d | The cram sheet + LAST full scored round | BLOCK 08 (build the cram sheet, 18 §4.2), BLOCK 05 (ROUND 5 H hybrid) | Anything not on the cram sheet is out of scope from this hour; the cram sheet is READ-ONLY from DAY 20 |
| DAY 16 | T-6d | Resume polish, no new content | BLOCK 06 (bullet strike without notes), ELEVATOR five reps | No new material; only polish, claim verification, and the LIE-DETECTOR |
| DAY 17 | T-5d | Light recall | BLOCK 02 (green chains only, one row each), BLOCK 03 (two tasks max) | Hard stop at 60 minutes; the load goes DOWN, never up |
| DAY 18 | T-4d | Recall, not research | BLOCK 04 (six FT, spoken only), cram-sheet read | No write tasks, no mock, no new sources; speaking beats reading |
| DAY 19 | T-3d | The method day | BLOCK 01 (one incident, FT-160 narration only), BLOCK 02 (14-12), blank incident page printed (18 §4.3) | One scare run on purpose, then the day ends; this is the last full narration |
| DAY 20 | T-2d | The full dry-run of the final 24h | Inter-section 5 walk-through rehearsed once; cram sheet read-only; sleep lock starts | 8+ hours of sleep tonight; the walk-through is logistics, not study |
| DAY 21 | T-1d | The night before | Clothes, bag, note-card, blank page, ONE cram-sheet read, early dinner, sleep plan | The read stops at 20:00; the note-card is the last page your eyes touch; nothing new is opened |

**Taper rules (from 18, non-negotiable):**
- Never study a scored item on interview day — recognition and recall blur under adrenaline; the morning reads the cram sheet and speaks the ELEVATOR, nothing else.
- A missed technique date during taper is a scoring event and a debt row, never a reset; the taper does not stretch to hide it.
- Rest is a scheduled block of the taper, not a lifestyle note: the sleep lock that starts at DAY 20 is the final study block.

---

### QC CHECKLIST — DAYS 15–21
| # | Check | Status |
|---|---|---|
| 1 | Exactly 7 day rows covering T-7d down to T-1d | PASS |
| 2 | Every taper theme named (reset, light recall, resume polish, sleep, prev-day relaxation) appears in a row | PASS |
| 3 | DAY 15 builds the cram sheet (18 §4.2) and runs the last scored hybrid (ROUND 5 H) | PASS |
| 4 | DAY 19 is the final FT-160 narration with 14-12 and the blank incident page (18 §4.3) | PASS |
| 5 | DAYS 20–21 restrict reading to the cram sheet and note-card; nothing new is admitted | PASS |
| 6 | Sleep lock (8+) is dated at DAY 20, not implied | PASS |
| 7 | The no-scored-item-on-interview-day rule from 18 is restated in spirit | PASS |
| 8 | A missed taper date is a scoring event with a debt row, matching 18 §6.4 | PASS |
| 9 | No emojis; no TODO/placeholder wording; no unpaired fence markers | PASS |
| 10 | Every row carries a guardrail tied to a real sibling rule or section | PASS |
| 11 | De-load monotonicity is enforced (load only ever shrinks from DAY 15) | PASS |
| 12 | Block citation is consistent with sections 1 and 2 | PASS |
| 13 | SELF-VERIFY — round/chain/incident IDs, cram-sheet and incident-page sections all resolve to real sibling rows | PASS |

VERDICT: **GO.** The taper converts nine days of heavy load into seven days of deliberate de-load; the scoreboard is frozen and the only score that matters is spoken in a room.
NEXT POINTER → the final 24 hours, hour by hour, where the cram sheet and note-card do the only remaining work.

**What the taper actually does, day by day:**

**DAY 15 (T-7d):** the cram sheet is built once and is the last new document of the campaign — one page, six bands: ELEVATOR, the spine, the FT-160 order, exit-code table, the two weakest verified facts, and the STAR anchors. ROUND 5 H is the last scored full round; its must-fix list is the final content that may enter the cram sheet, and anything else is out of scope from this hour. The cram sheet becomes READ-ONLY at DAY 20; edits after that are forbidden by rule, not by willpower.

**DAY 16 (T-6d):** resume polish with no new content. BLOCK 06 runs cold — bullets struck without notes, claim levels re-stamped, the LIE-DETECTOR pass across every bullet that surfaced in rounds. This is the last day the resume is allowed to change; from here it is what it is, and the note-card needs to match it line for line.

**DAY 17 (T-5d):** light recall only. Two green chains, one row each, standing; two write tasks max; a hard stop at 60 minutes. The load has one direction from this day forward — down. A session that exceeds the cap is logged as a red event, because over-drilling at T-5 is how the taper fails upward.

**DAY 18 (T-4d):** recall, not research. Six FT questions, spoken only, no write tasks, no mocks, no new sources; the cram sheet gets its single permitted read. Speaking beats reading here: the voice, not the eyes, is what has to be ready.

**DAY 19 (T-3d):** the method day. One incident, FT-160 narration only, chain 14-12, and the blank incident page printed. This is the intended scare run — one full narration on purpose to prove that the method holds cold — and then the day ends. It is the last full narration of the campaign, and it should feel easy by now.

**DAY 20 (T-2d):** the full dry-run of the final 24 hours — the logistics rehearsed once from the section-5 table; the sleep lock starts tonight at 8+ hours. The walk-through is mechanics, not study: route, bag, clothes, chargers, water, the note-card shell. From here the cram sheet is read-only and the only writing allowed is the note-card.

**DAY 21 (T-1d):** the night before. Clothes and bag final, note-card drafted, blank page printed; the single cram-sheet read stops at 20:00, dinner is early and known, and the note-card is the last page your eyes touch. Nothing new is opened — not one file, not one tab. The campaign's last act of restraint is also its most important one.

**The frozen scoreboard (DAY 15 onward, the only scoring artifact still allowed to exist):**

```
THEME          LAST SCORE    VERDICT      CARRIES INTO TAPER?
spine rely      5 / 5        green        no — frozen
FT pool         42 / 50      green        no — frozen
chains          8 / 14       two red      yes — but re-drill is FORBIDDEN morning-of
incident method 4.5 / 5      green        no — frozen
resume claims   18 / 18      green        no — frozen
```

Frozen means closed: from DAY 15 a score is a fact about the campaign, not a to-do. The only red row that may travel is a named chain row whose re-drill lands before DAY 19 and NEVER on the morning of the interview — anything opened at T-12h is a debt that cannot accrue usefully and can only shake the green rows beside it.

**Taper interruption protocol (when the taper itself is interrupted, per 18 §4.5):**
- If one day is lost (travel, work, family): the taper does not stretch; the DAY read just shifts one slot. DAY 20's sleep lock and DAY 21's restraint are the two dates that never move — they are the campaign's final content.
- If the interview is rescheduled by the company: the taper holds at its current position for at most 48 hours, then Day 15's cram sheet is rebuilt once with the new date and the windows do not re-open. A campaign that re-opens load-bearing days for a late interview forgets more than the delay was worth.
- If a scored item breaks during taper (e.g. an FT fumbled on DAY 18): it becomes a cram-sheet line IF it fits one line, and it is never re-drilled — the day tables from DAY 19 onward are already forbidden to question.

**The taper variants (chosen at the DAY 14 midpoint, unchanged after):**

| Variant | When chosen | What changes from the base taper |
|---|---|---|
| NORMAL | mid-point shows green rows riding the taper | base taper as tabled, all seven days |
| LIGHT | mid-point shows 1-2 red rows but the method holds | DAY 17 gains one extra green chain; DAY 18 keeps six FT; nothing else moves |
| HEAVY | mid-point shows a red theme or an unstable mock | DAY 16 becomes a full resume-strike + one scored narration; DAY 19 stays the last narration; the sleep lock stays absolute |

The variant is selected once and locked — taper mid-course revisions are how candidates trade rest for panic and lose both. Whatever the variant, DAYS 20-21 are byte-identical in all three: sleep, night-before restraint, and the note-card.

---

## 5. THE FINAL 24 HOURS AND THE DAY

Hour-by-hour from T-24h to post-interview. This is the last schedule in the war room, and it is a logistics sheet, not a study sheet: every earlier hour was spent so this night and morning have nothing left to prove.

| Time | Phase | The move | The discipline |
|---|---|---|---|
| T-24h | RE-ZERO | Set your watch and phone clock to interview time; the countdown is now literal. Confirm room, route, and buffer in the calendar | The plan is a plan, not a hope; the buffer is fixed at scheduling time, not discovered during the walk |
| T-18h → T-14h | EVENING | Pack: layered clothes, chargers, water bottle, printed cram sheet, blank incident page, note-card drafted in pencil | The bag is packed tonight so the morning has zero decisions; every decision made under adrenaline is a mistake looking for a host |
| T-14h → T-12h | LAST SECURE READ | One read of the cram sheet, then one read of the note-card. No chain recitation aloud | Talking through chains reshapes the adrenaline target list; the cram sheet is consumable, the chains are not open for business |
| T-12h → T-10h | TAPE-OFF | Lights off; phone outside the room. If the tape loops, the note-card on the nightstand is written permission to stop | The sleep block is the last study block; there are no exceptions for "one more look" — that look is exactly what costs the morning |
| T-10h → T-2h | THE SLEEP BLOCK | 8 hours protected, fixed start and end | Wall-clock, not alarm-clock hope; the interviewer walks in on a rested voice, not a heroic one |
| T-2h | WAKE, RE-ZERO | Sit up, water first, light real breakfast, no sugar spike. No recall drills of any kind | Morning recognition-vs-recall: you read the cram sheet and speak the ELEVATOR, nothing else (18) |
| T-90m | THE NOTE-CARD | Finalize the index card, six lines: ELEVATOR (16), the spine (00 §5), the FT-160 order, two red-flag facts (exit-code math 137 = 128+9; dmesg + vmstat leg), a STAR anchor list | The note-card is the whole war room in your pocket; the 550 KB playbook does not travel to an interview |
| T-60m | ARRIVAL | Leave with the full buffer; walk the route in your head once; phone on do-not-disturb | Arrival caffeine is fine; arrival phone-scrolling is not — the feed is a distraction engine and the corridor is silent |
| T-45m → T-30m | THE ROOM | Water within reach, watch on the desk, note-card flat, blank incident page for scratch. Narration/energy: one quiet 30s ELEVATOR and one L1 chain line at conversational volume | You are switching registers from reading to speaking; one cycle of the vocal engine, then voice is voice |
| T-15m | THE WALK | Stand, shoulders, feet on floor, two slow breaths out; re-read the note-card flat, then turn it face-down | The physical engine-start is what shows up in the first answer's cadence; skipping it reads as tension |
| T-5m | FIRST-ANSWER FRAMING | The cold-open shape below is loaded and ready; nothing else is in working memory | Never open with "I'm a DevOps engineer and..."; open with what you can prove |
| T-0 | THE ROOM | The interview. Water on reach, the note-card for the pause, FT-160 order for any technical question you need 15 seconds to scope | The pause is a feature: scope aloud, then answer; silence past 60 seconds is the only true failure mode |
| +15 min | THE BREAK | If a question went sideways, it becomes one line in the +24h debt and is released | Rehearsing the answer you just gave badly costs the next two questions; the post-mortem waits |
| +60–90 min | POST-INTERVIEW DEBRIEF | 10 minutes, three columns: what was asked, where the method held, where it broke; written to the day log | This log row seeds the next campaign's DAY 1 — a war room always loops into itself |
| +24h | THE RE-DRILL | The +24h re-drill of fumbled answers, per the 14/18 protocol — the loop applies after the interview too | A closed loop re-opens cleanly for the next target instead of decaying into a bad memory |

**The cold-open shape (the 30-second first answer):**

```
CLAIM -> EVIDENCE -> ONE LIMIT

CLAIM      the one-sentence answer ("the pod was never Ready, so the Service had
           zero endpoints and the request timed out")
EVIDENCE   the discriminating check that proved it ("get endpoints returned empty,
           readiness probe 404 on the health path")
ONE LIMIT  the honest boundary ("I diagnosed it in a kind cluster on a local box,
           not against a live multi-AZ ALB")
```

The shape is CLAIM → EVIDENCE → ONE LIMIT because it is the FT-160 method collapsed to one breath: statement, proof, boundary. It works on theory questions, incident questions, and the resume openers alike, and its third line is the honesty the claim levels (16) exist to protect.

**What the 30-second ELEVATOR sounds like (the shape spoken, from file 16's asset):**
"I started as a Linux operations engineer and spent the last year and a half inside the pipeline-to-production spine: I wrote the runbooks a 3 AM page wakes up to, dumped a terminal to a root cause using the method, and shipped the push-the-button part of a live pipeline. My ceiling is a kind cluster on a local box and a read-only AWS account — I say that plainly because I would rather prove a small claim than defend a big one." The elevator is the cold-open on the resume register: claim, evidence, limit, in one breath. It is rehearsed until the limit line comes out as a strength, not a caveat.

**Water:** a full bottle at hand and the first sip taken in the pre-room minute, not mid-answer. A dry mouth reads as nerves and costs cadence; the refill decision is made before the interview, never during.

**The five red-flag facts worth a card line each (all verified in the siblings):**

| Fact | The mechanism it names | Source |
|---|---|---|
| exit 137 = 128+9 | OOMKilled SIGKILL, not an app exit | INC 19, verified |
| connection refused vs timeout | RST answered vs SYN unanswered; empty endpoints time out | INC 01/02, NET.P0.2 |
| NXDOMAIN ≠ DNS down | the resolver answered; the name is absent | INC 03 |
| readiness 404 unsets endpoints | container healthy but never Ready → no traffic | INC 20 |
| tag CACHED vs no-cache digest | same tag, different artifact | INC 25, CICD.P0.5 |

These five transfer across more interview questions than any five chapters; if the note-card has room for nothing else, these are the lines it keeps.

**The three stalls and the one move each (loaded at T-5m):**
- Stall: you know the fact but the word will not surface. Move: pause, re-scope aloud from the question, name the layer the fact lives in — the answer follows the layer, not the hunt.
- Stall: you genuinely do not know it. Move: the honest ONE LIMIT plus the check you WOULD run — "I would start at the probe, then the Service endpoints" is an answer; "I don't know" alone is not, and a fabricated lab is worse than both.
- Stall: nerves, 20 seconds in. Move: the cold-open reload — restate the claim you can prove, then EVIDENCE; the first line back is always a claim, never an apology.

**A worked morning (from the alarm to the first question):**
- 06:00 alarm, one snooze max — a second snooze is the start of the tape.
- 06:05 sit up, glass of water on the nightstand, no phone pick-up before the first glass.
- 06:15 light real breakfast (protein, fruit, no sugar spike), water refill.
- 06:45 the note-card written fresh in ink on the drafted shell: six lines, no more.
- 07:15 dressed, bag checked once against the T-18h packing list.
- 07:30 out the door with the full buffer; phone on do-not-disturb from the doorway.
- 08:00 in the room, watch on the desk, water placed, note-card flat.
- 08:15 the vocal warm-up: one 30-second ELEVATOR and one L1 chain line at conversational volume.
- 08:25 the walk: feet, shoulders, two slow breaths out, note-card face-down.
- 08:30 the first question — and the shape loaded at T-5m answers it.

The whole sequence is mechanical; nothing in it requires a decision, because decisions under adrenaline are the mistakes the DO NOT list was written to prevent.

**The three question registers — the same shape, three volumes:**

- THEORY register ("what is the difference between X and Y?"). Use the cold-open shape and stop; CLAIM → EVIDENCE → ONE LIMIT is a complete theory answer in 45 seconds, and a theory answer past 90 seconds is a monologue.
- INCIDENT register ("here is a system, it is broken"). Use the FULL FT-160 order, scoped aloud first. The cold-open is the diagnosis sentence; the evidence is the discriminating command; the limit is what you verified and what you did not.
- DESIGN register ("design a pipeline for a 3-tier app"). Use the spine as the frame — walk the hops, name the decision at each hop, and close with the ONE LIMIT of your environment (the box sized what it can prove). A design answer narrated with the spine reads as senior; a design answer that lists components reads as a list.

The registers matter because the interview does not announce which volume is coming, but the opening of the question almost always does: "explain" is theory, "it's broken" is incident, "design" is spine-walk. Loaded at T-5m, all three are one shape at three volumes.

**The note-card, filled (the T-90m line it has to hold):**

```
FRONT                                BACK
ELEVATOR: 18 months ops, runbooks,   RED-FLAG FACTS:
  root-cause at 03:00, 137=128+9, 143=conn refused, dmesg+vmstat
  16-02/12-INC02/30.                 FT-160: READ SCOPE RANK CHECK
SPINE:  Git->CI->Docker->registry-   EVIDENCE FIX VERIFY PREVENT
  >EKS->Ingress->ALB->Route53        STAR ANCHORS: 16-09 (incident),
  with INC 02/16/20/27 at each hop   16-18 (runbooks), 13-10 (pipeline)
METHOD: scope aloud, hypothesis      THE LIMITS i may say: kind cluster,
  first, then command, then fix      local box, no live rotation
```

The card is six lines because six lines is what a working-memory under adrenaline can reach without hunting. Anything that needs a seventh line gets dropped — the card's size is the discipline, not its completeness.

---

### QC CHECKLIST — THE FINAL 24 HOURS AND THE DAY
| # | Check | Status |
|---|---|---|
| 1 | Hour-by-hour table spans T-24h through +24h, 15 rows | PASS |
| 2 | The sleep block is a fixed, wall-clocked 8h protected segment | PASS |
| 3 | Re-zero is explicit (clock reset, no recall drills, water-first wake) | PASS |
| 4 | The note-card is a defined artifact with six named lines, not a vague page | PASS |
| 5 | Arrival, room, narration/energy, water, the walk, and first-answer framing are each explicit rows or rules | PASS |
| 6 | The cold-open shape (CLAIM → EVIDENCE → ONE LIMIT) is fenced and closed | PASS |
| 7 | Post-interview: +15m release, +60–90m debrief columns, +24h re-drill, and the loop statement | PASS |
| 8 | The note-card's facts (137 = 128+9, dmesg/vmstat leg) cite real sibling content | PASS |
| 9 | No emojis; no TODO/placeholder wording; balanced fence markers as written | PASS |
| 10 | The morning read rule (cram sheet + ELEVATOR only) is restated in spirit from 18 | PASS |
| 11 | Every row states a discipline, not a wish — each can be failed and observed | PASS |
| 12 | The FT-160 method is the stated scope tool for technical questions | PASS |
| 13 | SELF-VERIFY — every fact in the table (rounds, chains, 18 §4.2/§4.3, ELEVATOR, claim levels) resolves to real sibling rows | PASS |

VERDICT: **GO.** The 24 hours are a logistics sheet, not a study sheet — every line removes a decision the room should never have to make.
NEXT POINTER → the DO NOT list: a day unwound in ten seconds by ten mistakes; the list exists to make that impossible by rule.

---

## 6. THE "DO NOT" LIST — DAY-OF DO-NOTS

Twenty rules, written because each one has already cost someone a round. Read them once the night before; on the day they exist to be obeyed, not debated.

1. **No new material after DAY 15.** A blog opened at T-12h is how a strong candidate becomes a shaky one.
2. **No scored-item re-study on the morning.** Recognition and recall blur under adrenaline; the cram sheet and note-card are the whole reading list.
3. **No full mock on T-1 or T-0.** The taper closes risk; a mock reopens it with a scored failure 12 hours before the real score.
4. **No re-drilling of red rows the morning of.** A red row cannot be fixed in three hours, only shaken; a shaken red row leaks into the green rows beside it.
5. **Do not carry the system.** The note-card is the war room in your pocket; the terminal stays home, the PDFs stay on disk.
6. **No caffeine after T-8h.** The sleep block is the last study block, and caffeine is its direct opponent.
7. **No new food on the day.** Interview day is not a cuisine experiment; a known breakfast in, a known breakfast out.
8. **No phone-reading in the waiting room.** The corridor feed is a distraction engine; the note-card flat is the only permitted reading, and only at the pre-room minute.
9. **Do not rehearse the question you just answered badly.** The next question is the one you can win; the post-mortem has a scheduled slot at +60 minutes.
10. **Do not say "I know that" in the answer.** The correction loop proved the difference between knowing and answering; the answer is the proof, the phrase is the leak.
11. **No environmental surprises.** Water, tissue, layered clothing — a 90-minute interview punishes an avoidable comfort gap on a curve.
12. **Do not justify a wrong exit code.** 137 does not want a "well, it's basically..." preface; the mechanism (128 + 9) is the answer, state it first.
13. **No fabricated labs, ever.** The LIE-DETECTOR pass exists because the claim level will be probed past the level you earned; downgrade, do not defend.
14. **Do not answer a design question as a memorized architecture.** The spine is the frame and the 3-tier app is the build; narrate the frame, then build.
15. **No silent thinking for 60 seconds.** The room grades narration, and narration is trained; scope aloud in the FT-160 order instead.
16. **Do not skip the walk.** The engine-start shows up in the first answer's cadence, and the room notices cadence first.
17. **Do not fight the interviewer's word choice.** "You said frontier, I meant branch" costs a whole block; scope the word by restating the question before you answer.
18. **No unreachable note-card.** A card you can find beats a card in a bag; it lives flat on the desk from the pre-room minute.
19. **No alcohol the evening before.** The sleep block is literally the last scored session; its grade is the first answer you give in the morning.
20. **Do not let the +24h post-interview debrief slip.** The loop that closed the war room is the loop that opens the next campaign; a skipped debrief is a debt left accruing.

**Why the list is framed as do-nots, not rules:** a rule is something a nervous candidate negotiates with; a do-not is a boundary the day does not cross. Every item above maps to a sibling fact — exit-code math (12), claim levels (16), narration grading (17, 14), the taper rules (18), the cold-open (this file's section 5). If a do-not ever feels unfounded, trace it to its source row; if no source row exists, the do-not has no right to be on the list.

---

### QC CHECKLIST — THE DO NOT LIST
| # | Check | Status |
|---|---|---|
| 1 | Exactly 20 do-nots present | PASS |
| 2 | Each rule is actionable and observable — it can be failed and it can be caught | PASS |
| 3 | Rules 1, 3, 4, 5 enforce the taper and note-card-only discipline from sections 4–5 | PASS |
| 4 | Rule 2 restates 18's no-scored-re-study-on-interview-day rule | PASS |
| 5 | Rule 10 ties to the AI/mock-correction loop's core finding (knowing ≠ answering) | PASS |
| 6 | Rule 12 cites the verified exit-code math | PASS |
| 7 | Rule 13 restates the 16 claim-levels honesty rule | PASS |
| 8 | Rule 14 ties design answers to the spine from BLOCK 07 | PASS |
| 9 | Rule 15 ties the narration rule to the FT-160 method | PASS |
| 10 | Rules 17–18 manage the in-room behavior the tables cannot reach | PASS |
| 11 | No emojis; no TODO/placeholder wording; no fence markers to imbalance in this section | PASS |
| 12 | Rule 20 closes the loop forward (post-interview debrief becomes the next campaign's DAY 1) | PASS |
| 13 | SELF-VERIFY — every referenced artifact (cram sheet, note-card, ELEVATOR, LIE-DETECTOR, claim levels, FT-160) resolves to real sibling content | PASS |

VERDICT: **GO.** Twenty cheap rules protect an expensive asset; the day cannot be won by adding, only by subtracting the ten-second mistakes.
NEXT POINTER → the SPECIAL MISSIONS window, a way to aim part of the campaign at a named target without breaking the taper.

---

## 7. SPECIAL MISSIONS WINDOW

Run only when a company is a strong, named target — the moment a real JD or a real product exists. Every mission is a template layered onto the base schedule; nothing here is executable without a target `(modeled reference — not executed)`. Missions amplify blocks; they never replace sleep, the taper, or the note-card, and the taper is immune to missions by rule from DAY 15.

| Mission ID | When it applies | The mission | Maps to | Placement in the 21 days |
|---|---|---|---|---|
| MISSION 01 | Platform/product company with public docs | Read the product docs (not marketing), map the product's stack to the spine, produce ONE page "the product through the spine" | BLOCK 07 (spine walk gains a product leg), BLOCK 04 (domain vocabulary enters the random draw) | DAYS 3–5 evening slot, one hour, before WINDOW A |
| MISSION 02 | GitOps shop (ArgoCD in the JD) | Re-drill CICD.P1.2 (09, model), INC 26 OutOfSync (12), chain 14-09; write the reconcile story in 90s | BLOCK 03 (new write task from memory), BLOCK 04 (a GitOps question added to every draw), BLOCK 02 (14-09 reruns) | DAY 5 + inside WINDOW A DAY 7 debt |
| MISSION 03 | AWS + Terraform shop | Zero-in the AWS/TF surface: chains 14-05/14-08, INC 09/11/13/14/22/23, WRITE 13-09/13-12/13-18; every design answer lands on the Route53 → ALB span | BLOCK 01 (identity + IaC incident cluster), BLOCK 02 (14-05/14-08), BLOCK 03 (13-09/13-12/13-18) | DAY 3, plus WINDOW C DAY 10 archetype-B pass |
| MISSION 04 | Observability-centric product (SLO culture) | Ownership pass on the rear half of the spine, OBS FT set drawn first, the PromQL write task (13-11) run twice, the SLO/DORA story fixed as a 90s narration | BLOCK 07 (rear half), BLOCK 04 (OBS-first draw), BLOCK 03 (13-11), BLOCK 02 (14-10) | DAY 5, plus WINDOW B DAY 8 |
| MISSION 05 | Incident-heavy on-call culture | The corpus window becomes BLOCK 01 everywhere: every incident narrated with the blank incident page rule (18 §4.3); the "3am runbook" (16-18) rehearsed as a spoken artifact | BLOCK 01, BLOCK 02 (14-12), BLOCK 06 (16-18 runbook bullets) | WINDOW C DAYS 10–11, at full intensity |
| MISSION 06 | Behavioral-critical (values-driven culture, senior panels) | BLOCK 06 twice in the residual half-hour, 14-14 every day, the company's stated values mapped to STAR anchors before the note-card is finalized | BLOCK 06, BLOCK 02 (14-14), BLOCK 08 (note-card STAR anchors) | DAYS 12–13, then folded into the note-card at T-90m |

**Mission rules:**
- One mission active at a time. Two missions split a loop and both die.
- A mission adds at most one hour per day and never pushes a window out of its slot; the mission rides the existing block, it does not create a new one.
- The moment a mission's material touches something outside the 18-file corpus, it is labeled exactly that — outside-corpus reading, `(modeled reference — not executed)` until the target exists — and its claims enter the LIE-DETECTOR like every other claim.
- If the target company calls an interview, the mission becomes the current window and the DAYS 15–21 taper guardrails override it from that hour.

**Per-mission notes (each mission's exact target of proof):**

MISSION 01 — the deliverable is the ONE-page product-through-the-spine sheet, and its proof is a 60-second narration that maps the product's stack onto the spine onto a real sibling fact (for a database product, the ALB health-check hop; for a CDN product, the Route 53 edge). If the sheet cannot cite a sibling file, the mission is outside-corpus reading and is labeled as such.

MISSION 02 — ArgoCD proof is the 90-second reconcile narration: desired state in Git, the App CR in the cluster, sync vs out-of-sync, self-heal loop, and why INC 26 would not self-heal. It rests on CICD.P1.2 (modeled in 09) and INC 26 (modeled in 12), so the narration is capped at what those source rows prove.

MISSION 03 — AWS/Terraform proof is one circuit: policy evaluation order on a real denied call, then the state-lock story from INC 22 and the destroy/recreate trap from INC 23, closed with the plan-apply narration verb fit from 13-09/13-12/13-18. Every design answer is required to land on the Route53 → ALB span so the spine stays the door.

MISSION 04 — observability proof is the SLO/DORA narration grounded in OBS.P0.x and CICD.P2.3, with a PromQL line (13-11) written from memory twice: once before DAY 5 and once after WINDOW B, to prove the decay curve is flat.

MISSION 05 — incident-culture proof is the 3am runbook (16-18) spoken, not read: symptom-first, discriminating first check, one-action prevention, and the honest "who else owns this" boundary. Every incident in the corpus window ends with its prevention line aloud.

MISSION 06 — behavioral proof is the values map itself: each stated company value matched to a STAR whose evidence cites a REAL session, with the claim level stamped. A value without a citable STAR is a value that does not go on the note-card.

**Choosing a mission (the decision is one line, made once at DAY 1):**
A mission is chosen when the target is named and the JD can be answered by blocks — otherwise no mission runs, and the base schedule is the whole plan. Read the JD twice: circle every concrete noun (ArgoCD, Terraform, Prometheus, on-call, SLO). The circled noun matches the mission whose Maps-to column already contains that block — that is the mission; every other mission is an un-chosen template and costs nothing to leave closed.

**Anti-missions (refuse these, they are not missions):**
- A mission that adds a new subject outside the corpus for "coverage" — outside-corpus boots are exactly the claims the LIE-DETECTOR hunts.
- A mission that promises to "read their blog" without producing a block output — reading without a scored output is a RED event in another disguise.
- A mission that arrives after DAY 14 — the taper is immune to missions by rule, including good ones; a mission that missed its window waits for the next campaign.

---

### QC CHECKLIST — SPECIAL MISSIONS
| # | Check | Status |
|---|---|---|
| 1 | Exactly 6 missions, each gated on a real, named target company | PASS |
| 2 | Every mission maps to at least one BLOCK ID from section 1 | PASS |
| 3 | Every mission cites real sibling IDs (09 CICD.P1.2, 12 INC 26, 14-05/08/09/10/12/14, 13-09/11/12/18, 16-18) | PASS |
| 4 | Mission material is labeled modeled-reference until a target exists | PASS |
| 5 | The one-mission-at-a-time rule is explicit | PASS |
| 6 | Mission daily cost is capped (≤1 hour, rides existing blocks) | PASS |
| 7 | Taper immunity is explicit: missions never touch DAYS 15–21 | PASS |
| 8 | Outside-corpus claims route through the LIE-DETECTOR rule | PASS |
| 9 | No emojis; no TODO/placeholder wording; no unpaired fence markers | PASS |
| 10 | Placement column references real window/day slots from sections 2–3 | PASS |
| 11 | The map-to-blocks stays consistent (a mission cannot invent a block) | PASS |
| 12 | Mission 06's STAR mapping resolves to the note-card build at T-90m | PASS |
| 13 | SELF-VERIFY — all cited mission IDs and placements resolve to real sibling rows and real day windows | PASS |

VERDICT: **GO.** Six missions convert a named target into amplified blocks without disturbing the campaign's spine; unchosen, they cost nothing.
NEXT POINTER → FINAL QC: the file closes into itself, and the war room re-opens at file 01.

---

## FINAL QC — FILE 20

The last table in the war room grades the file that schedules the war room. Before it, the completion bar the campaign exists to meet:

- By DAY 14 every domain file has been re-touched at least once through a block, and every red row has a logged due date.
- By DAY 15 the cram sheet exists, the scoreboard is frozen, and the note-card's six lines are drafted.
- By DAY 21 the two-page system (cram sheet + note-card) is the only artifact left, because the other twenty were turned into it.

**The sourcing map (where every claim in this file came from — the SELF-VERIFY audit trail):**

| Content in this file | Sourced from | Verified |
|---|---|---|
| exit-code math, incident ladder, archetypes | 12-troubleshooting INC 01–30 | yes, by file search |
| FT ranges and domain split | 15-question-bank FT-101..FT-160 | yes |
| chain list and rotation protocol | 14-attack-chains 14-01..14-14 | yes |
| WRITE task IDs and their sessions | 13-write-without-google TASK 13-NN | yes |
| mock rounds, seven axes, narration tone | 17-mock-interviews Rounds 1–6 | yes |
| claim levels, ELEVATOR, LIE-DETECTOR, bullets | 16-resume-defense 16-01..16-18 | yes |
| cram sheet, incident page, loops, debt rule, lookback | 18-revision §1/§2/§3/§4/§6 | yes |
| the spine, load order, the file map | 00-architecture §5 | yes |
| box facts (RAM, cores, PATH, no sudo) | 09-cicd environment-facts block | yes |

A row that cannot carry a "yes" here has no right to appear in the day tables — that is the same honesty rule the campaign drills, applied to the file that schedules the campaign.

| # | Check | Status |
|---|---|---|
| 1 | Header presents the file as the 20-file capstone with the one-line framing and the two-loop "How it works" text | PASS |
| 2 | DRILL BLOCKS defines exactly 8 blocks (BLOCK 01–08), each with name, real source sessions, target duration, and what it does | PASS |
| 3 | DAY 1–5 table has exactly 5 day rows with theme / blocks / gaps-to-fix / what-to-log | PASS |
| 4 | DAYS 6–14 table covers 9 days in four named windows plus a mid-point diagnostic reset | PASS |
| 5 | DAYS 15–21 table covers the full taper (reset, light recall, resume polish, sleep, prev-day relaxation) with guardrails | PASS |
| 6 | THE FINAL 24 HOURS AND THE DAY spans T-24h → post-interview +24h with sleep, re-zero, note-card, arrival, room, narration/energy, water, the walk, and first-answer framing | PASS |
| 7 | THE DO NOT LIST has 20 day-of do-nots, each actionable and traceable to a sibling rule | PASS |
| 8 | SPECIAL MISSIONS defines 6 target-gated missions mapped to real blocks and real day windows, labeled `(modeled reference — not executed)` | PASS |
| 9 | Every per-section QC is 13 rows with SELF-VERIFY last (7 section QCs + the file QC = 8 tables) | PASS |
| 10 | No emojis anywhere; typography limited to — · → | PASS |
| 11 | Fences balanced — all 9 fenced blocks (phases, two loops, daily-log sheet, cold-open, AI-grader rubric, Q-bank batch, frozen scoreboard, note-card) open and close in pairs; zero imbalance detected | PASS |
| 12 | No TODO / FIXME / placeholder wording; all modeled-only content explicitly labeled; line count within the 700–850 target band | PASS |
| 13 | SELF-VERIFY — every real session ID cited (LINUX/NET/GIT/BASH/AWS/DCK/K8s/TF/CICD/OBS/SEC session numbers, INC 01–30, FT-101–FT-160, chains 14-01–14-14, task IDs 13-01/03/04/05/06/07/09/11/12/18, bullets 16-01..16-18, mock rounds 1–6, 18-revision sections) resolves to a real sibling row, verified by file search at build time | PASS |

VERDICT: **FILE COMPLETE — THE CAMPAIGN IS THE CAPSTONE.** Twelve files of content, four of defense, two of revision, and one calendar: this file ties the war room into a single 21-day loop whose last action — the +24h post-interview debrief — is also its first action, because every future campaign starts from the log row that interview left behind.
NEXT POINTER → **01-linux (the war room closes into itself).** The campaign's very first block is the foundation that never gets to decay; restart the daily loop there.