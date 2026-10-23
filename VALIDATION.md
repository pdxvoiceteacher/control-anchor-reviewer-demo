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

## Public documentation update on 23 October 2026

Fresh isolated checkout from public main
`12bd38f7777cd6b1d5b329d69ebb616b8fee1e39`. The harness, tests, fixtures and all
33 copied extraction files remain unchanged. This update documents later
development evidence; it imports no private implementation or installer.

Environment: Windows-11-10.0.26300-SP0, existing CPython 3.12.14, `-S -B`,
standard library only, serial execution. The first sandboxed test attempt
returned exit 1: **11 setup errors in 0.135 seconds**, all at
`HOLD: EXCLUSIVE_OUTPUT_FAILED`. A separate hard-link probe returned access denied.
The failed log and partial fixtures remain in the isolated task directory.
No engine predicate or publication mechanism was changed.

One fresh test run outside the filesystem sandbox, using the same ordinary
Windows account, returned exit **0**: **11 tests in 49.680 seconds, OK**,
04:19:12–04:20:02 UTC. The [retained successful log](validation/2026-10-23-unittest.log)
contains the actual case results. No UAC elevation, dependency installation,
private software execution, provider/model call, listener or hosted CI was used.

The public repository has no package/build-system entry point. Its existing
`demo.py` generates the review HTML, evidence packages and exports. A separate
artifact-generation run, 04:20:44–04:21:01 UTC, returned exit **0**; the
[exact synthetic summary](validation/2026-10-23-summary.json) records:

- Six positive directory/ZIP verifications and **177 reopened evidence objects**.
- Both missing-source copies rejected at exit 3; retained originals PASS.
- Candidate self-authorization denied as authority, model-role decision denied,
  and missing human decision blocks sealing.
- One deliberate pre-seal decision interruption recovered once; second recovery
  leaves store bytes unchanged. This is not an OS crash test.
- Changed evidence rejected; parent candidate/findings preserved and
  `resolved_finding_ids=[]`. No AI-discovered correction or real human acceptance.

Commands from the public checkout, with a fresh sibling validation directory:

```powershell
$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:REVIEWER_TEST_ROOT = (Resolve-Path '..\validation-20261023-02\test-fixtures').Path
& $python -S -B -m unittest discover -s tests -v
& $python -S -B demo.py --output '..\validation-20261023-02\demo-run'
```

Generated stores, exports, partial failures and private upstream evidence remain
outside this public checkout. Only the successful public test log and synthetic
summary are added. Historical logs, results and HOLD fields are preserved.

Opening that exact generated `review.html` in a new Chrome tab was **denied**:
the browser URL policy permits HTTP(S), not local-file URLs. No tab opened or
workaround was attempted. **Rendered visual QA remains unperformed.** HTML source
inspection is separate from rendering and does not qualify accessibility.
The two added evidence links resolve locally and no script or external resource
is present. Inherited application navigation links use server-root routes; those
routes are not exercised by opening this standalone report. No server was started.

Documentation links, manifest hashes, copied-file identities, the changed-file
scope and public disclosure boundaries are checked for this successor. CI233's
upstream archive was inspected as data, separately from these public-only runs;
its installation result does not transfer to this extraction or the Project
Lead's PC. See the [dated evidence limits](docs/PRODUCT_MAP.md#evidence-edition-and-remaining-joins).

## Roadmap draft validation on 23 October 2026

This follow-up starts from public commit
`a4a1fd41637ee2b15beaded5a1aec17484bc8590`. The public implementation, tests,
fixtures and all 33 copied extraction files are unchanged. The proposed roadmap
uses the owner's explicit brief and verified repository evidence. The separate
design packet and diagrams were not locally inspected or imported. Public tests
do not qualify the proposed executive, learning, prior-storage or network behavior.

On the same Windows/CPython 3.12.14 environment, one fresh serial run of
`python -S -B -m unittest discover -s tests -v` returned exit **0**:
**11 tests in 49.374 seconds, OK**, 06:56:26–06:57:16 UTC. The
[new retained test log](validation/2026-10-23-roadmap-unittest.log) records the
actual results. The run used the already established ordinary-user hard-link
environment outside the filesystem sandbox; no protection in the public engine
was disabled.

A separate `python -S -B demo.py --output <fresh-output-directory>` artifact build,
06:57:16–06:57:33 UTC, returned exit **0**. It verified six directory/ZIP packages,
reopened 177 evidence objects and retained the expected adverse/recovery results.
Its synthetic summary is byte-identical to the [existing public summary](validation/2026-10-23-summary.json),
so no duplicate summary is added. The repository has no package build-system
entry point. Generated trees and command logs remain outside the public checkout.

The earlier local-file browser denial is respected; no alternate server or
browser route was used to open that generated file. Demo rendering remains
**unperformed**. HTML source/link inspection is separate from rendering.
No private project software, hosted CI, installation, provider activation,
model call, training, listener or dependency installation ran for this patch.

Existing upstream success and failed-gate artifacts were read as data. Their
digest/CRC/indexed-file checks and source-specific results inform the dated
product map, without adding private source identities or operational payloads.
An earlier installed success and a later failed source gate retain their own
meaning; neither transfers qualification to changed source. The newest scoped
success also preserves those failures and all unperformed product stages.

Final prose/provenance adjustments changed no runtime, test or fixture bytes.
Affected manifest, link and scope checks were rerun; the recorded test/build
results above are preserved rather than presented as a new execution.
