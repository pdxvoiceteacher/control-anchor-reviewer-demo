# A Sophia network built for human agency

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

## Build locally, prove cooperation, then widen participation

The first target is a dependable local workflow that people can understand, control and use. The next proposed step is a bounded exchange between independently administered nodes using public or synthetic data. Voluntary compute sharing would be evaluated separately from artifact exchange.

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

