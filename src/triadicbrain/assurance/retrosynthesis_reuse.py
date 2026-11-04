"""Pure, opt-in comparison of explicitly supplied declared retrosyntheses.

This leaf does not authenticate a grant, query a store, retain a reference,
materialize provider context or dispatch. The native caller must supply exact
authorized bytes and recheck current authority at its atomic use boundary.
Hashes and the frozen inputs below detect substitution; they are not credentials.
Historical same-root assistance and no-write PMR readers remain separate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import re

from .canonical import canonical_bytes, sha256_bytes, strict_loads

MAX_PRIORS = 16
MAX_ARTIFACT_BYTES = 16 * 1024
COMPARISON_SCHEMA = 'control-anchor.retrosynthesis-comparison.v1'
REFERENCE_SCHEMA = 'control-anchor.retrosynthesis-reference.v1'
RECEIPT_SCHEMA = 'control-anchor.persistent-prior-reference-receipt.v1'
PURPOSES = frozenset({'COMPARE', 'CONTEXT_HYPOTHESIS'})
_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z')
_HASH = re.compile(r'[0-9a-f]{64}\Z')
_COMMIT = re.compile(r'[0-9a-f]{40}\Z')
_UTC = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z\Z')


def _identifier(value):
    if type(value) is not str or not _ID.fullmatch(value):
        raise ValueError('REUSE_IDENTIFIER_INVALID')


def _digest(value):
    if type(value) is not str or not _HASH.fullmatch(value):
        raise ValueError('REUSE_DIGEST_INVALID')


def _instant(value):
    if type(value) is not str or not _UTC.fullmatch(value):
        raise ValueError('REUSE_UTC_TIME_REQUIRED')
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('REUSE_UTC_TIME_REQUIRED') from exc


@dataclass(frozen=True)
class TargetBinding:
    organization_id: str
    application_id: str
    principal_id: str
    task_id: str
    request_sha256: str
    profile_sha256: str
    scope_id: str


@dataclass(frozen=True)
class OriginBinding:
    """Original native binding; never synthesized from a future task/query."""
    organization_id: str
    application_id: str
    record_id: str
    request_sha256: str
    response_sha256: str
    decision_sha256: str
    profile_sha256: str
    source_commit: str
    derived_from_sha256: tuple[str, ...] = ()


@dataclass(frozen=True)
class InsightInput:
    proposal: bytes
    source_bytes: bytes
    grounding: bytes
    scope_id: str
    origin: OriginBinding | None


@dataclass(frozen=True)
class ReusePermit:
    """Native caller's current snapshot, not a portable authorization token.

    A production consumer must authenticate grant/audit ownership, quota/privacy,
    correction and revocation in existing custody. Retention alone is insufficient.
    This leaf checks the exact supplied target/reference/purpose/time bindings.
    """
    reference_sha256: str
    target: TargetBinding
    purpose: str
    grant_sha256: str
    audit_sha256: str
    valid_from: str
    expires_at: str
    observed_at: str
    status: str


@dataclass(frozen=True)
class PriorSelection:
    insight: InsightInput
    permit: ReusePermit
    mode: str
    vocabulary: str = 'NATIVE_V1'


def reconcile_mode(mode, *, vocabulary, purpose):
    """Explicitly cap legacy modes; never feed unknown modes to a lax auditor.

    Stronger answer-support/novelty/citation modes are unsupported in this slice.
    Router rank-3 cite_if_verified is not claimed to be a reachable output.
    A permitted mapping describes a view purpose, not a grant or a Sophia PASS.
    """
    if type(purpose) is not str or purpose not in PURPOSES:
        raise ValueError('REUSE_PURPOSE_UNSUPPORTED')
    if type(mode) is not str or type(vocabulary) is not str:
        raise ValueError('REUSE_MODE_UNSUPPORTED')
    if vocabulary == 'NATIVE_V1':
        capabilities = {'COMPARE': {'COMPARE'},
                        'CONTEXT_HYPOTHESIS': set(PURPOSES)}
    elif vocabulary in {'LEGACY_ROUTER_V1', 'LEGACY_AUDITOR_V1'}:
        capabilities = {
            'ignore': set(), 'shadow_only': {'COMPARE'},
            'background_only': set(PURPOSES), 'context_only': set(PURPOSES),
            'answer_support': set(), 'novelty_extension': set(),
            'cite_if_verified': set(),
        }
    else:
        raise ValueError('REUSE_MODE_VOCABULARY_UNSUPPORTED')
    if mode not in capabilities or purpose not in capabilities[mode]:
        raise ValueError('REUSE_MODE_NOT_PERMITTED')
    return purpose


def _target(value):
    if type(value) is not TargetBinding:
        raise ValueError('REUSE_TARGET_BINDING_REQUIRED')
    for name in ('organization_id', 'application_id', 'principal_id', 'task_id', 'scope_id'):
        _identifier(getattr(value, name))
    _digest(value.request_sha256)
    _digest(value.profile_sha256)


def _insight(value):
    if type(value) is not InsightInput:
        raise ValueError('REUSE_INSIGHT_REQUIRED')
    _identifier(value.scope_id)
    proposal = strict_loads(value.proposal, maximum_bytes=MAX_ARTIFACT_BYTES)
    if type(value.source_bytes) is not bytes or not 1 <= len(value.source_bytes) <= MAX_ARTIFACT_BYTES:
        raise ValueError('REUSE_EXACT_SOURCE_BYTES_BOUND_REQUIRED')
    # Use the maintained declared-alternative and exact-source validators. This
    # recount is not Sophia's separately attributable governed evaluation.
    from coherence.totality.retrosynthesis import evaluate_proposal
    projection = strict_loads(value.grounding, maximum_bytes=MAX_ARTIFACT_BYTES)
    if type(projection) is not dict or set(projection) != {'manifest', 'normalized_source', 'segments'}:
        raise ValueError('REUSE_RETAINED_GROUNDING_PROJECTION_REQUIRED')
    # Native bundle bytes travel separately from its JSON projection. Reinsert
    # those exact bytes, then let the maintained validator check the retained
    # manifest/segments; do not regenerate a successful replacement projection.
    grounding = {**projection, 'source_bytes': value.source_bytes}
    result = evaluate_proposal(proposal, grounding_bundle=grounding)
    origin = value.origin
    if origin is not None:
        if type(origin) is not OriginBinding:
            raise ValueError('REUSE_ORIGINAL_ORIGIN_INVALID')
        for name in ('organization_id', 'application_id', 'record_id'):
            _identifier(getattr(origin, name))
        for name in ('request_sha256', 'response_sha256', 'decision_sha256', 'profile_sha256'):
            _digest(getattr(origin, name))
        if type(origin.source_commit) is not str or not _COMMIT.fullmatch(origin.source_commit):
            raise ValueError('REUSE_SOURCE_COMMIT_INVALID')
        links = origin.derived_from_sha256
        if (type(links) is not tuple or len(links) > MAX_PRIORS
                or any(type(item) is not str for item in links)):
            raise ValueError('REUSE_LINEAGE_BOUND_REQUIRED')
        for item in links:
            _digest(item)
        if len(set(links)) != len(links):
            raise ValueError('REUSE_LINEAGE_DUPLICATE')
        if result['parent'] != {name: getattr(origin, name) for name in
                ('record_id', 'request_sha256', 'response_sha256', 'decision_sha256')}:
            raise ValueError('REUSE_ORIGINAL_PARENT_MISMATCH')
    return result


def _metadata(insight):
    return {'schema_id': REFERENCE_SCHEMA, 'scope_id': insight.scope_id,
            'proposal_sha256': sha256_bytes(insight.proposal),
            'source_sha256': sha256_bytes(insight.source_bytes),
            'grounding_sha256': sha256_bytes(insight.grounding),
            'origin': None if insight.origin is None else {
                **asdict(insight.origin),
                'derived_from_sha256': list(insight.origin.derived_from_sha256)}}


def reference_metadata(insight):
    """Immutable projection; missing original origin stays null.

    This binds exact proposal/source/retained-grounding bytes and original native
    metadata, including dependency links. Calling it does not retain anything.
    """
    _insight(insight)
    return _metadata(insight)


def _reference_hash(insight):
    # Private callers have already validated the exact insight once.
    return sha256_bytes(canonical_bytes(_metadata(insight)))


def _check_selection(selection, target, purpose, observed_at):
    if type(selection) is not PriorSelection or type(selection.permit) is not ReusePermit:
        raise ValueError('REUSE_EXPLICIT_SELECTION_REQUIRED')
    reconcile_mode(selection.mode, vocabulary=selection.vocabulary, purpose=purpose)
    permit = selection.permit
    _target(permit.target)
    for value in (permit.reference_sha256, permit.grant_sha256, permit.audit_sha256):
        _digest(value)
    now = _instant(observed_at)
    if (permit.status != 'CURRENT' or permit.purpose != purpose or permit.target != target
            or _instant(permit.observed_at) != now
            or not _instant(permit.valid_from) <= now < _instant(permit.expires_at)):
        raise ValueError('REUSE_CURRENT_TARGET_PURPOSE_AUTHORITY_REQUIRED')
    result = _insight(selection.insight)
    if permit.reference_sha256 != _reference_hash(selection.insight):
        raise ValueError('REUSE_REFERENCE_SUBSTITUTION')
    _scope(selection.insight, target)
    return result


def _scope(insight, target):
    if insight.scope_id != target.scope_id:
        raise ValueError('REUSE_SCOPE_MISMATCH')
    if insight.origin is not None and (
            insight.origin.organization_id != target.organization_id
            or insight.origin.application_id != target.application_id):
        raise ValueError('REUSE_ORGANIZATION_APPLICATION_MISMATCH')


def _relations(result):
    # Compare declared reference roles only for an identical explanation and
    # identical source segment. This is not a semantic contradiction detector.
    roles = {}
    for row in result['alternatives']:
        for ref in row['references']:
            key = (result['source_sha256'], row['explanation'],
                   ref['segment_id'], ref['segment_sha256'])
            roles.setdefault(key, set()).add(ref['relation'])
    return roles


def compare_supplied_priors(candidate, priors, *, target, purpose, observed_at, enabled=False):
    """Compare a finite already-authorized set, without lookup or context injection.

    All dispositions concern supplied declarations. Exact duplicate is byte/binding
    identity, related is dependency overlap, and conflict is an explicit reference
    role disagreement. None establishes truth, global novelty or corroboration.
    """
    if enabled is not True:
        raise ValueError('REUSE_COMPARISON_DISABLED')
    _target(target)
    _instant(observed_at)
    if type(purpose) is not str or purpose not in PURPOSES:
        raise ValueError('REUSE_PURPOSE_UNSUPPORTED')
    if type(priors) is not tuple or len(priors) > MAX_PRIORS:
        raise ValueError('REUSE_EXPLICIT_PRIOR_POPULATION_BOUND')
    result = _insight(candidate)
    _scope(candidate, target)
    candidate_hash = _reference_hash(candidate)
    current_roles = _relations(result)
    rows, seen = [], set()
    for selected in priors:
        old = _check_selection(selected, target, purpose, observed_at)
        prior_hash = selected.permit.reference_sha256
        if prior_hash in seen:
            raise ValueError('REUSE_DUPLICATE_SELECTION')
        seen.add(prior_hash)
        old_roles = _relations(old)
        conflicts = sorted({key[3] for key in current_roles.keys() & old_roles.keys()
                            if len(current_roles[key]) == len(old_roles[key]) == 1
                            and current_roles[key] != old_roles[key]})
        known = candidate.origin is not None and selected.insight.origin is not None
        links = set() if not known else (
            ({candidate_hash} | set(candidate.origin.derived_from_sha256)) &
            ({prior_hash} | set(selected.insight.origin.derived_from_sha256)))
        same_source = result['source_sha256'] == old['source_sha256']
        same_parent = known and candidate.origin == selected.insight.origin
        if not known:
            disposition = 'UNKNOWN_COMPARISON'
        elif prior_hash == candidate_hash:
            disposition = 'EXACT_DUPLICATE'
        elif conflicts:
            disposition = 'DECLARED_REFERENCE_ROLE_CONFLICT'
        elif same_parent or same_source or links:
            disposition = 'RELATED_HYPOTHESIS'
        else:
            disposition = 'NEEDS_TEST'
        rows.append({'reference_sha256': prior_hash, 'disposition': disposition,
            'origin_status': 'SUPPLIED_ORIGINAL_BINDING' if known else 'MISSING_ORIGINAL_ORIGIN',
            'shared_source': same_source, 'shared_derivation_sha256': sorted(links),
            'conflicting_declared_reference_sha256': conflicts,
            'independent_corroboration_established': False,
            'grant_sha256': selected.permit.grant_sha256,
            'audit_sha256': selected.permit.audit_sha256,
            'alternatives': old['alternatives']})
    return {'schema_id': COMPARISON_SCHEMA, 'candidate_reference_sha256': candidate_hash,
            'target': asdict(target), 'purpose': purpose, 'observed_at': observed_at,
            'comparisons': rows, 'candidate_alternatives': result['alternatives'],
            'interpretation_status': 'NOT_ESTABLISHED', 'human_decision': 'PENDING',
            'authority_effect': 'NONE', 'lookup_performed': False,
            'retention_performed': False, 'context_supplied': False, 'dispatch_performed': False}


def validate_reference_receipt(raw, *, insight, operation_id, principal_id,
                               retention_grant_sha256, retention_audit_sha256):
    """Check a native commit report, never create one or authenticate its issuer.

    The custodian owns the actual SAME-store transaction and replay reconciliation.
    The byte count is the canonical reference metadata payload, not WAL/filesystem
    allocation or physical durability proof. Historical zero-write receipts do not
    satisfy this version. No content persistence, reuse or export grant is implied.
    """
    metadata = reference_metadata(insight)
    if insight.origin is None:
        raise ValueError('REUSE_RECEIPT_ORIGINAL_ORIGIN_REQUIRED')
    _identifier(operation_id)
    _identifier(principal_id)
    _digest(retention_grant_sha256)
    _digest(retention_audit_sha256)
    value = strict_loads(raw, maximum_bytes=MAX_ARTIFACT_BYTES)
    fields = {'schema_id', 'mode', 'operation_id', 'organization_id', 'application_id',
              'principal_id', 'reference_sha256', 'retention_grant_sha256',
              'retention_audit_sha256', 'committed_metadata_bytes', 'content_bytes_written',
              'outcome', 'committed_at', 'training_used', 'federation_used', 'network_used'}
    if type(value) is not dict or set(value) != fields:
        raise ValueError('REUSE_PERSISTENT_REFERENCE_RECEIPT_REQUIRED')
    expected = {'schema_id': RECEIPT_SCHEMA, 'mode': 'CUSTODY_PERSISTENT_REFERENCE',
        'operation_id': operation_id, 'organization_id': insight.origin.organization_id,
        'application_id': insight.origin.application_id, 'principal_id': principal_id,
        'reference_sha256': sha256_bytes(canonical_bytes(metadata)),
        'retention_grant_sha256': retention_grant_sha256,
        'retention_audit_sha256': retention_audit_sha256,
        'committed_metadata_bytes': len(canonical_bytes(metadata)), 'content_bytes_written': 0,
        'outcome': 'COMMITTED', 'committed_at': value['committed_at'],
        'training_used': False, 'federation_used': False, 'network_used': False}
    _instant(value['committed_at'])
    # Canonical equality also distinguishes integer counts from bool/float.
    if raw != canonical_bytes(expected):
        raise ValueError('REUSE_PERSISTENT_REFERENCE_RECEIPT_MISMATCH')
    return value
