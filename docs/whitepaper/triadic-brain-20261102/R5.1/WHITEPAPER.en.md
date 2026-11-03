# Triadic Brain

## A public design for cooperative human and AI cognition

Conceptual and system design by Thomas Prislac  
Ultra Verba Lux Mentis  
English design documentation edition  
Document version 2026-11-02.R5.1  
2 November 2026

AI-assisted documentation. Documentation review concerns meaning, evidence and presentation; it is not runtime qualification or outside endorsement.

## Reading paths

Read the [summary](#S00), [garden task](#S02) and [architecture](#S03) first. Then explore [memory](#S05), [shared vocabulary](#S06), [efficiency](#S07), [governance](#S08), [observation](#S09), [cooperation](#S10), [human analogy](#S11), [optional extensions](#S12) or [evidence and delivery](#S13).

The [linear family guide](FAMILY_GUIDE.en.md) explains 86 mixed-kind registry entries, with functional inputs, outputs and owners only where applicable. The [compact index](#APP-A) is for comparison. The [English concept map download](PUBLIC_CONCEPTS.json) contains structured documentation, not an executable schema. The [English term and translation sense register](TERMS.en.md) preserves important distinctions. This is the English design documentation edition. No translated edition is included in this bundle.

The [conventional research and engineering crosswalk](STANDARDS_RESEARCH_CROSSWALK.en.md) connects the project names with familiar search terms, including source attribution, analogical reasoning, reason maintenance, local-first software and consumer-side authorization. It shows which overlaps are partial, where equivalence stops and which additional responsibilities remain project proposals. These complementary mechanisms help investigate gaps; they do not replace the connected design or rename its interfaces. The [structured crosswalk](STANDARDS_RESEARCH_CROSSWALK.json) accounts for all 86 registry entries.

The [Knowledge Waters appendix](#APP-B) explains the project's corridor, river and terrace research, including source-defined equations and the limits of their implementation and evidence. It uses the existing registry rather than adding a new component.

Reading these documents does not enroll anyone or grant access, execution, persistence, resource spending, credentials or permission to contact others. Participation remains subject to the relevant host/operator authorization and affected rights.

<a id="S00"></a>

## Summary

Triadic Brain is being designed to help people think, learn and work together while retaining meaningful control over their computers, information and AI assistance. Its intended home is a user-owned node that can work locally and cooperate with other independently governed nodes when their owners agree. Control Anchor is the human interface for that node. The product is the connected Brain: its task intake, analytical work, evaluation, memory, controls, evidence and cooperation.

The practical goal is useful, inspectable help for working people and under-resourced institutions. A community should be able to choose its models, understand where its data goes, set its own resource limits, preserve knowledge it is entitled to keep, and leave a provider or network without abandoning its work. Better-equipped participants could contribute bounded compute. Others could contribute expertise, corrections, reusable methods, accessible explanations or useful negative results. Participation should not require surrendering private records or accepting a donor's conclusions.

Efficiency matters because time, electricity, hardware and attention are scarce. The value of ownership and practical freedom does not depend on outperforming every centralized service. A person may reasonably prefer an eligible local or cooperative route even when it carries more overhead, provided the costs and tradeoffs are visible.

This paper explains the intended connected system and the responsibilities preserved across its development. Selected components have source implementations and bounded evidence. Actual installed cognition, complete native isolation and a real two-node exchange followed by a three-node Wi-Fi workflow still require demonstration. Global participation across millions of computers is an aspiration, not measured capacity. The possibility of emergent collective consciousness is an open research hypothesis; product value does not depend on resolving it.

<a id="S01"></a>

## 1 Purpose and scope

Triadic Brain begins with a human purpose rather than a requirement to use every available model or computer. A librarian may need to organize a local history collection. A small school may need to adapt teaching materials. A household may need help comparing repair options. The system should help them use available evidence, identify uncertainty, obtain a meaningful challenge and retain a useful result under understandable controls.

The ambition is broad: cooperative intelligence that supports agency, creativity, learning and an ecology of care. Its implementation must remain specific. Who owns this input? Which task is authorized? Which computer may process it? What may be retained? What happens when the answer is wrong, the connection disappears or permission changes? A network that cannot answer these questions has not fulfilled the ownership goal merely by being distributed.

The design therefore preserves several commitments. Each node retains local authority. Models and coordinators should be replaceable through supported, tested interfaces. Resource sharing is voluntary. Dissent and adverse evidence remain visible. People need accessible ways to inspect, correct, stop, export and leave. An institution can apply accountable local rules without silently rewriting another participant's evidence or rights. These are design and acceptance obligations, not a claim that social equity follows automatically from software.

This paper reconciles functions rather than treating every historical name as a separate product. A function is a responsibility with inputs, outputs, limits and consumers. Names can change while responsibilities survive. The appendix conserves 86 mixed-kind entries. They include the system and deployment scopes, capability responsibilities, contracts, principles, optional profiles, research, historical lineage and one historical testing document. Record kind is separate from maturity; this is neither a count of runtime functions nor a list of completed modules. The companion concept map carries the same identifiers so that translators, developers and readers can discuss a responsibility without depending on a particular English label.

<a id="S02"></a>

## 2 A task from beginning to end

Consider a community group preparing a garden plan. It has a public climate dataset, a site sketch, a small budget and notes from volunteers. Some notes contain personal information that should stay on the organizer's computer. The group wants an understandable comparison of options and a reusable planning method. The following is the target experience, not a report of a deployed pilot.

**Set the purpose and boundaries.** Through Control Anchor, the organizer selects the question, relevant evidence, a supported local model and a finite resource budget. Personal notes remain local. Public climate data can be shared with an admitted peer. Retention of the result is a separate choice from sending a task. Training on the notes is not implied by either choice. The interface explains which checks are supported and which still require a person.

**Receive and preserve the task.** Sonya is the intake and adapter boundary. It preserves the task's identity, source and declared context, treats incoming text as untrusted content, and routes only supported work. AEGIS applies technical admission and protective rules. UCC applies supported finite procedures under the accepted control version. The authoritative custody record retains the attempt and its actual outcome, including rejection or uncertainty, rather than recording only successful answers.

**Plan within delegated authority.** A user-designated executive proposes a bounded sequence: organize evidence, calculate selected quantities, compare alternatives and obtain a challenge. Some steps are deterministic and need no model. One model may perform several roles sequentially, or separate eligible workers may contribute. Preauthorized autonomy can carry out the permitted sequence without a new prompt at every minor step. The executive cannot enlarge its own authority, grant itself another node's resources or silently substitute a more permissive policy.

**Analyze and challenge.** An Analyst proposes options. CoherenceLattice connects claims, sources, assumptions and unresolved questions. A Challenge role looks for weaknesses. Sophia evaluates the fixed candidate using its declared checks and evidence. A Synthesis role addresses the findings without deleting dissent. Different role names or repeated model answers do not, by themselves, establish independent judgment.

**Use a peer only when useful and permitted.** A second node might receive the public climate subset and a narrowly defined comparison task. Both owners must permit the relevant disclosure and execution. The peer's resource owner must reserve real capacity and enforce limits. The organizer's private notes do not travel merely because another computer could run a larger model.

**Present a decision rather than a mysterious score.** Atlas presents the options, supporting evidence, contrary findings and remaining uncertainty. It may compare an eligible prior method if retrieval and current-use rights permit that comparison. A useful output might say that one option is cheaper but depends on an unverified water assumption. The organizer can correct the assumption or ask for a narrower next step. A numerical confidence label cannot replace that explanation.

**Return to the problem when circumstances change.** Suppose the group learns that its water allowance is lower, or deliberately changes its purpose from maximizing yield to minimizing maintenance. The intended [planning loop F47](FAMILY_GUIDE.en.md#F47) makes a successor context and bounded plan rather than rewriting the first observations. Evidence-relative beliefs remain attributable. CoherenceLattice proposes changed alternatives; Sophia reviews that changed candidate; Atlas carries the known and unfinished work forward. The executive rechecks the relevant role, scope, consent and resource limits before an attributable resume or hold. Question continuity means preserving the change and its origin, not forbidding an authorized new purpose.

A useful pattern unrelated to the garden answer takes the separate [novelty route F70](FAMILY_GUIDE.en.md#F70). It can be nominated for later review without being forced into the answer or automatically stored. If a session restarts or the model is replaced, [recovery F62](FAMILY_GUIDE.en.md#F62) should restore committed context and pending effects under the current owner, while rejecting obsolete workers' late output. It must not repeat an uncertain external effect. This connected feedback and recovery behavior is intended; the complete installed loop is not yet demonstrated.

**Retain the useful part.** With appropriate permission, PMR can retain a checked planning pattern, its assumptions, essential lineage and known failure conditions. The system need not preserve every temporary draft forever. A separately reviewed public derivative might share the method while excluding names, private notes and identifying metadata. Another group can adapt it and perform its own target checks.

**Handle interruption honestly.** If a reply disappears after a task may have started, the system reconciles the original attempt instead of blindly resending it. If permission is revoked, future dependent actions must recheck current authority. Previously disclosed information cannot be recalled with certainty. The history distinguishes what happened from what is permitted now.

The decisive outcome is useful work at an acceptable total burden, including review and correction. A failed analogy that prevents a costly mistake may be as valuable as a successful recommendation.

<a id="S03"></a>

## 3 The architecture and its boundaries

The central analytical relationship is CoherenceLattice, Sophia and Atlas. CoherenceLattice constructs grounded analytical candidates; Sophia evaluates a fixed candidate; Atlas makes results, disagreement and eligible prior context understandable. This triad works within a larger system of intake, procedures, custody, controls and local resource ownership. It should not be read as three biological brain regions or a claim that three models are always required.

| Responsibility | Intended contribution | Boundary |
| --- | --- | --- |
| Sonya | Receive tasks, bind context, route supported adapters and capture returned material | Incoming content cannot authorize itself |
| Sonya node | Hold a participant's resources, accepted integrations and local policy | Participation does not transfer ownership to a network executive |
| Control Anchor | Let people configure, inspect, select, stop and recover supported work | A visible setting must reach the real deciding service |
| CoherenceLattice | Ground claims and preserve alternatives, mappings and residual questions | Structural validity is not semantic truth |
| Sophia | Evaluate a fixed candidate and preserve findings and dissent | Advisory findings do not grant execution or memory rights |
| Atlas | Orient the reader, explain results and compare eligible priors | Presentation and retrieval do not authorize retention or reuse |
| Executive | Maintain goals and coordinate finite delegated work | No self-granted power or unbounded replication |
| UCC and authoritative owners | Supply supported advisory assessments while separately enforcing technical operational protections | A business finding is not a prompt veto or authorization for external action |
| Custody and TEL | Preserve actual lifecycle evidence and its declared relationships | Neither is privileged access to hidden model thought |
| PMR | Govern optional retention and cross-task reuse | Retention, retrieval, injection and training are separate choices |

Sonya names a logical boundary, not a requirement that one process hold every credential. An implementation may separate gateway transport, authoritative custody and downstream quarantine. Those process boundaries must be documented and tested. A statement that one downstream step makes no provider call does not erase an earlier call elsewhere in the workflow.

Control Anchor should answer five everyday questions: What is running? Where does my data go? What resources does it use? Why is it allowed? How do I stop or change it? Text, graphs and structured views should describe the same accepted state. A changed selection must invalidate stale previews. A dashboard that displays a permission while a bypassing caller can evade it is insufficient; enforcement belongs at the actual action boundary.

The same product has two connection directions. A supported AI host or plugin can submit an explicit task to the authenticated native Brain; the native Brain can also send a permitted request through Sonya to a selected model or provider. Both directions use the same local policy and custody authority. A host integration does not intercept every unrelated chat message. Host drafts or paraphrases, exact observed inputs and native replies must remain distinguishable. Returning data to a cloud host is a disclosure and cannot be described as entirely local processing. See [Sonya F04](FAMILY_GUIDE.en.md#F04) and [complementary evidence F61](FAMILY_GUIDE.en.md#F61).

Shared context means the relevant task, evidence, assumptions, versions, rights and unresolved state travel together through authorized stages. It does not mean every participant receives every record. A challenge worker may need the proposed claim and selected evidence while remaining unable to read private background notes. Context sufficiency and minimum necessary disclosure must be considered together.

A role is distinct from the model filling it, the runtime serving that model, the task it receives and the output contract it must satisfy. Model replaceability requires actual checks of supported modalities, context limits, errors, disclosure behavior, licensing and access rights. Detecting an installed desktop application does not establish API authorization. A local model, a remote service and an autonomous agent may be useful participants, but each needs an admitted interface and a scoped grant.

Autonomous participants are welcome to propose work or cooperation. Their messages first enter as untrusted data. Communication alone grants no execution, persistence, replication or access to personal drives. Within an owner's delegated purpose, duration and resource limits, an admitted agent could carry out a finite sequence and report back. This preserves meaningful autonomy without creating open execution on any reachable machine.

<a id="S04"></a>

## 4 From claims to understanding

CoherenceLattice is intended to organize the relationship between a question, its evidence and candidate answers. It should preserve alternatives and expose where the supplied material supports, contradicts or fails to address a claim. This is more useful than treating fluent language as evidence. A source can be genuine yet irrelevant; an accurately copied number can still be used under the wrong units or assumptions.

Coherence retrosynthesis works backward from an outcome, discrepancy or residual question to candidate branches, counterhypotheses and distinctions that might explain it. For the garden example, an unexpectedly poor result could reopen the assumptions about shade, soil or scheduling. The present bounded route can operate on declared or scripted alternatives. General autonomous discovery of the right alternatives and their semantic usefulness remains a separate research and integration question.

Sophia's evaluation is bound to the actual candidate reviewed. A later edit must not inherit the earlier evaluation without an appropriate successor check. Its findings should state what was checked, which evidence was available and what remains unsupported. The design preserves question integrity, limited prior use, post-use influence review and bounded exploration. These duties help prevent a system from answering a convenient substitute question, importing a prior beyond its allowed scope or continuing a loop merely because it can.

A challenge should be substantive. If two workers depend on the same mistaken source, their agreement is not two independent confirmations. Repeated copies of one observation must not manufacture a quorum. Contrary evidence, missing measurements, stale data and out-of-domain conditions remain relevant even when a summary score looks favorable.

Atlas gives this work an understandable form. It can show the original question, options, support, objections, assumptions and permitted next actions. Its operational role includes prior orientation and comparison. The optional Atlas432 dictionary is a different function: a bounded contextual humanities reference whose meanings must be tied to a particular source and version. It can offer competing readings or refuse an inadequate match. It is not a taxonomy of people, an exhaustive ontology or a moral ranking.

The distinction matters in practice. Operational Atlas might compare two previously checked garden procedures. Atlas432 might support an optional interpretive discussion about the meaning of a community's imagery. Neither use should secretly write to long-term memory, and a dictionary relation score should not be presented as a calibrated probability.

<a id="S05"></a>

## 5 Memory that keeps what matters

Selective retention and consolidation are foundational to the design. A useful system should turn experience into reusable methods without requiring every future task to replay every earlier discovery. Earlier conceptual work described experience becoming refined methods; the PMR research program made constrained retention, graph-aware pruning, compression, quarantine, revocation and reduced representations explicit. The current explanation clarifies how these responsibilities belong together.

Thomas's walking example captures the intended intuition: a person does not consciously recall every lesson in learning to walk before taking a step. For Triadic Brain, the engineering proposal is to retain a bounded procedure or compact pattern together with its scope, assumptions, essential evidence and conditions for reconsideration. This is an illustration of proceduralization, not a claim to reproduce biological learning.

Memory has several responsibilities. Working memory supports the current task. Episodic memory preserves selected events. Semantic memory holds eligible knowledge representations. Procedural memory holds reusable methods. Prospective memory holds future intentions. Each needs an owner, a purpose, an appropriate retention period and current-use control. Listing these roles does not establish that all are implemented in a durable product.

PMR, the Provenance Memory Reservoir, concerns optional retention and reuse of eligible priors. It is distinct from mandatory task custody, which records what occurred within the declared operational boundary. A record needed for accountability may not be eligible for use in a new answer. A retained item may be stale, contradicted, restricted or pending review. Historical execution status and current usefulness are separate axes: changing present permission does not rewrite the original event.

Consolidation should preserve enough lineage for the claims still made. If a compact procedure depends on an otherwise low-scoring ancestor, graph-aware pruning may need to retain that ancestor. A hash-only record can support later identity checking but cannot reconstruct missing content. Exact replay, functional replay and a weaker witness of prior activity require different retained material and should not share an undifferentiated replay label.

The intended lifecycle includes keeping originals where necessary, retaining dependencies, producing a permitted compact derivative, archiving, quarantining, downgrading to a limited reference or deleting eligible material. User retention choices, affected-party rights and applicable obligations constrain these choices. Contradicted records may remain useful as negative evidence rather than quietly returning as recommendations. When context changes or an outcome conflicts with expectations, the system should reopen the relevant assumptions and request new grounding.

Pruning can release storage, RAM or scheduled capacity for other work. Information does not literally transform into computing power. Nor does consolidation automatically train a model's weights. Retrieval, procedure reuse, profile modification and model training are distinct processes with different permissions and evaluation needs.

### A prior moves through several distinct decisions

In the intended reuse route, [lineage query F68](FAMILY_GUIDE.en.md#F68) supplies an index and purpose-specific recommendation. [Retrieval F84](FAMILY_GUIDE.en.md#F84) returns eligible candidate material with provenance and allowed-use reasons. A [memory posture F85](FAMILY_GUIDE.en.md#F85) can label a proposal pending, quarantined or a candidate for retention; that label does not write it. [Question continuity F80](FAMILY_GUIDE.en.md#F80) checks which question the task is now answering. [Prior routing F81](FAMILY_GUIDE.en.md#F81) limits how the selected prior may enter that task, and [influence review F82](FAMILY_GUIDE.en.md#F82) examines its declared use afterward. The actual authorized owner, not these recommendations, performs any storage, disclosure or current-use transaction. [Lifecycle F69](FAMILY_GUIDE.en.md#F69) governs the later dependency-aware retention or revocation operation. A [retrosynthesis candidate F14](FAMILY_GUIDE.en.md#F14) may enter a supplied-prior comparison without implying that this whole chain has run.

These responsibilities can remain separate even when one implementation combines several in a process. Their exact current consumer joins are not all established. This is why a retrieval result, a review recommendation and a completed memory transaction need different records.

A concrete codec and a pure retention planner already provide narrower source mechanisms. They do not establish the full semantic consolidation lifecycle. The durable, authenticated consumer must still connect exact retained bytes, current authority, actual storage effects, later eligible use and visible influence evidence. This is where the foundational design becomes a testable end-to-end capability.

<a id="S06"></a>

## 6 A shared vocabulary that preserves differences

GUFT is used here in its maintained engineering sense: a typed, extensible cross-domain representation and research grammar. A common packet can carry a task's native evidence, units, uncertainty, residual, provenance, consent and refusal. The shared format should make relationships inspectable while preserving the source domain's meaning. Historical acronym expansions remain source-specific; this paper does not promote the name into a demonstrated physical unification theory.

Universal Coherence Mapping, or UCM, is a projection within that program. A projection is an additional view, not a replacement for native state. For example, a physical measurement and a cultural interpretation can both include uncertainty and provenance, but they do not thereby become the same kind of evidence. Different symbols or coordinates can also have different meanings across source versions. Units, estimator versions, transformations and limits must accompany quantities.

A vocabulary is useful partly because it can say that a mapping fails. The conserved design includes plural mappings, no adequate mapping, out-of-domain input and proposed new patterns. It also distinguishes missing observation, restricted observation and a predicate that does not apply under the present grammar. These conditions call for different responses. A privacy restriction is not evidence that a phenomenon is absent. An inapplicable category should not force a person or artifact into a misleading classification.

Hierarchical reference views, including historical 432-to-36-to-3-to-1 proposals, must preserve distributions, disagreement and residuals where those matter. Incommensurable axes cannot be averaged into a supreme score simply because the interface has room for one number. Proposed vocabulary growth should respond to recurring residuals or a demonstrated missing distinction, then face comparison with simpler alternatives, held-out cases and meaningful native interpretation. More categories alone are not progress.

AHA is the hypothesis and analogy workflow. It begins with a grounded donor structure and a target problem. It states what relation may transfer, which invariants should hold, what differs, how scale or context changes the claim, and what target observation would weaken or reject it. A queue-management pattern might suggest an arrangement for volunteer tasks, for example. Whether that pattern helps people coordinate fairly must be checked in the target setting; a structural resemblance is only a candidate.

The governed bridge preserves donor passages, target hypotheses, proposed insertions, contrary readings and interpretation. A useful evaluation compares the proposed transfer with an ordinary native solution, a donor-free alternative and relevant negative controls. A false but plausible analogy is particularly informative. Current structural work does not demonstrate general automatic donor discovery, semantic transfer or an efficiency dividend.

Rosetta preserves another boundary. Its observation bridge maps declared axes through a local adapter into typed observation, state, provenance and optional geometric or waveform views. Declared values are not automatically measured values. Off-basis residual and translation residual answer different questions. A synthetic waveform or reference frequency is an expressive representation, not a person's physical frequency or evidence of physical energy. These optional views must preserve the distinction between geometry, native meaning and source authority.

<a id="S07"></a>

## 7 Efficiency and the honest accounting of burden

Triadic Brain seeks to avoid repeated work where reuse is appropriate. It also seeks to avoid shifting hidden costs onto reviewers, donors or people with less power to refuse. The right question is whether a supported workflow produces a useful result at an acceptable total burden, not whether one isolated count becomes smaller.

The Total Action Functional, TAF, is a research objective spanning physical, informational and governance or coherence burdens. Its canonical formulation separates normalized terms and declared weights. A physical-action term requires an appropriate normalization; a domain without a meaningful physical-action measure needs an explicit domain surrogate rather than a borrowed unit. A score cannot override consent, privacy, refusal or a resource owner's limits.

Current bounded diagnostics and retained-byte explanations are narrower. A retained-byte proxy can explain how much selected representation is kept or charged under a declared accounting rule. It does not measure all physical work, human review, uncertainty or externalized harm. A provisional weighted runtime score is not the fully measured canonical TAF. Keeping both names and their scopes clear preserves useful instrumentation without overstating what it proves.

DeltaSyn supplies concrete compression and reconstruction mechanisms. In the examined standalone lineage, bounded donor matching and copy/residual operations can reconstruct specified representations and account for declared costs. Byte-exact reconstruction means the chosen bytes return exactly. Canonical-exact reconstruction concerns a specified canonical representation. Neither label, by itself, establishes semantic equivalence or improved cognition.

DSCC is a distinct specification and assurance lane. Its six-component frame accounting covers code, model, prior synchronization, provenance, residual and framing. The standalone DeltaSyn implementation has five accounting components: model, prior synchronization, payload, residual and provenance; package and evidence archive sizes are reported separately. A shared compression theme does not make these ledgers interchangeable or turn specified operations into implemented ones.

The pure PMR planner considers declared privacy, consent, replay requirements, criticality, revocation and enablement. It can recommend retaining an original, retaining dependencies, treating a representation as redundant or seeking review. A recommendation does not perform a storage transaction. Declared consent does not authenticate the person whose permission is required. The native consumer must check current authority at the actual commit boundary.

Compression claims must charge the information needed for reconstruction. A donor supplied out of band cannot disappear from the accounting. A pre-shared donor needs exact identity and an applicable sharing assumption; a bundled donor contributes its bytes. Negative gains remain valid observations. A smaller description is not a measurement of energy saved.

Performance evaluation should include preparation, retrieval, transfer, queueing, inference, encoding, decoding, verification, coordination, failures and human correction. Cold and warm conditions differ. Resource counts need a defined population. Physical energy needs appropriate instrumentation and matched boundaries. Quality, useful abstention, false confidence and accessibility belong alongside latency and memory use.

The intended pilot comparator evaluates supplied evidence for local and distributed task graphs. Replacement work begins with its own evidence rather than inheriting unavailable results. A real comparison requires actual observations, declared baselines and complete cost coverage. The broader freedom goal remains valuable even if a particular cooperative arrangement is slower than a centralized alternative.

<a id="S08"></a>

## 8 Governance that reaches the action

The human-governed system includes preauthorized autonomy. Its central requirement is that delegated action remains within a real, inspectable grant. It should not force a person to approve every harmless instruction manually, nor allow a broad goal to become permission for unlimited actions.

UCC names deterministic controls and supported finite procedures. User or institutional requirements are expressed as versioned profiles and connected to procedures the system can actually perform, or to explicitly identified human work. Unsupported prose must remain unsupported rather than being translated into an approximate check and labeled complete. A missing value, a false value, a failed check and a check that was never run are different outcomes.

Business-control assessments provide guidance for authorized review, not final professional findings. They do not block ordinary prompts, withhold actual replies, require review before ordinary continuation or authorize external business actions. Preserve the original automated finding, actual response and any authorized human conclusion separately. Technical authentication, protected custody, privacy, resource limits, safe execution and explicit capture-outage rules remain separately enforceable. A missing or unperformed analysis is neither a pass nor a justified “not applicable” result. A review requirement selected for a supported process remains visible without becoming a universal manual gate on ordinary work.

Source-faithful control authoring preserves original requirements, proposed interpretations, exclusions, conflicts and the version explicitly adopted. A model may help explain or draft a control but cannot activate it through generated text. Changing a draft should invalidate affected previews. A new policy can change future action without altering the recorded result of a past task.

moralWARE, also encountered as MORALware, is the normative and rights-governance family. It combines a chosen normative profile with separated proposal, Guardian review, evidence audit and deterministic guard responsibilities. Historical names such as LANTERN and ANCHOR describe parts of that staged design; ANCHOR in this sense is not the Control Anchor interface. The aim is accountable review with visible reasons and recourse, not a universal moral score. The full current-product moralWARE chain remains inactive and staged after the useful local loop; historical guard source does not establish an active protected-action consumer.

Sophia can supply a Guardian role, but the same evaluator cannot manufacture independence by approving its own work under another label. Evidence review should examine whether the warrant actually supports a proposed decision and whether the framing excludes affected people or important alternatives. Contextual policies can vary while core protections against falsifying evidence, impersonating a reviewer or silently widening authority remain explicit.

CECP retains its Critical Epistemic Continuity Protocol lineage and a concrete rights-floor-first assessment. It asks about necessity, proportionality, least harm, reversibility, continuity of essential services, burden bearers, due process, appeal and remedy. These questions help prevent a technically tidy optimization from imposing unacceptable costs on someone else. Accepted non-runtime semantics or a structurally valid assessment do not grant operational authority.

TIAIP is an optional trauma-informed review profile. The profile, a historical standalone application and a compatibility module are separate artifacts and do not inherit one another's qualification. In the Brain, the aim is an optional, user-controlled way to shape relevant review and disclosure. Bounded synthetic evidence is not clinical validation, diagnosis or proof of adequate care in a live setting.

The provider-neutral review core exists independently of that optional profile. It preserves findings, human decisions, repair requests, successor lineage, revalidation, recovery and exact decision-bound export. A repaired successor should be tied to the candidate and decision that authorized it. A human approval cannot erase a deterministic failure or make an absent procedure occur. In-process consume-once checks still need durable, cross-process support when the application can restart.

AEGIS covers admission and defensive containment. Its intended response is bounded and accountable: pause, quarantine, isolate a data path, preserve relevant evidence, suspend a scoped capability and notify an appropriate owner when explicitly preauthorized. A suspected event is not proof of motive or guilt. The design includes counterevidence, reviewer assignment and recusal, deadlines, safe interim states, remedies and restoration. Protecting a system should not create an unreviewable permanent exclusion mechanism.

EIR supplies a contextual interpretation and counterpoint lens, including jurisdiction, translation loss and correction. Interaction-autonomy review asks whether system behavior pressures, isolates or manipulates a person or undermines practical disengagement. Artifact review considers source, depiction, accessibility and lost meaning. These functions should help users exercise judgment, not replace it with a hidden central doctrine.

<a id="S09"></a>

## 9 What is observed and what is not

Custody preserves the actual task lifecycle within a declared capture boundary. It should retain attempts before admission, relevant request and response bindings, effective versions, errors, corrections and uncertainty. A reservation is not a completed inference. A captured response can coexist with failed processing or pending review. Reports must preserve those distinctions rather than combine incompatible counts into a success percentage.

Required custody is a minimized, access-controlled record under declared retention and deletion rules, not permission to keep every rejected payload forever. Credentials and root or task keys are excluded from ordinary event logs and public provenance. Where appropriate and sufficient, an accountability record may retain a non-content reference rather than the original payload, with the corresponding replay limitation. Exceptional retention must be explicit and justified; it is not implied PMR consent or a perpetual audit exemption.

TEL, the Thought Exchange Layer, records declared stages and evidence relationships. Where a result contract requires a graph snapshot, summary and event stream, those are distinct artifacts; a favorable summary cannot replace missing required events. TEL is not a transcript of private cognition and does not capture hidden chain of thought.

Available evidence channels must remain typed. Observed inputs, outputs and actions differ from exposed model explanations, provider-generated reasoning summaries, instrumented numerical signals and later analytical interpretations. A supported explanation channel may be retained when authorized, but its text is not guaranteed to be exhaustive or faithful internal causation. An unavailable observation cannot be filled with generated prose and relabeled measured evidence.

TAC, the Telemetry Aperture Controller, is a separate design for governed observation and sampling. It asks which resolution, time window and retention level are justified by uncertainty that could change a decision, while maintaining an appropriate audit floor. More sampling does not automatically authorize more retention, export or federation. Necessity, consent or an emergency basis established by the relevant authorized owner or applicable governance process, automatic downshift, tail retention, appeal and post-window review remain separate duties. Any emergency collection stays within a defined scope and duration; a model's own emergency assertion cannot expand access. Preauthorized defensive steps need not each await a fresh prompt. The current admission aperture is not equivalent to a deployed general TAC collector.

An optional characterization function, historically called **Coherence Event Signatures or CES**, supplies typed event-context features for comparison and trace. It belongs within [F30](FAMILY_GUIDE.en.md#F30) but is a distinct subfunction: TAC chooses permitted observation; CES characterizes an event from supplied information. Event identifiers, content hashes, analytical measures and cryptographic signatures are different objects. Current CES integration remains unresolved, and it is not a prerequisite for the local pilot. The [admission aperture F29](FAMILY_GUIDE.en.md#F29) is different again: its necessary gates are noncompensatory, meaning that a high score elsewhere cannot offset a failed consent or privacy requirement.

The Brain's provenance record should preserve the origin of a claim, the activity that changed it, attributable corrections and any known gaps. Each export should carry only the relationships its recipient may see; a source reference is not a retrieval grant. These are project requirements, not properties established by choosing a format. Related vocabulary: [W3C PROV](https://www.w3.org/TR/prov-overview/).

Receipts should be minimally useful to people as well as machines. A person should be able to expand a source, inspect a finding, request correction, understand retention, export an eligible record or recover a pending task without becoming a protocol specialist. Keyboard, screen-reader, low-vision and first-time usability need observation with actual users. Documentation alone cannot establish accessible recourse.

<a id="S10"></a>

## 10 Cooperation across user owned computers

A Sonya network is intended to connect independently governed nodes, sometimes described historically as a Sophia network. Each participant owns its resources and accepted integrations. Coordination can propose placement, but only the relevant owner can authorize and enforce it. A network executive is not a universal administrator.

Shared CPU, GPU and RAM mean scheduled work on eligible machines. RAM remains attached to an actual execution owner with limits, reservations and a lifecycle. Wi-Fi does not turn separate PCs into one transparent, latency-free, globally coherent memory space. A task that needs frequent synchronization may perform poorly across ordinary links; another that can divide into bounded independent work may be a better fit.

The initial target is a real two-node exchange, followed by a three-node Wi-Fi pilot. Useful evidence includes enrollment, authenticated identity, actual contribution, resource limits, cancellation, restart, lost replies and recovery. A simulated peer or a second process can test a component boundary but does not demonstrate an independently governed physical machine.

Storage and evidence distribution can use content-addressed objects, selective replication, gossip or torrent-like exchange. This need not require blockchain, a token economy or a public record of private activity. Content identifiers bind particular representations; their construction, chunking and encoding matter. They support integrity and retrieval, not secrecy, truth or permission. [IPFS content addressing documentation](https://docs.ipfs.tech/concepts/content-addressing/)

Three sharing tiers make the intended distinction practical. **Local** material stays under the node's declared local custody and processing rules. **Trusted-group** material is shared with selected recipients for an agreed purpose and retention policy. **Public** material is a separately reviewed derivative suitable for unrestricted audience access under its actual rights. These tiers are independent of execution trust: a public output could be computed locally, while a private task might use a specifically qualified confidential-computing route.

Metadata also needs protection. Names, timestamps, participation patterns, dependencies and guessable content can reveal sensitive information even when a document body is removed. A benign summary does not sanitize the logs or attachments in its package. The release decision must inspect the complete derivative and its metadata, not only its visible first page.

### Encryption and computation have different boundaries

Transport encryption protects a channel under its protocol assumptions. TLS is designed to provide authenticated, confidential, integrity-protected communication between endpoints, while leaving some traffic properties observable. Its protection does not hide plaintext from an authorized receiving endpoint. [TLS 1.3 specification](https://www.rfc-editor.org/rfc/rfc9846)

Disk encryption protects stored data in defined states and threat scenarios. BitLocker, for example, addresses exposure from lost, stolen or improperly retired devices. Ordinary disk encryption does not establish confidentiality from a privileged host while an authorized workload is processing plaintext. [Microsoft BitLocker overview](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/)

An ordinary virtual machine is not sufficient evidence that the host cannot inspect a workload. Confidential computing adds a distinct protected-execution and attestation lane, with hardware, software and deployment assumptions that must be qualified. Specialized cryptographic methods may support particular computations under their own protocols and costs. The design does not promise that every encrypted AI workload can run privately on any volunteered PC. [Microsoft confidential computing overview](https://learn.microsoft.com/en-us/azure/confidential-computing/overview)

The wallet analogy concerns protected key custody and scoped release. Keys should be bound to an exact task, recipient, workload and current policy, with recovery and revocation controls. A role credential is not automatically a task-encryption key. Source hashes and native role labels alone are not grants. A valid-looking receipt cannot substitute for the actual key owner's authenticated decision.

### Revocation and uncertain effects

Revocation must reach the actual commit point. A worker can check permission and then race with a revocation before disclosure or dispatch. A sound implementation needs current version bindings, atomic consumption where required and an authoritative way to reconcile the outcome. “Checked recently” is not always sufficient.

Cancellation before dispatch differs from cancellation after work may have begun. A lost acknowledgment may leave an outcome unknown. The system should inspect the original attempt rather than invent a fresh one and risk duplicate effects. Revocation can prevent future authorized use or release; it cannot guarantee erasure of data already disclosed to another party. Derived artifacts and retained dependencies need their own propagation and retention rules.

Practical exit means more than a leave button. Participants need permitted exports, clear remaining obligations, a way to stop new work and an honest account of copies outside their control. Cooperation should preserve these choices even when a participant contributes little compute.

<a id="S11"></a>

## 11 Human learning and the emergence question

The human analogy helps ask design questions without asserting that software is a biological brain. Internal operating conditions, external evidence, proposed actions and observed outcomes should remain distinct. A resource shortage can justify a smaller task or a pause; it cannot make a factual claim true. An executive can revise a hypothesis, seek evidence or propose an authorized action, but a plan does not establish that the action occurred.

Mark Solms and Karl Friston offer one relevant theoretical reference. In their 2018 paper, they connect biological self-maintenance, predictive inference, attention and affect. They describe precision as the estimated reliability of evidence or predictions and discuss how it changes the influence of prediction errors. They also describe consolidation into more automatic forms and the reopening of certain memories when predictions fail. These are the authors' claims about biological systems, not an evaluation or endorsement of Triadic Brain. Page references here identify the 26-page accepted manuscript, not the journal's printed pagination. [Solms and Friston, accepted manuscript, pp. 6–12 and 17](https://discovery.ucl.ac.uk/id/eprint/10057681/1/Friston_Paper.pdf)

The engineering inference is modest but useful: reusable procedures should carry their applicable context and reasons to reconsider them; evidence weighting should consider reliability rather than mere repetition; and updating an internal representation should remain distinguishable from changing the world. The project's deletion, consent, authority and retention rules are additional governance choices. They are not prescribed by the biological theory.

A software confidence statement is not automatically statistical precision. An information-theoretic objective is not a reading in joules. A Markov blanket is a statistical construction within a specified model, not a firewall or cryptographic protection. Those distinctions keep an analogy from becoming an unsupported engineering guarantee. [Accepted manuscript, p. 4 footnotes 6–7, pp. 6–7 and 13–14](https://discovery.ucl.ac.uk/id/eprint/10057681/1/Friston_Paper.pdf)

The wider vision is an environment in which people and specialized agents develop useful patterns of cooperation that were not individually scripted. Thomas describes an artificially natural construct: designed conditions within which iterative activity can produce unplanned organization. The system need not contain a hand-coded model of the entire universe to try learning and reusing bounded relations.

That vision leaves important questions open. An organism's cells, independent microorganisms and a host's microbiome are different biological cases; none maps directly onto software agents. Better coordination, a large network, self-description or procedural consolidation would not by themselves settle whether a system has subjective experience. Solms and Friston explicitly decline to attribute feelings to every dynamical system with a Markov blanket. Possible collective consciousness and the separately named singularity aspiration remain open questions, not inevitable milestones or prerequisites for a useful product. This edition defines no measured singularity threshold. [Accepted manuscript, p. 11](https://discovery.ucl.ac.uk/id/eprint/10057681/1/Friston_Paper.pdf)

A productive research program can still compare coordinated agents with single-agent, pooled-output and communication-ablated baselines under matched budgets. It can test whether reuse saves effort without losing quality, whether changed assumptions reopen a routine, and whether pruning preserves the evidence still required. These would establish specific engineering findings, not consciousness tests.

<a id="S12"></a>

## 12 Optional extensions and conserved research

The Brain should remain useful without activating every research family. Optional components must declare their dependencies, rights, input and output contracts, and effect boundaries. A historical release or source review does not automatically qualify a new integration.

Open Web Steward illustrates this distinction. It is a local static workbench for supplied facts, teaching capsules, user-pasted untrusted candidates, findings, human posture, a bounded repair successor and export. It is not a web crawler or a provider adapter. Its native checks remain important even when a generic wrapper presents the result. Older and newer contract versions require explicit semantic comparison rather than assuming that similarly named fields are equivalent.

CivicProof preserves an optional civic accountability and offline election-research lineage. Its existence does not confer authority over public decisions or establish a generic Brain runtime. IntegrityLock preserves integrity and version-bound evidence duties. A local review runtime provides bounded review artifacts. A governed sequence kernel preserves neutral validation, compilation, planning, rendering, terminal closure and receipting separately from optional compositions, including historically named Call Engine or Clavis content. Completed, refused, held and incomplete sequences each need an explicit terminal posture; recording closure is distinct from performing its required procedure. Neither a sequence description nor its closure receipt grants execution or content-use rights. Exact current kernel/consumer equivalence remains unresolved. Optional content must retain its own access and use rights.

Mathematical quantity registries, formal proof scaffolds and formula-to-consumer ledgers likewise have a legitimate place without becoming empirical validation. A theorem can be valid under its stated assumptions while its application is uncalibrated or its software consumer unqualified.

These distinctions conserve work rather than dismissing it. The function map makes optional, historical and unresolved responsibilities visible so they can be investigated or deliberately deferred. It also reduces the risk of rebuilding a mechanism whose source already exists or importing an old mechanism without its current authority and disclosure safeguards.

<a id="S13"></a>

## 13 Evidence and the delivery path

The project separates four kinds of statement. **Design intent** says what should be possible. **Implemented source** identifies a mechanism that exists in code. **Bounded qualification** records what happened for an exact candidate, input population and environment. **Installed or network evidence** demonstrates the connected experience on actual machines. Progress in one category does not silently complete another.

At this edition's checkpoint, selected cognitive-contribution and reuse components, Observer and Home paths, TAF service paths and package closure have bounded evidence in their recorded scopes. A pure supplied-prior comparator exists. An authenticated durable native reuse consumer and its lifecycle are being implemented rather than demonstrated as complete. Real installed cognition, full native isolation and the actual two-node and three-node Wi-Fi workflows remain unproved. The function appendix deliberately avoids converting component evidence into a completion percentage.

The practical sequence is local usefulness first. Supported host and native entry points should inspect the same effective task and policy history; a host's own incomplete transcript must not replace native evidence. Local usefulness should remain possible without a host subscription, PMR or peers, while live host integration has its own qualification scope. A maintained installed local entry point should accept a permitted task, invoke the selected supported runtime, preserve the actual result and show the user the corresponding evidence. A distinct follow-up should retain its context and parent relationship without implicit cross-task memory. A prospective policy change should affect future work while preserving older outcomes. Unsupported routes and missing evidence should remain visible.

Next comes a real two-node exchange with independently governed owners. It must demonstrate what was disclosed, what ran, where resources were consumed and how interruption is handled. The three-node Wi-Fi pilot then asks whether the connected cognitive workflow is useful, understandable and recoverable, including challenge and synthesis. These stages require adverse cases as well as a successful demonstration.

Memory reuse deserves its own connected proof: exact eligible prior bytes, authenticated current-use authority, actual custody effects, comparison or injection through the intended consumer, and a visible record of how the prior influenced later work. The ability to retain or compare a reference does not prove this complete lifecycle.

Research can proceed alongside these delivery stages. Transfer utility, semantic consolidation, adaptive role selection, confidential computation and large-scale federation need their own evidence. They should neither be advertised as finished nor become blanket prerequisites that prevent a useful bounded local workflow from being delivered.

Useful progress includes negative results. A rejected mapping, a compression loss, an unreliable metric or a difficult exit path can expose the next necessary improvement. The project should watch for narrative maturity growing faster than user capability, duplicate architecture replacing missing integration, and optimized scores concealing human burdens. Reliability, fairness and the ability to stop take precedence over maximizing engagement.

<a id="S14"></a>

## 14 An editable and multilingual design

The English master and machine-readable concept map are intended to evolve together. A change to a definition should identify the affected family, preserve earlier senses where needed and state whether it changes a design obligation, a research claim or an implementation description. The JSON is a public documentation counterpart, not a runtime schema or an authorization file.

The planned language editions should follow a stabilized source. Each edition should preserve family identifiers, distinguish maintained terms from explanatory translations and flag ambiguities rather than silently merging concepts. Review must pay particular attention to authority, consent, uncertainty, refusal, care and the distinction between possible and demonstrated capability. A fluent translation can still alter a crucial boundary.

Triadic Brain's conceptual and system-design authorship belongs to Thomas Prislac. AI assistance has supported organization, drafting, reconciliation and review. Neither AI-generated prose nor a cited research paper constitutes outside endorsement. The aim of this document is a durable, inspectable account that others can understand, question and improve without requiring its author to repeat years of design context.

The invitation is practical: help establish useful local capability, identify missing relationships, contribute accessible explanations, challenge unsupported claims and preserve the rights of the people involved. A cooperative Brain earns trust through understandable work and correctable evidence, not through the size of its vocabulary or the grandeur of its ambition.

<a id="APP-A"></a>

## Appendix A Conserved registry entries

This map preserves 86 heterogeneous registry entries. Its record-kind column prevents a historical document, principle or schema from being mistaken for an intended runtime capability. It does not claim that all historical materials have been read, every term has a unique mapping or every described capability is implemented. The accompanying JSON and linear family guide carry typed term senses, known functional inputs and outputs, authority limits, narrative pointers and entry-specific evidence or maintenance needs. Related-entry links are unordered, non-exhaustive editorial associations, not execution dependencies or proof of integrated interfaces. Names below are reader-facing labels, not API changes.

**Maturity key.** **Bounded** means selected component evidence within a declared scope. **Source** means selected current or historical source mechanisms exist. **Design** means a preserved responsibility without complete demonstrated behavior. **Research** means research, optional or unresolved mapping. None means whole-product or installed-network acceptance. Historical-lineage, historical-material and human/process labels describe non-runtime records, not additional maturity stages. The labels are not a completion ranking; source presence, definition reconciliation and qualification are separate axes in the family guide.

| ID | Registry entry | Record kind | Reported scope |
| --- | --- | --- | --- |
| F01 | [Triadic Brain](FAMILY_GUIDE.en.md#F01) | system scope | Source |
| F02 | [Historical integration lineage](FAMILY_GUIDE.en.md#F02) | historical lineage | Historical lineage |
| F03 | [Control Anchor](FAMILY_GUIDE.en.md#F03) | capability responsibility | Bounded |
| F04 | [Sonya ingress and adapters](FAMILY_GUIDE.en.md#F04) | capability responsibility | Source |
| F05 | [Sonya node](FAMILY_GUIDE.en.md#F05) | deployment entity | Source |
| F06 | [Cooperative node network](FAMILY_GUIDE.en.md#F06) | deployment entity | Design |
| F07 | [CoherenceLattice](FAMILY_GUIDE.en.md#F07) | capability responsibility | Bounded |
| F08 | [Coherence retrosynthesis](FAMILY_GUIDE.en.md#F08) | capability responsibility | Source |
| F09 | [Sophia](FAMILY_GUIDE.en.md#F09) | capability responsibility | Bounded |
| F10 | [Atlas orientation](FAMILY_GUIDE.en.md#F10) | capability responsibility | Source |
| F11 | [Publisher view](FAMILY_GUIDE.en.md#F11) | capability responsibility | Source |
| F12 | [Atlas432 contextual dictionary](FAMILY_GUIDE.en.md#F12) | optional profile or extension | Research |
| F13 | [PMR retention and reuse](FAMILY_GUIDE.en.md#F13) | capability responsibility | Source |
| F14 | [Retrosynthesis prior candidate](FAMILY_GUIDE.en.md#F14) | schema or vocabulary contract | Source |
| F15 | [GUFT typed grammar](FAMILY_GUIDE.en.md#F15) | research proposal | Source |
| F16 | [Universal Coherence Mapping](FAMILY_GUIDE.en.md#F16) | capability responsibility | Source |
| F17 | [AHA analogy and transfer](FAMILY_GUIDE.en.md#F17) | capability responsibility | Source |
| F18 | [Governed bridge workflow](FAMILY_GUIDE.en.md#F18) | research proposal | Research |
| F19 | [User designated executive](FAMILY_GUIDE.en.md#F19) | capability responsibility | Source |
| F20 | [Analyst Challenge and Synthesis](FAMILY_GUIDE.en.md#F20) | capability responsibility | Bounded |
| F21 | [Bound peer contribution](FAMILY_GUIDE.en.md#F21) | capability responsibility | Source |
| F22 | [UCC finite procedures](FAMILY_GUIDE.en.md#F22) | capability responsibility | Source |
| F23 | [AEGIS admission and containment](FAMILY_GUIDE.en.md#F23) | capability responsibility | Source |
| F24 | [moralWARE rights and normative review](FAMILY_GUIDE.en.md#F24) | crosscutting responsibility | Design |
| F25 | [Normative guard kernel](FAMILY_GUIDE.en.md#F25) | capability responsibility | Source |
| F26 | [Staged normative workflow](FAMILY_GUIDE.en.md#F26) | crosscutting responsibility | Design |
| F27 | [Guardian and evidence auditor](FAMILY_GUIDE.en.md#F27) | crosscutting responsibility | Design |
| F28 | [Thought Exchange Layer](FAMILY_GUIDE.en.md#F28) | capability responsibility | Source |
| F29 | [Admission aperture](FAMILY_GUIDE.en.md#F29) | capability responsibility | Source |
| F30 | [Telemetry Aperture Controller](FAMILY_GUIDE.en.md#F30) | capability responsibility | Design |
| F31 | [CECP continuity and rights assessment](FAMILY_GUIDE.en.md#F31) | optional profile or extension | Source |
| F32 | [TIAIP optional profile](FAMILY_GUIDE.en.md#F32) | optional profile or extension | Bounded |
| F33 | [Provider neutral review and recovery](FAMILY_GUIDE.en.md#F33) | capability responsibility | Source |
| F34 | [Contextual interpretation lens](FAMILY_GUIDE.en.md#F34) | research proposal | Research |
| F35 | [Authoritative custody](FAMILY_GUIDE.en.md#F35) | capability responsibility | Bounded |
| F36 | [Owner admitted cooperative execution](FAMILY_GUIDE.en.md#F36) | capability responsibility | Bounded |
| F37 | [Rights governed artifact exchange](FAMILY_GUIDE.en.md#F37) | capability responsibility | Source |
| F38 | [Owner controlled confidential release](FAMILY_GUIDE.en.md#F38) | capability responsibility | Design |
| F39 | [Role and effort selection](FAMILY_GUIDE.en.md#F39) | research proposal | Design |
| F40 | [Pilot evidence comparator](FAMILY_GUIDE.en.md#F40) | crosscutting responsibility | Design |
| F41 | [CivicProof extension](FAMILY_GUIDE.en.md#F41) | optional profile or extension | Research |
| F42 | [Integrity protection](FAMILY_GUIDE.en.md#F42) | crosscutting responsibility | Source |
| F43 | [DeltaSyn compression research](FAMILY_GUIDE.en.md#F43) | research proposal | Source |
| F44 | [Iterative repair and discovery](FAMILY_GUIDE.en.md#F44) | crosscutting responsibility | Source |
| F45 | [User governed contextual controls](FAMILY_GUIDE.en.md#F45) | crosscutting responsibility | Source |
| F46 | [TAF objective and diagnostics](FAMILY_GUIDE.en.md#F46) | research proposal | Source |
| F47 | [Bounded cognitive planning](FAMILY_GUIDE.en.md#F47) | capability responsibility | Source |
| F48 | [Purpose separated memory roles](FAMILY_GUIDE.en.md#F48) | crosscutting responsibility | Research |
| F49 | [Predicate applicability review](FAMILY_GUIDE.en.md#F49) | research proposal | Research |
| F50 | [Explicit mapping outcomes](FAMILY_GUIDE.en.md#F50) | schema or vocabulary contract | Research |
| F51 | [Distribution preserving aggregation](FAMILY_GUIDE.en.md#F51) | optional profile or extension | Research |
| F52 | [Rosetta observation bridge](FAMILY_GUIDE.en.md#F52) | optional profile or extension | Research |
| F53 | [Typed quantity namespaces](FAMILY_GUIDE.en.md#F53) | schema or vocabulary contract | Research |
| F54 | [Formula to implementation crosswalk](FAMILY_GUIDE.en.md#F54) | crosscutting responsibility | Research |
| F55 | [Cross domain transfer evaluation](FAMILY_GUIDE.en.md#F55) | research proposal | Design |
| F56 | [Operational self model](FAMILY_GUIDE.en.md#F56) | research proposal | Research |
| F57 | [Public interpretation tiers](FAMILY_GUIDE.en.md#F57) | crosscutting responsibility | Research |
| F58 | [Artifact centered contextual review](FAMILY_GUIDE.en.md#F58) | crosscutting responsibility | Research |
| F59 | [Source faithful control authoring](FAMILY_GUIDE.en.md#F59) | capability responsibility | Research |
| F60 | [Attempt and population accounting](FAMILY_GUIDE.en.md#F60) | crosscutting responsibility | Research |
| F61 | [Complementary observation surfaces](FAMILY_GUIDE.en.md#F61) | crosscutting responsibility | Research |
| F62 | [Session recovery and stale owner fencing](FAMILY_GUIDE.en.md#F62) | capability responsibility | Source |
| F63 | [Typed evidence channels](FAMILY_GUIDE.en.md#F63) | schema or vocabulary contract | Research |
| F64 | [Role and capability contracts](FAMILY_GUIDE.en.md#F64) | schema or vocabulary contract | Source |
| F65 | [Typed continuity relationships](FAMILY_GUIDE.en.md#F65) | schema or vocabulary contract | Research |
| F66 | [Typed provenance graph](FAMILY_GUIDE.en.md#F66) | schema or vocabulary contract | Research |
| F67 | [Accessible workflow receipt](FAMILY_GUIDE.en.md#F67) | crosscutting responsibility | Research |
| F68 | [PMR lineage query and recommendations](FAMILY_GUIDE.en.md#F68) | capability responsibility | Source |
| F69 | [Dependency aware memory lifecycle](FAMILY_GUIDE.en.md#F69) | research proposal | Research |
| F70 | [Relevance and novelty routing](FAMILY_GUIDE.en.md#F70) | capability responsibility | Source |
| F71 | [Governed sequence kernel](FAMILY_GUIDE.en.md#F71) | research proposal | Research |
| F72 | [Local first ownership](FAMILY_GUIDE.en.md#F72) | crosscutting responsibility | Research |
| F73 | [Qualified model substitution](FAMILY_GUIDE.en.md#F73) | crosscutting responsibility | Source |
| F74 | [Local review runtime](FAMILY_GUIDE.en.md#F74) | capability responsibility | Source |
| F75 | [Version bound replay](FAMILY_GUIDE.en.md#F75) | capability responsibility | Source |
| F76 | [Evidence linked progress discipline](FAMILY_GUIDE.en.md#F76) | crosscutting responsibility | Human/process discipline |
| F77 | [Interaction autonomy review](FAMILY_GUIDE.en.md#F77) | research proposal | Design |
| F78 | [Metric gaming controls](FAMILY_GUIDE.en.md#F78) | crosscutting responsibility | Research |
| F79 | [TCHES historical testing document](FAMILY_GUIDE.en.md#F79) | historical test material | Historical material |
| F80 | [Pinned question continuity](FAMILY_GUIDE.en.md#F80) | capability responsibility | Source |
| F81 | [Scope limited prior use](FAMILY_GUIDE.en.md#F81) | capability responsibility | Source |
| F82 | [Post use prior influence review](FAMILY_GUIDE.en.md#F82) | capability responsibility | Source |
| F83 | [Bounded exploration and stopping](FAMILY_GUIDE.en.md#F83) | capability responsibility | Source |
| F84 | [Eligible prior retrieval](FAMILY_GUIDE.en.md#F84) | capability responsibility | Source |
| F85 | [Memory intent review posture](FAMILY_GUIDE.en.md#F85) | capability responsibility | Source |
| F86 | [Formal assumptions and consumer parity](FAMILY_GUIDE.en.md#F86) | crosscutting responsibility | Source |

<a id="HIST-F79"></a>

### Historical testing material

F79 retains the legacy TCHES document reference. TCHES was used as a testing document; it is not an intended Brain capability, optional product or implementation target. Keeping this history does not assert a particular test procedure, consumer or result. No replacement function is invented to preserve a numerical function count.

<a id="APP-B"></a>

## Appendix B Knowledge waters and revisable inquiry

The project's **knowledge waters** language connects a practical approach to inquiry with a mathematical research program. A **corridor** is a possible line of inquiry. **Braiding** compares related lines while retaining their different evidence and unresolved disagreements. A **knowledge river** represents a sustained research direction. Its tributaries include repair, explanation, calibration and stewardship, not only prominent discoveries. A **terrace** is provisional stability: an assessment that can be reproduced within a stated scope and reopened when its evidence or assumptions change.

The cycle is not a ladder to final truth. Apparent stability can come from repeated assumptions, excluded counterevidence or suppressed novelty. A changed observation can reopen the question and produce a linked revision while the earlier evidence remains visible. Convergence is not correctness; repeated use is not independent support. A map of inquiry does not authorize action. A memory reservoir, where that analogy is used, concerns governed storage and possible reuse; it is not automatically the same object as a river or terrace model.

### A source-defined mathematical model

One graph-field formulation defines corridor flux and local alignment as:

```text
F_ij = w_ij ((C_i + C_j) / 2) (Θ_j − Θ_i)
A_i  = |Σ_j F_ij| / (Σ_j |F_ij| + ε)
```

Here C is a declared corridor-density variable, Θ a declared potential, w a graph weight and A an alignment ratio. The formulation uses aligned corridor transport and memory support in proposed river evolution. These symbols are not measured water quantities, truth probabilities or automatic authority. Their domains, estimators, units or normalization, parameter choices and empirical interpretation must be stated. The same symbol may mean something different in another formulation; terrace density, transparency and traceability must not be collapsed into one quantity.

A separate recursive description is:

```text
X_(n+1) = M ∘ S ∘ R (X_n)
```

It represents receptive intake, structuring and memory/continuity acting on an evolving state. These functional passes may span existing components. They are not a one-to-one renaming of Sonya, Sophia and Atlas or a requirement to use three fixed models. A spiral can illustrate revisiting a question with retained history; it does not establish that every cognitive trajectory inevitably spirals or converges.

### Keep the model implementation and evidence separate

| Material found in the design lineage | What it supports | What it does not establish |
| --- | --- | --- |
| Graph-field and recursive specifications | Substantive proposed mathematical definitions, including river/terrace dynamics and reopening | Calibrated observables, universal physical laws or beneficial cognition |
| Numerical and heuristic producers | Source contains particular update rules and diagnostic constructions | Equivalence among different producers or exact parity with the graph-field equations |
| Restricted algebraic proof terms | Substantive arguments for explicitly bounded quantities in declared formal objects | General river dynamics, calibrated meaning or a fresh compilation and axiom-closure audit |
| Theorem-style statements and formal scaffolds | Intended propositions and a place to make assumptions explicit | Completed proofs of the claimed dynamics; a placeholder proposition proves no field equation |
| Synthetic metrics fixtures | An illustrative shape or controlled example | Measurements of actual inquiry or independent validation |
| Advisory audit and presentation consumers | Source-backed responsibilities for review and display | A completed interoperable chain; producer and consumer shapes still need explicit reconciliation |

Two historical river producers use different data shapes: a simpler one derives a flow label from novelty, while a richer one emits river classes and separate risk dimensions. The examined auditor expects strength and capture-risk inputs that those outputs do not directly supply; missing risk records can be treated as zero risk. The presentation consumer expects another provenance and review-keyed shape. No reconciled adapter chain is established here. These are specific source-level compatibility gaps, not merely unperformed deployment tests, and none of the heuristic values establishes equivalence to the equations above.

For practical use, the proposed translation is **evidence-linked, revisable inquiry**: preserve alternatives, compare their constraints, keep unresolved differences visible and state what would change the conclusion. This draws on existing construction, review, presentation, memory and lineage responsibilities. It adds no new Waters organ and is not a prerequisite for useful local work.

The relevant existing entries are [F53](FAMILY_GUIDE.en.md#F53) for source-specific quantities, [F86](FAMILY_GUIDE.en.md#F86) for assumptions and implementation correspondence, [F07](FAMILY_GUIDE.en.md#F07) and [F09](FAMILY_GUIDE.en.md#F09) for related construction and review, [F10](FAMILY_GUIDE.en.md#F10) and [F11](FAMILY_GUIDE.en.md#F11) for explanation, [F63](FAMILY_GUIDE.en.md#F63) and [F66](FAMILY_GUIDE.en.md#F66) for evidence typing and revision lineage, and [F55](FAMILY_GUIDE.en.md#F55) for evaluating any claimed transfer benefit. These are responsibility links, not assertions that every historical producer is an adopted implementation of the current Brain.

<a id="REFERENCES"></a>

## References

Project component definitions in this paper are original design definitions and editorial reconciliations. General technical mechanisms and the biological analogy use the primary sources linked near the relevant claims:

- W3C. [PROV Overview](https://www.w3.org/TR/prov-overview/).
- IETF. *The Transport Layer Security Protocol Version 1.3*, RFC 9846. Channel protection and its endpoint assumptions.
- Microsoft. *BitLocker overview* and *Azure confidential computing overview*. Distinct storage and protected-execution threat models; citations do not imply platform selection.
- IPFS. *Content addressing*. Representation-bound identifiers and their construction; citation does not mandate IPFS adoption.
- Solms, M., and Friston, K. (2018). *How and why consciousness arises: Some considerations from physics and physiology*. **Journal of Consciousness Studies, 25**(5–6), 202–238. [Primary bibliographic record](https://discovery.ucl.ac.uk/id/eprint/10057681/). Manuscript-page citations in this paper refer to the separately paginated accepted manuscript.
