"""Compare synthetic retained hypotheses through the real extracted consumers."""
from __future__ import annotations

from dataclasses import replace
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
for relative in ("src", "components/CoherenceLattice/python/src", "components/Sophia/python/src"):
    sys.path.insert(0, str(ROOT / relative))


def require_dependencies():
    try:
        installed = version("jsonschema")
    except PackageNotFoundError as exc:
        raise RuntimeError("Use an existing environment with jsonschema==4.26.0, or follow docs/RETROSYNTHESIS_COMPONENT.md.") from exc
    if installed != "4.26.0":
        raise RuntimeError(f"Expected jsonschema==4.26.0; found {installed}. This version is not qualified here.")


def demonstration():
    require_dependencies()
    from coherence.totality.grounding import build_grounding_bundle
    from coherence.totality.retrosynthesis import evaluate_proposal
    from sophia.triadic.governed_evaluation import _check_reconstruction
    from triadicbrain.assurance.canonical import canonical_bytes, sha256_bytes, strict_loads
    from triadicbrain.assurance import retrosynthesis_reuse as reuse

    now = "2026-11-02T00:02:00Z"
    target = reuse.TargetBinding("SYNTHETIC-ORG", "DEMO", "READER", "TASK-B", "b" * 64, "c" * 64, "LAB")

    def insight(record="TASK-A", source=b"Sampling failed.\n\nCalibration is unknown.\n"):
        grounding = build_grounding_bundle(source)
        origin = reuse.OriginBinding("SYNTHETIC-ORG", "DEMO", record, "a" * 64, "d" * 64, "e" * 64, "f" * 64, "1" * 40)
        parent = {key: getattr(origin, key) for key in ("record_id", "request_sha256", "response_sha256", "decision_sha256")}
        proposal = {"schema_id": "uvlm.coherence.retrosynthesis-proposal.v1", "trigger": "FAILURE",
                    "parent": parent, "attribution": {"actor_id": "SCRIPTED-PUBLIC-DEMO", "origin": "SCRIPTED"},
                    "alternatives": []}
        for index, segment in enumerate(grounding["segments"]):
            proposal["alternatives"].append({"id": f"H{index}", "explanation": ("Sampling error", "Calibration error")[index],
                "references": [{"segment_id": segment["segment_id"], "segment_sha256": segment["sha256"], "relation": "PROPOSED_SUPPORT"}],
                "observable_test": "Compare an independent retained measurement.",
                "falsification": "An independent retained measurement contradicts the hypothesis."})
        projection = {key: grounding[key] for key in ("manifest", "normalized_source", "segments")}
        return reuse.InsightInput(canonical_bytes(proposal), source, canonical_bytes(projection), "LAB", origin)

    def change(value, *, conflict=False):
        proposal = strict_loads(value.proposal)
        if conflict:
            proposal["alternatives"][0]["references"][0]["relation"] = "PROPOSED_COUNTEREVIDENCE"
        else:
            proposal["alternatives"][0]["explanation"] = "Another sampling hypothesis"
        return replace(value, proposal=canonical_bytes(proposal))

    def select(value):
        permit = reuse.ReusePermit(sha256_bytes(canonical_bytes(reuse.reference_metadata(value))), target,
            "COMPARE", "2" * 64, "3" * 64, "2026-11-02T00:01:00Z", "2026-11-02T00:03:00Z", now, "CURRENT")
        return reuse.PriorSelection(value, permit, "COMPARE")

    original = insight()
    priors = (original, change(original), change(original, conflict=True), replace(original, origin=None),
              insight("TASK-X", b"A different result.\n\nA different instrument.\n"))
    result = reuse.compare_supplied_priors(original, tuple(select(item) for item in priors),
        target=target, purpose="COMPARE", observed_at=now, enabled=True)

    # Reuse the real independent reconstruction consumer, without substituting it.
    proposal = strict_loads(original.proposal)
    grounding = {**strict_loads(original.grounding), "source_bytes": original.source_bytes}
    expected = evaluate_proposal(proposal, grounding_bundle=grounding)
    request = {"governance": {"analysis": {"retrosynthesis": proposal}},
               "repair": {"parent_id": "TASK-A", "parent_binding": dict(proposal["parent"])}}
    admission = {"native_request": {"meta": {"retrosynthesis": expected}},
                 "normalized_source_sha256": grounding["manifest"]["source_sha256"]}
    contents = {"native/grounding/segments.jsonl": b"".join(canonical_bytes(row) for row in grounding["segments"])}
    reconstructed = _check_reconstruction(request, admission, contents)
    if reconstructed != expected:
        raise RuntimeError("Independent reconstruction mismatch")
    return {"synthetic": True, "permits_are_synthetic_not_credentials": True,
            "provider_invoked": False, "comparison": result,
            "sophia_reconstruction_matches": True, "full_sophia_evaluation_performed": False}


if __name__ == "__main__":
    try:
        print(json.dumps(demonstration(), indent=2, ensure_ascii=False))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
