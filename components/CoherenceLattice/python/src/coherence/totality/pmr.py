"""Separately consented, append-only PMR reference lifecycle with no writes."""

from __future__ import annotations

import copy
from datetime import datetime, timezone
import re
from typing import Any, Mapping

from .canonical import require_exact_keys, require_identifier, require_sha256, validate_unicode_text
from .errors import ValidationError

PMR_CONSENT_SCHEMA = "uvlm.pmr.totality.consent.v1"
PMR_EVENT_SCHEMA = "uvlm.pmr.totality.reference_event.v1"
PMR_RECEIPT_SCHEMA = "uvlm.pmr.totality.receipt.v1"
_CONSENT_KEYS = {
    "schema_id", "consent_id", "run_id", "candidate_id", "logical_time", "decision", "scope",
    "quota_bytes", "expires_logical_time", "training_allowed", "federation_allowed", "authority_effect",
}
_RFC3339_UTC = re.compile(
    r"^[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])T"
    r"(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]{1,9})?Z$"
)


def _logical_time(value: Any, path: str) -> str:
    validate_unicode_text(value, path, allow_newlines=False)
    if not value or len(value) > 128:
        raise ValidationError(f"PMR_LOGICAL_TIME_INVALID:{path}")
    return value


def _utc_instant(value: Any, path: str) -> tuple[datetime, int]:
    logical_time = _logical_time(value, path)
    if _RFC3339_UTC.fullmatch(logical_time) is None:
        raise ValidationError(f"PMR_EXPIRY_TIME_RFC3339_UTC_REQUIRED:{path}")
    try:
        parsed = datetime.fromisoformat(logical_time[:19] + "+00:00")
    except ValueError as exc:
        raise ValidationError(f"PMR_EXPIRY_TIME_INVALID:{path}") from exc
    if parsed.tzinfo != timezone.utc:
        raise ValidationError(f"PMR_EXPIRY_TIME_UTC_REQUIRED:{path}")
    fraction = logical_time[20:-1] if len(logical_time) > 20 else ""
    nanoseconds = int(fraction.ljust(9, "0")) if fraction else 0
    return parsed, nanoseconds


def build_consent_packet(
    *,
    consent_id: str,
    run_id: str,
    candidate_id: str,
    logical_time: str,
    decision: str,
    quota_bytes: int = 1_048_576,
    expires_logical_time: str | None = None,
) -> dict[str, Any]:
    if decision not in {"GRANT", "DENY"}:
        raise ValidationError("PMR_CONSENT_DECISION_INVALID")
    if isinstance(quota_bytes, bool) or not isinstance(quota_bytes, int) or not 1 <= quota_bytes <= 100_000_000:
        raise ValidationError("PMR_CONSENT_QUOTA_INVALID")
    logical_time = _logical_time(logical_time, "$.logical_time")
    if expires_logical_time is not None:
        issued = _utc_instant(logical_time, "$.logical_time")
        expires = _utc_instant(expires_logical_time, "$.expires_logical_time")
        if expires <= issued:
            raise ValidationError("PMR_EXPIRY_NOT_AFTER_CONSENT")
    return {
        "schema_id": PMR_CONSENT_SCHEMA,
        "consent_id": require_identifier(consent_id, "$.consent_id"),
        "run_id": require_identifier(run_id, "$.run_id"),
        "candidate_id": require_identifier(candidate_id, "$.candidate_id"),
        "logical_time": logical_time,
        "decision": decision,
        "scope": "PROVENANCE_REFERENCE_ONLY",
        "quota_bytes": quota_bytes,
        "expires_logical_time": expires_logical_time,
        "training_allowed": False,
        "federation_allowed": False,
        "authority_effect": "NONE",
    }


def validate_consent_packet(value: Any) -> dict[str, Any]:
    require_exact_keys(value, required=_CONSENT_KEYS)
    rebuilt = build_consent_packet(
        consent_id=value["consent_id"], run_id=value["run_id"], candidate_id=value["candidate_id"],
        logical_time=value["logical_time"], decision=value["decision"], quota_bytes=value["quota_bytes"],
        expires_logical_time=value["expires_logical_time"],
    )
    if rebuilt != value:
        raise ValidationError("PMR_CONSENT_PACKET_INVALID")
    return rebuilt


def no_write_receipt(*, run_id: str, candidate_id: str, logical_time: str, reason: str) -> dict[str, Any]:
    require_identifier(reason, "$.reason")
    return {
        "schema_id": PMR_RECEIPT_SCHEMA,
        "run_id": require_identifier(run_id, "$.run_id"),
        "candidate_id": require_identifier(candidate_id, "$.candidate_id"),
        "logical_time": logical_time,
        "mode": "NO_WRITE_REFERENCE_IMPLEMENTATION",
        "consent_id": None,
        "consent_status": "NOT_GRANTED",
        "reason_codes": [reason],
        "events": [],
        "retained": False,
        "persistent_bytes_written": 0,
        "network_used": False,
        "federation_used": False,
        "training_used": False,
        "authority_effect": "NONE",
    }


class PMRReferenceStore:
    """In-memory reference state; no content copy, reinjection, or training.

    The lifecycle is a contracted/dormant reference implementation. Sophia- or
    human-authorized retention transitions and prior reinjection are not active.
    """

    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []
        self._consents: dict[str, dict[str, Any]] = {}
        self._lineages: dict[str, dict[str, Any]] = {}

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(copy.deepcopy(row) for row in self._events)

    def _append(self, event_type: str, consent: Mapping[str, Any], lineage_id: str | None, detail: Mapping[str, Any]) -> dict[str, Any]:
        sequence = len(self._events) + 1
        row = {
            "schema_id": PMR_EVENT_SCHEMA,
            "sequence": sequence,
            "logical_time": f"PMR+{sequence:06d}",
            "event_type": event_type,
            "consent_id": consent["consent_id"],
            "run_id": consent["run_id"],
            "candidate_id": consent["candidate_id"],
            "lineage_id": lineage_id,
            "detail": copy.deepcopy(dict(detail)),
            "persistent_write_performed": False,
            "training_used": False,
            "federation_used": False,
            "authority_effect": "NONE",
        }
        self._events.append(row)
        return copy.deepcopy(row)

    def apply_consent(self, packet: Any) -> dict[str, Any]:
        consent = validate_consent_packet(packet)
        if consent["consent_id"] in self._consents:
            raise ValidationError("PMR_CONSENT_ALREADY_RECORDED")
        self._consents[consent["consent_id"]] = {**consent, "active": consent["decision"] == "GRANT"}
        return self._append(
            "CONSENT_GRANTED" if consent["decision"] == "GRANT" else "CONSENT_DENIED",
            consent, None, {"scope": consent["scope"], "quota_bytes": consent["quota_bytes"]},
        )

    def retain_reference(
        self,
        *,
        consent_id: str,
        lineage_id: str,
        artifact_sha256: str,
        referenced_bytes: int,
    ) -> dict[str, Any]:
        consent = self._active(consent_id)
        lineage_id = require_identifier(lineage_id, "$.lineage_id")
        artifact_sha256 = require_sha256(artifact_sha256, "$.artifact_sha256")
        if lineage_id in self._lineages:
            raise ValidationError("PMR_LINEAGE_ALREADY_EXISTS")
        if isinstance(referenced_bytes, bool) or not isinstance(referenced_bytes, int) or referenced_bytes < 0:
            raise ValidationError("PMR_REFERENCED_BYTES_INVALID")
        used = sum(row["referenced_bytes"] for row in self._lineages.values() if row["consent_id"] == consent_id)
        if used + referenced_bytes > consent["quota_bytes"]:
            raise ValidationError("PMR_REFERENCE_QUOTA_EXCEEDED")
        self._lineages[lineage_id] = {
            "lineage_id": lineage_id, "consent_id": consent_id, "artifact_sha256": artifact_sha256,
            "referenced_bytes": referenced_bytes, "status": "ACTIVE", "corrections": [],
        }
        return self._append("REFERENCE_RETAINED", consent, lineage_id, self._lineages[lineage_id])

    def revoke(self, consent_id: str, *, reason: str) -> dict[str, Any]:
        consent = self._active(consent_id)
        require_identifier(reason, "$.reason")
        consent["active"] = False
        for row in self._lineages.values():
            if row["consent_id"] == consent_id and row["status"] == "ACTIVE":
                row["status"] = "REVOKED"
        return self._append("CONSENT_REVOKED", consent, None, {"reason": reason})

    def correct(self, consent_id: str, lineage_id: str, *, replacement_sha256: str) -> dict[str, Any]:
        consent = self._active(consent_id)
        lineage = self._lineage(consent_id, lineage_id)
        replacement = require_sha256(replacement_sha256, "$.replacement_sha256")
        lineage["corrections"].append(replacement)
        lineage["artifact_sha256"] = replacement
        return self._append("REFERENCE_CORRECTED", consent, lineage_id, {"replacement_sha256": replacement})

    def delete(self, consent_id: str, lineage_id: str, *, reason: str) -> dict[str, Any]:
        consent = self._active(consent_id)
        lineage = self._lineage(consent_id, lineage_id)
        require_identifier(reason, "$.reason")
        lineage["status"] = "DELETED_TOMBSTONE"
        return self._append("REFERENCE_DELETED", consent, lineage_id, {"reason": reason})

    def retrieve(self, lineage_id: str, *, logical_time: str) -> dict[str, Any]:
        lineage_id = require_identifier(lineage_id, "$.lineage_id")
        logical_time = _logical_time(logical_time, "$.retrieval_logical_time")
        lineage = self._lineages.get(lineage_id)
        if lineage is None:
            raise ValidationError("PMR_LINEAGE_NOT_FOUND")
        consent = self._consents.get(lineage["consent_id"])
        if consent is None or consent.get("active") is not True or consent.get("decision") != "GRANT":
            raise ValidationError("PMR_ACTIVE_CONSENT_REQUIRED")
        if lineage.get("status") != "ACTIVE":
            raise ValidationError("PMR_ACTIVE_LINEAGE_REQUIRED")
        expiry = consent.get("expires_logical_time")
        if expiry is not None:
            retrieved = _utc_instant(logical_time, "$.retrieval_logical_time")
            if retrieved >= _utc_instant(expiry, "$.expires_logical_time"):
                raise ValidationError("PMR_CONSENT_EXPIRED")
        return {
            **copy.deepcopy(lineage),
            "retrieval_logical_time": logical_time,
            "active_consent_verified": True,
            "content_stored": False,
            "training_eligible": False,
        }

    def receipt(self, consent_id: str) -> dict[str, Any]:
        consent = self._consents.get(consent_id)
        if consent is None:
            raise ValidationError("PMR_CONSENT_NOT_FOUND")
        events = [copy.deepcopy(row) for row in self._events if row["consent_id"] == consent_id]
        retained = any(row["event_type"] == "REFERENCE_RETAINED" for row in events)
        return {
            "schema_id": PMR_RECEIPT_SCHEMA,
            "run_id": consent["run_id"], "candidate_id": consent["candidate_id"],
            "logical_time": consent["logical_time"], "mode": "NO_WRITE_REFERENCE_IMPLEMENTATION",
            "consent_id": consent_id, "consent_status": "ACTIVE" if consent["active"] else "INACTIVE",
            "reason_codes": ["REFERENCE_EVENTS_ONLY_NO_CONTENT_WRITE"], "events": events,
            "retained": retained, "persistent_bytes_written": 0, "network_used": False,
            "federation_used": False, "training_used": False, "authority_effect": "NONE",
        }

    def _active(self, consent_id: str) -> dict[str, Any]:
        consent = self._consents.get(consent_id)
        if consent is None or consent.get("active") is not True:
            raise ValidationError("PMR_ACTIVE_CONSENT_REQUIRED")
        return consent

    def _lineage(self, consent_id: str, lineage_id: str) -> dict[str, Any]:
        lineage = self._lineages.get(lineage_id)
        if lineage is None or lineage["consent_id"] != consent_id or lineage["status"] != "ACTIVE":
            raise ValidationError("PMR_ACTIVE_LINEAGE_REQUIRED")
        return lineage


class SyntheticPriorLifecycle:
    """Opt-in synthetic exercise of the existing reference store, not a database.

    The caller must authenticate principals before this boundary. Exact distinct
    principal IDs implement role authorization here; a role string in a candidate
    never grants authority. This in-memory API has no persistence, provider or
    training capability. It is intentionally not wired to personal retention.
    Legacy PMRReferenceStore packets and behavior remain independently readable.
    """

    def __init__(self, *, enabled=False, principals=None):
        self.enabled = enabled is True
        self.principals = copy.deepcopy(principals or {})
        if self.enabled and (set(self.principals) != {'owner', 'sophia', 'custodian', 'consumer'}
                or len(set(self.principals.values())) != 4
                or any(not isinstance(v, str) or not v.strip() for v in self.principals.values())):
            raise ValidationError('PMR_DISTINCT_AUTHENTICATED_PRINCIPALS_REQUIRED')
        self._store = PMRReferenceStore()
        self._audits = {}
        self._reuse_audits = {}
        self._reuse = {}
        self._journal = []
        self._last_time = None

    @property
    def events(self):
        return tuple(copy.deepcopy(self._journal))

    def _role(self, actor, role):
        if not self.enabled:
            raise ValidationError('PMR_DISABLED')
        if actor != self.principals[role]:
            raise ValidationError('PMR_ROLE_DENIED')

    def _time(self, value):
        instant = _utc_instant(value, '$.observed_at')
        if self._last_time is not None and instant < self._last_time:
            raise ValidationError('PMR_TIME_ROLLBACK')
        return instant

    def _event(self, kind, actor, observed_at, detail):
        from .canonical import canonical_json_bytes, sha256_bytes
        instant = self._time(observed_at)
        row = {'schema_id': 'uvlm.pmr.synthetic-lifecycle-event.v1',
            'sequence': len(self._journal)+1, 'kind': kind, 'actor': actor,
            'observed_at': observed_at, 'origin': 'SYNTHETIC_LIFECYCLE',
            'detail': copy.deepcopy(detail), 'authority_effect': 'NONE',
            'previous_sha256': self._journal[-1]['sha256'] if self._journal else None}
        row['sha256'] = sha256_bytes(canonical_json_bytes(row))
        self._journal.append(row); self._last_time = instant
        return copy.deepcopy(row)

    def grant_retention(self, actor, consent, *, observed_at):
        self._role(actor, 'owner'); instant = self._time(observed_at)
        packet = validate_consent_packet(consent)
        if packet['expires_logical_time'] is None:
            raise ValidationError('PMR_BOUNDED_EXPIRY_REQUIRED')
        if not _utc_instant(packet['logical_time'], '$.logical_time') <= instant < _utc_instant(packet['expires_logical_time'], '$.expiry'):
            raise ValidationError('PMR_CONSENT_TIME_INVALID')
        self._store.apply_consent(packet)
        return self._event('RETENTION_CONSENT_RECORDED', actor, observed_at, packet)

    def _active(self, consent_id, observed_at):
        instant = self._time(observed_at)
        consent = self._store._active(consent_id)
        if not _utc_instant(consent['logical_time'], '$.issued') <= instant < _utc_instant(consent['expires_logical_time'], '$.expiry'):
            raise ValidationError('PMR_CONSENT_EXPIRED_OR_NOT_YET_VALID')
        return consent

    def audit_candidate(self, actor, *, consent_id, artifact_sha256, disposition, rationale, observed_at):
        self._role(actor, 'sophia'); self._active(consent_id, observed_at)
        digest = require_sha256(artifact_sha256, '$.artifact_sha256')
        if disposition not in {'PASS', 'HOLD', 'REJECT'} or not isinstance(rationale, str) or not 1 <= len(rationale.strip()) <= 2048:
            raise ValidationError('PMR_AUDIT_DISPOSITION_REQUIRED')
        event = self._event('SOPHIA_RETENTION_AUDIT', actor, observed_at,
            {'consent_id': consent_id, 'artifact_sha256': digest, 'disposition': disposition,
             'rationale': rationale, 'scope': 'Reference retention suitability, not semantic truth'})
        self._audits[(consent_id, digest)] = event
        return event

    def _audited(self, consent_id, digest):
        audit = self._audits.get((consent_id, digest))
        if audit is None or audit['detail']['disposition'] != 'PASS':
            raise ValidationError('PMR_PASS_RETENTION_AUDIT_REQUIRED')
        return audit

    def retain(self, actor, *, consent_id, lineage_id, artifact_sha256, referenced_bytes, observed_at):
        self._role(actor, 'custodian'); self._active(consent_id, observed_at)
        audit = self._audited(consent_id, artifact_sha256)
        self._store.retain_reference(consent_id=consent_id, lineage_id=lineage_id,
            artifact_sha256=artifact_sha256, referenced_bytes=referenced_bytes)
        return self._event('REFERENCE_RETAINED', actor, observed_at,
            {'consent_id': consent_id, 'lineage_id': lineage_id, 'artifact_sha256': artifact_sha256,
             'referenced_bytes': referenced_bytes, 'audit_sha256': audit['sha256']})

    def correct(self, actor, *, consent_id, lineage_id, replacement_sha256, reason, observed_at, replacement_bytes=None):
        self._role(actor, 'custodian'); self._active(consent_id, observed_at)
        prior = self._store._lineage(consent_id, lineage_id)
        old = prior['artifact_sha256']
        if old == replacement_sha256 or not isinstance(reason, str) or not 1 <= len(reason.strip()) <= 2048:
            raise ValidationError('PMR_CORRECTION_NEW_REFERENCE_AND_REASON_REQUIRED')
        audit = self._audited(consent_id, replacement_sha256)
        size=prior['referenced_bytes'] if replacement_bytes is None else replacement_bytes
        if type(size) is not int or size<0:raise ValidationError('PMR_REFERENCED_BYTES_INVALID')
        consent=self._active(consent_id,observed_at)
        used=sum(r['referenced_bytes'] for r in self._store._lineages.values()
            if r['consent_id']==consent_id and r['lineage_id']!=lineage_id)
        if used+size>consent['quota_bytes']:raise ValidationError('PMR_REFERENCE_QUOTA_EXCEEDED')
        self._store.correct(consent_id, lineage_id, replacement_sha256=replacement_sha256)
        prior['referenced_bytes']=size
        # Earlier grants bind the earlier bytes; they cannot silently follow a correction.
        return self._event('REFERENCE_CORRECTED', actor, observed_at,
            {'consent_id': consent_id, 'lineage_id': lineage_id, 'prior_sha256': old,
             'replacement_sha256': replacement_sha256, 'replacement_bytes':size,
             'reason': reason, 'audit_sha256': audit['sha256']})

    def grant_reuse(self, actor, *, consent_id, lineage_id, target_run_id, purpose, expires_at, observed_at):
        self._role(actor, 'owner'); consent = self._active(consent_id, observed_at)
        lineage = self._store._lineage(consent_id, lineage_id)
        target = require_identifier(target_run_id, '$.target_run_id')
        require_identifier(purpose, '$.purpose')
        if purpose not in {'COMPARE', 'CONTEXT_HYPOTHESIS'}:
            raise ValidationError('PMR_REFERENCE_REUSE_PURPOSE_UNSUPPORTED')
        if not self._time(observed_at) < _utc_instant(expires_at, '$.expires_at') <= _utc_instant(consent['expires_logical_time'], '$.retention_expiry'):
            raise ValidationError('PMR_REUSE_EXPIRY_INVALID')
        event = self._event('SEPARATE_REUSE_CONSENT', actor, observed_at,
            {'consent_id': consent_id, 'lineage_id': lineage_id, 'target_run_id': target,
             'purpose': purpose, 'expires_at': expires_at, 'artifact_sha256': lineage['artifact_sha256']})
        self._reuse[event['sha256']] = event
        return event

    def _reuse_scope(self, grant_sha256, target_run_id, purpose, observed_at):
        instant = self._time(observed_at)
        grant = self._reuse.get(grant_sha256)
        if grant is None:
            raise ValidationError('PMR_SEPARATE_REUSE_CONSENT_REQUIRED')
        detail = grant['detail']; self._active(detail['consent_id'], observed_at)
        if (detail['target_run_id'] != target_run_id or detail['purpose'] != purpose
                or instant >= _utc_instant(detail['expires_at'], '$.reuse_expiry')):
            raise ValidationError('PMR_REUSE_SCOPE_OR_EXPIRY_MISMATCH')
        value = self._store.retrieve(detail['lineage_id'], logical_time=observed_at)
        if value['artifact_sha256'] != detail['artifact_sha256']:
            raise ValidationError('PMR_CORRECTED_PRIOR_REQUIRES_NEW_REUSE_CONSENT')
        self._audited(detail['consent_id'],value['artifact_sha256'])
        return value

    def audit_reuse(self, actor, *, grant_sha256, target_run_id, purpose, disposition, rationale, observed_at):
        """A separate Sophia decision for this exact query, not retention passage."""
        self._role(actor, 'sophia')
        value=self._reuse_scope(grant_sha256,target_run_id,purpose,observed_at)
        if disposition not in {'PASS','HOLD','REJECT'} or not isinstance(rationale,str) or not 1<=len(rationale.strip())<=2048:
            raise ValidationError('PMR_AUDIT_DISPOSITION_REQUIRED')
        row=self._event('SOPHIA_REINJECTION_AUDIT',actor,observed_at,
            {'grant_sha256':grant_sha256,'target_run_id':target_run_id,'purpose':purpose,
             'artifact_sha256':value['artifact_sha256'],'disposition':disposition,'rationale':rationale,
             'scope':'This bounded prior reference query only; not source truth or automatic reinjection'})
        self._reuse_audits[grant_sha256]=row
        return row

    def retrieve(self, actor, *, grant_sha256, target_run_id, purpose, observed_at):
        self._role(actor, 'consumer')
        value=self._reuse_scope(grant_sha256,target_run_id,purpose,observed_at)
        audit=self._reuse_audits.get(grant_sha256)
        if audit is None or audit['detail']['disposition']!='PASS':
            raise ValidationError('PMR_PASS_REINJECTION_AUDIT_REQUIRED')
        self._event('PRIOR_REFERENCE_RETRIEVED', actor, observed_at,
            {'grant_sha256': grant_sha256, 'target_run_id': target_run_id,
             'artifact_sha256': value['artifact_sha256'], 'reuse_audit_sha256':audit['sha256'],
             'not_source_evidence': True})
        return copy.deepcopy(value)

    def record_reinjection(self, actor, *, grant_sha256, target_run_id, purpose, request_sha256, supplied_bytes, observed_at):
        """Audit an explicitly requested, hash-bound prior; never dispatch or inject."""
        from .canonical import sha256_bytes
        self._role(actor, 'consumer')
        if type(supplied_bytes) is not bytes or len(supplied_bytes) > 1_048_576:
            raise ValidationError('PMR_REINJECTION_BODY_BOUND')
        request_sha256 = require_sha256(request_sha256, '$.request_sha256')
        # Validate all fields before recording retrieval (failure cannot look like use).
        grant = self._reuse.get(grant_sha256)
        if grant is None or sha256_bytes(supplied_bytes) != grant['detail']['artifact_sha256']:
            raise ValidationError('PMR_PRIOR_BYTES_CHANGED')
        lineage=self._store._lineage(grant['detail']['consent_id'],grant['detail']['lineage_id'])
        if len(supplied_bytes)!=lineage['referenced_bytes']:raise ValidationError('PMR_PRIOR_SIZE_CHANGED')
        value = self.retrieve(actor, grant_sha256=grant_sha256, target_run_id=target_run_id,
            purpose=purpose, observed_at=observed_at)
        return self._event('PRIOR_INFLUENCE_DECLARED', actor, observed_at,
            {'grant_sha256': grant_sha256, 'request_sha256': request_sha256,
             'target_run_id': target_run_id, 'prior_sha256': value['artifact_sha256'],
             'classification': 'NON_AUTHORITATIVE_PRIOR_NOT_GROUNDING',
             'automatic_reinjection': False, 'dispatch_performed': False})

    def revoke(self, actor, *, consent_id, reason, observed_at):
        self._role(actor, 'owner'); self._time(observed_at)
        self._store.revoke(consent_id, reason=reason)
        return self._event('RETENTION_AND_REUSE_REVOKED', actor, observed_at,
            {'consent_id': consent_id, 'reason': reason})

    def delete(self, actor, *, consent_id, lineage_id, reason, observed_at):
        self._role(actor, 'custodian'); self._time(observed_at)
        # A tombstone never authorizes retrieval or removes audit history. Cleanup
        # remains possible after expiry/revocation; content was never stored here.
        lineage = self._store._lineages.get(lineage_id)
        if lineage is None or lineage['consent_id'] != consent_id or lineage['status'] == 'DELETED_TOMBSTONE':
            raise ValidationError('PMR_DELETION_SCOPE_INVALID')
        require_identifier(reason, '$.reason')
        lineage['status'] = 'DELETED_TOMBSTONE'
        return self._event('REFERENCE_TOMBSTONED', actor, observed_at,
            {'consent_id': consent_id, 'lineage_id': lineage_id, 'reason': reason})
