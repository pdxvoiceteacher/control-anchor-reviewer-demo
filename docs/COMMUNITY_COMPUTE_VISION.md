# A Sophia network built for human agency

Read the companion [whole-system concept and ethos reference](TRIADIC_BRAIN_VISION.md) for the component relationships, five user-control questions, everyday example and explicit distinction between aspiration, design and evidence.

## The ambition

We aim to build the world's largest decentralized, community-governed compute network: a Sophia network of user-controlled Sonya nodes that makes increasingly sophisticated AI work available without requiring people to surrender control of their models, data or participation.

The goal is frontier-level communal capability, with the reach to serve households, communities and organizations around the world. We want people to have a meaningful alternative to concentrated control of compute and information. Local usefulness, voluntary cooperation and accountable recommendations are the foundation.

This is the direction we intend to earn through engineering and reproducible evaluation. Global scale and frontier-level capability are ambitions to test, not results already achieved. More connected machines or more model responses do not automatically produce better intelligence.

## Proposed design: local authority at every layer

These layers describe the high-level design we propose to build and test.

1. **User-controlled nodes.** A local workbench would let people choose supported models, permitted data, tasks and resource limits. Useful local operation would remain available without joining the network. A remote model or peer would receive only an explicitly permitted exchange, with the destination and data transfer visible to the user.

2. **Voluntary community participation.** Participants could offer eligible compute or share useful work under stated limits. Sharing an artifact, donating compute, retrieving prior work and permitting training would remain separate choices. Joining the network would not grant blanket access to a person's machine or information.

3. **Local admission and consent.** Each receiving node would check whether a proposed task or contribution fits its permissions, resources and accepted purpose. Users would retain the ability to decline work, stop future participation and change their choices. Limits must be enforced where effects occur; stopping future sharing cannot promise deletion of copies already disclosed.

4. **A user-designated Executive.** The Executive would compare available options and recommend a course of action: use a local model, retrieve eligible work, seek an independent check or request additional authorized compute. It should explain expected benefit, uncertainty and resource cost. Recommendations would stay within the user's delegated scope and could not grant themselves authority.

5. **Evidence and provenance.** Results would retain their origin, relevant conditions, review status and correction history so others can inspect and challenge them. A receiving participant would choose whether to use the work. Traceability helps establish what happened; correctness still needs evaluation.

6. **Resource-aware escalation.** Additional models, peers or compute should be requested because they are expected to improve a defined task, not merely because they are available. The design would account for latency, bandwidth, memory, energy and financial cost, as well as privacy and consent. When authority, evidence or budget is missing, the workflow should stop or ask.

## A friendly front door, from home use to institutional controls

The proposed Sonya setup wizard would begin with a practical question: **what would you like help with, and what may Sonya use?** A person could start with one task and selected folders, choose supported local or hosted models, and stay off the community network. Schools, research groups and organizations could build on the same controls with administrator policy, role separation, budgets, retention rules and review requirements.

With permission, the wizard would discover supported installed AI applications, model runtimes, selected model locations and ComfyUI installations. It would explain what was found, what can connect through a reviewed adapter, what remains unqualified and what needs separate setup. Installing an app or owning a subscription would not automatically grant an integration, model entitlement or API access. Connecting an AI app to Sonya tools and asking Sonya to run inference through a provider are different connections, with different permissions.

Discovery, connection, configuration and execution would remain separate steps. The wizard would not silently search credentials, copy another app's tokens, install missing extensions, download models or run workflows. A local address alone would not establish that processing stays local. Each selected route would show its processing destination, data exposure, resource needs and possible charges before use.

Permissions should be understandable without becoming an infrastructure specialist. People would choose read, write, execute and share rights separately, with visible limits and revocation. An optional **broad authorized local-access profile** could offer convenience across explicitly listed local folders and operations. It would still respect operating-system and organizational restrictions; it would not authorize internet export, privilege escalation or every future plugin. Sensitive actions and external sharing would retain their own checks.

For ComfyUI, the goal is to help people select a workflow, understand its nodes and models, and approve a bounded run through a qualified adapter. Metadata discovery and execution have distinct surfaces in [ComfyUI's server documentation](https://docs.comfy.org/development/comfyui-server/comms_routes). Custom nodes are executable extensions: metadata requests also need qualification, and discovering a node would not make it trusted. [Ollama's model-list interface](https://docs.ollama.com/api/tags) illustrates another useful discovery surface, not a claim of universal runtime compatibility. These are proposed integration directions, not a supported-product list.

## A distributed virtual computer, with real resource boundaries

We want people to combine useful capacity without giving up control of the computers they own. The proposed distributed virtual computer would coordinate approved work across Sonya nodes. Participants could offer bounded CPU time, GPU capacity and peer-local RAM, select eligible purposes, reserve capacity for their own use and pause future participation.

A coordinator would match a task to an eligible node; the receiving node would independently enforce its permissions and resource budget. Work would have a stated recipient, duration, memory and compute limits, output rules and cancellation behavior. Nodes disappearing, running out of memory or returning uncertain results must be ordinary recovery cases, not reasons to silently broaden authority or replay costly work.

Shared RAM means memory available to work placed on a peer. It does not make distant machines into one latency-free global memory pool. Model placement, data movement, bandwidth, synchronization and failures can outweigh added capacity. Useful workloads and measured end-to-end benefit must determine how far distribution goes.

### Private jobs need an explicit trust tier

The design calls for encrypted private jobs and outputs, with user-controlled keys and narrowly authorized recipients. Encryption during transport and storage is only part of that design. Ordinary execution needs plaintext somewhere, and the user must know who can see it.

- **Local or explicitly trusted execution:** plaintext stays on the user's selected machine or is disclosed to an explicitly trusted peer operator. An ordinary VM or container can help isolate workloads but does not conceal plaintext from a privileged host. BitLocker protects offline storage; it does not supply host-confidential execution. See [Microsoft's protection scope](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bitlocker-drive-encryption?view=windows-11).
- **Hardware-confidential execution:** eligible jobs would require qualified hardware, firmware and workload configuration, fresh attestation, and policy-controlled key release to the approved environment. [Confidential Containers' attestation architecture](https://confidentialcontainers.org/docs/attestation/architecture/) provides a public reference for that approach. CPU qualification would not establish GPU protection: [GPU confidential computing has its own hardware and software prerequisites](https://docs.nvidia.com/attestation/attestation-client-tools-sdk/latest/gpu_and_switch_attestation.html). This tier could not be promised on every donated PC.
- **Specialized cryptographic computation:** fully homomorphic encryption (FHE) or secure multiparty computation (MPC) may fit selected workloads, with workload, cost and trust assumptions evaluated separately. [Microsoft SEAL](https://github.com/microsoft/SEAL/blob/main/README.md) and [MP-SPDZ](https://github.com/data61/MP-SPDZ/blob/master/README.md) are public research and engineering references, not evidence that arbitrary AI workloads can run privately and efficiently across ordinary peers.

A confidential job must stop if its required protection cannot be established, rather than fall back to ordinary execution. Attestation narrows a trust decision; it does not certify application correctness, eliminate every side channel or guarantee availability. Key custody, recovery, rotation and revocation must be understandable and controllable by the user or their designated organization. Revocation should block future authorization and key release; it cannot retract plaintext already disclosed or guarantee immediate termination on an uncooperative peer.

## Provenance that people choose to share

We propose three distinct provenance layers:

| Layer | Intended audience and boundary |
| --- | --- |
| **Private** | Detailed work history retained under the owner's controls, with access and retention chosen for the task. |
| **Trusted** | A selected, purpose-limited record shared with named people or approved groups. |
| **Public** | A separately reviewed, sanitized contribution explicitly approved for public distribution. |

The public layer could use content-addressed distribution so recipients can identify the exact approved artifact, verify its integrity and follow corrections. It would distribute the approved public record, not the private job or its hidden history. Public receipts should not contain private inputs, credentials, identifying operational details or hashes that expose guessable secrets. Provenance metadata itself can reveal people, relationships, timing and activity.

Content addressing does not provide confidentiality, establish truth or erase independent copies. [IPFS documents the visibility of content identifiers and provider metadata](https://docs.ipfs.tech/concepts/privacy-and-encryption/); a public distribution design must account for those exposures before publication. Users would approve the sanitized payload and disclosure scope, not merely agree to “share provenance.” Corrections and withdrawal notices could travel forward, while already disclosed copies may persist.

No blockchain or token scheme is required for this architecture. The useful foundation is explicit authorization, verifiable records, appropriately protected keys and accountable participation.

## Build locally, prove cooperation, then widen participation

The first target is a dependable local workflow that people can understand, control and use. The next proposed step is a bounded exchange between independently administered nodes using public or synthetic data. Voluntary compute sharing would be evaluated separately from artifact exchange.

Before widening participation, the verification roadmap should establish:

- A setup flow that separates discovery from execution, refuses unsupported routes and makes permissions, processing locality and revocation clear.
- Bounded two-node work with public or synthetic inputs, tested quotas, disconnection recovery and cancellation without unapproved retries.
- Separate confidential CPU and GPU qualification, with rejection tests for stale or invalid evidence, revoked access and missing protection. Sensitive inputs would wait for these gates.
- Private-to-trusted-to-public disclosure review, including metadata leakage, recipient authorization and the limits of withdrawal.

These are proposed acceptance gates, not completed tests or a deployment schedule.

From there, staged interoperable implementations could broaden the range of supported devices and models. Each stage should publish reproducible comparisons against simpler alternatives: one local model, an ordinary shared library or a manual handoff. Evaluation should count useful task quality, failures, review burden and total resource cost, including coordination and verification overhead. Negative results and low-resource deployments matter as much as favorable demonstrations.

The [proposed roadmap](PROPOSED_ROADMAP.md) and [Grand Vision](GRAND_VISION.md) provide the broader direction. Timing depends on implementation and evidence; this page sets no guaranteed delivery date.

## What you can inspect today

This repository provides an **offline, synthetic reviewer component with no model calls**. It captures supplied evidence, performs deterministic checks, records scripted review, preserves linked revisions and exercises export, reopening and altered-copy rejection. It does not implement the proposed shared-compute network or establish frontier-model parity. See the [demo](../README.md#what-this-repository-demonstrates-today), [validation](../VALIDATION.md) and [limitations](../KNOWN_LIMITATIONS.md).

## Help make the ambition real

We welcome collaborators who can turn this direction into useful, testable work:

- **Engineering:** propose bounded interoperability, consent, resource-control and recovery experiments.
- **Reproducible evaluation:** define tasks, baselines and failure cases that can distinguish real benefit from added complexity.
- **Low-resource deployment:** help make useful workflows practical on modest hardware and constrained connections.
- **Usability:** test whether people can understand recommendations, inspect evidence and control participation without becoming infrastructure specialists.

[Open a public issue](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/issues) with a concrete problem, proposed experiment and evidence that would establish success. Use public or synthetic data only. Keep personal data, credentials, confidential material and private implementation or research out of issues and pull requests. This page shares the proposed direction, not private algorithms, schemas or unpublished implementation.

The repository's existing [license scope](../LICENSE_SCOPE.md) and [notices](../NOTICE) continue to apply. The ambition is large. We invite rigorous challenge and practical help in making it real.

