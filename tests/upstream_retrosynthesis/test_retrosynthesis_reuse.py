"""Pure semantic contract tests; no authenticated persistence or dispatch proof.

The permits/commit reports are explicitly synthetic native-boundary inputs.
Actual Coherence reconstruction and canonical readers are not substituted.
"""
from dataclasses import replace
from copy import deepcopy

import pytest
from coherence.totality.grounding import build_grounding_bundle
from triadicbrain.assurance.canonical import canonical_bytes, sha256_bytes, strict_loads
from triadicbrain.assurance import retrosynthesis_reuse as reuse

NOW = '2026-11-02T00:02:00Z'
BEFORE = '2026-11-02T00:01:00Z'
END = '2026-11-02T00:03:00Z'
TARGET = reuse.TargetBinding('ORG', 'APP', 'READER', 'TASK-B', 'b'*64, 'c'*64, 'LAB')


def insight(*, record='TASK-A', source=b'Sampling failed.\n\nCalibration is unknown.\n'):
    grounding = build_grounding_bundle(source)
    origin = reuse.OriginBinding('ORG', 'APP', record, 'a'*64, 'd'*64, 'e'*64,
                                'f'*64, '1'*40)
    proposal = {'schema_id': 'uvlm.coherence.retrosynthesis-proposal.v1',
        'trigger': 'FAILURE', 'parent': {'record_id': record, 'request_sha256': 'a'*64,
            'response_sha256': 'd'*64, 'decision_sha256': 'e'*64},
        'attribution': {'actor_id': 'FIXTURE', 'origin': 'SCRIPTED'}, 'alternatives': []}
    for index, segment in enumerate(grounding['segments']):
        proposal['alternatives'].append({'id': 'H'+str(index),
            'explanation': ('Sampling error', 'Calibration error')[index],
            'references': [{'segment_id': segment['segment_id'],
                'segment_sha256': segment['sha256'], 'relation': 'PROPOSED_SUPPORT'}],
            'observable_test': 'Compare an independent retained measurement.',
            'falsification': 'A retained independent measurement contradicts the hypothesis.'})
    projection = {key: grounding[key] for key in ('manifest', 'normalized_source', 'segments')}
    return reuse.InsightInput(canonical_bytes(proposal), source, canonical_bytes(projection), 'LAB', origin)


def changed_proposal(value, change):
    proposal = strict_loads(value.proposal)
    change(proposal)
    return replace(value, proposal=canonical_bytes(proposal))


def selected(value, *, purpose='COMPARE', target=TARGET):
    # This fixture supplies an authorized-native snapshot; it is not a login,
    # credential verifier, custody grant, Sophia PASS or persistence operation.
    permit = reuse.ReusePermit(sha256_bytes(canonical_bytes(reuse.reference_metadata(value))),
        target, purpose, '2'*64, '3'*64, BEFORE, END, NOW, 'CURRENT')
    return reuse.PriorSelection(value, permit, purpose)


def compare(candidate, priors, **changes):
    args = dict(target=TARGET, purpose='COMPARE', observed_at=NOW, enabled=True)
    args.update(changes)
    return reuse.compare_supplied_priors(candidate, tuple(priors), **args)


def test_distinct_dispositions_keep_originals_counterevidence_and_unperformed_tests():
    original = insight()
    related = changed_proposal(original, lambda p: p['alternatives'][0].update(
        explanation='Another sampling explanation'))
    conflict = changed_proposal(original, lambda p: p['alternatives'][0]['references'][0].update(
        relation='PROPOSED_COUNTEREVIDENCE'))
    unknown = replace(original, origin=None)
    other = insight(record='TASK-X', source=b'A different result.\n\nA different instrument.\n')
    priors = tuple(selected(value) for value in (original, related, conflict, unknown, other))
    before = deepcopy((original, priors))
    result = compare(original, priors)
    assert [row['disposition'] for row in result['comparisons']] == [
        'EXACT_DUPLICATE', 'RELATED_HYPOTHESIS', 'DECLARED_REFERENCE_ROLE_CONFLICT',
        'UNKNOWN_COMPARISON', 'NEEDS_TEST']
    assert result['comparisons'][2]['alternatives'][0]['references'][0]['relation'] == 'PROPOSED_COUNTEREVIDENCE'
    assert all(not row['independent_corroboration_established'] for row in result['comparisons'])
    assert result['human_decision'] == 'PENDING' and result['interpretation_status'] == 'NOT_ESTABLISHED'
    assert all(row['interpretation_status'] == 'NOT_ESTABLISHED' and not row['observable_test_executed']
               and row['falsification'] for row in result['candidate_alternatives'])
    for name in ('lookup_performed', 'retention_performed', 'context_supplied', 'dispatch_performed'):
        assert result[name] is False
    assert (original, priors) == before


def test_ambiguous_declared_roles_are_preserved_and_alternative_order_is_not_a_conflict():
    original = insight()
    proposal = strict_loads(original.proposal)
    conflicting = deepcopy(proposal['alternatives'][0])
    conflicting['id'] = 'H2'
    conflicting['references'][0]['relation'] = 'PROPOSED_COUNTEREVIDENCE'
    proposal['alternatives'].append(conflicting)
    ambiguous = replace(original, proposal=canonical_bytes(proposal))
    proposal['alternatives'].reverse()
    reordered = replace(original, proposal=canonical_bytes(proposal))
    row = compare(ambiguous, [selected(reordered)])['comparisons'][0]
    assert row['conflicting_declared_reference_sha256'] == []
    assert row['disposition'] == 'RELATED_HYPOTHESIS'
    assert len(row['alternatives']) == 3


def test_actual_sophia_recounts_the_declared_projection_without_inventing_truth():
    request, admission, contents, expected = sophia_inputs()
    from sophia.triadic.governed_evaluation import _check_reconstruction
    result = _check_reconstruction(request, admission, contents)
    assert result == expected
    assert result['selection'] is None and result['prior_write'] is False
    assert all(row['interpretation_status'] == 'NOT_ESTABLISHED'
               and row['observable_test_executed'] is False for row in result['alternatives'])


def sophia_inputs():
    from coherence.totality.retrosynthesis import evaluate_proposal
    original = insight()
    proposal = strict_loads(original.proposal)
    grounding = {**strict_loads(original.grounding), 'source_bytes': original.source_bytes}
    expected = evaluate_proposal(proposal, grounding_bundle=grounding)
    request = {'governance': {'analysis': {'retrosynthesis': proposal}},
               'repair': {'parent_id': 'TASK-A', 'parent_binding': deepcopy(proposal['parent'])}}
    admission = {'native_request': {'meta': {'retrosynthesis': deepcopy(expected)}},
                 'normalized_source_sha256': grounding['manifest']['source_sha256']}
    contents = {'native/grounding/segments.jsonl': b''.join(
        canonical_bytes(segment) for segment in grounding['segments'])}
    return request, admission, contents, expected


@pytest.mark.parametrize('mutation', ['response', 'decision', 'projection', 'source'])
def test_actual_sophia_rejects_substituted_parent_projection_or_retained_source(mutation):
    from sophia.triadic.governed_evaluation import _check_reconstruction
    request, admission, contents, _ = sophia_inputs()
    if mutation in {'response', 'decision'}:
        request['repair']['parent_binding'][mutation+'_sha256'] = '0'*64
    elif mutation == 'projection':
        admission['native_request']['meta']['retrosynthesis']['alternatives'][0]['observable_test_executed'] = True
    else:
        contents['native/grounding/segments.jsonl'] = contents['native/grounding/segments.jsonl'].replace(
            b'Sampling failed.', b'Sampling passed.')
    with pytest.raises(ValueError):
        _check_reconstruction(request, admission, contents)


def test_query_provenance_never_fills_missing_original_or_grants_support():
    original = insight()
    missing = replace(original, origin=None)
    before = reuse.reference_metadata(missing)
    result = compare(original, [selected(missing)])
    assert result['target']['request_sha256'] == 'b'*64
    assert result['comparisons'][0]['origin_status'] == 'MISSING_ORIGINAL_ORIGIN'
    assert result['comparisons'][0]['disposition'] == 'UNKNOWN_COMPARISON'
    assert reuse.reference_metadata(missing) == before and before['origin'] is None


@pytest.mark.parametrize('mode,purpose', [
    ('shadow_only', 'COMPARE'), ('background_only', 'COMPARE'),
    ('background_only', 'CONTEXT_HYPOTHESIS'), ('context_only', 'COMPARE'),
    ('context_only', 'CONTEXT_HYPOTHESIS')])
@pytest.mark.parametrize('vocabulary', ['LEGACY_ROUTER_V1', 'LEGACY_AUDITOR_V1'])
def test_supported_legacy_modes_have_explicit_narrow_purposes(mode, purpose, vocabulary):
    assert reuse.reconcile_mode(mode, vocabulary=vocabulary, purpose=purpose) == purpose


@pytest.mark.parametrize('mode', ['ignore', 'answer_support', 'novelty_extension',
                                 'cite_if_verified', 'UNKNOWN'])
@pytest.mark.parametrize('vocabulary', ['LEGACY_ROUTER_V1', 'LEGACY_AUDITOR_V1'])
def test_stronger_ignored_and_unknown_modes_never_default_compliant(mode, vocabulary):
    with pytest.raises(ValueError, match='MODE_NOT_PERMITTED'):
        reuse.reconcile_mode(mode, vocabulary=vocabulary, purpose='COMPARE')


def test_compare_permission_cannot_become_context_or_training_permission():
    original = insight()
    with pytest.raises(ValueError, match='MODE_NOT_PERMITTED'):
        reuse.reconcile_mode('shadow_only', vocabulary='LEGACY_ROUTER_V1', purpose='CONTEXT_HYPOTHESIS')
    with pytest.raises(ValueError, match='PURPOSE_UNSUPPORTED'):
        compare(original, [selected(original)], purpose='TRAIN')
    with pytest.raises(ValueError, match='MODE_VOCABULARY_UNSUPPORTED'):
        reuse.reconcile_mode('COMPARE', vocabulary='UNKNOWN', purpose='COMPARE')
    result = compare(original, [selected(original, purpose='CONTEXT_HYPOTHESIS')], purpose='CONTEXT_HYPOTHESIS')
    assert result['context_supplied'] is False and result['authority_effect'] == 'NONE'


@pytest.mark.parametrize('change', ['organization', 'application', 'principal', 'task', 'request',
    'profile', 'scope', 'purpose', 'expired', 'revoked', 'unknown', 'stale', 'not-yet-valid'])
def test_changed_or_absent_current_reuse_authority_is_rejected(change):
    original = insight()
    selection = selected(original)
    fields = {'organization': 'organization_id', 'application': 'application_id',
        'principal': 'principal_id', 'task': 'task_id', 'request': 'request_sha256',
        'profile': 'profile_sha256', 'scope': 'scope_id'}
    permit = selection.permit
    if change in fields:
        name = fields[change]
        permit = replace(permit, target=replace(TARGET, **{name: '0'*64 if name.endswith('sha256') else 'OTHER'}))
    elif change == 'purpose': permit = replace(permit, purpose='RETAIN')
    elif change == 'expired': permit = replace(permit, expires_at=NOW)
    elif change == 'revoked': permit = replace(permit, status='REVOKED')
    elif change == 'unknown': permit = replace(permit, status='UNKNOWN')
    elif change == 'stale': permit = replace(permit, observed_at=BEFORE)
    elif change == 'not-yet-valid': permit = replace(permit, valid_from=END)
    with pytest.raises(ValueError, match='CURRENT_TARGET_PURPOSE_AUTHORITY'):
        compare(original, [replace(selection, permit=permit)])


def test_correction_cannot_follow_old_grant_and_ancestry_is_not_corroboration():
    original = insight()
    old_selection = selected(original)
    corrected = changed_proposal(original, lambda p: p['alternatives'][0].update(explanation='Corrected hypothesis'))
    with pytest.raises(ValueError, match='REFERENCE_SUBSTITUTION'):
        compare(corrected, [replace(old_selection, insight=corrected)])
    ref = old_selection.permit.reference_sha256
    successor = replace(corrected, origin=replace(corrected.origin, derived_from_sha256=(ref,)))
    row = compare(successor, [old_selection])['comparisons'][0]
    assert row['shared_derivation_sha256'] == [ref]
    assert row['disposition'] == 'RELATED_HYPOTHESIS'
    assert row['independent_corroboration_established'] is False


@pytest.mark.parametrize('name', ['record_id', 'request_sha256', 'response_sha256', 'decision_sha256'])
def test_actual_reconstruction_cannot_replace_original_parent(name):
    original = insight()
    changed = replace(original, origin=replace(original.origin, **{name: 'OTHER' if name == 'record_id' else '0'*64}))
    with pytest.raises(ValueError, match='ORIGINAL_PARENT_MISMATCH'):
        compare(changed, [])


def test_actual_source_reference_recount_rejects_tampering():
    original = insight()
    changed = changed_proposal(original, lambda p: p['alternatives'][0]['references'][0].update(segment_sha256='0'*64))
    with pytest.raises(ValueError, match='SOURCE_REFERENCE_MISMATCH'):
        compare(changed, [])


def test_source_stays_exact_bytes_and_cannot_follow_an_earlier_reference_grant():
    original = insight(source=b'Sampling failed.\r\n\r\nCalibration is unknown.\r\n')
    selection = selected(original)
    # Same normalized text is not identity of the retained original source bytes.
    changed = insight(source=original.source_bytes.replace(b'\r\n', b'\n'))
    assert reuse.reference_metadata(original)['source_sha256'] == sha256_bytes(original.source_bytes)
    assert reuse.reference_metadata(changed)['source_sha256'] != reuse.reference_metadata(original)['source_sha256']
    with pytest.raises(ValueError, match='REFERENCE_SUBSTITUTION'):
        compare(original, [replace(selection, insight=changed)])
    with pytest.raises(ValueError, match='EXACT_SOURCE_BYTES_BOUND'):
        compare(replace(original, source_bytes=original.source_bytes.decode()), [])
    with pytest.raises(ValueError, match='EXACT_SOURCE_BYTES_BOUND'):
        compare(replace(original, source_bytes=b'x' * (reuse.MAX_ARTIFACT_BYTES + 1)), [])


@pytest.mark.parametrize('mutation', ['source-bytes', 'manifest', 'segment', 'projection-fields'])
def test_actual_retained_grounding_consumer_rejects_substitution(mutation):
    original = insight()
    projection = strict_loads(original.grounding)
    if mutation == 'source-bytes':
        changed = replace(original, source_bytes=original.source_bytes.replace(b'failed', b'passed'))
    else:
        if mutation == 'manifest': projection['manifest']['source_sha256'] = '0'*64
        elif mutation == 'segment': projection['segments'][0]['text'] = 'Substituted source.'
        else: projection['source_bytes'] = 'Not authenticated original bytes'
        changed = replace(original, grounding=canonical_bytes(projection))
    with pytest.raises(ValueError):
        compare(changed, [])


@pytest.mark.parametrize('field', ['organization_id', 'application_id'])
def test_an_internally_consistent_snapshot_cannot_disclose_a_different_organization(field):
    original = insight()
    other = replace(original, origin=replace(original.origin, **{field: 'OTHER'}))
    with pytest.raises(ValueError, match='ORGANIZATION_APPLICATION_MISMATCH'):
        compare(original, [selected(other)])


def test_duplicate_bounded_and_default_off_do_not_start_work():
    original = insight()
    with pytest.raises(ValueError, match='COMPARISON_DISABLED'):
        reuse.compare_supplied_priors(None, None, target=None, purpose=None, observed_at=None)
    with pytest.raises(ValueError, match='DUPLICATE_SELECTION'):
        compare(original, [selected(original), selected(original)])
    with pytest.raises(ValueError, match='POPULATION_BOUND'):
        compare(original, [selected(original)] * (reuse.MAX_PRIORS + 1))
    with pytest.raises(ValueError, match='OVERSIZE'):
        compare(replace(original, proposal=b' ' * (reuse.MAX_ARTIFACT_BYTES + 1)), [])
    assert compare(original, [])['comparisons'] == []


def commit_report(value):
    """Synthetic custody output only; it performs no transaction or write."""
    metadata = canonical_bytes(reuse.reference_metadata(value))
    return {'schema_id': reuse.RECEIPT_SCHEMA, 'mode': 'CUSTODY_PERSISTENT_REFERENCE',
        'operation_id': 'RETAIN-1', 'organization_id': 'ORG', 'application_id': 'APP',
        'principal_id': 'CUSTODIAN', 'reference_sha256': sha256_bytes(metadata),
        'retention_grant_sha256': '4'*64, 'retention_audit_sha256': '5'*64,
        'committed_metadata_bytes': len(metadata), 'content_bytes_written': 0,
        'outcome': 'COMMITTED', 'committed_at': NOW,
        'training_used': False, 'federation_used': False, 'network_used': False}


def validate_report(report, value):
    return reuse.validate_reference_receipt(canonical_bytes(report), insight=value,
        operation_id='RETAIN-1', principal_id='CUSTODIAN',
        retention_grant_sha256='4'*64, retention_audit_sha256='5'*64)


def test_versioned_reference_receipt_preserves_original_and_claims_only_metadata():
    original = insight()
    report = commit_report(original)
    before = deepcopy(report)
    assert validate_report(report, original) == before
    assert report == before and report['content_bytes_written'] == 0
    assert report['committed_metadata_bytes'] > 0
    assert report['schema_id'] != 'uvlm.pmr.totality.receipt.v1'
    # Revalidating reports is pure; no operation is submitted or repeated here.
    assert validate_report(report, original) == before


@pytest.mark.parametrize('field,value', [
    ('schema_id', 'uvlm.pmr.totality.receipt.v1'), ('mode', 'NO_WRITE_REFERENCE_IMPLEMENTATION'),
    ('operation_id', 'OTHER'), ('organization_id', 'OTHER'), ('application_id', 'OTHER'),
    ('principal_id', 'OTHER'), ('reference_sha256', '0'*64),
    ('retention_grant_sha256', '0'*64), ('retention_audit_sha256', '0'*64),
    ('committed_metadata_bytes', 0), ('content_bytes_written', True),
    ('outcome', 'UNKNOWN'), ('training_used', True), ('federation_used', True), ('network_used', True)])
def test_unbound_uncertain_or_old_no_write_report_cannot_be_a_durable_reference(field, value):
    original = insight()
    report = commit_report(original)
    report[field] = value
    with pytest.raises(ValueError, match='PERSISTENT_REFERENCE_RECEIPT_MISMATCH'):
        validate_report(report, original)


def test_literal_historical_receipt_and_missing_origin_remain_separate_contracts():
    from coherence.totality.pmr import no_write_receipt
    original = insight()
    historical = no_write_receipt(run_id='R1', candidate_id='K1', logical_time=NOW, reason='DISABLED')
    before = deepcopy(historical)
    with pytest.raises(ValueError, match='PERSISTENT_REFERENCE_RECEIPT_REQUIRED'):
        validate_report(historical, original)
    assert historical == before and historical['persistent_bytes_written'] == 0
    with pytest.raises(ValueError, match='RECEIPT_ORIGINAL_ORIGIN_REQUIRED'):
        validate_report(commit_report(original), replace(original, origin=None))
