#!/usr/bin/env python3
"""Build navigable Markdown and machine-readable edge ledgers from public-safe sources."""
from pathlib import Path
import json,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent.parent
D=json.loads((P/'source/architecture-data.json').read_text());R={r['id']:r for r in D['records']};M={m['id']:m for m in D['modules']};recipes=json.loads((P/'source/diagram-recipes.json').read_text())['diagrams'];focus=json.loads((P/'source/focused-flows.json').read_text())['diagrams']
def link(r):return f"[{r['id']} {r['name']}](modules/{r['primary_module']}.md#{r['id']})"
def source(r,level=1):return '../'*level+r['source_anchor']
head='''# Triadic Brain visual architecture atlas

**Draft documentation for review.** This atlas positions the conserved registry by responsibility, record kind and source status. It does not claim that every responsibility is a separate executable module or that every drawn join is implemented.

The registry contains **86 mixed-kind records**, not 86 or 85 completed functions. Each ID has one primary editorial home; references in focused views do not duplicate capabilities. **F01** is the whole-system composition. **F02** and **F79** are historical records outside capability diagrams. TCHES is a historical testing document, not a Brain feature or a future heat-system implementation.

![Whole-system responsibility and connection map](png/00-overview.png)

[Open scalable overview](svg/00-overview.svg) · [Full text alternatives](TEXT_ALTERNATIVES.md) · [Complete placement ledger](PLACEMENT_LEDGER.md) · [Machine-readable ledger](source/architecture-data.json)

## Read connections correctly

- **Dashed arrows:** declared intended or research relationships; not implemented-edge evidence.
- **Solid arrows in the source-path view:** a caller and accepting consumer were inspected in source. This is not execution, installed or human acceptance evidence.
- **Teal:** data. **Amber:** control or current-owner constraint. **Purple:** provenance or recorded outcomes. A control arrow does not create authority.
- **REF boxes / focused nodes:** secondary references to the primary home, not new registry functions.
- **B:** selected bounded component evidence. **C:** selected current/historical source. **D:** design. **R:** research/optional/unresolved. **P:** human process. **H:** historical material. These are not a completion ranking.

A source file, a bounded component qualification, an unresolved join and a research responsibility are separate dimensions in the ledger. The public documentation does not contain underlying private execution receipts.

## Module navigation

Primary homes below are **proposed editorial responsibility groupings**, not an assertion about the current package tree or authenticated service owner. Contracts, profiles, lenses, deployment scopes, process vocabulary and optional branches retain those kinds.

| Home | Responsibility area | Primary records |
|---|---|---|
'''
for m in D['modules']:
 head+=f"| [{m['id']}](modules/{m['id']}.md) | {m['title']} | {', '.join(m['ids'])} |\n"
head+='''
## Focused connection views

| View | What it clarifies |
|---|---|
| [Source-connected cognitive route](svg/10-source-connected-cognitive-route.svg) · [PNG](png/10-source-connected-cognitive-route.png) | WORK, separate DISPATCH, JOINED analysis, separate evaluator, custody acceptance, Atlas/TEL and inspection. |
| [Prior-comparison boundary](svg/11-comparison-boundary.svg) · [PNG](png/11-comparison-boundary.png) | Existing pure comparison versus the unmerged/unqualified native custody/current-use join. |
| [Intended cognitive loop](svg/focus-cognitive-loop.svg) · [PNG](png/focus-cognitive-loop.png) | Candidate/review/orientation feedback and separate history. |
| [Authority and revocation](svg/focus-authority-revocation.svg) · [PNG](png/focus-authority-revocation.png) | Advisory findings, actual decision owners, revocation and stale-owner recovery. |
| [Memory lifecycle](svg/focus-memory-lifecycle.svg) · [PNG](png/focus-memory-lifecycle.png) | Custody, posture, retention, retrieval, current use and lifecycle are separate decisions. |
| [Intended three-node cooperation](svg/focus-three-node.svg) · [PNG](png/focus-three-node.png) | Each independently governed owner admits work; returned data still needs local current-use admission. |
| [Knowledge waters](svg/12-knowledge-waters.svg) · [PNG](png/12-knowledge-waters.png) | A bounded research overlay for revisable inquiry, not a new organ, literal fluid law or measured performance graph. |
| [Historical provenance register](svg/13-provenance-register.svg) · [PNG](png/13-provenance-register.png) | Historical lineage and testing-document records are not a capability backlog. |

## Source and scope

The core record descriptions are bound to a snapshot of the **2026-11-02.R5.1 frozen English source** concept map. The snapshot hash and status are in `source/architecture-data.json`. Guide/narrative anchors are retained as logical snapshot references rather than dead links to an unintegrated or wrong edition. The source-path supplement is a separate static inspection; it does not upgrade family maturity. Exact private source paths and repository locators are kept outside this public directory.

`source/diagram-recipes.json` contains editable lane layouts. `source/module-flow-edges.json` retains the intended arrow source bindings. `source/source-connected-edges.json` retains static-source status and boundaries. `source/focused-flows.json` and the DOT files retain all focused edges. No numeric performance or completion chart is included because no suitable measured dataset was established for this atlas.

[Build and verify locally](BUILD.md). No external rendering service, network access, installations, runtime/provider calls, CI runs or paid resources are needed.
'''
(P/'README.md').write_text(head)
ledger=['# Complete primary-placement ledger','','One primary editorial home per stable ID. Secondary links below are **source editorial associations**, not runtime dependencies or implemented-flow proof. Detailed contracts, classification and independent status dimensions are in the JSON ledger.','','| ID | Record | Kind | Primary home | Secondary associations | Status | Source anchor |','|---|---|---|---|---|---|---|']
for r in D['records']:
 secondary=', '.join(f"{l['target_id']} ({l['target_module']})" for l in r['secondary_links']) or 'None asserted'
 ledger.append(f"| {r['id']} | [{r['name']}](modules/{r['primary_module']}.md#{r['id']}) | {r['record_kind']} | [{r['primary_module']}](modules/{r['primary_module']}.md) | {secondary} | {r['maturity']['label']} | `{r['source_anchor']}` (bound R5.1 English snapshot) |")
(P/'PLACEMENT_LEDGER.md').write_text('\n'.join(ledger)+'\n')
for m in D['modules']:
 ds=[d for d in recipes if d['module']==m['id']]
 body=[f"# {m['id']} — {m['title']}",'','[Atlas index](../README.md) · [Placement ledger](../PLACEMENT_LEDGER.md)','',m['purpose'],'','**Placement status:** proposed editorial responsibility grouping, not an implemented package or service-owner map. Primary cards below retain different record kinds. Diagram arrows are declared intended relations unless explicitly marked source-connected.','']
 if m['id']=='M00':body+=['![System composition](../png/00-overview.png)','']
 if m['id']=='M10':body+=['![Historical provenance, outside capability diagrams](../png/13-provenance-register.png)','']
 for d in ds:body+=[f"![{d['title']}](../png/{d['id']}.png)",f"[Scalable SVG](../svg/{d['id']}.svg) · [Text alternative](../TEXT_ALTERNATIVES.md#{d['id']})",'']
 for f in m['ids']:
  r=R[f];body += [f'<a id="{f}"></a>',f"## {f} — {r['name']}",'',f"**Kind:** {r['record_kind']} — {r['record_subtype']}.",f"**Primary home:** {m['id']}. {r['placement_status']}.",'',r['purpose'],'',f"**Reported scope:** {r['maturity']['label']}. {r['maturity']['scope']}",f"**Source presence:** {r['implementation_status']['source_presence']}",f"**Whole-family / record integration:** {r['implementation_status']['whole_family_integration']}",f"**Specific join or documentary obligation:** {r['remaining_join']}",'',f"**Boundary:** {r['authority_boundary']}",f"**Deciding owner:** {r['controlling_owner']}",'']
  c=r.get('functional_contract')
  if c:body += [f"**Description type:** {c['kind']}",f"- Input / context: {c['input']}",f"- Output / record: {c['output']}",f"- Intended reader or consumer: {c['intended_consumer']}",f"- Interface limit: {c['interface_completeness']}",'']
  if r.get('sense_note'):body += [f"**Sense distinction:** {r['sense_note']}",'']
  body += [f"**Classification note:** {r['classification_note']}",'', '**Secondary editorial associations:** '+('; '.join(f"[{l['target_id']}]({l['target_module']}.md#{l['target_id']}) in {l['target_module']}" for l in r['secondary_links']) or 'None asserted.')+'.','',f"**Logical source anchor:** `{r['source_anchor']}` in the bound R5.1 English snapshot. This is intentionally not a relative hyperlink until its publication destination is settled. The preserved source description is embedded in the public JSON ledger; it is documentation, not an execution receipt.",'']
 (P/'modules'/(m['id']+'.md')).write_text('\n'.join(body))
(P/'PROVENANCE_REGISTER.md').write_text('''# Historical provenance register

[Atlas index](README.md) · [Scalable provenance view](svg/13-provenance-register.svg)

<a id="F02"></a>
## F02 — historical integration lineage

Historical repository/baseline lineage is retained so successor descriptions remain attributable. It is not an extra runtime organ, and no installed-integration milestone follows from this history record. [Full typed entry](modules/M10.md#F02).

<a id="F79"></a>
## F79 — TCHES historical testing document

The owner clarified that TCHES was used as a testing document. It is **not a Brain capability, optional Brain product, future heat-system implementation or implementation target**. The reference asserts no particular test procedure, consumer or passed result. It remains only in the historical register; there is no replacement function to preserve a misleading function count. [Full typed entry](modules/M10.md#F79).
''')
# Explicit per-arrow bindings: these are editorial mappings from public descriptions.
edges=[]
def fid(n):return n[1:].split('|',1)[0] if n.startswith('@') else n
for d in recipes:
 for j,lane in enumerate(d['lanes']):
  for k,(a,b,label,typ) in enumerate(lane['edges']):
   fa,fb=fid(lane['nodes'][a]),fid(lane['nodes'][b]);ids=[f for f in [fa,fb] if f in R]
   edges.append({'id':f"{d['id']}-L{j+1}-E{k+1}",'diagram':d['id'],'from':fa,'to':fb,'label':label,'type':typ,'status':'declared_intended_not_implementation_evidence','placement_or_sequence_status':'proposed editorial composition; exact adapter/current consumer may remain unresolved','source_refs':[{'id':f,'public_anchor':R[f]['source_anchor'],'fields':['functional_contract','authority_boundary','remaining_join']} for f in ids]})
(P/'source/module-flow-edges.json').write_text(json.dumps({'schema_id':'triadic-brain.module-flow-edges.v1','edges':edges},indent=2,ensure_ascii=False)+'\n')
# Text alternatives include the precise lane or edge content; SVG descriptions remain a short summary.
alts=['# Accessible text alternatives','','Read with the [placement ledger](PLACEMENT_LEDGER.md). All diagrams have SVG title/description or accessible-name/description metadata. Color is paired with named flow types.','']
for svg in sorted((P/'svg').glob('*.svg')):
 root=ET.fromstring(svg.read_text());ns={'s':'http://www.w3.org/2000/svg'};title=root.find('s:title',ns);desc=root.find('s:desc',ns);name=svg.stem
 alts += [f'<a id="{name}"></a>',f'## {title.text if title is not None else root.get("aria-label",name)}','',desc.text if desc is not None else 'See structured diagram source.','',f'[SVG](svg/{svg.name}) · [PNG](png/{name}.png)','']
 if name=='00-overview':
  alts += ['- Intended data return: Atlas / PMR → human task / human decision; “reviewed result / orientation / available recourse”. This returns an explanation to the human, not a new authority grant.', '- Representative intended control connector: UCC / AEGIS / moralWARE / controls → the cognitive loop; “scope at every deciding consumer”. The single drawn connection near Executive is representative: intake, dispatch, peer interaction, retention and release each require their own deciding consumer to enforce current scope.', '- Representative intended provenance connector: the cognitive loop → TEL / TAC / custody / provenance; “attempt / input / stage / outcome records”. The single drawn connection near Sophia represents records across all workflow stages, not only review outputs. Custody owns history; TEL organizes explicit stage links; TAC constrains permitted observation. Required custody is not optional memory.','']
 elif name in [d['id'] for d in recipes]:
  d=next(d for d in recipes if d['id']==name)
  for l in d['lanes']:
   alts += ['### '+l['title'],'']
   alts += ['- Primary: '+n+' — '+R[n]['name']+'; '+R[n]['record_kind']+'; '+R[n]['maturity']['label']+'.' if not n.startswith('@') else '- Reference: '+n[1:].replace('|',' — ')+'.' for n in l['nodes']]
   alts += ['- Intended '+typ+' flow: '+fid(l['nodes'][a])+' → '+fid(l['nodes'][b])+'; '+label+'.' for a,b,label,typ in l['edges']]+['']
 elif name in [d['id'] for d in focus]:
  d=next(d for d in focus if d['id']==name);alts += [d['caption'],'']
  alts += ['- '+n['id']+': '+n['label']+' ('+', '.join(n['family_ids'])+'). '+n['notes'] for n in d['nodes']]+['']
  alts += ['- Intended '+e['type']+' flow: '+e['from']+' → '+e['to']+'; '+e['label']+'.'+(' Condition: '+e['condition'] if e['condition'] else '') for e in d['edges']]+['']
 elif name=='10-source-connected-cognitive-route':
  se=json.loads((P/'source/source-connected-edges.json').read_text());alts += ['- '+e['from']+' → '+e['to']+': '+e['status']+'. '+e['data']+'. Boundary: '+e['boundary'] for e in se['edges']]+['']
 elif name=='12-knowledge-waters':
  alts += ['Conceptual path: corridors → braids → rivers → provisional terraces. New evidence or failed assumptions reopen inquiry through a linked revision. The old record is retained. Repair, explanation/teaching, calibration and stewardship remain visible support tributaries. Shared assumptions, excluded evidence or suppressed novelty can mimic stability.','', 'Source-defined research equations: F_ij = w_ij ((C_i + C_j) / 2) (Θ_j − Θ_i); A_i = |Σ_j F_ij| / (Σ_j |F_ij| + ε). C denotes declared corridor density, Θ declared potential, w graph weight and A alignment ratio. These are not literal water quantities, truth probabilities or authority. Domains, estimators, versions and parameters need separate evidence.','', 'Related existing records: F53/F86 mathematical definitions and parity; F07/F09 candidate construction and review; F10/F11 presentation; F63/F66 evidence and revision lineage; F55 transfer evaluation. No one-to-one renaming of Sonya/Sophia/Atlas is asserted.','']
(P/'TEXT_ALTERNATIVES.md').write_text('\n'.join(alts)+'\n')
(P/'BUILD.md').write_text('''# Local rendering and document checks

These files are documentation assets, not product runtime code. All inputs needed to reproduce the visuals are in `source/`.

## Existing local tools

- Python 3 standard library
- Inkscape (SVG → PNG)
- Graphviz `dot` (editable focused DOT graphs → SVG)

No package installation, paid resource or external rendering service is required. Do not submit a private source map to a hosted renderer.

From this directory:

```sh
python3 source/render_atlas.py
python3 source/render_special.py
python3 source/render_focus.py
python3 source/build_index.py
```

`render_atlas.py --svg-only` skips PNG rendering for its pages. The focus renderer uses 72-DPI SVG geometry, then exports a 1600-pixel-wide PNG; this avoids mismatched Graphviz scale/viewBox clipping. The DOT files are also directly editable.

## Before repository publication

1. Check the public source snapshot still matches the concept-map edition being released.
2. Confirm all 86 IDs remain unique in the data ledger, with one primary editorial home each.
3. Confirm F79 has no operational edge or capability placement; F02 remains historical lineage.
4. Inspect every final PNG at full size and fix clipping, overlaps or unreadable labels. Read SVG text alternatives as well.
5. Keep source-connected, bounded component evidence, installed behavior, missing joins and research separate.
6. Publish only the coordinator's explicit public allowlist. Never recursively upload a sibling private directory.

Source, diagram and accessibility inspection is not product runtime testing or CI.
''')
print('Built index, 11 home pages, placement ledger, long alternatives and',len(edges),'intended arrow records.')
