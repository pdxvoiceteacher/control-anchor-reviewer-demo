# Explore the Triadic Brain

[Back to the front page](../../README.md) · [Detailed product crosswalk](../PRODUCT_MAP.md)

![Techno brain with nine numbered function families; equivalent descriptions and links follow.](brain-map.svg)

**Reviewed 2026-11-03.** Public component code and dated public descriptions only. Not a whole-product completion score or a live development tracker.
Public source baseline: `51e5275f14d3b05e01cb0ee69be5819d6b9a611c`. Development descriptions retain their own dated evidence; this date does not requalify them.

- **CODED · public main:** bounded implementation in this offline synthetic repository, not the whole Brain.
- **DEVELOPMENT · reported:** broader components or integration work; any bounded public subcomponent is identified separately below.
- **PROPOSED · design / research:** broader intended behavior, even where smaller foundations exist.
- **UNKNOWN:** missing or uninspected proof stays unknown. No status implies production readiness.

## Choose a family

1. [Evidence & custody](#evidence) — CODED · public main
2. [Controls & authority](#controls) — CODED · public main
3. [Review & correction](#review) — CODED · public main
4. [Grounding & analysis](#grounding) — DEVELOPMENT · reported
5. [Evaluation & posture](#evaluation) — DEVELOPMENT · reported
6. [Workbench & providers](#interface) — DEVELOPMENT · reported
7. [Continuity & memory](#continuity) — PROPOSED · design / research
8. [Community compute](#community) — PROPOSED · design / research
9. [Learning & research](#research) — PROPOSED · design / research

<a id="evidence"></a>

## 01. Evidence & custody

**CODED · public main**

Retain captured inputs, canonical records and a hash-linked history in the offline demo.

**Boundary:** Logical checks in one process. No independent custody, signing, source-truth guarantee or full native runtime is demonstrated.

- [Code: captured transactions](../../src/triadicbrain/assurance/transaction.py)
- [Code: custody verification](../../src/triadicbrain/assurance/custody.py)
- [Function crosswalk](../../docs/PRODUCT_MAP.md#actual-included-function-crosswalk)

[Back to family directory](#choose-a-family)

<a id="controls"></a>

## 02. Controls & authority

**CODED · public main**

Logical authority checks and the bounded UCC plan engine are public. UCC runs declared predicates over supplied data and retains PASS, FAIL, HOLD and NOT_EXECUTED distinctions.

**Boundary:** Supplied-field checks do not establish source truth or professional compliance. Human procedures remain unexecuted; no operating-system enforcement or installed integration is claimed here.

- [Code: controls](../../src/triadicbrain/assurance/controls.py)
- [Code: authorization](../../src/triadicbrain/assurance/authorization.py)
- [Code: review policy](../../src/triadicbrain/assurance/review_policy.py)
- [Code: bounded UCC plans](../../src/triadicbrain/assurance/ucc_plan.py)
- [Run the UCC component](../../ucc_demo.py)
- [Vetted subsystem promotion](../../docs/PUBLIC_SUBSYSTEMS.md)

[Back to family directory](#choose-a-family)

<a id="review"></a>

## 03. Review & correction

**CODED · public main**

Scripted review decisions, a separate repair child, export/reopen and one interrupted-decision recovery are exercised by the demo.

**Boundary:** The human decisions are scripted; the original findings remain. This is not actual human acceptance, learned improvement or a professional conclusion.

- [Code: transaction and recovery](../../src/triadicbrain/assurance/transaction.py)
- [Code: export and views](../../src/triadicbrain/assurance/web.py)
- [Tests: component cases](../../tests/test_component.py)
- [Observed evidence](../../VALIDATION.md)

[Back to family directory](#choose-a-family)

<a id="grounding"></a>

## 04. Grounding & analysis

**DEVELOPMENT · reported**

The public retrosynthesis component runs bounded CoherenceLattice source grounding, proposal validation and supplied-prior comparison. Broader grounding and cognitive analysis remain development components.

**Boundary:** This is a synthetic component demonstration, not qualification of all bundled support modules, full CoherenceLattice execution or installed integration. Supplied data is not an independently established source of truth.

- [Code: bounded source grounding](../../components/CoherenceLattice/python/src/coherence/totality/grounding.py)
- [Run the retrosynthesis component](../../retrosynthesis_demo.py)
- [Runtime and qualification scope](../../docs/RETROSYNTHESIS_COMPONENT.md)
- [Responsibilities and role boundaries](../../docs/PRODUCT_MAP.md#local-workbench-workflow-and-role-boundaries)
- [Connections and proof obligations](../../docs/DEVELOPMENT_UPDATE_2026-10-30.md#provisional-connection-map)

[Back to family directory](#choose-a-family)

<a id="evaluation"></a>

## 05. Evaluation & posture

**DEVELOPMENT · reported**

The public retrosynthesis demo invokes Sophia reconstruction checking against actual CoherenceLattice output. Full Sophia governed evaluation and Atlas explanation retain broader development responsibilities.

**Boundary:** Reconstruction checking is a narrow executed path, not a complete Sophia evaluation. Included import dependencies are not blanket behavioral qualification; no whole-system or installed-runtime pass is claimed.

- [Code: Sophia reconstruction check](../../components/Sophia/python/src/sophia/triadic/governed_evaluation.py)
- [Executed scope and limits](../../docs/RETROSYNTHESIS_COMPONENT.md)
- [Roles and limits](../../docs/PRODUCT_MAP.md#local-workbench-workflow-and-role-boundaries)
- [Whole-product vision](../../docs/TRIADIC_BRAIN_VISION.md)

[Back to family directory](#choose-a-family)

<a id="interface"></a>

## 06. Workbench & providers

**DEVELOPMENT · reported**

Control Anchor interfaces, authenticated task intake, provider selection and retained outcomes are described in dated development checkpoints.

**Boundary:** Source, injected-boundary tests and hosted installation evidence have different scopes. No installer, live model invocation or current installed acceptance is supplied by this map.

- [Interface directions](../../docs/PRODUCT_MAP.md#two-interface-directions-one-local-authority)
- [Dated connection update](../../docs/DEVELOPMENT_UPDATE_2026-10-30.md)
- [Known public-demo limits](../../KNOWN_LIMITATIONS.md)

[Back to family directory](#choose-a-family)

<a id="continuity"></a>

## 07. Continuity & memory

**PROPOSED · design / research**

Opt-in comparison against explicitly supplied prior hypotheses is now public. Eligible retrieval, durable memory and restart-aware continuity remain broader design goals.

**Boundary:** The comparison performs no prior lookup, retention, provider dispatch or context delivery and grants no authority. Synthetic permits do not establish authenticated authorization; retention is not training consent.

- [Code: supplied-prior comparison](../../src/triadicbrain/assurance/retrosynthesis_reuse.py)
- [Run and inspect the comparison](../../docs/RETROSYNTHESIS_COMPONENT.md)
- [Memory and continuity connections](../../docs/DEVELOPMENT_UPDATE_2026-10-30.md#provisional-connection-map)
- [Privacy-aware lifecycle design](../../docs/design-notes/2026-11-03-refinements.en.md)

[Back to family directory](#choose-a-family)

<a id="community"></a>

## 08. Community compute

**PROPOSED · design / research**

Voluntary, locally governed Sophia cooperation is the network vision. Dated bounded peer experiments are groundwork, not an operating shared-compute service.

**Boundary:** Distributed execution, independent participants and practical usefulness remain separate proof obligations. This public demo performs no networked compute.

- [Community compute vision](../../docs/COMMUNITY_COMPUTE_VISION.md)
- [Dated peer evidence and limits](../../docs/PRODUCT_MAP.md#evidence-edition-and-remaining-joins)

[Back to family directory](#choose-a-family)

<a id="research"></a>

## 09. Learning & research

**PROPOSED · design / research**

Adaptive attention, analogy, recursive review and measurement proposals are research directions, not established improvements.

**Boundary:** No general learning, consciousness, speed, cost or scientific benefit is established by design descriptions or test totals. Negative and unknown findings remain relevant.

- [Research lineage and evaluation](../../docs/RESEARCH_LINEAGE_AND_EVALUATION.md)
- [Public micro-spectrum paper](../../docs/papers/triadic-brain-micro-spectrum/README.md)
- [Whitepaper and companions](../../docs/whitepaper/triadic-brain-20261102/README.md)

[Back to family directory](#choose-a-family)

## Optional browser explorer

GitHub renders this directory as Markdown. The front-page graphic opens this directory; the numbered family links are the clickable controls. The graphic itself is a static image, not an interactive SVG embedded in GitHub.

For the interactive graphic, download [explorer.html](explorer.html) and open it in a browser. It is self-contained, has no scripts or external assets, and uses ordinary keyboard-accessible links. Source links open this public repository at the reviewed baseline. No GitHub Pages site is enabled or required.

## Maintain this map

Edit [map.json](map.json), then run `python tools/build_brain_map.py` from the repository root. Run `python tools/build_brain_map.py --check` and `python -m unittest discover -s tests -p test_brain_map.py`. Update the source manifest using the repository's normal publication process. Preserve prior publication metadata and historical evidence.

A status change needs evidence for that specific scope. Do not promote private development to public-main code, treat a document as implementation, or imply that a new review date proves a fresh runtime result. No private source links, operational records, hosted analytics, external scripts or paid services belong in this map.
