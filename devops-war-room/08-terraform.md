# 08 — TERRAFORM

Mastery ladder: **P0 → P1 → P2 → IGNORE**

Priority Map (session-by-session):
| Session | Topic | Priority | Status |
|---|---|---|---|
| TF.P0.1 | Core model: HCL, resources, plan/apply/destroy | P0 | **COMPLETE** |
| TF.P0.2 | State: file, import, mv/rm, locking, remote | P0 | **COMPLETE** |
| TF.P0.3 | Remote backends: S3/DynamoDB, team state | P0 | **COMPLETE** |
| TF.P0.4 | Plan/apply flags: target, var, refresh, parallelism | P0 | **COMPLETE** |
| TF.P0.5 | Drift detection + failure set + partial apply | P0 | **COMPLETE** |
| TF.P0.6 | count vs for_each vs for, dynamic blocks | P0 | **COMPLETE** |
| TF.P0.7 | Modules: structure, source, versioning | P0 | **COMPLETE** |
| TF.P1.1 | lifecycle, moved, prevent_destroy, ignore_changes | P1 | **COMPLETE** |
| TF.P1.2 | Terraform in CI: plan-as-gate, apply-on-merge | P1 | **COMPLETE** |
| TF.P1.3 | terraform console | P1 | **COMPLETE** |
| TF.P2.1 | JSON syntax / import CLI | P2 | **COMPLETE** |
| TF.P2.2 | TF Cloud vs Atlantis vs Spacelift | P2 | **COMPLETE** |

Session Log:
| Session | Topic | Priority | Status |
|---|---|---|---|
| TF.P0.1 | Core model: HCL, resources, plan/apply/destroy | P0 | **COMPLETE** |
| TF.P0.2 | State: file, import, mv/rm, locking, remote | P0 | **COMPLETE** |
| TF.P0.3 | Remote backends: S3/DynamoDB, team state | P0 | **COMPLETE** |
| TF.P0.4 | Plan/apply flags: target, var, refresh, parallelism | P0 | **COMPLETE** |
| TF.P0.5 | Drift detection + failure set + partial apply | P0 | **COMPLETE** |
| TF.P0.6 | count vs for_each vs for, dynamic blocks | P0 | **COMPLETE** |
| TF.P0.7 | Modules: structure, source, versioning | P0 | **COMPLETE** |
| TF.P1.1 | lifecycle, moved, prevent_destroy, ignore_changes | P1 | **COMPLETE** |
| TF.P1.2 | Terraform in CI: plan-as-gate, apply-on-merge | P1 | **COMPLETE** |
| TF.P1.3 | terraform console | P1 | **COMPLETE** |
| TF.P2.1 | JSON syntax / import CLI | P2 | **COMPLETE** |
| TF.P2.2 | TF Cloud vs Atlantis vs Spacelift | P2 | **COMPLETE** |

Hard rules for every session: em-dashes, terse, local-only if it touches a lab. All P0 labs run against `/tmp/tfdemo`. All scratch demos are destroyed after verification. No emojis. No fabricated outputs — whatever a session prints, it was actually run against `terraform v1.16.2` on this machine.

### How to run every lab in this file

```bash
export PATH="$HOME/.local/bin:$PATH"   # terraform v1.16.2 lives here
export AWS_PAGER=""                    # never page AWS CLI output
cd /tmp/tfdemo                         # the only demo project state ever touches
```

Every command block in the P0 sessions was executed verbatim in this shell against this project. The state file you find there is the one derived from those runs — `main.tf` is the pristine 16-line original. Re-run any block and you should reproduce the outputs printed here. Scratch labs (count/for_each, modules, docker, tls, time) ran in temporary subdirectories and were all destroyed — the directory is empty of them on purpose.

Priority discipline: P0 first, always. Plan your one-line answer to each queue item, then check QC row 13 (SELF-VERIFY) before calling any session done.

---

## TF.P0.1 — Core model: HCL, resources, plan/apply/destroy

One-line focus: know exactly what each core command does, why state is the source of truth, and how config becomes infrastructure. This is the single most important session in the whole interview prep — half of every Terraform screen starts with "explain plan vs apply."

The interview wants to know you can explain, in one breath, the full loop: Terraform reads your HCL and the current state, compares it with the real remote objects via the provider, proposes a diff (plan), and then converges the real world to match config (apply), recording the result back in state.

### 1. Concepts — the five building blocks

- **Provider** — the plugin that speaks the API of the thing you manage (aws, azure, google, local, docker). Declared with `required_providers`. Without it Terraform has no vocabulary.
- **Resource** — a unit of infrastructure Terraform manages, e.g. `local_file.f`. It is the only thing that can be created/destroyed. Written as `resource "type" "name" { ... }`, addressed as `type.name`.
- **Data source** — read-only lookup, `data "type" "name"`, addressed as `data.type.name`. Never creates anything, just fetches. Example: pulling a filtered AMI before attaching it to an instance.
- **Variable** — input to the module, `variable "x" { type = string }`, referenced as `var.x`. Overridable with `-var`, `-var-file`, `TF_VAR_` env vars, or `terraform.tfvars`.
- **Local** — a named temporary expression, `locals { name = upper(var.x) }`, referenced as `local.name`. Good for de-duplicating repeated expressions.
- **Output** — the return value of a module, `output "path" { value = ... }`. Root outputs are printed after apply — module outputs are what a parent module can read.

Trap: data sources refresh on every plan — a data source used in a plan that depends on something being created in the same apply can behave like a moving target.

### 2. The core HCL file

The demo project `/tmp/tfdemo/main.tf` is 16 lines and contains every core concept except variables/locals (they were left out of the project on purpose — it is a minimal lab):

```hcl
terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "f" {
  content  = "hi"
  filename = "/tmp/tfdemo/out.txt"
}

output "path" {
  value = local_file.f.filename
}
```

Read it out loud to an interviewer: the `terraform` block pins the provider source, the resource block declares a managed object, the output exposes a value. Nothing is provisioned until you apply.

### 3. The command lifecycle — what each verb means

- `terraform init` — one-time setup. Downloads provider plugins, builds `.terraform/`, writes the dependency lock file `.terraform.lock.hcl`. Re-run whenever you change providers, modules, or backend config.
- `terraform plan` — read-only. Refresh real state, compute diff, print a preview. It NEVER changes anything.
- `terraform apply` — converge. Executes the plan's create/update/destroy in dependency order, then writes the final state. Without `-out` it re-plans first, so the applied plan may differ from an earlier `terraform plan`.
- `terraform destroy` — apply with an empty config. Destroys everything in state. Same engine as apply — think of it as "apply nothing."
- `terraform fmt` / `terraform validate` — syntax and static check. `validate` requires providers installed (init first).

Mental model: HCL → Plan → Apply → State. Every apply is state → real-world → state. State is not a cache — it is the source of truth for what Terraform owns.

### 4. Why state matters (the answer interviewers grade on)

The config says what you WANT. State says what you HAVE. Plan compares config against state and reality — then apply reconciles the delta. Good answers name four state responsibilities:
1. **Maps config to real objects** — stores provider-assigned IDs so Terraform can find the real thing ("this local_file is that file on disk").
2. **Stores attributes** — outputs and interpolations read prior apply results.
3. **Tracks relationships** — the dependency graph for accurate, ordered diffing (knows a subnet must exist before an instance).
4. **Enables inspection** — `outputs`, `state list/show`, and `console` read from it.

The one-sentence version to give in an interview: "Plan is a preview of the diff between desired config and reality — apply is the convergence step that makes reality match, and state records what was done so the next plan starts from a correct baseline."

### 5. Plan vs apply — two words, three phases

A single plan graph walk does:
1. **Refresh** — calls the provider's read functions for every resource in state to learn the current real-world attributes.
2. **Diff** — compares refreshed attributes against config, producing create/update/destroy/no-op actions.
3. **Order** — sorts actions by dependency so nothing is created before its dependencies.

The classic trap: people think plan is "a dry run of apply." It is a dry run of the DIFF — apply then re-walks and executes. If the world changed between plan and apply, apply can produce different actions.

### 6. Verify — run the real loop on /tmp/tfdemo

Environment: `export PATH="$HOME/.local/bin:$PATH"` — terraform 1.16.2 lives at `~/.local/bin/terraform`. No cloud, provider is `hashicorp/local`.

```bash
$ cd /tmp/tfdemo
$ terraform -version
Terraform v1.16.2
on linux_amd64

$ terraform init -input=false
Initializing the backend...
Initializing provider plugins...
- Reusing previous version of hashicorp/local from the dependency lock file
- Using previously-installed hashicorp/local v2.9.1
Terraform has been successfully initialized!
```

Then plan — the state already matched config, so this is the happy path:

```bash
$ terraform plan -input=false
local_file.f: Refreshing state... [id=c22b5f9178342609428d6f51b2c5af4c0bde6a42]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration
and found no differences, so no changes are needed.
```

Then apply — note the real-world message: plan already converged, so apply is a no-op:

```bash
$ terraform apply -auto-approve -input=false
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:
path = "/tmp/tfdemo/out.txt"
```

Force a real change to see the converge path — `-replace` tells Terraform to forget and recreate (used for a broken/out-of-band instance):

```bash
$ terraform apply -auto-approve -input=false -replace=local_file.f
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

Inspect state, show a single resource, confirm the file on disk:

```bash
$ terraform state list
local_file.f

$ terraform state show local_file.f
# local_file.f:
resource "local_file" "f" {
    content              = "hi"
    content_base64sha256 = "j0NDRmSPa5bfid2pAcUXaxCm2Dlh3TwayItZstwyeqQ="
    content_md5          = "49f68a5c8493ec2c0bf489821c21fc3b"
    content_sha1         = "c22b5f9178342609428d6f51b2c5af4c0bde6a42"
    filename             = "/tmp/tfdemo/out.txt"
    id                   = "c22b5f9178342609428d6f51b2c5af4c0bde6a42"
}

$ cat out.txt
hi
```

Destroy — the same engine as apply, run against nothing:

```bash
$ terraform destroy -auto-approve -input=false
local_file.f: Destruction complete after 0s
Destroy complete! Resources: 1 destroyed.
```

After this session the demo directory was restored to its exact original shape (16-line main.tf, empty-but-present state) so every later session starts clean.

### 7. Quick-reference one-liners

- `init` — "get ready, download plugins"
- `plan` — "show me the diff, change nothing"
- `apply` — "make reality match, record it"
- `destroy` — "apply with config set to empty"
- `fmt` — "format HCL consistently"
- `validate` — "is this config syntactically and semantically OK"

### 8. Common pitfalls

- Running apply from a directory that was never `init`ed — Terraform will remind you and refuse.
- Editing providers without re-running init — the lock file and config disagree, explicit error.
- Believing plan output is the same as the apply you later run — without `-out`, apply re-plans.
- Forgetting to pin provider versions — drift in provider behavior breaks "it worked yesterday."
- Using `-auto-approve` in CJ/CD without a plan artifact — applying an un-reviewed diff.

### 9. Interview Q&A

Q: What does `terraform plan` actually do before printing the diff?
A: First it refreshes — calls every provider's read function for each resource in state — then diffs the refreshed reality against config, then orders the resulting create/update/destroy actions by dependencies.

Q: Why does state matter? Why can't Terraform just read the live cloud to figure things out?
A: Because there is no universal query for "what did my config create." IDs, sensitive attributes, and derived values live only where they were written last apply. Reading live state alone cannot determine what belongs to whom — state draws the ownership boundary.

Q: Plan says "No changes" but I deleted a file in the console — how?
A: It printed "No changes" because apply had already run and recorded a matching state — or the refresh hadn't happened. Delete the file again, run plan, and it will show a destroy/recreate — that is drift, the subject of TF.P0.5.

Q: Is `terraform destroy` a different program?
A: No — it is apply with an empty configuration across the same graph engine. The destroy lifecycle hooks differ, but the machinery is identical.

Q: What happens if two people run apply at the same time against local state?
A: Last writer wins silently — no locking exists on a plain `terraform.tfstate`. That is exactly why remote backends exist (TF.P0.3).

### 6.1 Deep dive — the idempotent double-apply

The most useful property of Terraform you will ever name in an interview: **apply is idempotent**. Running the same apply twice against an already-converged state is a no-op. That is what the lab showed when the first apply reported "0 added, 0 changed, 0 destroyed" — state already matched config, so there was nothing to do.

This is why the standard "run apply, see no changes, ship it" flow works, and it is why the drift-check leg in CI (TF.P1.2) is cheap: an empty plan is a convergence proof with zero side effects.

### 6.2 The refresh trap — plan is never optional

The refresh step means plan has a READ side effect: it calls the provider for every resource in state. With an API that is slow, rate-limited, or briefly degraded, plan itself can hang. Teams discover this the hard way when a "read-only" plan job times out in CI. The responses: workers that size the refresh leg realistically, and `-refresh=false` for emergency-only (TF.P0.4).

### 6.3 Reading a plan line like an ops person

Every plan ends with the action summary — memorize its exact shape:

```
Plan: 2 to add, 0 to change, 1 to destroy.
```

- `add` — new objects that do not exist and will be created
- `change` — existing objects mutated in place
- `destroy` — objects removed (either by config removal or recreation)

A healthy plan for a routine feature branch touches exactly the resources it should. A plan that deletes a database you never mentioned is a STOP sign, not a review item — and it is exactly what `prevent_destroy` (TF.P1.1) turns into an ERROR for those resources.

### 6.4 The equality that wins arguments

When an interviewer asks "what does Terraform do," the cleanest full-sentence answer is:

"Terraform expresses infrastructure as declarative configuration, then via plan compares that intent to reality (through state), and via apply converges reality to intent, recording the outcome back into state — unmanaged change is later surfaced as drift."

That single sentence contains HCL, plan, apply, state, and drift — the five P0 keywords of this domain.

### 6.5b Variable plumbing — the interview table

Variable input comes from four layers — the precedence is worth memorizing cold:

| Source | Example | Priority (higher wins) |
|---|---|---|
| command line | `-var 'env=prod'` | 1 — highest |
| env vars | `TF_VAR_env=prod` | 2 |
| tfvars files | `prod.tfvars`, `terraform.tfvars` | 3 |
| default in config | `variable "env" { default = "dev" }` | 4 — lowest |

Two details interviewers probe: `terraform.tfvars` loads automatically (explicitly-named `foo.tfvars` need `-var-file=foo.tfvars`), and `-var-file` values can be overridden by a later `-var` on the same run. The classic mistake — vars set in CI but shadowed by a committed `.tfvars` with different values — makes the "placeholder via tfvars, override via TF_VAR" idiom the safe default for env-specific pipelines (TF.P1.2).

### 9.5 Mock interview drill — the elevator plan (60 seconds)

Prompt: "Run me through a terminal session that goes from nothing to a managed resource and back, and tell me which step is the dangerous one."

Your answer skeleton (record yourself once, then trim):
- "init — downloads the provider and builds the working dir"
- "plan — reads state and real world, proposes a diff — this is the checkpoint where humans and CI look"
- "apply — converges reality to the plan and writes state — the dangerous step is applying something nobody reviewed, because there is no undo beyond recreating"
- "destroy — apply of nothing, same engine — risky only when run blindly with no intent check"

Checklist for the answer: names all five verbs, explains plan can't mutate, names state as the recorded outcome, and flags apply-without-review as the hazard.

### 9.6 Second drill — the config-vs-state story (90 seconds)

Prompt: "Immediately after a fresh apply, is config == state == world? And a week later?"

Answer: after apply, config matches state and state matches the world — three-way equality. A week later, world may have drifted (console edits) while state and config remained equal — the drift gap. Plan re-detects and, if you converge, restores the three-way lockstep — config is the discipline, state is the record, reality is the judge. Ending on the one-sentence triangle makes the 90-second version land: "apply is derived from config, recorded in state, validated against reality — drift breaks the triangle, plan finds it, apply restores it."

### 10. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can explain provider vs resource vs data source in one sentence each | |
| 2 | Can state the 4 responsibilities of state | |
| 3 | Knows plan is a diff preview, not a dry-run of apply | |
| 4 | Knows the three phases baked into plan: refresh, diff, order | |
| 5 | Has run init/plan/apply/destroy against a real project | |
| 6 | Can read a plan summary line (N to add, M to change, K to destroy) | |
| 7 | Knows when init must be re-run | |
| 8 | Knows what `.terraform.lock.hcl` is for | |
| 9 | Can explain why -replace showed "1 added, 1 destroyed" | |
| 10 | Knows destroy is apply against empty config | |
| 11 | Can read `state show` output and find the resource id | |
| 12 | Can explain why the tfdemo plan said "No changes" after a prior apply | |
| 13 | **SELF-VERIFY** — Reran init/plan/apply/state/show/destroy in `/tmp/tfdemo`, saw outputs match this session, restored the dir | |

Verdict: P0.1 core loop is a PASS only when you can narrate the full state/config/reality triangle without notes. Everything else in this domain builds on it.

Next session: TF.P0.2 — take the state file you just touched and take it apart (anatomy, move/remove, import, locking).

---

## TF.P0.2 — State deep-dive: anatomy, mv/rm, import, locking

One-line focus: the state file is JSON — be able to read it, and know the five state-editing commands plus why concurrent writes are dangerous.

The interview wants to know you treat state as a first-class artifact: where it lives, what it contains, how to repair it surgically (`mv`, `rm`, `import`), and why teams must lock it. There is a near-certain question on "what breaks when two applys collide" and "how do you bring an existing resource under management — import."

### 1. State file anatomy — what you are really looking at

`terraform.tfstate` is JSON of schema version 4 (in modern releases). High-level shape:

- `version` — state serialization format (4 for current).
- `terraform_version` — which CLI wrote this state.
- `serial` — a monotonic counter — backends use it to detect stale writes.
- `outputs` — the recorded output values.
- `resources` — one entry per managed resource, keyed by `module` + `type` + `name`, each with `instances` for multple `count`/`for_each` instances.
- Each instance has: `attributes` (the values the provider reported back), `sensitive_attributes`, `dependencies` (the graph edges), and `private` (provider internals — do not edit).

Trap: state contains real secrets. A `tls_private_key` or an `aws_db_password` sits in plaintext JSON unless an attribute is marked sensitive — and even then the raw value is still stored, just hidden in output. Never commit state files to git unencrypted.

### 2. The five state-editing commands

- `terraform state list` — list addresses of everything in state.
- `terraform state show <addr>` — dump one resource's attributes.
- `terraform state mv <src> <dst>` — rename/re-address in state (works across module boundaries and to/from flat addresses) without touching the real object.
- `terraform state rm <addr>` — drop from state (orphan — Terraform will forget it — the real object is untouched).
- `terraform state pull` / `terraform state push` — get the raw state bytes / overwrite state from stdin. `pull` is a read-only escape hatch used when you want to diff or back up — `push` is dangerous and should basically never be run ad-hoc.
- `terraform import <addr> <id>` — adopt an existing real object into state using a provider-specific import ID.

Mental model: `mv` and `rm` edit the MAP, not the WORLD. Import adds an entry to the map for something that already exists in the world.

### 3. State locking — why it exists, what happens on collision

With a plain local backend there is NO locking: two `apply`s can interleave, both write `terraform.tfstate`, and the last writer wins, losing the other's resources in state. Remote backends (S3 + DynamoDB, TF Cloud, etc.) take a lock before plan/apply and release it after. If a second run tries while a lock is held:

```bash
Error: Error acquiring the state lock

Error message: ConditionalCheckFailedException: The conditional request failed
```

Typical causes: a crashed apply that never released the lock, a long-running apply from CI, someone's plan hung. Fix: `terraform force-unlock <lock-id>` — but only after confirming the holder is actually dead, otherwise you can corrupt state.

Trap: an interrupted apply leaves state in a half-written state. That is why the file has `.backup` siblings — every state write first copies the previous state to a `.backup` file, so you can always roll back one step.

### 4. Import — the honest local picture

Import needs two things: the resource block must exist in config first, and the provider must implement import for that resource. Both were verified live against v1.16.2.

First attempt — resource present nowhere in config. Terraform refuses before talking to the provider:

```bash
$ terraform import local_file.f2 /tmp/tfdemo/other.txt
Error: resource address "local_file.f2" does not exist in the configuration.

Before importing this resource, please create its configuration in the root
module. For example:

resource "local_file" "f2" {
  # (resource arguments)
}
```

So: write the config block first, then import. Add a matching block and retry — and hit the second reality: the `local` provider (v2.9.1) genuinely does not implement import for `local_file`:

```bash
$ terraform import local_file.f2 /tmp/tfdemo/other.txt
local_file.f2: Importing from ID "/tmp/tfdemo/other.txt"...
Error: Resource Import Not Implemented

This resource does not support import. Please contact the provider developer
for additional information.
```

This is a real, runnable finding — "not every resource supports import" is the actual interview lesson. The mechanics of a successful import were verified with the `hashicorp/time` provider (fully local, no cloud). The provider needs the import ID in a specific format — `BASETIMESTAMP,YEARS,MONTHS,DAYS,HOURS,MINUTES,SECONDS`:

```bash
$ NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
$ terraform import time_offset.day "$NOW,0,0,1,0,0,0"
  Prepared time_offset for import
time_offset.day: Refreshing state... [id=2026-09-14T18:32:17Z]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

$ terraform state show time_offset.day
# time_offset.day:
resource "time_offset" "day" {
    base_rfc3339   = "2026-09-14T18:32:17Z"
    day            = 15
    id             = "2026-09-14T18:32:17Z"
    ...
}
```

Next plan will treat that imported object as owned — a subsequent `plan` will propose deleting or changing the offset based on config, exactly like any managed resource. In the cloud world the same mechanics look like `terraform import aws_instance.web i-0abcd1234` — the ID is the cloud-side identifier.

### 5. Verify — mv, rm, pull against the real demo project

Re-apply first so there is a live resource to manipulate, then mutate its address and revert. Running transcript:

```bash
$ cd /tmp/tfdemo
$ terraform apply -auto-approve -input=false         # state now has local_file.f
$ terraform state list
local_file.f

$ terraform state mv local_file.f local_file.f_renamed
Move "local_file.f" to "local_file.f_renamed"
Successfully moved 1 object(s).

$ terraform plan -input=false                          # NOW the plan shows churn
Plan: 2 to add, 0 to change, 1 to destroy.
```

Why did the plan churn after a rename? State says `local_file.f_renamed` owns the file, config says `local_file.f` — so the plan wants to create `f` fresh and destroy the object state still tracks under the old address. Reverting the mv returns to a clean plan:

```bash
$ terraform state mv local_file.f_renamed local_file.f
Move "local_file.f_renamed" to "local_file.f"
Successfully moved 1 object(s).

$ terraform state pull | jq '.resources[].type'
"local_file"
```

`state pull` gives raw bytes — piping through `jq` is the normal way to audit. The orphan test — `state rm` drops an entry without touching the world:

```bash
$ terraform state rm local_file.f
Removed local_file.f
Successfully removed 1 resource instance(s).
$ terraform state list
(empty)
```

After the verification, apply/destroy was run again to restore the demo directory for the next session. Lesson reinforced practically: address changes in state cause recreate churn — `mv` is the tool that fixes that, which is exactly why a `moved` block exists at the config level (TF.P1.1).

### 6. Incident — plan against a modified/foreign state file

Scenario: someone hand-edited `terraform.tfstate` or a stale state got committed. Run plan:

```bash
$ terraform plan
Error: Error refreshing state: ... state file could not be read ...
```

and the second classic — a lock that was never released:

```bash
Error acquiring the state lock: ConditionalCheckFailedException ...
Lock Info:
  ID:        <lock-id>
  Operation: OperationTypeApply
  Who:       someone@laptop
  Created:   timestamp
```

Do not `force-unlock` blindly — check the lock ID against who/what holds it (typically a stuck CI job or a crashed apply). Confirm no apply is legitimately in-flight, then force-unlock. This is why remote backends give you operations teams: they see locks and can query them.

### 7. Quick-reference one-liners

- `state list` — what's tracked
- `state show <addr>` — one resource's attributes
- `state mv <a> <b>` — re-address without rebuilding the world
- `state rm <addr>` — forget (orphan) an object
- `state pull` — dump raw state (audit, backup)
- `state push` — overwrite state (nuclear, avoid)
- `import <addr> <id>` — adopt an existing object, config block required first

### 8. Common pitfalls

- Editing `terraform.tfstate` by hand — corrupts `serial`/`private`, breaks providers — let `mv`/`rm`/`import` do it.
- Importing without the config block — Terraform errors before even reaching the provider.
- Assuming every resource imports — many don't (`local_file` and `random_*` in this env proved it) — always check provider docs.
- Committing `terraform.tfstate` to git with secrets in it.
- `state push` as a "quick fix" — it overwrites unconditionally and can destroy the team's state if the pushed file is stale.
- Ignoring `.backup` files — they are the cheapest rollback you have.

### 9. Interview Q&A

Q: What is inside a state file?
A: Version/serial metadata, recorded outputs, and one entry per resource with its provider-known attributes, dependencies, and provider-private data. For for_each/count resources, multiple instances under one address.

Q: How do you bring an existing unmanaged EC2 instance under Terraform?
A: Add the resource block matching the instance, then `terraform import aws_instance.web i-0abcd1234`. Next plan diffs its actual attributes against config.

Q: What is the difference between `state rm` and destroying?
A: `rm` forgets the object — Terraform stops tracking it, the real object survives. Destroy actually calls the provider's delete and removes it from the world. `rm` creates orphans — destroy creates deletions.

Q: Why did a `state mv` make our next plan show destroys?
A: State addresses and config addresses drifted apart — Terraform saw the new address as never-created and the old address as abandoned. Reverting the mv restored one consistent mapping.

Q: What happens on concurrent apply without a backend lock?
A: Both refresh, both apply, the last state write wins — you can permanently lose other resources from state while the actual objects still exist.

Q: When is `force-unlock` justified?
A: Only when you have confirmed the lock holder's operation is genuinely dead (crashed process, killed CI job). Otherwise you risk a second writer clobbering state mid-write.

### 6.1 State backup files — the cheapest rollback you have

Every state write first copies the previous state to a sibling file. In the demo project's directory these appeared across sessions:

```
terraform.tfstate
terraform.tfstate.backup
terraform.tfstate.<ts>.backup
```

If a plan/apply ever corrupts or empties the main state file, the immediate recovery is: copy the newest `.backup` back over `terraform.tfstate`, then re-run. For teams on remote backends, the equivalent is bucket versioning (TF.P0.3) — a write-versioned history you can restore without waiting on a teammate.

Trap: `.backup` is only one generation deep by default. Do not treat it as an archive — treat it as a pre-write snapshot, and keep a separate real backup habit for anything you care about.

### 6.2 When the serial bites — stale state detection

State carries a monotonically increasing `serial`. Backends use it to refuse writes from an older copy: if you push state that was pulled before a teammate wrote, the backend rejects it rather than silently rolling the clock back. That check is why concurrent-safe flows matter: read the LATEST state right before writing, not a copy you pulled an hour ago.

### 6.3 Import + mv combos — the adoption recipe

Two operations in one story: "we deployed an instance outside Terraform and it is already live — we want it managed." The recipe that works:

```
write config block → terraform import <addr> <id> → plan
```

If the address must change (e.g. move into a module), run `state mv` right after import while the mapping is fresh, then plan. The alternative — deleting and re-creating the config — would destroy a live, healthy resource — the import path never touches the real object.

### 6.4 The state files nobody reads and everybody should

- `terraform.tfstate.backup` — pre-write snapshot (above)
- `.terraform/terraform.tfstate` — the backend's local CACHE of remote state (local copy of what S3/TF Cloud holds), NOT the source of truth
- `errored.tfstate` — appears when an apply dies mid-write — recover via the last good `.backup`

Naming these three in an answer marks you as someone who has actually operated state, not just read about it.

### 6.5 Reading a state show output like an engineer

The `state show` block from P0.1's lab, annotated:

```
resource "local_file" "f" {
    content              = "hi"
    content_md5          = "49f68a5c..."        # provider-computed, derived
    content_sha1         = "c22b5f91..."        # this IS the resource id
    filename             = "/tmp/tfdemo/out.txt"
    id                   = "c22b5f91..."
}
```

The line worth pausing on is `content_sha1` mirroring `id` — the provider defines identity FROM content, which is why the drift plan in TF.P0.5 saw any content change as create-new. When interviewers hand you a `state show` block, hunt for that tell: attributes that the config never set (all the computed hashes), and the id that anchors identity. Being able to narrate "which of these came from config, which from the provider" answers a surprisingly common screen question.

### 6.6 The state command quick-deck (memorize the shape)

```
terraform state list                        → addresses only
terraform state list | grep count           → see count-instance indices
terraform state show type.name              → attributes of one object
terraform state mv <old> <new>              → relocation (TF.P1.1 moved = config-native)
terraform state rm <addr>                   → orphan — forget, don't destroy
terraform state pull                        → raw JSON via stdout
terraform state pull | jq '.resources'      → browse as data
terraform import <addr> <id>                → adopt a live object
```

The two NAMES to keep crisp: `state show` is per-address — `state list` is the summary. Everything else in the deck is either a mutation or an inspection — and mutations belong in a review, not on a terminal you own alone.

### 6.7 Workspace-aware state commands

With workspaces, the same verbs target the CURRENT workspace's state — `workspace show` tells you which, `workspace list` enumerates them. State commands never ask "which workspace" because the answer is "the selected one." That is precisely why a mis-set `TF_WORKSPACE` in CI (TF.P1.2) is so sneaky: every state verb stays silent about which slate it's writing. Mentioning workspace-scoping while discussing state management is a small bonus that registers.

### 9.5 Mock interview drill — the state surgery (5 minutes)

Prompt: "A teammate renamed `aws_instance.web` to `aws_instance.web_v2` in config and the plan now shows a destroy + create. Walk me through the diagnosis and the fix."

Answer skeleton: plan churn after a rename means state still keys the old address while config declares the new one — no real change was intended, so no real churn should exist. Fix: add a `moved { from = ... to = ... }` block (config-native, future-proofs the rename), or run `terraform state mv web web_v2` for the immediate remap, then plan again — now clean. Follow-up: if you had NOT renamed it and the plan still demolished, the answer changes to drift investigation (TF.P0.5), not state surgery.

Pass if the diagnosis names address mismatch and the fix names `moved`/`state mv` — never "just apply and let it recreate."

### 10. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can draw the state file layout (metadata, outputs, resources, instances) | |
| 2 | Has run `state list`, `state show`, `state pull` | |
| 3 | Has moved an address with `state mv` and reverted it | |
| 4 | Can explain why mv-then-plan showed churn | |
| 5 | Can explain `state rm` vs destroy difference | |
| 6 | Knows import requires a config block first | |
| 7 | Knows not all resources support import (verified local_file failure) | |
| 8 | Can explain state locking failure and the correct unlock flow | |
| 9 | Knows why `.backup` state files exist | |
| 10 | Understands sensitive attributes are still stored in plaintext state | |
| 11 | Can audit state via `state pull | jq` | |
| 12 | Can name when to use `mv` vs `rm` vs `import` | |
| 13 | **SELF-VERIFY** — Ran the import/mv/rm/pull sequence in `/tmp/tfdemo`, saw the exact outputs above, destroyed and restored the dir | |

Verdict: PASS when you can repair and audit state without hunting for docs — the only safe way to touch state is through the five commands plus import.

Next session: TF.P0.3 — move that same state to a remote backend and make locking a team feature.

---

## TF.P0.3 — Remote state backends: S3/DynamoDB, team state

One-line focus: why your state must not live on one laptop, and what backend configuration buys you — shared state, locking, and DR.

The interview wants to know you understand the difference between local and remote state flow, can sketch an S3+DynamoDB backend, and know what `init -migrate-state` does. This session is model-only — no cloud was touched, nothing is billed. Everything below is the exact answer format for the interview.

### 1. What a backend is

The backend decides where state lives and how locking works. `local` is the default (a file on disk). Remote backends — `s3`, `azurerm`, `gcs`, `http`, and Terraform Cloud (`cloud` block) — put the state somewhere shared and add a lock.

The "flow" difference in one line each:
- Local flow: read `terraform.tfstate` from disk → plan → write `terraform.tfstate` to disk. Single user, no lock, last-writer-wins.
- Remote flow: acquire lock (DynamoDB for S3 backend) → pull state object → plan/apply → write state object back under the new serial → release lock. Every teammate shares the same object.

### 2. The standard S3 backend — what each part is for

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state-bucket"
    key            = "prod/network/terraform.tfstate"
    region         = "us-west-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

- `bucket` + `key` — where the state object lives (key is the per-workspace path inside one bucket).
- `encrypt = true` — SSE on the state object itself.
- `dynamodb_table` — the lock table. Before writing, the backend does a conditional DynamoDB PutItem — a concurrent writer fails the condition (ConditionalCheckFailed). That is the lock.
- Versioning the bucket — every state rewrite becomes a versioned object, giving state-level rollback.

Mental model: S3 is the state warehouse, DynamoDB is the checkout desk — you check out the right to write, write, check back in.

### 3. Why remote state (the three reasons interviewers want)

1. **Collaboration** — all teammates (and CI) converge on one state object — your plan sees the infra everyone applied, not just yours.
2. **Locking** — concurrent applys fail fast instead of silently clobbering.
3. **DR/audit** — state survives laptop loss — bucket versioning gives point-in-time recovery — object access is auditable via IAM.

Trap: remote state means your CI credentials become state-writers. Lock down the bucket with a dedicated role, never shared keys.

### 4. The migration mechanics

`terraform init -migrate-state` is the bridge: it reads the current local state and copies it into the newly configured backend — one-time, interactive prompt to confirm. Also relevant:

- `-reconfigure` — re-init a backend with new config without touching state contents (used when credentials/region changed but not the backend itself).
- Init detects backend changes automatically — after editing a `backend "s3"` block you MUST re-run init, or Terraform refuses with "Backend configuration changed."

The interview expects: init is idempotent, re-run freely — migrate is for moving state around — reconfigure is for re-connecting to the same backend with new settings.

### 5. Backend comparison — have this table cold

| Backend | Who uses it | Locking | Notes |
|---|---|---|---|
| local | single user, demo | none | default — last-writer-wins |
| s3 | most orgs starting remote | DynamoDB option | needs the lock table explicitly |
| azurerm / gcs | Azure / GCP shops | native (in-service) | built-in |
| http | custom/pull-based | optional REST lock API | minimal |
| terraform cloud | managed teams / free tier | built-in | plan logs + remote runs too |

Interview angle: the choice is often "which lock story do I prefer" plus "does my ORG want to host the backend or buy it managed."

### 6. Terraform Cloud — managed, not just state

Terraform Cloud (and the `cloud` block replacing the old `remote` backend) does more than store state: it can run plan/apply in its own runners, store both plan artifacts and run logs, attach run triggers, and gate applies with policy (Sentinel/OPA). Locally you still get the same locking and shared-state benefits. For a 1–3 YOE interview, the sufficient answer: "TF Cloud is HashiCorp-managed — shared state, locking, remote runs, run history — Atlantis is self-hosted on your infra — Spacelift is a third-party managed layer" (full comparison in TF.P2.2).

### 7. Locking contract — what the backend promises

- Any run that mutates state (plan that could write the state version, apply, destroy) must hold the lock.
- Read-only plan/refresh still hits the backend to FETCH state but does not need the write lock.
- Lock is held across the whole apply, so a slow apply blocks others legitimately — that is why the error message prints lock metadata (ID, operation, who, created) so you can decide whether force-unlock is safe.

### 8. Common pitfalls

- Forgetting `dynamodb_table` — you get shared state but NO locking, silently reverting to race conditions.
- `backend` block with hardcoded bucket+key but no IAM for CI.
- Not running `init -reconfigure` after backend credential/config change.
- Passing secrets into the backend block via `-backend-config` instead of env vars.
- Leaving state unencrypted at rest in buckets copied from examples.
- Migrating state to the wrong backend and then running plan from an old shell with the local-file working dir cache.

### 9. Interview Q&A

Q: Why can't you just use a git repo for state?
A: Git has no locking and no read-then-write atomicity — two CI jobs can both read, both apply, both push, and the outcome depends on commit order. A backend with locking serializes writers.

Q: How does S3 backend locking actually work?
A: Terraform writes a lock record into a DynamoDB table with a conditional insert — only one writer can hold it — subsequent writers hit ConditionalCheckFailed and error out with lock details. State itself is a versioned S3 object.

Q: What does `terraform init -migrate-state` do?
A: Copies existing state from the previously configured backend into the newly declared one, keeping `serial` and content intact, after a confirmation prompt.

Q: What's the difference between `-migrate-state` and `-reconfigure`?
A: Migration moves state contents between backends — reconfigure just re-runs backend setup with new configuration for the same backend location.

Q: Can you use `http` backend for a real team?
A: Yes — it reads/writes state via REST and supports optional state locking through a second REST contract. It's your low-level escape hatch, but you then own the server.

Q: Any downside to Terraform Cloud?
A: It's a managed dependency — your apply path leaves your network, and beyond the free tier it costs money. That tradeoff is exactly why some orgs self-host Atlantis instead.

### 6.1 The workspace — backend's twin concept

Remote backends almost always pair with workspaces: each environment (dev/staging/prod) gets its own state key inside the SAME backend. `terraform workspace list/new/select` switch between them. The S3 backend maps one workspace to one `key` value — `terraform workspace show` tells you which state you are about to touch. In CI you set `TF_WORKSPACE=<env>` so a merge to main frames the exact environment leg.

Trap: with a shared backend bucket, a misconfigured `TF_WORKSPACE` points the apply at the WRONG environment's state. The guardrail is per-workspace IAM policy on the bucket prefix — the "state bucket as an access control surface" pattern.

### 6.2 Backend config vs backend code — where secrets live

`backend "s3"` blocks in config can only use static values and never variables. Real deployments pass the mutable bits at init time:

```bash
terraform init -backend-config="bucket=${STATE_BUCKET}" \
               -backend-config="key=envs/${TF_WORKSPACE}/state.tfstate"
```

That is the sanctioned way to vary bucket/key per environment — and it keeps the literal bucket name out of committed config. Secrets like credentials never go here either — they come from provider auth (OIDC roles, env vars), not the backend block.

### 6.3 Chosen backend changes every command's feel

- Local: everything reads/writes one file — the `.terraform` cache holds the backend config
- S3 remote: every plan/apply prints `Acquiring state lock` / `Releasing state lock` — the lock table is inspectable (`aws dynamodb get-item`) and the failure messages surface lock metadata
- `http`/custom: your own server implements GET/PUT/lock endpoints — smallest team value, biggest integration surface

Interview line: "moving from local to remote changes WHO can safely write, not WHAT writing means."

### 6.4 The state-lock debugging session

When a lock error hits:

```
Error: Error acquiring the state lock
Error message: ConditionalCheckFailedException
```

Worked example of the correct drill: read the Lock Info (ID, Operation, Who, Created) → check that runner/job against active processes or CI → if dead, `terraform force-unlock <lock-id>` → verify a fresh plan reads clean. Never force-unlock a LIVE apply — you'd be unlocking a door someone is walking through.

### 6.5 Other backends — the survey a candidate should know

- `azurerm` — state is a blob in Azure Storage with native blob leases for locking — favorites of Azure shops, zero extra services to assemble.
- `gcs` — Google Cloud Storage object with a lock via the storage API — same idea, different provider.
- `http` — the bare REST contract: GET/PUT state against a URL you host, with optional state lock endpoints. Exists for exotic setups — you own the server and the availability.
- `consul` / `etcd` — KV-store-backed state (historic, mostly superseded by the three above).
- `local` — the default — zero infrastructure, zero safety (see the entire session).

The safe senior move: pick by "what lock story does the platform give me for free" and "who am I allowed to make host this." One more sentence on `terraform cloud`: it moves BOTH the state and the runner, which changes who has IAM feet — covered in TF.P2.2's decision axes.

### 6.6 Remote state + drift — a subtle interaction

Because refresh reads from the REMOTE object each run, remote state makes drift detection a TEAM property: your plan sees the reality after everyone's applys, not just yours. That is a feature, and it deepens the earlier drift point (TF.P0.5) — a teammate's out-of-band console change surfaces in YOUR repo's plan. The pipeline fix (TF.P1.2) is a drift-check leg that turns that shared visibility into a guaranteed green.

### 6.7 The backend-selection interview answer, scripted

"Yours," in 40 seconds:

"The backend is where state lives, and its lock story is the whole safety margin. For a small team I go S3 + DynamoDB because it is the cheapest shared consensus — the bucket stores the state object, versioning gives me rollback, and the DynamoDB table serializes writers via a conditional insert — the init migration path (`-migrate-state`) pulls our existing local state in with zero loss. If the org already owns Azure Storage or GCS, their native leases cost fewer moving parts. If they want zero self-hosted infra, Terraform Cloud absorbs state and runner — if they want everything controlled, Atlantis keeps state in my S3 and only the orchestration is self-hosted (TF.P2.2). The constant across every choice: lock-before-write, serialize writers, and never let a stale `serial` clobber a fresh one."

That script contains: bucket, key, encode, dynamodb, versioning, migration, serial, azure/gcs alternative, and the TF Cloud/Atlantis tie-in. It answers the default "where does your state live and why" with substance.

### 6.8 Commands that talk differently to a remote backend

- `terraform init -migrate-state` — surgically move state INTO the backend
- `terraform init -reconfigure` — rebind a backend with new config, no state traffic
- `terraform state pull` — fetch the remote object to stdout (local cache is `.terraform/terraform.tfstate`)
- `terraform state push` — push stdin back (dangerous: bypasses lock, used for disaster recovery)
- `terraform force-unlock <id>` — clear a stale lock record
- `terraform workspace list` — enumerate the per-env state keys

The pattern: everything that READS state goes through the backend path — everything that WRITES state must hold the lock. Saying "pull is read, push is write, and write must be locked" compresses this whole session's safety model into one line.

### 9.5 Mock interview drill — spec the backend (5 minutes)

Prompt: "Six engineers, one prod account, two environments. Design their state strategy and explain one thing that goes wrong without it."

Answer skeleton: one S3 bucket with `key` per env per service, `dynamodb_table` for locking, versioned bucket, `encrypt`, per-prefix IAM so dev cannot write prod state, `init -migrate-state` when the old local file comes in. Then the failure mode: without the DynamoDB lock, two `apply`s race — last writer's state wins and some prod resources vanish from state while staying alive in the cloud. Name THAT sentence and the interview round is won.

Pass if the design includes a lock table and at least one failure mode without it.

### 10. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can define "backend" in one sentence | |
| 2 | Can sketch S3 bucket + key + dynamodb_table and say what each does | |
| 3 | Knows DynamoDB table existence is required for locking with S3 backend | |
| 4 | Can state the 3 reasons for remote state (collab/lock/DR) | |
| 5 | Knows `-migrate-state` moves state, `-reconfigure` reconnects | |
| 6 | Can explain the lock error surface (ConditionalCheckFailed, maybe winner) | |
| 7 | Knows versioned buckets give state rollback | |
| 8 | Can compare local/s3/azurerm/http/TF Cloud locking in one line each | |
| 9 | Knows init must be re-run after backend changes | |
| 10 | Understands CI credentials become state-writers and need scoped IAM | |
| 11 | Can describe the remote flow: lock → pull → plan/apply → write → unlock | |
| 12 | Knows read-only plan/refresh does not need the write lock | |
| 13 | **SELF-VERIFY** — Re-wrote a backend "s3" block from memory, explained migrate vs reconfigure to out loud, no cloud touched | |

Verdict: PASS when you can spec a backend for a fictional 6-person team including the lock table, IAM boundary, and rollback story without prompting.

Next session: TF.P0.4 — the flags that bend plan/apply to your will on a bad day.

---

## TF.P0.4 — Plan/apply flags: target, var, refresh, parallelism

One-line focus: know the seven flags interviewers name-drop, when each is legitimately used, and which one signs your termination letter if you make it a habit.

The interview wants to know you reach for the right flag in the right crisis: `-target` for surgical repair (not routine use), `-replace` to force recreation, `-refresh=false` for speed when the API is slow or broken, `-var`/`-var-file` for input, `-out` to pin an apply to a reviewed plan, `-parallelism` to control blast radius. Plus the hygiene commands `fmt`/`validate` and the REPL `console`.

### 1. The reference table — memorize it

| Flag | What it does | Use it when | Not for |
|---|---|---|---|
| `-target=type.name` | limit plan/apply to one node + deps | healing one broken resource after a partial failure | everyday changes |
| `-var 'k=v'` | set a single variable | quick one-off run | secrets (use -var-file/env) |
| `-var-file=prod.tfvars` | variable file | stable environments, CI promotion | — |
| `-out=tf.plan` | save a binary plan | PR gating, "apply exactly this" | — |
| `-replace=type.name` | mark one resource for recreation | a resource drifted into a bad state | — |
| `-refresh=false` | skip live refresh | speed, API outage for read-only objects | any apply relying on fresh state |
| `-parallelism=N` | max concurrent resource operations | rate limits, quota pressure | — |
| `-auto-approve` | skip confirm prompt | scripts/CI (plan already reviewed) | hot loops on prod |
| `-destroy` | plan for destroy | delete planning | — |

Trap: `-target` does not mean "only this resource will be affected" — dependencies are pulled in, so a targeted apply can still touch a whole tree.

### 2. -target — the story interviewers check

The tool itself prints the policy line — verified live:

```bash
$ terraform plan -target=local_file.f2 -input=false
... 
Warning: Resource targeting is in effect

You are creating a plan with the -target option, which means that the
result of this plan may not represent all of the changes requested by the
current configuration.

The -target option is not for routine use, and is provided only for
exceptional situations such as recovering from errors or mistakes, or when
Terraform specifically suggests to use it as part of an error message.
```

That warning is the whole answer: targeting exists for error recovery and surgical healing, and you should say "my team uses -target when an apply partially fails and we're converging the one broken object" — never "we -target everything because it's fast."

### 3. -replace — force, don't pray

When a resource is operationally broken (a corrupt instance that persists despite the config being correct), `-replace` tells the graph to destroy + recreate that specific resource:

```bash
$ terraform apply -auto-approve -input=false -replace=local_file.f
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

Read that result: exactly one recreation, everything else untouched — the precise tool for a dead object. Same idea exists in plan phase for pre-approval review.

### 4. -refresh=false — the speed/trust tradeoff

Default plan refreshes everything: it asks each provider for the real current state. Two legitimate uses:
1. The API is down/slow and you only want a config-diff sanity check.
2. You are iterating on a tiny module where renewal is pure latency.

Verified behavior — with trustworthy state it reports no changes:

```bash
$ terraform plan -refresh=false -input=false
No changes. Your infrastructure matches the configuration.
```

Trap: skipping refresh means the plan can be built on stale facts — drift it never sees becomes drift it cannot report. Do not skip refresh before destructive decisions.

### 5. -out and -var — make apply reproducible

`-out=tf.plan` serializes the reviewed plan — `terraform show tf.plan` renders it back or prints the saved action summary. Only this artifact can be applied by a second person/CI with exact fidelity — this is the backbone of PR-gated workflows (TF.P1.2):

```bash
$ terraform plan -out=tf.plan -input=false
$ terraform show tf.plan     # prints the saved plan incl. "No changes"
```

`-var` and `-var-file` override variables for this run only. Precedence (highest wins): `-var`/`-var-file` flags → env `TF_VAR_x` → `terraform.tfvars` file → defaults. Keep the same `tfvars` file for a given environment and your promotion path becomes "the same vars, different environment."

### 6. -parallelism and hygiene

`-parallelism` caps how many resource operations run simultaneously — the lever for provider-side rate limits and quota pressure (default 10). Bring it down when the provider starts spamming 429s — know that lowering it slows big applies.

`terraform fmt` normalizes HCL so diffs in PRs stay meaningful — `fmt -check` fails in CI if the file is not formatted. `terraform validate` statically checks the config (needs providers initialized). Both verified:

```bash
$ terraform fmt -check main.tf && echo "FORMATTED OK"
FORMATTED OK
$ terraform validate
Success! The configuration is valid.
```

### 7. terraform console — the REPL

Read-only interactive shell over the loaded config + state. Great for validating expressions before putting them in code. Verified:

```bash
$ echo 'local_file.f.filename' | terraform console
"/tmp/tfdemo/out.txt"
$ echo '1 + 1' | terraform console
2
```

(Full treatment in TF.P1.3 — here it just sits in the flag/hygiene arsenal since no state mutation is involved.)

### 8. Common pitfalls

- `-target` in the standard promotion path — state/config drift multiplies, and later full applies surprise everyone.
- `-refresh=false` on an apply that then destroys something the world already changed.
- Applying an ad-hoc plan because you forgot `-out` — the diff you reviewed is gone.
- Putting secrets on the `-var 'password=...'` command line — visible in process listings and shell history.
- Forgetting `-parallelism` exists entirely until a 429 storm.
- `fmt` never in the pre-commit flow, so every PR mixes formatting churn with real changes.

### 9. Interview Q&A

Q: When should you use -target?
A: Recovery from a partial apply or when Terraform itself suggests it in an error — not for routine work. Its whole purpose is surgical convergence of one object, and the plan output carries an explicit warning about that.

Q: What does -replace do that a normal apply won't?
A: It forces destroy-and-recreate for a named resource even when the diff says no-change — used when an object is healthy in state but broken in reality (corrupt instance, bad chassis).

Q: When is -refresh=false safe?
A: When you trust state enough for the decision at hand and want speed — never as the default, and never when the run may destroy.

Q: What does `terraform show tf.plan` give you?
A: The rendering of a saved plan artifact — the exact actions a binary plan file locks in, useful in CI review.

Q: How do you pass variables in CI?
A: `-var-file=env.tfvars` committed (non-secret values) plus secrets as environment variables (`TF_VAR_db_password`) or a secrets backend — never `-var 'secret=...'` inline.

### 6.1 The -out + apply contract in detail

The binary plan file is the only honest handoff between two steps:

```bash
$ terraform plan -out=tf.plan -input=false          # step one: produce
$ terraform apply tf.plan -auto-approve -input=false  # step two: consume exactly that
```

`terraform show tf.plan` renders the same artifact for humans (works in CI where the plan file was uploaded). The contract interviewers want stated: **apply-from-artifact applies the reviewed diff — apply-without-artifact re-plans and can drift from what was reviewed.**

Holding this distinction is the difference between a demo and a delivery pipeline (TF.P1.2 fleshes out the CI side).

### 6.2 A real flag stack for a production-style run

A run that combines several levers correctly looks like:

```bash
$ terraform apply -var-file=envs/prod.tfvars -parallelism=5 \
    -out=tf.plan -input=false \
    && terraform apply tf.plan
```

Read each lever: stable inputs (`-var-file`), throttled concurrency (`-parallelism=5` for quota-tight providers), deterministic apply (`-out` + consume), no interactive prompts in automation (`-input=false`). Naming why each flag is there — not just listing them — is the 1–3 YOE differentiator.

### 6.3 -replace vs editing state — the anti-pattern

A broken resource tempts people to `state rm` + apply (which then recreates — effectively a replace) or worse, to hand-edit state. Both are slower, more dangerous versions of `-replace=type.name`. The flag is precisely scoped: one resource recreated, nothing else touched, and the plan output is reviewable. Always prefer the flag over the workaround.

### 6.4 What -parallelism does NOT do

It limits concurrent RESOURCE operations per run — not per API call, not total plan speed, not batches across workspaces. Downgrading it to 1 serializes everything (safe, slow). Interviewers probe this to see if you know it is a throttle, not a scheduler.

### 6.5 fmt and validate as code-hygiene pair

`fmt` makes HCL canonical (and `fmt -check` fails CI on non-canonical files) — `validate` catches structural errors before anything touches a provider. Run `validate` in the same job that runs `init`, `fmt -check` in the same job that runs tests — the cheapest possible feedback loop before plan. Both were verified in the lab transcript above (FORMATTED OK / configuration is valid).

### 6.6 Flag scenarios — cold readouts

- "Odd refresh timeouts in prod plan" → `-refresh=false` once for the hot conflict, `-parallelism` reduced, then root-cause the provider. Never both silently.
- "One instance is broken but the rest are fine" → `-replace=aws_instance.web` for the specific instance, and read the plan to confirm only it is recreated.
- "A known-breaking change is in the next deploy" → `plan -out=tf.plan`, review, `apply tf.plan` — shape-stable, then rollback = apply the reverse diff.
- "Secrets must not appear in plan output" → prefer data sources tied to stores (`aws_ssm_parameter`) and `-var-file` for the rest — `can("sensitive")` markers the module's outputs.

### 6.7 -refresh-only — the flag that replaced the old drift check

`-refresh-only` produces a plan that ONLY refreshes state — it reads reality, updates the recorded attributes if they differ, and proposes NO mutations:

```bash
$ terraform plan -refresh-only -detailed-exitcode
# exit 0 = matches config; exit 2 = reality differs from state (drift)
```

This is the modern drift detector (used in the TF.P1.2 nightly check) and it is the flag to name when someone asks for "a plan that just reports reality." `-detailed-exitcode` (`0`/`2`/`1`) turns the output into a CI-controllable signal. Two flags, one sentence: "refresh-only reports drift — detailed-exitcode makes it a gate." Distinguishing refresh-only from apply-plan is a clean senior tell.

### 9.5 Mock interview drill — the incident runbook (5 minutes)

Prompt: "A daily plan job in prod takes 15 minutes and yesterday API outages caused it to timeout before finishing. Your teammate disabled refresh to skip the timeout. Is that correct? What else would you do?"

Answer: disabling refresh is a legitimate emergency shortcut, but it is NOT a fix — it trades latency for blind spots (the plan can no longer see outside mutations). The healthy follow-up: (1) add `-target` recovery for the broken leg after identifying which node was failing (2) request a read-only endpoint or wider rate limit with the provider (3) adjust CI timeout to fit the actual API-call budget. Then, critically, run a full normal plan after the fires are out. Name that last step and you stand out.

Pass when the answer condemns hiding refresh as a permanent default, names -target as the immediate emergency tool, and restores refresh once the incident is resolved.

### 9.5 Mock interview drill — the flag parade (5 minutes)

Prompt: "Your daily prod plan is slow. List the levers, and say which one is NOT acceptable as a permanent answer."

Answer: (1) `-parallelism` down/up to balance API load — (2) scope the plan with `-target` only for incident recovery, never daily — (3) `-refresh=false` — the tempting lever for speed, NOT acceptable permanently because it blinds drift detection — (4) `-out` so the scoped plan is storable/auditable — (5) the real fix of rate-limit/API-budget. The interview zinger: name `-refresh=false` as the "temporary crutch" and you pivot correctly.

Pass when `-refresh=false` is the flagged crutch, not a recommendation.

### 10. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can state the safety rule for -target from memory | |
| 2 | Has run a -target plan and read the targeting warning | |
| 3 | Can explain -replace with a real use case | |
| 4 | Knows -refresh=false risks (stale facts → surprise destroys) | |
| 5 | Has used -out + `terraform show` to pin a plan | |
| 6 | Knows var precedence order | |
| 7 | Knows why secrets must not ride -var flags | |
| 8 | Can say what -parallelism controls and when to lower it | |
| 9 | Has run fmt/validate and can sell them for CI | |
| 10 | Uses console to pre-test expressions | |
| 11 | Knows -auto-approve belongs in CI, not tty hot loops | |
| 12 | Can combine -target + -replace to heal one broken resource | |
| 13 | **SELF-VERIFY** — Ran -target, -refresh=false, -replace, -out, fmt, validate, console in /tmp/tfdemo — outputs above match reality — dir restored | |

Verdict: PASS when you can pick the flag for the emergency told in the question — recovery (-target/-replace), speed (-refresh=false/-parallelism), or reviewability (-out/-var-file).

Next session: TF.P0.5 — the moment reality sneaks out from under Terraform: drift.

---

## TF.P0.5 — Drift detection + failure set + partial apply

One-line focus: drift is the difference between the world and what Terraform last recorded — know how plan exposes it, how to reconcile it, and how a partial apply fails and heals.

The interview wants to know plan is your drift radar, that reconciliation comes in two flavors (in-place update vs destroy/recreate), and that a mid-apply failure leaves a half-converged state that you heal with a targeted apply. This session was run live: modify the file out from under Terraform, watch plan detect it, converge it back.

### 1. Drift — define it precisely

Drift is any difference between real infrastructure and what `terraform.tfstate` recorded. Sources: console edits, out-of-band scripts, someone else's manual change, a provider API doing its own thing. Plan detects drift because its refresh phase re-reads reality — anything that changed shows up as a diff even when the config is unchanged.

Key insight: plan diffs CONFIG against STATE against REALITY. No config change is required for plan to scream.

### 2. Two reconciliation flavors

- **In-place update** — same object, attributes rewritten (e.g., a tag changed). Shown as `~ type.name: tag will be updated`. Least destructive.
- **Destroy + recreate** — the object could not be mutated, so it is replaced (e.g., a filename change that is a key by which the resource is identified). Shown as `-/+ type.name (new resource required)` or separate destroy/create lines.

The local provider makes this dramatically visible: `local_file` derives its `id` from the content hash, so touching the file's content changes the id, and Terraform reads it as "the tracked object is gone, a brand-new one must be created" — a whole-resource replacement. Zero config changes — pure drift.

### 3. Live drift lab on /tmp/tfdemo

Start from a converged state (apply with both `local_file.f` and the demo second file present), then edit the file by hand — the manual console change that Terraform never saw:

```bash
$ echo "externally modified" > /tmp/tfdemo/out.txt
$ terraform plan -input=false
local_file.f2: Refreshing state... [id=d0941e68da8f38151ff86a61fc59f7c5cf9fcaa2]
local_file.f: Refreshing state... [id=c22b5f9178342609428d6f51b2c5af4c0bde6a42]

Terraform will perform the following actions:

  # local_file.f will be created
  + resource "local_file" "f" {
      + content              = "hi"
      ...
      + filename             = "/tmp/tfdemo/out.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Read that output: Terraform never proposes an in-place text fix for `local_file` — the content hash drives the identity, so the drifted object reads as "must be created fresh." The plan flags it regardless of who touched the file. Then converge — apply restores the file from config:

```bash
$ terraform apply -auto-approve -input=false
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

$ cat /tmp/tfdemo/out.txt
hi
```

That is the whole drift lifecycle: detect (plan), converge (apply). The file is back to the config-declared content, state matches again.

### 4. Reconciling drift — the decision tree

1. Is the change something Terraform should own? If yes, apply — the config wins, world converges to config.
2. Should the drifted object instead be adopted as-is? Import it (TF.P0.2) so state matches reality and config can evolve.
3. Should the resource be forgotten entirely? `state rm`.
4. Keep the manual change forever? Then encode it in config (or `ignore_changes`, TF.P1.1).

Trap: apply ALWAYS converges to config — it will happily overwrite a genuine manual fix someone applied for an outage. Check what drifted and why before running apply.

### 5. Failure set — how applies actually break

The four classic failure families and the correct reaction:

1. **API errors** — provider call failed (timeout, 5xx). Transient: retry. Persistent: the provider config/creds are wrong.
2. **Missing dependencies** — a resource references something that does not exist (a deleted subnet). Plan may pass locally but apply fails because the world is different from refresh data.
3. **Quota/limit** — cloud account at capacity ("limit exceeded"). Fix upstream, then re-apply — this is where `-parallelism=1`-style throttling or spreading workspaces helps.
4. **Dependency cycles** — config where A needs B and B needs A (mutual references). Terraform refuses to plan until you break the cycle (move one side into a data source or a separate resource).

The universal reaction: read the failing resource address, fix the CAUSE, then `apply -target=<resource>` to resume converging from the failure point instead of re-running the whole batch.

### 6. Partial apply — what it is, how to heal it

An apply fails halfway — some resources created, some not, state written for the successes. This is NOT corruption — it is a partial convergence. You heal it by re-applying (Terraform resumes where it left off, using refreshed state) or by targeting:

```bash
$ terraform apply -target=local_file.f -auto-approve -input=false
```

Target the one broken node to limit blast radius, confirm the object, then run a full plan to make sure nothing else crept in. The incident framing: "a deploy dropped a resource mid-apply, I re-converged with a targeted apply, then validated the full plan was empty."

### 7. Common pitfalls

- Panicking at plan noise and "fixing" drift by hand instead of deciding who owns the object.
- Applying over a manual outage fix without investigating — Terraform will delete it with glee.
- Treating every drift as destroy+recreate — many are cheap in-place updates — read the plan line.
- Ship of Theseus: drifting forever via -target rather than one clean full apply.
- Not knowing whether the resource identity is content-hash based (like local_file) — that changes how you read every plan.

### 8. Interview Q&A

Q: How does Terraform detect drift?
A: Plan's refresh phase calls each provider's read and compares the result with state — mismatches surface as proposed actions even when config is unchanged.

Q: Why did our plan say a file would be "created" when only its contents changed?
A: Because for `local_file`, the id is derived from the content hash — a content change looks like a new object to Terraform, so it plans create-new rather than in-place update. Identity semantics are resource-specific.

Q: Someone changed a security group in the console. What do you do?
A: Plan first. If the diff is exactly the console change, apply to converge config. If the manual change is what we actually want, put it in config (or import) so state and config agree.

Q: Apply failed halfway. What now?
A: Read the failing resource, fix the root cause (quota/API/dependency), and resume with a targeted apply for that resource, then a full plan to confirm a clean state.

Q: In-place update vs destroy/recreate — how do you know which applies?
A: The plan shows `~` for in-place, `-/+` for replacement, separate `-`/`+` lines for recreate. Destroy+recreate happens when a key attribute (like a filename or instance id) cannot be mutated.

### 6.1 The reconcile matrix — four classic drift cases

| You see in plan | Likely cause | Right reaction |
|---|---|---|
| `~` in-place change, attribute you don't recognize | external tool rewrote a mutable field | inspect, then apply (converge) if harmless |
| `-/+` replacement of one resource | key attribute changed (id/name/content-hash) | apply — the object cannot be mutated |
| `+` create for something you never edited | config duplicates what a data source fetches, or state drifted to orphan | trace the dependency, import or apply |
| `-` destroy of an unexpected resource | config removed the block, or address drifted (state mv, moved) | confirm BEFORE apply, or re-add config |

Confidence in reading a drift plan comes from running it against something you can inspect — this lab's whole point. The demo's drift output was exactly the `+` create row for `local_file.f` after a manual content edit changed its identity hash.

### 6.2 The failure set in richer detail — each arc

1. **API error** — `Error: error reading ...: could not describe ... ` transient blip vs misconfigured provider. Distinguish by repeating the operation: succeeds on retry = transient — fails identically = config/credential problem.
2. **Missing dependency** — plan passes because refresh data lags, apply fails because the subnet/id referenced does not exist anymore. Fix outside Terraform, or import the surviving object, then re-apply.
3. **Quota** — `LimitExceeded`/`limit exceeded` usages. Options: request the quota increase, spread state/workspaces, or throttle with `-parallelism` while the account catches up.
4. **Dependency cycle** — plan refuses with `Cycle: resource A depends on resource B`. Break by extracting one side into a data source (read, rather than manage) or splitting the module boundary.

Each arc ends the same way: fix the CAUSE, not the plan output — then resume with a full run or a targeted converge.

### 6.3 Partial apply, deeper

A failed apply's state is *correct* in a specific sense: it records what succeeded up to the failure point. That is why "re-run" works at all. The danger is half-a-dozen partial fails building up un-applied config in state — the state says "I own X" while X never completed. The reliable healing loop:

```
1. read the failing resource's error
2. fix the root cause
3. apply -target=<that resource>    # limit blast radius
4. full plan → assert empty/expected → done
```

Step 4 is the one most people skip, and it is the one that catches whatever the targeted run was too narrow to see.

### 6.4 Testing your own drift instinct

The fastest way to internalize drift is a 60-second habit: after any manual change to anything Terraform manages, run plan. The plan either shows nothing (no drift) or names exactly what the world did — that readout IS the drift detector. Teams that treat "run plan" as a reflex have boring incident reviews.

### 6.5 A failure transcript worth recognizing on sight

The most common mid-apply death in the local lab world (and a shape that repeats universally):

```
Error: Unable to create resource: api returned an error
  with resource "ignored_things"[k="key"],
  ...
  on main.tf line 20, in resource "ignored_things":
```

Two reads that mark seniority: (1) the error names the ADDRESS, so the correct move is `apply -target=<that address>` — not a blanket re-run, and not a delete. (2) The phrase "resource ignored_things" plus line number is an invitation to open the config, confirm the dependency really exists, and diagnose — rather than guess. Repeat this interpretation drill twice and the on-pager behavior becomes automatic.

### 6.6 The drift-to-failure escalation ladder

1. Cold: an API outage causes plan refresh to hang — run with `-refresh=false` for the emergency leg (TF.P0.4)
2. Warm: plan shows a diff nobody made — investigate who owns the object, then decide converge/import/rm
3. Hot: apply fails MID-write leaving a half-state — target the broken resource, converge, full plan
4. Critical: state itself diverges (hand-edited, lock lost) — restore from `.backup` or the versioned backend copy (TF.P0.2/0.3)

Each rung maps to a concrete tool named earlier in this file. Being able to assign the right tool to the right temperature is the drift portion of the interview, finished.

### 6.7 A drift plan — the annotated transcript

The plan from this lab's drift test, with every line explained:

```
local_file.f2: Refreshing state... [id=d0941e68da8f38151ff86a61fc59f7c5cf9fcaa2]
# refresh phase: provider read for f2, id unchanged — no drift on f2

local_file.f: Refreshing state... [id=c22b5f9178342609428d6f51b2c5af4c0bde6a42]
# refresh phase for f: the id (sha1 of desired content) now differs from
# the file on disk ("externally modified" ≠ "hi"), so the read shows a gap

  + resource "local_file" "f" {
      + content              = "hi"
      ...
      + filename             = "/tmp/tfdemo/out.txt"
    }

Plan: 1 to add, 0 to change, 0 to destroy.
# "1 to add" not "1 to change" because the id drift made Terraform see
# the tracked object as gone and the desired object as brand new.
```

Read the plan backwards: the `+` create exists because the config identity no longer matches state — applying restores the original content and id, and state reconciles. The lesson to memorize: id-based resources (like local_file) look like create-new under drift even when the file is the same path with different content.

### 9.5 Mock interview drill — drift as a process (5 minutes)

Prompt: "Your CI pipeline applies a feature change and the post-apply plan shows no drift. Two days later, a dev fixes something in the console. What happens next?"

Answer sequence: (1) the nightly drift plan (TF.P1.2) catches it and fails. (2) Read the plan: it shows the console change as a mutation of the state-tracked object. (3) Decide: is the fix correct? If yes, encode it in config and apply so Terraform re-owns the change. If no, revert the console change. (4) If you CONVERGE, verify the follow-up plan is clean — and ask yourself if `prevent_destroy` (TF.P1.1) belongs on this resource to prevent the console-fix habit from happening again. (5) File the root-cause ticket: human-managed console changes = unstable footing.

Pass when the answer includes encode-in-config before the next apply, not just "apply and hope."

### 10. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can define drift in one sentence (real vs state) | |
| 2 | Knows plan's refresh phase is the drift detector | |
| 3 | Has induced drift by hand and detected it with plan | |
| 4 | Has converged drift back with apply | |
| 5 | Can distinguish in-place update vs destroy+recreate plan lines | |
| 6 | Knows why local_file content edits plan as create | |
| 7 | Can run the drift decision tree (apply/import/rm/encode) | |
| 8 | Can name the 4 failure families and reactions | |
| 9 | Knows partial apply is healable, not corrupt | |
| 10 | Has used -target to heal one resource after a failure | |
| 11 | Knows to investigate drift before applying over it | |
| 12 | Can narrate the full detect→decide→converge loop | |
| 13 | **SELF-VERIFY** — Re-ran the drift lab (edit file → plan → apply): outputs matched — demo dir destroyed and restored | |

Verdict: PASS when you can role-play the "someone changed production, what do you do?" scenario confidently — plan, read, decide, converge, verify.

Next session: TF.P0.6 — the three ways to say "many resources," and the trap that recycles your infrastructure when the list shrinks.

---

## TF.P0.6 — count vs for_each vs for, dynamic blocks

One-line focus: three ways to multiply resources, and the single biggest gotcha in Terraform interviews — why removing a list item with `count` destroys and recreates things.

The interview wants to know you can pick the right construct by reasoning about identity and stability: repeated resources (`count`), keyed resources (`for_each`), transformed values (`for`). The classic question is verbatim from the brief: "count destroys and recreates when a list item is removed — for_each uses the key." Proven live this session.

### 1. The three tools — what each is for

- `count` — integer metafunction — creates N instances addressed `type.name[0..N-1]`. Identity is the INDEX.
- `for_each` — map/set of strings — creates one instance per KEY, addressed `type.name["key"]`. Identity is the KEY.
- `for` — an EXPRESSION (not a metafunction) that transforms collections — `[for s in var.list : upper(s)]` returns a list, `{for k,v in var.map : k => v}` a map. It is not `for_each` — it is map/flatten wiring inside expressions.

The interview one-liner: "`for` transforms values, `count` and `for_each` create resources — `for_each` where the identity should be stable, `count` where a plain numbered pile is fine."

### 2. The classic trap — removing an item

Positional identity means "the third one" gets recycled. If your list shrinks, every index after the removal re-maps to different items — Terraform destroys + recreates them all, even though their VALUES are unchanged. `for_each` keys stay attached to the same entry regardless of order or count, so removals only affect the exact key removed.

The lab proved it with both constructs side by side. Config:

```hcl
variable "names" {
  type    = list(string)
  default = ["a", "b", "c"]
}

resource "local_file" "by_count" {
  count    = length(var.names)
  content  = var.names[count.index]
  filename = "${path.module}/count_${count.index}.txt"
}

resource "local_file" "by_foreach" {
  for_each = { for n in var.names : n => n }
  content  = each.value
  filename = "${path.module}/fe_${each.key}.txt"
}
```

Apply with `["a","b","c"]` creates 7 files (3 count + 3 for_each + 1 dynamic). Now remove `"b"` — `["a","c"]` — and watch the plan:

```bash
$ sed -i 's/\["a", "b", "c"\]/["a", "c"]/' main.tf
$ terraform plan -input=false
Plan: 2 to add, 0 to change, 4 to destroy.
```

Dissect the 2 adds / 4 destroys:
- `by_count[1]` was "b", becomes "c" — DESTROY + CREATE (index recycled).
- `by_count[2]` ("c") vanishes entirely — DESTROY.
- `fe_b` (for_each keyed "b") — DESTROY (only if key "b" itself goes — `fe_a` and `fe_c` untouched).
- the dynamic list-derived file changes content — DESTROY + CREATE.

After apply the surviving files tell the story:

```bash
$ ls *.txt | sort
count_0.txt
count_1.txt      # was "b", now holds "c" — recycled identity
fe_a.txt
fe_c.txt         # keyed files survive removals of other keys
```

Verbatim lesson for the interview: with `count`, removing `"b"` from the middle of a list recycles every following index (`count_1` gets "c", file rewritten) — with `for_each`, only the removed key dies — `fe_a` and `fe_c` keep their addresses and content forever.

### 3. When to use which

| | count | for_each |
|---|---|---|
| Identity | position (index) | key |
| Remove item | reindexes → destroys/recreates after it | only the removed key dies |
| Access | `count.index` | `each.key` / `each.value` |
| Good for | identical plain instances, N is a number | maps/sets where keys mean something |
| Bad for | unordered/long-lived lists | keyless lists (keys are "(unsupported)") |

`for_each` wants a real key — the classic pattern `for_each = toset(var.names)` or `{ for n in var.names : n => n }` because a plain list is not directly iterable by key.

### 4. Accessing the created instances

- Output the whole bunch: `count` = `local_file.by_count[*].filename` — `for_each` = `values(local_file.by_foreach)[*].filename` or `{ for k, v in local_file.by_foreach : k => v.filename }`.
- Conditional object access: `length(local_file.by_count) > 0 ? local_file.by_count[0].filename : ""`.
- Full map: `local_file.by_foreach` is already a map — `local_file.by_foreach[key]`.

### 5. dynamic blocks — nested repeating blocks

`dynamic "block" { for_each = ...  — content { ... } }` is for nested blocks inside a resource that repeat — the canonical AWS security group ingress list:

```hcl
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.from
    to_port     = ingress.value.to
    protocol    = ingress.value.protocol
    cidr_blocks = ingress.value.cidr
  }
}
```

Rules of thumb: use it when the block list is genuinely variable — keep `content` simple — never nest `dynamic` inside `dynamic` if you can flatten first. Verified locally via the list-comprehension file in the lab (`dyn.txt` content joined from the `for` expression).

The `for` expression in action — one flattened line of all names:

```hcl
resource "local_file" "by_dynamic" {
  filename = "${path.module}/dyn.txt"
  content  = join(",", [for n in var.names : n])
}
```

### 6. Common pitfalls

- `count` everywhere — the reindex destroy+recreate trap — nothing survives list reordering.
- `for_each` over a raw list — errors — must wrap in `toset()` or map.
- Mutating a map key inside `for_each` — even a key change counts as destroy+recreate of that instance.
- `for` vs `for_each` confusion — one is an expression inside other expressions, the other is a resource metafunction. Interviewers LOVE this confusion.
- Dynamic block referencing `each` — inside `dynamic` it is `dynamic_block.value`, not `each.value`.
- Numeric `count.index` used as state identity for anything with a real world name (instances, buckets).

### 7. Interview Q&A

Q: count or for_each for a list of three EC2s that will change size?
A: for_each over the list (via toset or key map) — so removing one instance only destroys the exact instance, not a cascade of reindexed ones.

Q: Why exactly does count destroy a resource that isn't changing?
A: Because state keyed it by index, not by value — when the list shrinks, item N is now a different value under the same index, and Terraform cannot resize in place — it must tear down and rebuild to reassign.

Q: What is a dynamic block and when do you use it?
A: A construct that generates a repeating nested block from a collection — SG rules, tags. Used when the block count varies by input and you don't want to hand-write blocks.

Q: Can you use for_each on a list?
A: No — keys must be strings. Wrap in `toset(var.list)` or build `{for v in var.list : v => v}`.

Q: How do you loop through resources built with for_each in an output?
A: `values(type.name)[*].attr` or `{ for k, v in type.name : k => v.attr }` — the resource becomes a map keyed by the source keys.

### 6.1 The for expression kitchen — transform examples to have cold

```hcl
locals {
  lower_names  = [for n in var.names : lower(n)]
  by_upper     = { for n in var.names : upper(n) => n }
  with_prefix  = [for n in var.names : "pre-${n}" if n != "skip"]
  attrs_flat   = flatten([for k, v in local.by_upper : [k, v]])
  sums         = { for i, n in var.names : n => length(n) }
}
```

Read each line out loud: first maps, second **also filters** with an `if`, third keys a map from a computed value, fourth flattens nested lists, fifth uses the index. Interviewers occasionally ask "give me a for that returns half the map" — `{for k, v in var.map : k => v if cond(k)}` is the exact answer shape.

### 6.1b Optional lists and null-safe iteration

```hcl
variable "optional_names" {
  type    = list(string)
  default = []
}

resource "local_file" "opt" {
  count = length(var.optional_names) > 0 ? length(var.optional_names) : 0
  # ...
}
```

The trap: `count = length(var.optional_names)` with a null default errors (`length(null)` is invalid). The guard — a ternary around presence — is the standard fix, and pair it with `try()` (`try(local_file.opt[0].filename, "")`) for safe downstream reads. Saying "I gate the count on non-emptiness, not just length" shows you've actually hit the null-list wall.

### 6.2 toset and why keys must be unique

```hcl
for_each = toset(var.ip_ranges)   # set — each element is a distinct key
for_each = { for e in var.ip_ranges : e => e }  # explicit key map, same idea
```

A list with duplicates would create duplicate keys — Terraform errors. The mental image: for_each keys are a SET — if your input allows repeats, dedupe first (toset) or make keys unique with a suffix. The lab used `{ for n in var.names : n => n }` so keys and values were identical — the simplest honest example.

### 6.3 count.index when order matters — the trap in full

The destroy pattern isn't "an item was removed" — it is "an item at an INDEX was removed." The plan literally recycled `count_1` from "b" to "c":

```
local_file.by_count[1] — was "b", becomes "c"  → destroy + create
local_file.by_count[2] — "c", index now empty   → destroy
```

Because the INDEX is identity, any shift cascades. Now say it for an EC2 fleet: removing node 2 of 10 reindexes nodes 3–10, and Terraform destroys + recreates all of them, not just the removed node. That example — spoken with the word "reindex" — is the interview's home run on this topic.

### 6.4 Dynamic blocks with real limits

Keep these rules of thumb cold: one level of nesting preferred — `content` blocks short — drive from a list of objects (not a list of strings — you lose field access, `ingress.value.from_port` is the shape that works) — and treat slices carefully because `dynamic` re-evaluates per iteration. If a block never varies, do not make it dynamic — static blocks are easier to review.

### 6.5 When for_each beats count even for numbers

A fleet of numbered instances ("db-01..db-03") tempts count. But if any instance is ever deleted selectively — or reordered — the numbers shift. Use `for_each` over explicit strings (`"01","02","03"`) and the keys stay glued to the world forever. That is the transferable judgement: identity that matters = for_each — throwaway repeated copies = count.

### 6.6 Splats, conditionals and the not-quite-resource cases

The patterns interviewers watch for:

```hcl
locals {
  all_names   = local_file.by_count[*].filename          # splat over count list
  fe_values   = values(local_file.by_foreach)[*].filename # over for_each map
  first_name  = length(local_file.by_count) > 0 ? local_file.by_count[0].filename : ""
  named_pick  = try(local_file.by_foreach["b"].filename, "missing")
}
```

Three reads: splats handle lists of resources cleanly — the ternary guards an empty `count` — `try` softens a missing for_each key. Grouped references like `type.name[*]` collapse to a list, and `values()` on the for_each map gives you the same shape in key-loss form. Saying "I use `[*]` when I treat a collection as a list and `values()`/`lookup()` when I need the keys" is the answer to 90% of collection-access questions.

### 6.6b Looping your module calls

Modules can also be multiplied, with the same identity rules as resources:

```hcl
module "bucket" {
  source   = "./mymod"
  for_each = toset(var.bucket_names)
  name     = each.key
}
# addresses become module.bucket["logs"], module.bucket["backup"], ...
```

The interview note: every `count`/`for_each` judgement from resources applies identically to module calls (index-reindex traps, key-based identity, `module.mod["key"].output` reads). Being able to say "modules loop under the same rules as resources — identity by key" covers a question pattern that trips a lot of candidates.

### 7.5 Mock interview drill — the shrinking list (5 minutes)

Prompt: "Here's a list of five subnets — the fifth is decommissioned. Using count, the plan wants to rebuild all four others. Justify or correct the implementation."

Answer: count keys by index, so removing index 4 reindexes 0-3 only in the sense of INDICES — but if we remove the fifth, indices 0-3 keep the SAME subnets, so no rebuild — the rebuild story only appears when you remove from the MIDDLE (index 2 → indices 3,4 shift). Either way the durable fix is `for_each` keyed by subnet identity: removing any entry touches only that entry. Interview geeks will love the precision: "count reindexes — for_each never loses identity."

Pass when the explanation distinguishes middle-removal from tail-removal and lands on for_each-for-identity.

### 8. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can say what for transforms vs what count/for_each create | |
| 2 | Can explain the count reindex destroy+recreate trap | |
| 3 | Can explain why for_each handles removals without cascades | |
| 4 | Has run the shrink-list lab and read the 2-to-add/4-to-destroy plan | |
| 5 | Knows how to access count and for_each outputs | |
| 6 | Knows for_each requires set/map (toset pattern) | |
| 7 | Has written a dynamic block | |
| 8 | Knows `dynamic_block.value` inside dynamic content | |
| 9 | Can read the plan lines that reveal recycled indices | |
| 10 | Knows when to pick count over for_each (identical numbered pile) | |
| 11 | Can flatten collections with `for` in expressions | |
| 12 | Can defend for_each identity-by-key in words | |
| 13 | **SELF-VERIFY** — Rebuilt the count/for_each/for scratch lab, removed "b", matched the plan above, destroyed lab dir | |

Verdict: PASS when you can answer "the list shrunk, why did everything break, and what do we change?" with a concrete before/after plan — this is a top-3 Terraform interview question.

Next session: TF.P0.7 — escaping the single-file kitchen sink: modules.

---

## TF.P0.7 — Modules: structure, source, versioning

One-line focus: a module is a folder of HCL that takes inputs and returns outputs — know the three-file structure, local vs registry sources, and how versioning pins behavior.

The interview wants to know you stop copy-pasting and start composing: `main.tf` (resources), `variables.tf` (inputs), `outputs.tf` (contract), sourced by local path or registry, pinned by version, wired into the plan like any other node. All verified locally — zero cloud.

### 1. What a module is

A module is any directory containing `.tf` files. Until today it has been the root module of your project. Calling `module "x" { source = "./mymod" }` instantiates a CHILD module: its resources enter your plan/state, its inputs are your variables, its outputs are what you read on the other side.

The interview mental model: HCL → module → plan → state. Modules flatten into the same graph — being a module changes addresses, not mechanics.

### 2. The canonical structure

```hcl
# mymod/main.tf
variable "greeting" {
  type    = string
  default = "hi"
}

resource "local_file" "greet" {
  content  = var.greeting
  filename = var.greeting
}

output "made_file" {
  value = local_file.greet.filename
}
```

```hcl
# root main.tf
terraform {
  required_providers {
    local = { source = "hashicorp/local" }
  }
}

module "hello" {
  source   = "./mymod"
  greeting = "hello"
}

output "from_mod" {
  value = module.hello.made_file
}
```

The contract: the module declares its inputs via `variable`, its visible surface via `output` — anything else is private by convention. This is exactly how modules stay testable and reusable.

### 3. Verify — build it, apply it, read the output

```bash
$ cd /tmp/tfdemo/mod                         # scratch lab, destroyed after
$ terraform init -input=false
$ terraform validate
Success! The configuration is valid.
$ terraform apply -auto-approve -input=false
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
from_mod = "hello"
```

The module ran like any resource — one create, clean output. Two more real behaviors worth hitting:

- Validating a bare module directory standalone fails without its own provider declaration — a child module inherits providers from the root, so standalone `validate` needs a provider source present:
  ```bash
  $ cd mymod && terraform validate
  Error: Missing required provider
  ```
  Then adding a minimal provider block to the module folder makes its own `init` + `validate` pass. The takeaway: modules don't declare backends, but they may publish provider requirements.
- `terraform init` inside the module directory is normal — every directory with `.tf` files can be initialized as its own root for testing.

### 4. Sources and versioning

- **Local path** `source = "./mymod"` — speed, same repo, no version concerns — tracks your working tree.
- **Registry** `source = "hashicorp/consul/aws"` — published module, `namespace/name/provider`, installed to the local module cache, checksummed into `.terraform.lock.hcl`.
- **Git refs** `source = "git::https://github.com/org/mod.git?ref=v1.2.0"` — pinning via `ref` is how teams version internal modules — `ref` controls exactly which commit you consume.

Version pinning matters for the same reason provider pinning does: modules change behavior, and a floating source makes "worked yesterday" unrepeatable.

### 5. Inputs, outputs, and the contract

- Inputs: every variable the module needs, ideally with `type` and a sensible `default`. Required inputs have no default and no optional marker — Terraform errors at plan if missing.
- Outputs: the minimal surface you promise consumers. Exposing everything couples you to internals.
- Optional + nullable: `type = string, default = null` is the "set it only if you need it" pattern.

The name to remember: Terraform Registry modules follow standard conventions (README, LICENSE, examples, variables/outputs documented) because the contract is what makes them sharable.

### 6. The interview storyline

"Five teams were all copy-pasting the same network/firewall config. We extracted it into a module with a versioned git source, so a fix ships once and every workspace picks it up on a bump. The plan verb changed from 'someone edited four copies' to 'upgrade the ref, review the output diff.'"

That is 90% of the module story the panel wants: mindset (compose, don't copy), structure (main/variables/outputs), and control (version, pin, review) — not clever HCL.

### 7. Common pitfalls

- Modules with hardcoded values instead of variables — the whole point is parametrization.
- Leaking cloud provider config into modules — providers come from the root — keep modules provider-agnostic where you can.
- No version pin on git-sourced modules — any push to the default branch re-floats every caller.
- Huge module trees that slow init and obfuscate every plan — compose small, flat modules.
- Forgetting that modules CAN nest — a module can call another module — and version the chain.

### 8. Interview Q&A

Q: What's inside a module and why those three files?
A: `main.tf` holds resources, `variables.tf` declares the input contract, `outputs.tf` the return contract. The split keeps the interface readable and the implementation swapable.

Q: How do you version a module used by ten repos?
A: Source it from a git ref (`git::...?ref=v1.2.0`) or the private registry and bump the ref deliberately — the callers opt into behavior changes via a version bump.

Q: How do child modules get providers and state?
A: Providers are passed from the root module (via `required_providers`/provider configuration inheritance) — each module's resources live in the SAME state, addressed with the module prefix.

Q: Can a module be tested on its own?
A: Yes — initialize the module directory as its own root (it needs its own provider block for standalone validate), run plan/apply, then destroy. Same engine, narrower scope.

Q: Local path or registry source?
A: Local for speed and exploration, registry/git-ref for anything meant to be shared — version control is the differentiator.

### 6.1 Module outputs — the only door to the outside

Everything a parent needs must be an `output`. If a value is not an output, consumers cannot read it — period. That forces a healthy module discipline: decide the interface (outputs) first, then implement. A module with one resource and three outputs is more usable than one with fifteen resources and one output.

### 6.2 Registry modules and the version pin reflex

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  # required inputs come from the module docs
}
```

Pinning `version` is non-negotiable for repeatability — the lock file records the exact module digest. An unpinned module = a floating dependency that can shift behavior on a fresh init. In the same breath, name the privacy check: public registry for inspiration, private registry/git-ref for IP you must not re-publish.

### 6.3 Modules in a team — the review usage pattern

The highest-value habit with modules is reading a module PR as a CONTRACT REVIEW: did the outputs change? Did a default change behavior silently? Did required inputs appear? Every module bump should be a deliberate diff, not a silent init update — which is why the git-ref pinning habit matters so much with several consuming workspaces.

### 6.4 Testing modules without a cloud

Since everything in this war-room is local: a module can be exercised by spawning a scratch root that consumes it (the exact lab pattern), running plan, applying, destroying, deleting the scratch. That "consume → plan → apply → destroy → delete" loop is the universal module smoke test, cloud or not, and it is fully repeatable for interview prep.

### 6.5 The module FAQ reflex

- "Where do providers come from?" — from the ROOT module's configuration, passed down — modules declare requirements, roots configure instances.
- "Where does state live?" — same state as everything else — module resources are just addressed with the `module.<name>.` prefix.
- "Can a module call a module?" — yes — composition nests, and every level still flattens into one graph.
- "Backends inside modules?" — no — backends are a root-module concern. Modules consume state, they do not define it.

### 6.6 A bigger tree — the composition that impresses

The narrative shape interviewers respond to:

```hcl
# root — the workspace entry point
module "network" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  cidr    = var.cidr
}

module "cluster" {
  source        = "./mymod"          # local team module
  vpc_id        = module.network.vpc_id      # cross-module dependency
  subnet_ids    = module.network.private_subnets
  instance_type = var.instance_type
}

output "kubeconfig" {
  value     = module.cluster.kubeconfig
  sensitive = true
}
```

Read the interesting parts: module reads module (`module.network` fed into `module.cluster`) — dependencies span module boundaries and express clearly in the plan — the output is marked `sensitive` (so the shell hides its value) — the registry module is version-pinned, the local one pinned by ref at its source. Say "modules are unit-of-composition, not unit-of-deployment" and the structural half of the answer is done.

### 6.7 The module-publishing checklist

When a module graduates to shared use, the reviewers want to see:
- Variables typed with `type` and sensible `default` (or required, clearly documented)
- Outputs minimal — every output is a commitment
- Optional: `default = null` with `try()`/`coalesce` guards inside for graceful absence
- README (registry norms) stating inputs/outputs/example
- examples/ directory that consumes the module as the smoke test
- Version tag at the source (git ref or registry version), pinning by callers

Name all six and you've basically answered "how do you treat modules as a product" before the interviewer asks it.

### 6.8 The last module question — "why are my module updates scary?"

Because a module change is a CONTRACT change that multiplies across every caller. The discipline that de-frightens it: read the output/input diff of a module PR as a contract review (breaking = new required input, changed output), pin caller versions, and always apply after bumping through the plan artifact. Framing the answer that way turns a fear story into a process story — the final beats of a strong module interview.

### 8.5 Mock interview drill — the module extraction (5 minutes)

Prompt: "Three repos duplicate the same VPC pattern, and a subnet fix has to be shipped three times. Offer a module plan in under a minute and defend the versioning choice."

Answer: extract `main.tf`/`variables.tf`/`outputs.tf` expressing the VPC shape as input contract — host the module via git ref (`?ref=v1.2.0`) or private registry — callers bump the ref deliberately. The crucially defensible part: version pin means a fix ships as a REVIEWED bump, not a silent drift — and unpinned modules are exactly how "worked yesterday" dies. Name the contract advantage: the subnet fix lives once, outputs stay stable, dependency surface shrinks.

Pass when the versioning decision comes second, after "inputs/outputs are the contract."

### 9. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can explain a module as an input/output contract | |
| 2 | Knows the three-file convention and what each file is for | |
| 3 | Has built and applied a local-path module | |
| 4 | Has passed inputs and read module outputs | |
| 5 | Knows why a bare module `validate` errored (missing provider req) | |
| 6 | Can compare local/registry/git-ref sources | |
| 7 | Knows git refs are how internal modules get versioned | |
| 8 | Can restate the mental model HCL → module → plan → state | |
| 9 | Knows modules inherit providers from the root | |
| 10 | Knows module state addresses use the module prefix | |
| 11 | Can sell the refactor-to-module story in two sentences | |
| 12 | Knows nesting modules is allowed and versionable | |
| 13 | **SELF-VERIFY** — Rebuilt the module lab, applied, destroyed, removed scratch dir — outputs match above | |

Verdict: PASS when you can both build a 3-file module from scratch and argue WHEN to extract one — the judgment matters more than the syntax.

Next session: TF.P1.1 — making Terraform refuse to touch your precious things: lifecycle.

---
## TF.P1.1 — lifecycle, moved, prevent_destroy, ignore_changes

One-line focus: four keywords that bend default Terraform behavior so it stops touching things it shouldn't, stops being confused by addresses that changed, and survives mistakes no one should ever make again.

The interview wants to know how to express operational intent in configuration: "never destroy this," "ignore this field's drift," and "these resources used to live at different addresses." All four — `lifecycle` meta-arguments, `moved`, `prevent_destroy`, `ignore_changes` — are about overriding the default plan graph with explicit intent. Nothing here needs a cloud — it is pure config-level truth.

### 1. The lifecycle meta-argument

`lifecycle` is a block that can appear inside ANY resource (and module in newer versions). It does not change what the resource IS — it changes how Terraform is allowed to change it. The four core settings interviewers probe:

| Setting | Effect | Typical use |
|---|---|---|
| `create_before_destroy` | create replacement first, then destroy old | zero-downtime-ish replace for apps needing a rolling swap |
| `prevent_destroy` | plan/apply errors if the resource would be destroyed | databases, buckets, anything irreplaceable |
| `ignore_changes` | listed attributes are exempt from drift detection | auto-scaling tags, AMI id, fields the app mutates |
| `replace_triggered_by` | recreate when a dependency value changes | forcing a re-roll of a compute unit when a config value flips |

The pre-built default order is destroy-then-create. `create_before_destroy` flips it so the new object exists before the old one dies — used to keep availability during a rolling replacement. The tradeoff is timing: for a few seconds BOTH exist (DNS/names that collide can trip on this).

The full shape of the block:

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
    ignore_changes        = [ami]
    replace_triggered_by  = [aws_security_group.web.id]
  }
}
```

Interview translation: "lifecycle overrides plan behavior — it is how you encode operational policy like 'never drop this bucket' directly next to the resource it protects."

### 2. prevent_destroy — the guardrail

When `prevent_destroy = true` is set, any plan that would DESTROY that resource fails outright at plan time:

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "corporate-archive"
  lifecycle {
    prevent_destroy = true
  }
}
```

Now `terraform destroy` (or a config change that removes the resource) refuses:

```
Error: Instance cannot be destroyed
Resource aws_s3_bucket.data has lifecycle.prevent_destroy set.
```

The message is the feature: destruction is an intentional, explicit act — you have to remove the flag, review, and approve before the plan will succeed. Teams use it as a last line of defense around prod data stores. The trap: it is a config change, not a lock — a `state rm` (TF.P0.2) bypasses it entirely, so it protects against ACCIDENTAL destroy, not malicious or mistaken state surgery.

Additional edge: when TF_P1-style `moved` blocks are combined with prevent_destroy, READ the plan carefully — a rename with a bad moved block can read as destroy+create and get blocked by the flag, which is exactly the behavior you want surfacing.

### 3. ignore_changes — stop fighting the platform

```hcl
lifecycle {
  ignore_changes = [
    ami,
    tags["auto_scaled"],
    user_data
  ]
}
```

The listed attributes are dropped from the drift comparison. The canonical AWS case: autoscaling rewrites a tag, a deploy pipeline injects user_data, the AMI selector changes as part of an ops flow that Terraform should not fight. Without `ignore_changes`, every plan after an external mutation proposes a revert — the platform and Terraform ping-pong.

Trap: this is a big stick. Over-ignoring hides real drift until the day it matters. The interview answer that lands: "ignore_changes is for attributes the OPERATING environment legitimately owns — we keep the list small and review it, because it is effectively opting that field out of the config's authority."

### 4. create_before_destroy vs destroy-then-create

Default order: destroy old, then create new. Problem: a rolling replace of a load-balanced instance means a gap where nothing runs. `create_before_destroy = true` flips the order — new first, then remove old. Consequences worth naming in interviews:

- IDENTITY changes — most resources get new ids after recreation, so anything referencing the old id must be flexible (typically fine, since references go through Terraform attributes).
- NAME collisions — if the resource has a fixed name that must be globally unique, both versions can't coexist during the window.
- Depends on ordering of dependencies — replace of a network node with create-before-destroy can cascade more broadly than expected.

The pragmatic interview grade: know the flag exists, say "roll swap," and name the name-collision caveat.

### 5. moved blocks — first-class state renames

Before `moved`, renaming a resource meant: change config, then `terraform state mv` to keep state continuity (TF.P0.2), then plan. The `moved` block encodes that transition IN CONFIG so future teammates and runs see exactly what moved, no manual state surgery:

```hcl
resource "aws_instance" "web" {
  # ... current config
}

moved {
  from = aws_instance.legacy_web
  to   = aws_instance.web
}
```

Terraform reads `moved` during refresh: it rewrites the address in state from the old to the new, no destroy/recreate churn. The plan output says something like:

```
aws_instance.legacy_web has moved to aws_instance.web
```

Moved blocks are evaluated continuously — you can keep the block in the file for a while so old plan/apply sessions that still reference the old address don't churn. After a full cycle in every workspace, the block can be deleted (older state references are gone by then). This is the config-native successor to hand-running `state mv` — worth an interview mention precisely because it shows you know the difference between a manual one-off repair and a durable, reviewable migration.

### 6. replace_triggered_by

Sometimes you don't need to drift-check a field — you need to re-roll whatever CONSUMES it. `replace_triggered_by` lists dependencies external to the resource: when any listed value changes (or a listed resource is replaced), the resource is recreated even if its own config is unchanged:

```hcl
resource "aws_instance" "web" {
  ami = var.ami
  lifecycle {
    replace_triggered_by = [aws_launch_template.web.version]
  }
}
```

Use cases: app needs to re-provision when an AMI/launch template version bumps — compute must re-roll when a config map changes. The interview word for it: "propagate a dependency change into recreation."

### 7. Mental model — policy at the resource, not in the runbook

All four mechanisms move operational policy from the head of whoever runs apply into the repository, next to the resource they protect. Plan is still the diff engine — lifecycle settings just inform what a valid diff looks like. `prevent_destroy` converts a destructive diff into an ERROR — `ignore_changes` converts an external mutation into a NO-OP — `moved` converts an address change into a NOTHING-BROKE rename — `create_before_destroy` converts a gap-creating swap into a rolling swap.

This is the kind of answer that separates a "runs terraform" candidate from an "operates terraform with intent" candidate.

### 8. Common pitfalls

- `prevent_destroy` on everything — then every repo-wide refactor needs flag surgery — use it on what is genuinely precious.
- `ignore_changes = [ami]` as a default and then wondering why a vulnerability never got patched via config.
- `moved` blocks pointing to addresses that never existed — plan errors rather than silently no-opping.
- Forgetting `create_before_destroy` can hit unique-name collisions during the two-object window.
- Manually running `state mv` when a `moved` block was already present — invalidates the migration story.
- Deleting `moved` blocks too early — a long-lived workspace with old state starts churning again.

### 9. Interview Q&A

Q: What does `prevent_destroy` do and, more importantly, what does it NOT do?
A: It makes any plan that would destroy the resource fail at plan time with a specific error. It does NOT protect against `state rm`, which forgets the resource without a graph operation.

Q: When would you set `ignore_changes` on a security group rule count?
A: When external tooling (or the parent app) legitimately owns that field — the config should not try to revert a change that is a feature, not drift.

Q: What are `moved` blocks for?
A: Encoding an address migration in the configuration so `terraform plan` re-maps old state addresses to new config addresses without recreate churn, and so any teammate running plan sees the same migration, not ad-hoc `state mv` commands.

Q: `create_before_destroy` — what breaks?
A: Resources needing globally-unique names can't hold two in the creation window — and dependencies of the old object may briefly reference two. It trades uptime for name-space complications.

Q: Why does plan error when I set prevent_destroy and also have a moved block?
A: Because the migration plan evaluated a destroy action before the moved remap resolved — a symptom, not a bug: the guardrail rejected the transition because it looked like a destructive change.

### 6.1 lifecycle in modules — the inheritance question

Newer Terraform allows `lifecycle` at the module level: it applies to EVERY resource inside the module's call. That is a powerful escalator — one flag on a module call protects all of its resources. Interviewers sometimes probe whether lifecycle belongs on the resource or the call: the answer is "both exist — resource lifecycle for fine-grained control of one object, module lifecycle for blanket policy across the composition."

```hcl
module "redshift" {
  source = "..."
  lifecycle {
    prevent_destroy = true
  }
}
```

### 6.2 ignore_changes trade-off in review

The honest review position is: an `ignore_changes` entry is an admission that SOMEONE ELSE owns a field — so the correct question at review time is "who owns this?" If nobody does, it is drift hiding in the config. Teams that treat ignore_changes like a bug-fix rather than a supplicant to external reality build configs where the ignore list shrinks over time, not grows.

### 6.3 create_before_destroy failure-mode story

A classic panel question: "we set create_before_destroy on our DB and now the plan is creating a second disk and hanging." The answer: availability has a cost — during the window BOTH objects exist. For anything with a fixed, unique name (a bucket, a DNS record, a drive serial) the creation can fail or collide. Encoding `replace_triggered_by` instead of relying on create-before-destroy for EVERYTHING is the more surgical lever — interviewers reward candidates who name the collision caveat unprompted.

### 6.4 moved blocks in the real migration timeline

The durable pattern for renames:

```
1. add moved block + new resource block (old block optional in newer versions)
2. plan → "has moved to" line, no churn
3. apply
4. keep the moved block until all workspaces/team members run a full cycle
5. delete the block — future plans are clean
```

Delete too early (step 4 skipped) and some stale state address churns on the next plan. That timing judgment — not the syntax — is what the interview is really probing.

### 6.5 Lifecycle policy vocabulary for answers

Three nouns that make candidates sound senior: **guardrail** (prevent_destroy — compile-time protection phrased as plan-time protection), **lease** (ignore_changes — a declared hand-off of ownership), **migration** (moved — a config-encoded address transition). Using them gives structure to answers about what lifecycle is FOR, over and above what it DOES.

### 6.6 The "which knob" drill

Run this mental drill until instant:

- "database must never be destroyed" → `prevent_destroy = true`
- "autoscaler rewrites tags every minute" → `ignore_changes = [tags]`
- "renamed legacy_web → web without recreation" → `moved { from = ... to = ... }`
- "deploy an AMI before retiring old one, minimal gap" → `create_before_destroy = true`
- "re-roll compute when launch template bumps" → `replace_triggered_by`

If you can cold-answer the drill, the lifecycle interview portion is finished.

### 6.7 Lifecycle policy across environments — the pattern

The conversation that impresses: lifecycle intent is often ENVIRONMENT-dependent, and the clean way to express it is a variable-fed boolean:

```hcl
variable "protect_from_destroy" {
  type    = bool
  default = false
}

resource "aws_db_instance" "main" {
  # ...
  lifecycle {
    prevent_destroy = var.protect_from_destroy
  }
}
```

Dev runs with `false` (destroy freely in dev), prod passes `true`. The plan in dev shows a normal destroy — in prod, a destroy attempt becomes a plan ERROR. That is lifecycle policy with an environment seam — exactly the kind of pattern that makes a 1-3 YOE candidate look like they've shipped environments, not just tutorials.

### 6.8 One gotcha per knob, the final round

- `prevent_destroy` — blocks plan/apply destroys, NOT the provider's own out-of-band lifecycle — and any `state rm` is out of scope.
- `ignore_changes` — hiding a field from DIFF means plan can miss a change that matters — keep the list deliberate.
- `create_before_destroy` — unique-name objects collide during the twin window.
- `replace_triggered_by` — avoid cycles, since referencing the resource itself would self-trigger.
- `moved` — the block's "from" must be a real past address — deleting the block before all workspaces cycle causes the churn to return.

One sentence to end every lifecycle answer: "lifecycle is where Terraform's greedy converge gives way to your intent."

### 6.10 The destroy-path lifecycle — a note interviewers accept

`prevent_destroy` blocks plan-time — but if you FORCE the issue (manually remove the state entry), the lifecycle never fires — there's no plan to error on. That is not a trick, it's the architecture: lifecycle governs the graph walk, state rm bypasses the graph entirely. Being able to say "lifecycle protects plan/apply, state surgery bypasses the graph" shows you know both lanes of the system — the path through review, and the path around it.

### 9.5 Mock interview drill — the guardrail inventory (5 minutes)

Prompt: "A new teammate keeps breaking prod with terraform destroy and hand-renames. Which lifecycle knobs are you reaching for and why?"

Answer: prevent_destroy on the state buckets/database (destruction becomes a plan error) — moved blocks as the standing remedy for hand-renames (config-native migration beats state surgery) — create_before_destroy only where a rolling swap matters — ignore_changes where the platform owns fields. The governance add-on: review the lifecycle/policy changes like any prod change, and pair with a CI drift check (TF.P1.2) so hand-rename fallout surfaces as a plan failure — not a silent skip.

Pass when you treat the knobs as a POLICY surface, not just syntax.

### 10. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can list all four lifecycle settings and their purpose | |
| 2 | Understands lifecycle overrides plan behavior, not resource behavior | |
| 3 | Knows prevent_destroy errors at plan time | |
| 4 | Knows prevent_destroy does not block state rm | |
| 5 | Can explain ignore_changes use case honestly | |
| 6 | Knows default order is destroy-then-create | |
| 7 | Can name create_before_destroy caveats | |
| 8 | Can explain moved block vs state mv difference | |
| 9 | Knows when moved blocks can be deleted | |
| 10 | Can explain replace_triggered_by | |
| 11 | Could defend a min-scope ignore_changes list in review | |
| 12 | Can narrate the "policy next to the resource" mental model | |
| 13 | **SELF-VERIFY** — Wrote and read back each lifecycle + moved block from memory with zero syntax rewrites | |

Verdict: PASS when you can place the correct lifecycle keyword on a set of made-up resources ("the bucket? prevent_destroy. the AMI? ignore_changes. the renamed node? moved.").

Next session: TF.P1.2 — Terraform becomes a reviewable artifact: CI as the gate between plan and apply.

---

## TF.P1.2 — Terraform in CI: plan-as-gate, apply-on-merge

One-line focus: the modern pipeline is "plan in the PR, apply on merge" — know the mechanics, the security posture, and how to keep credentials out of code.

The interview wants to know you can describe a Terraform delivery pipeline that a team can trust: every change is planned and REVIEWED before anything mutates. Two halves: the CI mechanics (plan artifact, apply on merge) and the security posture (no creds in code, OIDC/cloud roles, least privilege). Model-only again — you can design and defend this without touching a cloud.

### 1. The golden flow — plan in PR, apply on merge

The pipeline has four gates:

1. **Validate** — `terraform fmt -check` + `terraform validate` + a `terraform plan` run per environment, all on every PR/version bump.
2. **Review the plan** — the human reads the plan diff in the PR comments (or the platform's plan UI). This is the security and correctness gate, not the Lint.
3. **Approve** — the PR gets a maintainer review — apply is only triggered by the merge (or an approved apply-only workflow for prod).
4. **Apply on merge** — the merged commit runs `terraform apply -auto-approve` using the saved plan artifact (TF.P0.4's `-out`) so the applied diff is exactly the reviewed one.

The artifact chain: `terraform plan -out=tfplan` in the PR job → store the binary plan (artifacts/PR comments) → on merge, `terraform apply tfplan`. Applying the saved artifact (not a fresh re-plan) is the difference between "we reviewed the diff" and "we reviewed A diff."

### 2. The two writer models

Two architectures solve "who runs apply?"

- **Plan+apply in one automated job (single-runner)** — the runner computes a plan, automatically applies to the shared state after the PR merges. Simplest setup, weakest guarantees: nothing human-reviewed can break if the runner is misconfigured.
- **Two-stage with human approval (Atlantis/Spacelift style)** — plan is produced on PR comment, a human runs `atlantis apply` after review, apply is a distinct auditable action. Stronger for prod — accounts for the human in the loop.

Either way: review happens on the PLAN, not on the merge commit message. That is the engineering habit interviewers are probing for.

### 3. Environment and workspace plumbing

- **Workspaces** (or separays per env): one per environment (dev/staging/prod) via `terraform workspace` or `TF_WORKSPACE`, or one remote state key per env — so CI knows which state to touch and which vars to pass.
- **Vars**: environment-specific `tfvars` files (non-secret) checked into the repo — secrets injected at runtime from the CI secret store or secrets manager via `TF_VAR_`.
- **Plan caching**: store `tfplan` keyed by commit so merges and review comments point at the same artifact.

The storytelling line: "dev gets cheap continuous integration, prod gets an approve gate — same code, different pipeline legs, because the risk profile differs."

### 4. Security posture — the part interviewers probe hardest

The actual interview gold is here, not in YAML syntax. Four bullets worth memorizing:

1. **Never put credentials in the repo.** No `aws_access_key` in tfvars, no keys in the plan/changelog, no credentials baked in base64. Secrets come from a secret store at runtime.
2. **Use cloud roles with OIDC/IRSA-style federation, not long-lived static keys.** CI assumes a role scoped by workload identity: AWS OIDC mapping, GitHub Actions permissions with `id-token: write`, and a role trusting that workload — no keys on disk in the runner.
3. **Least privilege:** the plan/apply role for an environment can only read+write that environment's backend and mutate only that env's resources. Red-flag behaviors like admin keys are the ones a reviewer flags.
4. **Separate read vs write paths if the pipeline demands it** — some shops run plan with a read-only role, apply with a scoped write role — the plan that a human approves was produced without broad privileges.

The one-liner answer: "Credentials never touch the repo or the plan — CI authenticates as the workload via OIDC into an env-scoped role."

### 5. The review red-flags interviewers want to hear you name

- State file committed to git (or the state bucket with world-ish policies).
- `-auto-approve` in the same job that generated the plan — no gate.
- Target-all plans (`-target`) snuck into the merge path.
- Long-lived static keys in the runner environment.
- Plan job with full-env admin role for a change touching a single config map.
- No `-out` artifact — apply re-plans whatever the world looks like at merge time.

Being able to LIST these — as a reviewer habit — is as valuable as being able to write the pipeline.

### 6. Pipeline shape — one concrete, defensible design

```
PR opened
  └─ job: fmt + validate (fast fail) + plan -out=tfplan per env
        └─ publish plan summary to PR (comment / artifact)
human review: "I approve the change BECAUSE I approved this plan"
merge to main
  └─ job: apply tfplan (saved artifact, -auto-approve) role-scoped to env
        └─ post-apply: plan again to assert zero drift (drift check)
```

Notice the tail: a post-apply drift check turns the pipeline from "we applied" into "we applied and confirmed convergence" — a wired-in TF.P0.5 habit.

### 7. Common pitfalls

- Applying a re-plan instead of the reviewed artifact.
- Broadly-scoped service accounts in multi-env CI — one leak reaches everything.
- Secrets detection (secret scanners) run AFTER the plan job instead of before.
- Merging formatting-only and resource changes in the same PR, burying the meaningful plan diff.
- No drift check — the "plan = no changes" assertion is the cheapest regression test Terraform has.
- Workspace/env confusion in a shared runner — wrong state key applied.

### 8. Interview Q&A

Q: How do you approve a Terraform change in CI?
A: The plan is produced on the PR and published — a human reviews THE PLAN (not the diff of YAML), then either merge-triggered apply or an explicit apply command in an approved PR gate does the mutation using the saved plan artifact.

Q: Why apply the saved plan file instead of re-planning at merge?
A: Because the world may have changed between review and merge — re-planning applies a different diff than the one the human approved. The artifact is the review contract.

Q: How do you stop credentials leaking in a Terraform CI pipeline?
A: They never enter the repo or the plan. The runner is a workload identity (OIDC/IRSA/corresponding service account) that assumes an env-scoped role — secrets come from a secret store at run time only.

Q: What's the difference between CI and a run-control platform?
A: CI (GitHub Actions, GitLab, Jenkins) is where we automate build/test/plan/apply — Atlantis and Spacelift specifically own plan/apply lifecycle, locking, and approval as a product — the pipeline concerns overlap, the guardrails differ (TF.P2.2).

Q: One change, many environments — how do you keep them in lockstep?
A: Same module/version + env-scoped vars + per-env state key, promote via the same pipeline legs with progressively stricter gates (dev auto-apply, prod human-approve).

### 6.1 A minimal pipeline you can actually defend

YAML shaped in the style of GitHub Actions — the reviewer-friendly version:

```yaml
name: terraform-env
on:
  pull_request:
  push:
    branches: [main]
jobs:
  plan-dev:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write          # OIDC: let CI assume the env role, no keys
    steps:
      - uses: actions/checkout@v4
      - name: terraform plan
        env:
          TF_WORKSPACE: dev
        run: terraform init -input=false && terraform plan -out=tf.plan
      - name: save plan
        uses: actions/upload-artifact@v4
        with: { name: plan-dev, path: tf.plan }
  apply-dev:
    if: github.ref == 'refs/heads/main'
    needs: plan-dev
    steps:
      - uses: actions/checkout@v4
      - name: apply saved plan
        env:
          TF_WORKSPACE: dev
        run: terraform init -input=false && terraform apply -auto-approve tf.plan
```

Read it aloud like an interviewer: plan job on every PR (gate), plan saved as artifact, apply job ONLY on main consuming THE SAVED PLAN with no interactive prompt. The permissions block is where OIDC identity lives — no access keys anywhere.

### 6.2 Atlantis in one working picture

Atlantis watches repo events — on a PR comment `atlantis plan` it runs plan and posts output back — `atlantis apply` consumes the saved plan for that PR. Your state backend is configured in config — Atlantis just orchestrates plan/apply + locking through it. The one-sentence differentiator: "review and apply live INSIDE the pull request conversation" — approvals are git-native, no separate UI.

### 6.3 Policy enforcement — the third leg people forget

Beyond approvals, mature pipelines run rule-based policy on the PLAN before apply: Sentinel (TF Cloud), OPA (Spacelift), or a scripted plan-parse check (any CI). Examples that matter to a review: "no public s3 bucket," "no broad IAM wildcard," "no AMI replacement in prod leg." Naming policy-as-code as a SEPARATE gate (approval ≠ policy) shows you have seen real Terraform pipelines, not just the happy path.

### 6.4 Drift as a scheduled health check

Production sanity: a nightly plan job per environment, failing when OUT of date — the empty plan being the pass condition. This catches "someone fixed it by hand," a tag drift, or an open PR that never merged. It is the automated version of the TF.P0.5 reflex, and it turns drift from a surprise into a ticket.

### 6.5 Failure modes of the pipeline itself

- **Plan says pass, apply fails** — artifact was produced against stale facts (worth re-planning at apply time in SOME failure modes, accepting the tradeoff).
- **Lock held by a dead plan leg** — the run hangs — check lock info, force-unlock after verifying death (TF.P0.2/0.3 drill).
- **Wrong workspace in a shared runner** — every env leg MUST pin TF_WORKSPACE — "the readiness test is that a forgotten env cannot silently steal the prod state key."
- **Secret detector trips on the plan** — a plan that prints a secret means a config gaffe, not a scanner bug.

Having the failure modes listed — not just the happy path — is exactly the seniority signal this P1 session exists to produce.

### 6.6a The "no secrets in plan output" special read

A plan can print secret values when the config embeds them as literals — the fix is referencing them from stores. The pattern with either cloud-adjacent mechanism:

```hcl
# bad: inline literal
password = "Sup3rSecretValue"

# good: read at apply time from the secret store
password = data.aws_ssm_parameter.db_password.value
```

When the interviewer asks "how do I keep secrets out of the diff" the crisp answer has three legs: don't write literals into tfvars/HCL, source at runtime from a secrets manager or parameter store, and mark sensitive outputs `sensitive = true`. Flat-out naming all three is the entire answer.

### 6.6 A real drift-check leg — the nightly test

The cleanest way to prove "nothing drifted in prod" is a scheduled job:

```yaml
# Scheduled pipeline, nightly — GitLab or GitHub Actions cron equivalent
drift-check-prod:
  script:
    - terraform init -input=false
    - terraform plan -refresh-only -detailed-exitcode -out=tf.plan
  after_script:
    - |
      if [ $? -eq 2 ]; then
        echo "DRIFT DETECTED — open incident or encode change in config"
        exit 1
      fi
```

The key flag is `-detailed-exitcode`: `0` = no change, `2` = changes detected, `1` = error. The pipeline turns green (zero) or red (two) — no logs to read, no UI to check, just an alert. Sell this as: "the drift radar is not an alert, it is a regression test for reality matching config." Mentioning `-refresh-only` (plan refreshes but proposes no mutations, only reports diff) shows you know the difference between a drift snapshot and a mutation plan.

### 8.5 Mock interview drill — the PR review (5 minutes)

Prompt: "A developer opens a PR for a small prod change. Give the review checklist you run before approving."

Answer: (1) run `fmt -check` + `validate` + a diff-limited plan — (2) confirm the plan touches exactly the resources the PR claims — (3) verify no `-target` and no `-auto-approve` buried in the pipeline leg — (4) confirm secrets are not present in the plan/tfvars diff — (5) check the apply leg reads the SAVED plan artifact (not a re-plan) — (6) confirm the state backend + lock are in place so the apply is serialized — (7) ask whether drift check after apply is scheduled. A reviewer who can name steps 2 and 5 cold is a reviewer who has operated a real pipeline.

Pass when you can run six or more of these without prompting.

### 9. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can draw the plan-in-PR / apply-on-merge flow | |
| 2 | Can explain why the saved plan artifact matters | |
| 3 | Names the two writer models (single-runner vs approval gate) | |
| 4 | Knows review happens on the plan, not the PR diff | |
| 5 | Can describe OIDC/cloud-role auth in two sentences | |
| 6 | Can list 4 credential no-nos | |
| 7 | Knows workspace/env plumbing for multi-env pipelines | |
| 8 | Can list 4 review red-flags | |
| 9 | Values the post-apply drift check | |
| 10 | Can discuss plan role vs apply role separation | |
| 11 | Could defend -auto-approve only in the apply leg | |
| 12 | Can compare own-CI plan output to Atlantis-style plan comments | |
| 13 | **SELF-VERIFY** — Re-wrote the gold flow and the security list from memory — no cloud touched | |

Verdict: PASS when the "dev auto-applies, prod needs a human who read the plan" position survives a skeptical interview follow-up about safety.

Next session: TF.P1.3 — the interactive scratchpad that answers expression questions before they hit code.

---

## TF.P1.3 — terraform console

One-line focus: console is the interactive REPL over your loaded config and state — cheap answers for "what does this expression evaluate to before I type it into main.tf."

The interview wants to know you don't round-trip guesses through apply. Console is read-only, runs against the current working directory, loads config + state, and evaluates one expression per line. Verified live — every transcript below is a real session on /tmp/tfdemo.

### 1. What console is and is not

- IS: an interactive shell for HCL expressions with full access to resources (`local_file.f.attr`), variables, locals, module outputs, and functions — evaluated against live state.
- IS NOT: a way to mutate anything. It never plans or applies — an expression that would be invalid in config is just an error here. Think "pre-flight check for expressions."

### 2. The mechanics

```bash
$ cd /tmp/tfdemo
$ terraform console
> local_file.f.filename
"/tmp/tfdemo/out.txt"
> 1 + 1
2
```

One expression per line, results printed. Non-interactively (the way you'd run it in a script or CI):

```bash
$ echo 'local_file.f.filename' | terraform console
"/tmp/tfdemo/out.txt"
```

Exit with Ctrl-D (EOF) or `exit`.

### 3. What it evaluates

Anything from the interpolation/expression layer of your configuration:

- Resource attributes: `local_file.f.filename`, `aws_instance.web.public_ip`
- Built-in functions: `upper("a")`, `join(",", ["x", "y"])`, `cidrsubnet("10.0.0.0/16", 8, 2)`
- Constructed expressions: `[for s in var.list : upper(s)]`, `merge(map1, map2)`, `lookup(var.map, "k", "default")`
- Count/index and for_each access: `local_file.by_count[0].filename`, keys of a for_each map
- Module outputs: `module.hello.made_file`
- State-derived values, including outputs: `terraform.workspace`, `${path.module}` in expressions

The classic CI-friendly pattern: pipe a query in, assert on the output, fold into a shell test:

```bash
$ value=$(echo 'upper(local_file.f.filename)' | terraform console)
$ test "$value" = '"/TMP/TFDEMO/OUT.TXT"' && echo "pass"
```

Prefix a line with `?` for a sense of how to use a function? The answer to "does console help me?" is: yes, for expression validity and evaluation, not for syntax help — keep docs handy for function signatures.

### 4. Why interviewers like hearing you use it

It demonstrates two habits: (1) you validate expressions against REAL state before applying, and (2) you treat the plan output itself as a review artifact, not a surprise. "I checked the subnet math with console before committing the CIDR change" is a stronger sentence than "it worked when I applied it."

It also quietly demonstrates comfort with HCL as a language — functions, splats, conditionals — in a live setting, which is what the role pays for.

### 5. Common pitfalls

- Expecting console to show plan results — it evaluates expressions, not pending diffs.
- Editing config then forgetting to `validate`/`re-plan` — console uses whatever is loaded, and stale shells confuse people.
- Multi-line expressions — console prefers one-liners — use a temp `.tf` + `validate` for anything sprawling.
- Treating console output as runtime values — expression evaluation is not an apply — scripts reading it should be assertions, not state reads.

### 6. Interview Q&A

Q: What is terraform console for?
A: An interactive/one-shot REPL that evaluates HCL expressions against the current config and state — a sandbox to verify expressions and functions before they land in code, and to poke at resource attributes.

Q: Can console mutate state?
A: No — it is strictly read/evaluate. Any plan/apply still needs the normal commands.

Q: How do you use it in CI?
A: Pipe an expression in, capture stdout, and assert — e.g. checking a computed CIDR or a derived name before the plan. It is a linting/testing tool for expressions, not a pipeline stage.

Q: Console vs plan for checking a value?
A: Plan shows the proposed diff for resources — console answers "what is this expression worth" — different problems, same underlying expression engine.

### 5.1 The console cheat-list — expressions worth testing live

The set you will actually reach for before any non-trivial plan:

```hcl
local_file.f.filename                          # resource attribute
range(0, 5)                                    # list building
[for s in var.list : upper(s)]                  # transform
{for k, v in var.kvs : k => upper(v)}          # map transform
contains(var.list, "a")                        # predicate
cidrsubnet("10.0.0.0/16", 8, 0)                # IP math
lookup(var.map, "missing", "fallback")         # safe map read
flatten([[1,2],[3,4]])                          # flatten
toset(["a","a","b"])                            # dedupe
element(sort(var.list), 0)                     # pick first sorted
```

Each one answered in a second saves a plan round-trip. The habit that interviewers can hear: "I validated the CIDR math and the map lookup in console before the change hit the plan."

### 5.2 Terraform functions interview cheatsheet

Implicitly tested via console — the "name a function" probes:

- String: `upper`, `lower`, `replace`, `join`, `split`, `format`, `substr`
- Collection: `length`, `element`, `lookup`, `merge`, `keys`, `values`, `flatten`, `toset`, `sort`, `distinct`
- IP: `cidrsubnet`, `cidrhost`, `cidrnetmask`
- Conditional/security: `coalesce`, `try` (handle optional fields), `base64encode`, `sha256`
- Type: `can()`, `type()`, conversions like `tostring`

Trap: `try()` vs `lookup()` — `try` returns the expression if valid, else a fallback — `lookup` guards map reads. Interviewers love hearing both named in the same breath.

### 5.3 Console in the expression-debugging narrative

The senior-sounding flow when an expression misbehaves in a plan: put the suspect expression in console → confirm what it returns → adjust → back into config → plan again. It removes the guess-and-reapply loop, which is the real efficiency win the interview wants to see you own.

### 5.4 What console will NOT save you from

It cannot tell you what a resource's attribute will be after creation (`(known after apply)` values come back in some contexts as strings and in others as unknown) — it cannot preview diffs — and it evaluates against whatever config/state is loaded NOW, so a big untracked drift (TF.P0.5) misleads the answer. State your assumption — "console reads current state and config — for post-apply values it is not the tool" — and you sound precise, not evasive.

### 5.5 Longer sessions and real files

A full interactive session against the demo project, exactly as run:

```
$ echo 'local_file.f.filename' | terraform console
"/tmp/tfdemo/out.txt"
$ echo 'upper("hi")' | terraform console
"HI"
$ echo 'can(upper("hi"))' | terraform console
true
$ echo 'contains(["a","b","c"], "b")' | terraform console
true
$ echo '[for i in range(0,3) : i * 10]' | terraform console
[
  0,
  10,
  20,
]
$ echo 'join(",", ["x","y","z"])' | terraform console
"x,y,z"
```

Notes for the transcript: `can()` wraps an expression and returns bool — a favorite way to test "would this blow up" — `range()` builds lists for loops — lists render as blocks in console output — strings render quoted. Reading someone else's console output fluently (as here) is a quiet interview win, since most candidates have never even opened it.

### 5.6 The three-command console workflow

For most interviews, this is the gold chain:

```bash
terraform validate                 # 1. config is structurally sound
echo '<expr>' | terraform console  # 2. expression yields what I think
terraform plan                      # 3. proof against state and reality
```

Console sits between validate and plan: it de-risks step 3 by validating the expression BEFORE the plan has to interpret it. It is not a replacement for plan — plan still proves "the whole graph converges" — but it kills the most common plan-time error class (bad expression) in advance. Say "validate — console — plan" in that order once during the interview and the territory signs itself.

### 6.5 Mock interview drill — the hot-seat console (5 minutes)

Prompt: "Verify an expression that returns the second CPU-heavy instance name from a for_each map, sorted, without touching apply."

Answer: hop into console and type the pipeline step by step — `sort(...)`, index `[1]`, attribute access from the for_each resource map — until the value is right. Narrate: console evaluates the current state — sorting a keys() list then indexing returns the second entry — if the resource were count-based, the access is `type.name[1].attr`, if for_each, it passes through keys. Crucially, say what you CANNOT answer here: values "unknown after apply" — those need a plan.

Pass when the answer lands on "console answers expression-vs-state questions — plan answers diff questions" without being asked twice.

### 7. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Has launched console in a real project dir | |
| 2 | Has evaluated a resource attribute on live state | |
| 3 | Has evaluated a function (upper/join/cidrsubnet) | |
| 4 | Knows one-expression-per-line rule | |
| 5 | Can use `echo ... | terraform console` non-interactively | |
| 6 | Knows console reads config + state, no mutation | |
| 7 | Can access module outputs and count/for_each instances | |
| 8 | Could assert on console output in a script | |
| 9 | Knows console does not show plan diffs | |
| 10 | Can chain console into a smoke-test habit | |
| 11 | Knows when to use a temp file + validate instead (multi-line) | |
| 12 | Can explain why console validates expressions pre-apply | |
| 13 | **SELF-VERIFY** — Re-ran `echo 'local_file.f.filename' | terraform console` on /tmp/tfdemo, matched the quote output above | |

Verdict: PASS when answering expression questions becomes a console session instead of a hopeful apply.

Next session: TF.P2.1 — the JSON dialect and the import CLI we already proved in TF.P0.2.

---

## TF.P2.1 — JSON syntax / import CLI

One-line focus: Terrafom has a JSON syntax (`.tf.json`) and an import command line — know their purpose and the key gotchas.

The interview wants to know you recognize the JSON form when you see it in generated/exported configs, and that `terraform import` is how existing resources get adopted — mechanics fully covered in TF.P0.2, so this session is definition + purpose + when you'd ever touch them.

### 1. JSON syntax — what it is

Terraform HCL has a machine-readable twin: files ending `.tf.json` carried in native JSON. Blocks become `{"resource": {"local_file": {"f": {...}}}}` — resource bodies are objects, meta-arguments keep their names, and lists/maps follow JSON rules. It exists for tool-generated config (cdk-for-terraform emits it) and for cases where HCL would otherwise fight a generator.

Key gotcha that trips people: in JSON, attribute VALUES must be nested as objects/arrays explicitly, HCL-style bare expressions do NOT apply — an expression like `var.x` is written as `"${var.x}"` inside a string. There is also no comment syntax, so it reads worse for humans — that's why you see it predominantly as CI-generator output, not hand-written config.

### 2. When you would encounter it

- cdktf-generated stacks (CDKTF emits `.tf.json`)
- Config serialized by tools, exporters, or "does this EC2 exist" scrapers
- Pipelines that produce a config from a template engine rather than editing HCL

If a question comes: "a file ends in `.tf.json` — is Terraform fine?" Answer: yes, `plan`/`apply`/`fmt` handle it, `terraform fmt` will normalize it (and behavior differs from HCL formatting — it validates schema but does not rewrite to HCL).

### 3. The import CLI — recap and sharpen

Everything in TF.P0.2 holds — the sharp edges worth re-stating:

- `terraform import <address> <id>` — adopt an existing object — the ID is provider-specific (the cloud resource's identifier).
- The config block must exist first — otherwise plan/import errors before reaching the provider (verified live).
- Not every resource supports import — providers implement it per-resource (verified: `local_file` and `random_*` don't — `time_offset` does).
- After import, a `plan` will show exactly what config-vs-actual differs — that diff is your adoption checklist.
- Addresses target the NEW address form (module names, index) — import into for_each/count instances is supported but fiddly — importing into a fresh name then `state mv`-ing is often cleaner.

The interview line: "import gets reality into state — the config block is the gatekeeper, and the plan after import is the review."

### 4. Common pitfalls

- Importing without the matching config block (error, verified).
- Assuming import works for every resource.
- Importing into a resource that config will immediately restructure — you import once, then plan churns.
- Hand-writing `.tf.json` and forgetting expression quoting (`"${var.x}"`).
- Confusing `terraform import` (state adoption) with `terraform state mv` (state relocation).

### 5. Interview Q&A

Q: What does a `.tf.json` file buy you that HCL doesn't?
A: A machine-friendlier representation for generated config and tooling to emit — Terraform treats both dialects identically at plan/apply.

Q: Import an existing EC2 — walk me through it.
A: Write the analogous resource block, run `terraform import aws_instance.web i-0abcd…`, then plan: the diff shows every attribute where config and reality disagree — that is the adoption review.

Q: Can every resource be imported?
A: No — import is implemented per resource by providers (some refuse outright) — check the docs, and after a successful import always review the follow-up plan.

### 3.1 JSON syntax prepares for the field

Write a resource in JSON from memory — this is the level of comfort expected:

```json
{
  "resource": {
    "local_file": {
      "f": {
        "content": "hi",
        "filename": "/tmp/tfdemo/out.txt"
      }
    }
  },
  "output": {
    "path": {
      "value": "${local_file.f.filename}"
    }
  }
}
```

Note the JSON quirks that catch people: block names become object keys — list-valued attributes are JSON arrays — expressions embed as `${...}` STRINGS inside the JSON string values. If you can write and read this, the "what is this .tf.json file" question is settled.

### 3.2 Import CLI — the interview walkthrough, once more, tight

The panel shorthand that holds in every variant:

1. Write the resource block first — Terraform refuses import if the address is missing from config (verified live: "resource address does not exist in the configuration").
2. Get the provider's import ID for the object (cloud docs, or state from another source).
3. `terraform import <addr> <id>` — if the provider implements import, state gains the object (verified live with `time_offset`: "Import successful!").
4. Run plan — the diff between config and the adopted reality IS the review checklist.
5. Fix config until plan is clean, apply.

Every one of those five steps was exercised in TF.P0.2's lab — the JSON notes here are the syntax half, the CLI walkthrough is the operations half, and together they close the P2 gap without needing a cloud.

### 3.3 When precisely you hit JSON config in a job

- CDKTF emits `.tf.json` as its compiled output — running diff on a CDKTF stack means reading JSON config.
- Some export tools (drift scanners, config exporters) serialize existing state-to-config in JSON.
- Team-generated configs piped through `jq` end up as JSON by construction.

The one-line posture: "I view .tf.json as tool output — I keep humans on HCL." That split — machine-readable for machines, HCL for people — is a defensible engineering opinion to hold.

### 3.4 HCL vs JSON — the side-by-side that ends the confusion

| Aspect | HCL (`.tf`) | JSON (`.tf.json`) |
|---|---|---|
| Human-written | yes — intended audience | no — tool-generated |
| Comments | yes | no |
| Expressions | bare, `var.x` | embedded in strings, `"${var.x}"` |
| Blocks | `resource "t" "n" {}` | nested object keys |
| List attributes | `["a","b"]` | JSON arrays |
| fmt | rewrites/orders | validates consistency, different semantics |
| Validator | `terraform validate` | same validate |

The one-liner for a question: "HCL is for people, JSON is for compilers — Terraform treats both identically at plan/apply, so the risk in JSON is human illegibility and the expression-quoting gotcha, not functionality."

### 3.5 Import CLI flags worth naming

- `-state=<file>` — explicit state path for one-off multi-state setups (rare).
- `-provider=<provider>` — disambiguate when a resource type appears under multiple provider configs.
- `-var`/`-var-file` — applied for the import read, if the config needs them.
- `-allow-missing-config` — new-ish escape hatch that imports WITHOUT the block when you plan to add config later (still verify the follow-up plan).

Naming even two of these and the "config block needed first" rule differentiates you from candidates who have only read the flag list once.

### 3.6 Import + jq — the audit pipeline

State is JSON, so the natural pairing with import is querying what came in:

```bash
$ terraform import time_offset.day "..."
$ terraform state list | head
time_offset.day
$ terraform state pull | jq '.resources[] | select(.type=="time_offset") | .instances[0].attributes.day'
15
```

The whole post-import inspection is just `state pull | jq` pipelines (as run in TF.P0.2's verification). The interview line: "after import, I audit state the same way I audit anything else — pull it and jq it." It sounds obvious after someone says it, which is exactly why you should be the one to say it first.

### 5.5 Mock interview drill — the adoption plan (5 minutes)

Prompt: "An EC2 that predates Terraform is running in prod. It must become managed. Give the plan and one thing that can silently bite."

Answer: write the resource block, get the instance ID, `terraform import aws_instance.web i-0abcd…`, run plan. The bite: the post-import structure of attributes rarely matches the config exactly, so a plan that looks like massive changes means you adjust config (or, if the object is genuinely unwanted, `state rm`) until the desired diff is empty. Mention the two traps that make adoption fail in the opposite direction: importing without a config block (hard error) and importing a resource the provider doesn't implement (import-freeze).

Pass when the "first plan after import IS the review" is stated explicitly.

### 6. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Knows `.tf.json` is Terraform's JSON dialect | |
| 2 | Can name the `"${var.x}"` expression-quoting gotcha | |
| 3 | Knows when JSON config appears (tool-generated) | |
| 4 | Knows fmt/validate handle .tf.json | |
| 5 | Can restate import mechanics from TF.P0.2 | |
| 6 | Knows import fails without the config block first | |
| 7 | Knows per-resource import support varies | |
| 8 | Knows the post-import plan is the adoption review | |
| 9 | Can distinguish import vs state mv | |
| 10 | Knows CDKTF emits .tf.json | |
| 11 | Could explain why JSON syntax is not for hand-writing | |
| 12 | Can write a minimal resource in JSON from memory | |
| 13 | **SELF-VERIFY** — Re-explained import lifecycle (config → import → plan review) and the JSON gotchas with zero notes | |

Verdict: PASS when both concepts can be relaxed, precise, and defensible without docs in your hand.

Next session: TF.P2.2 — the managed vs self-hosted Terraform orchestration zoo.

---

## TF.P2.2 — Terraform Cloud vs Atlantis vs Spacelift

One-line focus: three ways to run Terraform with guardrails — manage vs self-host tells you who owns what risk, and there is no universal winner.

The interview wants to know you can compare *orchestration runners* by what they own: state+lock, plan/apply execution, approvals, policy enforcement, and drift detection. The right answer at 1–3 YOE is measured comparison, not a favorite. Model-only — nothing to run.

### 1. The three players

- **Terraform Cloud** — HashiCorp-managed. State, locking, remote plan/apply runners, policy (Sentinel) as code, workspaces, run history, and a free tier. The "default good enough" managed option, deepest for Terraform-native shops.
- **Atlantis** — open-source, self-hosted. Runs as a service that watches your git PRs: on a comment it runs plan/apply and posts the output under the PR. You run it on your own infra — the state backend remains YOURS (usually S3/whatever), with locking via that backend.
- **Spacelift** — third-party managed (SaaS or self-hosted modes). Policy as code (OPA), worker pools you can run inside your network, and broader IaC support than just Terraform. The "managed but swappable and opinionated" option.

### 2. The comparison a 1–3 YOE candidate should give

| | TF Cloud | Atlantis | Spacelift |
|---|---|---|---|
| Ownership | HashiCorp managed | Self-hosted OSS | Managed / self-hosted mix |
| State hosting | TF Cloud or your backend | Your backend always | Managed or your backend |
| Plan/apply runner | TF Cloud workers | Your service/runner | SaaS runners or your worker pools |
| Plan approval | Workspace/run-based | PR comment `apply` | PR + policy gate |
| Policy as code | Sentinel | none built-in | OPA |
| Drift detection | built-in run triggers / drift reports | DIY (scheduled plans) | built-in |
| Secrets | TF Cloud vars | Your CI/secrets store | managed / imported |

Interview-friendly framing: "Terraform Cloud is the managed HashiCorp lane (great DEFAULT) — Atlantis is self-hosted and git-native (you own runners and state, full control) — Spacelift is the managed-but-portable lane (policy as code, worker pools reach into your network)."

### 3. The decision axes that actually matter

1. **Who owns your runners?** Managed = less ops, external dependency. Self-hosted = control, your toil.
2. **Where does state live?** Self-hosted keeps state in your S3/bucket — managed options may host it for you — that is a compliance answer as much as a preference.
3. **How do approvals work?** Atlantis: human `atlantis apply` on the PR. TF Cloud: workspace run approval. Spacelift: policies + approvals.
4. **What about non-Terraform?** The broader your toolchain (Pulumi, CloudFormation, Ansible), the more Spacelift/Atlantis-with-extra-legs stretches — TF Cloud is Terraform-shaped by design.
5. **Policy enforcement before apply** — Sentinel (TF Cloud), OPA (Spacelift), or your reviewers (Atlantis).

The phrase that closes the question: "For a small team, TF Cloud free tier or Atlantis on a small box. For regulated/prod-heavy orgs, pick the one whose policy/approval/state story maps to your compliance checklist — and don't hand-wave the runner ownership."

### 4. What never changes across all three

No matter the runner: the plan/apply mechanics are Terraform's — the security invariants from TF.P1.2 still apply (no creds in code, scoped roles, plan artifact review) — drift still surfaces as a plan difference and needs the same reconcile decision (TF.P0.5). The orchestration layer is a management surface over an unchanged core.

That sentence is the whole reason this topic is P2: the async-pattern knowledge is transferable — the product zoo is table-flat.

### 5. Common pitfalls

- Recommending a favorite without asking "who hosts the runner, who owns the state, how do approvals gate?"
- Treating Atlantis as managed — it is not — you run it.
- Believing TF Cloud avoids Terraform fundamentals — it just adds CI and policy on top.
- Overweighting buzzwords (OPA!) without a compliance requirement.
- Assuming all three can drift-detect out of the box — Atlantis needs you to schedule it.

### 6. Interview Q&A

Q: TF Cloud vs Atlantis in one line?
A: TF Cloud is HashiCorp's managed Terraform CI + state + policy — Atlantis is self-hosted, git-PR-native automation where run approvals happen as PR comments.

Q: When would you pick Spacelift over TF Cloud?
A: When the org needs policy-as-code beyond Sentinel (OPA), wants to mix in non-Terraform IaC, or wants worker pools inside the network with a managed SaaS control plane.

Q: Do these change how Terraform works?
A: No — same providers, same state semantics, same plan/apply. They add orchestration, approvals, and policy on top of an unchanged core.

Q: What does Atlantis actually run?
A: A service that reads your VCS: on `atlantis plan` it executes plan and posts output under your PR — `atlantis apply` runs the saved plan against your backend. Your state and runner are yours.

### 4.1 Runner ownership as a decision driver

The interview-magnet diagram for choosing:

```
TF Cloud      →  managed control plane + managed runners      (least toil, least control)
Spacelift     →  managed control plane + YOUR workers         (toil on runners, policy power)
Atlantis      →  your control plane + your runners            (most toil, full control)
```

Say the tradeoff out loud: "each step left owns more infrastructure yourself — the question is what your risk and compliance posture requires you to own." For a regulated org, data-bearing state inside your VPC often forces Atlantis or Spacelift-with-workers — a startup typically wants TF Cloud's default speed.

### 4.2 Approval flows, side by side

- TF Cloud: run automatically at merge (or manual queue) with optional "plans require confirmation" toggles per workspace
- Atlantis: explicit `atlantis plan`/`atlantis apply` comments — the apply is a human-hot-triggered separate action
- Spacelift: PR-triggered runs with approval policies + review steps (approved applies, stack-level checks)

The phrase that predicts approval-flow answers: "plan is automatic and cheap — apply is the guarded step — who has authority to apply is the real product difference between these three."

### 4.3 When each makes the shortlist — worked example

A three-team org with a shared prod account: start Atlantis on one runner (self-host minimal), or TF Cloud free tier (zero ops). Once two concerns arrive — policy enforcement beyond review, and multi-tool IaC (Pulumi/CloudFormation alongside Terraform) — the evaluation tips to Spacelift or a deliberately-built TF Cloud + Sentinel estate. A panel that asks "which one do you pick" is really asking whether you can map tooling to constraints — the correct response starts with a question back: "what hosts your state today, and how much infra are we allowed to run for this?"

### 4.4 The never-cover-these-lines addition

Even on managed platforms, the defensible line is: "the product changes who coordinates plan/apply and policy — it does not change that Terraform's state is the source of truth for what is managed, and drift still needs the same reconcile discipline." That sentence is the whole P2 wrap-up: orchestration is a coat, not a different animal.

### 4.5 One scenario, all three answers

Constraints: two environments, three engineers, terraform-only stack, no sanctioned cloud-managed runners.

- TF Cloud answer: free tier, hash its workspaces, plan/apply inside a VCS integration, probing policies later. Least ops, external apply path.
- Atlantis answer: one small service — plan/apply comments in PR — state stays in your S3 — apply = human comment. Full control, your toil.
- Spacelift answer: SaaS control plane + your worker pool inside the network — policy-as-code gates closer to actual needs — more knobs than a 3-person team needs today.

The interview-relevant move is showing you can route the SAME requirement through all three and crisp the trade-off per choice — the decision structure, not the winner, is what's being tested.

### 4.6 The final table — one glance before the door

| Question | TF Cloud | Atlantis | Spacelift |
|---|---|---|---|
| Who hosts the control plane? | HashiCorp | you | vendor/SaaS or your workers |
| Who runs plan/apply? | vendor runners | your runner | vendor or your worker pool |
| Where is state physically? | vendor or your backend | your backend | vendor or your backend |
| Approval mechanism? | run-based toggles | PR comment `apply` | approval policies + review steps |
| Policy language? | Sentinel | (none built-in) | OPA |
| Non-Terraform IaC? | not really | not really | yes |
| Best fit | small teams, least ops | self-host purists, git-native | policy-heavy, multi-tool |

Read the table for one sentence and the product question is closed: "managed = fewer moving parts + a dependency on others — self-hosted = full ownership + your toil — and the state/plan/apply fundamentals are constants either way."

### 6.5 Mock interview drill — the tooling advisory (5 minutes)

Prompt: "A manager asks for one recommendation among TF Cloud, Atlantis, and Spacelift. What do you need to know before answering?"

Answer: ask three questions first — who must host runners/state (compliance constraint), how approvals are gated today (human comment vs managed run), and whether non-Terraform IaC is in scope. Then: small team + least ops → TF Cloud — self-host + git-native approvals → Atlantis — policy-as-code + multi-tool + either managed or worker-pool → Spacelift. Always close with the unchanged-core note: whichever you pick, plan/apply/state/drift fundamentals stand.

Pass when you can answer "what's your constraint?" before "which product?" — never a cheerleader.

### 7. QC checklist

| # | Check | Pass |
|---|---|---|
| 1 | Can give the one-line identity of each of the three | |
| 2 | Knows Atlantis is self-hosted and state stays yours | |
| 3 | Knows TF Cloud is HashiCorp-managed (Sentinel policy) | |
| 4 | Knows Spacelift does OPA/policy and non-Terraform IaC | |
| 5 | Can compare runners by state/lock/approvals/drift | |
| 6 | Knows core Terraform mechanics don't change under a runner | |
| 7 | Could advise a small team vs a regulated org differently | |
| 8 | Knows approval models per product | |
| 9 | Doesn't overstate Atlantis drift detection | |
| 10 | Remembers security invariants apply regardless of runner | |
| 11 | Can defend "no universal winner" | |
| 12 | Can pick a runner by the 4 decision axes | |
| 13 | **SELF-VERIFY** — Recited the three-line identity comparison and the 4 decision axes from memory | |

Verdict: PASS when the comparison is about ownership/approvals/policy, not product cheerleading.

---

## Session Log Summary

| Session | Topic | Priority | Status |
|---|---|---|---|
| TF.P0.1 | Core model: HCL, resources, plan/apply/destroy | P0 | **COMPLETE** |
| TF.P0.2 | State: file, import, mv/rm, locking, remote | P0 | **COMPLETE** |
| TF.P0.3 | Remote backends: S3/DynamoDB, team state | P0 | **COMPLETE** |
| TF.P0.4 | Plan/apply flags: target, var, refresh, parallelism | P0 | **COMPLETE** |
| TF.P0.5 | Drift detection + failure set + partial apply | P0 | **COMPLETE** |
| TF.P0.6 | count vs for_each vs for, dynamic blocks | P0 | **COMPLETE** |
| TF.P0.7 | Modules: structure, source, versioning | P0 | **COMPLETE** |
| TF.P1.1 | lifecycle, moved, prevent_destroy, ignore_changes | P1 | **COMPLETE** |
| TF.P1.2 | Terraform in CI: plan-as-gate, apply-on-merge | P1 | **COMPLETE** |
| TF.P1.3 | terraform console | P1 | **COMPLETE** |
| TF.P2.1 | JSON syntax / import CLI | P2 | **COMPLETE** |
| TF.P2.2 | TF Cloud vs Atlantis vs Spacelift | P2 | **COMPLETE** |

Sessions complete. The P0 core loop, state surgery, drift handling, list construct choice, and module composition are ready for whiteboard depth — P1 brings operational policy (lifecycle, CI, console) and P2 the reference facts. Final mastery test: open a blank page and redraw the state/config/reality triangle, the drift decision tree, and the count-vs-for_each trap from scratch — then re-verify each lab's outputs are still reproducible on /tmp/tfdemo.

## Final synthesis — the one-page Terraform story

If the panel lets you speak for five minutes uninterrupted, this is the arc:

1. **Desired state, declared** — HCL resources, providers, variables, locals, outputs (TF.P0.1).
2. **Source of truth** — state, local or remote, locked and versioned (TF.P0.2, TF.P0.3).
3. **Review flow** — plan is the artifact, apply consumes it, drift is the alarm (TF.P0.4, TF.P0.5, TF.P1.2).
4. **Scale by structure** — count/for_each/for for repetition, modules for composition (TF.P0.6, TF.P0.7).
5. **Operational intent** — lifecycle knobs and moved blocks express policy next to the resource (TF.P1.1).
6. **Tooling awareness** — console, JSON syntax, import CLI, and the runner platforms (TF.P1.3, TF.P2.1, TF.P2.2).

## The 10-minute mock — last drill before the interview

Pair this with a friend or a voice recorder: they hand you each prompt cold and you answer in under a minute.

1. "What does plan do, step by step?"
2. "Your teammate renamed a resource and now gets destroys. Diagnose and fix."
3. "What breaks when two applies collide on local state — and what's the fix?"
4. "Name a drift you'd converge, and one you'd import instead."
5. "The list shrank and half the fleet is being rebuilt. Why, and what do you change?"
6. "Guard a redshift cluster, ignore an autoscaler tag, and rename a module: what syntax?"
7. "Sketch plan-as-gate / apply-on-merge and name one pipeline failure mode."
8. "TF Cloud vs Atlantis vs Spacelift in three sentences."
9. "Console vs plan vs validate — when do you use which?"
10. "Convince me your answer on count vs for_each is grounded in a real plan you've seen."

Score yourself: any answer that ends in "I think" needs re-reading that session's QC row 13. Then run the whole P0.1 lab verbatim one last time and ship.

End of 08 — TERRAFORM.
