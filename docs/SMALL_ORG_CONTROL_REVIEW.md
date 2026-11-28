# Small-organization control review: a reviewer’s route

The Triadic Brain is the local-first system for governed cooperation among AI
workers. Control Anchor is one part of its Workbench interface. This guide
uses fictional small-organization controls to illustrate the method. The runnable
purchase approval example is a supplied-field check, not the proposed pre-payment
workflow below or a definition of how the Brain must work.

## Inspect what runs today

From the repository root with an existing Python 3.12, follow the
[Windows/PowerShell quickstart](../README.md#run-on-windows--powershell).
Use a fresh output directory. The offline, standard-library demo uses
artificial source and candidate data, scripted review, and no model calls:

```sh
python -S demo.py --output demo-output
python -S -B ucc_demo.py
python -S -B approval_control_demo.py
```

Inspect the [generated summary, review and reopened packages](../README.md#what-to-inspect).
Compare the retained parent and linked revision, and check what happens to a
disposable copy with missing evidence. The UCC totals demo shows an unperformed
human procedure. The separate [approval example](../approval_control_demo.py)
checks a fictional purchase item, exact revision, explicit statement, and
declared calendar date on or before the fictional deadline (inclusive).

The statement check returns `PASS` for explicit approval, `FAIL` for a supplied
acknowledgment, and `HOLD` when the statement is absent. These are per-check
results on supplied data, not an overall authorization. Human review remains
`NOT_EXECUTED`; the example does not authenticate a signature, establish who is
authorized, or produce a joined report or reopen record. It does not execute
the pre-payment control below. [Recorded validation](../VALIDATION.md) is scoped
to its dated runs; a rejected adverse case is not a verifier PASS.

## Run a control and evidence you supply

The no-argument command above is a canned illustration. For a variable-input
run, save both of these as UTF-8 JSON files in a local scratch directory.
Use fictional data only in this public reviewer exercise.

```json
{
  "schema_id": "control-anchor.ucc-plan.v1",
  "plan_id": "LOAN-RETURN",
  "version": 1,
  "steps": [{
    "id": "DUE",
    "title": "Check return against approved deadline",
    "kind": "executable",
    "phase": "result",
    "operation": "date_order",
    "arguments": {"earlier": "/source/returned", "later": "/evidence/deadline"}
  }]
}
```

Save that as `plan.json`. Save your evidence as `context.json`:

```json
{"source":{"returned":"2027-02-09"},"evidence":{"deadline":"2027-02-09"}}
```

```sh
python -S -B approval_control_demo.py --plan plan.json --context context.json
```

Change the return date or the policy inputs, predict the effect, then run the
same command. Try a later return and a missing return field. The interpreter
computes `PASS`, `FAIL` or `HOLD` from the supplied values, not from a named
scenario. You can also author a different supported result-phase plan, such
as `number_range` against a quantity; see the
[bounded UCC implementation](../src/triadicbrain/assurance/ucc_plan.py) for the
operation set and arguments. Files are bounded to 256 KiB each. Unsupported
plans or invalid files return a CLI error, not a default answer.

The JSON result records the two exact input-file digests, the validated plan
digest, and each check's result and input bindings. Save a receipt locally
with shell redirection if desired. Those hashes identify what was supplied;
they do not authenticate the facts. This is a real local execution of the
public control component, not Workbench admission, an approved payment, a
peer/model run, a persisted audit trail, or evidence of a deployed Brain.

## Proposed real-runtime exercise: evidence before payment

A fictional community workshop adopts this criterion: before paying a
supplier invoice, an authorized reviewer other than its preparer must
compare the exact invoice revision against the purchase approval and
delivery evidence, and document any disagreement. For a later, separately
authorized exercise, invite a participant to bring a fictional transaction
and define the effective rule and eligible evidence. Observe the real
workflow; do not script an approval or a model answer.

- **Prepare:** The preparer links the invoice revision, purchase approval,
  and delivery record, with dates and identifiers that let the reviewer
  determine whether they apply. Acknowledging receipt of the invoice is
  not evidence that goods arrived, that the comparison occurred or that
  payment was authorized.
- **Review:** The separately authorized reviewer records the evidence
  checked and the reason for their finding. Include one incomplete or
  contradictory record. Distinguish a missing or unperformed check from an
  actual negative result. Do not assume that a correctly named file or a
  model recommendation settled the criterion.
- **Decide and reopen:** Record an attributable human disposition and any
  further decision the organization still owes. No payment need be sent.
  If corrected evidence is submitted, keep the original evidence and
  disposition and link the new revision and its review. Reopen the record
  to see which revision was reviewed and whether the evidence was
  available before the decision; opening it must not repeat that decision
  or initiate payment.

This exercise is proposed, not an observed result. The repository’s current
fixture does not establish an installed Brain, actual professional audit
assurance, organizational uptake, or live peer operation.
See the [whole-system design and evidence boundaries](TRIADIC_BRAIN_VISION.md).
