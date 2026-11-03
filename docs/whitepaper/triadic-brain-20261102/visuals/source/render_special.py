#!/usr/bin/env python3
"""Source-connected cognitive route and bounded research overlay, local rendering only."""
from render_atlas import SVG,COL,P

def card(s,x,y,title,ids,note,w=392,h=150,style='source'):
 fill='#edf7f5' if style=='source' else '#fff8ed'
 s.rect(x,y,w,h,fill=fill,stroke='#80a99d' if style=='source' else '#b99761',dash='7 5' if style!='source' else None)
 s.text(x+18,y+27,ids,14,True,COL['muted']);s.wrap(x+18,y+63,title,w-42,21,True);s.wrap(x+18,y+h-36,note,w-42,14,color=COL['muted'],leading=18)
def source_route():
 s=SVG(1600,1660,'Maintained cognitive route: actual source connections','Static source inspection identified the maintained WORK, separate DISPATCH, JOINED analysis, credentialed evaluator, custody acceptance, Atlas, TEL and Home inspection routes. Solid arrows mean a caller and accepting consumer are present in the inspected source, not live execution, installed qualification or human acceptance. Capture-only explicitly records optional analysis not executed. Ordinary governed processing passes no PMR consent.')
 s.header('Static source trace · not installed or live evidence','The cognitive route already connected in source','Solid arrows below identify inspected callers and accepting consumers. They do not claim deployed inference or complete end-to-end usefulness.')
 s.text(44,176,'Work submission, provider dispatch, evaluator acceptance and human review are distinct transitions—not one automatic run.',17,True,COL['muted'])
 lanes=[
 ('01 · WORK submits a bound task; it does not authorize dispatch',[
  ('Control Anchor Home: WORK','F03','explicit human task / turn'),('Sonya explicit task / turn','F04','canonical request; explicit parent'),('Custody admission + AEGIS / UCC','F35 · F23 · F22','technical eligibility; business advisory')],['request / context','authenticated admission']),
 ('02 · DISPATCH needs a separate exact-request authorization',[
  ('Exact-request dispatch authorization','F45 · F35','record / version / actor / limits'),('Configured provider / model adapter','F04 · F73','configured operating bounds'),('Raw response capture + normalized text','F35 · F04','wire bytes and text remain separate')],['frozen request','response / error bytes']),
 ('03 · JOINED analysis emits derived evaluator inputs; core stops before Sophia / Atlas',[
  ('Retained capture → Sonya quarantine','F04 · F35','derived text; preserved raw capture'),('CoherenceLattice analytical route','F07 · F16 · F17 · F29','candidate / UCM / AHA / aperture'),('Evaluator publication / claim','F35 · F09','allowlisted artifacts; nonce manifest')],['captured adapter','derived artifacts']),
 ('04 · Separate credentialed evaluator; custody validates the returned result',[
  ('Sophia fixed-file audit','F09','nonce-bound manifested inputs'),('Custody accepts exact result','F35','actor / input / algorithm bindings'),('Atlas posture + TEL stage links','F10 · F28','accepted results; sealed projection')],['bound audit result','accepted result']),
 ('05 · Inspect retained history; human review remains separately attributable',[
  ('Retained projection / capture','F35 · F28','saved source, analysis and states'),('Home INSPECT / CONTROLS','F03 · F67','reopen does not resend effects'),('Separate human REVIEW','F33 · F03','pending until attributable action')],['saved bounded view','separate review action'])]
 y=228
 for title,nodes,labels in lanes:
  s.text(44,y,title,18,True)
  for i,(title2,ids,note) in enumerate(nodes):card(s,44+i*530,y+25,title2,ids,note)
  for i,l in enumerate(labels):
   x=44+i*530;s.path([(x+398,y+126),(x+520,y+126)],'data');s.wrap(x+410,y+63,l,112,14,color=COL['data'],leading=18)
  y+=222
 s.rect(44,1365,1512,190,fill='#f6f7f9');s.text(66,1400,'WHAT THIS SOURCE TRACE DOES NOT ESTABLISH',18,True)
 for i,t in enumerate(['CAPTURE_ONLY explicitly marks optional Coherence / Sophia / Atlas / TEL analysis NOT_EXECUTED.',
  'The ordinary governed route passes no PMR consent: required custody is not optional cognitive memory.',
  'Synthetic captured responses and injected boundaries are not installed provider inference or human acceptance.',
  'The full source edge ledger retains separate same-root role synthesis, reconstruction and comparison boundaries.']):s.text(66,1434+i*30,'• '+t,17,color=COL['muted'])
 s.text(44,1612,'Source-connected ≠ execution-tested ≠ installed ≠ human accepted. Exact private source anchors are retained separately.',17,True)
 s.finish('10-source-connected-cognitive-route')

def comparison_boundary():
 s=SVG(1600,850,'Prior comparison: existing source and the separate missing native join','Explicitly supplied prior declarations feed an existing pure comparator. A proposed native same-custody authorized retention and use consumer is an unmerged unqualified draft. No lookup, durable memory, credential authentication or provider-context injection is created by the pure comparator. Same-root role synthesis is separate from cross-task memory.')
 s.header('Source status boundary','Prior comparison is not a memory transaction','A working pure leaf and a native custody/current-use connection must not be collapsed into one completed memory feature.')
 card(s,44,240,'Explicitly supplied prior declarations','F14 · F84 reference','supplied bytes, not automatic lookup')
 card(s,574,240,'Pure comparison result','F14 · source-connected','duplicate / related / conflict / unknown')
 card(s,1104,240,'Native same-custody consumer','F13 · F35 · F81','unmerged, unqualified draft',style='draft')
 s.path([(442,340),(564,340)],'data');s.wrap(454,277,'bounded comparison',112,14,color=COL['data'],leading=18)
 s.path([(972,340),(1094,340)],'control',dashed=True);s.wrap(984,265,'draft authorized join',112,14,color=COL['control'],leading=18)
 s.text(44,452,'SOLID: INSPECTED SOURCE CONNECTION',17,True,COL['data']);s.text(820,452,'DASHED: DRAFT JOIN, NOT INSTALLED',17,True,COL['control'])
 s.rect(44,493,1512,230,fill='#f5f7f9');s.text(66,530,'Keep these boundaries visible',21,True)
 for i,t in enumerate(['The comparator performs no lookup, persistence, grant authentication, context injection or dispatch.',
  'The current ordinary cognitive route passes no PMR consent; reference examples are no-write or in-memory.',
  'Current grants, original / producer / target bindings, audit and retained effects belong at the real native owner.',
  'Same-root Analyst → Challenge → Synthesis is already separate source work, not proof of cross-task memory.',
  'No second controller or replacement core is introduced by this visual.']):s.text(66,570+i*30,'• '+t,17,color=COL['muted'])
 s.text(44,793,'This comparison status is a scoped source review, not a benchmark, live-provider demonstration or installed qualification.',17,True)
 s.finish('11-comparison-boundary')

def waters():
 s=SVG(1600,1230,'Knowledge waters: a research model for revisable inquiry','Conceptual research relationship: corridors represent admissible lines of inquiry; braids compare related evidence and preserve disagreement; rivers represent sustained research trajectories and support contributions; terraces are provisional scoped reproducible understanding. New evidence or failed assumptions reopen inquiry with linked revisions. Apparent stability may conceal shared assumptions, suppressed novelty, excluded evidence or shifted burden. This is not a literal fluid law, required runtime pipeline or new Brain organ.')
 s.header('Research overlay · no new function or runtime organ','Knowledge waters: revisable inquiry','A source-grounded conceptual model. Uniform dashed arrows express research relationships, not measured flows or guaranteed progress.')
 xs=[44,444,844,1244];titles=['Corridors','Braids','Rivers','Terraces'];descs=['Explicit questions and alternative lines of inquiry','Compare support, conflict and shared assumptions','Sustained inquiry with visible plural contributions','Provisional, scoped and reproducible understanding']
 for i,(title,desc) in enumerate(zip(titles,descs)):
  s.rect(xs[i],249,312,190,fill='#edf7f7',stroke='#8bb5b8',dash='7 5');s.text(xs[i]+18,287,title,25,True);s.wrap(xs[i]+18,328,desc,274,19,leading=27)
  if i<3:s.path([(xs[i]+320,342),(xs[i]+390,342)],'data',dashed=True)
 s.path([(1400,445),(1400,516),(200,516),(200,445)],'data',dashed=True);s.text(384,503,'new evidence / failed assumption → reopen → linked revision',19,True,COL['data'])
 s.rect(44,585,712,181,fill='#f3f6f9');s.text(66,621,'Support tributaries stay visible',22,True);s.wrap(66,662,'Repair · explanation and teaching · calibration · stewardship. Preserve plural contributions, not only headline discoveries.',664,20)
 s.path([(756,662),(1060,662),(1060,449)],'provenance',dashed=True);s.wrap(775,612,'support with source / limits',192,16,color=COL['provenance'])
 s.rect(1100,585,456,181,fill='#fff6e9',stroke='#c4a067');s.text(1120,621,'False stability is possible',21,True,COL['control']);s.wrap(1120,658,'Shared assumptions, excluded evidence or suppressed novelty can mimic convergence.',412,18)
 s.rect(44,815,1512,230,fill='#f8f8fa');s.text(66,851,'One source-defined graph model · research specification, not measured telemetry',20,True)
 s.text(66,897,'F_ij = w_ij ((C_i + C_j) / 2) (Θ_j − Θ_i)',23);s.text(66,936,'A_i = |Σ_j F_ij| / (Σ_j |F_ij| + ε)',23)
 s.wrap(825,891,'C: declared corridor density; Θ: declared potential; w: graph weight; A: alignment ratio. Domains, estimators, versions and parameters need explicit evidence.',688,18)
 s.text(66,1018,'No water pressure, volume, hydraulic conservation, truth probability or permission is inferred from these symbols.',17,True,COL['muted'])
 s.text(44,1094,'Existing cross-references: F53 / F86 mathematics and parity · F07 / F09 construction and review · F10 / F11 presentation',17,True)
 s.text(44,1127,'F63 / F66 evidence channels and revision lineage · F55 proposed transfer evaluation. These are associations, not equivalences.',17,color=COL['muted'])
 s.text(44,1180,'Receptive / structuring / continuity operations may span components. Do not force them into one-to-one Sonya / Sophia / Atlas identities.',17,True)
 s.finish('12-knowledge-waters')
if __name__=='__main__':source_route();comparison_boundary();waters()

def provenance_register():
 s=SVG(1600,760,'Historical provenance is not a capability backlog','F02 preserves historical integration repository lineage. F79 preserves the owner-corrected TCHES historical testing document. Both remain in the stable registry and outside the capability diagrams. There is no replacement function and no requirement to implement a heat-exchange system.')
 s.header('M10 · history outside capability diagrams','Preserve the record without inventing a function','Stable IDs conserve provenance. A historical repository or testing document is not automatically a missing runtime module.')
 s.rect(44,240,712,280,fill='#f4f6f8',stroke='#94a5b1');s.text(66,280,'F02 · HISTORICAL INTEGRATION LINEAGE',18,True,COL['muted']);s.text(66,327,'Historical integration lineage',26,True);s.wrap(66,374,'Retain the earlier baseline, source tuple and successor relationships. Historical canonical wording does not override the current product.',662,20);s.text(66,491,'No separate current Brain organ is inferred.',19,True)
 s.rect(844,240,712,280,fill='#f4f6f8',stroke='#94a5b1');s.text(866,280,'F79 · HISTORICAL TEST DOCUMENT',18,True,COL['muted']);s.text(866,327,'TCHES testing-document provenance',25,True);s.wrap(866,374,'Retain the document and its corrected classification. It is not a Brain capability, a future heat-system implementation or validated physical behavior.',662,20);s.text(866,491,'No replacement function is invented to keep a count.',19,True)
 s.text(44,591,'The registry contains mixed kinds: capability, scope, profile, extension, contract, research, crosscutting duty and history.',19,True)
 s.text(44,636,'Every ID has one primary editorial home. This is conservation of meaning—not a completion score or a count of active modules.',18,color=COL['muted'])
 s.text(44,704,'No operational arrows connect these history records to the cognitive path. Source provenance remains available separately.',17,True)
 s.finish('13-provenance-register')
if __name__=='__main__':provenance_register()
