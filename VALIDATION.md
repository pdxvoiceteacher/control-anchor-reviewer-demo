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
