# Bounded retrosynthesis comparison

This public component compares explicitly supplied hypotheses and checks their
retained source references. It uses the real extracted Coherence grounding and
reconstruction functions, and the real Sophia reconstruction check. It does not
generate hypotheses with a model, authenticate grants, retain memory, insert
provider context or dispatch work.

The accepted development leaf and its original 73-case test are copied exactly.
The extraction includes their full ordinary Python import closure, including real
package initializers. No replacement initializer, stub validator or skipped Sophia
consumer makes the demonstration pass.

## Run the demonstration

Use Python 3.12 or later and an existing environment with jsonschema 4.26.0:

```text
python -B -s retrosynthesis_demo.py
```

The example is fully synthetic. It prints five distinct results: exact duplicate,
related hypothesis, declared reference-role conflict, unknown comparison and
needs-test. Missing original origin stays missing. Declared counterevidence,
unperformed tests, PENDING human decision and NOT_ESTABLISHED interpretation
remain visible. The separate Sophia function recomputes the retained projection;
this is a reconstruction check, not the entire Sophia evaluation or an independent
human review.

If the dependency is not present, the script stops with an explanation. It never
installs packages automatically. If you choose to prepare a separate environment:

```text
python -m venv .venv-retrosynthesis
```

On Windows, use `.venv-retrosynthesis\Scripts\python.exe`; on Linux/macOS use
`.venv-retrosynthesis/bin/python`. With that interpreter, install the optional
[runtime requirement](../requirements-retrosynthesis.txt) using
`-m pip install -r requirements-retrosynthesis.txt`, then run the demonstration.
The original evidence and UCC demos remain standard-library-only and need no
additional package. Do not use `-S` for this optional component: it intentionally
uses the separately installed jsonschema package.

## Reproduce the focused qualification

With the chosen interpreter, install the optional
[test requirements](../requirements-retrosynthesis-tests.txt) if needed, then:

```text
python -B -s -m pytest -q -p no:cacheprovider tests/upstream_retrosynthesis
```

Set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` in the test environment to keep unrelated
installed pytest plugins out. The local conftest selects the three public import
roots and checks every imported project module against SOURCE_MANIFEST.json at
session end. A sibling checkout or installed private package cannot silently
satisfy a missing extraction dependency. The unchanged upstream test still runs
real Coherence, Sophia and PMR pure consumers. Test permits and commit reports are
synthetic inputs, not actual credentials or persistence receipts.

The existing public CI performs this focused suite and demonstration on Linux and
Windows, alongside the original standard-library suite. Consult each commit's CI
results; a historical pass does not qualify every later edit. Local extraction
results and the initial preparation failure are in
[VALIDATION.md](../VALIDATION.md#retrosynthesis-public-extraction-3-november-2026).

## Exact dependency boundary

The selected closure contains 45 production Python files, including three already
present in the public repository, plus the exact upstream test. Coherence's normal
totality initializer imports its adapter, AHA, aperture, claims, counterexamples,
grounding, PMR, request, seal, TEL and UCM modules; these also require AEGIS and AHA
package imports. Sophia's real reconstruction function imports its audit module.
Those files are dependency support, not a claim that every exposed helper or
broader subsystem has been publicly qualified by this test selection.

Three packaged schemas and their three byte-identical source copies are present
so the existing resource and source-parity checks operate normally. The two source
trees remain under their original components paths. Exact paths, source commit,
Git blobs, hashes, sizes and import edges are recorded in the existing
[source manifest](../SOURCE_MANIFEST.json).

The only additional runtime package is jsonschema 4.26.0 and its own dependencies.
pytest 9.1.1 is a test dependency. No dependency wheel, model, provider adapter,
Atlas implementation, native custody service, operational record or private Git
history is copied. Applicable MPL-2.0 and Unicode V3 notices are preserved in
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md#retrosynthesis-dependency-slice-3-november-2026).

## What remains outside this component

The comparison leaf is opt-in and receives at most 16 explicitly selected priors.
Each retained proposal, source and grounding input is bounded to 16 KiB. It checks
supplied organization/application/task/reference/purpose/time bindings, but those
fields are assertions from its caller. They do not authenticate an issuer.

Native COMPARE custody, actual current grants and revocation, durable references,
restart/recovery, provider-context delivery, installed use and human acceptance
remain separate work. No automatic learning, source truth, semantic contradiction,
independent corroboration, global novelty, clinical judgment or professional
assurance is established. The full cognitive loop remains development work.
