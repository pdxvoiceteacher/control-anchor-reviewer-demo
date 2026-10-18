# Control Anchor reviewer demo

Control Anchor is being developed to help organizations inspect the evidence
behind AI-assisted work and retain an attributable review history. Prospective
beneficiaries include small organizations, research teams and software builders
who need to examine and challenge AI-assisted work locally; user demand and
practical benefit have not yet been established.

This offline demo captures source, prompt, settings and candidate bytes, runs
deterministic evidence checks, records a scripted review, preserves a linked
revision, exports and reopens evidence, and rejects a deliberately modified copy.
**Synthetic inputs; no model is called. This is not the full live AI product.**

## Observed result and first steps

The recorded run used **Windows and Python 3.12.14**: **8 focused tests passed
in 18.957 seconds**, with **4 directory/ZIP verification checks**. Practitioner
JSON reopened with 133 evidence objects; the changed disposable copy was rejected
and the retained original verified afterward. These are bounded component results,
not an assurance opinion or proof of useful cognitive performance.

1. **Inspect without running:** read [VALIDATION.md](VALIDATION.md) and the
   [retained result summary](validation/observed-demo-summary.json).
2. **Run locally:** follow [Windows / PowerShell](#run-on-windows--powershell),
   using an existing Python 3.12 runtime and a fresh output directory. The two
   commands are `python -S demo.py --output demo-output` and
   `python -S -m unittest discover -s tests -v`. No dependency installation or API
   key is needed; the full quickstart explains runtime selection and hard links.
3. **Review the result:** open `demo-output/review.html`, inspect
   `demo-output/summary.json` and follow the [artifact guide](#what-to-inspect).

This repository is **private**. Public visibility and final contents require
the Project Lead's separate approval. Existing licenses and notices remain applicable;
no new media/prose license grant has been authorized. Adopting CC BY is not a
prerequisite for public visibility or funding eligibility.

## Reader routes

| Reader / purpose | Start here |
| --- | --- |
| Funders and prospective collaborators | [Funding and collaboration planning](docs/funding/README.md): an illustrative integration pilot, a smaller offline-tool scope and a university student intern opportunity, with the same evidence baseline. |
| Engineers | [Implementation/function crosswalk](docs/PRODUCT_MAP.md#actual-included-function-crosswalk), [focused tests](tests/test_component.py) and [exact source provenance](SOURCE_MANIFEST.json). |
| Academic collaborators | [Methods exercise and answer key](docs/METHODS_APPENDIX.md), [whole-product map](docs/PRODUCT_MAP.md) and [limitations](KNOWN_LIMITATIONS.md). No novelty or learning benefit is established. |
| Potential users | Run the local demo and inspect the human-readable review above; [product responsibilities](docs/PRODUCT_MAP.md) distinguish the intended workbench from this component. |
| Presenters | Optional [slides, scripts, teleprompters and covers](media/README.md), with dated evidence notes and source hashes. |

## Scope in one paragraph

The candidate is an authored fixture; `provider_invoked=false`. The actor
`SCRIPTED-DEMO-REVIEWER-NOT-THOMAS` records scripted decisions, not the Project Lead's actual
acceptance. The repair advisory is injected, not machine-discovered. Records named
Sophia and Atlas do not execute the separate cognitive components;
`STANDARD_PROFILE` has no semantic finding rules. Logical roles and a hash chain
do not establish independent custody, OS isolation, signing or factual correctness.
See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for the substantive boundaries,
including standalone ZIP verification.

The implementation is extracted unchanged from `pdxvoiceteacher/triadicbrain-open-alpha`
at `139932846cb1b6bf1571158464d89513d4e381f8`. The [source manifest](SOURCE_MANIFEST.json)
records original paths, byte identities, additions and modifications. The
[architecture context below](#where-this-fits) preserves the complete Triadic Brain,
Control Anchor and locally governed Sophia network vision while distinguishing
what this extraction actually demonstrates.

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

On the Project Lead's workstation, the existing Codex runtime was used instead of the
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
[PUBLICATION_REVIEW.md](PUBLICATION_REVIEW.md) candidate-specific notes before redistribution.

License and attribution: [LICENSE](LICENSE), [LICENSE_SCOPE.md](LICENSE_SCOPE.md),
[NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[AI_ASSISTANCE_DISCLOSURE.md](AI_ASSISTANCE_DISCLOSURE.md).
