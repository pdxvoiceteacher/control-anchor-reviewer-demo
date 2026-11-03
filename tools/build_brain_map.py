"""Generate public brain-map views from reviewed JSON; Python standard library only."""
from pathlib import Path
import html
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'docs/brain-map'
LABELS = {'coded': 'CODED · public main', 'development': 'DEVELOPMENT · reported', 'proposed': 'PROPOSED · design / research'}
COLORS = {'coded': '#65f5c8', 'development': '#ffd479', 'proposed': '#b6a0ff'}
BASE = 'https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/'

def render(data):
    families = data['families']
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 760" role="img" aria-labelledby="map-title map-desc">',
      '<title id="map-title">Triadic Brain function map</title>',
      '<desc id="map-desc">Nine functional families. Evidence, controls and scripted review have bounded code on public main. Grounding, evaluation and workbench are reported development. Continuity, community compute and learning describe broader proposals. See the linked text map for evidence and limitations.</desc>',
      '<defs><pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#16334b" stroke-width=".6"/></pattern><linearGradient id="brain" x2="1" y2="1"><stop stop-color="#112b42"/><stop offset="1" stop-color="#161c39"/></linearGradient></defs>',
      '<rect width="1080" height="760" rx="24" fill="#07111f"/><rect width="1080" height="760" rx="24" fill="url(#grid)"/>',
      '<g font-family="Arial, sans-serif"><text x="52" y="55" fill="#7ce8ef" font-size="15" letter-spacing="4">CONTROL ANCHOR / FUNCTION ATLAS</text><text x="52" y="102" fill="#f1f8ff" font-size="38" font-weight="700">The Triadic Brain</text><text x="52" y="132" fill="#c1d2e4" font-size="17">Explore the functions. Inspect the evidence. Keep the limits visible.</text>',
      '<path d="M535 165 C485 135 410 148 388 190 C310 175 244 215 240 274 C176 296 165 374 203 418 C172 480 216 553 284 555 C312 622 406 645 459 607 L500 646 L535 675 L573 642 L612 607 C690 645 773 604 790 553 C870 537 895 474 863 419 C910 361 878 291 825 274 C817 202 749 177 683 190 C650 145 582 139 535 165Z" fill="url(#brain)" stroke="#3a8ca3" stroke-width="3"/>',
      '<path d="M535 166V340 M535 465V675 M388 190L340 245L265 380L350 515L459 607 M683 190L735 250L805 385L725 520L612 607 M340 245L530 185L735 250 M265 380L535 415L805 385 M350 515L535 415L725 520 M350 515L535 610L725 520" fill="none" stroke="#38718d" stroke-width="2"/>']
    for n,f in enumerate(families,1):
        x,y=f['x'],f['y']; c=COLORS[f['status']]
        svg.append(f'<g><circle cx="{x}" cy="{y}" r="21" fill="#091525" stroke="{c}" stroke-width="3"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="17" font-weight="700" fill="{c}">{n:02}</text><rect x="{x-116}" y="{y+29}" width="232" height="46" rx="8" fill="#091525" stroke="#345169"/><text x="{x}" y="{y+48}" text-anchor="middle" font-size="16" fill="#f1f8ff">{html.escape(f["name"])}</text><text x="{x}" y="{y+66}" text-anchor="middle" font-size="11" fill="{c}">{html.escape(LABELS[f["status"]])}</text></g>')
    svg.append('<text x="52" y="711" fill="#c1d2e4" font-size="15">Status is scoped per family, not a completion percentage. Unknown proof stays unknown.</text><text x="52" y="738" fill="#93abc3" font-size="13">PUBLIC SOURCE SNAPSHOT / '+data['reviewed_at']+' · Click through to the family directory.</text></g></svg>')
    svg='\n'.join(svg)+'\n'
    intro=f'''# Explore the Triadic Brain

[Back to the front page](../../README.md) · [Detailed product crosswalk](../PRODUCT_MAP.md)

![Techno brain with nine numbered function families; equivalent descriptions and links follow.](brain-map.svg)

**Reviewed {data['reviewed_at']}.** {data['scope']}
Public source baseline: `{data['source_commit']}`. Development descriptions retain their own dated evidence; this date does not requalify them.

- **CODED · public main:** bounded implementation in this offline synthetic repository, not the whole Brain.
- **DEVELOPMENT · reported:** broader components or integration work; any bounded public subcomponent is identified separately below.
- **PROPOSED · design / research:** broader intended behavior, even where smaller foundations exist.
- **UNKNOWN:** missing or uninspected proof stays unknown. No status implies production readiness.

## Choose a family

'''
    md=intro+'\n'.join(f'{n}. [{f["name"]}](#{f["id"]}) — {LABELS[f["status"]]}' for n,f in enumerate(families,1))+'\n\n'
    sections=[]
    for n,f in enumerate(families,1):
        md+=f'<a id="{f["id"]}"></a>\n\n## {n:02}. {f["name"]}\n\n**{LABELS[f["status"]]}**\n\n{f["summary"]}\n\n**Boundary:** {f["boundary"]}\n\n'
        md+='\n'.join(f'- [{label}](../../{path})' for label,path in f['links'])+'\n\n[Back to family directory](#choose-a-family)\n\n'
        links=''.join(f'<li><a href="{BASE}{data["source_commit"]}/{html.escape(path,quote=True)}">{html.escape(label)}</a></li>' for label,path in f['links'])
        sections.append(f'<section id="{f["id"]}" tabindex="-1"><h2>{n:02}. {html.escape(f["name"])}</h2><p class="status {f["status"]}">{html.escape(LABELS[f["status"]])}</p><p>{html.escape(f["summary"])}</p><p><strong>Boundary:</strong> {html.escape(f["boundary"])}</p><ul>{links}</ul><a href="#families">Back to families</a></section>')
    md+='''## Optional browser explorer

GitHub renders this directory as Markdown. The front-page graphic opens this directory; the numbered family links are the clickable controls. The graphic itself is a static image, not an interactive SVG embedded in GitHub.

For the interactive graphic, download [explorer.html](explorer.html) and open it in a browser. It is self-contained, has no scripts or external assets, and uses ordinary keyboard-accessible links. Source links open this public repository at the reviewed baseline. No GitHub Pages site is enabled or required.

## Maintain this map

Edit [map.json](map.json), then run `python tools/build_brain_map.py` from the repository root. Run `python tools/build_brain_map.py --check` and `python -m unittest discover -s tests -p test_brain_map.py`. Update the source manifest using the repository's normal publication process. Preserve prior publication metadata and historical evidence.

A status change needs evidence for that specific scope. Do not promote private development to public-main code, treat a document as implementation, or imply that a new review date proves a fresh runtime result. No private source links, operational records, hosted analytics, external scripts or paid services belong in this map.
'''
    # Inline SVG: each visible family group becomes an ordinary, focusable link.
    interactive=svg.replace('role="img" aria-labelledby="map-title map-desc"','role="group" aria-labelledby="map-title map-desc"')
    for n,f in enumerate(families,1):
        start=f'<g><circle cx="{f["x"]}" cy="{f["y"]}"'
        interactive=interactive.replace(start,f'<a href="#{f["id"]}" aria-label="{html.escape(f["name"],quote=True)}: {html.escape(LABELS[f["status"]],quote=True)}"><g><circle cx="{f["x"]}" cy="{f["y"]}"')
        # Find closing group after this family's label, not the parent group.
        tail=f'{html.escape(LABELS[f["status"]])}</text></g>'
        pos=interactive.index(f'<a href="#{f["id"]}"'); end=interactive.index(tail,pos)+len(tail)
        interactive=interactive[:end]+'</a>'+interactive[end:]
    nav=''.join(f'<a href="#{f["id"]}">{n:02}. {html.escape(f["name"])}</a>' for n,f in enumerate(families,1))
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark"><title>Triadic Brain · Function explorer</title><style>
*{box-sizing:border-box}code{overflow-wrap:anywhere}body{margin:0;background:#07111f;color:#e9f2fb;font:18px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:24px}a{color:#87e4ff;text-underline-offset:4px}a:focus-visible{outline:3px solid #fff;outline-offset:5px}svg{display:block;width:100%;height:auto}svg a:focus-visible circle,svg a:hover circle{stroke:#fff;stroke-width:6}nav{display:flex;flex-wrap:wrap;gap:12px}nav a{padding:12px;background:#14263a;border:1px solid #45627e;border-radius:8px}section{margin:32px 0;padding:24px;border:1px solid #45627e;border-radius:16px;scroll-margin-top:16px}section:target{border:3px solid #87e4ff}h1{line-height:1.2}h2{font-size:1.4rem}.status{font-weight:700}.coded{color:#65f5c8}.development{color:#ffd479}.proposed{color:#b6a0ff}.skip{display:block}li{margin:10px 0}@media(max-width:600px){main{padding:16px}section{padding:16px}nav{display:grid}svg{min-width:0}h1{font-size:1.8rem}}
</style></head><body><main><a class="skip" href="#families">Skip graphic and choose a family</a><h1>The Triadic Brain function explorer</h1><p>Select a numbered region or use the family links. These are scoped evidence labels, not a whole-product completion score.</p>'''+interactive+f'<p>Reviewed {data["reviewed_at"]}. Public baseline <code>{data["source_commit"]}</code>. Development reports retain their original dates; unknown installed and live proof is not upgraded by this map.</p><p><strong>CODED</strong>: bounded public-demo implementation. <strong>DEVELOPMENT</strong>: broader development; bounded public subcomponents are identified below. <strong>PROPOSED</strong>: broader design or research, not delivery.</p><nav id="families" aria-label="Function families">'+nav+'</nav>'+''.join(sections)+'</main></body></html>\n'
    return {'brain-map.svg':svg,'README.md':md,'explorer.html':page}

def main():
    data=json.loads((DIR/'map.json').read_text())
    outputs=render(data)
    if '--check' in sys.argv:
        stale=[name for name,text in outputs.items() if not (DIR/name).exists() or (DIR/name).read_text()!=text]
        if stale: raise SystemExit('Stale generated views: '+', '.join(stale))
        print('PASS: all three brain-map views match map.json')
    else:
        for name,text in outputs.items(): (DIR/name).write_text(text,encoding='utf-8')
if __name__=='__main__': main()
