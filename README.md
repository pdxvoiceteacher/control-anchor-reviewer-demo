# Control Anchor reviewer demo

**OFFLINE EVIDENCE AND REVIEW COMPONENT DEMONSTRATION**

Private preparation candidate for review of Thomas Prislac's Sentient funding
application. The final publication decision and [candidate-specific contents
checks](PUBLICATION_REVIEW.md) are separate from merge authority. This repository
remains private and does not constitute a funding submission or public release.

This runs a small, existing part of Control Anchor: retain captured source,
prompt, settings and candidate bytes; execute deterministic evidence controls;
record a scripted review decision; preserve a linked repair; seal and verify
packages; export and reopen practitioner evidence. The Python implementation is
extracted unchanged from `pdxvoiceteacher/triadicbrain-open-alpha` at
`139932846cb1b6bf1571158464d89513d4e381f8`. See [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)
for exact original paths, Git blobs, SHA-256 hashes and adaptation notes.

The [methods appendix](docs/METHODS_APPENDIX.md) adapts the provenance pedagogy
into a synthetic teaching exercise and answer key. It distinguishes integrity,
claim support, review and bounded authority without claiming validated learning
or model training.

The [product map and customer-function crosswalk](docs/PRODUCT_MAP.md) show the
whole product's responsibilities, both interface directions and the exact
functions demonstrated here, with source elsewhere and proposed work marked.

All input records are conspicuously synthetic. **No model is called**:
`provider_invoked=false`. The candidate is an authored fixture. The actor
`SCRIPTED-DEMO-REVIEWER-NOT-THOMAS` exercises the decision API; its `APPROVE` records
are scripted, not Thomas's actual approval or an assurance conclusion.

## Run on Windows / PowerShell

Use an existing Python 3.12 runtime. No dependency installation or API key is
needed. The selected runtime uses the standard library, including the source's
closed local schema validator. `-S` disables site packages.

From this repository directory, if `python` already resolves to Python 3.12:

```powershell
$python = (Get-Command python -ErrorAction Stop).Source
& $python --version
& $python -S demo.py --output demo-output
& $python -S -m unittest discover -s tests -v
Get-Content .\demo-output\summary.json
Start-Process .\demo-output\review.html
```

On Thomas's workstation, the existing Codex runtime was used instead of the
Windows Store `python` alias:

```powershell
$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python -S demo.py --output demo-output
& $python -S -m unittest discover -s tests -v
```

Use a fresh output name for each run (for example `demo-output-2`). Existing
outputs are never overwritten. The filesystem must support ordinary NTFS-style
hard links for the implementation's atomic create-only publication. The initial
restricted sandbox denied this operation; the observed successful run used the
same Windows user outside that sandbox, without UAC elevation. See
[VALIDATION.md](VALIDATION.md). A denial is a failed run, not permission to replace
the publication mechanism or claim success.

## What to inspect

- `demo-output/summary.json`: directory and ZIP verification results, preserved
  parent bytes, export digests and the explicit tampered-copy rejection.
- `demo-output/store/packages/TX-SYNTHETIC-001/`: original/normalized source,
  raw candidate, prompt/settings manifests, 42 explicit control-result rows,
  review decision, custody chain, manifest and verification receipt.
- `demo-output/store/transactions/TX-SYNTHETIC-REPAIR/review/`: an **injected
  synthetic advisory finding**, its scripted selection and linked repair lineage.
  The harness uses the existing platform-observation API for this one fixture,
  following the upstream repair test. It does not claim AI discovery.
- `demo-output/store/packages/TX-SYNTHETIC-REPAIR-R1/`: separately captured and
  sealed child. Parent candidate/findings remain byte-identical; the lifecycle
  adds lineage records. `resolved_finding_ids=[]`: repair is not proven resolution.
- `demo-output/practitioner.json`, `.jsonl`, `.csv` and `review.html`: read-only
  projections. The runner rereads exported bytes and parses the JSON export.
  It also verifies retained directory/ZIP packages using the real verifier.
- `demo-output/tampered-disposable-copy/`: deliberately changed source bytes.
  Verification must reject this copy; the retained original must still verify.

For a separate CLI verification after the run:

```powershell
$env:PYTHONPATH = Join-Path $PWD 'src'
& $python -S -m triadicbrain.assurance.production_cli verify --package .\demo-output\store\packages\TX-SYNTHETIC-001.zip
```

## Where this fits

The Triadic Brain is the architecture for governed, cooperating AI workers;
Control Anchor is the intended local workbench for organization-defined control
analysis. In the full design, Sonya/AEGIS govern ingress and permitted exchanges,
UCC runs supported procedures, CoherenceLattice grounds and analyzes, Sophia
evaluates separately, Atlas explains and organizes eligible continuity, TEL links
performed stages, and custody retains authoritative records. Models are replaceable
workers; human and professional authority remains separately attributable.

This demo exercises the captured-output evidence/review seam in that architecture.
The source writes records named Sophia and Atlas but does **not** invoke the
separate CoherenceLattice, Sophia or Atlas implementations. `STANDARD_PROFILE`
contains **no semantic finding rules**. Its evidence-control PASS values concern
bounded recorded facts, not the truth of the attendance statement or observational
business-control classification. Other results, deferrals and open findings remain
visible; the 42-row catalog is not 42 proven effective business controls.

The intended locally governed Sophia network extends the vision toward cooperating
local instances, separately authorized exchange, review and continuity. This
candidate does not implement or activate that network, optional P2P, PMR or
federation. Live inference, installed startup and the full recurrent cognitive
loop remain separate product delivery work. The component demonstration preserves
that vision while bounding the evidence actually offered here.

**SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED.** Logical roles and a
hash chain are demonstrated; independent custody, OS isolation and cryptographic
signing are not. Read [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) and the
[PUBLICATION_REVIEW.md](PUBLICATION_REVIEW.md) HOLD checklist before redistribution.

License and attribution: [LICENSE](LICENSE), [LICENSE_SCOPE.md](LICENSE_SCOPE.md),
[NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[AI_ASSISTANCE_DISCLOSURE.md](AI_ASSISTANCE_DISCLOSURE.md).
