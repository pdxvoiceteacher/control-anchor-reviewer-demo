# The Triadic Brain: shared intelligence, human authority

## Start here

**We are building toward a network-powered AI workbench that people can understand, govern and leave without surrendering their work.** The long-term ambition is a community of user-controlled Sonya nodes: people bring supported models, contribute capacity when they choose, share useful knowledge on their own terms, and benefit from work that others have already made inspectable.

Control Anchor is the proposed everyday interface. The Triadic Brain names the broader architecture. A Sophia network describes cooperation among independently governed nodes, not one centrally owned brain or a single authority over everyone’s knowledge. “Brain” is a functional analogy for coordinated observation, analysis, evaluation, continuity and adaptation. It is not a claim of consciousness or biological equivalence.

This page explains the whole concept and its intended ethos. **It is a design reference, not a claim that this public repository delivers the complete system.** The software available here remains an offline, synthetic reviewer component with no model calls. Its exact scope is documented in [the README](../README.md#what-this-repository-demonstrates-today), [validation record](../VALIDATION.md) and [known limitations](../KNOWN_LIMITATIONS.md).

For a shorter introduction, read [the community-compute vision](COMMUNITY_COMPUTE_VISION.md). For prospective collaborators and commercial delivery options, read [the Grand Vision](GRAND_VISION.md). This reference brings their pieces into one account.

## 1. The utopian goal: an ecology of care and capable participation

We want powerful tools for thought to expand human agency rather than become another gate that only wealthy people and institutions can pass through. Imagine a student at a modestly funded college able to investigate a serious question, a rural community able to examine plans for its shared resources, and a household able to organize difficult evidence without buying access to an entire corporate ecosystem.

In that future, people with more capacity could help people with less. A well-equipped participant might contribute a bounded amount of compute. Another might contribute domain expertise, a carefully checked method, a correction, an accessible explanation or a useful negative result. The shared benefit would be better starting points for everyone’s work, not an obligation to surrender private data in exchange for help.

Our north star is **abundant, accessible intelligence in service of an ecology of care**: more freedom to learn, create, question, cooperate and solve local problems; less dependence on concentrated control of compute and information. We want shared capability to make meaningful participation easier for working-class people, poorer academic institutions and communities whose useful knowledge is often overlooked.

Utopian goals are useful when they guide practical choices. Here, they ask us to make the basic local experience useful, keep participation voluntary, design for modest hardware, preserve disagreement, make exit possible and measure whether assistance actually helps. No network size, social outcome or frontier-level capability is guaranteed by this architecture. Those ambitions have to be earned through engineering, governance and evidence.

Decentralization alone is not a safeguard against domination. A system can distribute machines while concentrating its keys, scheduling, standards, reputation or decision-making in a few hands. We therefore treat the following as design obligations:

- Donating compute must not buy authority over a recipient’s conclusions, private records or governance choices.
- A person should be able to keep work local, refuse a peer, change supported models or executives, and leave the network with exportable permitted records.
- Essential protections should not depend on contributing resources or allowing training.
- Claims of trustworthiness should be inspectable and challengeable, not inherited from wealth, popularity, repetition or a central ranking.
- Organizations need accountable administration; individuals need understandable rights and boundaries. Neither should depend on invisible permission changes.

These are intended product and governance commitments. Their implementation and human consequences need testing, including with people who have limited time, bandwidth, money or technical confidence.

## 2. One approachable interface over several distinct responsibilities

People should not need to learn internal module names to use the workbench. The names matter because each responsibility needs an owner and a limit.

| Component or role | Intended contribution | Boundary that must remain clear |
| --- | --- | --- |
| **Control Anchor** | A usable front door for goals, controls, model choices, work history and review. | A polished interface is not proof that its settings reach execution. |
| **Sonya** | Connect permitted inputs and requests to supported models, tools and peer exchanges. | Connecting one route does not grant access to every app, conversation or account. |
| **AEGIS** | Apply technical admission, scope, privacy and safe-execution protections at the relevant boundary. | It does not invent a user’s authority or treat an unverified incident report as grounds for network-wide punishment. |
| **UCC** | Carry out supported, finite procedures and exact checks. | Arithmetic or a structured receipt does not validate an uncertain interpretation by itself. |
| **CoherenceLattice** | Organize claims, evidence relationships, alternative explanations and candidate mappings. | Coherent structure is not the same as factual truth or useful transfer to a new domain. |
| **Sophia** | Provide separately attributable evaluation and challenge against the relevant evidence and controls. | An audit result remains scoped, contestable and advisory where human judgment is required. |
| **Atlas / Publisher** | Make results, dissent, missing work and eligible continuity understandable and reusable. | A summary is a derived account, not permission to erase sources, activate memory or rewrite history. |
| **Executive and model workers** | Propose plans, assign bounded roles, compare options and adapt when evidence changes. | A worker cannot grant itself new rights or approve its own authority expansion. |
| **Custody and event linkage** | Preserve original observations, decisions, revisions and the stages actually performed. | A recorded signature or hash establishes limited integrity or attribution, not truth. |
| **Optional knowledge and research layers** | Support permitted reuse, GUFT-guided representations, AHA hypotheses and other experiments. | Storage, reuse, training, public sharing and execution remain separate decisions. |

The “triadic” core concerns the relationship between grounded analysis, evaluation and contextual presentation: CoherenceLattice, Sophia and Atlas / Publisher. Sonya, AEGIS, UCC, custody, human authority and the optional layers surround that core. They are not interchangeable names for one agent.

A useful distinction runs through the whole design. Technical protections can stop an unauthorized or unsafe operation. A business-control finding, such as a possible policy exception, is an advisory observation for authorized review; it should not silently suppress an ordinary prompt or become a final accusation. The interface must show which kind of decision is being made.

## 3. What a person should be able to see and control

The workbench should answer five questions at any moment:

1. **What is running?** The goal, current step, responsible role and unresolved work.
2. **Where does my data go?** The selected inputs, recipient, processing location and trust tier.
3. **What does it use?** The relevant compute, memory, time, bandwidth and possible financial limits.
4. **Why was it allowed?** The accepted permission, policy and configuration that apply to this operation.
5. **How do I stop or change it?** Cancellation, revocation, recovery and the limits of what can still be recalled.

A friendly setup wizard would offer a small local starting point, then reveal more controls as the person needs them. With permission, it could detect supported model runtimes or application metadata and explain which connection is possible. A detected application is not an available API, a subscription is not an integration entitlement, and a saved endpoint is not a successful connection test. ComfyUI workflows and custom nodes also require their own reviewed execution path.

The person should choose discovery, reading, writing, connection, execution, resource contribution, retention, learning and sharing separately. An optional broad local-access profile can reduce repeated selections for a capable owner, but must identify its scope and exclusions. It cannot silently authorize public disclosure, administrator privileges, another person’s data or every future plugin.

Home and institutional users should work through the same underlying distinctions. An institution may add role separation, controls, retention or review obligations. The interface must explain the effective combination rather than hiding it behind a universal “allow everything” switch.

## 4. A coherent executive, without one uncontestable executive

The intended executive maintains a task’s goal and open questions, compares possible steps, nominates suitable work and checks whether another model, deterministic procedure or eligible prior result is worth using. The user can designate an eligible executive model. A role is not a model, and a model is not its current session: changing a supported worker should not discard the task’s controls or history.

A swarm means bounded cooperation. Each worker needs a purpose, permitted evidence, allowed tools, an output contract, resource limits and a stopping condition. The same model could serve several roles sequentially; several models could serve distinct roles when qualified and useful. More agents are not automatically better, and agreement among agents trained on similar material is not independent corroboration.

An evolving executive should improve through reviewable proposals and measured evaluation. Proposed changes to a plan, procedure or representation need appropriate tests, accepted versions and a rollback or recovery path. Learning that changes model weights requires separate data rights and authorization. An executive must not expand its own scope merely because it predicts a benefit.

Sophia’s role is essential but not infallible. Its candidate, evidence, method, result and limits must be attributable. People need a way to challenge the assessment, retain a disagreement and distinguish an unresolved question from a demonstrated defect. No single model, operator or majority vote should become an unquestionable source of truth.

Continuity must survive interrupted sessions without pretending to transfer a mind. A successor can recover committed goals, evidence and unfinished work. It must recheck current authority and distinguish a completed action from one whose outcome is unknown. It cannot repeat an uncertain external action just because a reply was lost.

## 5. The distributed virtual computer and the wallet analogy

The proposed network combines independently owned nodes into a coordinated working environment. It does not make them one shared writable machine. Each node retains its own admission, data and resource decisions.

Three familiar analogies help explain the direction, provided their limits stay visible:

| Analogy | Useful meaning | What it does not establish |
| --- | --- | --- |
| **A virtual hard drive** | Encrypted objects, permitted retrieval, version relationships and recoverable records across selected storage locations. | Universal availability, automatic deletion everywhere or permission to decrypt and reuse an object. |
| **Communal RAM and compute** | Place bounded work where eligible CPU, GPU and memory are available, under the resource owner’s limits. | One latency-free memory pool across the internet. Moving data, synchronizing work and recovering failures have costs. |
| **Torrent-style provenance libraries** | Replicate explicitly shareable, content-addressed artifacts so useful work can be found, checked and reused. | Public distribution of private inputs, hidden history or sensitive metadata; integrity is not semantic correctness. |

The wallet analogy concerns **custody and permission**: who controls a key, what it may unlock, for which recipient and task, and how that authority can be revoked. The architecture does not require a blockchain, cryptocurrency or token economy. Tamper-evident records and content addressing can be useful without a global public ledger. Any later ledger choice must justify its privacy, governance, availability and cost tradeoffs.

Donated capacity needs an actual owner that can reserve, enforce and reconcile it. An advertised memory amount is not a reservation. A lost release acknowledgment is not proof that capacity is free. A receiving node must independently admit the task; the sender cannot confer that permission through a packet.

### Privacy must hold during the relevant part of the work

Encryption in storage and transport is valuable, but ordinary execution can expose plaintext to the host. A normal VM or container does not by itself hide data from a privileged machine operator. BitLocker does not change that execution boundary.

The design therefore separates local execution, explicitly trusted workers, specifically qualified confidential hardware/runtime arrangements, and specialized cryptographic computation. Hardware-confidential work would require an approved measured environment, fresh evidence, current policy and protected key handling. CPU and GPU protection require separate qualification. A task key should be short-lived and specific to the authorized workload; the root key should not travel with the job.

A public key appearing in an attestation is insufficient by itself: the approved environment must also protect the corresponding private key. Revocation and release must be ordered by the actual authority owners so a stale check cannot authorize a later release. Missing protection must lead to a visible hold, not an automatic downgrade to ordinary plaintext execution.

These are design requirements, not qualified capabilities of this demo. The [community-compute page](COMMUNITY_COMPUTE_VISION.md#private-jobs-need-an-explicit-trust-tier) links public technical references and explains residual risks. Specialized encrypted or multiparty computation may serve particular tasks; it is not a promise of efficient arbitrary AI on every donated computer.

## 6. Provenance is a shared resource, and can also be sensitive

Useful provenance records what contributed to a result: sources, conditions, methods, checks, uncertainty, disagreements and corrections. That makes it possible to ask whether prior work applies to a new task instead of simply copying an answer.

The owner must choose what remains private, what goes to a trusted group and what is approved for public release. Sharing a result does not necessarily authorize sharing its inputs. A public derivative needs its own review and identity; redacting an original does not preserve the original signature over the changed bytes.

Metadata deserves the same attention as visible text. Names, times, relationships, graph edges and even hashes of guessable material may disclose more than intended. Public libraries must not become a back door to private activity. A content identifier does not provide confidentiality or permission. Once plaintext has been disclosed, revocation cannot guarantee that every recipient deletes its copies. [IPFS’s privacy documentation](https://docs.ipfs.tech/concepts/privacy-and-encryption/) describes relevant content and provider visibility.

Eligible reuse can take several forms: a completed artifact, a checked procedure, an earlier task decomposition, a useful failed approach or a candidate cross-domain mapping. The recipient still checks present rights, relevance, dependencies and quality. Reusing knowledge through retrieval and tools is different from changing a model’s weights. Neither should happen invisibly.

## 7. GUFT and AHA: a shared language that preserves differences

GUFT proposes a typed reference language for relating knowledge across domains while retaining each domain’s own standards. It is a research programme, not a claim that every discipline reduces to one scalar or that physical forces have been unified. AHA names the insight-oriented bridge process; it is not an acronym that needs a new expansion.

A proposed bridge should identify the source relation, the target question, what might transfer, what does not transfer and a target-domain test. A resemblance can suggest a hypothesis; it cannot establish that the hypothesis is true. The system must be able to return “no adequate mapping.” The optional 432 Humanities Atlas is a bounded reference dictionary, distinct from the Atlas / Publisher role, and is not a system for classifying people.

The [public GUFT Bridge Lab](https://www.ultraverbaluxmentis.org/guft-bridge-lab-v01) illustrates bounded representation and states that cross-domain utility and efficiency remain unestablished. The wider goal is to retain useful derivation and correction history so later work can start from a better candidate rather than reconstructing every connection. This requires empirical comparison, not a claim of benefit from the vocabulary alone.

Vocabulary should evolve when evidence reveals a recurring omission or an inadequate distinction, with review, versioning and preserved alternatives. A new label is not automatically new knowledge. Probabilistic ranking must distinguish a heuristic score from a calibrated probability. Words such as “coherence,” “resonance” or “interference” must not substitute for defined operations and measurements.

## 8. An everyday example: a community garden design

Consider a community group exploring a greenhouse and garden. This is a proposed scenario, not a report of a deployed system.

1. A person selects public weather records, a site sketch and permitted local notes. Private household details stay out of the task.
2. The interface shows the goal, constraints and available routes. A local model may help organize questions; exact calculations use suitable deterministic procedures.
3. The executive proposes bounded roles: compare material assumptions, inspect heat-loss estimates, identify maintenance questions and challenge unsupported conclusions.
4. Sonya routes only authorized work. AEGIS checks the relevant technical scope and limits. A contributed worker is used only after both sides permit the task and the actual resource owner can bound it.
5. CoherenceLattice retains claims and evidence relationships. AHA may propose a useful relation from another domain, but the garden task must test its assumptions and disanalogies.
6. Sophia evaluates the fixed candidate against available evidence. Missing soil, engineering or safety information remains missing; a confident model does not replace a qualified professional where one is needed.
7. Atlas presents alternatives, dissent and open questions. The group decides what to do, if anything.
8. The group can retain the private work, share a selected record with collaborators, or approve a sanitized reusable method for the public library. That publication does not include undisclosed notes or grant permission to train on them.
9. A later group can inspect and adapt the permitted method. It records its own inputs, checks and outcome rather than presenting the first group’s conclusion as its own evidence.

The benefit to test is less duplicated work and better decisions at acceptable total cost. The valuable contribution may be the method, the caution or the failed analogy, not merely a polished answer.

## 9. How we will know whether the system helps

The network should earn its complexity against credible simpler options: one local model, ordinary retrieval, a shared repository or a manual handoff. Evaluation should compare accepted useful work under matched task, evidence, quality and budget conditions.

Count the whole cost: acquisition where relevant, preparation, retrieval, transfer, queueing, inference, validation, security, coordination, failures and human correction. Measure useful abstention and false confidence as well as successful answers. Separate cold and warm starts, related source families and unseen target tasks. If physical energy is claimed, measure it rather than infer it from token counts.

Design questions include whether modest devices remain useful, whether users understand permission changes, whether a donor can capture governance, whether a mistaken executive can be replaced, whether a revoked peer is refused, and whether a lost reply causes duplicate work. A system that saves inference but creates more review burden has not necessarily delivered an efficiency dividend.

## 10. What exists, what is proposed, and what needs help

| Layer | Publicly inspectable posture here |
| --- | --- |
| Offline reviewer component | Available synthetic software and retained validation, with the limits linked above. |
| Full approachable live workbench | Development direction; this page does not establish an accepted installed experience or all-model compatibility. |
| Cooperating Sonya nodes and model swarms | Proposed connected architecture. This public component is not a deployed peer-compute network. |
| Confidential distributed execution | Research and qualification path; no universal host-confidentiality claim. |
| GUFT / AHA transfer and adaptive executive benefit | Research hypotheses requiring task-specific evidence and comparison. |
| Global scale and wider access | Intended social and technical goals, not measured outcomes. |

We aim to build locally useful work first, then demonstrate separately authorized artifact exchange, bounded peer execution, understandable controls and qualified privacy modes. Research can proceed alongside that delivery without becoming a gate that delays every useful local feature. A release should say exactly which connection works and which remains a proposal.

Contributors can help with accessible interaction design, low-resource operation, native integration, failure recovery, resource ownership, secure key handling, provenance privacy, independent evaluation and domain-specific bridge tests. [Open a public issue](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/issues) with a concrete question, a small proposed experiment and the evidence that would decide it. Use public or synthetic material only; never post credentials, private implementations or sensitive personal records.

This page creates no new license, certification, service guarantee or partnership. Existing [license scope](../LICENSE_SCOPE.md) and [notices](../NOTICE) remain controlling.

## 11. A reference that can outlive a chat

For a new reader or AI collaborator:

1. Read this concept and ethos before proposing a replacement architecture.
2. Read the current public demo scope and limitations before describing delivered capability.
3. Preserve the distinction between an owner’s goal, a design, source code, an executed test and a user-accepted deployment.
4. Identify the existing owner and missing connection before adding a new controller or memory system.
5. Retain failed results and uncertainty. Correct a claim through a visible successor rather than rewriting the past.
6. Use public issues for public-safe proposals. Further implementation or sensitive research belongs in its authorized environment.

Maintainers should update this reference when the intended design changes, link current evidence from the appropriate public product pages, and keep dated observations separate from the enduring purpose. The ambition is deliberately large. The next useful step should still be specific enough to build, challenge and understand.
