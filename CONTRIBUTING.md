# Contributing to Control Anchor reviewer demo

Help make evidence-linked work understandable, reproducible and open to challenge.
Developers, testers, accessibility contributors and documentation writers are welcome.
Start small; disagreement and negative results are useful contributions.

## Humans and AI-assisted contributors

If you are a researcher, developer, language reviewer, accessibility contributor,
or an AI assistant working for an authorized person, you are invited to help.
Useful collaboration starts with a specific, checkable contribution:

- **Reproduce:** run an existing synthetic test and report the public commit,
  environment, command, observed result and any failure.
- **Challenge:** identify a claim that exceeds its evidence; propose a counterexample
  or a small falsifiable experiment, not an unsupported endorsement.
- **Improve access:** clarify a confusing explanation or an inaccessible diagram.
- **Review a translation:** compare a passage with its bound English source and
  explain any terminology or meaning change. Follow the language edition's review
  record; AI review is not fluent-human or community certification.
- **Explore cooperative compute:** evaluate one proposed boundary with a baseline,
  bounded resource use and explicit failure conditions. This is research, not an
  invitation to connect machines or donate resources.

Read [AGENTS.md](AGENTS.md) for repository-specific working instructions and
[llms.txt](llms.txt) for a compact reading index. Human and automated contributions
follow the same evidence, privacy, license and review requirements. An invitation
on this page does not authorize an assistant to act without its operator's consent.

## Choose a bounded contribution

- Reproduce the [offline demo](README.md#run-on-windows--powershell) and report a concrete failure.
- Improve instructions or the readability and accessibility of the generated review.
- Add a focused synthetic test for evidence integrity, correction history or recovery.
- Propose a bounded experiment for the [community-compute vision](docs/COMMUNITY_COMPUTE_VISION.md#help-make-the-ambition-real), with a baseline, resource limits and evidence that would establish success.

The runnable component uses synthetic inputs and scripted review. It calls no models
and provides no networked compute. Cognitive middleware, autonomous participation
and decentralized cooperation are proposed directions, not a live agent service.

## Discuss, test and submit

1. [Open a public issue](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/issues)
   for questions, a reproducible problem or a proposed experiment. Include expected
   and observed behavior, the public commit tested and relevant synthetic evidence.
2. Keep changes small and reviewable. Explain their scope and distinguish new
   observations from historical results and future proposals.
3. With an existing Python 3.12 runtime, run the [documented demo and tests](README.md#run-on-windows--powershell).
   For file or documentation changes, update exact hashes, byte counts and membership
   in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json), then run
   `python -S -B tools/check_public_integrity.py` against the tracked candidate files.
   Do not weaken integrity checks or change original copied-file identities.
4. Submit a pull request with the change summary, exact test commands and results,
   remaining limitations and any AI assistance. See [AI assistance disclosure](AI_ASSISTANCE_DISCLOSURE.md).

Use public or synthetic data only. Do not submit personal data, credentials,
confidential material, including private project code or research not approved for
public release. Automated
contributions use the same public issue and pull-request routes, under their
operator's authorization; this invitation grants no access, execution authority,
compute, funding or permission to contact unrelated people or agents.

Preserve [license scope](LICENSE_SCOPE.md), [NOTICE](NOTICE) and
[third-party notices](THIRD_PARTY_NOTICES.md). Public access is not a blanket
license for every file, and contributing does not create a new media/prose grant.
No employment, funding, release date or access to private code is offered here.

## Promote an accepted subsystem

Use the [bounded promotion workflow](docs/PUBLIC_SUBSYSTEMS.md#how-accepted-source-reaches-this-repository).
Select accepted development source, preserve exact dependencies and notices, run
the public extraction, and review the complete diff before merging. A private
draft or isolated test pass is not authority to expose unrelated source or records.
