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

## Follow-up: three portable package-source checks

A separate coordinated virtual run recorded **three passed test cases in 0.96
seconds** on a frozen package-source revision, using Debian, Python 3.12.14 and
pytest 9.1.1. One invocation ran under a 120-second bound with no retries. These
are additional package-source checks, separate from the 89 ComfyUI component tests;
they must not be added to that count or treated as current whole-product acceptance.

The cases checked exact package membership and current-byte closure, then the
actual package-recipe consumer's positive path and rejection when a receiving
module was omitted. Setup, call and teardown output was retained; this is three
test cases, not nine separately passed checks or raw phase-event receipts.

The run left source checkouts unchanged and removed its temporary fixtures and
virtual environment. It performed no package build, installation, child subprocess,
model/provider call or listener startup. It does not qualify a Windows installation
or execute ComfyUI. **The seven real ComfyUI checks above remain UNRUN.**

Saved-task request and grant handling is also under implementation in its existing
development lane. It is not a delivered capability of this public demo. At the
package-source checkpoint, proposed saved-task tests were not counted as executed
evidence.

## Follow-up: five native task-grant core checks

Five owner-selected task-grant cases ran on Linux against a separate frozen
revision: **five collected, five passed**, in one invocation with no retries.
Fifteen actual setup/call/teardown records were retained for those five cases;
they are lifecycle evidence, not fifteen passed tests. Independent bounded review
accepted the source, test, dependency, lifecycle and cleanup evidence. Synthetic
fixtures remain available for review.

The cases cover rejection for a wrong recipient, purpose or custodian; rebinding
and expiry; and revoked permission blocking new use while an exact existing
native request can still reconcile. This qualifies the tested native task-grant
core paths on that revision. Home/MCP resend behavior, saved-task UI, other
Windows cases, installed behavior, live peers, models and product acceptance
remain outside this evidence. These five results stay separate from both the
89 ComfyUI component tests and the three package-source checks. **The seven real
ComfyUI checks remain UNRUN.**

## Prospective maintenance research

Research is underway on governed maintenance candidates and an engineering spiral
that examines both error families and reusable opportunity families. A proposed
maintenance flow would combine bounded swarm engineering, independent review and
local consent. The research scaffold and proposed queue sequence are now recorded
for owner review; production adoption and runtime enablement remain pending. This
public demo does not implement automatic updates or that maintenance flow.
Analogies generate hypotheses for testing, not proof of a capability.

This update adds a sanitized status narrative only. It includes no integration
source, machine inventory, model weights or operational logs and grants no new
license. Public test badges and [validation evidence](../VALIDATION.md) continue to
describe this repository's synthetic offline demonstration, not private ComfyUI
or full-product qualification.
