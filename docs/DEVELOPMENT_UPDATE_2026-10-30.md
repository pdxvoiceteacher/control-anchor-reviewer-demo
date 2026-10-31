# Development update — 30 October 2026

*Pacific date; prepared 31 October 2026 UTC.*

**A provisional map of the connections still worth building and proving.**
Control Anchor's public reviewer demo remains an offline, synthetic component.
This update changes documentation, not its runtime, and imports no private-alpha
implementation. The [product map](PRODUCT_MAP.md),
[proposed roadmap](PROPOSED_ROADMAP.md) and
[29 October update](DEVELOPMENT_UPDATE_2026-10-29.md) retain their dated scopes.

## Connections, not a completion score

The broader design can provisionally be organized into **15 connection families**.
This is neither a count of 15 defects nor an exhaustive audit. One connection may
contain working components, an unfinished adapter and an unproved installed
interaction. Further inspection may split, combine or remove items.

The distinction matters:

- **Implementation work:** a specified connection or behavior still needs to be
  built or joined. A design document is not that implementation.
- **Proof work:** implementation or bounded evidence exists, but the relevant
  end-to-end, installed, failure/recovery or human-use observation is missing.
- **Optional research:** an idea needs its own experiment before adoption; it is
  not a condition for delivering the first useful local workflow.

These categories can overlap. An uninspected path is **unknown**, not automatically
absent. Existing source and historical successes should be reused, not erased by
calling the whole architecture unfinished.

## Provisional connection map

The foundation column draws on the existing public descriptions linked above
and this proposed connection plan. New Observer/helper work is attributed
maintainer-reported development, not evidence supplied by those earlier pages.
Development components mentioned here are not included in this public demo unless
explicitly stated. The last column identifies work needed, not a delivery date.

| Connection family | Existing foundation or proposal | Next implementation or proof obligation |
| --- | --- | --- |
| 1. Human intent → controls and task meaning | Supported control-authoring and task components are described in development. | **Implementation + proof:** carry accepted meaning to supported checks and authorized activation; expose unsupported meaning. Business findings remain advisory. General document understanding is not established. |
| 2. Native user or AI host → authenticated task | Native and authenticated host interfaces have distinct responsibilities. | **Proof:** qualify the real caller, current permissions and attributable task creation. A test client is not an accepted installed host. |
| 3. Provider choice → activation → retained response | Selection, metadata checks and separate response experiments have bounded evidence. | **Integration + proof:** connect the installed authorized path to a real response; retain failures and uncertain outcomes. Saving a preference is not activation. |
| 4. Captured evidence → supported analysis | Grounding and procedure components exist in development; this demo performs deterministic checks. | **Proof:** show selected evidence reaching the intended native analysis, including missing evidence and contradictory inputs. |
| 5. Candidate → separate evaluation → correction | Evaluation and assistance components exist; the demo preserves a scripted correction. | **Integration + proof:** qualify actual evaluation and selected correction while retaining the original and unresolved findings. Agreement is not independent corroboration. |
| 6. Observer recommendation → authenticated selection → preview | Advisory coordination and owner-local selection helpers are development work, not public-demo features. | **Implementation + proof:** join the actual authenticated interface to the existing preview path, including cancellation, repeated clicks and lost replies. See the contract below. |
| 7. Performed work → retained history → review/export/reopen | This demo exercises synthetic capture, scripted review, export/reopen and one interrupted decision. Native consumers extend that foundation. | **Proof:** qualify the connected native workflow and actual human use. Named records do not prove every corresponding component ran. |
| 8. Task progress → restart or successor context | Continuity and bounded planning are design responsibilities. | **Implementation + proof:** define what may resume, retain unresolved effects and prevent a new process or model from inheriting unearned authority. |
| 9. Source → installed lifecycle and recovery | Dated hosted installation and restricted startup results exist. | **Proof + bounded repairs:** ordinary-user operation, restart, update/uninstall and interrupted publication need their own evidence. Hosted startup does not establish these. |
| 10. User intent → resource limits → child lifecycle → outcome | Resource controls and admission components are described in development. | **Integration + proof:** connect limits to actual owned processes, stopping and cleanup; reconcile uncertain completion before retrying. |
| 11. Completed peer artifact → evidence for a new task | Bounded receiving and exchange tests exist outside this demo. | **Proof:** qualify independently administered participants, permission checks and interrupted exchange. Received work is not automatically corroboration. |
| 12. Contributed compute → distributed work and reuse | Local opt-in and admission tests are groundwork, not an operating distributed service. | **Implementation + proof:** connect separately authorized resource execution and retained outcomes. Demonstrate usefulness against ordinary alternatives. |
| 13. History → eligible optional memory | Contextual retrieval and versioned reuse are proposed choices. | **Implementation + proof:** enforce purpose, eligibility, correction and expiry at retrieval. Retention is not training consent. |
| 14. Observation and prior structure → adaptive attention or learning | Optional research, separate from the working preview connection. | **Research:** compare against simple baselines, preserve negative results and measure failures as well as cost. No consciousness or general learning benefit is established. |
| 15. Proposal → separately governed action | The design keeps advice, permission and execution distinct. | **Optional future capability — integration + proof:** show that recommendations cannot authorize themselves and that the actual action boundary enforces the current decision. |

## The next narrow join: choosing a recommendation safely

The proposed interaction reuses the existing assistance-preview path rather than
creating a second executor. Its target behavior is:

1. An authenticated user sees a bounded recommendation list. Selection refers to
   that exact displayed recommendation and context, not a newly generated substitute.
2. One explicit selection claims one local attempt. Repeated clicks cannot create
   multiple attempts. This is **not** a claim of distributed exactly-once execution.
3. Cancellation can prevent work only before that claim wins. Afterward, the UI
   must report the actual state rather than promise that cancellation undid it.
4. An expired or changed context requires a fresh explicit choice. A retry must
   not silently renew the original validity window.
5. A lost reply or process restart leaves an uncertain result until inspected or
   reconciled. It must not cause automatic replay of a possibly completed effect.
6. Preview remains consent-false and advisory: inspecting it does not submit a
   task, invoke a model, grant execution authority or record a human approval.

Owner-local helpers and synthetic lifecycle checks are being developed around
this contract. They are **not shipped in this repository** and do not establish
an authenticated installed route, process isolation or human acceptance. Actor
authentication also does not by itself prove a genuine human selection gesture.
The decisive proof is the connected native path, including its actual retained
inspection effects and adverse cases—not the number of helper tests.

## What would move the map forward?

Start with one bounded local workflow: authenticated task, permitted response,
selected analysis, explicit correction where needed, attributable review and
export/reopen. Add the real selection/recovery observations to that path before
expanding optional peer, memory or adaptive-learning features. Preserve failed,
unexecuted and uncertain results rather than combining different revisions into
one readiness claim.

This map is a planning aid, not a certification or a new approval authority.
Maintainer-reported private development and AI-assisted review are not publicly
reproducible qualification. The public [validation record](../VALIDATION.md) and
[limitations](../KNOWN_LIMITATIONS.md) describe what readers can actually inspect
and reproduce here. No new runtime test result, efficiency gain, release,
funding commitment or license grant is claimed by this documentation update.
