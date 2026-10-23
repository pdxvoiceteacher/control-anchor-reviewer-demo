# Proposed Control Anchor roadmap

**Owner-proposed direction, 23 October 2026. Not demonstrated product capability.**
This concise planning summary uses the owner's supplied roadmap brief. It does
not claim that the proposed-design handbook, research sources or a new backend
have been implemented or qualified. The [current evidence map](PRODUCT_MAP.md#evidence-edition-and-remaining-joins)
and [offline demo limitations](../KNOWN_LIMITATIONS.md) remain controlling for
claims about observed behavior.

## Function first, learned executive second

First make useful coordination explicit: retain a persistent goal state, show
constraints and unresolved work, choose supported actions, inspect results and
stop or ask when a bounded plan cannot proceed. A later learned executive model
could help propose or revise those plans after suitable evaluation. A named
executive, persistent goal record or generated plan is not proof of intelligence,
awareness, universal interpretation or useful autonomous performance.

Users would supply eligible models through supported adapters and choose the
roles they perform. Coordination must preserve each role's permitted evidence,
tools, outputs and human authority. Compatibility and resource limits need actual
checks; adding a coordinator is not a turnkey upgrade to an arbitrary model.

NCM is an **optional experimental generation/representation backend**. Evaluating
it would be a separate research choice. It does not establish executive
intelligence, automatic learning or improved performance, and it is not a
prerequisite for the first useful local workflow.

## Separate learning, retrieval and exchange

| Proposed choice | Required distinction |
| --- | --- |
| Task history and PMR retrieval | Contextual retrieval supplies selected records for an eligible task. It does not itself change model weights, grant training rights or turn a recalled statement into truth. |
| Local learning | Any supported model update would need explicit opt-in scope, selected data, resource limits, evaluation and a retained version. Saving history is not consent to train. |
| Network learning | Participation would be separately optional. Local operation must remain possible without sharing data, memory or updates with peers. Local-first does not guarantee privacy when a selected model or peer receives data. |
| Shared-prior bundles | Versioned reusable priors would have declared purpose, format, target compatibility, provenance, permissions and validity. Optional P2P peers could distribute eligible bundles; receiving one would not authorize activation or future reuse. |

PMR retrieval and adoption of a model prior are different operations. A shared
bundle's meaning must be declared rather than inferred from its name.
Source hashes establish byte identity; signatures can authenticate an origin
under the chosen trust arrangement. Neither establishes truth, correctness,
license eligibility, model compatibility or permission to use the contents.
Corrections, revocation, expiry and version changes must affect later eligibility
without rewriting earlier evidence or promising erasure of disclosed copies.

## Govern both ingress and egress

Sonya would bind incoming tasks and selected context to their purpose and current
permissions. Enforced egress would also check the actual destination, payload,
operation and limits before an allowed exchange. Generated text would not grant
network access or override those checks. Input filtering alone is not an egress
control, and a written privacy rule is not evidence that an actual transport
enforces it.

Protected, application-managed prior storage is proposed so users would not need
to move internal files or manage hashes by hand. The application would retain
versions and provenance, check eligibility before loading or retrieval, and
separate storage from adoption. Protection against ordinary unauthorized writes
would not imply immunity from a trusted administrator or automatic confidentiality.

## Carry one accepted meaning to the runtime decision

Canonical typed inputs and owning formulas would define units, bounds and derived
values once. Generated consumer files would carry those accepted inputs and
derivations to their real readers rather than become independent authorities.
The deciding runtime consumer must validate the relevant version and bindings
and apply the intended calculation to the actual effect.

The proof obligation is the connected path: accepted input, saved representation,
generated consumer, actual runtime predicate, effect and retained result.
Generation success, matching hashes and a passing fixture do not alone prove that
the runtime uses the value. Legitimate, changed-input and adverse cases must reach
the real consumer; a report must preserve failed, missing and unexecuted work.

These proposals add no model call, training, provider activation, peer connection,
installation, spending or release authority. They establish no compute savings,
learning benefit or delivery date. The immediate delivery work remains the
qualified local task, actual permitted response, selected analysis, correction,
attributable review and export/reopen sequence described in the product map.
