# 18 — REVISION PLAN

**Knowledge decays on a schedule — beat it with a schedule. Five loops re-expose every studied item at 15min → 24h → 7d → 14d → 30d, each pass through a different activation mode so you recall instead of merely recognize.**

> **The decay model:** recall strength halves roughly on a curve; the plan schedules re-exposure at 15min → 24h → 7d → 14d → 30d per item. Each loop either hits a DIFFERENT angle (write / quiz / teach / debug / design) or a different ACTIVATION MODE so it never degrades into recognition.
> Activation modes: WRITE (13-write-without-google), QUIZ (15-question-bank), CHAIN (14-attack-chains), DEBUG (12-troubleshooting), DEFEND (16-resume-defense), MOCK (17-mock-interviews), TEACH (explain aloud to an imaginary teammate).

This file is the only file in the War Room that says WHAT to re-attend and WHEN. Everything below cites sibling sessions, drills, and scoring gates by their real IDs — no generic "review your notes" instructions. If a task, question, chain, incident, bullet, or round is named, it exists in files 12–17 and you can open it inside sixty seconds.

**The one law this plan enforces:** an item is only "owned" when you can reproduce it cold at +24h AND +48h after the session that taught it (the 48h rule of file 13). The daily loop is the engine, the weekly loop is the auditor, the 7/14/30 day loops are the forgetting-curve backstops, and the taper is the dress rehearsal. Every loop writes its scores to the tracking sheets in Part 7 — a loop that is not logged is a loop that did not happen.

**Two systems, one loop (built in weeks 8+, maintained forever):**
- The FILE CYCLES (this file) tell you what to re-attend, at which offset, in which activation mode.
- The WORKBOOKS (13, 14, 15) already carry their own re-drill ladders — file 13's weekday batch plan, file 14's 4-week drill rotation, file 15's "any FT below 3/5 re-drills". This plan does not replace those ladders; it schedules them into time-boxed loops. When this file and a workbook disagree, the stricter one wins (a "5" in the workbook still lands in the 30-day lane per file 13's graduation rule).

**Why five loops and not one:** a single review pass at any fixed offset produces a classic spaced-repetition curve failure — the interleave is too short (everything re-heats, nothing consolidates) or too long (everything decays before re-exposure). The four offsets in this file (15min / 24h / 7d / 14d / 30d) bracket the forgetting curve for interview material: 15 minutes proves you encoded it, 24 hours separates short-term from working memory, 7 days catches domain fade, 14 days tests mechanism depth, 30 days forces re-integration. Each offset uses a different activation mode so the retrieval cost stays high — retrieval practice that is easy produces little consolidation.

---

## MASTER MATRIX — WHICH ACTIVATION MODE, WHICH LOOP, HOW OFTEN

| Activation mode | Runs in loop | Sibling file sections it pulls from | Frequency |
|---|---|---|---|
| WRITE (write-without-google) | 15-min daily · 1-h weekly · 7d · 14d · taper | 13-write-without-google, TASK 13-01 … 13-26 (Batch 1 = 13-01..13-12 P0, Batch 2 = 13-13..13-26) | 3 tasks daily · full batch weekly · full P0 batch monthly · all 26 at T-7d |
| QUIZ (short-answer + full-treatment) | 15-min daily · 7d · taper | 15-question-bank, FT-101 … FT-160 (60 full treatment) + SA-161 … SA-300 (140 short answer) | 5 picks daily · domain pass at +7d · sweep at T-14d |
| CHAIN (attack-chain oral drill) | 15-min daily · 14d · taper | 14-attack-chains, CHAIN 14-01 … 14-14, WEEKLY DRILL ROTATION TABLE | 1 chain daily · full 14-chain sweep at +14d · L1 sweep at T-7d |
| DEBUG (narrated live incident) | 1-h weekly · 14d · taper | 12-troubleshooting-playbook, INCIDENT 01 … 30 (archetypes A–D: reachability / identity-authz / orchestration-state / delivery) | 1 incident weekly · archetype pass at +14d · 4-incident relay at T-14d |
| DEFEND (resume claim defense) | 1-h weekly · 30d · taper | 16-resume-defense, BULLET 16-01 … 16-18, THE LIE-DETECTOR LIST, THE 30-SECOND ELEVATOR | bullet pass weekly · full 18-bullet sweep at +30d · daily in taper |
| MOCK (scored interview round) | 1-h weekly · 30d · taper | 17-mock-interviews, ROUND 1 (T 45min) … ROUND 6 (F 90min), 7-axis scoring | 1 round weekly · +30d full set re-run · ROUND 6 at T-7d |
| TEACH (explain aloud to an imaginary teammate) | 30d · taper | any completed session in 01–11 (message lens: 00-architecture mental models), plus 10-observability build-up | 1 topic monthly · 1 anchor daily in taper |

**Reading the matrix:** every item that enters your memory gets its first re-exposure inside 15 minutes (WRITE or QUIZ), its survival test at +24h/+48h (file 13's rule, Part 6), its quota pass at +7d (QUIZ), its mechanism pass at +14d (DEBUG + CHAIN), and its top-level integration pass at +30d (TEACH + MOCK). The 1-hour weekly loop runs all four high-touch modes (WRITE, DEBUG, DEFEND, MOCK) so no single week degrades into one activity.

**The recognition trap, named once:** recognizing an answer when you read the file is NOT recall. Every loop in this plan either hides the answer (WRITE), imposes a clock (QUIZ/CHAIN/MOCK), makes you narrate a method (DEBUG), defend a claim (DEFEND), or build the model twice (TEACH). When a task, question, or chain "feels easy," that is the moment to run it again with the answer hidden — that is the only valid easy. The worst review state in this whole system is the one where you read file 13's answers and think "yes, I remember that." Remembering is recognition. Reproducing cold is recall. Only the second one survives an interviewer's follow-up.

**Which loop proves which skill (the interviewer's view):**

| Interview skill at 1–3 YOE | Loop that trains it | Scoring gate |
|---|---|---|
| Byte-level config recall (write the YAML/HCL/workflow) | 15-min WRITE + weekly full batch | 0–5 per task, file 13 rubric |
| Instant one-sentence answers under pressure | 15-min QUIZ + ROUND 1 / ROUND 5 | ≤30s per SA, one clean sentence |
| Depth under follow-up (the "one-two punch") | CHAIN (L1.5/L2 rows) + ROUND 1 go-deep | L1.5 ≤45s, L2 ≤60s, file 14 score |
| Structured troubleshooting narration | DEBUG + ROUND 2 / ROUND 6 live-debug | 9-step method score /5 |
| Claim honesty under hostile probe | DEFEND + ROUND 4 / ROUND 6 | 3-probe pass/fail, downgrade mandatory |
| Design + end-to-end spine | TEACH + ROUND 3 / ROUND 6 | fluency, not polish |

**The monthly frequency table (how often each mode fires, four-week month):**

| Activation mode | Fires per four-week month, at full health | The minimum honest month (every loop logged) |
|---|---|---|
| WRITE | 3/day × 28 = 84 daily attempts + 4 full batches (each up to 8 tasks) | 84 daily + 4 batches |
| QUIZ | 5/day × 28 = 140 picks + the +7d QUIZ passes (6 FT + 5 SA per theme) | 140 + 4 passes |
| CHAIN | 1/day × 28 daily slots + the 14d sweeps | 28 + 2 sweeps |
| DEBUG | 1/week narrated, 2 incidents each, + the 14d archetype passes | 8 incidents + 2 passes |
| DEFEND | 4 bullets/week × 4 = 16 defense passes | 16 + the T-7d LIE-DETECTOR re-read |
| MOCK | 1/week = 4 rounds | 4 rounds (a miss is logged MISSED, never dropped) |
| TEACH | 1/month per the 30d router | 1 |

The numbers are the plan's definition of "at full health": a month that shows far fewer logged rows is a month the lookback (2.6) audits as decay, not as coincidence.

---

## 1. THE 15-MINUTE DAILY LOOP

One fixed 15-minute slot every day. Morning is better than evening (the 24h clock starts the moment you study; a morning slot means the next study session lands ~24h later on the same clock). If the morning is lost, run it at lunch — but never skip two days in a row, because a two-day skip stakes a 48h-test failure you set yourself.

**Why three modes in one slot:** WRITE proves byte-level encoding (configs, commands, math), QUIZ proves instant one-sentence recall, CHAIN proves oral depth under a clock. An interviewer's live round is exactly one part "write the YAML", one part "answer fast", one part "talk through the chain" — so a daily 15-minute slot that does all three is the smallest unit of interview-shaped rehearsal that exists. Nothing in the slot is read-first; everything is recall-first.

**The rigid protocol (same order, every day, every week, every month):**

```text
DAILY 15-MIN LOOP — timer on, paper and pen (the file is the answer key, not the scratch pad)

SLOT 1 — WRITE (5 min): the day's 3 tasks from the table below. Cover the ANSWER block, attempt
under the task's printed time limit (each task header prints its seconds), then grade 0–5 on the
TRUE score row. Score <=3 → the task's RE-STUDY LOOP row is now armed: +24h and +48h re-attempts
go into the tracking sheet (this OVERRIDES the daily cadence for that task).

SLOT 2 — QUIZ (5 min): fire the day's 5 picks aloud, one clean sentence each, <=30s per question,
no notes. A wrong or frozen answer routes that question to the +24h lane in the tracking sheet.

SLOT 3 — CHAIN (5 min): run the day's chain from the map below — L1 aloud <=30s, L1.5 <=45s,
L2 <=60s, L3 <=90s (file 14 protocol). Score 0–5. Red rows (score <4) → +24h/+48h re-drill,
exactly per file 14's reset rule.

END: update the tracking sheet — today's three scores plus any +24h/+48h due dates that changed.
Close the file. Five minutes late is better than zero; never extend the slot into your work day.
```

### 1.0 THE MINUTE MAP (what 15 minutes physically looks like)

| Minute | Action | Clock note |
|---|---|---|
| 0:00–0:02 | Open the tracking sheet (Part 7, Table A). Read today's armed items first — anything whose +24h or +48h due date is today opens the loop | If armed items exist, they are quota 1–2 and the day's fresh quota-thirds the rest |
| 0:02–0:07 | SLOT 1 WRITE — 3 tasks, answer folded, each under its printed limit | Timer per task; grade immediately after each |
| 0:07–0:12 | SLOT 2 QUIZ — 5 picks aloud, ≤30s each, one sentence | No notes; misses written as +24h lines |
| 0:12–0:14 | SLOT 3 CHAIN — L1→L3 standing, wall clock | Score in the chain's drill log |
| 0:14–0:15 | Update the log: scores, misses, armed dates | If it takes longer than a minute, you are narrating — stop |

### 1.1 THE THREE-SLOT ROTATION TABLE (Mon–Sun)

The WRITE slot follows file 13's own 48-HOUR RE-DRILL PLAN weekday batches verbatim (Monday → tasks 13-01/02/03/04, and so on). Each daily slot runs 3 of that batch's tasks; the batch's 4th task is consumed by the 1-hour weekly loop, so across 7 days + the weekly batch nothing in the file is missed. Sunday's slot is always the deficit lane.

| Day | SLOT 1 — WRITE (3 tasks from file 13, batch = file 13's weekday set) | SLOT 2 — QUIZ (5 picks from file 15) | SLOT 3 — CHAIN (file 14 rotation week, see 1.2) |
|---|---|---|---|
| Mon | 13-01 (process states + signals), 13-02 (set -euo pipefail + health-check script), 13-03 (CIDR/subnet math) | FT-101 (load average), FT-105 (rwx + ssh Publickey), FT-113 (reset vs revert + reflog), SA-161 (process states R/S/D/Z/T), SA-192 ($? and why to save it) | Rotation Week primary chain 1 |
| Tue | 13-05 (Deployment YAML), 13-06 (Service + Ingress YAML), 13-07 (multi-stage Dockerfile, non-root) | FT-130 (image vs container vs layer), FT-135 (control plane), FT-137 (probes), SA-221 (container vs VM), SA-236 (three Service types) | Rotation Week primary chain 2 |
| Wed | 13-09 (Terraform HCL + state commands), 13-10 (GitHub Actions workflow), 13-11 (PromQL rate/irate/increase/quantile) | FT-144 (what tfstate is for), FT-149 (CI vs CD three-word test), FT-151 (GitHub Actions model), SA-251 (why Terraform is declarative), SA-264 (one artifact per run) | Rotation Week primary chain 3 |
| Thu | 13-13 (Helm values + release lifecycle), 13-14 (HPA YAML), 13-15 (PV/PVC YAML) | FT-139 (Service → endpoints → pods), FT-142 (HPA replica math), FT-143 (ConfigMap vs Secret), SA-237 (selector matches no pods), SA-248 (PV → PVC → StorageClass) | Rotation Week primary chain 4 + secondary re-drill |
| Fri | 13-17 (NetworkPolicy YAML), 13-18 (Terraform module + S3 backend), 13-19 (ArgoCD Application CR) | FT-157 (roles + trust + STS assume flow), FT-159 (container + supply-chain security), SA-272 (ArgoCD push vs pull), SA-288 (IAM deny order), SA-292 (scan + SBOM gate in CI) | File 14 Friday rule: 3-question sample drawn from each chain of the week |
| Sat | 13-21 (Alertmanager route + grouping), 13-22 (SLI/SLO/error-budget math), 13-23 (EKS managed node group) | FT-153 (Prometheus model + rate contract), FT-160 (the incident method), SA-277 (counter vs gauge), SA-282 (pending → firing → resolved), SA-296 (blast radius ordering) | File 14 Saturday rule: cross-domain run — 1 question per chain, answered WITH the source session name |
| Sun | 13-25 (OTel span + traceparent), 13-26 (SBOM + supply-chain gate), then ALL tasks scored ≤3 this week | FT-152 (rolling vs blue-green vs canary), SA-297 (four incident archetypes), SA-299 (rollback vs forward-fix), SA-162 (SIGTERM vs SIGKILL), SA-176 (TIME_WAIT) | Green-chain maintenance: re-run only chains with a row below 4 in the last 14 days |

**Why these exact picks:** the Monday slot clusters the P0 foundation tasks and the questions that every other domain references (signals, exit codes, $?); Tuesday clusters the YAML writers; Wednesday clusters the "write config, write the pipeline, write the query" trio that output-centric interviewers love; Thursday is Kubernetes depth; Friday is security + GitOps (the 2026 filter topics from 00-architecture §7); Saturday is observe + incident method; Sunday is the deficit lane by design. The Sunday QUIZ set is deliberately cross-domain so the week ends with breadth rather than theme-tunnel.

**The 4th task of each weekday batch** (13-04 Mon, 13-08 Tue, 13-12 Wed, 13-16 Thu, 13-20 Fri, 13-24 Sat) is not lost — it is the weekly batch's property (Part 2, Block 3). If a week's deep session falls, the 4th tasks re-enter the following week's daily slots on the day their +48h would have passed. Nothing in file 13's weekday plan is ever silently dropped.

### 1.2 THE CHAIN SLOT MAP — 4-WEEK ROTATION (from file 14's WEEKLY DRILL ROTATION TABLE)

| Rotation week | Mon | Tue | Wed | Thu + secondary | Fri | Sat |
|---|---|---|---|---|---|---|
| Week 1 | 14-01 LINUX | 14-02 NETWORKING | 14-03 GIT | 14-04 BASH (+ 14-01 rows bare, no notes) | file 14 Friday sample across 14-01..14-04 | cross-domain (file 14) |
| Week 2 | 14-05 AWS | 14-06 DOCKER | 14-07 KUBERNETES | 14-08 TERRAFORM (+ 14-04 exit-code crossover) | sample across 14-05..14-08 | cross-domain |
| Week 3 | 14-09 CI/CD | 14-10 OBSERVABILITY | 14-11 SECURITY | 14-12 TROUBLESHOOTING (+ 14-07 endpoints + rollout rows) | sample across 14-09..14-12 | cross-domain |
| Week 4 | 14-13 SYSTEM DESIGN | 14-14 BEHAVIORAL | 14-01 LINUX | 14-02 NETWORKING (+ 14-12 the mirror chain) | sample across 14-13/14-14/14-01/14-02 | cross-domain |

The daily CHAIN slot is a fixed 5 minutes — chain L1 through L3 at speed, standing, wall clock. Week 4 loops the foundations chains back through because file 14 requires re-drills to keep landing inside the same week. A chain only turns green when every row scores ≥4 at +48h (file 14 reset rule); a red row re-enters the following week's secondary pass. The Friday sample and Saturday cross-domain rule are file 14's own — the daily slot implements them at the 5-minute scale: Friday = three questions drawn one from each chain of the week, Saturday = one question per chain across the whole rotation week, each answered with the source session name attached (an extra retrieval hook: you are naming the session, not just the fact).

### 1.3 THE DAILY LOOP'S OWN 24H CLOCK

Because the loop is daily, the +24h re-attempt of anything you fail today lands in tomorrow's identical slot — same weekday, same batch, same quiz theme. Write "due tomorrow" on the tracking sheet entry today, and tomorrow's WRITE slot opens with your failed tasks before the quota tasks. This is how the 15-minute loop and file 13's +24h/+48h re-study lane become one mechanism instead of two competing checklists. Concretely: score 13-11 (PromQL) a 3 on Wednesday → Thursday's WRITE slot runs 13-11 BEFORE 13-13/13-14/13-15; Friday's slot runs it again (the +48h); if it is still ≤3 by Sunday, the Sunday deficit lane runs it a third time and it graduates into next week's Wednesday QUIZ set as a fourth activation.

**The armed-items rule, stated precisely:** armed items (anything in a +24h/+48h window) take precedence over the day's pre-printed quota. The day's 3 WRITE tasks and 5 QUIZ picks still run — they are the loop's stabilizer — but armed items open the slot at minute 0:00 and are graded before the quota. A day with 6 armed items is a day with 6 re-attempts and a shortened quota (the quota's least-recent item falls to the weekly batch). The tracking sheet's "Next-review dates armed" column is what makes armed items findable at 0:00 instead of at 0:10.

### 1.4 THEME-TILT BY CALENDAR WEEK (which daily slot flexes while the study calendar runs)

The core table above is constant — Mon–Sun IDs never change. But Part 5's weekly theme adds a tilt so the daily loop and the study week pull the same direction:

| Calendar week (Part 5) | Tilted daily slot | What changes |
|---|---|---|
| Week 1 · Foundations | CHAIN | Favor rotation Week-1 chains; Saturday cross-domain draws from 14-01..14-04 |
| Week 2 · Cloud compute + identity | QUIZ | 2 extra AWS/IAM picks replace 2 generic picks on Tue/Thu (FT-119/FT-120, SA-199/SA-200) |
| Week 3 · Cloud network + TF | WRITE | 13-09 and 13-18 appear twice (Wed + Sat replace 13-22/13-23 on a rotation) |
| Week 4 · Containers | WRITE | 13-07 and 13-08 appear twice (Tue + Fri) |
| Week 5 · Kubernetes | QUIZ | 5 Kubernetes picks daily (SA-234..SA-250 pool), 2 FT slots stay constant |
| Week 6 · Delivery | WRITE | 13-10, 13-19, 13-20 appear twice (Wed + Sat) |
| Week 7 · Operate | QUIZ | Observability + security picks dominate (SA-276..SA-294 pool) |
| Week 8 · Defend | CHAIN | Rotation pauses; daily = 1 random chain + 1 green-chain re-check |

Tilt rule: a tilted slot still fits inside 5 minutes. Tilt means WHICH IDs run, never MORE than 5 minutes. When a tilted ID and an armed item collide, the armed item wins (1.3).

### 1.5 A WORKED WEEK (read this once, then never re-read it)

Monday: WRITE 13-01 (90s), 13-02 (300s — split-grade: shape now, byte-exactness in the weekly batch), 13-03 (180s). Scores 4/3/5. QUIZ: FT-101 clean, FT-105 fumble on StrictMode ("the group-writable .ssh makes sshd ignore authorized_keys" — missed the client-side 0644 rejection), FT-113 clean, SA-161 clean, SA-192 clean. CHAIN 14-01: L1 fine, L2 zombie reaping fumbled (said "kill the child" instead of "kill the parent so PID 1 reaps"). Log: armed FT-105 and 14-01-L2 for Tuesday.

Tuesday: opens with FT-105 re-attempt (clean now) and 14-01-L2 re-drill (≥4). WRITE 13-05/13-06/13-07 (split-grade the 300s ones). QUIZ, CHAIN 14-02. Nothing new armed; FT-105 graduates back to quota status.

Wednesday: WRITE quota + armed 13-02 +48h (the Monday 3). QUIZ, CHAIN 14-03. Sunday's deficit list is already predictable: any task ≤3 across Mon–Sat, run cold with full timer.

This is the loop. Weeks of this produce a Sunday deficit list that is almost empty, a weekly batch with byte-exactness, and a 7d pass that scores 4+. Weeks of NOT doing this produce the same three signals in reverse — and the taper pays for it.

### 1.6 FAILURE MODES OF THE DAILY LOOP (and the fix for each)

| Symptom | Likely cause | Fix |
|---|---|---|
| Scores plateau at 4, never 5 | Grading yourself generously (you "knew it" but had a hint in view) | Answer with the file physically closed; grade byte-accuracy first, then meaning; a 4 must come with the exact slip written down |
| Weekly batch keeps grabbing the same 4th tasks | Daily slots are bleeding into the batch's property | Enforce the timer; the batch tasks are not for speed, they are for completeness |
| Sunday deficits are always empty | You are not scoring honestly | A task with a vague "mostly right" is a 3 by file 13's definition; re-read the rubric and re-grade the week |
| The slot is drifting later each day | No fixed cue | Anchor to a hard daily event (after your first coffee, after the standup, before lunch) — never "when I have time" |
| You finish in 9 minutes and feel smug | You are blurting, not recalling | Slow down into the clocks: 30s per sentence, 90s per L3, pen moving on WRITE. Early finish = shallow recall |
| Armed items pile up faster than they clear | The +24h lane is running ahead of re-encoding | Stop adding new quota, run a 3-day armed-only loop — the daily loop survives, the quota is provisional |
| Same task fails 3 weeks running | Retrieval outrunning encoding (the source session is under-taught) | Re-run the ruling session per 13's source pointer before attempting the task again (Part 7, "What to do with a same-score pattern") |

### 1.7 THE SPLIT-GRADE RULE (shape now, byte-exactness in the weekly batch)

Some tasks are long enough that one 15-minute slot cannot honestly grade them byte-exact AND finish the other two slots. File 13's task headers print a seconds value for exactly this. The split-grade rule: on the first in-slot attempt, grade SHAPE — structure, block presence, order of operations, the required lines in the right order — and mark byte-exactness as a debt to be proven in the weekly batch (Part 2, Block 3), where the same task gets the full timer and the byte-gold standard.

| Task | Why it splits | Shape grade | Byte-exact proof lands at |
|---|---|---|---|
| 13-02 set -euo pipefail + health-check script (300s) | script length exceeds a fair 5-min WRITE slot | structure + the trap / exit-code lines present | weekly Block 3 under the 300s timer |
| 13-05 Deployment YAML | ~40 lines of spec | required blocks (metadata / spec / template / containers) present and ordered | weekly Block 3 |
| 13-06 Service + Ingress YAML | two resources in one task | the selector-port wiring resolves: Service → endpoints → Ingress → backend | weekly Block 3 |
| 13-07 multi-stage Dockerfile, non-root | two stages + hardening | base per stage, COPY --from stage mapping, USER non-root line | weekly Block 3 |
| 13-11 PromQL rate/irate/increase/quantile (180s) | four functions + histogram | `sum by (le)` guard present in the quantile query | weekly Block 3 |

A 4 on shape with a byte-debt is honest; a 4 with "I corrected it in my head" is not — corrections in your head are recognition, and recognition does not count.

### 1.8 THE WEEKEND SLOT (Saturday is the freest proof, Sunday is the debt lane)

No work day sits on Saturday, which makes it the only slot where the timer can honestly run long. Use it for the two things the work-week slot cannot afford: the file-14 Saturday cross-domain rule (1.2) with the source-session-name attachment, and a re-drill of every chain that carried a red row this rotation week. Sunday's slot is the deficit lane by design (1.1): every task scored ≤3 across the week runs cold under its full timer, and the day's QUIZ set mixes domains so the week ends broad. Sunday is also the only day the slot may legitimately run to 20 minutes — spend the extra five minutes re-writing the week's armed items into next week's Table A rather than taking more tasks.

### 1.9 THE 3-DAY ARMED-ONLY RECOVERY PROTOCOL

Failure-modes row six ("armed items pile up") gets a named protocol instead of a vague "run fewer tasks." When the armed stack (everything with a live +24h/+48h date) exceeds three days' worth of quota:

```text
ARMED-ONLY RECOVERY — 3 days, freeze the quota
DAY 1: run ONLY today's armed items, plus re-read each item's source-session section
       named in file 13 / file 14 (10 min re-read, 5 min attempts). No fresh quota.
DAY 2: re-run every arm that still scored <4 on day 1 (the +24h), plus the day's due
       +48h arms. No fresh quota; today's CHAIN slot is drawn from the green-list only.
DAY 3: the surviving arms at +48h run a final time. On exit, armed stack <= 2,
       full quota resumes.
EXIT RULE: if the stack is still > 2 on day 3, the weekly deep session's Block 3 is
       swapped for a batch of ARMS ONLY — the weekly batch's tasks defer a week.
```

The protocol's point is that the daily loop survives disrupted encoding, not that it clears a backlog in 72 hours. It restores the loop to exactly the state the 15-minute design assumes: at most a handful of armed items, each with a date.

### 1.10 THE TRAVEL-DAY FLOOR (the two-minute minimum)

A day lost entirely is not a failure; two days in a row is. On a travel/sick day run the two-minute floor: read today's armed IDs from the tracking sheet, and for each say the answer aloud in the exact formats (task answer, one-sentence SA, chain L1) without opening the answer file. Grade pass/fail only — that is enough to hold the +24h clock to its due date. A floor day is logged as a floor day with its pass/fail per item, and the next normal slot re-runs anything that failed the floor; per 6.4, a missed due date is a scoring event, not a reset — the floor just keeps the gap to a single day instead of two.

### 1.11 THE LOOP AS A HABIT STACK

The loop is most reliable when it rides an existing daily event rather than existing as one. The hall-of-fame stack is: the same 15 minutes, the same surface (the tracking sheet sitting open), the same first action (read tomorrow's armed dates, not today's scores). Each of the three fixed anchors removes one decision; each removed decision is a day the loop runs without negotiation. The failure-modes table's drift row ("the slot is slipping later") is the habit stack failing — the fix is not discipline, it is re-attaching the slot to whichever hard event still stands at the end of a bad week.

### 1.12 THE WEEKLY PICK ADVANCE (same weekday, fresh IDs, eight weeks of coverage)

Part 1.1 fixes the IDs for demonstration; the real cadence advances them inside each verified band so no weekday goes stale. The advance rule: each week, advance the day's five QUIZ picks one slot within their band, so over eight weeks the entire verified question bank walks through the daily slot. The bands are the ones the router (3.1) and Part 1.1 actually use:

| Band (file 15) | Printed in | Advanced by one slot per week, so the band rounds |
|---|---|---|
| SA-161 .. SA-197 foundations | router w1 (`5 random SA from SA-161..SA-197`) | every 8 weeks |
| SA-198 .. SA-207 first AWS | router w2 | every 2 weeks |
| SA-221 .. SA-233 containers | router w4 | every 3 weeks |
| SA-234 .. SA-250 Kubernetes | router w5 | every 4 weeks |
| SA-251 .. SA-263 first Terraform | router w2 | every 3 weeks |
| SA-264 .. SA-275 delivery | router w6 | every 3 weeks |
| SA-276 .. SA-285 / SA-286 .. SA-294 observability / security | router w7 | every 2 weeks each |
| SA-295 .. SA-300 incident synthesis | router w8 | weekly (all six live) |

The FT picks rotate the same way inside the router rows' FT sets (60 FTs across eight weeks of daily slots is an easy full pass with margin). A domain whose +7d pass scored <4 has its band re-opened early (3.1) — the advance is a default, the band is the contract.

---

## 2. THE 1-HOUR WEEKLY LOOP

One deeper session per week on a fixed evening. This is the audit pass: the weekly loop consumes what the daily loop sampled. Budget 90 minutes when the week's mock round is 45–60 minutes; a 60-minute round (ROUND 2, ROUND 3) or 90-minute round (ROUND 5, ROUND 6) becomes the anchor and the other three blocks compress — the rule is all four modes fire once per week, and only the anchor's duration flexes.

**Why the weekly loop has four blocks:** Monday–Saturday the daily loop gives you three activation modes in 15 minutes. That is enough to hold an item, but not enough to prove it under interview conditions. The weekly session adds the two modes interviews actually pay for — DEFEND (claims) and MOCK (the live event) — and it waves the "full batch, whole file" flag on WRITE so the daily 3-of-4 sampling cannot drift into permanent blindness. If you only ever run the daily loop, you will sound like someone who has flashcards, not like someone who has operated.

```text
WEEKLY DEEP SESSION — one fixed evening, phone on do-not-disturb, voice memo app open

BLOCK 1 — MOCK ROUND (rotation table below): run the full round protocol from file 17 — timer on,
read the scenario brief, give the scripted opening prompt VERBATIM, record your spoken answers,
grade the 7 axes x/10, transcribe the REFLECTION section, then write MUST FIX / SHOULD FIX /
NICE TO HAVE. Every MUST FIX line enters the +24h lane NOW (file 17's rule: an answer solved
silently in your head is not an answer).

BLOCK 2 — LIVE-DEBUG INCIDENT (rotation table below): narrate the week's incident aloud through
file 12's fixed skeleton — symptom → scope → hypotheses → first-check-with-why → evidence →
root cause → fix → verify → prevent. Score narration + method, not the fix. You are scored the
way ROUND 2 and ROUND 5 score you: wrong-fix-but-narrated beats silent-correct.

BLOCK 3 — FULL WRITE BATCH (rotation table below): attempt EVERY task in the week's batch cold,
answer folded, task timer running. The daily loop sampled this batch three times; the weekly loop
proves you hold it whole. Grade each task 0–5; any ≤3 arms that task's +24h/+48h lane.

BLOCK 4 — RESUME DEFENSE PASS (rotation table below): for the week's bullets, fire file 16's
3-probe aloud ("how?", "why did you choose X?", "what went wrong and how did you fix it"), then
run the STAR narrative, then the HONEST DOWNGRADE, under 90 seconds each. Any bullet you cannot
hold → it is now a +24h item AND you lower the claim on the resume before you say it in a room.

END: update the weekly tracking sheet; carry MUST FIX lines into the coming week's daily slots.
```

### 2.1 BLOCK-BY-BLOCK GRADING

**Block 1 (MOCK round) — the 7 axes.** File 17 scores technical accuracy, reasoning & structure, communication, depth & nuance, follow-up defense, production judgment, uncertainty handling — each /10. Do not average the axes into a number and stop; the reflection is the deliverable. Transcribe what you actually said (voice memo → text, errors and hesitations included), then mark the exact line where you froze and the exact phrase you overclaimed. A round that scores 8/10 on every axis while quieting the uncertainty axis is a round that flatters you — the axis you instinctively spare is the axis the interviewer will actually probe. A ≤45/70 on ROUND 1 sends you back to 13-write-without-google before any further mock (file 17's own verdict rule) — honor it; it is the round being honest about you.

**Block 2 (live-debug incident) — the method score /5.** The skeleton is file 12's. Score 1 point per step done aloud in order: symptom named in one sentence / scope before jumping / ≥3 hypotheses before the first check / first check carries a why / root cause stated before the fix / the fix is verified with the same evidence channel that caught the symptom / a prevention that fits the root cause rather than the symptom. Blast radius (SA-296) must visibly shape the order — containment first, evidence second, root cause third. A correct fix reached by magic is a 2. A wrong fix reached by honest narration is a 4. ROUND 2's entire premise is that narration + method get scored, not just the solve.

**Block 3 (full write batch) — whole-batch coverage.** For the low-time tasks (13-03 CIDR 180s, 13-04 git 120s, 13-08 run flags 120s, 13-11 PromQL 180s) the daily loop already proved speed; the weekly batch proves completeness across the batch's 4-8 tasks without a gap. Grade every task on the 0–5 scale; an average below 4 across the batch sends the batch's theme into next week's daily QUIZ set. The batch table: Batch A = 13-01..13-08 (foundations + containers), Batch B = 13-09..13-16 (provisioning + orchestration core), Batch C = 13-17..13-22 (security gates + delivery depth), Batch D = 13-23..13-26 + all month deficits.

**Block 4 (resume defense) — claim-level honesty.** The 3-probe is pass/fail per probe; the STAR narrative must be under 90 seconds with a defensible middle; the HONEST DOWNGRADE is mandatory even when you pass — say the downgrade aloud every session so the truthful version is the automatic one in a real room. File 16's claim-levels (USED / UNDERSTOOD / PRACTICED / OPERATED / DESIGNED, per 00-architecture §9) gate every bullet: a bullet you could not rehearse at its claimed level is downgraded to the level you just proved, tonight, before the resume gets sent anywhere. Every bullet's EVIDENCE ANCHOR must name a real war-room session — 05-aws, 06-docker, 07-kubernetes, 08-terraform, 09-cicd, 10-observability, 11-security, or 12-troubleshooting — because the anchor is what survives the second question.

### WEEKLY ROTATION TABLE (4 weeks, then the cycle repeats with ROUND 1 again)

| Week | Block 1 — MOCK round | Block 2 — DEBUG incidents | Block 3 — WRITE batch (file 13) | Block 4 — DEFEND bullets (file 16) |
|---|---|---|---|---|
| 1 | ROUND 1 · T · 45 min — fundamentals gauntlet (FT rapid-fire set + go-deep probe + 3 L2 chains) | INCIDENT 01 (kubectl connection refused) + INCIDENT 03 (DNS fails inside a pod) | Batch A: 13-01 .. 13-08 (foundations + containers) | 16-01 (CI/CD pipelines) · 16-02 (AWS infra) · 16-03 (Terraform modules) · 16-04 (containers + Kubernetes) |
| 2 | ROUND 2 · R · 60 min — narrated live-debug simulation, scored on narration + method | INCIDENT 16 (CrashLoopBackOff) + INCIDENT 19 (OOMKilled) | Batch B: 13-09 .. 13-16 (provisioning + orchestration core) | 16-05 (monitoring/alerting) · 16-06 (hardening/security) · 16-07 (Linux automation) · 16-08 (git workflows) |
| 3 | ROUND 3 · S · 60 min — system design: CI/CD pipeline + rollout for a 3-tier app | INCIDENT 22 (Terraform state lock + partial apply) + INCIDENT 23 (plan wants destroy/recreate) | Batch C: 13-17 .. 13-22 (security gates + delivery depth) | 16-09 (incident debugging) · 16-10 (IaC + config mgmt) · 16-11 (state/persistence) · 16-12 (networking: DNS/LB/TLS) |
| 4 | ROUND 4 · B · 45 min — behavioral + resume strike with hostile doubling-down probes | INCIDENT 28 (bad deploy — rollback vs forward-fix) + INCIDENT 29 (pipeline green, site on old version) | Batch D: 13-23 .. 13-26 + every task with ANY ≤3 in the month (deficit reruns) | 16-13 (observability pipelines) · 16-14 (cost/capacity) · 16-15 (dev environment support) · 16-16 (platform ownership) · 16-17 (architecture input) · 16-18 (runbooks/docs) |

**Why these incidents pair with these bullets:** ROUND 1 is breadth; the week-1 incidents are the two reachability signatures (refused vs silent) that every network follow-up reuses. Week 2 pairs the two orchestration-state killers with the on-call claim (16-09) — the same crash loop you debug is the story you must not overclaim. Week 3 pairs the state-failure pair with the Terraform and security bullets your reviewer will probe with INCIDENT 22/23. Week 4 pairs the delivery incidents with the CI/CD and observability bullets — and the resume strike round (ROUND 4) exists to catch the inflated phrase before a real interviewer does.

**After week 4 the table cycles** and ROUND 1 runs again under a stricter bar: any S block that scored below its first run's score is a regression, and regressions prove the +7d QUIZ pass for that domain was skipped. ROUND 5 (H · 90 min hybrid) and ROUND 6 (F · 90 min final comprehensive) are reserved for the 30-day loop and the taper (Parts 3 and 4) — they are the two rounds that certify you, not calibrate you. Across the first month you therefore play ROUND 1 → ROUND 4 once each (calibration), receive ROUND 5 + ROUND 6 via the 30-day loop and the taper (certification), and then repeat the four-round calibration cycle while the six-round set in file 17's matrix stays fully accounted.

### 2.2 A WORKED WEEK 1 SESSION

Block 1 runs ROUND 1 under the full 45-minute protocol. Score: technical 7, reasoning 8, communication 6, depth 6, follow-up 5, production judgment 7, uncertainty 7. The reflection catches the real problem: on S7 (ALB 502, FT-122) you said "the target is failing health checks" for a 502 — the 503 distinction — and on the go-deep probe 2 you had to restart the liveness-vs-readiness sentence. MUST FIX: re-drill FT-122's 502/503 split; re-drill 14-07 L2 probe rows. Both enter the +24h lane.

Block 2 runs INCIDENT 01 + INCIDENT 03 with the 9-step skeleton. Method score 3/5 — you fix-hunted at hypothesis 2 both times instead of opening with the first-check-with-why (for INCIDENT 01 the first check is the kubeconfig server URL + reachability, not the cluster). INCIDENT 03's DNS failure you nailed to the 4 failure classes. MUST FIX: first-check discipline on reachability incidents.

Block 3 (Batch A) — 13-01/02/03/04 scored 5/4/4/5 (13-02 dropped the `|| true` justification), 13-05/06 byte-perfect, 13-07 dropped CA-copy line (4), 13-08 5. Batch average 4.4 → theme stays, but 13-02 note goes into Wednesday's daily tilt.

Block 4 — 16-01 survived the 3-probe until "what went wrong and how did you fix it," where the downgrade sounded rehearsed but the STAR middle was thin (the pipeline's history, not just its parts). 16-02/03/04 passed at PRACTICED level. Conclusion: the resume bullet wording stands, the STAR middle needs one more pass next week — which is why week 2's Block 4 re-runs bullets 16-05..16-08 but file 16's NEXT POINTERs push 16-01's STAR re-run into the daily slot.

The weekly log row for this session writes: ROUND 1 / 47/70 / INC 01+03 / 3/5 / batch A 4.4 / 1 bullet ≤3 / MUST FIX: FT-122, 14-07-L2, first-check discipline, 16-01 STAR. That row is the input to week 2's daily slots.

### 2.3 WHEN A WEEK DIES (travel, work crisis, sickness)

Do not let the daily loop die with the week. Rule: the daily loop survives any week; the weekly session is the thing that compresses. A dead weekly session's four blocks get absorbed: the mock round postpones to the following week (the two-round month becomes a three-round month), but the WRITE batch's 4th tasks (Part 1.1) and the deficit reruns re-enter daily slots immediately. A missed round is logged as MISSED in Table B with a new due date — never silently dropped, because the round's 7-axis data is how you know which daily tilt the next fortnight needs. The only unforgivable month is one where missed sessions go unlogged — the tracking sheet keeps its empty week visible so the following month's quota expands to cover it.

### 2.4 THE WEEKLY SESSION RUN SHEET (the 90-minute minute map)

| Block | Time | What physically happens |
|---|---|---|
| Setup | 0:00–0:05 | Phone on do-not-disturb, voice memo app open, Table B row pre-filled with the week's rotation IDs, file 17's round brief open at the verbatim prompt |
| Block 1 — MOCK | 0:05–up to the round | the full round protocol; stop the recorder at the round end; never transcribe "from memory" — the recording is the evidence |
| Grade + reflection | +0:10 | 7-axis score sheet (Table E, Part 7), then the single most valuable minute of the week: listen to the recorded answers on axis 6 (production judgment) and axis 7 (uncertainty handling) and re-grade |
| Block 2 — DEBUG | +0:17 | both incidents narrated through file 12's 9-step skeleton, method score /5 per incident; wrong-fix-but-narrated beats silent-correct, scored the way ROUND 2 scores you |
| Block 3 — WRITE batch | +0:25 | full batch under the task timers; the only Block not recorded — scored straight into Table B |
| Block 4 — DEFEND | +0:12 | each bullet: 3-probe aloud + STAR + HONEST DOWNGRADE under 90s; a fail lowers the claim on the resume the same evening (file 16) |
| Close-out | +0:06 | MUST FIX lines written, each carrying a +24h/+48h date, copied verbatim into next week's Table A Monday row |

Durations flex when the round is ROUND 2/3 (60 min) or ROUND 5/6 (90 min): the round absorbs the whole session and Blocks 2–4 compress into the remaining minutes rather than being dropped (Part 2 intro). A session that misses Block 4 still logs it as MISSED — a skipped defense pass is a claim shipped unproven.

### 2.5 SCORING THE SEVEN AXES WITHOUT DELUDING YOURSELF

File 17's seven axes are technical accuracy / reasoning & structure / communication / depth & nuance / follow-up defense / production judgment / uncertainty handling, each /10. Calibration anchors remove the "I felt good about that" grade:

| Axis | A 5 | A 7 | A 9 |
|---|---|---|---|
| Technical accuracy | no wrong facts, some misses | all facts right, one gap named | right, with the boundary case volunteered |
| Reasoning & structure | steps in a sensible order | method visible before the first check | hypothesis list precedes the first check |
| Communication | mostly clean | one-sentence answers under the clock | trades length for precision when asked |
| Depth & nuance | surface naming | mechanism under the name | the alternative, and why not |
| Follow-up defense | re-states the original | extends the original | says "I don't know" cleanly and recovers |
| Production judgment | does not crash things | chooses the least-blast-radius move | names blast radius out loud (SA-296) |
| Uncertainty handling | hedges | admits and bounds | quantifies the uncertainty and redirects |

Grade twice: once immediately, then once more after listening to the recording. If the two grades differ by 2 or more on any axis, the LOWER one is the real one — the immediate grade is the one inflated by adrenaline. The uncertainty axis is the one interviewers weigh most at 1–3 YOE (00-architecture's whole thesis) and the one self-graders spare most; it is the only axis with a mandatory re-grade.

### 2.6 THE THREE-WEEK LOOKBACK (reading your own weekly rows backward)

Every month, before the 30-day loop fires, read the last three weekly rows in Table B as a control chart. The questions: (1) did each week's MUST FIX list shrink from the row above? (2) did armed-items-cleared climb while the batch ≤3 count fell? (3) is any MUST FIX item the same across two rows — a repeated MUST FIX is a source-session problem, not a retrieval problem (Part 7, same-score rule)? (4) which axis scored lowest on average across the three mock rows, and did a weekly tilt address it? The lookback exists to catch what the daily view hides: a stable weekly score with falling daily averages means the daily loop is drifting (lazy grading, slot drift) — fix the grader, not the material.

### 2.7 WHEN THE WEEKLY SESSION MUST SHRINK (the 30-minute variant)

Some weeks do not contain 90 minutes. The 30-minute shrunken session is still a weekly session and still logs a row: Block 1 compresses to the round's highest-signal 20 minutes (file 17's own brief marks its highest-value block; for ROUND 1 that is the go-deep probe, for ROUND 4 the hostile doubling-down probes), Block 4 compresses to the two bullets the resume ships first, and Blocks 2 and 3 are reduced to their slash-line scores from the daily loop — the week's incidents were already daily-narrated, the batch's 4th tasks were already daily-attempted. The shrink rule's teeth: never drop Block 4 (the defense pass), never run the round below 20 minutes, and log every compressed block as compressed so the next normal week's lookback can tell a true 30-minute week from a skipped one.

### 2.8 A WORKED WEEK 2 SESSION

Block 1 runs ROUND 2 (R, 60 min — narrated live-debug). Immediate scores: technical 6, reasoning 7, communication 6, depth 5, follow-up 6, production judgment 7, uncertainty 5. The recorded re-grade drops depth to 5 for real: the third hypothesis was announced but never tested — narration jumped back to hypothesis 1's check. MUST FIX: hypothesis discipline in narrated debugging (state all three, then test the first discriminator), plus the probe-actors model (chain 14-07's L2 went slow under narration).

Block 2 runs INCIDENT 16 + INCIDENT 19 with the 9-step skeleton. Method 4/5: INCIDENT 16's first-check-with-why landed (CrashLoopBackOff → describe + logs before touching: liveness vs image vs OOM), and INCIDENT 19's OOM evidence preceded its fix. The missed point: INCIDENT 19's prevention was written as a symptom fix ("add memory limits") instead of a root-cause fix (the limit-exhaustion pattern behind 19's class). MUST FIX: prevention-that-fits-the-root-cause on memory deaths (SA-296's blast-radius framing extends to prevention, not just remedy).

Block 3 (Batch B: 13-09 .. 13-16) — 13-09 5, 13-10 4 (the workflow `on:` path-filter detail was thin), 13-11 4 (the `sum by (le)` guard still slipping), 13-12 4, 13-13 5, 13-14 5, 13-15 4 (reclaim policy detail), 13-16 3. Batch average 4.25 → the batch stays, and 13-11's histogram guard moves into the weekday tilt.

Block 4 — 16-05 passed the 3-probe, 16-06 passed, 16-07's "Linux automation" failed the third probe ("what went wrong and how did you fix it" — the story needed the exact incident, not the symptom), 16-08 passed at PRACTICED. One downgrade written tonight: 16-07 PRACTICED → USED until re-anchored. MUST FIX carries into week 3's daily slots: 13-11 sum-by-le, INCIDENT 19 prevention, 16-07 anchor, hypothesis discipline.

That row is week 2's answer to week 1's row. The few items that repeat across both rows (13-11, hypothesis discipline) are exactly the source-session items the same-score rule (Part 7) names — the worked weeks are the plan demonstrating its own audit.

### 2.9 THE ROUNDS AND WHAT EACH ONE CERTIFIES (the interviewer's view)

| Round | Duration | What it certifies | The axis it attacks hardest |
|---|---|---|---|
| ROUND 1 · T | 45 min | fundamentals gauntlet: breadth under fire | technical accuracy + speed |
| ROUND 2 · R | 60 min | narrated live-debug under the 9-step method | reasoning & structure |
| ROUND 3 · S | 60 min | system design, end to end | depth & nuance |
| ROUND 4 · B | 45 min | behavioral + hostile doubling-down probes | follow-up defense + uncertainty |
| ROUND 5 · H | 90 min | hybrid marathon | all seven axes, endurance |
| ROUND 6 · F | 90 min | final comprehensive (elevation + design + live-debug + behavioral + "say you don't know") | the whole rubric at certification weight |

The certification framing changes how you score: ROUND 1–4 are calibration (their data feeds the daily tilts), ROUND 5 and ROUND 6 are certification (their MUST FIX lists feed the taper). File 17's matrix assigns each round its source assets; this file's weekly rotation (2.1) and taper (Part 4) do the scheduling.

### 2.10 WHAT NOT TO BRING INTO THE WEEKLY SESSION

The weekly session is the audit; it inherits the daily loop's tools but not its decorations. Leave out: the answer files (Block 3's answers are the folded copy, not the file), any tool you would not have in the room (the phone is DND, the voice memo app open, no browser), and any "I looked it up since" — a task graded against a lookup is a task graded as recognition, and file 13's rubric has no column for it. The one permitted prop is the tracking sheet and this file's tables: the session's job is to prove the row, not to improve the prose.

---

## 3. THE 7-DAY / 14-DAY / 30-DAY LOOPS

These are the forgetting-curve re-encounters. They run on fixed offsets from when you STUDIED a theme, not from the calendar day — the calendar in Part 5 tells you what you are studying each week; this section tells you what to do once that week is 7, 14, and 30 days old.

### 3.1 THE RE-VISIT ROUTER

| After you study a theme (Part 5 week) | → +7d QUIZ pass | → +14d DEBUG + CHAIN pass | → +30d TEACH + MOCK pass |
|---|---|---|---|
| Week 1 · Foundations (Linux, Networking, Git, Bash) | FT-101, FT-105, FT-106, FT-111, FT-113, FT-115, plus 5 random SA from SA-161..SA-197 | INCIDENT 15 (ssh publickey) + INCIDENT 01 (kubectl refused) + INCIDENT 03 (pod DNS) · CHAIN 14-01, 14-02, 14-03, 14-04 | TEACH the signal → zombie → OOM model from 01-linux LINUX.P0.1 · MOCK ROUND 1 (T, fundamentals gauntlet) |
| Week 2 · Cloud compute + identity (AWS core, Terraform basics) | FT-119, FT-120, FT-124, FT-127, FT-144, FT-145, plus 5 random SA from SA-198..SA-207 and SA-251..SA-263 | INCIDENT 09 (AccessDenied on S3) + INCIDENT 10 (kubectl Forbidden) + INCIDENT 11 (AssumeRole fails) · CHAIN 14-05 (AWS), 14-08 (Terraform) | TEACH the IAM assume-role chain (SEC.P0.3, FT-157) · MOCK ROUND 4 (B, resume strike — your AWS bullets are probed) |
| Week 3 · Cloud network + provisioning (VPC/ALB/Route53, TF state/modules) | FT-121, FT-122, FT-123, FT-125, FT-146, FT-148 · SA-203 (NACL ephemeral), SA-213 (unhealthy target group), SA-214 (alias vs CNAME), SA-259 (state lock), SA-256 (terraform import) | INCIDENT 04 (ALB 502/503) + INCIDENT 06 (intermittent timeouts under load) + INCIDENT 22 + INCIDENT 23 (TF state pair) · CHAIN 14-05, 14-08 | TEACH the SG-vs-NACL intersection + the "what state is for" model (TF.P0.2) · MOCK ROUND 3 (S, CI/CD system design) |
| Week 4 · Containers + runtime (Docker write-from-memory) | FT-130, FT-131, FT-132, FT-133, FT-134 · SA-222 (copy-on-write), SA-225 (alpine/distroless/scratch), SA-229 (restart vs HEALTHCHECK), SA-232 (non-root), SA-230 (immutable tags) | INCIDENT 17 (ImagePullBackOff) + INCIDENT 25 (stale layers / wrong artifact) · CHAIN 14-06 (Docker), and re-drill 14-01 (signals) bare | TEACH the multi-stage Dockerfile + docker run hardening flags from memory (TASK 13-07 + 13-08) · MOCK ROUND 5 (H, hybrid marathon) |
| Week 5 · Kubernetes core (control plane, workloads, net, RBAC) | FT-135, FT-136, FT-137, FT-138, FT-139, FT-140, FT-141 · SA-234..SA-250 spot picks (5) | INCIDENT 16 (CrashLoopBackOff) + INCIDENT 18 (Pending unschedulable) + INCIDENT 20 (readiness failing, process healthy) · CHAIN 14-07 (Kubernetes) | TEACH the control-plane diagram + the probe actors (kubelet vs endpoints) · MOCK ROUND 2 (R, narrated live-debug — you debug a sick deployment) |
| Week 6 · Delivery + GitOps (CI/CD, Helm, ArgoCD) | FT-149, FT-150, FT-151, FT-152 · SA-264..SA-275 spot picks (5) · re-quiz any CI/CD FT you scored <4 on ROUND 3 | INCIDENT 26 (OutOfSync won't self-heal) + INCIDENT 27 (rollout stuck) + INCIDENT 24 (CI fails locally-passing tests) · CHAIN 14-09 (CI/CD) | TEACH the pipeline-as-code model + same-artifact promotion rule · MOCK ROUND 3 (S, CI/CD design) a second time, scored against your first attempt |
| Week 7 · Operate + harden (Observability, Security) | FT-153, FT-154, FT-155, FT-156, FT-157, FT-158, FT-159 · SA-276..SA-285 and SA-286..SA-294 spot picks (5) | INCIDENT 05 (TLS expired) + INCIDENT 12 (Secret mount) + INCIDENT 13 (IRSA no creds) + INCIDENT 30 (secret in git) · CHAIN 14-10 (Observability), 14-11 (Security) | TEACH the three pillars + alert-on-percentiles reasoning · MOCK ROUND 4 (B, resume strike — 16-05/16-06/16-13/16-18 bullets) |
| Week 8 · Incident synthesis (12-troubleshooting) | FT-160 (incident method) + SA-295..SA-300 (all six) + one un-named FT drawn at random from the whole bank | All four archetype maps: INCIDENT 02+07 (A), INCIDENT 12+13 (B), INCIDENT 16+21 (C), INCIDENT 28+30 (D) · CHAIN 14-12 (Troubleshooting method), 14-13 (cross-cutting), 14-14 (behavioral) | TEACH the 9-step incident method from memory, top-down · MOCK ROUND 5 (H, hybrid) a second time |

**The 7-day QUIZ pass is not "answer the ones you know."** It is a timed pass — each FT under 60 seconds aloud, each SA under 30 seconds with one sentence. A hit is only a hit if it came out of your mouth under the clock. Score the whole pass; a domain below 4/5 routes that domain into next week's daily QUIZ slot as a +7d override. The 7d pass is deliberately LIGHTER than the study week that produced it (six FT + five SA, not the full domain file): the goal at +7d is to catch the fade before it spreads, not to re-study. If the pass scores 4+ you have proof the item consolidated; if it scores 3 you have proof the daily loop needs to keep feeding that domain; below 3 and the domain's study week effectively did not happen and its sessions re-enter the calendar as a next-month repeat.

**The 14-day DEBUG + CHAIN pass is the mechanism test.** File 14's L2 rows are built to fail you if you remember the fix without the mechanism ("if it stays hard, the CROSS-EXAM"); file 12's skeleton demands first-check-with-why on every incident, so a memorized fix that skips the evidence step scores a 2. This loop is where "I know Kubernetes" becomes "I reason through the endpoints promise" — it is the same question ROUND 1's go-deep probe will fire at you. Run the incidents NARRATED, standing, one incident each direction; the +14d pass's point is not the four incidents, it is the recall of the METHOD across four unrelated failure classes.

**The 30-day TEACH + MOCK pass is the integration test.** TEACH forces the material back through a second build — explaining the model to an imaginary teammate 30 days after you learned it is the strongest single predictor an interviewer's open question will not flop. The MOCK round then judges the whole month under the 7-axis rubric. A month that ends with a MUST FIX list is a month that worked — the list IS the next month's +24h lane. When two 30-day passes land the same week (calendar offset collision, which happens around month 3), merge them: run the month's TEACH topic, then the month's MOCK round, and treat the second month's items as already-partially-proven — do not double the load, double the grading.

### 3.2 HOW THE THREE PASSES FIRE OFF THE WEEKLY CALENDAR (worked month)

Study Week 1 (Foundations) in calendar week 1 → at calendar week 2 the +7d QUIZ pass lands (six FT + five SA, timed). At calendar week 3 the +14d DEBUG + CHAIN pass lands (INCIDENT 15/01/03 + chains 14-01..14-04). At calendar week 5 (calendar week 1 + 30 days) the TEACH + MOCK pass lands (TEACH the signal/zombie/OOM model, MOCK ROUND 1). Meanwhile calendar week 2's study week fires its own +7d in calendar week 3, and so on. From calendar week 5 onward the plan is always one pass behind a former theme — exactly the state the decay model wants: every day contains a re-encounter, every week contains two offsets, every month contains an integration. At calendar week 9 the cycle has closed: Week-8's passes fire, and week 5's 30-day TEACH+MOCK re-confirms the earlier theme before the second cycle begins.

**Collision rule:** when the +7d QUIZ pass, +14d DEBUG+CHAIN pass, and +30d TEACH+MOCK pass all land in the same calendar week (they will, starting month 3), the order of precedence is: +30d (integration, highest value) → +7d (cheapest to run, highest frequency) → +14d (postponable into next week IF only one week late). Never postpone a +30d pass; it is the only one that proves re-integration.

### 3.3 THE 30-INCIDENT ARCHETYPE MAP (file 12's four failure classes, for the 14d pass and the taper relay)

| Archetype | Incidents | The class signature | The first-check that separates it |
|---|---|---|---|
| A · Reachability | INCIDENT 01..08 | name/socket promising, traffic not landing | refused (RST arrived) vs timeout (silence) — curl -v / nc -zvw2 / ss -tlnp |
| B · Identity/Authorization | INCIDENT 09..15 | valid request, no permission | explicit deny vs no-allow vs wrong principal — the IAM eval chain, STS, aws-auth |
| C · Orchestration/State | INCIDENT 16..23 | desired declared, reconcile opinion | events + describe first: CrashLoopBackOff, Pending, state lock — kubelet/controller evidence |
| D · Delivery | INCIDENT 24..30 | pipeline green, reality disagrees | verify the DEPLOYED artifact, not the pipeline: served version string, digest, rollout status |

The 14d pass runs one incident per archetype (the router row for each week chooses them); the taper relay (T-14d) runs INCIDENT 02 + INCIDENT 12 + INCIDENT 16 + INCIDENT 28 in one session specifically because those four are the archetype exemplars. If you can only afford one incident per archetype ever, those four are the ones.

### 3.4 BOUNDARY CASES

| Situation | Rule |
|---|---|
| A +7d pass scores 5 across the board | Mark the six FTs "5 twice at +48h equivalent" and graduate them to the 30-day lane per file 13 — do NOT keep re-quizzing them |
| A +14d pass's chain scores <4 on two different weeks | The theme's chain is under-encoded; re-run the source sessions (the chain's "Source sessions" row names them) then re-drill at +24h/+48h |
| A +30d TEACH wobbles on the mechanism segment | Re-study the ruling session and re-TEACH at +7d — the +30d schedule bends for exactly this, the 30-day clock does not restart |
| Two 30-day passes collide | Merge (3.2): one TEACH + one MOCK, double grading |
| You reach the interview week mid-30d-loop | The taper (Part 4) supersedes the router from T-7d; the router's remaining passes become MUST FIX items for the post-interview cycle |
| You finish all 26 tasks with 5s | That is the premise, not the finish: graduation moves them to 30d, and the second cycle's calendar adds the deepened bars (5.2) |

### TEACH PROTOCOL (used by the 30-day loop and the taper)

```text
TEACH PROTOCOL — your imaginary teammate is a new hire with six months of Linux, no domain background.
- 60 seconds: what this is and why it exists (the problem the tool/session solves).
- 2 minutes: the mechanism — the mental model from the source session, drawn not listed.
- 30 seconds: the failure — "here is how a real team breaks this, and the FIRST check."
- 15 seconds: prevention + one honest limit — "what I have not operated."
Record it on your phone in one take. Do not edit; grade fluency, not polish. A wobble on any
segment adds the source session to the +24h lane this week.
```

**Why TEACH is the 30-day mode and not QUIZ or CHAIN:** at 30 days the recall is either consolidated or gone. If it is consolidated, QUIZ/CHAIN merely confirm; if it is gone, they only measure the loss. TEACH forces you to rebuild the model top-down, which is the exactly the operation an interviewer's "explain X to me" performs. The +24h lane after a weak TEACH is the honest grade: the wobble names the session to re-study, and the next TEACH re-attempt lands +7d later rather than +30d — a fast second build for a topic that needed it.

### 3.5 WHAT TO PACK INTO EACH PASS (item selection, not item completion)

Each pass picks items because a signal booked them, not because a whole domain deserves re-attention. The signals, per pass: the +7d pass takes whatever scored ≤4 in the last week's daily logs plus the router row's fixed FT/SA set; the +14d pass takes the router rows' incidents and every chain with a red row that rotation week; the +30d pass takes the router row's TEACH topic plus the month's mock round. That keeps each pass small enough to fit inside the day's loop (7d: six FT + five SA ≈ 6 minutes; 14d: two incidents + chains ≈ 25 minutes; 30d: TEACH 3 minutes + a mock round from the weekly slot). A pass that grows is a pass that fell back into completion-thinking — the pass's job is to CATCH the fade, not to empty the domain.

### 3.6 THE COLD-START MONTH (when the study weeks do not exist yet)

The router fires off calendar-week themes, but a candidate who begins the plan with an interview six weeks out has no study block behind them. The cold-start rule: the 7/14/30 clocks begin at the FIRST study session of a theme, not at the calendar's week number. A cold-start month therefore looks like: weeks 1–4 (study the Phase-0 → Phase-2 themes of the calendar), week 5 (+7d for week-1's themes), week 6 (+7d for week-2's themes, +14d for week-1's), week 7 (+7d week-3, +14d week-2), week 8 (+7d week-4, +14d week-3, +30d week-1). The day the +30d of week 1 collides with week-4's +7d, apply the collision rule (3.2): +30d first, +7d second, +14d only if it is exactly one week away from its true date. The cold-start month is the honest picture of what five months of calendar feel like — denser and uglier — and the taper recognizes it by folding the +30d passes into the T-30d diagnostic rather than dropping them.

### 3.7 THE PASS PROTOCOLS (fenced, the exact runs)

```text
+7d QUIZ PASS (~6 min, timer on, answers aloud)
1. Open Table C's +7d row. Items: the router row's six FT + five SA, plus any domain
   scored <=4 in the last week's logs (the +7d override from 3.1).
2. FT first: 60s aloud per FT, answer fully, then move on. SA: 30s each, one sentence.
3. Score the pass /5. Domain <4 -> that domain re-enters the next week's daily QUIZ slot.
4. Log: items, score, and the exact phrase you fumbled. A fumble is a +7d sees it once;
   a miss is +24h.
```

```text
+14d DEBUG + CHAIN PASS (~25 min, standing, narrated)
1. Open Table C's +14d row. Items: the router row's incidents + chains.
2. Incident one, narrated through file 12's 9 steps aloud, method scored /5. Then the
   chains: every chain's L1 (30s) plus the router row's L1.5/L2 rows (45s / 60s).
3. Any chain with a row <4 -> +24h/+48h re-drill this week. Incident method <4 -> the
   class-signature first-check (archetype map, 3.3) is re-narrated aloud.
4. Log: scores, wobbled rows, and the next-step date.
```

### 3.8 THE POST-INTERVIEW CYCLE (the plan does not end at T-0)

The taper is a rehearsal for a date, not a permanent state of readiness (4.5). The day after the interview, the plan resumes at the loop it was in when the taper began: the calendar's next theme in Part 5's shifted slot, the daily loop unchanged, and every MUST FIX item the taper's mocks produced entering Table C as the new month's +24h lane. Two post-interview rules hold forever: (1) the interview's own failure memories are the single richest input the plan will ever get — the question that froze you becomes tomorrow's WRITE task and this week's 7d pass, not a narrative; (2) a passed interview is not a graduation from the loops — the loops are the hobby and the craft, and the taper was only the tour date.

### 3.9 THE OFFSET CLOCK SNAPSHOT (one line per theme, the +7/14/30 state)

The router is only useful if its state is visible in one place. Each week, before the weekly session, update the snapshot line for every theme whose clock is still running:

| Theme (study date) | +7d QUIZ | +14d DEBUG + CHAIN | +30d TEACH + MOCK | Next action |
|---|---|---|---|---|
| Foundations (wk 1) | FT-101/105/106/111/113/115 + 5 SA | INCIDENT 15/01/03 · chains 14-01..14-04 | TEACH signal→zombie→OOM · ROUND 1 | the +14d pass lands this week |
| Cloud compute (wk 2) | FT-119/120/124/127/144/145 + 5 SA | INCIDENT 09/10/11 · chains 14-05/14-08 | TEACH assume-role chain · ROUND 4 | the +7d pass lands this week |

The snapshot's rule: an empty cell means the clock has not started or already closed — there is no third state. If a theme's row shows a pass overdue by more than one week, that pass is executed at its true offset before anything else in the current week (the collision rule's +30d-first discipline, 3.2). The snapshot is written by hand once a week, not maintained in list software — the act of writing it is the reminder that a pass is due.

### 3.10 THE ROUTER WITH REAL DATES (a worked quarter)

Assume the study calendar (Part 5) starts on Monday of calendar week 1. The router rows name offsets; here they are with dates so "what fires this week" has a text answer, not a formula:

| Calendar week | Study theme | +7d fires | +14d fires | +30d fires |
|---|---|---|---|---|
| W1 | Foundations | — | — | — |
| W2 | Cloud compute | W1 QUIZ | — | — |
| W3 | Cloud network + TF | W2 QUIZ | W1 DEBUG+CHAIN | — |
| W4 | Containers | W3 QUIZ | W2 DEBUG+CHAIN | — |
| W5 | Kubernetes | W4 QUIZ | W3 DEBUG+CHAIN | W1 TEACH+MOCK |
| W6 | Delivery | W5 QUIZ | W4 DEBUG+CHAIN | W2 TEACH+MOCK |
| W7 | Operate | W6 QUIZ | W5 DEBUG+CHAIN | W3 TEACH+MOCK |
| W8 | Defend | W7 QUIZ | W6 DEBUG+CHAIN | W4 TEACH+MOCK |
| W9 (cycle 2, shifted slot) | Foundations | W8 QUIZ | W7 DEBUG+CHAIN | W5 TEACH+MOCK |

The pattern to see: from W5 onward every week carries one 7d, one 14d, and one 30d pass in addition to the study theme and the daily loop — that is the plan at full working load, and the collision rule (3.2) is what keeps it from collapsing. From W9 the cycle-2 themes start at the shifted slot and the previous cycle's later +30d passes land inside cycle 2's first weeks: the year runs as an interleaved pipeline, never as a series of restarts.

---

## 4. THE PRE-INTERVIEW TAPER (T-MINUS)

When the interview calendar is real, the loops compress into a taper. The rule above all rules: **from T-3d onward you learn nothing new; you only re-prove what you own.** The taper's job is confidence + sleep, not cramming. Everything you need already exists in this file's parts: the taper is just the loops with dates.

| Checkpoint | What you actually do |
|---|---|
| T-30d | Run ROUND 1 and ROUND 2 back-to-back as a cold diagnostic (breadth + narration). Run file 13's full P0 batch (TASK 13-01 .. 13-12) cold — this is your real ceiling. Read file 16's LIE-DETECTOR LIST and rewrite every bullet that contains managed / led / production / proficient as written. Produce the MUST FIX list for the month. |
| T-14d | Run ROUND 3 (S, system design) + ROUND 4 (B, resume strike). Run the 14d loop's incident relay — one incident per archetype (A/B/C/D) in one session, narrated aloud. Re-attempt every task and question you have scored ≤3 in the last 30 days — each at its true +24h/+48h date. Lock your sleep schedule: same wake-up time for the next two weeks. |
| T-7d | Run ROUND 6 (F · 90 min — final comprehensive: elevation, full design, live-debug, behavioral, and the "say you don't know" block). Refresh file 13's entire P0 batch (13-01..13-12) plus your strongest P1 tasks. Full CHAIN sweep at L1 speed: all 14 chains, L1 row only, 30 seconds each. Read file 16's LIE-DETECTOR LIST once more and confirm zero bullets carry a dangerous word. Build the cram sheet (below). |
| T-3d | No new material, no new drills. Re-run ROUND 6's MUST FIX items only, plus the three ANCHOR stories from file 16's ELEVATOR, spoken aloud three times each. Verify your stories: every STAR narrative you might deploy has a start, a middle, and an honest downgrade. |
| T-1d | No mocks, no drills, no new material. Read the cram sheet twice. Run the file 16 ELEVATOR once aloud in the bathroom mirror. Everything else is logistics: route, clothes, documents, travel time, water. Go to bed at your locked time. |
| T-night | Bag check, laid out before dinner: laptop + charger, printed resume (the printed one matches the one they have), the cram sheet, a blank incident template (file 12's 9-step skeleton on one page), water. Read the ELEVATOR once. Lights out on schedule. No screens in bed. |
| T-morning | Light touch: read the cram sheet once, ELEVATOR once, then STOP. Do not drill — drilling the morning of primes you to recite scripts instead of listen. Arrive 30 minutes early. Water, bathroom, quiet breath. You are re-proving what you own, not inventing what you do not. |

### 4.1 TAPER DETAIL — WHAT HAPPENS AT EACH DATE (expanded)

**T-30d — the diagnostic month opens.** ROUND 1 cold tells you breadth; ROUND 2 cold tells you narration under fire; the full P0 batch (13-01..13-12) tells you the honest ceiling in a number. From this date every MUST FIX the mocks produce goes into the +24h lane as if it were a daily task — the taper IS the daily loop with sharper teeth. The LIE-DETECTOR rewrite is mandatory, not optional: file 16's ten phrases (managed, led, production, "I know Terraform", "I've done load testing", "I optimized infrastructure", "I set up CI/CD for the company", "I built a monitoring stack", "I'm proficient in [tool]", "I have production experience") each have a truthful replacement, and the rewrite is where your resume drops its suspect vocabulary 30 days before the room hears it.

**T-14d — the relay and the merge.** The 4-incident relay (one per archetype: INCIDENT 02 reachability, INCIDENT 12 identity, INCIDENT 16 orchestration-state, INCIDENT 28 delivery) is the single most expensive 45 minutes of the taper and the single best predictor of ROUND 2 performance. Sleep lock is not optional: 00-architecture's whole thesis is that at 1–3 YOE the differentiator is fundamentals depth + structured reasoning + honest navigation — all three are sleep-dependent. Two weeks of a fixed wake time will visibly lift the uncertainty-handling axis.

**T-7d — ROUND 6 is the exam.** File 17's ROUND 6 (F · 90 min) is the final comprehensive: the file-16 ELEVATOR, a full design, a live-debug, a behavioral block, and the deliberately staged "say you don't know" moment. Score it as if it were the real interview — because it is the last full simulation you get. File 17's matrix says ROUND 6's source assets include FT-152, FT-160, INCIDENT 28 and chain 14-14 — so the week before ROUND 6, the daily slots converge on those four items plus the P0 batch. After ROUND 6, the L1 chain sweep (all 14 chains, only the L1 row, 30 seconds each) is a breadth audit, not a depth exercise: any chain whose L1 row wobbles is a red flag that you have been studying the current theme and starving the foundations — exactly what the previous 7 weeks were supposed to prevent. The cram sheet is built ONCE at T-7d and then read-only (it must be aged by T-1d so it is familiar, not novel).

**T-3d → T-morning — nothing new.** Novel material the night before an interview increases activation errors. The taper's last 72 hours are re-proof: ROUND 6's MUST FIX items (in the +24h/+48h lanes), the three anchor stories at a spoken cadence, the ELEVATOR until it is automatic, and then logistics. T-night's "blank incident template" is a deliberate trap-avoidance tool: if the interviewer pivots to a live-debug you have never seen, the blank 9-step page in front of you is the scaffolding that keeps you narrating instead of freezing.

### 4.2 THE T-MINUS WEEK GRID (the final 7-ish days, hour by hour)

| Day | Fixed blocks | Float (≤30 min, stop at T-1d) |
|---|---|---|
| T-7d | ROUND 6 full 90-min mock; post-mock reflection; L1 chain sweep (all 14 chains) | P0 write batch review; cram sheet drafted |
| T-6d | Cram sheet finalized (three pages); ROUND 6 MUST FIX +24h re-attempt | INCIDENT 28 re-narration (the round-6 debug) |
| T-5d | ROUND 6 MUST FIX +48h re-attempt; LIE-DETECTOR re-read | daily 15-min loop only |
| T-4d | ELEVATOR ×3; STAR stories verified aloud | daily 15-min loop only |
| T-3d | Nothing new: MUST FIX re-proof, anchors spoken ×3 | daily 15-min loop (light) |
| T-2d | Cram sheet read twice; logistics (route, clothes, documents) | no drills |
| T-1d | Cram sheet read twice more; ELEVATOR once; bed on time | no drills |
| T-night / T-morning | Bag check 8pm; cram sheet once + ELEVATOR once; arrive 30 min early | no drills |

The T-6d/T-5d float rows are the loop's normal daily slot with the calendar's musts removed — the only difference in the taper is that everything below T-3d is re-proof, not study.

### THE CRAM SHEET (built at T-7d, read-only from T-1d onward)

```text
CRAM SHEET — THREE PAGES, MADE ONCE AT T-7d, THEN READ-ONLY

PAGE 1 — MENTAL MODELS: the end-to-end spine (Git → CI → Docker → Registry → EKS → Ingress →
ALB → Route 53); the five canonical pipeline stages and the one-artifact rule; the k8s control-plane
diagram (apiserver / etcd / controller-manager / scheduler / kubelet); the IAM assume-role chain;
the incident 9-step skeleton. Each drawn, not written out in sentences.

PAGE 2 — THE NUMBERS: signals 1/2/9/15/17/18/19 and their defaults; common ports 22/53/80/443/
8080/3306/5432/6379/9000; the HTTP status taxonomy from NET.P0.4 (esp. 401 vs 403, 502 vs 503);
CIDR quick math (2^(32-prefix), usable minus 2); docker/k8s exit codes 125/126/127/137; RFC1918 +
loopback + link-local; probe defaults and rollout maxSurge/maxUnavailable; the burn-rate triggers.

PAGE 3 — THE THREE ANCHORS: file 16's ELEVATOR verbatim; your three anchor stories in STAR form;
and every claim you downgraded in the LIE-DETECTOR pass, with its truthful replacement already
memorized so the downgrade comes out sounding intentional.
```

**Cram-sheet rule:** at T-1d and T-morning you read the sheet; you do not write it, quiz it, or extend it. Writing it again is cramming; reading it is rehearsal. The sheet's whole value is that it is YOUR map of the domain, compressed by you, aged for two days until it is furniture.

### 4.3 THE BLANK INCIDENT PAGE (the T-night page, printed full size)

The page the taper packs is file 12's 9-step skeleton rendered as blank scaffolding, not a summary:

```text
THE BLANK INCIDENT PAGE — one page, pen only, written left to right
SYMPTOM (one sentence, observable): _________________________
SCOPE (who / what / where, before you touch): _________________________
HYPOTHESES (>=3, ranked roughly): 1. ____ 2. ____ 3. ____
FIRST CHECK + WHY (the cheapest test that discriminates #1): _________________________
EVIDENCE (what the check returned): _________________________
ROOT CAUSE (stated before the fix): _________________________
FIX (smallest blast radius, SA-296): _________________________
VERIFY (the same evidence channel as the symptom): _________________________
PREVENT (fits the root cause, not the symptom): _________________________
```

The point is the blank rows, not the text above them. Faced with a live-debug you have never met, the page supplies the order; your brain supplies only the content.

### 4.4 TAPER FAILURE MODES

| Symptom | Cause | Fix |
|---|---|---|
| The cram sheet keeps growing after T-7d | Novelty hunger — "one more page" is nerves | The sheet is sealed the night it was built; additions go on a separate "maybe" page that is never read on the day |
| ROUND 6 collapses versus the calibration rounds | The taper started too hot (deep new drills at T-10d) | The taper re-proves; verify the last three weeks of Table C rows are green, and do not touch the round's score |
| The T-14d relay method-scores 2–3 | The 9-step skeleton is not automatic | Re-run INCIDENT 28 with the skeleton laid flat in front of you — narration is the skill, not the diagnosis |
| T-1d / T-morning slips back into drilling | Adrenaline does not trust the re-proof | Reading the cram sheet IS rehearsal; drilling the morning primes scripts over listening (Part 4) |
| Sleep slips at T-3d | Novel material gets picked up "one last time" | Novel material after T-3d is prohibited by rule; the fixed wake time is the schedule, not a suggestion |

### 4.5 TAPER INTERRUPTIONS

The interview rarely survives contact with life intact. If it moves: the taper pauses at whatever checkpoint it reached and the plan returns to the normal loops from the next calendar day — no debt is treated as missed, the due dates simply re-aim at the new T-0. If it is cancelled: the taper's asset is the 30 days of MUST FIX items now sitting in Table C, which become the next month's +24h lane — exactly the state the loops are designed to consume. If the gap is longer than 60 days, the taper is stood down entirely and Part 5's cycle resumes at the shifted slot: a taper is rehearsal for a date, not a permanent state of readiness.

### 4.6 THE FULL TAPER CALENDAR (T-30d through T-morning, day by day)

The weekly grid (4.2) covers the last week; this is the rest of the month of a real taper. The daily 15-minute loop runs underneath every one of these days, narrowed to the leaner quotas from T-7d onward:

| Day | The fixed build | The float |
|---|---|---|
| T-30d | ROUND 1 + ROUND 2 cold diagnostic · full P0 batch (13-01..13-12) cold · LIE-DETECTOR rewrite pass | the first MUST FIX list, written tonight |
| T-29d → T-28d | diagnostic's MUST FIX into the +24h lane · resume rewrite finished from the LIE-DETECTOR output | daily loop, armed-items-first |
| T-27d → T-21d | a normal weekly cycle: daily loop + one weekly deep session (rotation week as it falls) | the MUST FIX list feeds the daily tilt |
| T-20d → T-17d | second weekly deep session · the sleep week begins (T-21d was the last irregular night) | daily loop |
| T-16d → T-15d | third weekly deep session if the calendar affords it · the ≤3 re-attempt windows open for the month's stubborn items | daily loop |
| T-14d | ROUND 3 + ROUND 4 · the 4-incident relay (INCIDENT 02/12/16/28) in one narrated session · every ≤3 item re-attempted at its TRUE due date · sleep locked | — |
| T-13d → T-8d | daily loop only, but the daily QUIZ leans the relay's four archetypes and the WRITE leans the P0/P1 gaps the diagnostic named | MUST FIX re-proof |
| T-7d | ROUND 6 · 13-01..13-12 refresh · 14-chain L1 sweep · LIE-DETECTOR re-read · cram sheet built once | — |
| T-6d → T-5d | ROUND 6 MUST FIX at +24h and +48h · cram sheet finalized | daily loop (light) |
| T-4d → T-3d | anchors ×3 spoken · nothing new · cram sheet sealed | daily loop (light) |
| T-2d → T-1d | cram sheet twice · ELEVATOR once · logistics finished by T-1d evening | no drills |
| T-night / T-morning | bag check · cram sheet + ELEVATOR once · arrive 30 minutes early | no drills |

The dates in the left column are the offsets of the checkpoints — when the interview date moves, every row moves with it wholesale, and only the T-7d boundary changes what the daily loop is allowed to do. A taper that starts from the cold-start month (3.6) or the 4-week compression (5.6) folds its accumulated +30d passes into the T-30d diagnostic; the calendar above is unchanged, only the diagnostic's weight grows.

### 4.7 A WORKED T-14d (the heaviest day of the taper, hour by hour)

| Time | Block |
|---|---|
| 07:00 | fixed wake; the day's daily 15-min loop already done, armed-items-first (1.3) |
| 18:30 | ROUND 3 (S, 60 min) full protocol, recorded |
| 19:40 | ROUND 4 (B, 45 min) full protocol, recorded |
| 20:30 | the relay: INCIDENT 02 + 12 + 16 + 28, one per archetype, narrated aloud, method scored /5 each — one sitting, about 25 minutes |
| 21:00 | the ≤3 re-attempt windows: every task scored ≤3 in the last 30 days re-attempted at its TRUE date (Table C's due columns), never as a stock "re-quiz everything" |
| 21:30 | logs: Table B (both rounds + relay), Table C, the debt ledger, next week's Table A arms |
| 22:00 | lights out at the locked time |

The day is heavy on purpose, and that is why it sits at T-14d and not T-7d: two full weeks remain to repair everything the day exposes, and ROUND 6 at T-7d measures the repair — not the day itself.

### 4.8 THE TAPER Q&A (asked once, answered finally)

**"Should I re-PROVE by reading, or re-prove by drilling?"** Reading. At T-7d the cram sheet is read; the drills already happened. Drilling the last week re-opens the very recognition channels the taper is trying to close — the morning-of rule (Part 4) is the whole taper in miniature.

**"What if I realise I never truly learned X at T-5d?"** You do not learn X at T-5d. X goes on the "maybe" page of the cram sheet and into the debt ledger with a date; the interview answers what you own, and everything else is the next month's +24h lane (3.8). The taper's rule "learn nothing new" exists precisely to protect you from the worst possible version of this sentence being said at T-5d.

**"Should the days before T-14d be heavier?"** No — the only heavy day is T-14d and T-7d by design (4.7, 4.2). A taper that ramps into the interview burns exactly the sleep the fixed wake time is protecting.

**"What if ROUND 6 at T-7d goes badly?"** It is data, not judgment. ROUND 6 is the certification instrument; a bad one means the MUST FIX list is real and the T-6d→T-5d re-attempts are its treatment (4.2). A taper that quietly deletes a bad ROUND 6 is the one failure every sheet in Part 7 was built to catch.

---

## 5. SUBJECT WEEKLY ROTATION CALENDAR (8 WEEKS)

The master calendar. Each week has ONE theme, a file set to hit, the primary (heaviest) loop, and its Phase from 00-architecture (Phase 0 Foundation… Phase 5 Defend). The "+7d / +14d / +30d" columns point to Part 3's router rows so the forgetting-curve passes fire off the correct theme. Weeks 9+ repeat the cycle shifted one slot so no theme is ever studied on the same weekday twice.

| Week | Phase (00-architecture) | Theme | Files to hit (sessions) | Primary loop | +7d / +14d / +30d pass |
|---|---|---|---|---|---|
| 1 | Phase 0 · Foundation | Foundations: Linux, Networking, Git, Bash interleaved | 01-linux (LINUX.P0.1–P0.8), 02-networking (NET.P0.1–P1.1), 03-git (GIT.P0.1–P0.7), 04-bash (BASH.P0.1–P1.1) | 15-min daily (WRITE/QUIZ/CHAIN) + weekly deep session | Router row Week 1 |
| 2 | Phase 1 · Cloud | AWS core (compute + IAM) interlaced with Terraform basics | 05-aws (AWS.P0.1–P0.5), 08-terraform (TF.P0.1–P0.3), 11-security (SEC.P0.2–P0.3 on IAM) | 15-min daily + weekly deep session | Router row Week 2 |
| 3 | Phase 1 · Cloud | AWS networking + storage, Terraform state/modules | 05-aws (AWS.P0.6–P0.10), 08-terraform (TF.P0.5–P0.7) | 15-min daily + weekly deep session | Router row Week 3 |
| 4 | Phase 2 · Containers | Docker — write from memory | 06-docker (DCK.P0.1–P1.1), 01-linux (process/signal cross-refs) | 15-min daily (WRITE-tilted: 13-05/13-07/13-08 daily) + weekly deep session | Router row Week 4 |
| 5 | Phase 2 · Containers → Orchestration | Kubernetes / EKS core | 07-kubernetes (K8s.P0.1–P0.9), 05-aws (AWS.P0.10 EKS), 11-security (SEC.P1.1 RBAC) | 15-min daily (QUIZ-tilted: 5 k8s picks daily) + weekly deep session | Router row Week 5 |
| 6 | Phase 3 · Delivery | CI/CD, GitOps, deployment strategies | 09-cicd (CICD.P0.1–P0.8, P1.1–P1.4, P2.x), 07-kubernetes (K8s.P1.4 Helm), 10-observability (OBS.P0.1–P0.9) | 15-min daily (WRITE-tilted: 13-10/13-19/13-20 daily-with-neighbors) + weekly deep session | Router row Week 6 |
| 7 | Phase 4 · Operate | Observability + Security hardening | 10-observability (OBS.P0.1–P2.2), 11-security (SEC.P0.1–P2.2) | 15-min daily (QUIZ-tilted) + weekly deep session | Router row Week 7 |
| 8 | Phase 5 · Defend | Incident synthesis + full rehearsal | 12-troubleshooting (all 30 incidents), 13-write-without-google (full file), 14-attack-chains (all 14), 15-question-bank, 16-resume-defense, 17-mock-interviews | 15-min daily + weekly deep session (ROUND 4 or ROUND 5) + begin T-minus if locked | Router row Week 8 |

### 5.1 WEEK-BY-WEEK SESSION DETAIL (what "files to hit" means per week)

**Week 1 — Phase 0 Foundation.** Read the priority maps of 01/02/03/04 first (each file's P0 vs P1 vs P2 line), then hit the P0 sessions in delivery order. The week's real work is the four chains (14-01..14-04) and file 13's Batch 1 tasks that cover foundations (13-01, 13-02, 13-03, 13-04). The daily loop runs the Monday/Tuesday/Wednesday WRITE slot against these tasks all week. Phase 0 is where "every command needs `export PATH="$HOME/.local/bin:$PATH"` and no sudo" (the recorded environment facts from 09-cicd's preamble) becomes second nature, because every later lab reuses them. The week's advised BREAK exercises, per 00's loop motif (BUILD → VERIFY → BREAK → OBSERVE → HYPOTHESIZE → ISOLATE → FIX → VERIFY → PREVENT): kill a service with TERM then KILL and watch the state change; break a health-check script and read its exit code; resolve a CIDR by hand against a real interface.

**Week 2 — Phase 1 Cloud compute + identity.** AWS.P0.1–P0.5 (regions/AZ, IAM, VPC, EC2/EBS, S3 core) streets over TF.P0.1–P0.3 (HCL, plan/apply, remote state). The IAM sessions dominate the week's QUIZ set (SA-198..SA-207, FT-119/FT-120) and the DEFEND bullets 16-02/16-03. This week plants the two identity models the whole system rests on — the IAM evaluation chain (explicit deny > allow > implicit deny) and the STS assume-role flow — so the WEEKLY deep session runs INCIDENT 09/10/11 with a strong narration bar. Advised BREAK: attach an over-broad policy, observe the audit flag, then least-privilege it and re-verify the same API works — the "verify works, verify can't do more" pair.

**Week 3 — Phase 1 Cloud network + provisioning.** AWS.P0.6–P0.10 (S3 versioning, ALB/target groups, Route 53, CloudWatch, ECR/EKS) with TF.P0.5–P0.7 (drift/partial apply, count-vs-for_each, modules). The week's WRITE slots center 13-09/13-18; the QUIZ set pulls the ALB/Route53/NACL items (FT-121/122/123/125, SA-203/213/214); the DEBUG pair is INCIDENT 04 + 06 (ALB 502/503 and intermittent timeouts) which exercise the reachability archetype at the AWS layer. The phase's thesis (00 §1 rule 5) is the single spine Git → CI → Docker → Registry → EKS → Ingress → ALB → Route 53 — Week 3 is where the spine's last four hops become concrete. Advised BREAK: take a healthy endpoint pair and remove the ephemeral NACL rule → observe replies drop while requests succeed — the stateless-reply lesson that CHAIN 14-05's L2 exists for.

**Week 4 — Phase 2 Containers.** DCK.P0.1–P1.1 end to end, with the file-13 writers that the file itself demands ("Docker (write from memory)" is the phase's verb, per 00 §5). The daily WRITE slot is tilted so 13-07 (multi-stage Dockerfile) and 13-08 (run hardening) appear more than once in the week; the QUIZ set is docker-heavy (FT-130..FT-134, SA-221..SA-233). This week's TEACH-ready deliverable (per the router) is reproducing the multi-stage + hardening pair cold — the exact thing the +30d pass will re-test. Advised BREAK: build the multi-stage image, then run it with --read-only and observe the first crash; re-add the writable mount and observe the fix.

**Week 5 — Phase 2 → Orchestration.** K8s.P0.1–P0.9 is the heaviest single week in the calendar. The daily QUIZ slot is tilted to 5 Kubernetes picks (SA-234..SA-250 pool, FT-135..FT-143), the DEBUG pair is the orchestration archetype C incidents (16 CrashLoopBackOff, 18 Pending, 20 readiness), and CHAIN 14-07 runs twice in the week (once primary, once as file-14's secondary pass). The week is the detector for the whole system: if Week 5's +7d QUIZ pass scores below 4, the Kubernetes foundation did not consolidate and the router's Week-5 row fires a full restudy in place of the 14d pass. Advised BREAK: deploy a Pod with a wrong readiness path, watch 0/1 while the process is healthy, then fix the path and watch endpoints populate — the readiness story that ROUND 1's go-deep probe re-fires.

**Week 6 — Phase 3 Delivery.** CICD.P0.1–P0.8 and P1.1–P1.4 plus the Helm session (K8s.P1.4) and ArgoCD model (CICD.P1.2, honesty-flagged model-only in file 09). The WRITE-tilted daily slots cover 13-10 (Actions workflow), 13-19 (ArgoCD Application CR), and 13-20 (Jenkins declarative) — the three configs interviewers ask to see written. The DEBUG set (24/26/27) is the delivery archetype D: the CI-fails-locally puzzle, OutOfSync, stuck rollout. The weekly deep session's mock is deliberately ROUND 3 (system design of a CI/CD pipeline) because the material and the round are the same muscle. Advised BREAK: run a pipeline, watch it fail in CI while passing locally, and isolate the environment delta — the exact INCIDENT 24 mechanism.

**Week 7 — Phase 4 Operate.** 10-observability (OBS.P0.1–P2.2, with the three-pillar, PromQL, SLO, alerting sessions) and 11-security (SEC.P0.1–P2.2, with IAM/IRSA/RBAC/network/secrets). The daily QUIZ set leans the metric-to-alert logic (FT-153/154/155, SA-276..SA-285) and the security depth (FT-156..FT-159, SA-286..SA-294). The DEBUG pair is the mixed identity + security set (INCIDENT 05/12/13/30). This is also the week to re-serve the model-only honesty boundaries (ArgoCD, Jenkins, RDS P1.2) so the taper's LIE-DETECTOR pass has nothing new to discover. Advised BREAK: alert on a percentile, then cause the slow-tail latency and watch the p95 breach while the average stays green — the "percentiles-not-averages" lesson from 13-22 and SA-285.

**Week 8 — Phase 5 Defend.** Everything before becomes rehearsal: 12-troubleshooting's full 30 incidents (four archetypes), 13's whole workbook, all 14 chains, the question bank, resume defense, mocks. The primary loop is the MOCK; the daily loop still runs its three modes but the WRITE slot's Sunday deficit sweep gets the first claim on the week. If an interview is locked, Week 8 turns into the taper (Part 4) with the calendar dates pinned — T-30d and T-14d land inside Week 8, T-7d one week out.

### 5.2 THE SECOND 8-WEEK CYCLE (Weeks 9–16) AND BEYOND

Repeat the calendar shifted by one week (Week 1's theme starts in calendar week 9's slot, and so on) so a theme is never rehearsed on the same weekday twice in a row. The second cycle runs with raised bars: every daily score must beat the first cycle's same-slot score, every chain must run its rotation at full depth (not the L1 version), and the +7d QUIZ passes from cycle one are merged so nothing is re-tested that already scored 5 twice (the graduation rule from file 13's 48-HOUR RE-DRILL PLAN). A candidate on a 5-day emergency timeline does NOT run this calendar — read Part 4's taper and skip straight to T-30d with the loops compressed to a 30-minute daily block.

### 5.3 PHASE-TO-LOOP TIE (from 00-architecture §5)

| Phase | Theme set | Dominant loop | Evidence gate that the phase is done |
|---|---|---|---|
| Phase 0 · Foundation | Linux, Networking, Git, Bash | daily WRITE + CHAIN (chains 14-01..14-04) | file 13 tasks 13-01..13-04 all ≥4 at +48h; chains 14-01..14-04 green |
| Phase 1 · Cloud | AWS core, Terraform | daily QUIZ + weekly DEBUG | INCIDENT 04/06/09/10/11/22/23 narrated ≥4/5 method score; FT-119..FT-125 ≥4 |
| Phase 2 · Containers | Docker, Kubernetes core | daily WRITE (tilted) + weekly MOCK | 13-05/13-06/13-07/13-08 byte-accurate; ROUND 2 narration ≥4 on uncertainty axis |
| Phase 3 · Delivery | CI/CD, GitOps, strategies | daily WRITE (tilted) + weekly MOCK (ROUND 3) | 13-10/13-19/13-20 byte-accurate; INCIDENT 24/26/27/28/29 method ≥4 |
| Phase 4 · Operate | Observability, Security | daily QUIZ + weekly DEBUG | FT-153..FT-159 ≥4; INCIDENT 05/12/13/30 narrated ≥4 |
| Phase 5 · Defend | Incident synthesis, rehearsal | MOCK + taper | ROUND 6 scored without a MUST FIX in uncertainty handling |

### 5.4 THE SPINE, REVIVED EVERY WEEK

00-architecture's one-mental-model rule means every week's deepest session should end the same way: redraw the end-to-end spine (Git → CI → Docker → Registry → EKS → Ingress → ALB → Route 53) with that week's theme written on top of it. Week 1 draws the spine with the git hop and the network hops labeled; Week 3 labels the AWS hops with real service names; Week 5 labels the orchestration hop with the objects; Week 6 labels the delivery hop with the artifact; Week 7 labels the observability hop with the pillars. The cram sheet's Page 1 is this drawing. A candidate who can redraw it cold, walking left to right with one sentence per hop, has the domain joined in the way interviewers actually probe it (the open "so what do you do?" first question).

### 5.5 HOW A STUDY WEEK MAPS ONTO THE TWO LOOPS

The grid below assumes a working week and deliberately does NOT assume evening study. Morning slot = the 15-minute loop (Part 1.1); lunch = 20–30 minutes of the week's theme sessions; the weekly deep session = one fixed weekday evening (Part 2). The theme's sessions are distributed so a day's QUIZ picks become tomorrow's theme:

| Day | Study (the week's theme files) | Daily 15-min loop (IDs never change) | Weekly deep session |
|---|---|---|---|
| Mon | theme sessions 1–2 | loop as printed (Mon IDs: 13-01/02/03, FT-101/105/113, SA-161/192, chain) | — |
| Tue | theme sessions 3–4 | loop as printed (Tue IDs) | — |
| Wed | theme sessions 5–6 | loop as printed (Wed IDs) | — |
| Thu | theme sessions 7–8 (the week's last big chunk) | loop as printed (Thu IDs) | the weekly deep session lands here, or |
| Fri | file 14's Friday sample — the theme closes with the sample itself | loop as printed (Fri IDs, Friday sample rule) | Friday evening if Thursday fell |
| Sat | theme wrap: redraw the week's file priority map from memory | Saturday slot with the cross-domain chain rule (1.2) | — |
| Sun | nothing new | Sunday deficit lane (1.1) | — |

The loop's IDs never change; only the study chunk's length flexes. A heavy theme (Week 5 Kubernetes) moves one session to Saturday morning.

### 5.6 THE EMERGENCY COMPRESSIONS (when the calendar does not fit the calendar)

Two compressors are built in, because real timelines are shorter than the plan.

5-day emergency: read Part 4's taper and skip straight to T-30d behavior, compressed. Day 1 = diagnostic (the cold ROUND 1 + the full P0 batch 13-01..13-12 + the LIE-DETECTOR rewrite); day 2 = the 4-incident relay (INCIDENT 02/12/16/28) + the three delivery bullets (16-01/16-05/16-09); day 3 = ROUND 6 + the 14-chain L1 sweep; day 4 = cram sheet built + the anchors spoken; day 5 = T-1d behavior (cram sheet twice, ELEVATOR once, logistics already done). The daily 15-minute loop runs every day underneath, narrowed to the leaner quotas.

4-week delivery: run Part 5 exactly as printed, but let the 30-day passes accumulate into the T-30d diagnostic rather than interleaving. The collision rule (3.2) applies from week 5 onward, and it is +30d first every time — the 4-week version has no margin for postponing integration.

### 5.7 THE MONTHLY DEEP-DIVE (one Saturday per month, 3 hours)

Once a month, replace the Saturday slot with a three-hour block aimed at the weakest signal in the last three weekly rows (2.6). Structure: 60 min — full write batch for the weakest domain ONLY (not the rotation batch; the domain's tasks from file 13's index), 60 min — the domain's incidents narrated one after another until the method score holds 4/5 twice, 30 min — the domain's chain at full L1–L3 with the source-session map open, 30 min — one mock round's design or behavioral block, whichever the lookback flagged. The deep-dive writes exactly one new row in Table G and then disappears until the next month — it is a treatment, not a second weekly session.

### 5.8 THE LONG VIEW (how the plan reads at week 26 and week 52)

Once the second cycle is running (5.2), the shape of the year is: months 1–2 build the domain (cycles 1–2 of the calendar), months 3–5 consolidate it (the shifted third and fourth cycles at the raised bars), months 6+ maintain it (one cycle per two months, taper whenever a date appears). The loops never stop: the daily 15-minute loop and the weekly deep session are the craft, and a missed week is a logged miss, not a re-plan. The year's hardest sell is the month after an interview (3.8) — the plan's whole design assumes you keep the loops precisely when nothing external is pushing you, and the 30d pass is the calendar's way of proving that no month runs on momentum alone.

### 5.9 THE ARCHETYPE-AWARE WEEK (when the JD is incident-heavy)

A job description that leads with operations ("respond to SEV-1s", "own the platform", "you will be on call") tells you which archetype the interview's debugging question will come in. With 1–3 days' notice before the WD, tilt: the week's Block 2 and daily QUIZ pool lean the JD's archetype from file 12 (reachability for network-heavy roles, identity/authorization for security-flavored, orchestration/state for platform + Kubernetes, delivery for CI/CD-owned teams) — the relay exemplar at the heart of that archetype (INCIDENT 02/12/16/28) is narrated twice in the week instead of once. The tilt changes WHICH incidents run, never the method: the 9-step skeleton is the whole point, and the archetype is only the costume it wears (3.3).

### 5.10 THE WEEK-8 TO-TAPER HANDOFF

When an interview date is fixed, Week 8 is where the calendar hands off to Part 4. The handoff rule: pin the taper dates the moment the interview is confirmed (T-30d = interview date minus 30), then let Week 8's sessions serve the taper as priority — the week's mock becomes the T-30d diagnostic (ROUND 1 + ROUND 2 back-to-back), the WRITE slot runs the full P0 batch (13-01..13-12) cold, and the LIE-DETECTOR rewrite happens inside the week rather than outside it. Week 8 succeeds exactly when its last row stops being a topic and becomes a countdown; Part 4 then takes over and the calendar pauses at week 8's shifted slot for whenever the loops resume (3.8, 4.5).

### 5.11 THE RECORDINGS LIBRARY (the two recordings that get kept)

Two things are recorded forever, everything else is recorded and discarded: the TEACH pass — the 3-minute rebuilt-model talk, one take, never edited — because a year later the difference between that take and your then-current take is the honest curve of your depth; and every mock round's audio, labeled with its ROUND number and date, because the pre-interview week wants the T-30d diagnostic's audio at hand to re-audit, not just its scores. The daily loop and the weekly non-mock blocks are heard-and-forgotten: the 2.5 re-grade rule already mined their value the same evening. The library is storage, not study — re-listening to old sessions is grade-school tape review, and this plan has no lane for it.

---

## 6. THE 24-HOUR RULE AND THE 48-HOUR RULE (RECAP, INTEGRATED)

These come from file 13's rigid protocol and file 14's chain rules. They are the spine of every schedule in this file; here they are restated so the mechanism is explicit and then wired into each loop.

**The rules, verbatim in spirit:**
1. **The 48h ownership rule (file 13):** an answer is "known" only if you can rewrite it cold 48 hours after studying the source session. The workbook's 48-HOUR RE-DRILL PLAN re-attempts every task on its fixed weekday slot regardless of score, and a task scored 5 twice in a row (48h apart) graduates to the 30-day review lane; a task scored ≤3 stays in the weekly lane until it proves a 5 at +48h.
2. **The +24h/+48h re-study rule (file 13):** any task scored ≤3 forces a re-study of the ruling sibling session (each task header names its source) and a re-attempt at +24h AND +48h. Those re-attempts OVERRIDE the weekly cadence for that task — the daily slot must open with them.
3. **The chain re-drill rule (file 14):** fumbled chain rows are re-drilled at +24h and +48h at full speed with no notes. A chain is green only when every row scores ≥4 at +48h; a red row re-enters the next rotation week's secondary pass. Re-drilling everything is dilution; re-drilling nothing is fantasy.
4. **The FT/SA re-drill rule (file 15):** after any mock, self-rate every FT and re-drill anything below 3/5; an SA you cannot answer instantly routes you to its source session for re-study.

**How the schedule enforces them:**

| Rule | Enforced by | Where it lives |
|---|---|---|
| +24h re-attempt | Tomorrow's daily slot opens with today's armed items | Tracking sheet (Part 7), daily log |
| +48h re-attempt | The day-after plus the Sunday deficit lane | Tracking sheet, Sunday WRITE slot |
| ≤3 override | Daily loop SLOT 1 + weekly BLOCK 3 re-grade the task at its due date before touching quota tasks | Daily + weekly logs |
| Chain red-rows | Daily CHAIN slot + file 14 WEEKLY DRILL ROTATION secondary pass | Chain log per chain |
| FT/SA <3 | Weekly BLOCK 1 post-mock scoring routes them to +7d QUIZ pass | Weekly log + router |

**The hand-off this creates:** score a task 3 on Monday → its +24h lands Tuesday's slot → its +48h lands Wednesday's slot → if it is still ≤3 by Sunday, the Sunday deficit lane runs it again AND it appears in next week's 7-day QUIZ pass for its domain. The same item is therefore re-attempted at +24h, +48h, +7d, and (if it stubbornly fails) +14d by three different activation modes — WRITE, WRITE-again, QUIZ, DEBUG/CHAIN. An item that survives all four is owned.

### 6.1 A WORKED 48H INTERVAL (task example)

Take TASK 13-11 (PromQL rate/irate/increase/histogram_quantile, 180s, source OBS.P0.3/OBS.P0.4). Monday's WRITE slot scores it a 3 (histogram_quantile query written without `sum by (le)`). Under file 13's rule the task arms +24h/+48h, and the ruling session is OBS.P0.4 (histogram/quantile).
- +24h (Tuesday): re-study OBS.P0.4's histogram section, then re-attempt 13-11 under the 180s timer. If the `sum by (le)` line now lands byte-exact, score 4.
- +48h (Wednesday): re-attempt again. 5 twice in a row (48h apart) would graduate it; a persistent 4 keeps it in the weekly lane.
- If it stays ≤3: Sunday's deficit lane runs it, then next week's +7d QUIZ pass includes it (router row continues), and the ruler shifts to "re-encode, don't re-attempt" (Part 7).

### 6.2 A WORKED 48H INTERVAL (chain example)

Take chain 14-07 KUBERNETES: during Week 5 you drill it Tuesday (primary). You fumble the L2 row (the probe-actors mechanism — who restarts vs who routes). Under file 14's rule that row is dead until re-drilled at +24h AND +48h at full speed with no notes:
- +24h (Wednesday): re-drill ONLY the L2 row of 14-07, plus the same row's TRAP VARIANT and CROSS-EXAM, aloud, no notes. If the L2 answer is still the fix-without-mechanism, score the row <4 and keep it red.
- +48h (Thursday): re-drill again; if the mechanism now lands (kubelet restarts via liveness, endpoints routes via readiness), score ≥4 and the row goes green.
- The row chain (file 14's WEEKLY DRILL ROTATION, Week 3) then carries 14-07's endpoints + rollout rows as its secondary pass anyway — a second independent re-encounter a fortnight later, in a different depth context. That is the 24h/48h rule meeting the 14d loop on a single row.

### 6.3 GRADUATION AND RETENTION LADDER

| Score pattern | Consequence |
|---|---|
| Task ≥4 at +48h | Stays in its weekly batch slot; moves to +7d QUIZ coverage automatically |
| Task 5 twice at +48h | Graduates to the 30-day review lane (file 13's rule); the daily/weekly loops stop re-running it |
| Task ≤3 at +48h | Stays in the weekly lane; Sunday deficit lane + next 7d QUIZ pass cover it, and its source session is re-studied |
| Missed re-attempt | The item is treated as ≤3 for the next scheduled pass — the due date is NOT pushed; the debt accrues |

The graduation rule is load control AND honesty control: without it, the daily loop would grow unboundedly (every task forever). With it, mastered items are retired to the 30-day lane and the loops stay at 15 minutes.

### 6.4 WHY "DUE DATE NOT PUSHED" MATTERS

A missed +24h re-attempt is not forgiven by running the +48h later — the 24h gap is the point, and skipping it means the next retrieval happens at 72h+, which is precisely the decay window the +24h slot exists to interrupt. The tracking sheet treats a missed due date as a scoring event: the item is marked ≤3-equivalent for the next scheduled pass, and the +24h count restarts from the day it was actually re-attempted. This one policy is what keeps the whole ladder honest — every date in the sheet is a contract, and broken contracts are visible in Tables A and C before the taper ever starts.

### 6.5 A WORKED 48H INTERVAL (FT example)

Take FT-122 (ALB 502 vs 503). Wednesday's QUIZ: you say 502 is "the target failing health checks" and 503 is "no targets in service," and score 3/5 (you missed that 503 also surfaces when the target is deregistering or the group is empty mid-rollout — the 502/503 split is the exact distinction S7 of ROUND 1 catches). Under file 15's rule and the +7d override, FT-122 arms +24h:
- +24h (Thursday): re-read the ALB/health-check source section named in FT-122, then re-answer aloud: 502 = the target is registered but failing the checks; 503 = no healthy target is reachable to forward to. Score 4.
- +48h (Friday): answered again under the 30s clock. If 5 twice in a row it graduates per file 13's graduation rule to the 30-day lane; a steady 4 keeps it in the daily pool, and the +7d pass covers it at its domain's offset.

The FT variant differs from the task variant only in the mode: the task re-attempt is a WRITE, the FT re-attempt is a spoken 30-second answer — same clock, same +24h/+48h dates, same graduation rule.

### 6.6 A WORKED 48H INTERVAL (BULLET example)

Defending BULLET 16-05 (monitoring/alerting): Friday's Block 4 fires the 3-probe and the STAR middle goes thin — the story has a start ("we had no alerts") and an end ("we now page on p95"), but the middle ("what exactly did you change") is two seconds of filler. File 16's rule is that an unrehearsable bullet is a +24h item AND lowers the claim:
- +24h (Sunday): re-run the STAR aloud, anchored to the concrete change — the percentile-based trigger from 13-22's lesson (SA-285) — because the anchor is what survives the second question.
- +48h (Monday): the next weekly Block 4 re-runs 16-05 PROBED, not reheard. If the middle now lands under 90 seconds with a named evidence anchor, the bullet's claim formally survives; otherwise the claim on the resume is downgraded one level (OPERATED → PRACTICED, per file 16's claim levels) before the taper arrives.

The bullet's 48h clock is the same mechanism as the task's, run against a claim instead of a fact — which is why the taper's LIE-DETECTOR pass (T-7d) is mostly a formality when this rule was honored for a month.

### 6.7 WHEN RULES COLLIDE ON ONE ITEM

| Collision | Resolution (the stricter rule wins) |
|---|---|
| One item is armed +24h on the same day its +7d pass is due | Armed items open the slot at 0:00 (1.3); the +7d pass then runs. The item counts once, not twice — a pass never double-tests |
| A chain row is red while the 14d pass lists that chain | The chain runs at the pass AND the red row re-drills +24h/+48h — they resolve to different rows of the same chain |
| A task graduates to 30d while the weekly batch still lists it | Graduation wins; the batch drops the task (file 13's rule) and the 30d lane receives it (6.3) |
| T-7d collides with a +30d pass | The taper supersedes the router from T-7d (3.4); the +30d items become MUST FIX items for the post-interview cycle |
| The emergency compression and a mock round share a day | The loop runs daily; the round gets its own evening — a round never shares a slot with the daily loop |

### 6.8 THE 48H RULE BY ACTIVATION MODE

The ownership rule is one rule; its handler differs by the mode that failed. This table is the single reference for what a ≤3 actually triggers per mode:

| Activation mode | What "owned" means | The fail handler | The graduation test |
|---|---|---|---|
| WRITE (task) | rewrite cold under the timer, byte-exact | +24h re-attempt + source re-study; +48h re-attempt; Sunday deficit lane | 5 twice at +48h → 30d lane (6.3) |
| QUIZ (FT) | full answer aloud under 60s | +24h re-answer + FT's source re-read | 5 twice at +48h → 30d lane |
| QUIZ (SA) | one clean sentence under 30s | +24h re-answer; miss routes to the source session (file 15) | 5 twice → stays in the daily pool |
| CHAIN (row) | L1/L2 row at its clock, no notes | +24h/+48h full-speed re-drill of THAT row + trap variant + cross-exam | row ≥4 at +48h → green (file 14) |
| DEBUG (method) | 9-step narration, method /5 | re-narrate the class's archetype exemplar, skeleton laid flat | method ≥4 twice in a row |
| DEFEND (bullet) | 3-probe + STAR under 90s | +24h re-run AND the claim downgrades one level (file 16) | bullet defended probed at the honest level |
| TEACH (topic) | model rebuilt top-down, 3 min | wobble → source session re-run, re-TEACH at +7d | fluency without the cheat notes |

### 6.9 A WORKED MISSED DATE (the contract in action)

Monday: TASK 13-11 scores a 3, its +24h due Tuesday. Tuesday: the slot is lost entirely (the two-minute floor runs, 1.10). Per 6.4, the miss is a scoring event — Tuesday's log marks 13-11 as ≤3-equivalent and the table re-aims: the +24h count restarts from the next true attempt, Wednesday. Wednesday: 13-11 runs cold first (it opens the slot), scores 4. Its +48h now lands Thursday (not Friday — the counter restarted from Wednesday). Thursday: 13-11 re-attempts, scores 4 again; it stays in the weekly lane and the +7d pass covers PromQL at its domain's offset. The date math is deliberate and messy on purpose: the penalty for the missed Tuesday is not a bigger drill, it is a fresh 24h gap from a real attempt — the exact gap the rule exists to enforce.

### 6.10 THE SCORE-LANGUAGE MAP (one number means one thing)

Every drill in the War Room uses its own scale; mixing them up silently corrupts logs and comparisons. The map:

| Where | Scale | What the top score means | What a bad score means |
|---|---|---|---|
| WRITE tasks (file 13) | 0–5 | byte-accurate under the timer, no hints | ≤3 → the +24h/+48h lane arms |
| CHAIN rows (file 14) | 0–5 | row answered at its clock with no notes | <4 → row re-drills; chain stays red |
| Method score (file 12, Block 2) | /5 | all 9 steps narrated aloud, in order, prevention fits the root cause | silent-correct is a 2, honest-wrong is a 4 |
| Mock round axes (file 17) | /10 × 7 | axis answered as the interviewer would score it, not as you felt it | the uncertainty axis is the one people inflate |
| 3-probe (file 16) | pass/fail per probe | all three probes held with a real evidence anchor | a fail downgrades the claim one level |
| QUIZ (file 15) | FT 60s / SA 30s | came out of your mouth under the clock | a fumble is +7d; a miss is +24h |

The one rule that joins them: anything graded with a hint, a corrected memory, or a "I would have gotten it" is graded as if it scored one step worse. Ladders are lying to you if they are flattered.

---

## 7. TRACKING SHEET TEMPLATES

Print these pages (or mirror them in /notes) and fill them every time a loop runs. The "Next review" column is where the +24h/+48h override lives — write the date, not a tick. Three rules: a loop without a log entry did not run; a score without a next-review date has no spine; a MUST FIX without a date will resurface in an interview.

### TABLE A — DAILY LOOP LOG (one row per day, 7 rows per week)

| Date | WRITE IDs (3) | WRITE score | QUIZ IDs (5) | QUIZ misses | CHAIN ID | CHAIN score | +24h due | +48h due | Next-review dates armed |
|---|---|---|---|---|---|---|---|---|---|
|    | 13-__ · 13-__ · 13-__ | /5 · /5 · /5 | __ · __ · __ · __ · __ |    | 14-__ | /5 |    |    | 13-__ → +24h/ +48h |
|    |    |    |    |    |    |    |    |    |    |

Repeat for all 7 rows; each row pre-prints the day's fixed IDs from Part 1.1 so filling is a numbers-only act. The "Next-review dates armed" column is where the +24h/+48h override dates get written — a row that leaves it blank is a row with an unlocked 24h lane.

### TABLE B — WEEKLY DEEP SESSION LOG (one row per week, 4 rows per cycle)

| Date | ROUND played | 7-axis totals | INCIDENTs run | Method score | WRITE batch | Batch ≤3 count | BULLETs defended | MUST FIX carry-over |
|---|---|---|---|---|---|---|---|---|
|    | ROUND __ (T/R/S/B/H/F) | /70 | INC __ + INC __ | /5 (narrated) | 13-__ .. 13-__ |    | 16-__ .. 16-__ |    |

The MUST FIX carry-over column is the input to the next week's daily slots — copy it verbatim into Table A's +24h column on Monday. The 7-axis totals column should show the six sub-scores plus the /70, not a single average: one number hides which axis died.

### TABLE C — 7d / 14d / 30d ROUTER LOG

| Pass | Theme (source week) | Date due | Items (FT/SA / INCIDENTS / CHAIN) | Score | Must-repeat items (→ next pass) | Next review date |
|---|---|---|---|---|---|---|
| +7d QUIZ |    |    | FT-__ … SA-__ | /5 |    |    |
| +14d DEBUG+CHAIN |    |    | INC __, __ · 14-__ | /5 |    |    |
| +30d TEACH+MOCK |    |    | ROUND __ | /10×7 |    |    |

### TABLE D — T-MINUS TAPER CHECKLIST

| Checkpoint | Date | Items (all with explicit IDs) | Done |
|---|---|---|---|
| T-30d |    | ROUND 1 + ROUND 2 cold · 13-01..13-12 full P0 batch · LIE-DETECTOR rewrite pass | [ ] |
| T-14d |    | ROUND 3 + ROUND 4 · 4-incident archetype relay (INC 02/12/16/28) · all ≤3 re-attempts at true due dates · sleep locked | [ ] |
| T-7d |    | ROUND 6 · 13-01..13-12 refresh · 14-chain L1 sweep · LIE-DETECTOR re-read · cram sheet built | [ ] |
| T-3d |    | ROUND 6 MUST FIX items only · ELEVATOR ×3 · STAR stories verified | [ ] |
| T-1d |    | cram sheet ×2 · ELEVATOR once · logistics done · bed on time | [ ] |
| T-night |    | bag check · cram sheet + incident blank page + ELEVATOR read once · lights out | [ ] |
| T-morning |    | cram sheet once · ELEVATOR once · no drills · arrive 30 min early | [ ] |

### THE SINGLE-PAGE DAILY SCORECARD (printer's version of Table A)

```text
DATE ______   DAY ______ (circle: Mon Tue Wed Thu Fri Sat Sun)

SLOT 1 WRITE   tasks: 13-__  13-__  13-__     scores: __ __ __    (≤3 → +24h/+48h = ______)
SLOT 2 QUIZ    5 IDs: ______ ______ ______ ______ ______   misses: ______
SLOT 3 CHAIN   chain 14-__   score __      red rows: ______   → +24h/+48h = ______

NEXT WEEKDAY'S ARM: ______   (tomorrow's slot opens with these before quota tasks)
```

### 7.1 THE WEEKLY ROLL-UP (one line per week, the month's spine)

| Week ending | Daily avg score | Weekly session score profile | Armed items cleared | New files mastered | Next review debt |
|---|---|---|---|---|---|
| W1 | /5 | ROUND __ /70; INC method __/5 | /N |    |    |

The roll-up is the only sheet an interviewer's preparation never sees — it is your own control chart. A month whose roll-up shows a falling daily average while the weekly session stays flat means the daily loop is decaying (drift, lazy grading) : correct the grader, not the material.

### WHAT TO DO WITH A SAME-SCORE PATTERN

If the same task scores a 3 three weeks running (same WRITE score, same +7d miss), the surface loop is not the problem — the source session is under-taught. Stop re-drilling the task and re-run its ruling session end-to-end (each task in file 13 names its source): re-read the 16-part template section, re-run the file's relevant BUILD section, and re-attempt the task only after the session. Then the whole item graduates to a +24h lane as if it were new. Same-score persistence is the signal that retrieval practice is running ahead of encoding; only re-encoding fixes it. The same rule applies to a chain row that has been red through two whole rotation cycles: re-run the chain's Source sessions (file 14's map at the top of each chain), then re-drill.

### HOW TO READ THE SHEETS IN THE TAPER

From T-14d the sheets are read backwards: you read the MUST FIX columns, not the scores. The taper's whole job is clearing the columns marked "next review" that carry a real date. Any debt row that survives T-7d is exactly the item the interviewer will find — because you wrote it down yourself as the thing you could not hold.

### TABLE E — MOCK ROUND SEVEN-AXIS SHEET (one page per round)

| Axis | Score /10 | What I actually said (quote the recording) | The line I froze on | Fix (→ +24h lane) |
|---|---|---|---|---|
| Technical accuracy | | | | |
| Reasoning & structure | | | | |
| Communication | | | | |
| Depth & nuance | | | | |
| Follow-up defense | | | | |
| Production judgment | | | | |
| Uncertainty handling | | | | |

Quote the recording, not the memory — a frozen line you cannot quote is a line you were never going to fix. The Fix column feeds Table A's +24h column verbatim on the next daily slot.

### TABLE F — INCIDENT NARRATIVE LOG (one row per incident)

| Date | INCIDENT | Skeleton steps narrated in order | Symptom sentence | First check + why | Root cause pre-fix | Method /5 | The class first-check I should have opened with |
|---|---|---|---|---|---|---|---|

The last column is the 14d-pass's memory aid: the archetype map (3.3) gives each class a first-check, and the column accumulates that check until it is automatic. INCIDENT 01 through INCIDENT 30 each get a row, filled during Block 2 of the weekly loop — never "later."

### TABLE G — THE MONTHLY DASHBOARD (one row per month)

| Month | Weakest axis (from Table E) | Weakest domain (from Table B ≤3 counts) | Deep-dive target (5.7) | MUST FIX carried into the taper | Next month's single improvement |
|---|---|---|---|---|---|

The dashboard is read once a month at the 30-day pass and is the only sheet allowed to carry prose — "the uncertainty axis never scored above 6 in February" beats fourteen scores nobody re-reads.

### THE DEBT LEDGER

Every armed item that survives its +24h and +48h dates still-unproven gets a row here. Columns: item · first failed · times re-attempted · source session to re-run · next attempt date. The ledger is the taper's first read from T-14d onward, because a debt that survived a month is exactly the phrase an interviewer will burn you on — you wrote it down yourself. A row closes only when the item scores 5 at +48h after a full re-run of its source session; closing it by deletion is the one administrative sin this file forbids.

### 7.2 WORKED EXAMPLE ROWS (how the templates look filled)

**A worked Table A row (Wednesday, rotation week 3):**

| Date | WRITE IDs (3) | WRITE score | QUIZ IDs (5) | QUIZ misses | CHAIN ID | CHAIN score | +24h due | +48h due | Next-review dates armed |
|---|---|---|---|---|---|---|---|---|---|
| Wed | 13-13 · 13-14 · 13-15 | 5 · 4 · 3 | FT-139 · FT-142 · FT-143 · SA-237 · SA-248 | FT-142 (HPA math frozen at the maxReplicas cap) | 14-09 | 4 | 13-15 → Thu · FT-142 → Thu | 13-15 Fri · FT-142 Fri | 13-15 + FT-142 |

**A worked Table B row (week 1):**

| Date | ROUND played | 7-axis totals | INCIDENTs run | Method score | WRITE batch | Batch ≤3 count | BULLETs defended | MUST FIX carry-over |
|---|---|---|---|---|---|---|---|---|
| Fri | ROUND 1 (T) | 7·8·6·6·5·7·7 = 47/70 | 01 + 03 | 3/5 + 4/5 | A: 13-01..13-08 | 1 (13-02) | 16-01..16-04 | FT-122 · 14-07 L2 · first-check discipline · 16-01 STAR |

**A worked Table C row (foundations, +7d):**

| Pass | Theme (source week) | Date due | Items (FT/SA / INCIDENTS / CHAIN) | Score | Must-repeat items (→ next pass) | Next review date |
|---|---|---|---|---|---|---|
| +7d QUIZ | Foundations (wk 1) | +7d | FT-101/105/106/111/113/115 · 5 SA from SA-161..SA-197 | 4/5 | FT-105 (StrictMode: still the client-side 0644 miss) | +14d as a re-quiz |

**A worked Table F row (weekly, INCIDENT 04):**

| Date | INCIDENT | Skeleton steps narrated in order | Symptom sentence | First check + why | Root cause pre-fix | Method /5 | The class first-check I should have opened with |
|---|---|---|---|---|---|---|---|
| Wed | 04 | 9/9 | "users see 502 on ALB, backend healthy" | `curl -v` the target directly, because 503≠502 tells you whether the group is empty | yes — target registered but failing health checks | 4 | A: refused-vs-timeout first, before any target-group theory |

The worked rows are not aspirational formatting; they are the level of specificity — real IDs, real clock lanes, real archetype names — that keeps a filled sheet from being a decorated diary.

---

## APPENDIX — ID INDEX (every sibling-file ID this plan cites, resolved)

Derived from the verified contents of files 12–17 as this file was written. Every ID named in this file exists at the cited location; the mapping is one-to-one, not illustrative.

### APPENDIX A — THE QUESTION BANK MAP (file 15)

| ID range | Count | What the range is | First appearances in this file |
|---|---|---|---|
| FT-101 … FT-160 | 60 | full-treatment questions (write the answer, then the mechanism, then one sentence) | Part 1.1 daily QUIZ · router 3.1 rows · taper |
| SA-161 … SA-300 | 140 | short-answer questions (one sentence under 30s) | Part 1.1 · router 3.1 · scoring gates throughout |

### APPENDIX B — THE ATTACK CHAIN MAP (file 14)

| Chain | Domain | Where this file runs it |
|---|---|---|
| 14-01 LINUX · 14-02 NETWORKING · 14-03 GIT · 14-04 BASH | Foundations | daily CHAIN slot, rotation week 1 · router w1 · 7d pass |
| 14-05 AWS · 14-06 DOCKER · 14-07 KUBERNETES · 14-08 TERRAFORM | Cloud · containers · provisioning | rotation weeks 2–3 · router w2/w4/w5 · 14d pass |
| 14-09 CI/CD · 14-10 OBSERVABILITY · 14-11 SECURITY · 14-12 TROUBLESHOOTING | Delivery · operate | rotation weeks 3–4 · router w6/w7/w8 |
| 14-13 SYSTEM DESIGN · 14-14 BEHAVIORAL | Cross-cutting | rotation week 4 · router w8 · taper L1 sweep |

### APPENDIX C — THE INCIDENT MAP (file 12, by archetype)

Archetype A reachability (INCIDENT 01–08), B identity/authorization (09–15), C orchestration/state (16–23), D delivery (24–30). The relay exemplars are INCIDENT 02 (A), 12 (B), 16 (C), 28 (D); the archetype signature and separating first-check live in 3.3.

| Archetype | Incidents | Verified titles used in this file | Where this file runs them |
|---|---|---|---|
| A · Reachability | 01–08 | 01 kubectl connection refused · 03 DNS fails inside a pod · 04 ALB 502/503 · 05 TLS expired · 06 intermittent timeouts under load · 15 ssh publickey | weekly rotation w1/w3 · router +7/+14 rows · taper relay |
| B · Identity/Authorization | 09–15 | 09 S3 AccessDenied · 10 kubectl Forbidden · 11 AssumeRole fails · 12 Secret mount · 13 IRSA no creds | weekly rotation w2 · router w2/w7 · taper relay |
| C · Orchestration/State | 16–23 | 16 CrashLoopBackOff · 17 ImagePullBackOff · 18 Pending unschedulable · 19 OOMKilled · 20 readiness failing · 22 state lock + partial apply · 23 plan wants destroy/recreate | weekly rotation w2/w3 · router w4/w5 · taper relay |
| D · Delivery | 24–30 | 24 CI fails locally-passing tests · 25 stale layers / wrong artifact · 26 OutOfSync won't self-heal · 27 rollout stuck · 28 bad deploy — rollback vs forward-fix · 29 pipeline green, site on old version · 30 secret in git | weekly rotation w3/w4 · router w6/w8 · taper relay |

### APPENDIX D — THE RESUME BULLETS (file 16) AND THE ROUNDS (file 17)

| Bullet | Claim topic | First defended at |
|---|---|---|
| 16-01 CI/CD pipelines · 16-02 AWS infra · 16-03 Terraform modules · 16-04 containers + Kubernetes | operational breadth | weekly week 1, Block 4 |
| 16-05 monitoring/alerting · 16-06 hardening/security · 16-07 Linux automation · 16-08 git workflows | operational depth | weekly week 2 |
| 16-09 incident debugging · 16-10 IaC + config mgmt · 16-11 state/persistence · 16-12 networking: DNS/LB/TLS | the mechanisms | weekly week 3 |
| 16-13 observability pipelines · 16-14 cost/capacity · 16-15 dev environment support · 16-16 platform ownership · 16-17 architecture input · 16-18 runbooks/docs | breadth + honesty | weekly week 4 · taper LIE-DETECTOR |

| Round | Duration | Role in this plan |
|---|---|---|
| ROUND 1 · T | 45 min | calibration: breadth (weekly w1 · router 30d · taper T-30d) |
| ROUND 2 · R | 60 min | calibration: narration (weekly w2 · taper T-30d) |
| ROUND 3 · S | 60 min | calibration: design (weekly w3 · router w3/w6 · taper T-14d) |
| ROUND 4 · B | 45 min | calibration: hostile probe (weekly w4 · taper T-14d) |
| ROUND 5 · H | 90 min | certification: hybrid (30d pass · router w4/w8) |
| ROUND 6 · F | 90 min | certification: final comprehensive (taper T-7d) |

### APPENDIX E — THE 24H/48H HANDLER MAP

| Score event | Handler | Where |
|---|---|---|
| TASK ≤3 | +24h + +48h re-attempts, then Sunday deficit lane, then +7d QUIZ, then source re-run | Part 6 · 1.3 · 1.8 |
| Chain row <4 | +24h/+48h full-speed re-drill of that row; red-until-green | 6.2 · 1.2 |
| FT <4 in a mock | re-quiz + FT's source re-read; routes to +7d | 6.5 · 2.1 |
| SA stagger | one-sentence re-answer + source re-study | 6.8 |
| Bullet fails the 3-probe | +24h re-run AND the claim downgrades one level | 6.6 |
| Missed due date | marked ≤3-equivalent; the counter restarts at the real attempt | 6.4 · 6.9 |

### APPENDIX F — THE FILE-BY-FILE QUICK INDEX (files 00–17)

| File | What it holds (as this plan uses it) |
|---|---|
| 00-architecture | phases 0–5 · the spine · the BUILD→VERIFY→…→DEFEND loop · 7-axis rubric · claim levels · 6-round set |
| 01-linux | LINUX.P0.1–P0.8 (signals, process states, ssh, permissions) |
| 02-networking | NET.P0.1–P1.1 (CIDR, HTTP taxonomy, DNS, L4/L7) |
| 03-git | GIT.P0.1–P0.7 (reset vs revert, reflog, workflows) |
| 04-bash | BASH.P0.1–P1.1 (scripting, `set -euo pipefail`, exit codes) |
| 05-aws | AWS.P0.1–P0.10 (IAM, VPC, EC2/EBS, S3, ALB, Route 53, EKS) |
| 06-docker | DCK.P0.1–P1.1 (multi-stage, non-root, run hardening) |
| 07-kubernetes | K8s.P0.1–P0.9 + P1.4 Helm (control plane, objects, probes, RBAC) |
| 08-terraform | TF.P0.1–P0.7 (HCL, state, modules, partial apply) |
| 09-cicd | CICD.P0.1–P0.8, P1.1–P1.4 (Actions, Jenkins, ArgoCD, artifact rule) |
| 10-observability | OBS.P0.1–P2.2 (pillars, PromQL, SLO, alerting) |
| 11-security | SEC.P0.1–P2.2 (IAM, IRSA, RBAC, network, secrets, supply chain) |
| 12-troubleshooting | INCIDENT 01–30 · 9-step skeleton · four archetypes |
| 13-write-without-google | TASK 13-01…13-26 · weekday batches · 0–5 rubric · 48h rule |
| 14-attack-chains | CHAIN 14-01…14-14 · drill rotation · L1–L3 clocks |
| 15-question-bank | FT-101…FT-160 · SA-161…SA-300 |
| 16-resume-defense | BULLET 16-01…16-18 · LIE-DETECTOR LIST · ELEVATOR · 3-probe · claim levels |
| 17-mock-interviews | ROUND 1–6 · 7-axis scoring · round matrix |

---

## RULES THAT TRUMP EVERYTHING

1. **The loops are a floor, not a ceiling.** If an interviewer question breaks a model you thought you owned, that model is tomorrow's WRITE task and this week's 7-day pass — regardless of where the file-cycle is.
2. **Honesty over completion (files 00/16).** Any drill you cannot score — or would have to fake — is re-studied, not ticked. The tracking sheets exist to show you the gap, and the taper exists to downgrade the claim before a room hears it.
3. **Rest is a scheduled loop.** The decay model cuts both ways: sleep is when recall strength consolidates. The taper's sleep lock (T-14d) is a fixed block, not a lifestyle note.
4. **Every loop writes to Part 7.** A session that ends without a log row is, by this file's definition, a session that never ran.
5. **Never study a scored item on interview day.** Recognition and recall blur under adrenaline; the morning of, you read the cram sheet and speak the ELEVATOR — nothing else. The taper is where the risk is closed, not the morning of.
6. **A missed date is a scoring event, never a reset.** The +24h/+48h due dates hold; the sheet marks the miss, the debt accrues, and the next pass starts the counter from the real attempt day (6.4). This one rule keeps every other rule honest.

---

## QC CHECKLIST — FILE 18

| # | Check | Status |
|---|---|---|
| 1 | Header present: title, one-line framing, decay model, activation modes list | PASS |
| 2 | MASTER MATRIX maps every activation mode → loop → sibling file sections → frequency | PASS |
| 3 | 15-min daily loop has 3 named write tasks, 5 named SA/FT picks, 1 named chain, and a Mon–Sun 3-slot rotation table | PASS |
| 4 | 1-hour weekly loop has a mock round, live-debug incidents, a full write batch, and a resume-defense pass, with a 4-week rotation table | PASS |
| 5 | 7d / 14d / 30d loop tables name concrete source files and session groups per row | PASS |
| 6 | Pre-interview taper covers T-30d / T-14d / T-7d / T-3d / T-1d / T-night / T-morning with real actions | PASS |
| 7 | 8-week subject rotation calendar maps week → phase (0–5) → files → primary loop | PASS |
| 8 | 24-hour and 48-hour rules recapped from file 13 (and chain/FT variants) and integrated into every loop | PASS |
| 9 | Tracking sheet templates per loop with date / task IDs / score / next review date columns | PASS |
| 10 | All fenced code blocks balanced (even count of fence markers) | PASS |
| 11 | No emojis anywhere (typography limited to — · →) | PASS |
| 12 | No TODO / FIXME / placeholder wording in the body | PASS |
| 13 | SELF-VERIFY — all cited IDs verified to exist in files 13–17 | PASS |

VERDICT: **PASS** — the revision engine is complete: every loop, router row, taper checkpoint, and calendar week resolves to a real task, question, chain, incident, bullet, or round in files 12–17, and every schedule writes its evidence to a tracking sheet so "did I study" is a logged fact, never a feeling.