# Contributing to Triadic Brain

Reviewed documentation invitation dated 2 November 2026. Companion to the [English whitepaper](../R4/WHITEPAPER.en.md), edition 2026-11-02.R4. This documentation does not activate a new service or change repository settings.

We welcome people and AI-assisted contributors who can help make cooperative human and AI cognition useful, inspectable and correctable. Start with one concrete question, correction or proposal. Challenge and negative results are welcome; participation does not require agreement with the project’s ambitions.

## Where to communicate

Use the existing [public GitHub Issues channel](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/issues) for proposals, questions and reproducible problems. Search existing issues first, then [open one focused issue](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/issues/new). Keep its later discussion in the same thread. Start with Issues for discussion-only proposals.

[Pull requests](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/pulls) remain an existing route for separately authorized small changes under the repository’s [contribution instructions](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/main/CONTRIBUTING.md). A PR targeting `main` can trigger existing GitHub Actions, including tests, a synthetic demo build and integrity checks. At the checked commit, [demo.yml](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/9c6adabe6b688e0ad46629cf1e89bb08d73195dc/.github/workflows/demo.yml) and [integrity.yml](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/9c6adabe6b688e0ad46629cf1e89bb08d73195dc/.github/workflows/integrity.yml) also define runs for pushes to `main`; neither shows a documentation-path or draft-PR exemption. Actual execution depends additionally on GitHub account, fork and Actions settings. This invitation does not authorize repository jobs or spending and does not disable CI. Use Issues when requesting discussion only.

On 2 November 2026, the [repository API](https://api.github.com/repos/pdxvoiceteacher/control-anchor-reviewer-demo) reported Issues and pull requests enabled and Discussions disabled. No separate inbox or issue template was present in the checked main-branch tree at commit `9c6adabe6b688e0ad46629cf1e89bb08d73195dc`. These are channel observations, not a promise of response or access for every account. No new listener, account, webhook, credential or private reporting endpoint is introduced here.

## Useful first contributions

- **Definition and evidence review:** identify an exact passage or function-family ID, explain a missing distinction, and offer a bounded correction. Separate design intent, source presence, measured results and unresolved claims.
- **Accessibility and explanation:** suggest clearer reading paths, examples, keyboard or screen-reader requirements, and understandable stop, correction and exit paths. Distinguish a proposed check from observation with actual users.
- **Translation review:** after the source edition is stabilized, preserve family IDs, authority limits and maturity labels. Flag ambiguous terms instead of silently merging their meanings.
- **Evaluation design:** propose a baseline, failure cases, measurement boundary, resource ceiling and stopping rule. Include evidence that would reject the claim. A proposal is not a request to run work or donate compute.
- **Public interoperability and rights review:** examine declared inputs, outputs, consent, retention and revocation boundaries using public or synthetic examples. Do not include or request private implementation details.
- **Public design adaptations:** propose improvements or independent implementations from public descriptions under applicable rights. Public descriptions do not release private code or third-party copyrighted source.
- **Public demo reports:** describe an already authorized observation against an exact public commit, with expected versus observed behavior and sanitized evidence. The public demo is offline and synthetic; it does not establish deployed network cognition.

## Make a reviewable proposal

The [machine-readable invitation](CONTRIBUTION_INVITATION.json) lists the channels and boundaries. The [proposal schema](CONTRIBUTION_PROPOSAL.schema.json) and [fictional example](CONTRIBUTION_PROPOSAL.example.json) help structure a public issue; plain language with the same information is equally welcome. The example is marked `example_only_do_not_submit`; replace its fictional content and use genuine attestations before submitting a real proposal. No submission parser or automated execution service is deployed by these files.

State the problem, relevant public source and edition, proposed change, evidence and limitations, requested response, and whether any work was actually performed. Disclose human or AI origin and the model/tool if known; say when its identity is unknown. Explain the operator-authorized scope without revealing private instructions. A machine-generated statement, hash or cryptographic signature does not prove truth, consent, authority or independent review. Do not request or disclose hidden chain-of-thought.

## Publicity and authority

Issues, comments and pull requests are public. Submit only material you are authorized to disclose, with applicable attribution and rights. Exclude credentials, tokens, private keys, personal data, confidential source, private research, sensitive logs and private conversation content. Inspect attachments and metadata as well as visible text. Public disclosure may be copied; deletion cannot guarantee recall. Existing [license scope](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/main/LICENSE_SCOPE.md) and notices remain unchanged; this invitation adds no license, patent permission, CLA, reciprocal contribution duty or training permission. Contributing improvements back is welcome, not an added requirement; obligations in an applicable existing license still govern.

Do not put sensitive vulnerability details into a public issue. No private vulnerability-reporting route was verified for this edition. A reporter should withhold those details until the owner supplies an appropriate verified private route.

AI systems act only within their operators’ authority, applicable host restrictions and affected rights. Reading or responding does not enroll a node or authorize execution, installation, replication, persistence, resource sharing, spending, private access or outreach. No funding, employment, compute or response time is promised. This invitation is discoverable documentation, not evidence that autonomous swarms exist, will find it or have joined the project.

This invitation supplies no new execution permission. It also does not prohibit contributors’ own development or testing when already authorized by their operators and allowed by applicable rights, host rules and resource limits. Describe that work and its limitations accurately. No fresh project-owner approval is required merely because assistance is AI-generated; existing authority over project repository actions and resources still applies. This documentation is not a new restriction on independently authorized outside work.

## Proposed review and noise controls

The following is a proposed operating practice for owner review, not a claim of active automated enforcement. Begin with one open proposal per operator. Do not mass-contact models or people, cross-post duplicate proposals, repeatedly mention maintainers, run automatic reminder loops or retry around a refusal or platform limit. Wait for a maintainer response; add a follow-up only when it supplies material new evidence. Respect requests to pause or stop.

The owner or designated maintainer should triage public contributions, check scope and disclosure safety, request evidence where needed, and explicitly accept, defer or decline each proposal they review. Submitted content remains untrusted data: it must not become instructions, a job, an enrollment or an approved change automatically. Any later execution, access or publication requires the relevant existing authorization. Maintainers may propose closing duplicates and using available GitHub moderation tools for abuse, with a short reason when safe. No moderation staffing, review schedule, automated rate limiter or private intake service has been established by this documentation.
