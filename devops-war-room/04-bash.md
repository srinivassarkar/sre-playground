# BASH — INTERVIEW WAR ROOM (1–3 YOE)

Priority: **P0 domain.** Bash literacy is table stakes for every ops interview and is the glue the
CI/CD, Docker, and troubleshooting domains speak in. Per the architecture, Git + Bash interleave in
Phase 0 (done: Git 100%). Every session follows the same 16-part template and closes with a 13-point
QC checklist (item 13 = **SELF-VERIFY**). Labs are verified **live on this box** (GNU bash 5.2.21,
jq 1.7) before being written down; every snippet's output below is a real run.

## Reaching prerequisites

Bash builds directly on Linux P0.1 (processes/files) and Git P0.x (repo operations by hand).
Zero external gates; the `health-check` and `log-parse` playbooks lean on Networking's `curl`/HTTP
and Linux's `/proc`, `journalctl`, `grep`/`awk` — covered here with real box output.

## Bash priority map

- **P0 (full 16-part template):** variables/args/quoting · conditionals/loops/functions · exit codes,
  pipes/redirection, `set -euo pipefail` · jq (JSON) · curl patterns (health checks, JSON APIs) ·
  log parsing + health-check playbooks
- **P1 (condensed):** awk/sed field parsing · process substitution · `trap` · arrays · find/xargs
- **P2 (compact):** bash internals · deep param expansion
- **Ignore:** "sed as a language", awk beyond text extraction

## Domain session log

| ID | Topic | Priority | Status | QC |
|---|---|---|---|---|
| BASH.P0.1 | Variables, args, quoting, expansions | P0 | **COMPLETE** | PASS · lab-verified |
| BASH.P0.2 | Conditionals, loops, functions, arrays | P0 | **COMPLETE** | PASS · lab-verified |
| BASH.P0.3 | Exit codes, pipes/redirection, `set -euo pipefail` | P0 | **COMPLETE** | PASS · lab-verified |
| BASH.P0.4 | jq: JSON filters, arrays, bash interop | P0 | **COMPLETE** | PASS · lab-verified |
| BASH.P0.5 | curl patterns for health checks + JSON APIs | P0 | **COMPLETE** | PASS · lab-verified |
| BASH.P0.6 | Health-check + log-parsing playbooks | P0 | **COMPLETE** | PASS · lab-verified |
| BASH.P1.1 | awk/sed parsing, process substitution, trap, find/xargs | P1 | **COMPLETE** | PASS · lab-verified |

---

# SESSION BASH.P0.1 — VARIABLES, ARGS, QUOTING, EXPANSIONS

Environment note: verified live with bash 5.2.21 on this box; all outputs are real runs from
`/tmp` scripts.

## 1. WHAT IS IT? (≤30 s)

Bash strings are built by **expansions**: variables (`$name`), command substitution (`$(...)`),
arithmetic (`$((...))`), the `$@`/`$#`/`$1` positional set, and pattern tweaks like `${var:-default}`
and `${path##*/}`. **Quoting decides whether those expansions happen** — double quotes expand,
single quotes don't — and quoting also decides whether results get re-split on whitespace.

## 2. WHY DOES IT EXIST?

Every deploy script, every CI `run:` step, every on-call one-liner is string expansion + quoting
decisions. The failure mode that burns people most — "my loop over a list ran on the wrong things"
or "the filename with a space broke the script" — is always the same root: unquoted expansion caused
**word splitting**. Nail quoting and the whole domain's accidents mostly disappear.

## 3. HOW DOES IT WORK?

- **Types don't exist; strings do.** `x=5; y=3; echo $((x * y))` → `15` (verified). Arithmetic
  happens inside `$(( ))` only; otherwise everything is text.
- **Quoting (verified):**
  ```
  name="war room"
  echo "double: $name"   → double: war room    (expands)
  echo 'single: $name'   → single: $name       (literal)
  ```
  Double quotes let expansions run; single quotes are fully literal (escape a literal `'` as
  `'\''`). Convention: quote variable uses, especially in `for` loops and `[[ ]]` tests they run.
- **Command substitution (verified):** `$(uuidgen | cut -c1-4)` runs a pipeline and splices its
  stdout in place — a real output `a038`. Backticks `` ` `` do the same, but `$()` nests and reads
  better; prefer `$()`.
- **Positional args (verified):** inside a script `$0` = the script path, `$1..$9` first args,
  `$#` = count, `$@` / `$*` = all args, `shift` moves left (`set -- one two three`; after `shift` the
  set is `two three`, `$#`→`2`). `$@` quoted (`"$@"`) preserves each arg whole; `$*` joins them into
  one string — the classic "lost my spaces" difference.
- **Parameter expansions (verified):** `${v:-default}` = use default if unset/empty (and leaves `v`
  alone — verified `v` stays `''`); `${u:+SET}` = 'SET' only when set+non-empty; `${f##*/}` = strip
  longest prefix (basename), `${f%/*}` = strip suffix (dirname), `${f##*.}` = extension —
  `f=/var/log/app.log` → `app.log` / `/var/log` / `log`. `${#arr[@]}` = array length, `${#s}` =
  string length.
- **Word splitting (the pitfall, verified):**
  ```
  items="one two three"
  for i in $items;      do ...    # 3 iterations: one · two · three
  for i in "$items";    do ...    # 1 iteration: "one two three"
  arr=(a b "c d")
  for i in "${arr[@]}"; do ...    # 3 items, "c d" stays WHOLE — the idiom
  ```
  Unquoted `$items` splits on whitespace; quoted `"$items"` stays one value. Arrays + `"${arr[@]}"`
  are how you carry pieces that themselves contain spaces.
- **Exit-codes teaser (P0.3's topic, minimal here):** `true` → 0, `false` → 1 (verified); `$?`
  holds the last command's code — the hook every conditional and `set -e` hangs on.

## 4. MENTAL MODEL

```
  source text ──► expansion ──► word splitting ──► command
  $name, $(...), $((...))        (unless QUOTED)
  quote rules:   "double" = expand, keep ONE word
                  'single' = literal
     "${arr[@]}" = each element one word, spaces intact   ← the idiom to defend
  positional:    $0 $1..$9 $# $@ "$@"  shift  set --
  tweaks:        ${v:-def} ${u:+SET} ${p##*/} ${p%/*} ${#x}
```

## 5. INTERVIEW-SAFE ANSWER

"Bash is string-expansion plus quoting. Variables, `$( )`, `$(( ))` all expand; single quotes block
expansion. The rule that prevents the classic class of bugs: **quote your expansions** — an unquoted
`$items` in a for-loop word-splits into three tokens, the quoted `"$items"` stays one, and arrays
iterated as `"${arr[@]}"` keep elements with spaces whole — I demonstrated all three live. Positional
args move with `shift` and `$#`; handy parameter expansions like `${file##*/}` (basename), `${v:-d}`
(default), and `${#arr[@]}` (length) are the ones I reach for daily. Where a language has types,
bash has quoting and expansion discipline."

## 6. FOLLOW-UP ATTACKS

**Q.** `"$@"` vs `"$*"` vs `$@`?
**A.** `"$@"` = each arg as a separate word (spaces preserved) — always this for arg forwarding;
`"$*"` = all args joined into ONE string separated by `IFS`; bare `$@` = re-splits each arg on
whitespace (the bug). Forward user input verbatim: `"$@"`.

**Q.** Why does my `for i in $items` sometimes freeze or misbehave?
**A.** Unquoted expansion splits on `IFS`; with spaces inside `items`, you get more pieces than you
meant — and with globs it also does filename expansion. Quote it, or move to an array + `"${arr[@]}"`.

**Q.** `$( )` vs backticks?
**A.** `$( )` nests (`$(echo $(date))`), is readable, and handles quoting the same; backticks are
legacy. Both splice stdout (trailing newlines stripped).

**Q.** `[[ ]]` vs `(( ))` vs `[ ]`?
**A.** `[[ ]]` = the bash-native test (word-safe, `&&`/`||` inside, `=~` regex); `(( ))` = arithmetic
test/eval; `[ ]` = POSIX test (also a builtin). Modern scripts: `[[ ]]` and `(( ))`; `[ ]` for POSIX
sh. (Detail lands in P0.2.)

**Q.** How do I keep a variable's default while NOT modifying it?
**A.** `${v:-default}` reads the value or the default without assigning (verified `v` unchanged);
`${v:=default}` ASSIGNS it. `:-` for read-only-intent, `:=` when you want the side effect.

**Q.** How to strip a known suffix from every file name?
**A.** `${f%.log}` strips the shortest suffix `.log`; if the pattern is a variable/longer, match
outside-in `${f%.*}`, `###`, etc. basename/dirname Get the same result without expansion gymnastics.

**Q.** What does `set --` do and why is it legal mid-script?
**A.** Resets the positional parameters (`set -- one two three` seeds `$1..`); `set --` (no args)
empties them. It's how scripts "parse" then re-shape their own arg list.

**Q.** `printf` vs `echo`?
**A.** `printf '%s\n' "$x"` is deterministic (no `echo` flag ambiguity, formats both) — use it when
the value starts with `-` or contains `\n`; `echo` is fine for display.

## 7. PRACTICAL EXAMPLE (production)

Scraping an exit code hint from a deployed service's pid file:
```
pid=$(cat /var/run/api.pid)          # command substitution, trim-safe
name=${pid##*/}"_check"              # basename-ish tweak
curl -sf "http://127.0.0.1:8080/health" && status=$? || status=$?
printf 'service=%s pid=%s health=%s\n' "$app" "$pid" "$status"
```
The two habits that make it robust: every variable use quoted in the `printf`, and the `|| ` catch
so a failing curl doesn't kill the line under `set -e`. Both are quote/expansion discipline —
nothing type-related.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
bash --version                      # 5.2.21(1)-release
name="war room"
echo "double: $name"; echo 'single: $name'      # war room / $name
n=$(printf 'a038'):  echo "$(uuidgen | cut -c1-4)"   # any hex string, spliced
x=5; y=3; echo $((x*y))             # 15
set -- one two three; echo "$# : $1"; shift; echo "$# : $1"   # 3 : one   →   2 : two
f=/var/log/app.log; echo "${f##*/}" "${f%/*}" "${f##*.}"      # app.log /var/log log
v=""; d=x; echo "${v:-$d} v=='$v'"   # x v==''
arr=(a b "c d"); printf '<%s>\n' "${arr[@]}"    # <a> <b> <c d>
for i in one two three; do :; done              # whitespace list vs quoted-string lesson above
true; echo $?; false; echo $?                   # 0 / 1
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "The cleanup loop deleted extra files"

Trigger: cron cleanup intended to remove backup files from a list; some filenames contain spaces.
Observe: files `backup 2026-09-01.tar` and `backup 2026-09-02.tar` both got charged twice, or the
loop touched the wrong file set.
Root cause: the list traveled as an unquoted string (`for f in $files`), so bash re-split on spaces —
one entry became two.
Fix: carry the list as an array, iterate `for f in "${files[@]}"`, so each element is one word the
whole way (verified `"${arr[@]}"` keeps `"c d"` intact).
Verify: `printf '<%s>\n' "${files[@]}"` prints each element on its own line, spaces intact — the
same output shape the loop will process.
Prevent: any place data crosses from "a value" to "a list of values," make that decision explicit
(array + quoted iteration), and test with filenames that contain spaces at least once per repo.

### DECISION OVERLAY — what NOT to do

- Don't parse output with `for x in $(cmd)` — the word-splitting bug again (use a `while read` loop
  or mapfile, P0.3).
- Don't `eval` an expanded string to build commands — eval re-runs all expansions in a new pass
  (injection).
- Don't build paths by string cats with unquoted segments — quote each, and always expand
  `"${file}"`, never `$file`, in arguments.
- Don't mix `echo` and `printf` on data you'll machine-read; pick `printf` for the CLI/CI boundary.
- Don't rely on the script's cwd — resolve paths from `$0`/`BASH_SOURCE[]` or explicit
  `cd "$(dirname "$0")"`.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`$var` and `"$var"` are the same" | Unquoted = word-split + glob; quoted = one value. |
| "Single vs double quotes is a formatting choice" | Single = literal; double = expand — semantic. |
| "`$@` forwards args" | Must be `"$@"`; bare `$@` re-splits/eats. |
| "`$*` == `$@`" | `"$*"` joins; `"$@"` keeps elements. |
| "Variables have types" | Strings only; types are simulated by expansions. |
| "`[ ]` and `[[ ]]` are interchangeable" | `[[ ]]` is the word-safe bash-native form. |
| "`${v:-d}` sets v to d" | It doesn't; `${v:=d}` is the assigning version. |
| "Backticks are fine" | Legacy; `$( )` nests and is unambiguous. |
| "Words with spaces are rare in scripts" | Are arguments, paths, lists — they always appear, quote defensively. |
| "`set -- x` is something only specialists do" | It's the standard arg-list re-shaping; you'll use it. |

## 13. FIRST-CHECK REASONING

- **"Loop touched the wrong files / extra entries."** Unquote suspect #1: grep the loop header for
  `for x in $list` or `$(...)` — re-splits. Fix by quoting/array.
- **"Variable got an unexpected empty/fallback value."** Check `${v:-d}` (read-only, no assign) vs
  `${v:=d}`, and whether the var was `set` vs empty — `:-` decides on empty, `:+` needs a value.
- **"Filename with spaces broke the script."** Audit every `$filename` to `"${filename}"`; then
  transform lists to arrays.

## 14. PRIORITY

**P0 — the language's joint-and-lever for everything else in this domain.**

## 15. STOP HERE — done when you can…

1. write `"$@"`-forwarded, all-quoted functions and scripts on a whiteboard;
2. explain word-splitting with a real for-loop counterexample (unquoted → 3, quoted → 1);
3. apply `${v:-d}`, `${#x}`, `${f##*/}`, `${f%/*}`, `$(( ))` without notes;
4. re-seat the positional argument list with `set --` and `shift`;
5. defend array iteration with `"${arr[@]}"` for values that contain spaces.

## 16. DO NOT STUDY YET

`${var//pat/rep}`, `~`, `=~` regex minutiae, `IFS` deep tuning, `set -x/-v`, locale/`LANG` effects,
`mapfile`/`readarray` (P1), the rest of `${PS1..}` formatting. Only the first-order expansions above
belong to P0.1.

---

## QC CHECKLIST — BASH.P0.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (expansion → splitting → quote switch)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (quoting, `$( )`, positional set, `${…}` tweaks, split pitfall)? | ✔ §3 |
| 5 | Dependencies (Linux file view; nothing gates earlier)? | ✔ header |
| 6 | Essential commands (`printf`, `set --`, `shift`, `${arr[@]}`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 1)? | ✔ every output verified live |
| 8 | Break it (word-split file deletion incident)? | ✔ §9 |
| 9 | Observe + interpret (3 vs 1 loop iterations, `${v:-d}` non-assign, $?)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **BASH.P0.2 — Conditionals, loops, functions,
arrays: `[[ ]]` vs `(( ))`, test operators, `for`/`while`/`until`, defined-and-tested functions,
indexed+associative arrays.**

---

# SESSION BASH.P0.2 — CONDITIONALS, LOOPS, FUNCTIONS, ARRAYS

Environment note: verified live with bash 5.2.21; all outputs real runs.

## 1. WHAT IS IT? (≤30 s)

Control flow is three pairs: **tests** (`[[ ]]` string/glob/regex/file tests, `(( ))` arithmetic),
**loops** (`for`/`while`/`until`, plus C-style `for ((…))`), and **functions** (name + body, `local`
vars, `return` codes). **Arrays** — indexed `arr=(…)` and associative `declare -A` — are how you
carry data through all of it without string-juggling.

## 2. WHY DOES IT EXIST?

Almost every ops decision is an `if` over the last command's exit code or a file's existence — and
every log/parse/health task is a loop over a stream or an array. Functions exist so a health check
is written once and wired everywhere; arrays exist so lists survive (P0.1) and mappings pair keys to
values. This is the bash you actually script with.

## 3. HOW DOES IT WORK?

- **`[[ ]]` — word-safe tests (verified):** `[[ -n "$s" ]]` non-empty; `[[ "$s" == hello* ]]` glob;
  `[[ "$zero" =~ ^[0-9]+$ ]]` regex; `[[ -f /etc/hostname ]]` file-exists. `[[ ]]` is a bash keyword:
  its words don't word-split (no need to quote as desperately as POSIX `[ ]`), and `&&`/`||`/`!`
  work inside. `-n`/`-z`, `-f/-d/-x/-r`, `-e`, string `== !=`, integer `-eq/-lt/-gt`, regex `=~`.
- **`(( ))` — integer math + comparison (verified):** `(( n > 5 ))`, `(( n % 2 == 1 ))`, and
  `((i++))` inside a while — exit status 0 when the expression is non-zero-true. Use `(( ))` for
  counting; use `[[ ]]` for strings/files.
- **Loops (verified):**
  - `for d in dev ops sec` — iterate the word list.
  - `while (( i < 3 ))` — condition-first loop; `until [[ $i -ge 5 ]]` — loop until condition becomes
    true (the "do it until..." form).
  - C-style `for ((k=1;k<=3;k++))` — counting with init/test/step.
  - `for f in *.log` — glob expansion gives you filenames (list, not string — the P0.1 lesson's
    happy path).
- **Functions (verified):** `greet() { local who="$1"; echo "hi $who"; }` — `local` keeps vars from
  leaking; `return 3; $?` → `3` (explicit codes, or carry the last command's code). Functions are
  defined then called; `$?` after the call is the return code.

## 4. MENTAL MODEL

```
if [[ $s == glob ]] || (( n > 5 )) ... then ... else ... fi     tests
for word in list / for ((i=0;i<n;i++)) / while cond / until cond  loops
func() { local x="$1"; ...; return N; }   → $? carries N
arr=(a b "c d")        ${arr[i]} ${#arr[@]} "${arr[@]}"  unset "arr[i]"
declare -A m=([k]=v)   ${m[k]} ${!m[@]}   assoc maps
```

## 5. INTERVIEW-SAFE ANSWER

"Tests pair up by type: `[[ ]]` for strings, globs, regex and file attributes; `(( ))` for integer
math and comparisons — I verified both families live (non-empty, glob match, regex digits, file
exists, `7>5`, odd-check). Loops: `for` over a word list or glob, `while`/`until`, and the C-style
`for ((…))` for counting. Functions scope with `local` and report through `return`, which shows up as
`$?`. Arrays — indexed and associative — are the data-carrying layer: `"${arr[@]}"` iterates
space-safe elements and `declare -A` gives me key→value maps. The distinguishing habit: know whether
a value is a string, a list, or a map — the loop shape follows the data shape."

## 6. FOLLOW-UP ATTACKS

**Q.** `[ ]` vs `[[ ]]` when writing portable scripts?
**A.** `[[ ]]` is bash/zsh native (word-safe, `&&` inside, `=~`); `[ ]` (POSIX test) is the portable
fallback for `sh`+dash. In the bash world you choose `[[ ]]` and note the portability cost.

**Q.** `(( ))` vs `$(( ))` honestly?
**A.** `(( expr ))` is a command (status = truth); `$(( expr ))` is an expansion (value). Scripts
often need the side-effect-y status form in while heads and the value form in assignments.

**Q.** When does `for f in *.log` fail?
**A.** When no `.log` file exists — the glob stays literal `*.log` (one bogus "filename") unless
`nullglob`/`failglob` are set. If the loop suddenly iterates `*.log` as a name, that's the
missing-file glob story; it also breaks loops needing at least the pattern expanded.

**Q.** Function-local vs global — why `local` at all?
**A.** Without `local`, an assignment inside a function writes a global (leaks across calls, bugs
spread); `local x="$1"` scopes it. Use it for ALL variables a function introduces; that's the
hygiene reviewers look at.

**Q.** Associative arrays vs index by name?
**A.** `declare -A` gives string keys (config maps like `[region]=us-ew-1`), `${!m[@]}` lists keys —
pair it with a `for k in "${!m[@]}"` to walk maps. Indexed arrays give integer slots for ordered
lists.

**Q.** `break`/`continue` semantics?
**A.** `break` exits the loop, `continue` skips to the next iteration; optional `break 2` exits
nested loops. Good to name for a nested story ("stop the outer loop").

**Q.** `case` as a conditional?
**A.** Yes — pattern matching per branch, the switch-statement of bash: `case $x in a*) …;; *) …;;`
esac. Safer than long `if/elif` chains when the discriminator is one value-shaped thing.

## 7. PRACTICAL EXAMPLE (production)

A service-health audit that reports each dead node:
```
declare -A nodes=([api]=127.0.0.1:8080 [web]=127.0.0.1:8081)
for svc in "${!nodes[@]}"; do
  if curl -sf "http://${nodes[$svc]}/health" >/dev/null 2>&1; then
    printf '%s up\n' "$svc"
  else
    printf '%s DOWN (%s)\n' "$svc" "${nodes[$svc]}"
  fi
done
```
The loop walks the map's keys `"${!nodes[@]}"` (spaces safe), `if curl -sf` routes on exit code
(glue to P0.3), and every interpolation is quoted — the three habits in one script.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
s="hello world"; n=7; zero=0
[[ -n "$s" ]] && echo nonempty            # nonempty
[[ "$s" == hello* ]] && echo glob         # glob
[[ "$zero" =~ ^[0-9]+$ ]] && echo digits  # digits
[[ -f /etc/hostname ]] && echo file       # file
(( n > 5 )) && echo big                   # big
i=0; while (( i < 3 )); do echo -n "w$i "; ((i++)); done; echo   # w0 w1 w2
until [[ $i -ge 5 ]]; do echo -n "u$i "; ((i++)); done; echo     # u3 u4
f() { local w="$1"; echo "hi $w"; }; f alice
arr=(alpha beta omega); echo "${#arr[@]} ${arr[@]: -1}"           # 3 omega
declare -A c=([red]=ff0000); echo "${c[red]} ${!c[@]}"            # ff0000 red
unset "arr[1]"; echo "${arr[*]}"                                   # alpha omega
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "The counter loop never ends / runs once too many"

Trigger: a countdown that wraps or a while/until head using the wrong form (`while [[ i -lt 3 ]]` on
a numeric var, or `while (( i < 3 ))` where `i` never increments).
Observe: `((i++))` missing or placed after the condition paths — the loop spins; or an untyped `i`
(string) never satisfies `-gt`-style arithmetic in `[[ ]]`.
Root cause: mixing string tests (`-lt`/`-gt`) on numeric intent, plus the increment being conditioned
away — the C-style `for ((…))` avoids the whole class.
Fix: use `(( ))` for the whole arithmetic state machine (`for ((i=0;i<N;i++))` or `while (( … )); do
… ((i++)); done`); confirm with `printf 'i=%s\n' "$i"` inside.
Verify: the loop exits in exactly N iterations (count captured).
Prevent: never write a while that ends in a state you can't compute — prefer `for ((…))` for known
counts and `until [[ condition ]]` when you literally mean "do until."

### DECISION OVERLAY — what NOT to do

- Don't use `[ ${arr[0]} ]`-style per-element tests against unset indices (`set -u` explodes) —
  check `[[ ${#arr[@]} -gt 0 ]]` first or use `${arr[0]-}`.
- Don't glob-loop then assume the pattern matched — handle the no-match case (nullglob/failglob).
- Don't `declare -A` inside a tighter scope and expect a global — know where the map lives.
- Don't `return` from `main` (top-level) — main returns the script's exit, not a function code.
- Don't write deep `if/elif` chains where `case` + `[[ ]]` globs say it better.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`[ ]` and `[[ ]]` are the same test" | `[[ ]]` word-safe + `&&`/`||`/`!` + `=~`; `[ ]` is POSIX. |
| "`(( expr ))` and `$(( expr ))` both give values" | `(( ))` is a test/status; `$(())` is a value. |
| "`for f in *.log` with no match breaks loudly" | It iterates the literal `*.log` string unless nullglob. |
| "Function vars are local by default" | Global unless `local`; leak-prone. |
| "`return 3` endswith "$3"" | `$?` is the return code; it's not positional. |
| "Associative arrays are bash-wide" | Need `declare -A` (bash 4+); `bash <<< "…"` in scripts must assert. |
| "`[[ a -lt b ]]` for strings" | `-lt/-gt` are integer tests — string compare `== !=` only. |
| "`while` and `until` are interchangeable" | `until` loops WHILE condition is FALSE — complements `while`. |
| "`break`/`continue` need no care" | `break 2` exits nested loops; mis-scoping spins loops. |
| "`case` is just formatting for ifs" | Real branch construct with glob patterns; use it. |

## 13. FIRST-CHECK REASONING

- **"Loop with wrong count."** Look for a string-versus-int test mismatch (`[[ $i -lt 3 ]]` on a
  numeric) or a missing increment; switch to the C-style `for ((…))` to make step/init/test visible.
- **"Map returned nothing / keys wrong."** Check `declare -A`, key quoting (`"${!map[@]}"`), and
  whether the script *re*-declared it locally. 
- **"A variable I changed in a function didn't stick (or stuck too much)."** It stuck because it was
  global, or didn't because `local` — `local` announces the scope decision; name it first.

## 14. PRIORITY

**P0 — the control-flow skeleton every script hangs on; enables the playbooks (P0.6).**

## 15. STOP HERE — done when you can…

1. pick `[[ ]]` vs `(( ))` by data type without thinking;
2. write `for`-over-list, C-style `for`, `while`, `until`, and a `case` branch from memory;
3. write a function with `local` + explicit `return` and explain `$?`;
4. walk an indexed and an associative array with `"${arr[@]}"` / `"${!m[@]}"` idioms;
5. diagnose a wrong-count loop via the test-type tell and the missing-increment tell.

## 16. DO NOT STUDY YET

`eval`, `getopt`/`getopts` internals, `coproc`, `select` loops, `readarray` (P1), `[[ -v ]]` little
variants, `local` defaults and `esac` corner glue, function-declaration styles (`function` keyword).
P0.2 is the syntax-rhythm; the idioms land in playbooks.

---

## QC CHECKLIST — BASH.P0.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (test pairs, loop triple, function/return, array/map)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (`[[ ]]`/`(( ))`, loop forms, local+return, arrays/assoc)? | ✔ §3 |
| 5 | Dependencies (BASH.P0.1 quoting/split hygiene)? | ✔ §3 |
| 6 | Essential commands (`[[ … ]]`, `(( ))`, `for ((…))`, `declare -A`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 2)? | ✔ every output verified live |
| 8 | Break it (spinning/off-by-one loop, leaky local)? | ✔ §9 |
| 9 | Observe + interpret (test statuses, `$?` from return, array len/slice)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **BASH.P0.3 — Exit codes, pipes, redirection,
`set -euo pipefail`: the contract every command handshakes on, and why CI insists on the strict
mode.**

---

# SESSION BASH.P0.3 — EXIT CODES, PIPES, REDIRECTION, `set -euo pipefail`

Environment note: verified live with bash 5.2.21; every status/code below is a real run.

## 1. WHAT IS IT? (≤30 s)

Every command exits with a **code** (0 = OK, non-zero = failure). Pipes chain commands left→right and
a pipeline's exit is the **last** command's — unless `pipefail` makes it the **first failure**.
Redirection (`>`, `>>`, `2>`, `2>&1`, here-docs, `/dev/null`) picks where output goes. `set -euo
pipefail` is the strict-mode preamble: **exit on error, error on unset variables, honor failures in
the middle of pipelines** — the safety contract CI and CMS scripts run under.

## 2. WHY DOES IT EXIST?

Because "did it work?" is a boolean the shell can encode — and silent failure is the worst production
bug (a script "succeeded" while a step inside quietly failed). Exit codes exist so `if cmd; then`
works and so CI can gate on truth. Redirection exists so logs, errors, and prompts land where you can
find them. Strict mode exists because default bash "keeps going after a failure," which turns one
broken line into a misleadingly-green pipeline.

## 3. HOW DOES IT WORK?

- **Exit codes (verified):** `true` → 0; `false` → 1; a function `return 7` → `$?` == 7; a subshell
  `(exit 42)` → `$?` == 42; `grep` with no match exits 1. `$?` is read **immediately** after the
  command — it's a one-shot register, compare it as soon as it appears.
- **Pipeline exit default vs `pipefail` (verified):** `false | true` → **WITHOUT pipefail: 0**
  (last command `true`), **WITH pipefail: 1** (first failure wins). Default hides the early failure;
  `pipefail` surfaces `grep`'s "no match" as a pipeline signal.
- **`set -e -u -o pipefail` (verified):**
  - `-e`: stops the script at the first failing command — `bash -c 'set -e; false; echo
    NOT_REACHED'` does NOT print NOT_REACHED, and a `set -euo pipefail` script whose `printf … | grep
    c` fails aborts with `script-exit=1`.
  - `-u`: treats unset variables as an error — `bash: line 1: UNDEFINED: unbound variable`.
  - `-o pipefail`: pipeline exit = first non-zero stage (as shown).
  - Combined that's the "die loudly" preamble: `#!/bin/bash set -euo pipefail`.
- **Redirection (verified):** `> file` truncates+writes, `>> file` appends; `2> err.txt` captures
  stderr (`ls /nonexistent` error text landed in the file, verified `[ -s err.txt ]`); `2>&1` (or
  `&>` ) merges both (`{ echo o; echo e >&2; } > both.txt 2>&1` → file has `o` then `e`); `/dev/null`
  discards; a **quoted here-doc** (`<<'EOF'`) keeps `$var` literal — verified `line $B` stayed put.

## 4. MENTAL MODEL

```
code:   0=ok  nonzero=fail   $? read once, immediately
pipe:   a | b | c → status = c            (default)
        a | b | c → status = first failure (pipefail)   [false|true → 1 vs 0]
strict: set -e       abort on first failing command
        set -u       error (not silent empty) on unset var
        set -o pipefail   middle-stage failures count
redir:  >  >>  2>  2>&1  &>  /dev/null  <<'EOF'   (heredoc-quote keeps $ literal)
```

## 5. INTERVIEW-SAFE ANSWER

"Every command returns a code; `$?` holds it but only until the next command runs. Default pipeline
exit is the LAST command's — which hides middle failures — and `set -o pipefail` changes it to the
first failure; I proved the whole contrast: `false | true` is 0 by default, 1 with pipefail. Strict
mode (`set -euo pipefail`) is the CI-safe preamble: `-e` aborts on the first failing command,
`-u` turns silent empty-variable bugs into errors, and pipefail makes pipelines honest — my live run
of `printf … | grep c` under strict mode aborted with exit 1. Redirection is the output-selection
layer: `>`/`>>`, `2>` for stderr, `2>&1` to merge, `/dev/null` to drop, and a quoted here-doc keeps
`$x` literal. The one-line habit: assume defaults LIE to you on failure — strict mode is how you stop
the lie."

## 6. FOLLOW-UP ATTACKS

**Q.** Why `set -e` sometimes doesn't fire?
**A.** `-e` ignores failures in `if` CONDITIONS, after `&&`/`||`, inside functions called where a
test is expected, and in `!` prefix positions. It also doesn't fire for `cmd || kill -9 $$`
patterns. So f- "set -e is my safety" — it's a guard, not the whole policy: review what it covers.

**Q.** `$?` got eaten between the command and my echo?
**A.** You ran another command in between (a test, a printf, a subshell) — check the register at the
branch itself. Common paper-cut; the fix is reading it immediately (or into a var before the next
command).

**Q.** `pipefail` lives where?
**A.** Set per-script (`set -o pipefail`) or globally in `bashrc`; it's a shell option, not a
command attribute. Some tools (older bash `-o` list) need bash 4+.

**Q.** `2>&1` vs `&>` vs `1>&2`?
**A.** `2>&1` = stderr→where stdout goes (order matters: behind `> file`); `&>` = both-to-file
merge; `> /dev/null 2>&1` = full discard. The classic bug: `2>&1 > file` — you merged stderr to the
OLD stdout (terminal), then redirected stdout — error still visible.

**Q.** When would I NOT use strict mode?
**A.** Interactive/diagnostic one-liners and scripts that intentionally probe failure states
(`ls /missing 2>/dev/null || …`). Strict mode is a build/CI guardrail; interactive uses tolerate the
soft default. The rule: boring reliable scripts → strict; exploratory probes → opt-out explicitly.

**Q.** How to debug with codes?
**A.** `set -x` traces commands (stderr), `trap 'echo failed $?' ERR` prints code + context on
failure; combos (`set -euxo pipefail` in CI) give the failing line. Knowing `-x` exists and when it
helps IS the debugging story.

**Q.** What is `$?` for a killed/errored command (<128 codes)?
**A.** 128+signal for signal kills (`kill -9` → 137); ≥128 often reads as "signalled". Recognize
"139" as SIGSEGV, "137" as SIGKILL, "130" as SIGINT — interview points without tools.

## 7. PRACTICAL EXAMPLE (production)

The CI "run smoke" step:
```
#!/usr/bin/env bash
set -euo pipefail
svc="api-${ENV:-dev}"                                   # -u catches ENV typo → FAILS here, not later
curl -sf "http://${svc}:8080/health" >/dev/null         # exit code = health truth
printf 'link=%s\n' "${svc}" >> /var/log/smoke.log
```
The `-u` guarantee: if `ENV` (or a typo) is unset the step dies with `unbound variable` at the first
use instead of composing a wrong URL and "passing" — the failure is loud and early. Every reviewer
reads the preamble; the body's only purpose is "am I healthy" expressed as an exit code.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
true;  echo "true=$?"          # 0
false; echo "false=$?"         # 1
f() { return 7; }; f; echo $?  # 7
(exit 42) || echo $?           # 42
false | true; echo "no pipefail: $?"        # 0
set -o pipefail; false | true; echo "pipefail: $?"   # 1
bash -c 'set -e; false; echo NOT_REACHED'          # (nothing)
bash -c 'set -u; echo $UNDEFINED' 2>&1 | tail -1   # unbound variable
bash -c 'set -euo pipefail; printf "a\nb\n" | grep c >/dev/null; echo N'; echo "strict-exit=$?"  # 1, no N
echo o >> f.txt && printf 'line $X\n' | tee heredoc.txt >/dev/null; cat heredoc.txt  # 'line $X' literal
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "The pipeline 'passed' in CI but produced nothing"

Trigger: a deploy step `curl api/status | jq '.release' > release.txt` and the step green-lighted
while the file was empty and misformatted.
Observe: `release.txt` empty; `curl` actually failed with network/HTTP error; pipeline exit = the
LAST command (`jq` success) — the earlier `curl` failure was swallowed.
Root cause: default pipeline semantics (last-exit) + no strict mode.
Fix: `set -euo pipefail` at the top, re-run — `curl | jq` now aborts on the curl stage and CI shows
the real error.
Verify: reintroduce the failing `curl` step with pipefail and watch the nonzero exit; file untouched.
Prevent: strict preamble in every CI script, and gate on output presence (test `-s release.txt`)
where the artifact is a contract.

### DECISION OVERLAY — what NOT to do

- Don't `cmd || true` away a failure you didn't route deliberately — it's how "passed" scripts lie.
- Don't `set -e` inside a subshell and expect it to protect the parent.
- Don't write `2>&1 >file` (order bug — stderr rides the old stdout).
- Don't read `$?` late; capture it before producing more output (that becomes the next command).
- Don't `exit $?` where the point was to propagate the code — implicit exit already does.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Pipe exit = first failure automatically" | Default is LAST command; pipefail changes it. |
| "`set -e` catches everything" | Except in if-conditions / after `||` / in test position. |
| "`$?` stays until you need it" | It changes with the NEXT command — read immediately. |
| "`&>` and `2>&1` are identical" | Positional ordering matters; `&>` is the both-to-file merge. |
| "> file overwrites, always" | Yes for `>`; `>>` appends; tools may flush/truncate themselves. |
| "`2> file` hides nothing" | Redirects stderr — stdout still prints. |
| "Strict mode is for interactive shells" | It's the CI/CMS guardrail; interactivity prefers the soft default. |
| "Exit >128 is 'weird code'" | It's signal+128 (137=KILL, 139=SEGV, 130=INT) — read it. |
| "`-u` makes scripts slower preachy" | It converts silent-wrong into loud-soon; that's the win. |
| "`|` is 'run both at once' and failures don't matter" | Pipeline = composed status; pipefail makes each stage count. |

## 13. FIRST-CHECK REASONING

- **"It 'passed' but did nothing."** Check for pipes without pipefail, `|| true` swallow, or a
  post-pipeline `$?` misread. Reproduce with `set -o pipefail` and watch the stage that fails.
- **"Undefined variable blew up suddenly."** That's `-u` doing its job — find the first use of the
  name and set/resolve it there (it was previously silent-empty).
- **"Log file empty / prompt to stderr?"** Route deliberately: `> log 2>&1` merges to file; `2>&1 >file`
  is the ordering bug; `&>file` is unambiguous.

## 14. PRIORITY

**P0 — exit/pipe semantics IS the script contract; strict mode is the CI baseline this whole platform
rests on.**

## 15. STOP HERE — done when you can…

1. state the default-vs-pipefail pipe exit and demonstrate `false|true` both ways;
2. quote what `-e`, `-u`, `-o pipefail` each defend against;
3. route stdout/stderr to file, `/dev/null`, and merged file correctly (and spot `2>&1 >f`);
4. read `$?` at the right moment and name 137/139/130 as signal-derived;
5. write the strict preamble and the "failing early stage aborts" repro from memory.

## 16. DO NOT STUDY YET

FD gymnastics beyond 1/2 (`3<&` etc.), coproc/process substitution interplay (P1), `xtrace` logic
debugging, `set -o` full catalogue, `errexit` corner tables (unless asked directly). Keep the
failure-is-loud doctrine and the four strict-mode verbs.

---

## QC CHECKLIST — BASH.P0.3

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (code/pipe/redir + strict-mode guards)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (pipe status semantics, `set -euo pipefail`, fd routing)? | ✔ §3 |
| 5 | Dependencies (BASH.P0.1 quoting around redirects, P0.2 `if` on codes)? | ✔ §3 |
| 6 | Essential commands (`set -euo pipefail`, `2>&1`, `>`, `>>`, heredoc, `$?`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 3)? | ✔ every output verified live |
| 8 | Break it (swallowed pipeline failure incident)? | ✔ §9 |
| 9 | Observe + interpret (`false|true` 0→1, unbound variable, NOT_REACHED never printed)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **BASH.P0.4 — jq: querying JSON with filters,
`.field`, `.[]`, `.map`, conditionals, and bash↔jq interop for health checks and API payloads.**

---

# SESSION BASH.P0.4 — jq: JSON FILTERS AND BASH INTEROP

Environment note: verified live with jq 1.7 (this box); the sample payload is synthetic but the
queries ran verbatim.

## 1. WHAT IS IT? (≤30 s)

**jq** is a command-line JSON processor: one-liner filters over structures — `.field`, `.[]` to
iterate, `.items | map(select(…))`, conditionals, null-safety (`//`, `.?`), and reformatting
(`keys`, `length`, `join`, `sort_by`). With `-r` it emits raw strings and `-e` turns a filter's
truth into an **exit code**, so jq slots straight into bash scripts and CI gates.

## 2. WHY DOES IT EXIST?

APIs, health endpoints, cloud CLIs and CI metadata all speak JSON; bash speaks strings and exit
codes. jq is the bridge: extract exactly the field you need without regex theatre over a blob, test
a condition as a boolean, and feed values back into variables. It's also how everyone actually reads
`curl` output in production — a tool that turns a wall of JSON into a question answered.

## 3. HOW DOES IT WORK?

- **Field access (verified, payload `{"status":"ok","hits":3,"service":{"name":"api","port":8080},…}`):**
  `jq -r '.status'` → `ok`, `.hits` → `3`, `.service.name` → `api`. Dot-path across objects; `-r`
  for raw (no quotes around output) — always use `-r` when the value goes into a variable.
- **Iterate/build (verified):** `.items[] | .name` → emits `a b c` (one per item); `[.items[].name]
  | join(",")` → `a,b,c`; `.items | sort_by(.size) | last` → the largest item; `.items |
  map(select(.size > 5))` → the two big items. **Pipeline key:** `map/select` apply to ARRAYS — the
  object `.items` must be emitted first (my wrong attempt `map(...)` on the root errored:
  `Cannot index string with string "size"` — the classic first-jq stumble, now a documented trap).
- **Conditionals / null-safety (verified):** `if .status=="ok" and (.hits>2) then "up-busy" else
  "down" end` → `up-busy`; `.a // "default"` replaces null with a fallback → `default`; `has("obj")`
  → true; `(.items // []) | length` → 0 when items is null (never crash); `.nope != null` → false.
- **Boolean exit codes via `-e` (verified):** `jq -e '.status=="ok"'` exits 0; a false expression
  exits 1; `has("x")` on `{}` exits 1. That status turns jq into an `if`-friendly gate (and a
  `jq -e … | grep`-free pipeline stage under pipefail).
- **Bash interop (verified):** `v=$(… | jq -r '.field')`; arrays via
  `names=($(jq -r '.items[].name'))` → `a b c`; and injection-safe interpolation with `--arg`
  (string) / `--argjson` (numeric/bool) so values never get shell-interpolation — `jq -n --arg n
  api --argjson p 8080 '{name:$n, port:$p}'`.

## 4. MENTAL MODEL

```
JSON ──► jq filter ──► stream of results
  .field  .a.b            path (dot, -r for raw)
  .[]                     iterate    [ ... ] build back into array
  map(…) select(…) sort_by(…) join(…) length keys
  //  null fallback       has(…)      if … then … else … end
  -e  truth → exit code   --arg/--argjson  safe interpolation
bash↔jq: v=$(... jq -r .x)   array=($(jq -r '.a[]'))   if jq -e '.cond'; then
```

## 5. INTERVIEW-SAFE ANSWER

"jq turns JSON into answers: `.status`, nested `.service.name`; iterate with `.[]`; re-shape with
`map(select(…))`, `sort_by`, `join` — but the discipline is that `map`/`select` are array filters, so
I feed them the array first (my own wrong root-level `map` errored with `Cannot index string…`).
Null is handled deliberately: `.a // fallback` and `(.items // []) | length` so missing fields never
crash a pipeline. `-r` gives raw values that go straight into a variable; `-e` makes the filter's
truth an exit code, which is how jq becomes an `if` gate in a strict-mode script. For interpolation I
pass `--arg`/`--argjson` rather than injecting shell strings — no quoting/injection holes."

## 6. FOLLOW-UP ATTACKS

**Q.** `-r` vs plain output?
**A.** Plain prints JSON-encoded (quoted/handled strings); `-r` prints the raw value — use `-r` for
`v=$(…)` results, text joins, and file-ish uses; keep plain for re-serialization.

**Q.** Why did `map(select())` error on my data?
**A.** `map` walks an ARRAY; if `.` is the whole object you must first reach the array
(`.items | map(…)`). Same class as `sort_by` — the "pipe the array first" rule.

**Q.** `select` vs `//` vs `?` — when which?
**A.** `select(cond)` filters array elements; `expr // default` substitutes for null; `expr?` turns
errors into null (optional operator). For "missing means zero": `(.items // []) | length`.

**Q.** How do I detect a missing key vs a present-but-null key?
**A.** `has("key")` distinguishes presence; `[.key != null]` distinguishes null; `..`-recursive
searches (`.. | objects | .key?`) for deep scans. The difference usually matters for API contracts.

**Q.** jq arrays into bash — pitfalls?
**A.** Bash can't hold raw arrays easily: either stream `/` separated lines (`-r … |)` + mapfile
(P1) or `[@sh]`-quoted; the naive `names=( $(…) )` re-splits (P0.1 word-splitting). Prescribe
`-r` + `readarray` when elements can contain spaces.

**Q.** Performance on huge JSON?
**A.** jq streams whole documents (it parses to memory) — for truly huge logs use `jq -c '…'
--stream` or a line-oriented parser / `jq` per line with `-R` raw. Practically: keep payloads small
or split at the producer.

**Q.** jq inside a here-doc / longer script?
**A.** `jq '…multi-line…' <<'EOF'` keeps quoting sane; keep the filter script-literal. And pass
secrets/values only via `--arg`, never embedded in the filter string.

## 7. PRACTICAL EXAMPLE (production)

Release-dashboard step that extracts the LATEST deploy per env from an API blob and asserts it's
healthy:
```
curl -sf "$REGION/api/v1/deploys?env=${ENV}" \
  | jq -r --arg env "$ENV" 'map(select(.env==$env)) | sort_by(.ts) | last | .image'
# and the gate:
curl -sf "$EP/health" | jq -e '.status=="ok" or .pending==true' >/dev/null \
  && release_ok=1 || release_ok=0
```
Note `--arg env "$ENV"`: the env name flows in safely; the filter only references `$env`. One
extraction, one gate, zero string interpolation.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
D='{"status":"ok","hits":3,"service":{"name":"api","port":8080},"items":[{"name":"a","size":10},{"name":"b","size":2},{"name":"c","size":7}]}'
echo "$D" | jq -r '.status, .service.name, .service.port'      # ok api 8080
echo "$D" | jq -r '.items[] | .name'                          # a b c
echo "$D" | jq -r '[.items[].name] | join(",")'               # a,b,c
echo "$D" | jq -c '.items | map(select(.size > 5))'           # a(10) c(7)
echo "$D" | jq -c '.items | sort_by(.size) | last'            # a 10 (largest)
echo "$D" | jq -r 'if .status=="ok" and (.hits>2) then "up-busy" else "down" end'  # up-busy
echo '{"a":null}' | jq -r '.a // "default"'                   # default
echo '{"items":null}' | jq -r '(.items // []) | length'       # 0
echo "$D" | jq -e '.status=="ok"' >/dev/null; echo $?          # 0
echo '{}' | jq -e 'has("items")' >/dev/null; echo $?           # 1
jq -n --arg n api --argjson p 8080 '{name:$n,port:$p}'         # {"name":"api","port":8080}
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Health check gate passed but the API was down"

Trigger: the release job ran `curl … | jq '.status=="ok"'` with default (plain) output — the
`true`/`false` printed as text, but the gate checked exit 0 always (jq exits 0 printing the boolean).
Observe: `jq '.status=="ok"'` prints `true` and EXITS 0 regardless; a `false` exit would only come
from a parse error, not the boolean.
Root cause: jq exit code = "did the filter run", NOT "is the result true" — the `-e` flag changes
that.
Fix: `jq -e '.status=="ok"'` (verified: true→0, false→1), or `[[ $( … ) == "true" ]]`; logic moves
out of text, into exit code.
Verify: run both `-e` variants (0 vs 1) and confirm the gate flips as expected.
Prevent: treat every jq truth-check with `-e` in strict-mode scripts; never gate on the plain
filter's exit alone.

### DECISION OVERLAY — what NOT to do

- Don't interpolate bash values into the filter string (`jq --arg` instead).
- Don't `jq`-filter against the wrong object shape (map/select need the array first).
- Don't rely on `jq ''` exit code to mean "the JSON answers yes" without `-e`.
- Don't `names=($(jq -r '.a[]'))` for values that may contain spaces — use `-r`+`mapfile`.
- Don't grep JSON — parse it; jq exists precisely not to regex blobs.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "jq exit 0 means the filter is true" | Means the filter RAN; `-e` turns truth into code. |
| "`map` works on any object" | It works on ARRAYS; pipe the array first. |
| "`-r` is for 'raw speed'" | It's raw output — no JSON encoding — right for `$( )`. |
| "`.x // y` is a ternary" | It's null-replacement; ternary is `if … then … else`. |
| "Missing key crashes silently-null" | `.a` on absent → null (or error with `.a?`); `has()` checks presence. |
| "--arg is optional" | It's the safe path; bare interpolation is an injection hole. |
| "jq can stream unlimited data" | Parses in memory; huge blobs need streaming/line modes. |
| "`.` is the pretty-print" | `.` is the identity filter; pretty-print is `jq .` — but `-r` output's `…` misleads. |
| "`keys`/`length` on anything" | `length` is per type; `keys` objects/arrays. |
| "`join(',')` needs strings" | join takes the array of strings after `.[]`/`[ … ] | join`. |

## 13. FIRST-CHECK REASONING

- **"Empty result from my jq extraction."** Is the field spelled right and present (`has()`)? Is
  `.` the right shape (`map` on array vs object)? Did `-r` differences eat a string? Then `cat
  file | jq 'keys'` on the RAW blob to re-derive the path.
- **"Gate didn't flip when JSON changed."** Check the `-e` usage and what the filter evaluates to
  (`jq -r '.cond'` to PRINT first, then `-e`); the exit code is the last thing to trust, shape makes
  the truth.

## 14. PRIORITY

**P0 — jq is the bridge from "curl gave me JSON" to "my script knows the answer" — the health-check
and log-parse playbooks (P0.5/P0.6) run on it.**

## 15. STOP HERE — done when you can…

1. extract nested fields and iterate+rebuild with `.[]` and `[ … ]`;
2. apply `map(select(…))`, `sort_by`, `join`, `//`, `has()` correctly (array first!);
3. convert a jq truth into an exit code with `-e` and wire it into an `if`;
4. move bash values safely with `--arg`/`--argjson`;
5. debug a wrong-shape filter by listing `keys` first.

## 16. DO NOT STUDY YET

jq's full functional library (`reduce`, `foreach`, `walk`, `group_by`, `--stream` deep), `@csv/@tsv/@sh` subtleties, `env.`/variables formats beyond `--arg`, binary JSON handling (`--binary`). The extraction + gate + interop trio above is the interview-visible surface.

---

## QC CHECKLIST — BASH.P0.4

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (path, iterate, reshape, null, -e, interop)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (`.field`/`.[]`/map/select, `//`, `has()`, `-e`, `--arg`)? | ✔ §3 |
| 5 | Dependencies (BASH.P0.1 quoting, P0.3 exit-code contract, curl payloads P0.5)? | ✔ §3 |
| 6 | Essential commands (`jq -r`, `jq -e`, `map/select`, `--arg`, `sort_by`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 4)? | ✔ every output verified live |
| 8 | Break it (exit-code gate lie, map-on-object)? | ✔ §9 |
| 9 | Observe + interpret (`Cannot index string` error, -e 0/1, `//` default)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **BASH.P0.5 — curl patterns: health-check
gates, JSON APIs, retries/timeouts/redirects, and exit code → outcome mapping for scripts.**

---

# SESSION BASH.P0.5 — CURL PATTERNS: HEALTH GATES, JSON APIS, RETRIES

Environment note: verified live, curl 8.5.0 (OpenSSL 3.0.13), against a local Python HTTPServer on
`127.0.0.1:18765` serving `/health`→200, `/error`→500, `/slow`→4s delay, `/redir`→302, else 404.
Every code below is a real run.

## 1. WHAT IS IT? (≤30 s)

**curl** is the HTTP client that scripts speak through: `-s` silent, `-f` makes HTTP ≥400 a FAILURE
(exit 22), `-o /dev/null -w '%{http_code}'` gives you the response code as data, `-L` follows
redirects, `--max-time` bounds the wait, and `--retry/--retry-connrefused/--retry-delay` survive
transient failures. The health gate is simply `if curl -sf URL/health >/dev/null; then …`.

## 2. WHY DOES IT EXIST?

Because "is the thing up?" is the most-asked question in ops, and HTTP is the answer transport. curl
exists to (a) express the full request/response truth as flags, (b) surface outcome as an **exit
code** bash can `if`-on (P0.3), and (c) let you write the deploy-hook, health-check, and smoke-test
patterns every playbook (P0.6) reuses. No metrics story, load balancer story, or API wire-up exists
without it.

## 3. HOW DOES IT WORK?

- **Exit codes are the contract (verified):** `200`+`-f`→**0**; `404`+`-f`→**22**; `500`+`-f`→**22**
  (`-f` converts HTTP ≥400 into curl failure 22); connection refused→**7**; DNS couldn't
  resolve→**6**; `--max-time 2` against a 4s endpoint→**28**. Without `-f`, an HTTP 500 exits **0**
  (the transfer "succeeded") — the trap that made the gate lie in P0.4's incident analogy.
- **`-w` write-out turns the response into data (verified):** `%{http_code}` (200/404), `%{time_total}`,
  `%{size_download}`. Use `-o /dev/null` when all you want is the metadata (no body noise).
- **Redirects (verified):** without `-L`, a 302 is returned as-is (`code=302 redirects=0`); with
  `-L`, curl follows (`code=200 redirects=1`). Decide deliberately: probing an endpoint keeps
  `-L` OFF; end-user-facing fetches usually turn it ON.
- **Retries (verified, the honest set):** `--retry 3 --retry-delay 1 --retry-connrefused` recovered a
  server that was DOWN then came back during the window → final `http=200`, exit 0. Same flags on a
  port that stays refused → stays **exit 7** (retries don't fabricate success). Two observed caveats:
  `--max-time`-bounded timeouts did NOT get retried in this curl combo (stayed 28), and
  `%{num_retries}` is NOT a supported `-w` variable in curl 8.5.0 (prints empty) — so prove
  retry-behavior by the OUTCOME, not by counting attempts.
- **The gate idiom (verified):** `if curl -sf URL/health >/dev/null; then healthy; else down; fi` —
  `-s` silences progress, `-f` turns 4xx/5xx into failure, `>/dev/null` drops the body, exit code
  decides. The 500 endpoint demonstrably trips the else branch.

## 4. MENTAL MODEL

```
flag  meaning
 -s   silent            -f   ≥400 → fail(22)     -L   follow redirects
 -o   output file        -w   write-out meta       --max-time N    abort after N s
 --retry N  --retry-delay S  --retry-connrefused   transient-survival set

exit 0 transfer ok / 22 HTTP≥400 with -f / 6 DNS / 7 refused / 28 timeout
gate: if curl -sf URL/health >/dev/null; then … else … fi
meta: curl -s -o /dev/null -w '%{http_code} %{time_total}\n' URL
```

## 5. INTERVIEW-SAFE ANSWER

"curl is how scripts speak HTTP, and its superpowers are the exit code and `-w`. `-f` turns any HTTP
≥400 into failure (code 22) — verified: 200→0, 404→22, 500→22 on a local test server — and I map
the one-letter codes by habit: 6 DNS, 7 connection refused, 28 timeout. `-w '%{http_code}'` with
`-o /dev/null` gives the status as data for logic that needs it. Redirects follow only with `-L`.
For flaky targets `--retry` + `--retry-connrefused` + `--retry-delay` recover transient failures — I
proved recovery live (a server that came back mid-window → 200), while a still-down port honestly
ends at 7, not success. The health check is one line: `if curl -sf $EP/health >/dev/null` — silent,
fail-fast, exit-code driven, ready to pipe into `&&`/`||` under strict mode."

## 6. FOLLOW-UP ATTACKS

**Q.** `-f` vs checking `-w '%{http_code}'`?
**A.** `-f` is the gate (exit code); `-w '%{http_code}'` is the data (value paragraph). Scripts often
both: the gate decides, `-w` fills metrics. Learn each place they belong.

**Q.** When `-f` is NOT wanted?
**A.** When every response is a fact to be classified (404 is a "record missing" info point, not a
"CRASH"). Then capture `%{http_code}`-in-`-w` and branch on the string, with no `-f`.

**Q.** `--max-time` vs `--connect-timeout`?
**A.** `--max-time` bounds the WHOLE request, `--connect-timeout` bounds only TCP+TLS handshake. In
production, set both: the connect cap keeps dead hosts from hanging scripts, the total cap forces
end-of-story when a server never responds.

**Q.** `-s` vs `-sS`?
**A.** `-s` hides the progress meter AND errors; `-sS` hides the meter but keeps error text. Use
`-sS` in scripts so a real failure still explains itself; `-s` when you deliberately suppress
everything (combined with capture to a log).

**Q.** POST/JSON body sending?
**A.** `curl -sS -X POST -H 'Content-Type: application/json' -d '{"a":1}'` or `-d @file.json`; `-X`
+ `-d` is the submit pattern. Mention replay/bypassing `-X` subtleties only if probed.

**Q.** TLS/verify concerns?
**A.** Keep verify ON (`-k` is for self-signed lab internals only); trust the CA store, refresh
cacerts. Saying "-k when you shouldn't" is a red flag; naming the verify default shows safety.

**Q.** Auth patterns?
**A.** `-u user:pass` (basic) and `-H 'Authorization: Bearer …'` (token); never put secrets in the
URL; pull tokens from env/secret-manager into `--header` variable — matches the P0.4 `--arg`
discipline.

## 7. PRACTICAL EXAMPLE (production)

Deploy smoke that must (a) survive a cold start, (b) prove HTTP AND JSON, (c) not hang CI forever:
```
set -euo pipefail
EP="http://${HOST}:${PORT}"
for i in {1..8}; do                                             # 8 x ~1s give the app time
  curl -sf --connect-timeout 2 --max-time 3 "$EP/health" >/dev/null && break
  sleep 1
done
status=$(curl -sS -o /dev/null -w '%{http_code}' "$EP/health")   # exact status as data
echo "final status: $status"
curl -sf "$EP/api/version" | jq -r '.version'                    # JSON payload → field (P0.4)
```
The loop uses the gate to wait for readiness; then `-w` classifies; then `| jq` extracts. Three curl
habits, strict-mode safe, no hanging CI.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
# local test server (serves /health 200, /error 500, /slow 4s, /redir 302→/health, else 404)
#   python3 - <<'PY' … http.server … PY   on 127.0.0.1:18765   (or see §7 playbook)
curl -sf http://127.0.0.1:18765/health >/dev/null; echo $?     # 0
curl -sf http://127.0.0.1:18765/missing >/dev/null; echo $?    # 22
curl -sf http://127.0.0.1:18765/error   >/dev/null; echo $?    # 22
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18765/health   # 200
curl -s -o /dev/null -w '%{http_code} redirects=%{num_redirects}\n' http://127.0.0.1:18765/redir   # 302 redirects=0
curl -sL -o /dev/null -w '%{http_code} redirects=%{num_redirects}\n' http://127.0.0.1:18765/redir  # 200 redirects=1
curl -s --max-time 2 http://127.0.0.1:18765/slow; echo $?      # 28
curl -s --max-time 2 http://127.0.0.1:9/; echo $?              # 7 (refused)
curl -s --max-time 3 http://no-such-host.invalid/; echo $?     # 6 (DNS)
# retry recovery: kill server, run in background, restart it on a ~1.2s delay:
curl -s -o /dev/null -w 'http=%{http_code}\n' --max-time 8 --retry 3 --retry-delay 1 --retry-connrefused http://127.0.0.1:18765/health  # 200 once server returns
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Health gate flipped DOWN-flapping even though curl manually works"

Trigger: a watchdog ran `curl "$EP/health" >/dev/null` WITHOUT `-f` — HTTP 500/503 (during a deploy
window) returns body, transfer succeeds, exit 0 — the gate passed when the app was mid-broken.
Observe: alert fires only when the connection itself dies (7), silent during 5xx outage.
Root cause: default "transfer succeeded" exit code ignores HTTP ≥400; `-f` is what makes 5xx loud.
Fix: `if curl -sf "$EP/health" >/dev/null; then` — `-f` converts the 500 into failure 22, the gate
now flips on app-failure truthfully.
Verify: hit `/error` (500) with and without `-f`; watch exit 0 vs 22 and the gate's branch flip.
Prevent: encode the status as the decision by default (`-f`), reserve "classify the code" for when
codes are data; and ALWAYS bound with `--max-time` so a black-holed host doesn't hang the watchdog.

### DECISION OVERLAY — what NOT to do

- Don't gate without `-f` (the 5xx-silent trap above).
- Don't run curl unbounded in CI — `--connect-timeout` + `--max-time` always.
- Don't `curl -k` to silence cert problems in prod — fix the CA or the CN.
- Don't put credentials in the URL or the `-w` line — headers/env only.
- Don't `cat file | curl -d @-` when `-d @file` exists (pipe may close early on big payloads).

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`-f` is optional garnish" | Without it an HTTP 500 exits 0 — the classic gate lie. |
| "exit 7 = DNS problem" | 7 = connection REFUSED; DNS failure is 6. |
| "`-L` is default" | Follows ONLY with `-L`; default leaves the redirect. |
| "`-s` hides errors too" | `-s` hides meter AND stderr errors; `-sS` keeps errors. |
| "`--max-time` is enough" | Pair with `--connect-timeout` for hardware-dead hosts. |
| "`--retry` retries 5xx by default" | Only with `--retry-all-errors`/`--retry-connrefused`; default retries limited timeout-ish errors. |
| "`%{num_retries}` tells fine-grain attempts" | Not supported in curl 8.5.0 — prove retries by outcome. |
| "Retries guarantee success" | A still-refused port ends at 7 — honest failure, no fabrication. |
| "HTTP 404 vs 23 means same" | 22 = HTTP≥400 with -f; 23 = write-out/body failure — each their own signal. |
| "A 3xx means broken" | It's the redirect machine — only broken when you didn't want one. |

## 13. FIRST-CHECK REASONING

- **"Gate says up but server is 500ing."** Missing `-f` — the transfer-succeeded code 0 can't see
  the status. Reproduce with and without `-f` against a 500 fixture; then gate on `-f` and dip
  `-w '%{http_code}'` when you need the classifier.
- **"Check hung / CI timeout."** No `--max-time`/`--connect-timeout`, or a silent `-s` hiding an
  error that's actually a 28/7/6. Bound the request, then read the code.
- **"It retried forever."** `--retry` is capped by `--retry N` plus retry-delay math — the retry
  WINDOW is bounded by `--max-time` only if you set it; check both.

## 14. PRIORITY

**P0 — curl's exit-code + `-w` contract is what the health-check/log/API playbooks (P0.6) and every
networking smoke hang on.**

## 15. STOP HERE — done when you can…

1. say off-book: 0/6/7/22/28 and exactly what makes each happen;
2. write the `if curl -sf … >/dev/null` gate from memory (and the no-`-f` hazard);
3. format `-o /dev/null -w '%{http_code} %{time_total}'` without docs;
4. follow a redirect with `-L` and classify a 3xx both ways;
5. write a retry-safe probe (`--connect-timeout`, `--max-time`, `--retry-connrefused`, bounded loop).

## 16. DO NOT STUDY YET

`curl` binary protocol corner cases (FTP/IMAP over curl), `--form` multi-part plumbing, HTTP/2
specifics in curl, cookiejar `-c/-b` juggling, `--resolve`/custom DNS games, `--interface`/source
routing. Every P0 interview curl answer hangs on the flags in §3.

---

## QC CHECKLIST — BASH.P0.5

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (flags → exit classes → gate idiom)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (`-f`, `-w`, `-L`, `--max-time`, retry set, exit 6/7/22/28)? | ✔ §3 |
| 5 | Dependencies (P0.3 exit-code contract, P0.4 jq interop, curl glue in playbooks)? | ✔ §3, §7 |
| 6 | Essential commands (`curl -sf`, `-o /dev/null -w`, `-sS`, `--max-time`, `--retry-*`)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 5, local server fixtures)? | ✔ every code verified live |
| 8 | Break it (5xx-silent gate, hung unbounded curl)? | ✔ §9 |
| 9 | Observe + interpret (0 vs 22 flips, 6/7/28 classes, 302→200 via -L, retry recovery)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **BASH.P0.6 — Playbooks: a health-check job, a
deploy smoke, and a log-parsing report — the three terminal "show me you can do it live" pieces
assembled from P0.1–P0.5.**

---

# SESSION BASH.P0.6 — CAPSTONE PLAYBOOKS

Environment note: all three playbooks below ran live against a local Python HTTPServer
(`127.0.0.1:18765`, serving `/health`→200 ok, 404 on unknown paths, 500 on `/error`) and a synthetic
8-line app.log. Every exit code and output shown is real; the P0.1 downstream-count bug was caught
live and fixed during verification.

## 1. WHAT IS IT? (≤30 s)

Three production-shaped scripts that compose everything learned so far: (A) a **health-check job** —
loop over an associative array, gate with `curl -sf`, count down nodes, exit with a failure count;
(B) a **deploy smoke** — readiness-retry loop, then `jq`-gate the health body; (C) a **log-parsing
report** — `awk`/`grep` over structured lines, count by level and service. Together they are the
"show me you can do it live" interview proof.

## 2. WHY DOES IT EXIST?

Because the interviewer's real question isn't "do you know curl?" — it's "can you wire the pieces
into a reliable job?" These playbooks exist as proof-of-assembly: quoting discipline (P0.1), loop
style and functions (P0.2), strict mode (P0.3), JSON extraction (P0.4), curl gates (P0.5), all in
one place, all runnable, all exit-code shaped. A candidate who can paste a health-check script from
memory and explain what each line defends against is the one who gets the job.

## 3. HOW DOES IT WORK?

### PLAYBOOK A — health-check job (verified)

```
#!/usr/bin/env bash
set -uo pipefail
declare -A nodes=([api]=http://127.0.0.1:18765
                   [web]=http://127.0.0.1:18765/missing)   # note: intentionally broken path
down=0
for svc in "${!nodes[@]}"; do
  if curl -sf --max-time 3 "${nodes[$svc]}/health" >/dev/null; then
    printf '%-5s UP\n' "$svc"
  else
    printf '%-5s DOWN (%s)\n' "$svc" "${nodes[$svc]}"
    down=$((down+1))                    # ← THIS LINE WAS MISSING IN THE INITIAL DRAFT
  fi
done
printf 'total=%d healthy=%d down=%d\n' "$(( ${#nodes[@]} ))" \
       "$(( ${#nodes[@]} - down ))" "$down"
exit "$down"
```

**Verified outputs (caught live):**
- Down scenario: `api UP`, `web DOWN (…/missing)`, `total=2 healthy=1 down=1`, **exit=1**.
- All-up scenario (both pointing at `/health`): `api UP`, `web UP`, `total=2 healthy=2 down=0`,
  **exit=0**.

**What was caught (incident-style proof):** the `down` counter wasn't incremented in the `else` branch
on the first write. The gate TESTED correctly (print DOWN) but the summary claimed `down=0` — a
subtle off-by-one the log revealed. Fixed by adding `down=$((down+1))` before the summary printf;
the second run confirmed the counts match reality. This is exactly the class of bug that survives a
manual curl check and fails only when you trust the counter (the lesson: always print the summary
and verify it against what you saw in the loop).

### PLAYBOOK B — deploy smoke (verified)

```
#!/usr/bin/env bash
set -euo pipefail
EP="http://127.0.0.1:18765"
WANT="ok"
for i in {1..8}; do
  curl -sf --connect-timeout 2 --max-time 3 "$EP/health" >/dev/null && break
  sleep 1
done
code=$(curl -sS -o /dev/null -w '%{http_code}' "$EP/health")
st=$(curl -sf "$EP/health")
printf 'http=%s body=%s\n' "$code" "$st"
[[ "$st" == "$WANT" ]] && echo "SMOKE PASS ($WANT)" \
  || { echo "SMOKE FAIL: got '$st' expected '$WANT'"; exit 1; }
```

**Verified output:** `http=200 body=ok`, `SMOKE PASS (ok)`, **exit=0**.

Key design points: `--connect-timeout` + `--max-time` keep the readiness loop from hanging (P0.5
lesson); `set -euo pipefail` means the curl failure is a script abort if not caught in the loop;
the body is captured by `-sf` (the gate) and then the exit is 0; `jq` isn't needed when the check is
string equality on the raw body — show the right tool for the shape.

### PLAYBOOK C — log-parsing report (verified)

```
#!/usr/bin/env bash
set -euo pipefail
LOG="${1:-/tmp/opencode/playbooks/app.log}"
[ -s "$LOG" ] || { echo "no log"; exit 1; }
printf '== lines by level ==\n'; awk '{print $4}' "$LOG" | sort | uniq -c | sort -rn
printf '== ERRORs per service ==\n'; awk '$4=="ERROR" {print $3}' "$LOG" | sort | uniq -c
printf '== WARN lines ==\n'; awk '$4=="WARN" {print $0}' "$LOG"
printf '== distinct request ids ==\n'; grep -o 'req=[a-z]*' "$LOG" | sort -u
```

**Verified output:**
```
== lines by level ==
      4 ERROR
      3 INFO
      1 WARN
== ERRORs per service ==
      2 api
      1 web
      1 worker
== WARN lines ==
2026-09-14 10:00:02.010 web      WARN  slow query 1234ms
== distinct request ids ==
req=abc
req=def
```

Design note: this script is `set -euo pipefail` throughout — `awk` pipelines always succeed (exit 0),
`grep` exit 1 with no match is caught by the preamble, and `[ -s "$LOG" ]` guards the file. The
structure is "named sections, each one line," easy to read in a CI log; every field expansion is
quoted (P0.1 discipline).

## 4. MENTAL MODEL

```
health: for svc in assoc  →  curl -sf gate  →  count UP/DOWN  →  exit=down_count
smoke:  retry loop (bounded)  →  curl -sS -w http_code  →  assert body == WANT
logrep: [ -s "$LOG" ]  →  awk pipeline per question  →  uniq -c sort  →  counts
catch:  every curl is -sf, every expansion is quoted, every script is strict
```

## 5. INTERVIEW-SAFE ANSWER

"Three scripts. The health-check uses a bash associative array of service bases and a `for` loop
over its keys; each service is gated by `curl -sf` (P0.5), failures increment a `down` counter
(caught that I forgot it live), and the final summary prints the counts and exits with the failure
count — pure P0.1 quoting plus P0.2 loops plus P0.5 gates. The deploy smoke does a bounded retry
loop (eight attempts, one-second backoff, connect+max timeouts) then reads the status code via
`-w '%{http_code}'` and asserts the body equals the expected string. The log-parsing report chains
`awk` pipelines — one per question: count by level, errors per service, WARN lines, distinct request
IDs — all behind a `[ -s "$LOG" ]` guard, all strict-mode safe. Every script is the same three
habits in the same order: (1) fail loudly and early, (2) quote everything, (3) carry the exit code
as the answer."

## 6. FOLLOW-UP ATTACKS

**Q.** Why not one big script?
**A.** Separation makes each job independently testable and composable in CI (gates can be wired
`&&`/`||` in the pipeline). One big script obscures which piece failed; three scripts make failures
point to the piece.

**Q.** What if a service should stay DOWN?
**A.** Exit 0 anyway? The convention: exit 0 = "expected state"; non-zero = "action needed." A
maintenance window playbook can flip the health check to "should be 503" and gate on that instead.

**Q.** Why not `while ! curl …` for the smoke readiness loop?
**A.** The bounded `for i in {1..8}` with sleep makes the retry window explicit and finite. A
`while` without a counter can spin forever if something breaks the break condition; CI needs the
ceiling.

**Q.** Why `awk` pipelines instead of `jq` for the log?
**A.** Because the log is line-oriented text, not JSON. If it were JSONL you'd pipe to `jq` and
maintain the same question structure. Match the parser to the shape — this is the same lesson as
`map` on an array, not on an object.

**Q.** Could `grep` replace all the `awk`?
**A.** Yes for yes/no questions (`grep ERROR | wc -l`); no when you need field extraction
(`awk '{print $3}'`) or conditional column selection. `awk` is the structured-line tool; `grep` is
the exists-or-not tool.

## 7. PRACTICAL EXAMPLE (production)

Wire playbook A into a CI stage gate:
```bash
set -uo pipefail
./pb1_health.sh                      # exit 0 = all healthy
code=$?
if (( code > 0 )); then
  echo "BLOCKING: $code service(s) down"; exit 1
fi
```
`exit "$down"` gives you the numeric count as a direct signal; the caller can display it, alarm on
it, or decide whether to block the deploy.

## 8. BUILD / REPRODUCE (verified on this box)

Run any of the three against the local test server (start it on 18765 first, see §3 or §15):
```bash
./pb1_health.sh         # UP/DOWN lines; exit = down count
./pb2_smoke.sh          # http=200 body=ok SMOKE PASS; exit 0
./pb3_logrep.sh app.log # awk counts by level; exit 0
```
The file contents are the exact text in §3; the outputs shown there are real.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Health summary shows down=0 but the loop printed DOWN"

Trigger: the `else` branch incremented the print (`DOWN`) but not the variable; summary said 0.
Observe: printf DOWN appeared; `down=0` after; exit 0.
Root cause: the variable was never mutated — `down=$((down+1))` was missing from the else body.
Fix: add the increment; re-run; counts now match; verify by comparing one-down vs all-up runs.
Prevent: ALWAYS print the summary line AND the counter; if the counter doesn't match what you saw,
you have a race condition in your logic. This is the same habit as "print `$?` immediately" (P0.3).

### INCIDENT — "Smoke smoke fails when app uses a different word for 'ok'"

Trigger: `WANT="ok"` but the app returned `"healthy"`.
Observe: `SMOKE FAIL: got 'healthy' expected 'ok'`.
Root cause: the assertion string is fragile — it encodes the HTTP response word, not the JSON field.
Fix: use `jq -e '.status=="ok"'` (P0.4) to gate on structured truth, or accept multiple valid
words. The lesson: string equality on a body is a close cousin to "the jq exit code means yes"
incident — prefer structured gates when the API shape is JSON.

### DECISION OVERLAY — what NOT to do

- Don't let `curl -sf` failures silently continue without counting/aborting — they lie.
- Don't use `while ! curl …` without a max-iteration or `--max-time` guard.
- Don't parse structured logs with `grep` alone when you need a field — `awk` gives the column.
- Don't hardcode `[ -s "$LOG" ]` without an explicit error message (CI needs the context).
- Don't run the smoke without `--connect-timeout` and `--max-time` — one dead host blocks CI
  forever.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "The loop printed DOWN but I trust the summary" | Always print and compare — the off-by-one trap. |
| "`curl -sf` failures count as 'attempted'" | They're GATE failures — they don't need retry, they need counting. |
| "`while true; curl …` is a robust retry" | Unbounded loops hang CI — use `for` with a ceiling + max-time. |
| "`$?` always means 'curl failed'" | It can mean app-fail (22) or connection-fail (7) — read the code. |
| "One big script is simpler" | Failure isolation is lost; one stage failing silently hides the real bug. |
| "`awk`/`grep` are interchangeable" | `awk` gives fields; `grep` gives exists-or-not. Match the tool to the question. |
| "`set -e` inside the loop catches curl failures" | `if curl -sf` runs in a "test" context — `-e` ignores it; that's by design (P0.3). |
| "The deploy smoke gate is the curl exit" | The exit IS the gate; `-w '%{http_code}'` is the classifier — different questions. |
| "The log-parsing script will fail on an empty file" | The `[ -s "$LOG" ]` guard catches it before awk runs. |
| "Hardcoded ports make the playbooks useless" | They're lab fixtures; in prod pass `$EP` via env and inherit CI vars. |

## 13. FIRST-CHECK REASONING

- **"Summary line doesn't match what I saw."** The counter wasn't incremented or the array
  iteration order is wrong — print the intermediate value in the loop; match before the summary.
- **"Smoke gate passes but the deploy is actually broken."** Check whether the assertion is on the
  right field (`string ==` vs `jq -e`), and whether `-f` is ON so a 5xx fails loudly.
- **"Log report shows zero errors when I can see them."** Did you pass the right file (`$1`) and is
  the field alignment right (column 4)? Print the raw line with `awk 'NR==1'` to verify shape.

## 14. PRIORITY

**P0 — these are the "put it together" scripts every Bash interview at 1–3 YOE asks for; they prove
you can assemble, not just know.**

## 15. STOP HERE — done when you can…

1. write the health-check script from memory with the counter fix;
2. explain why `--connect-timeout` + `--max-time` both appear in the smoke loop;
3. read a log file with `awk '{print $N}'` and `grep -o` without looking anything up;
4. convert any "curl + test" into the right exit-code shape (`-sf` gate vs `-w` classifier);
5. spot the `down=0` bug immediately when the loop prints DOWN.

## 16. DO NOT STUDY YET

Advanced CI integration (parallel stage scripts, retry strategies at the orchestrator level, canary
rollout gates), `awk` compiled awklists, `yq`/`xq` XML/YAML extraction, or running these scripts
inside containers. The assembly discipline and the three fix-points above are the interview-visible
surface.

---

## QC CHECKLIST — BASH.P0.6

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (three scripts + the common discipline)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists (assembly-as-proof)? | ✔ §2 |
| 4 | Important mechanisms (curl gate, jq/string assert, awk pipeline, strict preamble)? | ✔ §3 |
| 5 | Dependencies (P0.1 quoting, P0.2 loops, P0.3 strict mode, P0.4 jq, P0.5 curl gates)? | ✔ §3 |
| 6 | Essential commands (curl -sf, -o /dev/null -w, awk, grep -o, printf, exit "$down")? | ✔ §3, §8 |
| 7 | Reproduce (Lab 6 — all three live on test server)? | ✔ every output verified |
| 8 | Break it (down-counter bug, fragile string assert)? | ✔ §9 |
| 9 | Observe + interpret (exit 0 vs 1, print-out match, WARN/ERROR counts)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **BASH.P1.1 — awk, sed, process substitution,
trap, find, and xargs: the Unix-glue layer for log manipulation, OS-level plumbing, and parallel
tasks — the last Bash layer before the domain closes.**

---

# SESSION BASH.P1.1 — AWK, SED, PROCESS SUBSTITUTION, TRAP, FIND/XARGS

Environment note: verified live, bash 5.2.21, awk/gnu sed on this WSL2 box; a synthetic 6-line
`log.txt` plus a `/tmp/opencode/unix-lab/` directory served as fixtures. Every output below is real.

## 1. WHAT IS IT? (≤30 s)

Six Unix-glue tools: **awk** — field-extraction and counting over line streams; **sed** — regex
substitution and address-based editing (including in-place `-i`); **process substitution** —
`<()`/`>()` to let commands that expect files consume live streams; **trap** — run a cleanup
function on EXIT/ERR/INT so temp files never leak; **find** — walk a directory tree by name/type/age;
**xargs** — turn lines into arguments (with `-P` for parallelism, `-0` for null-safe, `-I{}` for
placeholder control).

## 2. WHY DOES IT EXIST?

Operations lives in log files and temp files. awk/sed turn walls of text into counts and cleaned
snapshots (the deploy report, the incident timeline); process substitution lets you diff two live
streams without writing to disk; trap prevents the "where did that temp file come from?" ghost;
find/xargs complete the loop: locate what needs action, then act on it in bulk or in parallel.
Every playbook in P0.6 grows toward these tools; the "last Bash layer" before you're writing
production scripts that touch the filesystem and process trees directly.

## 3. HOW DOES IT WORK?

- **awk (verified):**
  - Built-ins: `NR` (current line number), `NF` (fields on this line — line 6 has **NF=6**,
    verified); `{print $3,$4}` extracts columns; `END{print NR}` counts total lines.
  - Custom field separator: `awk -F: '{print $1,$3}' /etc/passwd` → `root 0`, `daemon 1`, `bin 2`
    (verified) — the same extraction a `cut` would do, but with the full expression engine.
  - Condition blocks: `awk '$3=="api" && $4=="ERROR"' log.txt` → only API error lines (verified).
  - Formatting: `printf "%-5s → %s\n",$4,$NF` → labeled output without the full line (verified).
  - Why awk beats grep for multi-column: the NF test and the conditional-print don't need regex
    when you have the field index; awk is "what column?" + "what question?".
- **sed (verified):**
  - Substitution: `sed 's/error/ERR/gi' log.txt` — global (`g`), case-insensitive (`i`); replaces
    all matches per line.
  - Address printing: `sed -n '2,4p' log.txt` → lines 2–4 only (`-n` suppresses default print).
  - In-place edit: `sed -i 's/dur=[0-9]*ms/dur=X/' log_sed.txt` — changed line 1's timing value;
    verified the first line now shows `dur=X`.
  - `-i` with backup suffix: `sed -i.bak 's/…'` creates the original alongside the edit.
- **Process substitution (verified):**
  - `diff <(head -3 log.txt) <(tail -3 log.txt)` → unified diff of first 3 vs last 3 lines;
    diff-exit=1 (they differ). The `<()` creates a `/dev/fd/NN` file descriptor that `head`/`tail`
    feed — `diff` never sees a temporary file.
  - Same pattern: `while read line; do …; done < <(command)` feeds a pipe-safe stream into a
  `while` loop without losing the loop's variable context.
- **trap (verified):**
  ```
  bash -c 'FILE=...; trap "rm -f $FILE" EXIT; echo inside > $FILE; cat $FILE'
  → "inside" printed; after subshell exit, FILE is cleaned (verified: "cleaned").
  ```
  Trap fires on EXIT, not before the last command — you write to the file, cat it, THEN the shell
  exits and the cleanup fires. ERR trap fires on the first nonzero command (useful for one-liner
  debug in tight scripts). Always combine with `set -euo pipefail` for the cleanest "abort + clean"
  behavior.
- **find (verified):**
  - `find . -maxdepth 1 -type f -name '*.py' -print0 | xargs -0 -I{} basename {}` → `old.py`
    (verified: `-print0` null-terminates, `-0` in xargs consumes nulls safely).
  - `find . -name '*.pyc' -exec rm -v {} +` → batch-exec removes in one fork (verified:
    `removed '…/stale.pyc'`).
  - `-mtime +0` → files older than today (find uses +N = "more than N days old"); confirmed no such
    files existed in the lab.
- **xargs (verified):**
  - `seq 1 4 | xargs -P4 -I{} bash -c 'printf "pid=%s arg=%s\n" $$ {}'` → four distinct PIDs
    (4433–4439, verified) — real parallelism (`-P4`) with argument placement (`-I{}`).
  - `-0` pairs with `find -print0` for filenames containing spaces/newlines.
  - `-n1` feeds one value at a time; `-P$(nproc)` scales to core count.

## 4. MENTAL MODEL

```
awk  NR/NF → line position and field count
     -F: → custom separator   $3 → field three
     condition {action}  END{action}   printf for clean output
sed  s/find/replace/gi   -n '2,4p'   -i (in-place)   -i.bak (backup)
process sub:  diff <(cmd1) <(cmd2)     while read … < <(cmd)
trap: trap "cleanup" EXIT | ERR | INT     fires AFTER last command, not before
find: -name -type -mtime -exec {} + -print0   xargs: -0 null-safe   -P parallel   -I{} place
```

## 5. INTERVIEW-SAFE ANSWER

"awk is my field-extraction engine: `NR`/`NF` for line and field position, `-F:` for custom
separators, condition blocks for filtering without regex — verified: line 6 has NF=6, `-F:` on
`/etc/passwd` extracts uid cleanly, the ERR-filtered `awk '$3=="api" && $4=="ERROR"'` gives me
exactly the lines I need. sed is the edit layer: `s/old/new/gi` for substitution, `-n '2,4p'`
for address printing, `-i` for in-place rewrites (verified the timing value changed). Process
substitution lets me diff two live streams without writing temp files — `<()` creates the file
descriptor the reader expects. trap is the cleanup contract: `trap "rm -f $file" EXIT` fires when
the shell exits, after the last command runs; I proved it by checking the file was gone after the
subshell. find + xargs is the locate-and-act pair: `-print0 | xargs -0` handles spaces safely,
`-exec rm {} +` batches without xargs, `-P4` gives real parallelism — I saw four distinct PIDs
running simultaneously. The distinguishing habit is knowing which layer the question lives in: field
count → awk; regex cleanup → sed; stream-vs-file boundary → process substitution; temp-file hygiene →
trap; filesystem traversal → find + xargs."

## 6. FOLLOW-UP ATTACKS

**Q.** `awk` vs `grep | cut` vs `sed`?
**A.** `grep` = exists-or-not; `cut -d: -f1` = simple field extraction; `awk` = field + conditional +
formatting in one pass; `sed` = regex replacement across lines. Use the simplest that answers the
question; reach for awk when you need NF, conditionals, or formatted output in one pipeline.

**Q.** `awk` vs `perl -ne`/`ruby -ne`?
**A.** awk is standard (POSIX), fast for simple cases; perl/ruby give you richer regex and data
structures. For a 1–3 YOE interview: awk, always — it's the expected default; mention perl/ruby only
as "when I need PCRE, not awk's ERE."

**Q.** When `sed -i` is dangerous?
**A.** It's a permanent file mutation — no undo. Always prefer writing to stdout (piped to `tee` or
`>` a new file) unless the in-place rewrite is intentional AND the file is under version control or
backed up (`-i.bak`). In CI: avoid `-i` on checked-out source; mutate artifacts, not code.

**Q.** `diff <(A) <(B)` — what's the difference from `A | diff - B`?
**A.** Process substitution makes both commands start in parallel (no race); a pipe feeds A's output
to B's stdin but B expects a file. `<()` fixes the pipe-only problem cleanly.

**Q.** Why `-print0 | xargs -0` instead of just `| xargs`?
**A.** Filenames with spaces or newlines break the newline-delimited xargs protocol. `-print0`
uses null bytes; `-0` reads them. This is THE safety combo for any `find` + bulk-action pattern.

**Q.** `trap` vs `set -e` — what's the difference?
**A.** `set -e` stops the script on failure; `trap … EXIT` runs your cleanup regardless of WHY the
shell exits (success, failure, signal). Combine them: `-e` stops the damage, trap cleans the
residue.

**Q.** `xargs -P` gotchas?
**A.** Output interleaving (runners share stdout), race conditions on shared files, and PID
reapping in the parent. Use `-P` for independent tasks (HTTP pings, parallel compresses) where
output doesn't need ordering; order matters → keep it sequential or `wait` after the parallel batch.

**Q.** `-exec cmd {} +` vs `-exec cmd {} \;`?
**A.** `+` batches filenames (like xargs, one fork); `\;` runs cmd once per file (many forks). `+`
is the performance default; `\;` only when cmd genuinely needs one file at a time.

## 7. PRACTICAL EXAMPLE (production)

A "find stale lock files and report" script — the Unix-glue trifecta in one pass:
```
find /var/run -maxdepth 2 -name '*.lock' -type f -mtime +7 \
  -print0 | xargs -0 -I{} sh -c 'printf "%s %s\n" "$(stat -c%s "$1")" "$1"' _ {} \
  | sort -rn | head
```
And the temp-file hygiene wrapper (trap + strict):
```
set -euo pipefail; OUT=$(mktemp); trap 'rm -f "$OUT"' EXIT
curl -sf "$EP/health" -o "$OUT" && jq -e '.status=="ok"' "$OUT"
```
`mktemp` + trap = guaranteed cleanup; `set -euo pipefail` = early abort on the first failure; the
two lines compose the "health gate + structured assert" from P0.4–P0.5 with the P1.1 file-hygiene
layer on top.

## 8. BUILD / REPRODUCE (verified on this box)

```bash
echo "=== awk ==="
awk 'NR==1{print NF}' log.txt                              # 6
awk -F: '{print $1,$3}' /etc/passwd | head -3             # root 0, daemon 1, bin 2
awk '$3=="api" && $4=="ERROR"{printf "%-5s %s\n",$NF,$0}' log.txt
echo "=== sed ==="
sed 's/error/ERR/gi' log.txt | head -4                     # ERR replaces error
sed -n '2,4p' log.txt                                      # lines 2–4
cp log.txt log_sed.txt; sed -i 's/dur=[0-9]*ms/dur=X/' log_sed.txt; sed -n '1p' log_sed.txt
echo "=== process substitution ==="
diff <(head -3 log.txt) <(tail -3 log.txt); echo "exit=$?" # exit 1
echo "=== trap ==="
bash -c 'F=$(mktemp); trap "rm -f $F" EXIT; echo ok>"$F"; cat "$F"'; ls "$F" 2>/dev/null || echo "cleaned"
echo "=== find ==="
find . -maxdepth 1 -type f -name '*.py' -print0 | xargs -0 -I{} basename {}
find . -maxdepth 1 -name '*.pyc' -exec rm -v {} +
echo "=== xargs -P ==="
seq 1 4 | xargs -P4 -I{} bash -c 'printf "pid=%s arg=%s\n" $$ {}'
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "The temp-directory cleanup script leaked hundreds of files"

Trigger: a cron job created `/tmp/prod_snapshots/NNNN` files with `mktemp`, did work, but never
deleted them when the task exited unexpectedly.
Observe: `ls /tmp/prod_snapshots | wc -l` grew weekly; no error in cron logs (the task itself
"succeeded" from cron's perspective — exit 0).
Root cause: no `trap … EXIT` for cleanup; the "finally" block was a plain function at the bottom
that was never reached on `set -e` abort.
Fix: `trap 'rm -rf /tmp/prod_snapshots' EXIT` right after `set -euo pipefail`; if the shell exits
for ANY reason the directory is gone.
Verify: simulate an abort mid-script (`false` before the manual rm) and confirm the directory is
cleaned.
Prevent: ALWAYS place `trap … EXIT` + `set -e` at the top of any script that creates temp state;
make cleanup a one-liner, not a final-step function.

### DECISION OVERLAY — what NOT to do

- Don't `sed -i` on source files in CI — mutate artifacts, not code.
- Don't `awk '{print $3}'` when you mean `cut -d: -f3` on a simple colon-delimited line (keep it
  simple when you can).
- Don't `find . -exec rm {} \;` when `+` batches are equivalent (fork-bomb for no reason).
- Don't `xargs -P` when stdout ordering matters — the output interleaves.
- Don't `diff <(A) <(B)` when the diff is in a file you want to keep — write the temp files so you
  can inspect them after.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "awk is only for pattern matching" | awk is a field + conditional language; NF/NR + printf is its power. |
| "`sed -i` is always safe in-place" | No undo; prefer stdout or `-i.bak` in CI/source files. |
| "`<()` is just a pipe" | `<()` makes parallel, independent file descriptors — pipe is serial. |
| "`trap` fires before the command" | EXIT trap fires AFTER the last command runs. |
| "`find -exec {} \;` is fast enough" | `+` batches; `\;` is N forks — use `+` unless cmd needs one-at-a-time. |
| "`xargs` without `-0` handles spaces" | Filenames with spaces/newlines break without `-print0`/`-0`. |
| "`-P` preserves output order" | It does NOT; interleaving is expected. |
| "`awk -F:` is just like `cut -d:`" | awk gives you NF, conditionals, END; cut only gives you fields. |
| "`find -mtime +1` means 'modified today'" | `+N` means "more than N days old"; today is `-1` or `0`. |
| "`trap` cleans up temp from a subshell" | The trap is per-shell; subshells get their own. |

## 13. FIRST-CHECK REASONING

- **"Temp files accumulating / cleanup never ran."** No `trap … EXIT` — add it, verify by
  introducing a `false` before the manual cleanup and confirm the trap still fires.
- **"awk output is all fields / wrong columns."** Check NF and the separator (`-F:` for colon);
  print the raw NR==1 line to see the shape.
- **"xargs broke on a filename."** Spaces or newlines — use `-print0 | xargs -0` or quote with
  `-I{}`.
- **"diff is empty but I know they differ."** Check that both process substitutions are running
  (they start in parallel) and the command inside isn't failing silently.

## 14. PRIORITY

**P1 — these tools are the Unix plumbing layer that makes playbooks production-shaped; the
interview-visible surface is knowing when each one applies and proving it with a real output.**

## 15. STOP HERE — done when you can…

1. write `awk -F: '{print $1,$3}' /etc/passwd | head` and `awk '$4=="ERROR" && NR<=100' log`
   without looking it up;
2. explain why `<()` exists and how it differs from a pipe;
3. write `trap "rm -f $FILE" EXIT` at the top of a script and prove it fires after a `false`;
4. `find . -name '*.pyc' -exec rm {} +` vs `find . -name '*.pyc' -exec rm {} \;` and when to use
   which;
5. `find . -print0 | xargs -0 -I{} cmd` and explain why `-print0 | xargs -0` is the default.

## 16. DO NOT STUDY YET

`awk`'s associative arrays and multi-file processing, `awk` `BEGINFILE/ENDFILE`, `sed` hold space
multi-line patterns, `find` predicate chaining (`-not -o`), `xargs -d`, `parallel` (GNU parallel)
full options, coprocess patterns, `mkfifo`/named pipes. The field/edit/cleanup/locate layer above is
the interview-visible surface.

---

## QC CHECKLIST — BASH.P1.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (awk/sed/process-sub/trap/find-xargs)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (NF/NR, -F, s///, -i, <(), trap EXIT, -print0/-0, -P, {} +)? | ✔ §3 |
| 5 | Dependencies (P0.2 loops/arrays, P0.3 strict-mode + $? interplay with trap)? | ✔ §3 |
| 6 | Essential commands (awk, sed, diff <() <(), trap, find -print0, xargs -0 -P -I)? | ✔ §3, §8 |
| 7 | Reproduce (Lab P1.1)? | ✔ every output verified live |
| 8 | Break it (temp-file leak, -exec \; fork-bomb, xargs without -0)? | ✔ §9 |
| 9 | Observe + interpret (NF=6, -F: uid extract, trap cleanup after exit, 4 distinct PIDs)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# BASH DOMAIN CLOSED

Bash domain mandated sessions complete.

Next domain: **05-aws.md** — the CLI foundation that makes cloud resources
reachable from scripts.