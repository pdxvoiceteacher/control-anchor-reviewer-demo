# Observed local validation — 18 October 2026

**Current documentation note — 29 October 2026:** the
[new development summary](docs/DEVELOPMENT_UPDATE_2026-10-29.md) separates private-alpha
observations from this public component. Runtime, tests and fixtures are unchanged;
no demo/test rerun or hosted CI is claimed for this documentation update. Historical
results below remain bound to their original dates, source and environment.

The existing lightweight checker, `python -I -S -B tools/check_public_integrity.py`,
passed for **93 manifest-bound files**, copied source identities and local Markdown
destinations/anchors. The documentation diff also passed `git diff --check`.
These checks do not execute the demo or certify external links, rendering,
private-alpha behavior or product readiness.

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

## Automated public checks

The [demo workflow](.github/workflows/demo.yml) runs the public unittest suite and
`demo.py` artifact build on standard Ubuntu 24.04 and Windows 2022 runners with
Python 3.12. The [integrity workflow](.github/workflows/integrity.yml) runs the
gate's positive/adverse tests, then [the offline checker](tools/check_public_integrity.py).
It checks every tracked file against the manifest (except the self-referencing
manifest), copied SHA256/Git-blob identities, file sizes, and local Markdown
destinations/anchors. Fenced and inline code examples are excluded from link checks.
External URLs, including private provenance links, are not fetched. This small
checker is not a full Markdown renderer or a security audit. A maintainer can
change source and its declarations; commit/review provenance remains separate.

Jobs have 10-minute demo and 5-minute integrity timeouts and cancel superseded
runs of the same workflow/ref. Both workflows have only `contents: read`, do not
persist checkout credentials, and use full action commit pins verified against
the official checkout v7.0.1 and setup-python v7.1.0 release tags. No repository
secret inputs, project dependency installs, model calls, artifact uploads or Actions caches are
configured. GitHub's automatic read-only token serves checkout/runtime acquisition.
Only standard GitHub-hosted runners in this public repository are used; see
[GitHub's public-runner billing policy](https://docs.github.com/en/billing/concepts/product-billing/github-actions).
No billing, permission or branch-protection settings are changed.

The README badges link to these two actual workflows on `main`. A badge reflects
its latest selected branch run, not every historical commit. Use the run's source
SHA, platform/job outcome and logs; failed, cancelled, skipped and unrun jobs do
not become PASS. Historical results above and all extracted source identities
are preserved. CI neither installs the full product nor resolves the unperformed
packet inspection, rendered demo QA or live-provider/human-acceptance limits.

## UCC public extraction: 3 November 2026

The exact two runtime modules and two tests are copied from accepted development
main `ad4a0e94972a5fa12965cd2f394cce504655d78b`. Git blob identities were verified:
`ucc_plan.py` ac943825f6acfa104520ba703442bbce932a8d3f;
`ucc_primitives.py` ab85ef3dc4cea040fe26bc821be0add9795580d8;
upstream plan tests 4ac806d0b7546f5aca0a7e93efcb9d5c1af4f8b0;
precision tests c11a61bfc742e4e84d07c418987d7c6e30442b1a.
The existing canonical dependency is unchanged and matches development main.

Executed in a Linux Python 3.12.14 public checkout, without installation,
provider/model contact or paid spending:

- `python -S -B ucc_demo.py`: completed; synthetic total and sections PASS,
  wrong total FAIL, absent total HOLD, human review NOT_EXECUTED.
- `python -S -B -m unittest discover -s tests -v`: **26 tests passed**,
  including the previous component/navigation/integrity tests and four UCC
  test methods. [Retained output](validation/2026-11-03-ucc-unittest.log).
- Existing approved pytest 9.1.1 environment, plugin autoload and cache disabled,
  PYTHONPATH set to this checkout's src: `python -B -s -m pytest -q -p no:cacheprovider tests/upstream_ucc/test_ucc_plan.py tests/test_ucc_amount_precision.py`:
  **46 tests and 77 subtests passed**, exit 0. These overlap the precision methods
  above and must not be added to the 26 as independent coverage.

The precision oracle covers 72 valid comparisons across three precisions and
three rounding modes, plus five invalid inputs. It does not normalize arbitrary
Decimal exponent limits or traps. Focused success establishes supplied-field
behavior, not source truth, human acceptance, installed Windows behavior,
performance, full-product integration or a formal assurance opinion. No private
run evidence or history is published. Public CI reports its own exact-head results.

## Retrosynthesis public extraction: 3 November 2026

This second projection starts from public main e33da6cb. The accepted private
source pin remains ad4a0e94972a5fa12965cd2f394cce504655d78b. The leaf blob is
e9854000b7ed113028fd626458698cdea42070ee; exact upstream test blob is
4331aa4fb31ea59aac436f94c9f783c3b3a27ee1. The complete ordinary import closure,
schema pairs and Unicode license are bound in SOURCE_MANIFEST.json, not replaced
by stubs or satisfied by a private sibling installation.

Preparation history is retained distinctly: an initial materialization attempt
lacked the three source-parity schema files and stopped. The subsequent attempted
pytest command found no relocated test file and ran zero tests. Exact missing
schema bytes were fetched and identity-checked before successful qualification.
After the module-origin hook was added, one independent run executed all 74 cases
but failed at session finish because new source-manifest entries were not yet
finalized. That guard failure is not counted as a successful run. The completed
manifest and final identity-checked run below supersede those preparation gaps.

Local qualification uses existing Python 3.12.14, jsonschema4.26.0 and pytest9.1.1
on Linux, without package installation, live model/provider/network invocation,
native service or paid spending. The unchanged 73 upstream cases passed before
the public demo was added. The demo adds one test, yielding 74 selected cases.
The final focused command is `python -B -s -m pytest -q -p no:cacheprovider tests/upstream_retrosynthesis`
with plugin autoload disabled. Imported project-module identities are checked
against the public manifest at session finish. Final result: **74 passed**, including all 73 unchanged upstream cases, and
**29 imported project modules** matched the public manifest. The existing
standard-library suite separately passed all **26 tests**. These counts cover
different selected paths; they do not imply whole-product qualification.
Exact final output is retained in
[the extraction log](validation/2026-11-03-retrosynthesis-pytest.log).

The synthetic demonstration exercises the real Coherence grounding/proposal
validator and Sophia reconstruction consumer, returning all five comparison
dispositions with authority NONE, human decision PENDING, interpretation
NOT_ESTABLISHED, and no lookup, retention, context delivery or dispatch.
Permits/reports remain synthetic. This does not establish full Sophia evaluation,
actual grants, native COMPARE custody, durable memory, installed behavior, source
truth or full cognitive-loop acceptance. Support modules included for ordinary
imports are not all behaviorally qualified by these selected tests.

The existing bounded public CI job separately installs the optional pinned test
requirements and executes this suite and demonstration on its Linux/Windows
matrix. Consult exact commit CI for its outcome; local source results are not
represented as installed or cross-platform proof before those checks finish.

### Public CI workflow parsing correction

The first public candidate at `70c257b8f3f723402e4dd18eace48cd50cc38027` failed before starting any demo jobs: [workflow run 41733828844](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/actions/runs/41733828844). A local YAML parser reproduced the syntax error at the unquoted colon-space sequence in the pip `--only-binary=:all:` command. The correction expresses that unchanged command as a YAML block scalar. This failed attempt is not a test pass. Exact-successor CI must run the Ubuntu and Windows suites before merge.
