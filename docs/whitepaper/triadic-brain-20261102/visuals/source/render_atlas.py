#!/usr/bin/env python3
"""Render documentation-only SVG/PNG architecture assets locally. No network or installs.
Usage: python3 source/render_atlas.py [--svg-only]
Requires Python standard library; PNG output uses existing Inkscape.
"""
from pathlib import Path
import json, html, textwrap, subprocess, sys, re
P=Path(__file__).resolve().parent.parent
D=json.loads((P/'source/architecture-data.json').read_text()); R={r['id']:r for r in D['records']}; M={m['id']:m for m in D['modules']}
COL={'text':'#172b3a','muted':'#465b6c','data':'#087f8c','control':'#9a5b06','provenance':'#7451a8','association':'#71808b','panel':'#f5f8fa','border':'#becbd3','bg':'#ffffff'}
STATUS={'bounded_evidence':'B','source_components':'C','design':'D','research_or_unresolved':'R','historical_record':'H','not_applicable_historical_material':'H','process_discipline':'P'}
TYPE={'functional_responsibility':'RESPONSIBILITY','system_composition':'COMPOSITION','historical_integration_lineage':'HISTORY','optional_reference_asset':'OPTIONAL ASSET','handoff_artifact_contract':'HANDOFF CONTRACT','representation_contract':'CONTRACT','staged_normative_architecture':'STAGED DESIGN','historical_guard_responsibility':'HISTORICAL GUARD','staged_workflow_design':'STAGED DESIGN','separated_review_roles':'REVIEW ROLES','optional_policy_profile':'OPTIONAL PROFILE','crosscutting_interpretive_lens':'CONTEXT LENS','optional_domain_extension':'OPTIONAL EXTENSION','codec_and_research_lineages':'CODEC / RESEARCH','research_objective_and_diagnostics':'OBJECTIVE / PROXY','memory_role_taxonomy_and_design':'ROLE TAXONOMY','typed_outcome_vocabulary':'OUTCOME VOCABULARY','optional_research_branch':'OPTIONAL RESEARCH','optional_representation_branch':'OPTIONAL VIEW','typed_quantity_namespace':'QUANTITY CONTRACT','assumption_evidence_crosswalk':'EVIDENCE CROSSWALK','research_responsibility':'RESEARCH','publication_evidence_doctrine':'PUBLICATION DOCTRINE','control_authoring_responsibility':'AUTHORING','evidence_channel_contract':'CHANNEL CONTRACT','role_capability_contract':'ROLE CONTRACT','continuity_relation_contract':'CONTINUITY CONTRACT','typed_lineage_contract':'LINEAGE CONTRACT','proposed_optional_composition':'PROPOSED COMPOSITION','crosscutting_deployment_principle':'PRINCIPLE','quality_process_risk_vocabulary':'PROCESS VOCABULARY','historical_test_document_asset':'HISTORICAL DOCUMENT','formal_assumption_consumer_crosswalk':'FORMAL CROSSWALK'}
def esc(t): return html.escape(str(t))
class SVG:
 def __init__(self,w,h,title,desc):
  self.w,self.h=w,h;self.title=title;self.desc=desc
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',f'<rect width="{w}" height="{h}" fill="white"/>','<defs>']
  for k in ('data','control','provenance','association'):
   self.s.append(f'<marker id="arrow-{k}" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="{COL[k]}"/></marker>')
  self.s.append('</defs><g font-family="DejaVu Sans, sans-serif">')
 def rect(self,x,y,w,h,fill=None,stroke=None,rx=10,dash=None):
  self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or COL["panel"]}" stroke="{stroke or COL["border"]}" stroke-width="1.5"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def text(self,x,y,t,size=18,bold=False,color=None,anchor='start'):
  self.s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or COL["text"]}" text-anchor="{anchor}"'+(' font-weight="700"' if bold else '')+f'>{esc(t)}</text>')
 def wrap(self,x,y,t,width,size=18,bold=False,color=None,leading=None):
  # Font-metric conservative wrapping, including long identifiers.
  lines=textwrap.wrap(t,width=max(8,int(width/(size*.60))),break_long_words=True,break_on_hyphens=False) or ['']
  for i,line in enumerate(lines):self.text(x,y+i*(leading or size*1.35),line,size,bold,color)
  return len(lines)*(leading or size*1.35)
 def path(self,pts,kind='data',dashed=False,arrow=True):
  q=' '.join(('M' if i==0 else 'L')+f'{x},{y}' for i,(x,y) in enumerate(pts))
  self.s.append(f'<path d="{q}" fill="none" stroke="{COL[kind]}" stroke-width="2.7" stroke-linejoin="round"'+(' stroke-dasharray="8 6"' if dashed else '')+(f' marker-end="url(#arrow-{kind})"' if arrow else '')+'/>')
 def link_start(self,url):self.s.append(f'<a xlink:href="{esc(url)}">')
 def link_end(self):self.s.append('</a>')
 def finish(self,name):
  self.s.append('</g></svg>');fp=P/'svg'/f'{name}.svg';fp.write_text('\n'.join(self.s)+'\n')
  if '--svg-only' not in sys.argv:
   subprocess.run(['inkscape',str(fp),'--export-type=png',f'--export-filename={P/"png"/(name+".png")}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 def header(self,kicker,title,sub):
  self.text(44,40,kicker.upper(),15,True,COL['data']);self.text(44,86,title,32,True);self.wrap(44,122,sub,self.w-88,18,color=COL['muted'])
 def footer(self,y):
  self.text(44,y,'B bounded components · C source components · D design · R research / unresolved · P human process',15,False,COL['muted'])
  self.text(44,y+25,'Record kind ≠ maturity. No whole-family integration or permission is implied. Open the index for source scope and missing joins.',15,False,COL['muted'])

def overview():
 s=SVG(1600,1330,'Triadic Brain: responsibility and connection map','A layered intended architecture. Human task enters Control Anchor and Sonya, then finite executive planning, CoherenceLattice analysis, Sophia review and Atlas orientation. User controls and custody/provenance crosscut this loop. Independent peer/provider integration and optional research are separate supporting branches. All module groupings are editorial; arrows are intended data/control/provenance relationships, not installed integration proof. F02 lineage and F79 TCHES historical testing document are outside capability diagrams. Every registry ID is indexed once by primary home.')
 s.header('Visual architecture · draft for review','How the responsibilities fit together','Start with the local cognitive loop; use the module pages for every typed function, contract, profile and research responsibility.')
 s.rect(44,237,1512,964,fill='#ffffff',stroke='#7d929f',rx=14,dash='7 6');s.text(580,265,'F01 · TRIADIC BRAIN = THE WHOLE COMPOSITION',16,True,COL['muted'])
 s.rect(68,164,360,60,fill='#eaf5f5',stroke=COL['data']);s.text(90,201,'Human task / human decision',19,True)
 s.path([(218,224),(218,311)],'data',dashed=True);s.text(235,296,'scope + context',15,color=COL['data'])
 boxes=[('M01','Control Anchor / Sonya','Intake, local owner, visible control'),('M02','Executive / planning','Finite goals, roles and stopping'),('M03','CoherenceLattice / GUFT / AHA','Grounded candidate, alternatives, limits'),('M04','Sophia / review','Fixed-candidate findings and dissent'),('M05','Atlas / PMR','Orientation; separate memory decisions')]
 for i,(m,t,desc) in enumerate(boxes):
  x=68+i*304;s.link_start('../modules/'+m+'.md');s.rect(x,324,272,195,fill='#eff7f7',stroke='#76a4a8');s.text(x+18,351,m,16,True,COL['data']);s.wrap(x+18,383,t,236,22,True);s.wrap(x+18,458,desc,236,17,color=COL['muted']);s.link_end()
  if i<4:s.path([(x+272,414),(x+299,414)],'data',dashed=True)
 s.text(68,550,'TASK',14,True,COL['data']);s.text(372,550,'FINITE PROPOSAL',14,True,COL['data']);s.text(676,550,'FIXED CANDIDATE',14,True,COL['data']);s.text(980,550,'ATTRIBUTED REVIEW',14,True,COL['data']);s.text(1284,550,'READABLE RESULT',14,True,COL['data'])
 s.path([(1420,324),(1420,194),(440,194)],'data',dashed=True);s.text(685,181,'reviewed result / orientation / available recourse',17,True,COL['data'])
 # Crosscutting layers have direct, typed constraint / provenance connectors.
 s.path([(420,666),(420,574),(622,574),(622,525)],'control',dashed=True);s.text(445,622,'scope at every deciding consumer',16,color=COL['control'])
 s.path([(1230,525),(1230,645)],'provenance',dashed=True);s.text(850,602,'attempt / input / stage / outcome records',16,color=COL['provenance'])
 s.link_start('../modules/M07.md');s.rect(68,666,708,206,fill='#fff8ee',stroke='#c69b5c');s.text(90,699,'M07 · UCC / AEGIS / moralWARE / CONTROLS',18,True,COL['control']);s.wrap(90,736,'Each deciding consumer enforces its current scope: intake, dispatch, peers, retention and release.',664,20,True);s.wrap(90,816,'Advisory business findings do not veto ordinary prompts. Rights review, technical protection and recourse stay distinct.',664,17,color=COL['muted']);s.link_end()
 s.link_start('../modules/M06.md');s.rect(820,666,708,206,fill='#f5f1fb',stroke='#a88bc7');s.text(842,699,'M06 · TEL / TAC / CUSTODY / PROVENANCE',18,True,COL['provenance']);s.wrap(842,736,'Records span the workflow, not just review. Custody owns history; TEL organizes explicit stage links.',664,20,True);s.wrap(842,816,'TAC constrains permitted observation. Lineage and replay preserve unknowns. Required custody is not optional memory.',664,17,color=COL['muted']);s.link_end()
 s.text(68,919,'SEPARATE SUPPORTING ROUTES · NOT MANDATORY PREREQUISITES FOR EVERY LOCAL TASK',16,True,COL['muted'])
 s.link_start('../modules/M08.md');s.rect(68,942,708,198,fill='#f4f7fa');s.text(90,975,'M08 · OWNER-GOVERNED PEERS / RESOURCES / PROVIDERS',17,True);s.wrap(90,1014,'Connects to M01 intake, M02 roles and M04 review through explicit owner admission.',664,20,True);s.wrap(90,1090,'Remote grants do not grant local current use. Real two/three-node cognition is not established by these diagrams.',664,17,color=COL['muted']);s.link_end()
 s.link_start('../modules/M09.md');s.rect(820,942,708,198,fill='#f4f7fa',dash='7 5');s.text(842,975,'M09 · RESEARCH / QUALITY / OPTIONAL EXTENSIONS',17,True);s.wrap(842,1014,'Connects to planning, typed representation and review through bounded comparisons and source-specific contracts.',620,20,True);s.wrap(842,1090,'No invented benchmark, completion percentage, mandatory research organ or automatic permission upgrade.',664,17,color=COL['muted']);s.link_end()
 s.text(68,1177,'Historical register only: F02 integration lineage · F79 TCHES testing document. Neither is a missing runtime organ.',17,True,COL['muted'])
 s.text(44,1231,'Arrows above are declared intended flows. Static-source caller evidence is shown separately in the source-path view.',17,True)
 s.text(44,1273,'Primary homes are navigational groupings, not a claim of current service ownership. Open a module for its typed records and evidence limits.',16,color=COL['muted']);s.text(44,1298,'Reference, profile, contract, principle, research, historical record and capability are not interchangeable kinds.',16,color=COL['muted']);s.finish('00-overview')

if __name__=='__main__':overview()

# Responsibility maps deliberately distinguish contracts/assets/principles from services.
def family_card(s,node,x,y,w=392,h=146):
 if node.startswith('@'):
  ident,label=node[1:].split('|',1);ref=R.get(ident);kind='REFERENCE · '+(ref['primary_module'] if ref else 'ROLE / BOUNDARY')
  s.rect(x,y,w,h,fill='#ffffff',stroke='#8c9eaa',dash='6 5');s.text(x+18,y+26,kind,14,True,COL['muted']);s.wrap(x+18,y+62,label,w-40,22,True);s.text(x+18,y+h-16,ident if ident.startswith('F') else 'Not a new registry function',14,color=COL['muted']);return
 r=R[node];sub=r.get('visual_type_key',r.get('record_subtype',r['record_kind']));k='DEPLOYMENT SCOPE' if r['record_kind']=='deployment_entity' else TYPE.get(sub,r['record_kind'].replace('_',' ').upper());status=STATUS[r['maturity']['label']]
 fill='#eef7f7' if r['record_kind']=='capability' else '#f3f5f8';dash=None
 if r['record_kind'] in ('research_proposal','optional_profile_or_extension'):fill='#fff8ed';dash='7 5'
 if r['record_kind']=='deployment_entity':fill='#eaf2f8'
 s.link_start('../modules/'+r['primary_module']+'.md#'+node)
 s.rect(x,y,w,h,fill=fill,dash=dash);s.text(x+18,y+26,f'{node} · {k} · {status}',13,True,COL['muted']);s.wrap(x+18,y+63,r['visual_label'],w-40,22,True);s.text(x+18,y+h-16,'Primary home '+r['primary_module']+' · source scope in index',14,color=COL['muted']);s.link_end()

def module_diagram(d):
 h=530+len(d['lanes'])*218
 desc=d['subtitle']+' '+ ' '.join(d['boundaries'])+' '+' '.join(f"Lane {l['title']}: "+'; '.join(n[1:].split('|',1)[1] if n.startswith('@') else n+' '+R[n]['name'] for n in l['nodes']) for l in d['lanes'])
 s=SVG(1600,h,d['title'],desc);s.header(d['module']+' · proposed responsibility grouping',d['title'],d['subtitle'])
 s.text(44,180,'Arrows: intended data (teal) · control / constraints (amber) · provenance (purple). REF boxes are secondary references.',16,False,COL['muted'])
 y=220
 for lane in d['lanes']:
  s.text(44,y,lane['title'],18,True)
  by=y+24
  for i,node in enumerate(lane['nodes']):family_card(s,node,44+530*i,by)
  for a,b,label,kind in lane['edges']:
   xa=44+530*a;xb=44+530*b
   if a<b:pts=[(xa+398,by+100),(xb-10,by+100)];lx=xa+410
   else:pts=[(xa-8,by+100),(xb+400,by+100)];lx=xb+410
   s.path(pts,kind,dashed=True);s.wrap(lx,by+34,label,112,14,color=COL[kind],leading=18)
  y+=218
 s.text(44,y+4,'SECONDARY MODULE CONNECTIONS',16,True,COL['data'])
 for i,(a,b,label) in enumerate(d['crosslinks']):
  yy=y+37+i*32;s.text(44,yy,f'{a} → {b}',17,True,COL['data']);s.text(180,yy,label,17,color=COL['muted'])
 yy=y+153
 for note in d['boundaries']:
  used=s.wrap(44,yy,'• '+note,1512,17,color=COL['muted'],leading=23);yy+=max(26,used+5)
 s.footer(h-50);s.finish(d['id'])

def modules():
 for d in json.loads((P/'source/diagram-recipes.json').read_text())['diagrams']:module_diagram(d)

if __name__=='__main__':modules()
