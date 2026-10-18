"""Deterministic, nonauthoritative claim references derived from captured bytes.

The captured candidate remains immutable and untrusted.  Only the exact
canonical envelope below is interpreted, and interpretation can create control
evidence only through fixed platform rules; candidate fields are never treated
as control results, findings, decisions, or authority.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from . import AUTHORITY_EFFECT, NONASSURANCE_NOTICE
from .canonical import CanonicalError, canonical_bytes, sha256_bytes, strict_loads


CANDIDATE_CLAIM_ENVELOPE_SCHEMA_ID = (
    "uvlm.triadicbrain.aep01.captured_candidate_claims.v1"
)
CLAIM_MAP_SCHEMA_ID = "uvlm.triadicbrain.aep01.candidate_claim_map.v1"
MAX_CLAIMS = 256
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def captured_claim_envelope(claims: list[Mapping[str, Any]]) -> bytes:
    """Render the documented structured-candidate envelope for local import."""

    return canonical_bytes(
        {
            "claims": [dict(row) for row in claims],
            "schema_id": CANDIDATE_CLAIM_ENVELOPE_SCHEMA_ID,
        }
    )


def derive_candidate_claim_map(
    *,
    transaction_id: str,
    candidate_bytes: bytes,
    source_bytes: bytes,
) -> dict[str, Any]:
    """Derive exact claim/source relations without mutating or trusting input."""

    claims: list[dict[str, Any]] = []
    extraction_status = "NO_STRUCTURED_CLAIM_ENVELOPE"
    try:
        candidate = strict_loads(candidate_bytes)
    except (CanonicalError, UnicodeError, ValueError):
        candidate = None
    if (
        isinstance(candidate, dict)
        and candidate.get("schema_id") == CANDIDATE_CLAIM_ENVELOPE_SCHEMA_ID
    ):
        extraction_status = "DECLARED_ENVELOPE_INVALID"
        source_claims = candidate.get("claims")
        if (
            set(candidate) == {"claims", "schema_id"}
            and isinstance(source_claims, list)
            and 0 < len(source_claims) <= MAX_CLAIMS
        ):
            parsed: list[dict[str, Any]] = []
            seen: set[str] = set()
            for source in source_claims:
                if not isinstance(source, Mapping) or set(source) != {
                    "claim_id",
                    "source_sha256",
                    "source_span",
                    "text",
                }:
                    parsed = []
                    break
                claim_id = source.get("claim_id")
                text = source.get("text")
                digest = source.get("source_sha256")
                span = source.get("source_span")
                if (
                    type(claim_id) is not str
                    or _IDENTIFIER.fullmatch(claim_id) is None
                    or claim_id in seen
                    or type(text) is not str
                    or not text
                    or len(text) > 4096
                    or type(digest) is not str
                    or _SHA256.fullmatch(digest) is None
                    or not isinstance(span, Mapping)
                    or set(span) != {"end", "start"}
                    or type(span.get("start")) is not int
                    or type(span.get("end")) is not int
                ):
                    parsed = []
                    break
                seen.add(claim_id)
                start = span["start"]
                end = span["end"]
                source_status = "BOUND"
                reason_codes = ["SOURCE_REFERENCE_BOUND"]
                if digest != sha256_bytes(source_bytes):
                    source_status = "SOURCE_DIGEST_MISMATCH"
                    reason_codes = ["SOURCE_DIGEST_MISMATCH"]
                elif start < 0 or end <= start or end > len(source_bytes):
                    source_status = "EVIDENCE_RANGE_INVALID"
                    reason_codes = ["EVIDENCE_RANGE_INVALID"]
                parsed.append(
                    {
                        "authority_effect": AUTHORITY_EFFECT,
                        "claim_id": claim_id,
                        "claimed_source_sha256": digest,
                        "claimed_source_span": {"end": end, "start": start},
                        "evidence_relation": "SUPPORTING_REFERENCE",
                        "reason_codes": reason_codes,
                        "source_binding_status": source_status,
                        "text": text,
                    }
                )
            if parsed:
                claims = parsed
                extraction_status = "STRUCTURED_CLAIMS_DERIVED"
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "candidate_sha256": sha256_bytes(candidate_bytes),
        "claim_extraction_status": extraction_status,
        "claims": claims,
        "nonauthority": (
            f"{NONASSURANCE_NOTICE} Candidate claims and references remain "
            "untrusted observations; matching a digest does not establish truth."
        ),
        "schema_id": CLAIM_MAP_SCHEMA_ID,
        "transaction_id": transaction_id,
    }


def claim_control_observations(
    claim_map: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Return fixed control observations for a recognized claim envelope."""

    if claim_map.get("claim_extraction_status") == "DECLARED_ENVELOPE_INVALID":
        return {
            "AI-CLM-01": {
                "observed_condition": (
                    "The declared captured-candidate claim envelope was malformed; "
                    "no evidence reference was silently accepted."
                ),
                "reason_codes": ["CANDIDATE_CLAIM_ENVELOPE_INVALID"],
                "result": "HOLD",
            },
            "AI-CLM-02": {
                "observed_condition": (
                    "Malformed candidate claim metadata remains visible for review."
                ),
                "reason_codes": ["INVALID_CLAIM_METADATA_EXPOSED"],
                "result": "HOLD",
            },
        }
    claims = claim_map.get("claims")
    if not isinstance(claims, list) or not claims:
        return {}
    statuses = [str(row.get("source_binding_status")) for row in claims]
    if "SOURCE_DIGEST_MISMATCH" in statuses:
        primary_result = "FAIL"
        primary_reason = "SOURCE_DIGEST_MISMATCH"
        primary_observation = (
            "At least one captured candidate claim references a source digest "
            "different from the immutable transaction source."
        )
    elif "EVIDENCE_RANGE_INVALID" in statuses:
        primary_result = "FAIL"
        primary_reason = "EVIDENCE_RANGE_INVALID"
        primary_observation = (
            "At least one captured candidate claim references a source span outside "
            "the immutable transaction source."
        )
    else:
        primary_result = "PASS"
        primary_reason = "AUTHENTICATED_PLATFORM_CONDITION_OBSERVED"
        primary_observation = (
            "Every structured captured-candidate claim reference matches the "
            "immutable source digest and a bounded source span."
        )
    adverse = primary_result != "PASS"
    return {
        "AI-CLM-01": {
            "observed_condition": primary_observation,
            "reason_codes": [primary_reason],
            "result": primary_result,
        },
        "AI-CLM-02": {
            "observed_condition": (
                "Misbound or invalid candidate claim references were exposed as "
                "review findings."
                if adverse
                else "No unsupported or misbound structured claim reference was observed."
            ),
            "reason_codes": [
                "MISBOUND_CLAIM_EXPOSED"
                if adverse
                else "AUTHENTICATED_PLATFORM_CONDITION_OBSERVED"
            ],
            "result": "HOLD" if adverse else "PASS",
        },
    }


__all__ = [
    "CANDIDATE_CLAIM_ENVELOPE_SCHEMA_ID",
    "CLAIM_MAP_SCHEMA_ID",
    "captured_claim_envelope",
    "claim_control_observations",
    "derive_candidate_claim_map",
]
