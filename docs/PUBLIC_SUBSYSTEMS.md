# Vetted public subsystems

This repository is a selective public projection of accepted development source.
It is not a mirror of the private repository or a distribution of the full product.
Completed, reviewed components can be useful and independently inspectable before
the complete installed workflow is qualified.

## Included today

| Component | Public entry point | What is demonstrated | Boundary |
| --- | --- | --- | --- |
| Evidence, custody and review | [demo.py](../demo.py) | Synthetic capture, scripted review, linked correction, export/reopen, adverse integrity checks and recovery | No model or separate cognitive component executes |
| Bounded UCC plan engine | [ucc_demo.py](../ucc_demo.py) | Declared deterministic procedures over supplied canonical data, with input bindings and explicit PASS/FAIL/HOLD/NOT_EXECUTED results | No source-truth, compliance, human approval, provider or installed-integration claim |

The UCC extraction adds two exact runtime modules from accepted development main:
[ucc_plan.py](../src/triadicbrain/assurance/ucc_plan.py) and
[ucc_primitives.py](../src/triadicbrain/assurance/ucc_primitives.py).
Their canonical-data dependency is already public and byte-identical. No private
Git history, operational evidence, personal data, credentials, models, installer,
service or provider configuration is imported. The prior reviewer-demo runtime
remains byte-identical; this is a separate runnable component, not a new integrated
reviewer workflow.

## Run the UCC component

Using an existing Python 3.12 runtime, from the repository root:

```text
python -S -B ucc_demo.py
python -S -B -m unittest discover -s tests -v
```

The example prints a matching total, a mismatching total, a missing-input HOLD,
section-presence checks and an unexecuted human procedure. It writes no files and
performs no network or model calls. PASS means only that the declared predicate
holds for the supplied values. It does not establish the accuracy of those values.

Supported operations are field presence, typed equality, decimal range, amount
comparison, total comparison, calendar-date order, required sections and literal
text containment. Plans admit at most 64 steps; total comparisons admit 2–16
distinct terms. Canonical context is bounded to 256 KiB. Unsupported operations,
unknown plan fields and paths outside admitted context reject rather than execute.
Human and advisory procedures remain NOT_EXECUTED.

Amount comparisons retain the reviewed precision repair: subtraction and total
calculation use a local precision of 96 for the accepted decimal domain. Tests
use a separate rational-number oracle. Precision and rounding changes in the
caller's Decimal context are covered; arbitrary exponent limits and traps are
not normalized or claimed safe. Supply ordinary Decimal context settings.

The exact upstream pytest cases are preserved in
[tests/upstream_ucc/test_ucc_plan.py](../tests/upstream_ucc/test_ucc_plan.py).
They are outside standard-library discovery because they require an existing
pytest installation. No package is bundled or installed by the demo. To run them
with an already available pytest environment, set PYTHONPATH to this checkout's
src directory and run pytest on that file plus
[tests/test_ucc_amount_precision.py](../tests/test_ucc_amount_precision.py).
For focused UCC-only unittest discovery, also set PYTHONPATH to src; the exact
upstream precision test does not modify the import path. The documented full
discovery command already loads the public package through the demo tests.
See [validation](../VALIDATION.md#ucc-public-extraction-3-november-2026).

## How accepted source reaches this repository

1. Select an exact accepted development commit and the component's real consumer.
   An open draft, source proposal or design description is not completed code.
2. Establish the minimal dependency closure and inspect applicable rights,
   attribution and privacy. Keep private records and unrelated source out.
3. Preserve exact source identities or identify every adaptation. Use the existing
   [source manifest](../SOURCE_MANIFEST.json), not a parallel status registry.
4. Run focused positive, adverse and compatibility tests in the public extraction.
   Distinguish source tests from installed, live-provider and human acceptance.
5. Independently review the public diff, notices and claims; publish a scoped PR,
   check its exact-head CI, then merge under the owner's delegated authority.

This is a contribution/review workflow, not an unattended export job. Future
promotions follow the same existing PR and manifest mechanism. Private drafts for
cognitive exploration, hypothesis retention, AHA and provider/service integration
are not included merely because they have code or isolated test evidence. The
broader [function map](brain-map/README.md) keeps development and proposals visible.

## Source and rights

Source pin: development main `ad4a0e94972a5fa12965cd2f394cce504655d78b`.
The amount repair was reviewed, focused-tested and merged before this extraction.
Exact copied file identities and their original paths are in SOURCE_MANIFEST.json.
The owner requested public promotion of completed vetted subsystems on
3 November 2026. Applicable existing MPL-2.0 rights and attribution are preserved.
The selected UCC adaptations have a bounded donor history described in
[third-party notices](../THIRD_PARTY_NOTICES.md#bounded-ucc-extraction-3-november-2026).
This publication does not relicense a donor repository or claim independent
verification of all title. No formal release, deployment or new license is created.
