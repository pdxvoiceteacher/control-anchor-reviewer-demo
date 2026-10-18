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
| Install, start, uninstall and update | Package backend/recipe, Windows setup, Inno delivery, native finalization and installed entry | ELSEWHERE: delivery source and source-bound installation work. PROPOSED/unfinished acceptance: usable installed startup, ordinary-user consent, supported PRODUCT uninstall and history-preserving update. No installer is included here. |
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
| Cooperate across local instances | Scoped artifact sharing, locally governed Sophia network, optional PMR/P2P and peer resources | ELSEWHERE: bounded prototype/research source. PROPOSED: live receiving custody, peer compute and separately authorized network/memory joins. These remain product goals, not initial installer dependencies or demonstrated capabilities. |

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
| Seal and reject changed evidence | `finalize_transaction` in [transaction.py](../src/triadicbrain/assurance/transaction.py); `build_transaction_package` in [transaction_package.py](../src/triadicbrain/assurance/transaction_package.py); `verify_transaction_directory`, `verify_transaction_zip` in [verification.py](../src/triadicbrain/assurance/verification.py); `validate_instance` in [schema_validation.py](../src/triadicbrain/assurance/schema_validation.py) | Package/schema consistency and directory tamper rejection, subject to the [ZIP boundary](../KNOWN_LIMITATIONS.md). |
| Export/reopen practitioner evidence | `build_practitioner_export`, `build_practitioner_view` in [web.py](../src/triadicbrain/assurance/web.py); `build_practitioner_index` in [practitioner.py](../src/triadicbrain/assurance/practitioner.py) | Read-only projections can be written, reread and parsed; they issue no assurance or authority. |

## Evidence edition and remaining joins

The pinned [current delivery checkpoint](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/blob/37583fd91ff7f0d912256c10fea89ff6896763cf/CURRENT_PRODUCT.md#integrated-development-checkpoint--18-october-2026)
reports source-specific installation progress but no established usable installed
startup or accepted live-provider journey. It retains an UNKNOWN installation
outcome and distinguishes repaired source checks from installed behavior. Older,
contradictory dated README snapshots do not supersede that scoped checkpoint.
This map transfers no installation result to the extraction and does not qualify
the entire documentation snapshot's source tree.

Reviewer evidence remains the [observed local validation](../VALIDATION.md):
offline capture, deterministic checks, scripted review/repair, export/reopen and
adverse verification. Full live inference through analysis and attributable review,
ordinary-user installed acceptance and optional network/continuity functions need
their own evidence when claimed. They are not prerequisites for accurately
presenting this limited source demonstration.
