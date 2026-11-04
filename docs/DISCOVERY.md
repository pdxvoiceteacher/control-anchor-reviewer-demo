# Finding, reading and contributing to Control Anchor

Control Anchor is the intended interface for the Triadic Brain design. This public
repository provides an offline synthetic Python reviewer demo, bounded component
source and research documentation. It invites human and authorized AI-assisted
contributions through [CONTRIBUTING](../CONTRIBUTING.md). It is not a live agent
network, an execution endpoint or a request to use anyone's machines or accounts.

## Reader entrypoints

- [README](../README.md): concise purpose, working demo and proposed architecture.
- [Brain map](brain-map/README.md): a linked directory separating code, reported
  development and proposals.
- [AGENTS.md](../AGENTS.md): working instructions for authorized contributors.
- [llms.txt](../llms.txt): optional compact navigation for tools or readers that
  choose to use it. This file neither initiates contact nor makes agents join.
- [CodeMeta](../codemeta.json): machine-readable project description; not a
  certification, ranking signal or replacement for path-specific license terms.
- [Technical manuscript](papers/triadic-brain-micro-spectrum/README.md) and
  [whitepaper](whitepaper/triadic-brain-20261102/README.md): source-bound editions
  and their language indexes. Translation availability and review status belong
  to each edition, not a blanket claim of certification.

When reporting or citing behavior, retain the exact Git commit and link to that
revision, rather than relying solely on mutable `main` links. Keep code behavior,
recorded tests, source reconstruction and research proposals distinct.

## What search optimization can establish

GitHub supports searching names, descriptions, topics and README content with
explicit search qualifiers. Relevant topics can help readers locate related
projects; they should describe actual subject matter rather than repeat keywords.
See GitHub's [repository search guide](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
and [topic guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).

Google recommends useful original content and ordinary technical SEO for its AI
search features. Its guidance states that `llms.txt` is not used for Google Search
ranking or visibility, and special AI schema is not required. The index here is a
reading convenience, not an SEO guarantee. See Google's
[generative AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

OpenAI distinguishes its search crawler, OAI-SearchBot, from GPTBot, which is used
for model training, and user-initiated ChatGPT-User fetches. Search accessibility
and training choices are separate. See the official
[crawler documentation](https://developers.openai.com/api/docs/bots).

## Hosting boundaries

A `robots.txt` file inside a GitHub repository would be ordinary repository
content; it would not replace the host's root crawler policy at `github.com/robots.txt`.
These documentation changes do not change GitHub's crawler controls, configure
GitHub Pages, submit a sitemap, verify a Search Console property or change
training permissions. On a separately controlled website, evaluate its actual
hosting, root crawler policy and indexing settings before claiming they are set.
See Google's [robots.txt guidance](https://developers.google.com/search/docs/crawling-indexing/robots/intro).

Publicly readable source and accurate metadata make inspection easier. They do not
prove indexing, ranking, AI citation, crawler visits or future contributions.
Do not manufacture traffic, endorsements or repetitive submissions to imply otherwise.

Guidance checked 4 November 2026; external services can change independently.
