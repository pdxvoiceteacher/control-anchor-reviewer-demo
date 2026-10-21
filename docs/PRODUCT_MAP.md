# Product map and reviewer crosswalk

Control Anchor is the intended local workbench; the Triadic Brain is its governed
cognition architecture. The whole product combines substantive analysis, challenge,
correction and continuity with controls and retained evidence. This repository
demonstrates one offline captured-output component of that system.

This summary adapts the source README's **Repository map** and **Customer
functionality crosswalk**, its product-file map and its installer map at
`pdxvoiceteacher/triadicbrain-open-alpha` commit
`37583fd91ff7f0d912256c10fea89ff6896763cf`:
[README](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/blob/37583fd91ff7f0d912256c10fea89ff6896763cf/README.md#repository-map),
[product functions](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/blob/37583fd91ff7f0d912256c10fea89ff6896763cf/docs/current/product-file-map.md),
[installer process](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/blob/37583fd91ff7f0d912256c10fea89ff6896763cf/docs/delivery/WINDOWS_INSTALLER_MAP.md).
Attribution: Thomas Prislac / UVLM. Exact source identities are in
[SOURCE_MANIFEST.json](../SOURCE_MANIFEST.json). This is a new summary, not the
private inventory, a standards mapping or a new implementation.

Milestone descriptions below were refreshed on **21 October 2026 UTC** against
upstream main `206aeb6d6f17cf4e2656f14890ea5ddc04237a06`, its `CURRENT_PRODUCT.md`
and `docs/current/product-file-map.md`. The earlier attribution above remains the
architecture-summary source; this refresh changes no extracted engine identity.
The pinned branch evidence below was verified **21 October 2026, 04:52:47 UTC**
during this update's source review. These are named checkpoints, separate from
the main documentation snapshot; later branch activity does not retarget them.

## Two interface directions, one local authority

```text
Local user -> Control Anchor -> supported configured AI provider -> retained outcome
AI application -> authenticated Control Anchor tools -> native authority/custody -> tool result
```

The first uses provider contracts, readiness and bounded transport. The second
uses authenticated MCP/native integration; it is not downstream inference or
automatic capture of every host conversation. Both reuse the common task, control,
review and custody implementation in the full design. Neither live direction is
executed here: the runner imports authored local candidate bytes with
`provider_invoked=false`.

## Whole-product responsibilities

**HERE** means observed in this synthetic extraction. **ELSEWHERE** identifies
source in the pinned development repository, not demonstrated here; file presence
does not establish installed or live acceptance. **PROPOSED** identifies intended
connections or staged capabilities needing their own implementation/acceptance
evidence. Rows can span these states.

| Customer capability / responsibility | Owning source area | Reviewer status and boundary |
| --- | --- | --- |
| Install, start, uninstall and update | Package backend/recipe, Windows setup, Inno delivery, native finalization and installed entry | ELSEWHERE: CI206 demonstrated application-only installation and restricted terminal Home at its exact source. Ordinary-user consent/UAC, restart, supported PRODUCT uninstall and history-preserving update remain unproved. No installer is included here. |
| Author organization controls | Original document -> editable rule/draft -> preview -> authorized version; control-authoring/admin/policy families | ELSEWHERE: supported data-driven authoring and custody activation. General document comprehension and live semantic fidelity are not established here. |
| Enter tasks and deliberate follow-ups | Native workbench/task authoring, Sonya message/parent binding and gateway | ELSEWHERE: interactive/service source. HERE: captured transaction registration only, not an installed task or live reply. |
| Govern ingress and permitted exchanges | Sonya/AEGIS consent, identity, adapter permission, quarantine and admission | ELSEWHERE: provider/native protection paths. HERE: bounded local inputs and logical role/action checks; no OS isolation or provider exchange. |
| Connect providers and retain actual outcomes | Provider contract/readiness/transport, protected selection publication, credentials and custody reopening | ELSEWHERE: supported protocol adapters, not universal model compatibility. Saved labels, connection and inference are distinct; none is proved here. |
| Let an AI host use Control Anchor | Authenticated MCP tools, fixed native grants/clients and administration companion | ELSEWHERE: the opposite interface direction. A factory or SDK fixture is not an accepted installed host connection. |
| Ground and analyze; apply configured procedures | CoherenceLattice grounded alternatives, claim/evidence links and counterexamples; cross-cutting UCC execution; governed bridge/pipeline | ELSEWHERE: substantive component implementations. HERE: deterministic evidence controls and captured claim envelope only; not business-control interpretation or full CoherenceLattice execution. |
| Evaluate separately and present posture | Sophia evaluates supported evidence; Atlas explains posture, prior context and eligible continuity; TEL links performed stages | ELSEWHERE: separate component implementations and joined source. HERE: named audit/posture records, not those component executions or independent model corroboration. |
| Retain authoritative history and enforce permissions | Custody, actor/transition policy, canonical bytes and recovery | HERE: captured records, logical role separation and hash chain. ELSEWHERE: native protected custody/services. Independent custody and signing are not demonstrated here. |
| Assist, challenge, correct and continue inquiry | Analyst/Challenge context, assisted/feedback families, explicit parent purpose and retrosynthetic alternatives | ELSEWHERE: bounded assistance and feedback source. HERE: scripted advisory selection and separate repair child preserve original candidate/findings. No learned improvement or resolved finding is claimed. |
| Human review, reporting, export and reopen | Review workbench, population/period projections and transaction/governed exports | HERE: scripted decisions, verification and practitioner export/reopen. ELSEWHERE: richer native/MCP consumers. Actual human acceptance and professional conclusions remain separate. |
| Cooperate across local instances | Scoped artifact sharing, locally governed Sophia network, optional PMR/P2P and peer resources | ELSEWHERE: unmerged PR67 separates source-qualified local receiving from unexecuted staging. Live peer networking, compute and broader memory joins remain unproved. None is included or activated here. |

Application modules and selected components are runtime source. Delivery tools
and configuration define package membership. Integrations expose different entry
points. Tests, examples, research and development evidence have other purposes;
copying the whole repository would not produce a valid installer. This extraction
includes none of the full private inventory or operator history.

## Actual included function crosswalk

These relative links lead to the unchanged implementation extracted at
`139932846cb1b6bf1571158464d89513d4e381f8`, not the later documentation snapshot.

| Demonstrated operation | Included function / file | Supported observation |
| --- | --- | --- |
| Parse and dispatch captured inputs | `main`, `dispatch` in [production_cli.py](../src/triadicbrain/assurance/production_cli.py); harness [demo.py](../demo.py) | The actual CLI consumes fixture files without a provider invocation. |
| Retain source, prompt/settings and candidate | `create_evidence_store`, `register_captured_transaction` in [transaction.py](../src/triadicbrain/assurance/transaction.py); [canonical.py](../src/triadicbrain/assurance/canonical.py) | Exact retained inputs and canonical records, not source truth. |
| Check evidence and custody | `execute_controls` in [controls.py](../src/triadicbrain/assurance/controls.py); `verify_events` in [custody.py](../src/triadicbrain/assurance/custody.py); `authorize` in [authorization.py](../src/triadicbrain/assurance/authorization.py) | Deterministic conditions and logical roles. `STANDARD_PROFILE` in [review_policy.py](../src/triadicbrain/assurance/review_policy.py) has no semantic finding rules. |
| Select the advisory and create a child | `submit_human_decision`, `create_repair_child`, `register_platform_observed_transaction` in [transaction.py](../src/triadicbrain/assurance/transaction.py) | Injected advisory and scripted decision; preserved parent bytes and added lineage; `resolved_finding_ids=[]`. |
| Recover one interrupted decision | `submit_human_decision(..., fault_after_target=1)`, `TransitionInterrupted`, `recover_pending_transition` in [transaction.py](../src/triadicbrain/assurance/transaction.py) | Deliberate pre-seal fault: pending state/journal, one recovery receipt/event, no duplicate decision transition, unchanged second recovery, then verified directory/ZIP. No actual OS crash evidence. |
| Seal and reject changed evidence | `finalize_transaction` in [transaction.py](../src/triadicbrain/assurance/transaction.py); `build_transaction_package` in [transaction_package.py](../src/triadicbrain/assurance/transaction_package.py); `verify_transaction_directory`, `verify_transaction_zip` in [verification.py](../src/triadicbrain/assurance/verification.py); `validate_instance` in [schema_validation.py](../src/triadicbrain/assurance/schema_validation.py) | Package/schema consistency and directory tamper rejection, subject to the [ZIP boundary](../KNOWN_LIMITATIONS.md). |
| Export/reopen practitioner evidence | `build_practitioner_export`, `build_practitioner_view` in [web.py](../src/triadicbrain/assurance/web.py); `build_practitioner_index` in [practitioner.py](../src/triadicbrain/assurance/practitioner.py) | Read-only projections can be written, reread and parsed; they issue no assurance or authority. |

## Evidence edition and remaining joins

The [21 October upstream checkpoint](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/blob/206aeb6d6f17cf4e2656f14890ea5ddc04237a06/CURRENT_PRODUCT.md)
and product-file map distinguish these exact milestones:

| Milestone | Evidence and limits |
| --- | --- |
| Merged installed Home source | CI206 at product `73ec4d1d34f080104df803cf264e6bf513cba157`: 26 selected source cases / 78 phases passed, actual application-only Inno installation, installed verification, restricted terminal Home and the same provider selection saved/reread. PR56 merged those product trees; PR65/68 maintain the current navigation. [Run](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39517587826) uses a separate helper SHA, not the product SHA. |
| Provider metadata, failed CI212 and unexecuted repair in draft PR66 | [CI212](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39544384534) at `6b92a9bb4419053b5c3f16fe0b1bd672d9e5a79a` collected 26 cases: 0 complete PASS, 1 FAIL, 25 unexecuted. The first case failed before metadata I/O when the source-only guard blocked Windows client-journal DLL acquisition. Fixture-only successor `caaf8af33ac64e5fd9bf21b75770903ec3dd493d` is unexecuted; production, guards and the 26-case selection are unchanged. Earlier source checks do not qualify this repair or an installed/live connection. |
| Local peer receiving, separate PR67 baseline | CI211 passed 51 cases / 153 phases at `b1e684b5c81f3df623fd654f1bb4ceeb21788e7b`, using synthetic material and injected boundaries. This is local receiving source qualification, not live peer networking or shared compute. |
| Reviewed peer staging checkpoint, unmerged draft PR67 | `a4c2f28087038fec13d0417cfa47b6f994f34d87` carries transfer/staging with 35 authored/unexecuted cases, including the added metadata-response regression. Its maintained P2P map separates staging, explicit receipt and reconciliation. CI211 does not qualify these newer bytes. |

CI206 does not establish provider contact, inference, application restart,
ordinary-user/UAC behavior or actual human acceptance. Earlier failures and
UNKNOWN outcomes remain historical evidence; the later pass does not identify
CI195's original pipe failure cause. No installation or branch result transfers
to this offline extraction. The full live-provider journey and record-preserving
uninstall/update remain unfinished.

Reviewer evidence remains the [observed local validation](../VALIDATION.md):
offline capture, deterministic checks, scripted review/repair, export/reopen and
adverse verification. Full live inference through analysis and attributable review,
ordinary-user installed acceptance and optional network/continuity functions need
their own evidence when claimed. They are not prerequisites for accurately
presenting this limited source demonstration.

The purpose is to help people inspect and correct work under their own rules.
This demo supplies no worker scoring, discipline or employment monitoring.
