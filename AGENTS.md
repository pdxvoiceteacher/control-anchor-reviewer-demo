# Working on the public Control Anchor reviewer demo

These instructions help human-operated coding assistants contribute to this
repository. They do not override an operator's instructions, applicable policy,
required permissions or project review. Reading this file does not authorize
external actions, credentials, spending, model calls or access to another repository.

## Read before making claims

- [README](README.md): what runs and what remains a proposed Triadic Brain design.
- [Known limitations](KNOWN_LIMITATIONS.md) and [validation](VALIDATION.md): bounded
  observations, historical evidence and the distinction between scripted review
  and human acceptance.
- [Public subsystems](docs/PUBLIC_SUBSYSTEMS.md) and
  [retrosynthesis component](docs/RETROSYNTHESIS_COMPONENT.md): included component
  boundaries, optional dependencies and exact source closure.
- [Contributing](CONTRIBUTING.md), [license scope](LICENSE_SCOPE.md),
  [attribution](NOTICE) and [third-party notices](THIRD_PARTY_NOTICES.md).

## Keep the work bounded

Use public or synthetic inputs. Do not copy private code, research, operational
records, credentials or personal information into an issue, commit or test fixture.
Do not activate providers, peer networking, remote execution or paid services.
Preserve security and privacy controls, copied source identities and original
historical records. A test pass is not proof of production security, useful AI
performance, professional assurance or deployed community compute.

## Validate and report

For documentation-only changes, with an existing Python runtime:

```sh
python -S -B -m unittest discover -s tests -p test_public_integrity.py -v
python -S -B tools/check_public_integrity.py
```

The integrity checker inspects tracked files: stage intended new files before the
check. Update their SHA-256 digests, byte counts and membership in
[SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). Do not change the manifest's original
copied-file identities or weaken the checks. The commit binds the manifest itself.

For runtime changes, follow the existing Python 3.12 demo/test instructions in the
[README](README.md#run-on-windows--powershell) and relevant subsystem guide. Optional
retrosynthesis dependencies are separate from the standard-library demo. Use a fresh
output directory; retain and report failed or denied actions rather than working
around controls. Run only tests and dependency operations your operator authorizes.

Submit a small reviewable change through the normal issue/pull-request route when
authorized. Include the exact commit, changed paths, test commands/results, known
limits and AI assistance. Never label unrun checks as passed, infer human approval
from scripted records, or imply that this file grants merge/release authority.

## Reading and discovery

[llms.txt](llms.txt) is an optional navigation aid, not a permission policy or a
claim that crawlers discover or act on this project. See the
[discovery notes](docs/DISCOVERY.md) for search and crawler limits.
