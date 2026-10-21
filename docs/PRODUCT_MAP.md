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

Milestone snapshot checked **21 October 2026, 08:11:33 UTC** against private
development main `ff5a40adb43191b2018b13e1a4dcf00ebc5bcc9e`, its P2P map and
PR66/PR70 evidence. This supersedes the earlier 04:52:47 milestone summary;
earlier attribution and source identities remain historical provenance.
The private-development links below attribute reported evidence; those tests
are **not publicly reproducible from this reviewer repository**. No private code
or operational artifacts are included. These are named source checkpoints;
later branch activity does not retarget their results.

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
| Connect providers and retain actual outcomes | Provider contract/readiness/transport, protected selection publication, credentials and custody reopening | ELSEWHERE: merged metadata CHECK and a separate REREAD predicate have source-specific passing evidence with injected replies. Installed activation, actual provider contact and inference remain unverified; none is executed here. |
| Let an AI host use Control Anchor | Authenticated MCP tools, fixed native grants/clients and administration companion | ELSEWHERE: the opposite interface direction. A factory or SDK fixture is not an accepted installed host connection. |
| Ground and analyze; apply configured procedures | CoherenceLattice grounded alternatives, claim/evidence links and counterexamples; cross-cutting UCC execution; governed bridge/pipeline | ELSEWHERE: substantive component implementations. HERE: deterministic evidence controls and captured claim envelope only; not business-control interpretation or full CoherenceLattice execution. |
| Evaluate separately and present posture | Sophia evaluates supported evidence; Atlas explains posture, prior context and eligible continuity; TEL links performed stages | ELSEWHERE: separate component implementations and joined source. HERE: named audit/posture records, not those component executions or independent model corroboration. |
| Retain authoritative history and enforce permissions | Custody, actor/transition policy, canonical bytes and recovery | HERE: captured records, logical role separation and hash chain. ELSEWHERE: native protected custody/services. Independent custody and signing are not demonstrated here. |
| Assist, challenge, correct and continue inquiry | Analyst/Challenge context, assisted/feedback families, explicit parent purpose and retrosynthetic alternatives | ELSEWHERE: bounded assistance and feedback source. HERE: scripted advisory selection and separate repair child preserve original candidate/findings. No learned improvement or resolved finding is claimed. |
| Human review, reporting, export and reopen | Review workbench, population/period projections and transaction/governed exports | HERE: scripted decisions, verification and practitioner export/reopen. ELSEWHERE: richer native/MCP consumers. Actual human acceptance and professional conclusions remain separate. |
| Cooperate across local instances | Scoped artifact sharing, locally governed Sophia network, optional PMR/P2P and peer resources | ELSEWHERE: separately qualified local receiving, injected-transport staging and one synthetic same-process loopback TCP case are merged. Installed/distributed peers, TLS, discovery and shared compute remain unproved. None is included or activated here. |

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

The [private P2P map at the pinned main](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/blob/ff5a40adb43191b2018b13e1a4dcf00ebc5bcc9e/docs/current/p2p-development-map.md),
[merged PR66](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/pull/66)
and [merged PR70](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/pull/70)
distinguish these milestones. Each result retains its own source and population;
the rows do not add up to a full-suite or current whole-product PASS.

| Milestone | Evidence and limits |
| --- | --- |
| Merged installed Home source | CI206 at product `73ec4d1d34f080104df803cf264e6bf513cba157`: 26 selected source cases / 78 phases passed, actual application-only Inno installation, installed verification, restricted terminal Home and the same provider selection saved/reread. PR56 merged those product trees; PR65/68 maintain the current navigation. [Run](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39517587826) uses a separate helper SHA, not the product SHA. |
| Provider metadata CHECK, merged PR66 | [CI216](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39550198540) passed 26 cases / 78 phases at `fdc101f00980e782c021f9a2951c58cc57ac24d0`. Actual UI/broker/gateway/custody consumers used injected HTTP metadata replies. PR66's merged integration source is `3ed834c027ec0babe850ad101b79792e8e0ac6e1`. This is source qualification, not installed provider contact or inference. |
| Separate REREAD predicate | [CI217](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39551310691) passed exactly one existing predicate case / 3 phases at `4c4f002812b7b17cd5b76f5c2dda3d2bef91efe3`. This result belongs to that predicate; it neither repeats nor extends CI216's 26-case result into a full-suite claim. |
| Local peer receiving, separate PR67 baseline | CI211 passed 51 cases / 153 phases at `b1e684b5c81f3df623fd654f1bb4ceeb21788e7b`, using synthetic material and injected boundaries. This is local receiving source qualification, not live peer networking or shared compute. |
| Peer staging, merged PR67 | [CI213](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39545535104) passed 35 cases / 105 phases at `a4c2f28087038fec13d0417cfa47b6f994f34d87` using injected HTTP transport and actual native source/receiver consumers. Keep this result separate from CI211's earlier receiving source. |
| One synthetic loopback TCP case, merged PR70 | [CI219](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39559159214) passed exactly one case / 3 phases at `d9d0e1427c3a4bfbbbebb9e5b361bad28cdd6f73`: five TCP exchanges, staging, one explicit receiving receipt and fresh-store reopen without resend. The receiver remained in-process. PR70 merged at `ad6f595105bc31a86d0ec62d78f6111b34ebfec6`. This does not demonstrate installed/distributed peers, TLS, discovery, interrupted TCP recovery or shared compute. |

Original failures remain failures: [CI212](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39544384534)
at `6b92a9bb4419053b5c3f16fe0b1bd672d9e5a79a`
recorded 0 complete PASS, 1 FAIL and 25 unexecuted cases before metadata I/O;
CI214/215 also remain failed history. [CI218](https://github.com/pdxvoiceteacher/triadicbrain-open-alpha/actions/runs/39554984743)
failed before TCP connection and is
not relabeled by CI219. The later passes do not reconstruct missing historical
causes. PR66's recorded CI217 evidence supersedes the specific stale REREAD
"unexecuted" statement in the pinned private `docs/current/provider-delivery.md`.

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
