# Contributing to Control Anchor reviewer demo

Help make evidence-linked work understandable, reproducible and open to challenge.
Developers, testers, accessibility contributors and documentation writers are welcome.
Start small; disagreement and negative results are useful contributions.

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
