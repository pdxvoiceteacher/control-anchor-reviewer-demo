"""Read-only validation of this paper's explanatory artifacts.

Uses only the Python standard library. Makes no network requests, imports no
product code, and writes no files. JSON Schema validation is separate from these
cross-file invariants. Passing checks establishes artifact consistency, not the
truth of claims, product execution, or permission to publish.
"""
from pathlib import Path
from datetime import date
import hashlib
import json
import re
import sys


def validate(root):
    checks = []

    def require(condition, description):
        if not condition:
            raise ValueError(description)
        checks.append(description)

    def load(name):
        return json.loads((root / name).read_text(encoding="utf-8"))

    ledger = load("CLAIM_LEDGER.json")
    graph = load("TRANSFORMATION_GRAPH.json")
    catalog = load("QUANTITY_CATALOG.json")
    witness = load("BYTE_WITNESS.json")
    groups = load("SOURCE_GROUPS.json")
    manuscript = (root / "TRIADIC_BRAIN_MICRO_SPECTRUM.md").read_text(encoding="utf-8")
    claims = ledger["claims"]
    ids = [c["id"] for c in claims]
    by_id = {c["id"]: c for c in claims}
    source_ids = {s["id"] for s in groups["groups"]}
    require(len(ids) == len(set(ids)) == ledger["claim_count"], "claim count and unique identifiers")
    require(ledger["version"] == graph["version"] == catalog["version"] == "release-1.2-candidate", "candidate version consistency")
    date.fromisoformat(ledger["as_of"])
    date.fromisoformat(graph["as_of"])
    date.fromisoformat(catalog["as_of"])
    require(set(ledger["evidence_class_definitions"]) == set("SCTRD PHU".replace(" ", "")), "all declared evidence classes")
    headings = re.findall(r"^#{1,3} (.+)$", manuscript, flags=re.M)

    for c in claims:
        require(bool(c["scope"].strip()) and bool(c["statement"].strip()), c["id"] + " nonempty scope and statement")
        require(c["limitations"] and all(x.strip() for x in c["limitations"]), c["id"] + " nonempty limitations")
        require(c["source_groups"] and set(c["source_groups"]) <= source_ids, c["id"] + " source-group resolution")
        require(set(c["depends_on"]) <= set(ids) and c["id"] not in c["depends_on"], c["id"] + " dependency resolution")
        require(c["product_executed_by_this_study"] is False, c["id"] + " execution ceiling")
        require(any(h.startswith(c["manuscript_section"] + " ") for h in headings), c["id"] + " manuscript section")

    visiting, visited = set(), set()

    def visit(cid):
        if cid in visiting:
            raise ValueError("cyclic claim dependency: " + cid)
        if cid in visited:
            return
        visiting.add(cid)
        for dep in by_id[cid]["depends_on"]:
            visit(dep)
        visiting.remove(cid)
        visited.add(cid)

    for cid in ids:
        visit(cid)
    require(len(visited) == len(ids), "acyclic claim graph")

    stage_ids = {n["id"] for n in graph["stages"]}
    proposal_ids = {n["id"] for n in graph["research_extension_nodes"]}
    reference_ids = {n["id"] for n in graph["external_references"]}
    all_graph_ids = [n["id"] for key in ("stages", "research_extension_nodes", "external_references") for n in graph[key]]
    require(len(all_graph_ids) == len(set(all_graph_ids)), "globally unique graph node and reference IDs")
    for node in graph["stages"] + graph["research_extension_nodes"]:
        require(set(node["claim_ids"]) <= set(ids), node["id"] + " claim resolution")
    edge_fields = {"from", "to", "relation", "evidence_classes", "condition", "claim_ids"}
    for edge in graph["edges"] + graph["branch_edges"] + graph["research_extension_edges"]:
        require(edge_fields <= set(edge), "typed edge fields: " + edge["from"] + " to " + edge["to"])
        require(edge["from"] in stage_ids | proposal_ids and edge["to"] in stage_ids | proposal_ids, "edge endpoints resolve to nodes, not references")
        require(bool(edge["condition"].strip()) and edge["evidence_classes"], "edge condition and evidence present")
        require(set(edge["claim_ids"]) <= set(ids), "edge claim resolution")
        if edge["to"] == "D18" or (edge["from"], edge["to"]) == ("D18", "D19"):
            require(edge["relation"] == "CONCEPTUAL_UNESTABLISHED_INTEGRATION" and "C" not in edge["evidence_classes"], "peer-model integration remains unestablished")
        if (edge["from"], edge["to"]) == ("D09", "D10"):
            require("CAPTURED" in edge["condition"] and "JOINED" in edge["condition"] and "CAPTURE_ONLY bypasses" in edge["condition"], "native analysis remains conditional")
    n0 = next(n for n in graph["stages"] if n["id"] == "D00")
    require(any("messages<=16" in v and "8 complete pairs" in v and "effective-message" in v for v in n0["guards"]), "prior-history bounds remain messages not pairs")

    required_quantity = {"formula_version", "estimator_kind", "evidence_classes", "input_domain", "missingness", "clipping_and_rounding"}
    qids = [q["id"] for q in catalog["quantities"]]
    require(len(qids) == len(set(qids)), "unique quantity identifiers")
    require(catalog["coverage"] == "SELECTED_NOT_EXHAUSTIVE", "selected quantity coverage")
    for q in catalog["quantities"]:
        require(required_quantity <= set(q), q["id"] + " estimator contract fields")
        require(set(q["claim_ids"]) <= set(ids), q["id"] + " claim resolution")
        require(q["missingness"]["kind"] and q["missingness"]["behavior"], q["id"] + " typed missingness")
        require(q["formula"] is not None or q["estimator_kind"] == "UNAVAILABLE", q["id"] + " unavailable formula explicit")
    q5 = next(q for q in catalog["quantities"] if q["id"] == "Q05")
    q17 = next(q for q in catalog["quantities"] if q["id"] == "Q17")
    require(q5["formula"].startswith("round12(mean(x_j^2))"), "waveform final rounding")
    require("R_(n+1)" in q17["formula"], "sequential terrace river input")

    for key, item in witness["bytes"].items():
        raw = bytes.fromhex(item["hex"])
        require(len(raw) == item["length"], key + " byte length")
        require(raw.decode("utf-8") == item["utf8"], key + " UTF-8 text")
        require(hashlib.sha256(raw).hexdigest() == item["sha256"], key + " SHA-256")
    require(witness["conditions"]["observed_run"] is False, "witness not executed")
    source = witness["bytes"]["native_grounding_source"]["utf8"]
    span = witness["span"]
    lo, hi = span["normalized_source_char_interval"]
    excerpt = source[lo:hi]
    require(excerpt == span["text"], "witness code-point interval")
    blo, bhi = span["normalized_source_utf8_byte_interval"]
    require(source.encode("utf-8")[blo:bhi] == excerpt.encode("utf-8"), "witness UTF-8 interval")
    require(hashlib.sha256(excerpt.encode("utf-8")).hexdigest() == span["claim_and_excerpt_sha256"], "witness excerpt digest")

    require(not re.search(r"\[[^\]]*I\d{2}[^\]]*\]\(https?://", manuscript), "internal citation labels not linked to public references")
    body, references = manuscript.split("## References", 1)
    references = references.split("## Source evidence index", 1)[0]
    bibliography_urls = set(re.findall(r"\]\((https?://[^)]+)\)", references))
    body_urls = set(re.findall(r"\]\((https?://[^)]+)\)", body))
    require(bibliography_urls <= body_urls and len(bibliography_urls) == 18, "18 bibliography URLs cited in body")

    manifest = load("MANIFEST.json")
    names = [r["file"] for r in manifest["files"]]
    require(len(names) == len(set(names)) and "MANIFEST.json" not in names, "manifest is non-self-referential")
    actual_names = {p.name for p in root.iterdir() if p.is_file()} - {"MANIFEST.json"}
    require(set(names) == actual_names, "manifest file coverage")
    for record in manifest["files"]:
        require(Path(record["file"]).name == record["file"], "manifest basename-only paths")
        raw = (root / record["file"]).read_bytes()
        require(len(raw) == record["bytes"] and hashlib.sha256(raw).hexdigest() == record["sha256"], record["file"] + " manifest identity")
    return {"status": "PASS", "candidate": "release-1.2-candidate", "checks": len(checks), "claim_count": len(ids), "quantity_count": len(qids), "stage_count": len(stage_ids), "exact_byte_domains": len(witness["bytes"]), "product_execution": False, "scientific_truth_validated": False, "publication_authorized": False}


if __name__ == "__main__":
    directory = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parent
    if len(sys.argv) > 2:
        raise SystemExit("Usage: python validate_companion.py [candidate_directory]")
    print(json.dumps(validate(directory), indent=2))
