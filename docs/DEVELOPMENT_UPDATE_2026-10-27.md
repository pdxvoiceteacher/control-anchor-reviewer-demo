# Development update — 27 October 2026

The optional ComfyUI integration has a later source-bound component checkpoint:
**89 focused model-free tests passed**, with no failures, errors or skips, and
**51 tested-file hashes** recorded. These are development-component results;
the public repository does not contain or independently reproduce that integration.
The [24 October update](DEVELOPMENT_UPDATE_2026-10-24.md) remains a historical
record of the earlier checkpoint. Counts from overlapping runs must not be added.

The new validation seam reuses the existing bounded JSON-object parser for literal
node inputs. Component tests cover valid objects and malformed, duplicate-key,
nonfinite, non-object and oversized inputs. Values supplied by links still require
runtime parsing. The validation hook does not invoke a provider, resource probe
or custody operation. These component tests do not establish how the actual
ComfyUI validator or executor handles every graph.

A separate seven-case harness targets ComfyUI's real prompt validator and executor
with a reviewed allowlist of pure nodes. Its planned checks include required
inputs, link types, deferred linked-value parsing, independent outputs beside an
invalid branch, and execution of existing pure workflows. **All seven real ComfyUI
checks remain UNRUN.** Backend execution and frontend visual import remain
separate qualification steps.

An isolated Linux attempt independently passed eight data-only admission fixtures,
then stopped at the resource guard because its process memory-limit mapping could
not be qualified. It stopped **before dependency installation or ComfyUI import**.
This is an environment blocker, not a failed ComfyUI workflow. The fixture results
overlap the component selection above and are not eight additional unique cases.
No model calls, preloads or server startup occurred in these checks.

The guard repair considers the process's memory-control membership, mount mapping
and visible ancestor limits. An unresolved mapping remains a refusal: locating a
visible process does not prove every hidden ancestor constraint. No threshold was
lowered and no layout exemption, remount or process migration was used. The next
runtime attempt requires a supported environment or execution-owner evidence that
establishes all applicable limits under the unchanged admission policy.

Live inference, measured GPU placement, actual human-approved export, a complete
reusable provenance library, full swarm behavior and installed Windows equivalence
remain unproved or incomplete. The shared-core adapter is an integration route,
not a sandbox for unrelated Python nodes. Provenance records identity and history;
it does not establish truth or turn repeated model roles into independent evidence.

This update adds a sanitized status narrative only. It includes no integration
source, machine inventory, model weights or operational logs and grants no new
license. Public test badges and [validation evidence](../VALIDATION.md) continue to
describe this repository's synthetic offline demonstration, not private ComfyUI
or full-product qualification.
