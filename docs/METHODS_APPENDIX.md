# Methods appendix: teaching evidence boundaries

**Private reviewer candidate. Public visibility awaits the final-content decision.**

This appendix adapts Thomas Prislac / UVLM's provenance pedagogy into one exercise
for the [offline component demo](../README.md). Its merit here is an inspectable
way to practice distinguishing a retained artifact, a supported claim, a review
and an authorized consequence. Novelty and educational effectiveness have not been
validated. This is not model-weight training, improved-intelligence evidence or
a measured reduction in hallucination. No learner report, user conversation,
live record, training ledger or credit-scoring implementation is included.

## Source and adaptation boundary

- **S1:** [UVLM Provenance Pedagogy v1.0.0, CoherenceLattice](https://github.com/pdxvoiceteacher/CoherenceLattice/blob/f0566d8f79c308eaeb9ab10cb8255478e8913a71/docs/provenance/pedagogy/UVLM_PROVENANCE_PEDAGOGY_v1.md),
  commit `f0566d8f79c308eaeb9ab10cb8255478e8913a71`.
- **S2:** [UVLM Provenance Pedagogy Refinement Overlay v1.1, Sophia](https://github.com/pdxvoiceteacher/Sophia/blob/36165bdca0c5fbdc58d7500c41af6c9fd775197c/docs/provenance/UVLM_PROVENANCE_PEDAGOGY_REFINEMENT_OVERLAY_v1.1.md),
  commit `36165bdca0c5fbdc58d7500c41af6c9fd775197c`.

This is a scoped paraphrase with a new synthetic exercise, not a copy of either
curriculum or an adoption of all its rules. Exact document paths, Git blobs and
artifact-byte SHA-256 hashes are recorded in [SOURCE_MANIFEST.json](../SOURCE_MANIFEST.json).
The source documents state no authority or release effect. No applicable license
grant was identified in these documents or a repository license file at the
inspected snapshots. The candidate's [license scope](../LICENSE_SCOPE.md) does not
establish upstream title or relicense those sources. Thomas's ownership attestation
and instruction to include methods support this private adaptation. Preserve
applicable existing rights and attribution as described in
[PUBLICATION_REVIEW.md](../PUBLICATION_REVIEW.md). No new prose license is granted,
and a new CC BY grant is not a prerequisite for visibility or funding eligibility.
Merge authority does not itself change repository visibility.

## Method: inspect, challenge, decide within scope

S1 distinguishes byte identity from meaning, production history from evidential
sufficiency, and review from permission. An unchanged artifact can contain a false
claim. A well-recorded lineage can trace an unreliable source. An auditor may
challenge the evidence without owning or rewriting the subject. A human decision
can authorize one declared consequence without certifying truth or authorizing
unrelated retention, publication or deployment.

S2 makes these distinctions operational through separate evidence dimensions:

| Dimension | Ask in this demo |
| --- | --- |
| Byte integrity | Do retained source/candidate bytes match their recorded digests? |
| Lineage completeness | Can the captured input, scripted review and repair child be traced? |
| Source independence | Are these independent observations, or records from one synthetic harness? |
| Epistemic support | Which exact source statement supports the proposed conclusion? |
| Authority clarity | Who actually made a decision, for which consequence? |
| Privacy and consent | Are the inputs synthetic, and would real inputs have permitted use? |
| Operational usefulness | Can a reviewer reopen and understand the evidence and its limits? |

Do not combine these into a legitimacy score. Strong integrity does not repair
weak semantic support, and incomplete lineage alone does not prove a claim false.
Keep disagreements beside the relevant evidence: state the disputed premise,
counterexample, uncertainty and proposed correction. Dissent can improve the
method while work continues toward the authorized outcome; it grants no extra
authority. Preserve original evidence and attribute any later adopted conclusion.

A false positive flags a problem that the chosen evidence does not support; a
false negative misses a relevant problem. Assess them against the specific claim
and consumer being checked. An environment or validation-driver failure invalidates
that evidence segment; a green helper check cannot stand in for an unexercised
product entry point. Preserve failures, repair the implicated check and inherit
only unaffected evidence. No error-rate improvement is measured here.

This appendix **does not adopt S2's refinement 10 patch-count shortcut**. Three
patches without an observed mismatch are insufficient grounds to retire a
control. Review its protected consequence, actual coverage, failure sensitivity,
cost and continuing usefulness; preserve required security, privacy and authority
protections. No control is retired by this documentation.

## Synthetic teaching exercise

Use the existing [PowerShell quickstart](../README.md#run-on-windows--powershell)
once in an eligible environment, or inspect the retained
[observed summary](../validation/observed-demo-summary.json). No additional runtime
is needed for this appendix. All proposed assertions below are authored teaching
inputs, not machine-discovered findings.

Read [source.txt](../fixtures/source.txt), [candidate.txt](../fixtures/candidate.txt),
the injected [advisory](../fixtures/advisory.json), the scripted
[approval rationale](../fixtures/approve.txt) and [repair rationale](../fixtures/request-repair.txt).
Then answer:

1. What supports "20 session attendances"? Would a package PASS support the
   counterfactual assertion "20 unique people attended"?
2. If a reviewer flags the actual candidate as claiming 20 unique people, what
   kind of error is that? If a reviewer accepts the counterfactual solely because
   controls passed, what problem could be missed?
3. Was the advisory discovered by Sophia or an AI? Does the recorded APPROVE
   establish Thomas's acceptance, publication permission or finding resolution?
4. Inspect the parent candidate/findings, repair lineage and child package. What
   is preserved, what is added, and what remains unresolved? Name one defensible
   dissent and one bounded human decision that could follow this exercise.
5. What do the tampered-copy rejection and practitioner reopen establish? Name
   one important claim neither establishes.

## Answer key

1. The synthetic source records session counts 12 and 8; their arithmetic sum is
   20 attendances. Unique-person overlap is unknown, as the actual candidate says.
   A package PASS verifies bounded evidence conditions, not the counterfactual's
   meaning or real-world attendance. `STANDARD_PROFILE` has no semantic finding
   rules, and the source itself is an authored fixture.
2. The first flag is a false positive against the actual candidate: inspect its
   words before attributing the counterfactual to it. Accepting the unsupported
   unique-person assertion is a semantic false negative. Passing evidence controls
   do not establish that such an assertion was checked. These are illustrative
   error cases, not measured test rates or a new automatic classifier.
3. The harness injects the advisory through the existing platform-observation
   API. The demo invokes no separate Sophia implementation or provider. Its
   reviewer identity and decision are scripted fixtures, not Thomas's actual
   acceptance. They grant no publication permission and do not resolve the issue.
4. Original parent candidate/findings bytes remain unchanged. Linked child and
   lifecycle records add the declared candidate change; the parent advisory stays
   open and `resolved_finding_ids=[]`. A defensible dissent is "a clearer child
   summary does not prove independent attendance or closure of the advisory."
   An actual authorized human could decide to request a separately evidenced
   revision for this synthetic exercise and record that limited purpose. This
   suggested decision has not occurred and would not authorize live data use,
   memory write or publication.
5. The changed disposable directory is rejected while the retained original
   verifies; exported bytes can be reread and practitioner JSON parsed. Neither
   proves truthful attendance, independent custody or educational effectiveness.
   The [known limitations](../KNOWN_LIMITATIONS.md) also distinguish standalone
   ZIP-member verification from exact ZIP-byte binding in the live transaction.
