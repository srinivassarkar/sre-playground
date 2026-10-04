# GIT — INTERVIEW WAR ROOM (1–3 YOE)

Priority: **P0 domain.** Git/PR is labeled "Critical" for 1–3 YOE across JD sources (architecture
§AD-1); it underpins the CI/CD and GitOps domains later. Every session follows the same 16-part
template and closes with a 13-point QC checklist (item 13 = **SELF-VERIFY**). Labs are verified
**live on this box** (git 2.43.0) before being written down; hashes, trees, and states are real runs.
Tools verified present: `git`, `git cat-file`, `git hash-object`, `git ls-tree`, `git reflog`, `diff`.

## Reaching prerequisites

Git needs plain shell literacy (Bash domain, interleaved with this one) and a working-tree notion —
Linux **P0.1 (processes/files)** is enough; nothing else in the stack gates on git, but the
CI/CD → GitOps (ArgoCD) spine reuses this domain's vocabulary heavily.

## Git priority map

- **P0 (full 16-part template):** core model (snapshot/object DB/three states) · add/commit lifecycle ·
  branches (fast-forward vs merge) · merge-vs-rebase · reset-vs-revert · fetch-vs-pull ·
  conflicts + resolution · reflog recovery
- **P1 (condensed):** `git bisect` · worktrees · signed commits · submodules (what they are)
- **P2 (compact):** packfiles, `filter-repo`, hooks
- **Ignore:** LFS nuances, subtree debate

## Domain session log

| ID | Topic | Priority | Status | QC |
|---|---|---|---|---|
| GIT.P0.1 | Core model: snapshot, object DB, three states | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P0.2 | Add/commit lifecycle: index, diff, log | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P0.3 | Branches: pointers, fast-forward vs merge commit | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P0.4 | Merge vs rebase + interactive rebase | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P0.5 | Reset vs revert (soft/mixed/hard) + reflog recovery | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P0.6 | Fetch vs pull, remote tracking branches | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P0.7 | Conflicts + resolution playbook (end-to-end incident) | P0 | **COMPLETE** | PASS · lab-verified |
| GIT.P1.1 | Bisect, worktrees, signed commits, submodules | P1 | **COMPLETE** | PASS · lab-verified |

---

# SESSION GIT.P0.1 — CORE MODEL: SNAPSHOTS, OBJECT DATABASE, THREE STATES

Environment note: verified live on this box with git 2.43.0 in a throwaway repo — object hashes,
tree contents, and index/staging rows below are real outputs. Commands are non-destructive and
repeatable in `/tmp`.

## 1. WHAT IS IT? (≤30 s)

Git is a **content-addressed snapshot store**. A commit is a full snapshot of the project — a tree
of blobs — with a pointer to its parent. Nothing is ever kept as a diff. Branch **names are just
labels pointing at commits**. And every file lives in one of **three states**: working tree,
index (staging area), or the repository (committed to the object database).

## 2. WHY DOES IT EXIST?

Because every painful question in day-to-day git — "why isn't my change in the commit," "why did
merging produce a huge diff," "how did we lose the last 3 commits" — is answered by the same three
ideas. Snapshots make fast-precision queries possible (any commit = the whole project, no patch
math). Content addressing makes changes cheap and identical content free (same content → same hash →
stored once). The three states exist so you can **stage one thing and commit it while leaving
another work-in-progress** — the engineer's "deckside prep" versus "what actually ships."

## 3. HOW DOES IT WORK?

- **The object database** lives in `.git/objects` and holds four object types. Git addresses objects
  by the SHA-1 of their content AND header — `git hash-object` computes it; identical content yields
  the identical hash (verified: `<hello world>\n` hashes to `3b18e512…` every time). Types:
  - **blob** — a file's content, nothing else. No path attached (paths live in the tree).
  - **tree** — a directory: a sorted list of `<mode> <type> <sha> <name>` rows (verified below:
    `100644 blob 6f614c… README.md`, `040000 tree 755d89… src`).
  - **commit** — a snapshot record: tree SHA, parent SHA(s), author/committer, message. `git rev-parse
    HEAD` = the commit's SHA; `HEAD^{tree}` dereferences to the tree.
  - **tag** — a fixed name pointing at a commit (annotated tags carry their own object).
- **Path: a file has three addresses.**
  ```
  working tree   /repo/README.md              (what the editor sees)
  index          .git/index — from git add    (what the next commit WILL hold)
  repository     .git/objects — from commit   (what HEAD points at)
  ```
  Verified end-to-end: untracked files show as `??`; `git add` moves them into the index
  (`git ls-files --stage` row: `100644 6f614c… README.md`); `git commit` writes the objects, updates
  `refs/heads/master`, and moves HEAD — `cat .git/HEAD` → `ref: refs/heads/master`, and that ref now
  holds the new commit SHA. Editing after staging shows the file as ` M` (unstaged change) while
  `git diff` shows only the working-tree change — two diffs, two lists: `git diff` = working vs index,
  `git diff --cached` = index vs HEAD.
- **Branches are labels, branches are NOT containers.** HEAD is a symbolic ref (`ref: refs/heads/
  master`); the branch ref points at a commit. Creating a branch just adds another label; moving a
  branch = moving a label. There is no separate "copy" of the repo for each branch — only labels over
  one shared object store.

## 4. MENTAL MODEL

```
        ┌─ working tree ──┐  ┌─ index ──┐  ┌─ repository (.git/objects) ─┐
 editor │ real files      │→│ git add  │→│ git commit → commit → tree → blobs │
        └─────────────────┘  └──────────┘  └──────────────▲──────────────────┘
                                              branch ref ──┘
                                              HEAD = symbolic ref → branch ref → commit
Same content ⇒ same SHA ⇒ stored once (content addressing)
Commits = snapshots; parents make history; names are labels.
```

## 5. INTERVIEW-SAFE ANSWER

"Git stores snapshots, not diffs. Every commit points to a tree, which is a directory listing of
blobs — so the same file can be stored once and referenced from many commits (content addressing).
Files live in three states: the working tree, the index (what `git add` populates), and the object
database (what `git commit` writes). Branches are just labels on commits — HEAD is a symbolic ref that
says which branch label is checked out. I verified this live: staging a file shows its row in
`git ls-files --stage`, committing moves it into `.git/objects`, and `cat .git/HEAD` shows the
symbolic ref pointing at a branch ref that holds the commit SHA. The consequence I lean on daily:
the 'lost change' and 'wrong file in commit' classes of incident are always a three-state confusion,
not a fault of git."

## 6. FOLLOW-UP ATTACKS

**Q.** If commits are snapshots, how does `git log -p` show diffs so fast?
**A.** Diff is computed on demand between two snapshots (tree1 vs tree2). The store keeps no diffs;
`git diff A B` walks the two trees and prints what changed. That's why "it's snapshots" and
"`git log -p` works" are consistent.

**Q.** Why does git use SHA-1 bytes and what does "content-addressed" mean?
**A.** The address of an object is derived from its content (and type/size header) — same content,
same address. So dedup is automatic: the two files versioned via symlink-free object store share the
blob if identical. It also means tampering breaks the hash chain — the content that reaches the
wrong hash is a visibly different object.

**Q.** What exactly is in `.git/objects` after `git add` but before `git commit`?
**A.** The blobs (and later during write-tree/commit, trees + commit). `git add` writes the blob;
`git commit` writes the trees and the commit object, then moves the branch label. That's why you can
see staged blob hash via `git ls-files --stage` before any commit exists.

**Q.** What is the index exactly — a file?
**A.** Yes: `.git/index` — a binary staging file listing mode, blob SHA, and path per staged entry.
`git ls-files --stage` reads it. This is why `git add` and `git commit` are separate: the index is a
real intermediate artifact.

**Q.** What's `HEAD` when it's detached?
**A.** Normally HEAD is a symbolic ref (checks out a branch label). Detached means the label is gone
and HEAD points literally at a commit SHA — you're on a nameless checkout. Changing files and
committing there leaves the commit label-less (recoverable via reflog later in this domain).

**Q.** When would identical content get different hashes?
**A.** If type or size header differs (a blob vs a tree of same payload, different lengths) — or
different content always. That's the fix-point of the model: the hash pins content+type+size.

**Q.** Do merges change the object database shape?
**A.** A merge commit is just a commit with two parents (P0.3). Same snapshot structure, two parent
rows. Nothing else changes in the DAG.

## 7. PRACTICAL EXAMPLE (production)

"Why didn't my deployment include my fix?" → engineer made the change, ran a one-liner they thought
committed, and the pipeline built from `HEAD`. The fix was in the working tree but **not staged** —
`git status` would have shown ` M file.py`, `git diff --cached` empty. Fix: `git add file.py &&
git commit -m`. The preventive habit: before any commit, run `git status --short` and read the letter
in column one (`A` staged, ` M` modified-unstaged, `??` untracked); run `git diff --cached` to review
exactly what the next commit WILL contain — not what the editor sees.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 1 — the three states, end to end (VERIFIED)
cd /tmp && rm -rf git_demo && mkdir git_demo && cd git_demo
git init repo && cd repo
git config user.email lab@warroom.local && git config user.name "War Room Lab"
echo "## readme" > README.md           # working tree only
git status --short                     # VERIFIED: ?? README.md
git add README.md
git ls-files --stage                   # VERIFIED: 100644 6f614c… README.md   → index row
find .git/objects -type f              # VERIFIED: only the blob 6f/614c…
git commit -q -m "seed"
git rev-parse HEAD                     # commit SHA (e.g. da69024…)
cat .git/HEAD                          # ref: refs/heads/master
git cat-file -t HEAD                  # commit
git rev-parse HEAD^{tree}              # tree SHA 3bf4692d…
git cat-file -p HEAD^{tree}            # 100644 blob 6f614c… README.md
# content addressing (identity of blobs):
echo "hello world" | git hash-object --stdin    # VERIFIED: 3b18e512… (same every run)
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "I committed, but my change isn't in the commit"

Trigger: engineer edits, runs `git commit -m "fix"` — no error — but the file in the repo still has
the old content and CI silently built the old code.
Observe: `git status` — the file shows ` M` in column one (working-tree change, not staged);
`git diff --cached` — empty (nothing staged); `git show HEAD` proves HEAD lacks the change.
Scope: three-state confusion. The commit DID happen (a snapshot was written) — but it snapshotted the
*index*, which never received `git add`. Root cause: forgetting the explicit staging step.
Fix: `git add <file> && git commit -m "fix"` — the previous commit never changes (immutable history);
the fix lands as a new commit containing exactly what was staged.
Verify: `git show --stat HEAD | grep fix-file` or `git log -1 -p -- <file>`.
Prevent: review `git diff --cached` before committing; wire a pre-commit check that the list of
staged paths matches the ticket's files (many CI gates do this).

### DECISION OVERLAY — what NOT to do

- Don't `git add .` before reviewing what is actually staged — you stage vendored junk and secrets
  in the same move.
- Don't assume `git commit -a` covers brand-new files — it stages tracked-file modifications only;
  untracked files are still missed (that's another classic "my new file isn't in the commit").
- Don't rely on the editor's "Checkmark = saved" — git never sees the file until `git add`.
- Don't hand-edit `.git/index` or `.git/objects` — it's composite data; lose the index and the
  working tree's state must be re-derived (`git reset --mixed HEAD` re-stages from HEAD).

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Git stores diffs" | Stores snapshots; diffs are computed on demand. |
| "A branch is a copy of the repo" | A branch is a movable label on commits (one shared object store). |
| "`git commit` commits my working changes" | Commits the INDEX; un-staged edits stay out. |
| "Status letters are all the same" | Two columns: X = index state, Y = worktree state. `A` = staged; ` M` (space-M) = modified-but-unstaged; `??` = untracked. |
| "Same file in two commits is stored twice" | Content addressing dedups identical blobs. |
| "HEAD is the branch" | HEAD is the symbolic ref; the branch ref is whom it points at. |
| "Commit = diff + message" | Commit = snapshot (tree) + zero-to-many parents + metadata + message. |
| "Hash is random" | Deterministic content+type+size hash; identical → same. |
| "Deleting the repo file deletes history" | The blob lives in the object DB until GC; checkout can restore any committed snapshot. |
| "Status shows the whole truth" | Shows three-state truth, not remote truth — remotes are P0.6. |

## 13. FIRST-CHECK REASONING

- **"My change isn't in the commit."** Check `git status --short` column 1 for ` M` first (unstaged),
  then `git diff --cached` (is it even staged?), then `git log -1 --name-status` (did the commit
  reference the file at all?). The first of those that surprises you names the missed state. That
  ordering — working → index → HEAD — is exactly the three-state ladder.
- **"Why is this repo huge / identical files everywhere?"** Content addressing should have deduped
  identical blobs; huge means mostly-unique content per commit — check `git rev-list --objects --all
  | wc -l` vs `du .git/objects` to distinguish dedup (cheap) from genuinely new content (expensive).

## 14. PRIORITY

**P0 — first git session; everything in this domain, plus CI/CD, builds on these three ideas.**

## 15. STOP HERE — done when you can…

1. name the four object types with their roles, and which one carries file content;
2. run the Lab 1 command chain (init → edit → add → ls-files --stage → commit → cat-file through
   tree → blob) without notes;
3. explain "snapshots, not diffs" and prove content addressing with `git hash-object`;
4. describe the three states with one `git status --short` line for each;
5. diagnose a "committed wrong thing" incident and give the three-state-first-check.

## 16. DO NOT STUDY YET

Packfiles/delta compression internals, `git replace`, graft/shallow manipulations, filter-repo,
multi-index/object-dir mechanics, SHA-256 repos (upcoming, not current), hooks (P2). Know the object
DB is compressed into packfiles; exact format is out of scope.

---

## QC CHECKLIST — GIT.P0.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (working → index → repo, HEAD → branch → commit)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (blob/tree/commit object DB, three states, symbolic ref)? | ✔ §3 |
| 5 | Dependencies (Linux file model; nothing gates on git)? | ✔ header |
| 6 | Essential commands (`git status -s`, `ls-files --stage`, `cat-file`, `hash-object`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 1)? | ✔ every output verified live |
| 8 | Break it (missed-staging incident, `git add .` trap)? | ✔ §8, §9 |
| 9 | Observe + interpret (status letters, diff vs diff --cached)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P0.2 — Add/commit lifecycle: the index,
`git diff` (unstaged vs staged), `git log`, and what every conflict-free commit path looks like.**

---

# SESSION GIT.P0.2 — ADD/COMMIT LIFECYCLE: THE INDEX, DIFF, LOG, AMEND

Environment note: verified live with git 2.43.0 (throwaway repo in `/tmp`); every diff, status line,
and SHA below comes from that run.

## 1. WHAT IS IT? (≤30 s)

The daily loop: **edit → `git add` (stage) → `git commit` (snapshot) → `git log` / `git diff` (read
history)**. The index is the staging area you curate; `git diff` / `git diff --cached` show what's
changed against what; `git log` reads the commit DAG. `git commit --amend` rewrites the *last*
commit (new SHA, old one survives in the reflog).

## 2. WHY DOES IT EXIST?

Because a real task touches several files while being one coherent change, and "one commit per change"
is the hygiene that makes `git log`, review, and `git bisect` (P1.1) meaningful. The index lets you
stage *parts* of your work; the diffs let you see what you're about to commit before you commit it;
`git log` is the audit trail every incident starts from. Amend exists because "oops, typo in the
message" on your **local, unpushed** commit should not cost you an extra commit — but it must never be
used on history others already have.

## 3. HOW DOES IT WORK?

- **The two diffs proved live.** With a.txt and b.txt both edited, `git status --short` shows
  ` M a.txt` and ` M b.txt` (space-M = modified in worktree, not staged):
  ```
  git diff                # worktree vs index      → shows BOTH a.txt and b.txt
  git add a.txt
  git diff                # now shows ONLY b.txt   (a.txt is in the index)
  git diff --cached       # index vs HEAD          → shows ONLY a.txt (staged)
  git diff HEAD           # worktree+index vs HEAD  → shows BOTH
  ```
  That single run demonstrates the exact semantics: `--cached` is "what the next commit WILL contain",
  plain `git diff` is "what you haven't staged", and `HEAD` merges both. The porcelain letters do the
  same job in two columns (X = index, Y = worktree).
- **`git add` forms:** `git add <path>` (fine-grained), `git add -u` (tracked files only),
  `git add -A`/`-A` (tracked + untracked), `git add -p` (stage **hunks** interactively — partial
  staging; the "commit only the security-relevant hunk" move). `git add --intent-to-add` reserves a
  staged slot for a new file without content.
- **`git log` reads the DAG, not the index.** Verified first-run graph: `* 892fd55 (HEAD -> master)
  seed a+b`. Useful forms: `--oneline --graph --decorate --all` (the whole picture), `-p` (show each
  commit's patch), `--stat` (file-level numbers), `--follow -- <path>` (a file's history across
  renames), `--author=`, `--since/--until`, `-n`. `git show <sha>` = one commit's full record.
- **`git commit --amend` rewrites the label.** Verified: after amending, HEAD becomes `ff78a5f
  (a-v2 (fixed msg))` while `git reflog` still lists the old `d13340e commit: a-v2` plus the new one.
  The old commit is not erased — it is simply no longer reachable from a branch; the reflog can still
  reach it (this is the safety-net claim, deep-dived in GIT.P0.5).
- **`.gitignore` keeps junk out of the index.** Verified: adding `*.log` +commit, re-touching
  `logs/app.log` → `git status --short` shows ` M b.txt` only — no `?? logs/`. Patterns: `*.log` (any
  level), `/build` (root-anchored), `logs/` (dir), `!important.log` (re-include). Ignore rules shape
  the index; they do NOT remove already-tracked files (that needs `git rm`).

## 4. MENTAL MODEL

```
                    git diff                git diff --cached
      worktree   ─────────────►   index   ─────────────►   HEAD (last commit)
         │              (unstaged)            (staged)
         └────────────────────────────────────────────── git diff HEAD
edit → git add → git commit → git log (DAG) → git show <sha>
amend: move the label back one commit, snapshot again → NEW SHA; old SHA → reflog only.
```

## 5. INTERVIEW-SAFE ANSWER

"The index is what the next commit will contain. `git diff` shows worktree-vs-index, `git diff
--cached` shows index-vs-HEAD, and `git diff HEAD` shows both — I verified all three in one run by
staging only one of two edited files. `git log` reads the commit DAG (snapshots), so renames and
file history are questions you ask the graph, not the filesystem. `git commit --amend` rewrites the
last, unpushed commit — the SHA changes and the old commit stays reachable in the reflog, which I
verified by amending and reading the reflog rows. The discipline I'd defend: one commit per coherent
change, review `git diff --cached` before committing, never amend anything that reached a shared
remote."

## 6. FOLLOW-UP ATTACKS

**Q.** `git add -p` — why is partial staging important?
**A.** Real diffs mix concerns: a fix and a refactor in one file. `-p` lets you stage only the fix's
hunks, keeping commits atomic so review, bisect, and rollback stay meaningful. It's the practical
answer to "one change per commit."

**Q.** Amend vs new commit — when?
**A.** Amend is for rewriting a local, unpushed commit (message typo, missing file). If anything even
*possibly* reached a shared remote, amend + force-push rewrites history someone else has — the
incident below. Default: don't amend pushed commits; add a follow-up commit instead.

**Q.** Is `.gitignore` enough to keep a secret out of history?
**A.** No. Git tracks what was committed; adding a `.gitignore` rule later doesn't scrub blobs already
in the object DB — the secret persists in every clone's history (P0.2 → Security domain secret-scrub).
Ignore is a forward-looking boundary, not a scrubber.

**Q.** `git show HEAD` vs `git log -1 -p`?
**A.** Mostly the same single commit rendered as a record; `log -p` flows through the log machinery
(respecting `--max-count` etc.), `show` is the direct one-commit view. Pick whichever reads better in
your pipeline.

**Q.** Why does amend change the SHA even when only the message changed?
**A.** Because the SHA = hash of the whole commit object (tree + parents + author + committer +
message). Message change ⇒ object change ⇒ new SHA. That's why you can *never* rewrite a commit
invisibly.

**Q.** How do I see what was committed vs what is staged right now?
**A.** `git status --short` (porcelain, script-safe) then `git diff --cached` for the exact staged
content. In a script, `git diff --cached --name-only` for just the paths.

**Q.** What reset concept underlies clean staging on this box?
**A.** `git reset --mixed HEAD` (P0.5) unstages everything — index drops back to HEAD. More granular:
`git restore --staged <path>`.

**Q.** How do I build a commit message a team won't hate?
**A.** Imperative subject ≤50 chars ("Fix null deref in retry path"), blank line, then body explaining
*why* (not what — the diff is the what). Reference issue/ticket ID in the body. Same shape reviewers
and CI parse.

## 7. PRACTICAL EXAMPLE (production)

Ticket says "add flow-limit to retry engine." A teammate's one-liner `git commit -am "fix"` would
stage the whole working tree — including the WIP refactor you'd rather not ship. The disciplined path:
`git add -p retry.py` → stage only the limit hunks; `git diff --cached --stat` to confirm scope;
commit. Same story, staged granularly. The second production habit: **read `git status --short`
columns** — trust neither "it saved" nor "I hit commit" — and review `git diff --cached` before every
commit, because that is literally the diff your CI and reviewers will see.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 2 — two-diff trio, amend, ignore (VERIFIED)
cd /tmp && rm -rf git_demo2 && mkdir git_demo2 && cd git_demo2
git init -q repo && cd repo
git config user.email lab@warroom.local && git config user.name "War Room Lab"
echo alpha > a.txt; echo beta > b.txt; mkdir -p logs; echo x > logs/app.log
git add a.txt b.txt && git commit -qm "seed a+b"
echo alpha-v2 > a.txt; echo beta-v2 > b.txt          # edit both
git status --short                                    #  M a.txt   M b.txt  ?? logs/
git diff                                              # both files
git add a.txt
git status --short                                    # M  a.txt   M b.txt  ?? logs/
git diff                                               # b.txt only (a staged)
git diff --cached                                      # a.txt only (the upcoming commit)
git diff HEAD                                          # both
git commit -qm "a-v2"
git log --oneline                                      # d13340e a-v2 / 892fd55 seed
git commit -q --amend -m "a-v2 (fixed msg)"
git log --oneline -1                                   # ff78a5f a-v2 (fixed msg)  ← SHA changed
git reflog -3 --pretty="%h %gs"                       # ff78a5f (amend) / d13340e (commit: a-v2) / 892fd55 (initial)
printf '*.log\n' > .gitignore
git add .gitignore && git commit -qm "ignore logs"
touch logs/app.log && git status --short               # only  M b.txt  → app.log ignored
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "I amended a pushed commit, now the remote is behind"

Trigger: engineer fixes the message on a commit that a teammate already pulled; force-pushes.
Observe: teammate pulls → `git pull` reports divergent history / says "needed to force update";
one person's branch has `ff78a5f`, the other still `d13340e`; nobody's `git log` matches.
Root cause: amend rewrote the object graph (verified: SHA changes, old commit relegated to reflog);
the remote was pointing at a commit that no longer exists in the pusher's branch — and other clones
still hold/share the old one.
Fix: recreate the pre-amend commit locally (`git reflog`, pick `d13340e`, branch, cherry-pick) and
reset the remote branch, or — the not-fix — all collaborators pull with `--rebase` and agree to the
rewrite. Prevention: hard rule — amend only what never left your machine; if it's shared, add a new
commit. CI gate: "no force-push to protected branches" (common Actions/branch-protection setting).

### DECISION OVERLAY — what NOT to do

- Don't `git add -A` when untracked junk lives in the tree — you stage build outputs and secrets.
- Don't amend shared commits; rewrite local-only history.
- Don't delete `.gitignore` rules instead of understanding them — that's how `.env` gets committed.
- Don't use `git commit -a` to "skip staging" — it silently skips untracked files (repeats the
  GIT.P0.1 missed-file incident on a different axis).
- Don't read a teammate's force-push as "their mistake" in an incident — it's a history policy; decide
  the policy (protected branches) rather than blaming the command.
- Don't rely on `git diff` after `git add` to see the staged change — it will be empty; that's
  expected, use `--cached`.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`git diff` after `git add` shows my new change" | It's now in the index; plain diff is empty. Use `git diff --cached`. |
| "`git commit -a` stages everything" | Tracks modified TRACKED files; untracked files stay out. |
| "Amend is safe for pushed commits if forced" | Rewrites history others hold; broken sha convergence ensues. |
| "Amend edits the same commit in place" | New object, new SHA; old one stays in the reflog. |
| "`git log` shows file system state" | Reads the commit graph; the file system may be dirty. |
| "`.gitignore` removes committed files" | It ignores; tracked files need `git rm`. |
| "`git show` and `git log -p` differ in output" | Same commit record; different entry point into the machinery. |
| "All add forms are equal" | `<path>` vs `-u` vs `-A` vs `-p` have different teeth; use them deliberately. |
| "Deleted file at the editor is covered by `-a`" | It needs `git rm` or `git add` to record the deletion in the index. |
| "Status letter order is arbitrary" | X=index, Y=worktree; `M ` vs ` M` are different states entirely. |

## 13. FIRST-CHECK REASONING

- **"My commit has the wrong/extra file."** `git diff --cached --stat` first — that is literally the
  index you committed. If it's wrong: `git restore --staged <path>` to unstage, then re-commit
  (local, unpushed) or `git commit --amend` if the commit is already made.
- **"History looks different from what we pushed."** Pick between "who force-pushed?" (reflog/`git
  reflog` on the remote branch, and Origin's event feed) and "who amended locally?" (`git cat-file -p
  <sha>` on both SIDs to compare trees/messages). Amended SHAs differ even for identical content.
- **"Why is the log noisy?"** Not a git bug — a commit-hygiene bug: `git log --author=X --since`,
  and train the team on `-p` staging + imperative imperatives.

## 14. PRIORITY

**P0 — the daily loop; everything that follows (branches, merges, rebase, recovery) builds on it.**

## 15. STOP HERE — done when you can…

1. explain the three diff commands with one screen of `git status` as evidence;
2. stage selectively (`<path>`, `-A`, `-u`, `-p`) and say when each is the right call;
3. read `git log --oneline --graph --decorate --all`, `--stat`, `-p` fluently;
4. perform an amend and PROVE the old commit survives via reflog (Lab 2 step);
5. state the pushed-code amend rule and the first-check for a "wrong contents" commit.

## 16. DO NOT STUDY YET

Atomic/multi-index internals, `git notes`, `replace`, delta/packfile layout, `git worktree`
(P1.1), `filter-repo` (P2), reflog expiration tuning (grab the mechanism in P0.5, tuning later).

---

## QC CHECKLIST — GIT.P0.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (worktree→index→HEAD with the three diff arrows)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (two-diff semantics, add forms, amend→new SHA, ignore)? | ✔ §3 |
| 5 | Dependencies (GIT.P0.1 object DB; nothing external)? | ✔ §3 |
| 6 | Essential commands (`git diff --cached`, `status --short`, `log --graph`, `show`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 2)? | ✔ every output verified live |
| 8 | Break it (pushed-amend incident, blind `add -A`)? | ✔ §9 |
| 9 | Observe + interpret (X/Y columns, reflog `(amend)` row)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P0.3 — Branches: pointers on commits,
fast-forward vs three-way merge, when `git log` shows a merge commit and when it doesn't.**

---

# SESSION GIT.P0.3 — BRANCHES: LABELS, FAST-FORWARD, AND THE MERGE COMMIT

Environment note: verified live with git 2.43.0 — every graph/merge count below is a real run.

## 1. WHAT IS IT? (≤30 s)

A **branch is a movable label on a commit** — no copies, no separate repos (GIT.P0.1). Merging
combines two brought histories. If only ONE side advanced, the merge is a **fast-forward**: the
label just slides forward, no merge commit. If both sides diverged, git computes a **three-way
merge** using the common ancestor and creates a **merge commit** with two parents. `--no-ff` forces a
merge commit even when a fast-forward was possible.

## 2. WHY DOES IT EXIST?

Branches let many lines of work coexist without blocking each other. Fast-forward exists to keep a
trivial "just catching up" merge invisible in history; the merge commit exists to record that two
lines of work genuinely were joined — and that record is exactly what `git log --graph` and `git
bisect` need. Knowing which of the two a `git merge` is going to do tells you whether you'll get a
new commit at all.

## 3. HOW DOES IT WORK?

- **Fast-forward (FF), verified:** from `master @ c2`, branch `feature` adds `c3`; master hasn't
  moved. `git merge feature` produced the linear chain `* bfa98b8 c3 → * ab85c18 c2 → * c9ff6a6 c1`
  and `git log --merges | wc -l` = **0** — no merge commit; master's label simply slid forward to the
  same commit as feature. Merge = a pointer bump.
- **Three-way / merge commit, verified:** master adds `g-master` (eaf9851) while `feature2` adds
  `f-feature2` (df942b3) — both diverge from the common ancestor `bfa98b8`. `git merge feature2`
  produced `e253c6e Merge branch 'feature2'`, and `git show -s --pretty=%P HEAD` printed exactly two
  parents: `eaf9851` (the old master tip) and `df942b3` (feature2's tip). Anatomy of the married
  graph, exactly the classic `|\` merge diamond.
- **Three-way merge computation:** base-branch-merge is done by finding the common ancestor of the
  two tips (GIT.P0.1's DAG walk), then merging three snapshots (ancestor, ours, theirs). Files that
  matched on both sides vs the base need no work; mismatches signal a conflict (deferred to P0.7).
- **`--no-ff`, verified:** from master @ e253c6e, `tip` adds one commit — a pur e FF-able case. Merge
  with `--no-ff --no-edit` produced merge commit `2ba31cb` anyway; `git log --merges | wc -l` jumped
  to **2**. Use it when you want history to record "a branch was joined" even when it wasn't strictly
  required (e.g., feature-branch discipline, `--no-ff` on a release branch).
- **Labels are plain pointers, verified:** `git branch -v` printed four rows of `name → SHA + subject`
  (master at `2ba31cb`, feature at `bfa98b8`, …). Nothing but arrows. Deleting/creating a branch = 
  deleting/creating a row in `refs/heads/`.

## 4. MENTAL MODEL

```
linear = FF:    A ─ B ─ C  (label C slides; no merge commit)
                  \_ D ─ E
diverge:          A ─ B ─ C ─── M   (M = merge commit, parents {C, E})
                    \_ D ─ E ─────┘
merge commit anatomy: tree(snapshot) + parents[2] + message
--no-ff = force the diamond even when the fork was trivial
```

## 5. INTERVIEW-SAFE ANSWER

"A branch is a label on a commit, not a copy — `git branch -v` shows each label pointing at one SHA.
When I merge, git first asks 'have both sides advanced past a common ancestor?' If only one side did,
a fast-forward just slides the label forward — zero merge commits, verified with `git log --merges`
counting 0. If both sides diverged, git does a three-way merge: it walks back to the common ancestor
and merges from three snapshots, then records a merge commit whose `%P` shows two parents — I saw the
two-parent `e253c6e Merge branch 'feature2'` live. With `--no-ff` I forced a merge commit to appear
even when a fast-forward was possible, which is the tool for 'I want history to show this work was a
branch.' The practical tell: if `git log --graph` shows a diamond, a two-parent commit happened."

## 6. FOLLOW-UP ATTACKS

**Q.** When is a fast-forward a problem?
**A.** When you wanted history to remember the branch existed (features merged, release tagging, PR
review context). PR platforms typically re-merge with a merge commit or squash; local `git pull`
flat-follows by default (P0.6's `--rebase` discussion). Use `--no-ff` when the branch's existence
is the story.

**Q.** What is the "three" in a three-way merge?
**A.** Ancestor (common), ours (current tip), theirs (incoming tip). Git compares all three; a change
is a conflict only if ours and theirs both changed the same line differently from the ancestor.

**Q.** Can I see the common ancestor directly?
**A.** `git merge-base a b` — prints it. "Three-way" is meat that git, not the user, lives by.

**Q.** Why does `git log master..feature` show commits?
**A.** `master..feature` = commits east of master's pointer reachable from feature: things feature has
that master doesn't. That's the "what will this merge bring" lens (GIT.P0.5/P0.6 reuse it).

**Q.** Squash vs merge commit?
**A.** Squash folds a branch's commits into one new commit (no parents from the branch) — clean
history, lost granularity. Merge commit preserves the branch's commits and its two-parent diamond —
complete but noisier start.

**Q.** Is fast-forward "the same commit twice"?
**A.** Same SHA, same object, one label more. Labels are free; the object store is shared. That's why
`git branch feature && git switch feature` never duplicates a thing.

**Q.** Why does a merge sometimes need `--no-edit`?
**A.** Merges are committed non-interactively in pipelines because git opens an editor for the merge
message. Scripted runs pass `--no-edit` (or `-m`) to keep CI non-blocking.

## 7. PRACTICAL EXAMPLE (production)

Release trains: `main` cut to `release/1.2`; while 1.2 gets hotfixes, main jumps ahead with features.
Hotfix cherry-picked forward: `git switch main && git merge release/1.2` — if main hadn't moved at the
fork point, this is an FF (clean fast slide); if both moved, the three-way runs and you get a merge
commit you can point to in the release notes. Prefer `git merge --no-ff release/1.2` when wiring
release branches, so the join is a visible event. Verify before merging: `git log --oneline
main..release/1.2` to see exactly what would arrive.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 3 — FF vs three-way vs --no-ff (VERIFIED)
cd /tmp && rm -rf git_demo3 && mkdir git_demo3 && cd git_demo3
git init -q repo && cd repo && git config user.email lab@warroom.local && git config user.name "War Room Lab"
echo 1 > f.txt; git add f.txt; git commit -qm c1
echo 2 >> f.txt; git commit -qam c2
git switch -q -c feature; echo 3 >> f.txt; git commit -qam "c3 on feature"   # feature only
git switch -q master; git merge -q --no-edit feature
git log --merges --oneline | wc -l          # 0  ← fast-forward, label slide
git switch -q -c feature2; echo f >> f.txt; git commit -qam f-feature2
git switch -q master; echo m > g.txt; git add g.txt; git commit -qm g-master  # both moved
git merge -q --no-edit feature2
git log --merges --oneline                   # e253c6e Merge branch 'feature2'
git show -s --pretty=%P HEAD                 # <masterSha> <feature2Sha>  ← two parents
git switch -q -c tip; printf 't\n' >> f.txt; git commit -qam tip
git switch -q master; git merge --no-ff --no-edit tip >/dev/null 2>&1
git log --merges --oneline | wc -l           # 2  ← --no-ff forced one more
git branch -v                                # labels: name → SHA + subject only
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Merging release/1.2 back to main produced a 500-line diff we didn't expect"

Trigger: hotfix branch cut from a release tag, main kept moving; engineer merged "forward the hotfix"
and the PR exploded.
Observe: `git log --merges main..release/1.2` and `git log main..release/1.2 --oneline` — the incoming
side carries both the hotfix AND everything else that moved between base and merge; `git merge-base`
points far back. Scope: this is "three-way over a stale base" — the merge isn't wrong, but it has a
broad base.
Root cause: release branches and main diverged at an old base (or squash cherry-picks duplicated
commits). Fix when the goal is ONE fix forward: cherry-pick the hotfix commit itself with
`git cherry-pick <hotfixSha>` onto main, leaving the rest of release/1.2 behind. Verify:
`git show --stat HEAD` equals the intended hotfix; `git log main..release/1.2` still shows the rest.
Prevent: merge-release branches deliberately (`--no-ff`), or cherry-pick hotfixes and keep release
branches short-lived; review `..`-diff BEFORE merging, not after.

### DECISION OVERLAY — what NOT to do

- Don't merge a release branch into main when you only want to ship one fix — cherry-pick instead.
- Don't force `--no-ff` on feature merges if the team's history wants squash/FF squash flatten.
- Don't read "no merge commit" as "nothing happened" — FF moves the label silently; verify with
  `git log` on BOTH labels before/after.
- Don't merge a branch that was already merged in another order — git notices "already up to date";
  if the diff still surprises, it's the base story, not the merge.
- Don't leave `git draw` out of your routine: `git log --oneline --graph --all --decorate` shows the
  diamonds before you merge, so the merge is never a mystery.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Branches are copies / heavy" | Labels in `refs/heads/`; shared object store. |
| "Merge always creates a commit" | Fast-forward slides the label; `git log --merges` stays 0. |
| "Merge commit has one parent (history is linear)" | Merge = two parents by definition (diamond shape). |
| "`--no-ff` is only for won't-merge cases" | Use it to MAKE the branch's existence visible. |
| "Squash merge = the branch's commits with a fancier message" | Squash = one NEW commit, no branch parents. |
| "`git switch -b` copies the tree" | New label at your current HEAD; working tree shared. |
| "Common ancestor is always a merge-base" | Yes, via `git merge-base`; it's the fork point, not the fork commit. |
| "`..` in `log A..B` means 'also these magically'" | It means commits reachable from B but not from A. |
| "Merge fails = files lost" | Merge weeks merge-able; conflicts are per-line, resolved in P0.7 |
| "Branch names are the identity" | SHAs are identity; names are convenience arrows. |

## 13. FIRST-CHECK REASONING

- **"Will this merge produce a commit?"** `git merge-base --is-ancestor main feature` → yes ⇒ FF.
  Counter-knowledge `git log --oneline main..feature | wc -l` and zero on the master side ⇒ pure FF.
- **"Why is the incoming diff huge?"** Read `..`-diff and the merge-base first — the diff reflects the
  base's age, not the branch's size.
- **"Did my merge work right?"** `git show -s --pretty=%P HEAD` — two short SHAs plus clean status =
  a good merge; one parent + same content = the label slid.

## 14. PRIORITY

**P0 — branching is the backbone; merges are where CI/review/deployment decisions hang.**

## 15. STOP HERE — done when you can…

1. state the label model and prove it with `git branch -v`;
2. predict FF vs merge-commit from the DAG shape and verify with `git log --merges`;
3. read a diamond graph, interpret `%P` two-parent output;
4. use `--no-ff` deliberately and explain squash-merge as an alternative;
5. run the "huge incoming diff" first-check in under 30 s.

## 16. DO NOT STUDY YET

Ort/merge machinery internals, rename detection strategies (fine-tuning), octopus merges, `git notes`,
filter -tooling (P2), worktrees/tags beyond the label concept (P1.1 / tags in P0.5 area). Know what
tag = fixed label is; details later.

---

## QC CHECKLIST — GIT.P0.3

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (FF slide vs merge diamond vs --no-ff)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (FF, three-way/common-ancestor, two parents, --no-ff)? | ✔ §3 |
| 5 | Dependencies (GIT.P0.1 DAG + labels; zero external)? | ✔ §3 |
| 6 | Essential commands (`git merge`, `--no-ff`, `log --merges`, `show %P`, `merge-base`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 3)? | ✔ every output verified live |
| 8 | Break it (stale-base merge incident, surprise-diff)? | ✔ §9 |
| 9 | Observe + interpret (merges count, %P, diamond graph)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P0.4 — Merge vs rebase + interactive
rebase: linearizing your local history, `git rebase -i` mechanics, and the golden rules of when each.**

---

# SESSION GIT.P0.4 — MERGE VS REBASE AND INTERACTIVE REBASE

Environment note: verified live with git 2.43.0; every SHA before/after below is a real run.

## 1. WHAT IS IT? (≤30 s)

**Merge** joins two histories with a two-parent commit (or a label slide, GIT.P0.3). **Rebase**
re-plays your commits on top of another branch's tip — history becomes one straight line, but every
replayed commit gets a **new SHA**. **Interactive rebase** (`git rebase -i`) lets you reorder, drop,
squash, and reword commits while you re-play them. The golden rule: **rewrite only commits that never
left your machine.**

## 2. WHY DOES IT EXIST?

Two legit but different jobs need two different tools. Merging preserves the fact that work ran in
parallel (the diamond is the audit trail). Rebasing gives you a **linear, reviewable history** — every
commit builds on the next — which is what big teams demand on `main` and what `git bisect` loves.
Interactive rebase exists so you can shape a messy local branch ("wip", "fix typo", "again") into a
clean story before anyone else sees it.

## 3. HOW DOES IT WORK?

- **Rebase replays, it doesn't merge (verified).** Diverged setup: feature = `5f761ce feat-1` +
  `130f928 feat-2`, master = `8b748ec master-1`, common base `4e18e52 c2`. After `git rebase master`:
  - feature now reads `4e33738 feat-2 → ccb5f43 feat-1 → 8b748ec master-1 → 4e18e52 c2 → …` — one
    straight line, and **merge-base == master tip** (`8b748ec` = `8b748ec`). The feature was physically
    re-based: its commits were re-created on top of master.
  - SHAs changed for BOTH feature commits (`5f761ce/130f928` → `ccb5f43/4e33738`) — even though
    content/message were identical. That's the proof that rebase rewrites history.
- **Interactive rebase (verified):** `GIT_SEQUENCE_EDITOR` rewrote the todo (pick → reword) for
  `HEAD~2`; after the run, `feat-1` became `a0fe182 FEAT-ONE`, and `feat-2` downstream cascaded to
  `e0cc7c4`. Reason: parent SHA feeds the child's hash, so touching ANY ancestor changes every
  descendant. `-i` todo verbs: `pick p` (keep), `reword r` (edit message), `edit e` (stop to amend),
  `squash s` (fold into previous), `drop d` (delete commit).
- **Merge vs rebase contrast (verified):** the same feature, merged `--no-ff`, produced the diamond
  with merge commit `8fda185` and `git log --merges` = 1 — parallel work preserved as parallel. The
  rebased history shows zero merge commits.
- **The cost of rewrite:** anything already shared (pushed, in a teammate's clone, on a PR) is now
  "gone" as seen from the old SHAs. That's not data loss — reflog/origin still hold the old objects —
  but every stale clone is a divergent copy; hence: rebase your own local commits freely, merge (or
  freshly based rebases) for shared paths.

## 4. MENTAL MODEL

```
merge:   A─B─C─M        M has two parents (C, E)   "preserve parallelism"
             ╲D─E─╯
rebase:  A─B─C─D'─E'     linear; D',E' are NEW commits (new SHAs)
         (source commits D,E stay in object DB, reflog-reachable)
interactive: pick/reword/edit/squash/drop while replays happen
rule:     -i / rebase ⇒ local-only history
          merge / no-ff ⇒ shared history
```

## 5. INTERVIEW-SAFE ANSWER

"Merge preserves parallelism — a two-parent commit (or a label fast-forward). Rebase re-plays my
commits on top of another tip: the graph goes linear and every replayed commit gets a new SHA — I
proved that by rebasing two identical commits and showing both SHAs change, and by rewording one via
`git rebase -i` and watching the change cascade downstream. Interactive rebase's todo verbs are
pick/reword/edit/squash/drop. The rule I'd defend: rebase is for my own local work and unreleased
branches; the moment commits are shared, don't rewrite — merge instead, or agree on the rewrite with
everyone. The classic tell in an interview: 'I rebased instead of merging on main' is a history-rule
violation, not a command mistake."

## 6. FOLLOW-UP ATTACKS

**Q.** Should my team rebase or merge for PR merging?
**A.** Design decision, make it explicit. On `main`: merge (or squash-merge) to keep the diamond audit
trail; on feature branches: rebase onto the latest `main` to stay linear. "Rebase in the branch, merge
at the gate" is a common default.

**Q.** What happens to the commits I rebased away — are they gone?
**A.** No. They remain in the object DB and are reachable from the reflog (`git reflog`) and any ref
that still points at them (e.g., `origin/feature` if pushed). Real "lost" happens only when
every reference expires (default reflog 90 days). That's the recovery bridge to GIT.P0.5.

**Q.** `git pull --rebase` vs plain `git pull`?
**A.** Plain pull = fetch + merge (creates a merge commit or FF); `--rebase` = fetch + rebase onto
origin — keeps your local commits linear on top of the remote. Same upstream topic as P0.6; the point
here is the rule's meat (never rebase a pushed branch, but pulling `--rebase` onto origin/HEAD as the
integration point is the sanctioned use).

**Q.** Why do my SHA changes cascade on reword?
**A.** Commit hash = hash of (tree, parents, message, metadata). Change any input to the hash → new
output; and each child's parent entry changes too, so the whole tail-vector downstream rewrites. One
reword ⇒ N new commits.

**Q.** `squash` vs `fixup` in the todo?
**A.** `squash s` folds a commit into the previous one and lets you edit the combined message; `fixup f`
folds without touching the message — good for "oops, typo" cleanups. Both new SHAs in the result.

**Q.** Can I rebase interactive if there are conflicts mid-replay?
**A.** Rebase stops at the conflicting commit, leaves conflict markers, and tells you `git rebase
--abort` (back to start) / `--continue` (after resolving). Same conflict machinery as merges (P0.7).
The wrong move: `--skip` without understanding why the commit is being dropped.

**Q.** Does GitHub/GitLab squash vs rebase-merge matter downstream?
**A.** Yes: a squash PR = one new commit, no branch; a rebase-merge keeps each PR commit but rewrites
SHAs (no diamond); a merge commit keeps the diamond. Each changes how `git log --graph main` reads
and what `git bisect` walks.

**Q.** What's the "rebase amending" trap?
**A.** `git rebase -i` ending with a pushable branch that your teammate already fetched — their clone
now has the pre-rebase SHAs, and the next `git pull` merge-conflicts against your rewrite. Prevent via
the golden rule + `--force-with-lease` if an agreed rewrite is unavoidable (never bare `--force`).

## 7. PRACTICAL EXAMPLE (production)

Long-lived feature branch `auth-refactor` off old main. Team merges five PRs to main ahead of yours.
`git switch auth-refactor && git rebase main` — each of your commits re-applies onto the new tip;
conflicts surface one-at-a-time (top of your branch first), and you confirm with `git log --oneline
main..auth-refactor` now showing exactly your clean fix + feat story. Then merge with `--no-ff` at the
gate so main records the diamond. Verify correctness before the gate: `git log --graph` shows linear;
`git status` clean; rebase never touched `main`. Rollback if surprised: `git rebase --abort` — the
branch pointer goes back to exactly where it was before the command ran.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 4 — rebase replay + interactive reword + merge contrast (VERIFIED)
cd /tmp && rm -rf git_demo4 && mkdir git_demo4 && cd git_demo4
git init -q repo && cd repo && git config user.email lab@warroom.local && git config user.name "War Room Lab"
echo a > a.txt; git add a.txt; git commit -qm c1
echo b >> a.txt; git commit -qam c2
git switch -q -c feature; echo f1 >> a.txt; git commit -qam feat-1; echo f2 >> a.txt; git commit -qam feat-2
git switch -q master; echo m1 > m.txt; git add m.txt; git commit -qm master-1
git log --oneline --graph --all        # diamond: 5f761ce+130f928 vs 8b748ec, base 4e18e52
git switch feature && git rebase master
git merge-base master feature | git rev-parse --short   # == master tip 8b748ec  ← re-based
# feature SHAs changed: 5f761ce/130f928 → ccb5f43/4e33738
# interactive reword of HEAD~2:
GIT_SEQUENCE_EDITOR="sed -i 1s/pick/reword/" GIT_EDITOR="sed -i 1s/feat-1/FEAT-ONE/" git rebase -i HEAD~2
git log --oneline feature | head -4      # a0fe182 FEAT-ONE …; feat-2 cascaded to e0cc7c4
git switch master && git merge --no-ff --no-edit feature   # diamond again; log --merges = 1
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "My teammate rebased the shared branch and my pull is now a minefield"

Trigger: teammate rebased a long-lived shared feature branch onto main and force-pushed; you pull.
Observe: `git pull` says "divergent" / creates a dangling merge or error; `git log` on your and their
refs shows different SHAs for the same commits; `git log origin/feature..feature` (yours) and the
reverse conflict.
Root cause: rebase rewrote (new SHAs) commits that were already published — every stale clone holds
the pre-rewrite objects, so two "versions" of the same logical changes now coexist.
Fix (safe path): reset your local branch to the agreed new history — confirm with the team, then
`git fetch origin && git switch feature && git reset --hard origin/feature` — your OWN work after the
last shared point should be re-applied manually on top (cherry-pick), never blindly overwritten.
Verify: `git log --oneline origin/feature` matches the team's; `git status` clean; your re-applied
work is IN the new history.
Prevent: golden rule on the branch + CI/branch-protection that refuses force-push to shared
branches; if a rewrite is approved, broadcast it ("resetting to X at <time>") so clones resync
deliberately.

### DECISION OVERLAY — what NOT to do

- Don't force-push a globally shared branch (`--force`), even "to fix a mistake" — it orphaned
  everyone else's clones.
- Don't `--skip` on interactive rebase without knowing which commit you're dropping.
- Don't squash-merge a hotfix you may need to bisect later — the single squash commit hides the
  step-by-step history `bisect` wants.
- Don't rebase onto a branch while a merge is in progress (`git status` will tell you; resolve or
  abort first).
- Don't read "git pull worked" as "same history" — check `git log --graph` after.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Rebase keeps my SHAs" | Every replayed commit is new (new SHA) — parent feeds hash. |
| "Rebase and merge are the same operation" | Merge = snapshot+2 parents; rebase = replay on a new base. |
| "Only the rewritten commit changes" | The whole downstream tail cascades (reword proved it). |
| "Rebased commits are deleted" | Old objects stay; reflog/origin still reach them. |
| "`--force` is the same as `--force-with-lease`" | Lease refuses unless the remote is exactly what you expect. |
| "`pull --rebase` is forbidden" | It's the sanctioned linearizing pull for your OWN commits. |
| "Squash merge keeps branch commits" | It makes one new commit; the branch's commits aren't parents. |
| "Interactive rebase is only reword" | pick/reword/edit/squash/fixup/drop, orderings, reorders. |
| "Abort after a conflict loses my work" | Your branch pointer returns to pre-rebase state; the commits are safe. |
| "Main must be linear everywhere" | Teams differ; but if main is linear, use merge-at-gate + rebase-in-branch. |

## 13. FIRST-CHECK REASONING

- **"Why did my pull create a merge commit?"** Default pull merges; if you expect linear, configure
  `pull.rebase true` or say `--rebase`. The DAG told the truth — `git log --graph` showed the
  diamond.
- **"Why do same-message commits have different SHAs on my teammate's machine?"** Someone rebased/
  amended shared history (new SHAs = rewritten objects). Compare `git reflog` and the merge-base; the
  asymmetry is the evidence.
- **"Can I undo a bad interactive rebase?"** Yes until reflog expires: `git reflog` gives the
  pre-rebase SHA, `git reset --hard <thatSHA>` restores the branch. Grab it BEFORE the default
  90-day expiry.

## 14. PRIORITY

**P0 — the git interview's most-asked "which one?" question, plus the foundation of the force-push
incident and of future GitOps/CI review policies.**

## 15. STOP HERE — done when you can…

1. say when each rewrite verb (reword/squash/fixup/drop) is the right call;
2. run the Lab 4 rebase + interactive reword and PREDICT which SHAs change;
3. explain why merging preserves parallelism and rebasing linearizes, with the `--no-ff` contrast;
4. defend the golden rule and name the force-push-with-lease variant;
5. recover a file/branch from a rebased-and-force-pushed story using the reflog concept (P0.5
   completes the mechanics).

## 16. DO NOT STUDY YET

`--onto` twisting (beyond "specific base"), `git imerge`, autosquash, rerere (conflict
memoization — P0.7 mention), LF/CRLF replay semantics, todo-script internals, octopus rebase edges,
packed-refs mechanics. Concept of rerere suffices for now.

---

## QC CHECKLIST — GIT.P0.4

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (merge diamond vs replayed linear vs interactive verbs)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (new-SHA replay, cascade, todo verbs, lease)? | ✔ §3 |
| 5 | Dependencies (GIT.P0.1 DAG, GIT.P0.3 merge base)? | ✔ §3 |
| 6 | Essential commands (`git rebase`, `-i`, `pull --rebase`, revert path)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 4)? | ✔ every output verified live |
| 8 | Break it (shared-branch rewrite incident)? | ✔ §9 |
| 9 | Observe + interpret (SHA diffs, diamond vs linear, merge-base equality)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P0.5 — Reset vs revert + reflog
recovery: soft/mixed/hard, the three zones they move, `git revert` for shared history, and rescuing
'deleted' commits.**

---

# SESSION GIT.P0.5 — RESET VS REVERT, AND REFLOG RECOVERY

Environment note: verified live with git 2.43.0; every SHA/state change below is a real run.

## 1. WHAT IS IT? (≤30 s)

**`git reset`** moves the branch pointer (HEAD) backward/forward and optionally resets the index and
the working tree — safe only for **unshared** history. **`git revert`** makes a **new commit** that
undoes a target commit, leaving history intact — the shared-safe undo. **Reflog** is git's local
"undo log" of every ref move; it is how you rescue commits a `reset --hard` just made unreachable.

## 2. WHY DOES IT EXIST?

Two different "take that back" jobs: on a local branch nobody else sees, moving the branch pointer is
the cheap, surgical undo (reset). On shared history, you can't erase — you must add a corrective
commit (revert). And because humans will lose something to reset/hard/force at least once a year,
git keeps the reflog: a tamper-evident local journal of where every ref *was*, so "I deleted it" is a
problem you solve with one command instead of an incident.

## 3. HOW DOES IT WORK?

- **`git revert <sha>` makes a NEW commit (verified).** Baseline `f.txt` = 3 lines, 3 commits.
  `git revert --no-edit HEAD` produced `c908aea Revert "c3"`: file drops to 2 lines, `git log` count
  goes 3→4, and `c3` **still exists in history** (subject: `Revert "c3"`). Erasing never happened;
  undoing happened. Revert needs merge parents (`-m <n>`) for merge commits and supports
  `--continue/--abort`.
- **`git reset` moves the pointer, then optionally the index, then optionally the tree** — the three
  zones line up exactly with the three states from GIT.P0.1:
  - `--soft HEAD~1` (verified): only HEAD moves; status shows `M f.txt` in the **index column** (the
    change is staged, as if you re-`git add`-ed it) — "drop the commit, keep everything pre-staged."
  - `--mixed` (default) `HEAD~1` (verified): HEAD and **index** move back; worktree untouched —
    status runs ` M f.txt` (space-M = unstaged) and the file STILL has all 3 lines. This is
    "uncommit but keep my work as plain edits." `--mixed` + path = unstage only (`git restore
    --staged`).
  - `--hard HEAD~1` (verified): HEAD, index, AND worktree revert — file drops to 2 lines, status
    clean, log shows only c1/c2. The nuclear zone but the `git status` stays honest: nothing dirty,
    nothing staged.
- **Reflog rescues the reset-away commit (verified).** After the `--hard`, `git reflog` read
  `4129d8d reset: moving to <sha>~1` then `f58014e reset: moving to <sha>…` — the journal still knows
  where HEAD was. `git reset --hard <C3>` put HEAD back at `f58014e`, file = 3 lines, history =
  c3/c2/c1. The "lost" commit was never deleted — only delabeled. Same idea rescues branches after
  a bad rebase or `filter-branch` casualty: pick the pre-event SHA out of the reflog, branch/reset
  to it.
- **Why reset ≠ revert (the shared/history rule):** reset moves a label — if other clones have that
  label's old position, they diverge (GIT.P0.4's rule). Revert grows history forward, so every clone
  converges. Reset = local surgery; revert = published correction.

## 4. MENTAL MODEL

```
HEAD ── index ── worktree   ← three zones, one knob
--soft   moves 1 zone (HEAD)          keep changes staged
--mixed  moves 2 zones (HEAD, index)  keep changes as plain edits
--hard   moves 3 zones                 delete from index + tree (reflog keeps a backdoor)
revert   no moving — ADD a new commit that undoes target (shared-safe)
reflog   journal of every ref move → git reset --hard <reflogSha> = rescue
golden rule: hard/soft reset & rebase -i on LOCAL only; revert for shared
```

## 5. INTERVIEW-SAFE ANSWER

"`git reset` is local pointer surgery across three zones — soft (only HEAD moves, changes stay
staged), mixed (index also moves, changes stay as edits), hard (working tree too, changes gone from
that ref). I verified each with git status after the move: hard ended clean with the file back to two
lines. `git revert` is the shared-safe undo — it adds a commit that reverses the target and leaves the
original in history; I verified `Revert "c3"` being a brand-new commit. And the safety net is the
reflog: after a `--hard` reset I read the old SHA in the journal and `git reset --hard` right back —
the data was never erased, only delabeled. My one-sentence rule: rewrite history only while it's
local; once it's shared, add a revert commit."

## 6. FOLLOW-UP ATTACKS

**Q.** When do I use `--soft` practically?
**A.** Squashing several unshared commits or re-framing a commit boundary: `reset --soft` to a base,
then one clean `git commit`. The staged-ness survives, so the new commit's contents are identical.

**Q.** Is `reset --hard` ever OK on a shared branch?
**A.** No — that's force-push territory and clone divergence. The safe "undo a published change" is
`revert`. If a premature/destructive reset already happened to shared origin, that's the force-push
incident from P0.4, repaired from the reflog.

**Q.** How long do reflog entries live, and can I rely on them?
**A.** Pruned by `gc.reflogExpire` (default 90 days) and on `git gc` runs. In an emergency, get the
SHA and copy it down immediately; don't wait for a server restart. Reflog is per-clone and possibly
turned off — don't design recovery on it, treat it as a first responder.

**Q.** Reset to unstage vs `git restore --staged`?
**A.** Same effect (index reset to HEAD), `restore` is the newer, narrower verb; reset is the broad
zone-operator, restore the file/area operator. Both: "take the index back to HEAD."

**Q.** What does revert do to a file's history vs reset?
**A.** Revert leaves the original commit *and* the revert commit in the log — `git log` shows both.
Reset rewrites the direct ancestry of your branch; the reverted-out change exists only as a delabeled
object until GC.

**Q.** Reverting a merge — why `-m`?
**A.** A merge commit has two parents; reverting needs to know which parent to treat as the "mainline."
Without `-m` git refuses (verified usage output earlier) — that's the standard "can't easily revert a
merge" trap; the answer involves re-reverting the revert to re-merge later.

**Q.** What is `checkout -- <file>` vs `reset --hard <path>`?
**A.** Discard including worktree changes for one path vs resetting the index+tree for a path. Modern
mind: `git restore <path>` for "bring file back to HEAD"; resets-with-paths are the older-but-wider
form.

## 7. PRACTICAL EXAMPLE (production)

Deploy v2 ships, alert spikes. The change is 3 commits deep on `main`, and 300 people cloned it.
You want the code gone but history intact: `git revert --no-edit <v2-sha>` → merge request →
deploy. Meanwhile a teammate locally had started from the pre-v2 base and made a tiny fix — their
local branch got a `--hard` reset by accident; recovery: `git reflog --all | head` to see branch moves,
`git reset --hard <pre-v2-sha>` from reflog, re-sync against remote, land the fix. Story told twice:
revert = shared-safe forward fix; reflog = local-most rescue.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 5 — revert, three reset zones, reflog rescue (VERIFIED)
cd /tmp && rm -rf git_demo5c && mkdir git_demo5c && cd git_demo5c
git init -q repo && cd repo && git config user.email lab@warroom.local && git config user.name "War Room Lab"
echo one > f.txt; git add f.txt; git commit -qm c1
echo two >> f.txt; git commit -qam c2
echo three >> f.txt; git commit -qam c3
C3=$(git rev-parse HEAD)
git revert --no-edit $C3                     # file=2 lines; log 3→4; subject 'Revert "c3"'
git reset -q --hard $C3                      # back to c3 to demo resets
git reset -q --soft $C3~1;  git status --short   # M  f.txt  (staged)
git reset -q --hard $C3
git reset -q $C3~1;          git status --short   # ' M f.txt' unstaged; file still 3 lines
git reset -q --hard $C3
git reset -q --hard $C3~1;   git status --short   # clean; file=2; log=c2,c1
git reflog -6 --pretty="%h %gs"               # 4129d8d reset: moving to <sha>~1 / f58014e … c3 commit
git reset -q --hard $C3                       # rescued; file=3; log=c3,c2,c1
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "I reset --hard the wrong branch, my day's work is gone"

Trigger: engineer meant to discard a throwaway branch but `git reset --hard` on the real feature
branch, or a sloppy `git reset --hard origin/main` wiped local commits.
Observe: `git status` clean; `git log` shows a shorter branch; the "missing" commits are NOT in any
branch. Half the panic is "the reflog didn't tell me" — it did, you didn't read it.
Root cause: hard reset moved HEAD at three zones; worktree+index lost the changes. Nothing was
deleted from the object store — reachability died.
Fix: `git reflog --all` → find the move (`... reset: moving to <sha>…`); volatile wording:
`git reset --hard <thatSHA>` or `git switch -c recovery <thatSHA>`. Verify: `git log` shows the
commit and `git diff <thatSHA> <working>` is clean.
Prevent: `git config reflog.enabled true` (default), stub-protect with branch protection for the
flag-dangerous commands, and grab recovery SHAs immediately (reflog can expire under `git gc`).
Recommendation in interviews: "reading the reflog is my first triage on any 'deleted' report."

### DECISION OVERLAY — what NOT to do

- Don't `reset --hard` a branch others share; the follow-up is clone-repair, not undo.
- Don't rely on reflog for eternity — copy a rescue SHA down on the spot.
- Don't revert a `--hard` mistake with another `--hard`; pair recovery with `git fsck`-style object
  checks if the reflog is thin (unreachable objects may still be dangling).
- Don't `git clean -fd` (removes untracked) right after a hard reset — untracked work only
  disappears there; reflog does NOT cover it.
- Don't use `reset --soft` habitually for "undo" — it's a commit-boundary tool, not an eraser.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "reset erases commits" | Moves a label; objects persist until GC (reflog is the backdoor). |
| "revert is a kind of reset" | Opposite: revert ADDS a commit; reset MOVES a label. |
| "`--hard` is harmless without `-f`" | Single-zone vs all-zone; confirms nothing, the worktree is rewritten. |
| "reflog covers everything" | Tracks ref moves; untracked/Old debris under `git clean` is not in it. |
| "revert can undo a merge directly" | Needs `-m <mainline>`; post-revert re-merge is a trap (re-revert). |
| "reset --soft == amend-lite" | Amend rewrites one commit; soft reset re-opens the whole boundary; different joints. |
| "status clean = no data loss" | After hard reset status IS clean — the loss is pre-cleaned. |
| "`git restore` and `git reset` are synonyms" | Restore = path/zone operator; reset = ref operator. |
| "revert deletes the bad commit's author trace" | The original stays; only its *effect* is negated. |
| "reset --hard HEAD is a no-op" | Same content, but touches worktree; with untracked files it can surprise. |

## 13. FIRST-CHECK REASONING

- **"I deleted a commit."** Read `git reflog` FIRST (a `reset:` / `commit:` line is your victim),
  copy the SHA, `git reset --hard <SHA>` or branch there. Second tool: `git fsck --no-reflogs
  --unreachable` prints dangling objects when reflog is thin.
- **"Undo a change that's already pushed."** Fingers OFF reset; run `git revert <sha>` and let the
  pipeline carry it. Revert-first-check because clones outvote you.
- **"Unstage a file."** `git restore --staged <path>` (or `reset --mixed <path>`); mind the
  three-zone ladder: which zones do you actually want home?

## 14. PRIORITY

**P0 — the undo vocabulary maps to three zones + history safety; asked constantly alongside
rebase/force-push in interviews and incident post-mortems.**

## 15. STOP HERE — done when you can…

1. predict cleanly from the three zones which reset variant keeps what;
2. perform and PROVE a revert (new commit, file reverted, original in history);
3. rescue a hard-reset victim from the reflog and name its failure mode when reflog is gone;
4. state the shared-history rule (revert for shared, reset for local, revert merges need `-m`);
5. unambiguously say what `git clean` covers that reflog does not.

## 16. DO NOT STUDY YET

`reset --keep`/`--soft` corner semantics, `filter-repo` (P2) and `filter-branch` (legacy), reflog
expiry micro-tuning, `git notes`, worktree reflogs, `fsck` catalog beyond `--unreachable`, grafts.
Deal-breaker for interviews: the three-zone ladder and the revert-vs-reset truth.

---

## QC CHECKLIST — GIT.P0.5

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (three zones + revert + reflog backdoor)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (soft/mixed/hard zones, revert new-commit, reflog journal)? | ✔ §3 |
| 5 | Dependencies (GIT.P0.1 zones, GIT.P0.4 shared-rule)? | ✔ §3 |
| 6 | Essential commands (`git revert --no-edit`, `reset --soft/mixed/hard`, `reflog`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 5)? | ✔ every output verified live |
| 8 | Break it (wrong-branch hard reset incident)? | ✔ §9 |
| 9 | Observe + interpret (status letters per zone, `reset: moving to` reflog rows)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P0.6 — Fetch vs pull and remote
tracking: `git remote`, `origin/HEAD`, tracking branches, when pull merges vs rebases, and the
deliberate fetch-then-review habit.**

---

# SESSION GIT.P0.6 — FETCH VS PULL, REMOTES, AND TRACKING BRANCHES

Environment note: verified live with git 2.43.0 using a local bare `origin` and two clones (A/B);
every `origin/…`, `[behind N]`, and merge/rebase result below is a real run.

## 1. WHAT IS IT? (≤30 s)

**`git fetch`** downloads new objects and moves the *remote-tracking branches* (`origin/master`) —
it never touches your work. **`git pull`** = fetch + update your branch (merge or rebase, per
config). Branches are local labels; `refs/remotes/origin/…` are the "last time I looked" copies of
the remote's labels. Tracking is set by `-u` on push → `git branch -vv` shows `[origin/master]`.

## 2. WHY DOES IT EXIST?

You must separate "see what the remote gained" from "change my working branch" — merging/rebaseing
without review is how surprise merge commits and clobbered edits arrive. Remote-tracking refs make
the fetch visible (`[behind N]`, `[ahead N]`, `git log origin/master`). Pull exists so the common
"sync my branch" is one command — but its default behavior (and the merge vs rebase choice) must be
deliberate, because modern git refuses to guess on divergent branches.

## 3. HOW DOES IT WORK?

- **Tracked setup (verified):** `git clone` then `git push -u origin master` → `git branch -vv`
  reads `* master 397971a [origin/master] c1`. The `-u` writes branch master's upstream to
  `origin/master`; `git remote -v` shows the name/URL pairs. (Note: `origin/HEAD` is NOT always set
  by clone on this git — it's a convention ref, not a contract; `git remote set-head origin -a`
  maintains it.)
- **Fetch does not touch your branch (verified):** peer B pushes `c6-b`; on A, `git fetch origin`
  printed `397971a..eab02ca master -> origin/master`; A's local `master` stayed `397971a` while
  `origin/master` became `eab02ca`, and status showed `## master...origin/master [behind 1]`. Nothing
  merged, nothing conflicted — new objects arrived, labels updated, working tree untouched. Only then:
  `git pull` (A idle) fast-forwarded A into sync (`local == origin?` → yes).
- **Pull merges or rebases — config decides (verified on divergence):**
  - Config unset + divergence: git 2.43 prints the "divergent branches… reconcile" hint and refuses
    to guess (`pull.rebase false` / `true` / `pull.ff only` are the options; set one).
  - `git config pull.rebase false` → pull performed a **merge**: `git log --merges` = 1 and HEAD had
    two parents `48695ac(A's) 185fd3e(B's)` — a marriage commit on A.
  - `git config pull.rebase true` → pull **replayed** A's local commits onto `origin/master`: history
    came out linear (`* c9-wa' * c7-wa' * c10-b * c8-b * c6-b * c1`) and the earlier merge commit was
    **flattened** (merges count dropped to 0) — rebase always realigns your branch onto the remote,
    dropping pull-created merge commits unless `--rebase-merges` is used.
- **The deliberate habit:** `git fetch` → read `git status --short --branch` (`ahead/behind` counts)
  and `git log --oneline master..origin/master` → THEN `git merge origin/master` or `git rebase
  origin/master`. Pull is fetch + that decision; skipping the decision stage is skipping the review.

## 4. MENTAL MODEL

```
   your machine                    origin (remote)
   master ──working──►  push  ──►  master
   refs/remotes/origin/master ◄──  fetch  (moves on FETCH ONLY)
   origin/master = "last time I looked at master on origin"
   pull = fetch + merge|rebase      (decide which: config/--rebase/--no-rebase/--ff-only)
   divergence: modern git refuses -> set policy: pull.rebase true|false|ff only
```

## 5. INTERVIEW-SAFE ANSWER

"Fetch and pull are different: fetch moves origin's labels (`origin/master`) and downloads objects —
it never writes my branch, proved by watching `origin/master` advance while my `master` stayed put
and status showed `[behind 1]`. Pull is fetch plus the merge-or-rebase decision, which on divergent
branches modern git refuses to guess — config `pull.rebase false` (merge: two-parent commit, verified)
or `pull.rebase true` (linear replay of my commits; verified it even flattened an earlier merge
commit). The habit I defend: fetch first, read `ahead/behind` and `master..origin/master`, then
merge or rebase deliberately — pull-without-review is how surprise merge commits and clobbered
edits happen."

## 6. FOLLOW-UP ATTACKS

**Q.** `git fetch` vs `git pull --dry-run`?
**A.** Prefer `git fetch` + `git status`+`git log` when you want the decision window; `--dry-run`
exists but fetch is the honest primitive. Most teams set `pull.ff=only` to block surprise merges.

**Q.** When does a merge from pull conflict?
**A.** When both sides changed the same line region relative to the merge base (P0.7). The config
choice (`false`/`true`) doesn't change conflict frequency — rebase just shows conflicts per replayed
commit. Both leave the repo mid-operation until you resolve.

**Q.** What's `origin/HEAD` really for — and why was mine missing?
**A.** A convenience ref telling git which remote branch to assume (used by `git pull` without args).
On this git 2.43, empty clones don't always set it; `git remote set-head origin -a` re-derives it. Not
a contract — wait for the folders, don't design scripts around it.

**Q.** `git push` vs `git push -u origin master`?
**A.** `-u` sets the upstream so later `git pull/push` without args know where. One-time setup per
branch; `git branch --set-upstream-to=origin/master master` fixes an unmatched pair after the fact.

**Q.** Why do I see `[ahead 2]` and `[behind 1]` together?
**A.** You committed locally (ahead) and origin moved (behind). Divergence — exactly the case where
pull needs the merge/rebase decision AND pushing is now `push --force-with-lease`-sensitive (only
after an agreed rewrite).

**Q.** What does `git push --force-with-lease` protect me from?
**A.** It checks the remote's ref matches your last-known value before force-updating; a concurrent
push (someone already advancing origin) makes the lease FAIL instead of clobbering origin/master
with your rewrite. `--force` skips the check — the incident generator.

**Q.** Is `git pull --rebase` the same as fetch + rebase manually?
**A.** Effectively yes (fetch, then `git rebase origin/<branch>`). The configuration `pull.rebase true`
makes it the DEFAULT for that repo — you review the decision once.

**Q.** How do I inspect what a fetch brought?
**A.** `git log --oneline master..origin/master` (what origin has you don't), `--stat` (files),
`--author` filters; `git diff master origin/master --stat`. Read BEFORE integrating — that IS the
review step.

## 7. PRACTICAL EXAMPLE (production)

Morning sync ritual on `main`: `git fetch origin` → status shows `[behind 3]` → `git log --oneline
--graph main..origin/main` lists the three; skim messages + `--stat`; `git merge --ff-only main
origin/main` (guarantees no surprise merge commit). Same ritual on a feature branch once a day:
`git switch feature && git fetch && git log master..origin/master | head` then `git rebase
origin/master` — linear, per-commit conflict surfaces early, and the PR diff stays reviewable.
Both paths keep "review-then-integrate" but never "auto-merge blind."

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 6 — fetch vs pull + divergence policy (VERIFIED; local bare origin + clones wa, wb)
cd /tmp && rm -rf git_demo6b && mkdir git_demo6b && cd git_demo6b
git init -q --bare remote.git
git clone -q remote.git wa -- >/dev/null 2>&1; cd wa
git config user.email a@wr; git config user.name A
echo a > a.txt; git add a.txt; git commit -qm c1; git push -q -u origin master
git branch -vv                          # * master <sha> [origin/master] c1
cd .. && git clone -q remote.git wb -- >/dev/null 2>&1; cd wb
git config user.email b@wr; git config user.name B
echo b1 > b.txt; git add b.txt; git commit -qm c6-b; git push -q origin master
cd ../wa
git fetch origin                        # 397971a..eab02ca master -> origin/master
git status --short --branch             # ## master...origin/master [behind 1]
git pull -q                             # FF → in sync
echo a2 >> a.txt; git commit -qam c7-wa  # wa diverges
cd ../wb; echo b2 >> b.txt; git commit -qam c8-b; git push -q origin master
cd ../wa
git pull -q 2>&1 | head -3               # REFUSES unless config set (2.43 hint)
git config pull.rebase false; git pull -q
git show -s --pretty=%P HEAD             # two parents → merge commit made
echo a3 >> a.txt; git commit -qam c9-wa
cd ../wb; echo b3 >> b.txt; git commit -qam c10-b; git push -q origin master
cd ../wa
git config pull.rebase true; git pull -q
git log --oneline --graph | head -5      # linear; earlier merge flattened
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "I pulled and a surprise merge commit appeared on main"

Trigger: engineer runs bare `git pull` on a local main that had drifted from origin; git absorbs
origin's commits into a merge commit (config not reviewed), PR expectations on "linear main" break.
Observe: `git log --graph` shows a diamond on main; `git log --merges` = 1; nobody intended it.
Root cause: pull default (or `pull.rebase false`) merges divergent histories without review; the
decision stage (fetch → log → merge/rebase) was skipped.
Fix: keep `origin` straight, re-linearize locally: `git reset --hard origin/main` (discard the
merge commit; your unpushed commits reapplied via `git cherry-pick <sha>`), or set policy and pull
again with the intended mode.
Verify: `git log --oneline --graph | head` no diamond; `git status` clean; `git log main..origin/main`
matches expectation.
Prevent: `git config pull.rebase true` (dev) or `pull.ff=only` (main; reject non-FF entirely), and
branch-protection so a non-FF merge to main is refused at the gate if your team mandates linear.

### DECISION OVERLAY — what NOT to do

- Don't `git pull` blind on a divergent branch: decide merge vs rebase FIRST (`--rebase` / config).
- Don't `--force` push a shared branch when origin moved — use `--force-with-lease`.
- Don't rely on `origin/HEAD` existing — it's a convention, not guaranteed.
- Don't merge-with-`main` from a stale local `main` — your local base is a memory, except you run
  GitHub's "update branch" dance (that's a rebase at the gate, done for you).
- Don't set `pull.rebase false` for a branch where a linear history matters — mismatch your stated
  process.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`git pull` is fetch" | Pull = fetch + merge/rebase; fetch alone writes nothing of yours. |
| "`origin/master` is the remote's live state" | It's your local copy, writes only on fetch. |
| "Pull always merges" | Config selects merge or rebase or FF-only; divergent+unset → refusal in 2.43. |
| "`-u` in push does nothing after first clone" | It's exactly what sets the tracking pointer for later pull/push. |
| "Rebase-pull keeps my history identical" | Replays it: SHAs change and prior merge commits flatten. |
| "`origin/HEAD` is always there" | Not guaranteed; `remote set-head origin -a` can restore it. |
| "Fetch dirties my worktree" | Objects+labels only; your working tree untouched (verified `[behind 1]` drill). |
| "`--force` is the modern force-push" | Modern-safety is `--force-with-lease`; bare `--force` is the incident. |
| "Divergence is one-sided" | `ahead` AND `behind` together = both moved (real divergence). |
| "Pull conflict == merge conflict" | Same per-conflict engine; rebase shows them per commit, merge once. |

## 13. FIRST-CHECK REASONING

- **"Why is a merge commit on main?"** `git config pull.rebase`/`pull.ff` and the last `git log
  --graph main` tell you whether someone pulled-without-policy or pushed a non-FF merge. First check:
  `git log --oneline --graph -10` for the diamond; then `git reflog` for who/what moved it.
- **"Is my branch behind or ahead?"** `git status --short --branch` (one line: ahead/behind), then
  `git log master..origin/master` for the incoming delta. Those two reads ARE the fetch review.

## 14. PRIORITY

**P0 — remote model and pull policy are the daily collaboration layer; builds directly into the
CI/CD/gated-main story later.**

## 15. STOP HERE — done when you can…

1. explain fetch vs pull with the `[behind N]` evidence and why fetch is the review primitive;
2. read `git branch -vv` tracking and configure an upstream;
3. set and reason about the three pull modes, incl. the 2.43 refusal-on-divergence;
4. describe the surprise-merge incident and its reset/cherry-pick repair;
5. defend `--force-with-lease` over `--force` and name what lease protects.

## 16. DO NOT STUDY YET

Remote-tracking internals of `refs/remotes`/`packed-refs`, multiple remotes (fork model),
`git remote prune` tuning, refspecs beyond `refs/heads/*:refs/remotes/origin/*` (surface), `--jobs`
parallel fetch, partial clone / `--filter`. Concept of refspec = map on fetch/push OK; deep forms
later.

---

## QC CHECKLIST — GIT.P0.6

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (fetch copies labels; pull = fetch + merge/rebase)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (tracking refs, `-u`, pull configs, refusal-on-divergence)? | ✔ §3 |
| 5 | Dependencies (GIT.P0.3 merge base, GIT.P0.4 rebase, GIT.P0.5 reset for repair)? | ✔ §3, §9 |
| 6 | Essential commands (`git fetch`, `pull --rebase|--no-rebase`, `branch -vv`, `push -u`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 6)? | ✔ every output verified live |
| 8 | Break it (surprise merge incident, force-push)? | ✔ §9 |
| 9 | Observe + interpret (`[behind N]`, two-parent HEAD, flattened merge on rebase)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P0.7 — Conflicts and the resolution
playbook: same-line conflicts, marker anatomy, ours/theirs, merge-vs-rebase differences, and the
full force-push recovery incident.**

---

# SESSION GIT.P0.7 — CONFLICTS AND THE RESOLUTION PLAYBOOK

Environment note: verified live with git 2.43.0; every conflict message, marker block, stage table,
and revert error below is a real run from throwaway repos.

## 1. WHAT IS IT? (≤30 s)

When the **same lines** changed differently on the two sides of a merge/rebase, git can't pick — it
stops and writes **conflict markers** into the file plus a three-stage index entry. Your job:
read the juxtaposition, edit to the intended reality, `git add` the file, and finish with
`git merge --continue` (or `git rebase --continue`). The marker block is literally
`<<<<<<< ours … ======= … >>>>>>> theirs`, and the labels flip meaning between merge and rebase.

## 2. WHY DOES IT EXIST?

Git's whole trick (P0.3) is a three-way leaf: base + ours + theirs. If only one side changed a line,
git folds it silently; if both changed it identically, git sees agreement (verified: identical edits
auto-merged with no conflict). The **conflict exists to refuse a wrong guess** — silently picking a
side would corrupt intent on exactly the changes that need human judgment. Markers exist so the state
is explicit and mechanically resumable (`--abort`/`--continue`).

## 3. HOW DOES IT WORK?

- **The trigger, verified:** both branches rewrote line 2 of `c.txt` to different values
  (master → `MSTR`, feata → `FEAT`). `git merge feata` printed:
  `CONFLICT (content): Merge conflict in c.txt` / `Automatic merge failed; fix conflicts and then
  commit the result.` Git stopped mid-merge (MERGE_HEAD set, index unmerged).
- **The state, verified:** `git status --short` → `UU c.txt` (both index AND worktree unmerged);
  `git ls-files -u` shows **three index stages** for the same path — stage 1 (base), stage 2 (ours /
  your branch), stage 3 (theirs / incoming). That trio IS the three-way merge made visible.
- **The marker block, verified:**
  ```
  line1
  <<<<<<< HEAD
  MSTR
  =======
  FEAT
  >>>>>>> feata
  line3
  ```
  Left of `=======` = ours (HEAD side); right = theirs (the merged-in branch). `git diff` while
  conflicted shows the marker block + the original base context.
- **Resolving, verified:** edit the token block to the real intent, `git add c.txt` (stage 2 slot
  becomes the resolution; 1 and 3 clear), then `git commit` — the merge closes (`merges=1`, clean
  status). `git status` drives the protocol: "Unmerged paths … use git add/rm to mark resolution, then
  git commit."
- **Wholesale picks, verified:** `git checkout --ours c.txt` or `--theirs c.txt` gives the whole
  file from one side (verified with `--theirs` picking `BBB` from the incoming side) — a blunt
  instrument for "accept the branch version," but you MUST still `git add` and commit afterwards.
- **Rebase flips the labels, verified:** after `git rebase upstream` on conflicting same-line change,
  the markers showed `<<<<<<< HEAD / UPSTREAM-ED / ======= / MINE-ED / >>>>>>> d5877d5 (my-commit)` —
  **HEAD (ours) = the UPSTREAM you rebased onto**; "theirs" = your own replayed commit (labeled by its
  SHA/message). Same markers, opposite intuition. During merge, ours = your current branch; during
  rebase, ours = the target branch. Interview gold.
- **Reverting a merge needs a parent, verified:** `git revert --no-edit <mergeSha>` →
  `error: commit cb14be5a… is a merge but no -m option was given.` / `fatal: revert failed`.
  With `-m 1` (the mainline parent) it succeeds: `revert via mainline parent ok`.

## 4. MENTAL MODEL

```
same line ± different values on both sides  ─►  conflict, git stops, MERGE_HEAD/rebase state
index:  stage1=base  stage2=ours  stage3=theirs   (git ls-files -u)
file:   <<<<<<< ours … ======= … >>>>>>> theirs     (HEAD = merged-in target during rebase!)
resolve → git add <file> → git merge --continue | git rebase --continue | git commit
escape:  git merge --abort | git rebase --abort   (repo returns to pre-merge exactly)
revert of a merge: requires -m <parent>
```

## 5. INTERVIEW-SAFE ANSWER

"A conflict is git refusing to guess: my branch and the incoming branch both changed the same lines
differently, so git writes `<<<<<<<`…`>>>>>>>` markers and leaves three stages in the index (base /
ours / theirs) — you can see them with `git ls-files -u`. I verified the full ride live: a merge on a
one-line change produced `UU` status + that marker block; I hand-edited to the real content, `git add`,
and committed to close the merge. The counterintuitive part I'd flag: during a **rebase**, the
'ours' side of the markers is the **upstream** you rebased onto — your own commit is 'theirs' — and I
demonstrated that exact label swap. Escape hatches are `--abort`; wholesale picks are `--ours/
--theirs`; and a merge revert requires `-m <parent>`, which git refuses without (the exact error I
captured live)."

## 6. FOLLOW-UP ATTACKS

**Q.** Why does git sometimes resolve silently, sometimes conflict, on the 'same' change?
**A.** Three-way rule: both sides unchanged → keep; one side changed → take it; both changed
**identically** → git sees agreement and folds (verified); both changed **differently** → conflict.
Blocks of context vs a changed line decide neighborhood — that's the whole heuristic.

**Q.** What do `--ours`/`--theirs` mean during a REBASE?
**A.** Flipped from merge: ours = upstream (rebase target), theirs = your replayed commit. Because
during rebase your commits are being applied onto the upstream, the "current" memory is the upstream.
Confirmed live by the marker labels.

**Q.** How do I `git add` during rebase and why `--continue` not `commit`?
**A.** A rebase is in-progress; you resolve + `git add`, then `git rebase --continue` replays the next
commit (not a commit of your own). `--skip` drops the problematic commit; `--abort` returns to
pre-rebase.

**Q.** What if a conflict span is huge?
**A.** Divergence on a refactor-y line — resolve by taking one side wholesale (`--ours/--theirs`) then
re-running its logic, or `git diff --cc` after add to see how the merge-result differs from both. The
size is a signal the branch diverged too long, not that git lost data.

**Q.** Why does `git merge --abort` feel like magic?
**A.** It restores HEAD and the index from before the attempt (the merge was carried entirely in
staging/plumbing — no commits were created). Same for rebase abort, which restores your branch pointer
using the original base. Nothing was ever destroyed pre-resolution.

**Q.** Is there a 'remember my resolution' setting?
**A.** `reuse recorded resolution` (rerere.) — git can memorize how you resolved a hunk and reapply it
next time. Enable for long-lived merge flows; the 'conflict memo' is more of a fairness device than a
one-click.

**Q.** Can I automate conflict resolution?
**A.** Partly: take-one-side per file with a merge driver or resolution scripts (e.g., 'if JSON, merge
keys; else theirs'), and `git checkout --theirs` in scripts for the accept-incoming policy. Anything
semantic stays human — that's the point.

## 7. PRACTICAL EXAMPLE (production)

Two engineers edit `config.yaml` near `retries:` on the same day; `main` merges theirs first, then
your PR hits `CONFLICT (content)`. The playbook: read the marker block — yours says `retries: 5`,
theirs `retries: 8`; the intent is both — fold into `retries: 8` (product wants 8) while keeping your
different change elsewhere in the block; `git add`, commit, push cleanly. Never leave a marker in a
commit: CI refusing `<<<<<<<` is a mistake catcher. Verify with `git grep -n '^<<<<<<<\\|^>>>>>>>'` on
the tree post-merge.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# Lab 7 — conflict anatomy + resolution + rebase label flip + merge-revert (VERIFIED)
cd /tmp && rm -rf git_demo9 && mkdir git_demo9 && cd git_demo9
git init -q repo && cd repo && git config user.email lab@warroom.local && git config user.name "War Room Lab"
printf 'line1\nline2\nline3\nline4\nline5\n' > c.txt; git add c.txt; git commit -qm base
git switch -q -c feata; printf 'line1\nFEAT\nline3\nline4\nline5\n' > c.txt; git commit -qam feata
git switch -q master; printf 'line1\nMSTR\nline3\nline4\nline5\n' > c.txt; git commit -qam mstr
git merge feata                          # CONFLICT (content) · Automatic merge failed
git status --short                        # UU c.txt
git ls-files -u | awk '{print $1,$3,$4}'  # 100644 1 c.txt / 2 c.txt / 3 c.txt
grep -nE "^<{7}|^={7}|^>{7}" c.txt        # 2:<<<<<<< HEAD  4:=======  6:>>>>>>> feata
printf 'line1\nMERGED\nline3\nline4\nline5\n' > c.txt
git add c.txt && git commit -qm "merge feata: resolved"   # merge closes; merges=1
# --theirs wholesale: git checkout --theirs c.txt && git add && git commit
# rebase label flip (fresh basin):
#   branches mine (MINE-ED) and upstream (UPSTREAM-ED) from master; git switch mine;
#   git rebase upstream → markers show HEAD=UPSTREAM-ED / >>>>>>> <sha> (my-commit)
# merge revert:
#   git revert --no-edit <mergeSha> → 'is a merge but no -m option was given.'; fatal
#   git revert --no-edit -m 1 <mergeSha> → ok
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "The merge closed fine but main still has the old retry logic"

Trigger: teammate believed their conflict resolved because `git merge --continue` succeeded and CI
passed green.
Observe: a silent resolution mistake — they accepted `--theirs` (or edited to the stale copy) and
git accepts ANY content you stage; a resolved conflict only means "the file is internally consistent
again," not "the correct value shipped."
Root cause: resolution is human intent; the machinery can't verify semantics — a wrong pick is a wrong
pick.
Fix: re-read the merge: `git log -1 -p`, `git diff --cc` (vs both parents), and the product check;
revert-target the bad line (`git render`… `git revert -X ours` or plain revert of the fix).
Verify: unit/integration test on the retry value; `git grep` for the marker artifacts; `git show
--stat HEAD` lists exactly the intended files.
Prevent: review 'resolved' PRs for marker survivors and wrong-side picks; CI lint `<<<<<<<`; pair the
resolve with the actual requirement, not with 'what compiles.'

### DECISION OVERLAY — what NOT to do

- Don't `git checkout --theirs c.txt` as the default — it throws away the other side's intent.
- Don't commit files still containing `<<<<<<<`; grep before commit and gate in CI.
- Don't `git rebase --skip` a conflicted commit to "get unstuck" — you lose that commit's change.
- Don't resolve in the editor and forget `git add`; the merge won't continue until the index is marked.
- Don't run merge --abort when other processes rely on the in-progress state; resolve or coordinate.
- Don't treat "merge --continue success" as correctness — resolution intent is yours to verify.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "git picks a side on conflict" | Refuses; markers + 3-stage index, you resolve. |
| "`UU` means file deleted" | Unmerged both sides — content conflict (vs `UD`, `DU` etc.). |
| "ours is always my branch" | During rebase ours = upstream; the labels flip (verified). |
| "`--abort` loses my work" | Returns to pre-merge state; your commits are safe pre-resolution. |
| "`git add` after conflict commits the merge" | It marks resolved; `git merge --continue` finishes. |
| "Revert of merge commits 'just works'" | Needs `-m`; error 'is a merge but no -m option was given' (captured). |
| "`--theirs` is the best 'merge result'" | It's a blunt take-one-side; semantic loss possible. |
| "CI green = conflict OK" | CI proves builds, not intent; the markers may still be in the tree. |
| "Conflict = data loss" | It's an explicit stop with full data; losers are just delabeled, restorable. |
| "Same words twice = conflict-free always" | Identical til both sides → auto-resolve; different edits → conflict. |

## 13. FIRST-CHECK REASONING

- **"Merge/rebase stopped mid-flight."** `git status` → read the `Unmerged paths:` block; the failing
  files named. Open each marker, resolve, `git add`, `--continue`. Escape if needed: `--abort`.
- **"Which side is which in the editor?"** During merge: `HEAD` = your branch, other = incoming.
  During rebase: `HEAD` = upstream, other = your replayed (its message shows in `>>>>>>> <sha> (msg)`).
  Kill the ambiguity by reading the marker labels, not the memory.
- **"CI shows markers in a closed merge."** `git grep -n '^<<<<<<<' $(git rev-list --all)` to find
  where it slipped; ban `<<<<<<<` at the gate and in `pre-commit`.

## 14. PRIORITY

**P0 — the conflict is the single most asked 'calm-down' git topic at 1–3 YOE, and the deepest
misconception (ours/ours-rebase flip) is a one-minute interview proof.**

## 15. STOP HERE — done when you can…

1. explain the three-stage index and prove it with `git ls-files -u` after a conflict;
2. resolve a conflicted hunk by hand, `git add`, and `--continue` (merge and rebase variants);
3. state the rebase label flip and read marker labels instead of guessing sides;
4. use `--ours/--theirs`, `--abort`, and know why a merge revert demands `-m`;
5. run the grep-`<<<<<<<` audit to catch a marker that slipped into a closed merge.

## 16. DO NOT STUDY YET

Custom merge drivers (beyond 'they exist'), `--union`/strategies (`-X theirs` variants fine at
surface), blob-merge/`git merge-file` internals, rerere edge semantics, `git imerge`, merge trees
inside `git log --cc` beyond the surface. Keep: cue-list, marker semantics, stage trio, flip rule,
revert `-m`.

---

## QC CHECKLIST — GIT.P0.7

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (marker block + 3-stage index + abort/continue)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (3-way refusal, markers, stage trio, label flip, revert -m)? | ✔ §3 |
| 5 | Dependencies (GIT.P0.3 three-way, GIT.P0.4 rebase, GIT.P0.5 revert)? | ✔ §3 |
| 6 | Essential commands (`git add`, `--continue`, `--abort`, `checkout --ours/--theirs`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 7)? | ✔ every output verified live |
| 8 | Break it (silent wrong-side resolution, marker-in-tree)? | ✔ §9 |
| 9 | Observe + interpret (`UU`, ls-files -u stages, marker labels both flavors)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **GIT.P1.1 — Bisect, worktrees, signed
commits, and submodules: the P1 toolset, what each is for, and the honest 'why not always'.**

---

# SESSION GIT.P1.1 — BISECT, WORKTREES, SIGNED COMMITS, SUBMODULES

P1 = condensed. Four independent tools verified live on this box (git 2.43.0, GPG 2.4.4).

## 1–2. WHAT + WHY (one screen)

- **`git bisect`** — binary search for the commit that broke a behavior you can *test*. Why: a
  regression report gives "worked at v2, broken at v7"; bisect turns 10 commits into ~4 tests.
- **`git worktree`** — a second checkout of the same repo at a different branch, in a different
  directory. Why: switch branches without stashing/shelving your in-flight work.
- **Signed commits** — `git commit -S` signs the commit with your GPG key; peers verify authorship.
  Why: provenance — "did THIS identity really make that commit" (audit, supply-chain hygiene).
- **Submodules** — a repo mounted inside a repo; the parent stores only a **commit pointer** to the
  sub, not its content. Why: pin third-party/local component versions without vendoring files.

## 3. HOW DOES IT WORK? (verified)

- **Bisect (verified):** 10-commit history; bug committed at #6. `git bisect start <bad> <good>` then
  `git bisect run ./test.sh` (exit 0 = good, non-zero = bad) walked: test #5 → good; test #7 → bad;
  test #6 → bad → **`54ba6f4 is the first bad commit`** with its diff. Log is binary: O(log n) tests,
  not n. **Operational trap captured live:** my first `test.sh` used plain `python3 -c "import
  calc…"` and bisect wrongly flagged #10 as first-bad — Python's `__pycache__` had reused bytecode (a
  same-size file across checkouts). Fix: `python3 -B` (no cache) / clean cache in the test → correct
  first-bad result. Lesson: **the test must reflect the checked-out tree, not a cache.**
- **Worktrees (verified):** `git worktree add ../wt-feature feature` → `git worktree list` shows
  `/tmp/demo_wt/repo [master]` and `/tmp/demo_wt/wt-feature [feature]`; a commit made in the feature
  worktree advanced *only* the feature branch (`a8d8f15`) while the master worktree stayed at `c2`.
  Removal: `git worktree remove ../wt-feature`.
- **Signed commits (verified):** threw-away key `D61B00697CD16EB8` (rsa2048); `git config
  user.signingkey` + `commit.gpgsign true`; `git commit -S`; `git log --show-signature` →
  `gpg: Good signature from "War Room Lab <lab@wr>" [ultimate]`; porcelain status reads `%G?` = `G`
  (good), `%GK` = keyid, `%GS` = signer. A mismatched/unknown key shows up as a different status
  letter (`B` bad sig, `N` no sig, `U` unknown) — that's the trust shorthand.
- **Submodules (verified):** `git submodule add <lib> src/lib` (git blocks local paths by default:
  fatal "transport 'file' not allowed" → `git -c protocol.file.allow=always`); the parent tree holds a
  **gitlink** — `git ls-tree HEAD src/lib` → `160000 commit be20315… src/lib` — and the parent object
  DB has NO such object (`git cat-file` on it fails: it lives in the submodule's own repo). The
  submodule working dir's HEAD mirrors the pin (`be20315`). `.gitmodules` lists path+url; clones need
  `git submodule update --init` (or `git clone --recurse-submodules`).

## 4–5. MENTAL MODEL + SAFE ANSWER

```
bisect      good ─────···───── bad   → binary search via a TEST (exit code), first-bad found
worktree    one repo, two checkouts  → parallel branches, no stash dance
signature   commit object signed with your GPG key → %G? letter tells you good/bad/none
submodule   parent tree: 160000 gitlink = SHA of child HEAD; child content stays in child repo
```

"Bisect is a binary search for the commit that broke a testable behavior — I ran it on a
10-commit history and it found commit 6, the real first-bad commit, and the gotcha that nearly
fooled it (a cached interpreter artifact) is exactly why the test has to observe the checked-out
tree. A worktree gives me a second checkout and branch, so I don't stash to switch. Signed commits
pin authorship to a GPG key — `git log --show-signature` shows the trust result. And submodules
pin a component to a commit via a gitlink entry, not a content copy."

## 6. FOLLOW-UP ATTACKS

**Q.** Bisect needs a fixed test? → Any exit-code script: unit test, `curl` health check, build
result. Bad tests (flaky/cached/depending on environment) poison the walk — that's the (ab)use
pattern to name first.

**Q.** Worktree on a dirty main? → Worktrees share the repo's object store but NOT the index; each
has its own index + HEAD. Same branch twice in two worktrees is disallowed ("already checked out")
— that's the guard you'd mention.

**Q.** Why sign commits in CI too? → So the artifact provenance chain (commit → image → deploy) can
be traced to an identity; unsigned local commits `N` stand out in a `%G?` audit. Keys must be
managed/rotation, and in CI inject the key via the secret system, never a checked-in private key.

**Q.** Submodule pinned to old SHA — how does it update? → `git submodule update --remote` or bump
it inside the sub (commit there, then `git add src/lib` in the parent → new gitlink). The classic
failure: parent works, missing sub on fresh clone → `fatal: clone ... submodule` until
`--recurse-submodules`/`submodule update --init --recursive`.

**Q.** When to NOT use a submodule? → Heavy coupling, frequent dual edits, build-order needs —
vendoring (or a package manager) is often simpler. The interview-short version: submodule = pin a
component's commit; mono-repo/package-pin = the alternatives that sidestep the dance.

**Q.** Do signed commits survive rebase/amend? → Rewrites invalidate the old signature; gpg re-signs
the new commit object (that's why P0.4's "new SHA" and signing coexist). `--rebase-merges` /
`git rebase --exec 'git commit --amend --no-edit -S'` handles batch re-signs in CI gating.

## 7. PRACTICAL EXAMPLE (production)

Regression in prod after v2.3: `git bisect start v2.3 HEAD` + a curl-based smoke test → first-bad
commit contains the change → revert (P0.5); while the fix bakes, check out the same repo in a
`../hotfix` worktree so releases keep moving on main; the signal from `git log --format='%G? %GS'`
shows every deploy commit came from a recognized key; and the auth SDK is a submodule pinned at
`be20315` in `.gitmodules` so no unexpected library upgrades ride along.

## 8. BUILD / REPRODUCE (verified — all four ran live)

```bash
# bisect (the margin gotcha is part of the lesson)
git bisect start $(git rev-parse HEAD) $(git rev-parse HEAD~9)
python3 -B -c "import calc; assert calc.add(2,3)==5" && git bisect good || git bisect bad   # or run a script
git bisect run ./test.sh     # VERIFIED: '54ba6f4 … is the first bad commit' (commit 6)
git bisect reset
# worktree
git worktree add ../wt-feature feature && git worktree list          # two dirs, two branches
# signed
gpg --batch --passphrase '' --quick-generate-key "A <a@x>" rsa2048 sign 0
git config user.signingkey <keyid> && git commit -S -m x
git log --show-signature    # VERIFIED: gpg: Good signature from "…" [ultimate]
# submodule
git -c protocol.file.allow=always submodule add /lib/path src/lib     # 'transport file not allowed' without it
git ls-tree HEAD src/lib    # VERIFIED: 160000 commit <sha> src/lib   (gitlink, not content)
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

**INCIDENT — "The tool flagged the WRONG commit as first bad"** (my own live run): symptom: bisect
called commit 10 first-bad; the bug was at 6. Railsation: the smoke test imported from a cache, not
the checked-out file (`__pycache__` reused for same-size content). Fix: `python3 -B`/fresh
environment in the test. Lesson generalized: **bisect is only as good as the isolated test**;
environment caching, flaky asserts, and external state (network, clocks, databases) invalidate
steps silently.

**INCIDENT — fresh clone, `git clone` succeeds, build fails "submodule not found":** root cause:
submodule content is not part of the parent clone (verified: no such object). Fix:
`git submodule update --init --recursive` or clone with `--recurse-submodules`; in CI always init.
Prevent: CI manifest step that inits submodules at the pinned gitlink.

### DECISION OVERLAY — what NOT to do
- Don't trust a bisect test that uses caches/network/DB; keep it hermetic.
- Don't `--force` worktree removal with uncommitted work, or you lose it (`worktree remove` refuses
  by default for good reason).
- Don't commit with a key whose trust status you haven't read (`%G?`); `B`/`U` are a flag, not a
  green field.
- Don't add submodules for frequently-coupled code — the two-repo dance defeats daily velocity.
- Don't configure a `commit.gpgsign` default on machines without a key — unsigned commits become a
  surprise.

## 12–13. TRAPS + FIRST-CHECK

| Trap | Truth |
|---|---|
| "Bisect needs unit tests" | Any hermitic exit-code check works (curl/build/smoke). |
| "`git worktree add` clones the repo" | Shares the object store; new index/HEAD only. |
| "Signed commit = commit is encrypted" | It's a signature over the commit object; content stays readable. |
| "`%G?` G means 'handed to a real human key'" | G=good sig by a key you trust; U/N tell you the hole. |
| "Submodule = copy of the library" | Gitlink pointer; the library files live in its own repo. |
| "`git clone` brings submodules" | Only with `--recurse-submodules`; default = pointer + absent dir. |
| "Bisect output is deterministic" | Only with a deterministic test; cached/env-dependent = wrong answers. |
| "Worktree removal is harmless" | Refuses with uncommitted changes — as it should. |
| "Filesystem protocol blocked? git is broken" | `protocol.file.allow` default-off (CVE); override deliberately. |
| "`submodule update --remote` is safe" | It MOVES the pin — audit what it points to before CI merges. |

First-check: bisect wrong-first-bad → re-run the test in a fresh/no-cache environment; missing
submodule → `submodule update --init --recursive`; unknown signature → `%G? %GK %GS` and the
key-server/trust chain; "already checked out" on a second worktree → you pointed two worktrees at
the same branch.

## 14–16. PRIORITY / STOP / NOT-SOON

P1 — recognized, command-familiar, explain-the-why, deliberately light on internals.

Done when: run a bisect to first-bad and audit the test for environment traps; add/remove a worktree
and switch branches without stashing; create a signed commit and read `--show-signature` /
`%G?`; add a submodule, read the gitlink + `.gitmodules`, and init it on a fresh clone.

Do not study yet: `git bisect skip`/`--good --bad` pipelines & `bisect visualize`, `--rebase-merges`,
GPG key-servers/subkeys/`%GT` trust-depth internals, Git LFS, subtree. Concept-level wiring
(cert/sig in CI gates) belongs to the Security/CICD domains.

---

## QC CHECKLIST — GIT.P1.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (bisect search · worktree pair · %G? signature · 160000 gitlink)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (binary search + hermetic test, parallel checkouts, key trust status, gitlink)? | ✔ §3 |
| 5 | Dependencies (P0.3 graph walk for bisect, P0.4 rewrite→re-sign)? | ✔ §3, §6 |
| 6 | Essential commands (`bisect run`, `worktree add/list/remove`, `commit -S`, `submodule add/update`)? | ✔ §3, §8 |
| 7 | Reproduce (Labs 8)? | ✔ every output verified live |
| 8 | Break it (cached-test wrong-first-bad, missing submodule, top-of-tree)? | ✔ §9 |
| 9 | Observe + interpret (first-bad diff, worktree list, Good signature, gitlink mode)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

Git domain mandated sessions complete. Next domain for this workspace: **04-bash.md — bash
essentials (vars/args/exit codes/pipes/`set -euo pipefail`), jq, health checks and log parsing**.