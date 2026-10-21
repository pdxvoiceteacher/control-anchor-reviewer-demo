# Observed local validation — 18 October 2026

Scope: this extraction and its synthetic fixtures only. Windows, existing bundled
CPython **3.12.14**, serial execution, `-S` (site packages disabled). Pytest was not
available; none was installed. No model, GPU task, application installation,
background service or hosted CI run was used. One positive test replaces
`socket.socket` with a rejecting test guard; that is a Python test precaution,
not OS isolation evidence.

The source manifest records 33 exact copied files: 20 Python modules, 12 schemas
and LICENSE, totaling 653,223 bytes. Each copied file's computed Git blob matched
the authenticated source-tree identity. No product implementation was modified.

## Demo run

The exact command used the existing runtime under the user's profile:

```powershell
$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python -S demo.py --output demo-output-ordinary-user
```

Observed exit code: **0**. Both `TX-SYNTHETIC-001` and
`TX-SYNTHETIC-REPAIR-R1` verified PASS as directories and ZIPs. Parent candidate
and findings remained unchanged; resolved finding IDs remained empty. The runner
wrote and reread practitioner JSON/JSONL/CSV, parsed 133 JSON evidence items,
and rendered a local HTML view. These are evidence objects, not 133 controls or
an audit sample. The deliberately changed directory copy returned exit code 3:
`HOLD: PACKAGE_MANIFEST_MEMBER_BINDING_INVALID`. The retained original verified
PASS afterward. See [validation/observed-demo-summary.json](validation/observed-demo-summary.json)
for the actual result and export digests. Run roots remain local and Git-ignored.

## Focused tests

```powershell
& $python -S -m unittest discover -s tests -v
```

Final observed result: **8 tests, 18.957 seconds, OK, exit code 0**. Cases cover
CLI capture/seal/directory+ZIP verification, missing decision rejection, model-role
decision denial, candidate self-authorization rejection, preserved repair lineage
and duplicate-child rejection, declared-change mismatch, tampered ZIP member
rejection, and the live snapshot's changed-ZIP detection.

The successful demo/test runs used the same ordinary Windows user outside the
filesystem sandbox; no UAC or administrator elevation was used.

## Original failures retained

1. Initial `-S demo.py --output demo-output` inside the restricted filesystem
   sandbox failed at store initialization: `EXCLUSIVE_OUTPUT_FAILED`, caused by
   `os.link` returning WinError 5 (access denied). No transaction completed.
   Partial output was retained. The successful ordinary-user run used a fresh
   output root outside that sandbox, with the implementation's publication
   mechanism unchanged.
2. Initial seven-case unittest run returned exit code 1: six passed, one failed
   in 14.714 seconds. The authored adverse test incorrectly expected the standalone
   ZIP verifier to reject appended trailing bytes. Source review and execution
   showed that standalone verification checks members while the actual live
   transaction snapshot binds exact deterministic ZIP bytes. The test was replaced
   by an explicit member-tamper rejection case and a separate live-consumer case
   documenting standalone acceptance plus incomplete live terminal evidence.
   This is a disclosed boundary, not an implementation repair or erased failure.

These results do not qualify installed startup, live AI, separate cognitive
components, independent custody/signing, production scale, all source tests,
another interpreter or the full product. Public-release review remains HOLD.

## Focused update — 21 October 2026

New execution on Thomas's connected Windows computer, distinct from the historical
eight-test run above. Clean task checkout began at reviewer main
`394b042511f970d3dfcebab947a20cc89c868a1f`; no existing checkout was modified.
No applicable `AGENTS.md` was present in this repository or task ancestors.
The 33 copied extraction files (20 runtime modules, 12 schemas and LICENSE) remain
byte-identical at source `139932846cb1b6bf1571158464d89513d4e381f8`.

Environment: **Windows-11-10.0.26300-SP0**, AMD64, existing bundled **CPython
3.12.14**, MSC v.1944 64 bit, `-S -B`, standard library only, serial execution.
The runs used the same ordinary Windows account outside the filesystem sandbox
so the engine could use its existing create-only hard links. No UAC elevation,
dependency installation, provider/model call, listener, hosted CI or full-product
installation was involved. The end-to-end test rejects Python socket creation;
this is a test guard, not OS isolation. Fixture logical times are synthetic and
are not the wall-clock execution times.

From the fresh checkout, the exact commands (profile path expressed portably) were:

```powershell
$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
New-Item -ItemType Directory -Path '..\validation-20261021-01','..\validation-20261021-01\test-fixtures' | Out-Null
$env:REVIEWER_TEST_ROOT = (Resolve-Path '..\validation-20261021-01\test-fixtures').Path
& $python -S -B -m unittest discover -s tests -v *> '..\validation-20261021-01\unittest.log'
& $python -S -B demo.py --output '..\validation-20261021-01\demo-run' *> '..\validation-20261021-01\demo.log'
```

Both commands exited **0**. Tests ran 04:36:02–04:36:53 UTC: **11 tests in
50.592 seconds, OK** ([retained log](validation/2026-10-21-unittest.log)). The
separate demo ran 04:37:20–04:37:37 UTC and produced the
[new exact summary](validation/2026-10-21-summary.json). The local task directory
retains all test fixtures, the demo store, disposable adverse copies, the actual
interrupted journal, exports, HTML and command logs. No failed new test/demo run
was discarded; both first executions passed. Those generated trees are outside
the public checkout. Only the synthetic summary and test log are committed.

- **Six positive directory/ZIP verifications:** captured original, linked child
  and recovered decision transaction all PASS. JSON/JSONL/CSV were written and
  reread; JSON reopened **177 evidence objects**, not the historical 133.
- **Missing evidence:** separate directory and ZIP copies omit
  `source/original.bin`. Both real CLI consumers return exit **3** /
  `HOLD: PACKAGE_TOPOLOGY_INVALID`. Both retained originals remain PASS.
- **Authority:** candidate APPROVE text remains data; model-role decision raises
  `AUTHORIZATION_DENY_BY_DEFAULT`; missing decision returns exit **3** /
  `HOLD: TRANSACTION_NOT_FINALIZABLE`. The adverse transaction stays pending,
  has no human decision or directory/ZIP package and retains identical bytes.
- **One bounded recovery:** public `submit_human_decision(...,
  fault_after_target=1)` raises exact `TransitionInterrupted` after
  `review/human_decision.json`. State and custody remain at the pending before-image;
  the actual journal is retained separately before recovery. Public
  `recover_pending_transition` reaches APPROVED with exactly one decision
  transition and one SYSTEM-RECOVERY event bound to the matching receipt and
  original journal digest. Source, candidate and decision bytes are preserved.
  A second call returns `NO_PENDING_TRANSITION`, `recovered=false`, with identical
  store file digests. Sealing then succeeds; directory/ZIP verification and live
  terminal completeness pass. This is deliberate synthetic pre-seal fault
  injection, not an OS crash. The engine's `UNOBSERVED_PROCESS_INTERRUPTION`
  posture does not establish root cause or general crash recovery.
- **Other retained boundaries:** the authored breakdown advisory remains OPEN
  with `resolved_finding_ids=[]`; parent bytes are preserved. Altered-directory
  and ZIP-member copies are rejected. The existing trailing-byte test confirms
  standalone ZIP acceptance while the actual live snapshot reports incomplete
  terminal evidence. No verifier or engine predicate was changed.

`review.html` now begins with readable adverse/recovery observations and links to
the exact local summary and interrupted journal. HTML source checks found the
expected section and local links, with no script or external resource added.
Opening this exact local file in **Thomas's Chrome browser** was **denied** by
the browser URL policy: only HTTP(S) protocols were allowed. No tab was opened,
no server was started and no workaround was attempted. **Rendered visual QA is
unperformed**; source inspection is not a browser render.

The update helps people inspect and correct work; it supplies no worker scoring
or employment monitoring. These results establish neither AI-discovered errors,
independent assurance, actual human acceptance nor a live/installed product.
Historical results, HOLD fields, failures, source attribution and license scope
remain intact. Upstream installation/provider/P2P milestones are separately dated
in [the product map](docs/PRODUCT_MAP.md#evidence-edition-and-remaining-joins).
