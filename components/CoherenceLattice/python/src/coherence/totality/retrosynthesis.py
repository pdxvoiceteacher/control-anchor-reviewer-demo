"""Bounded declared counter-hypotheses; no reconstruction of hidden thoughts."""
from __future__ import annotations
import copy
from .canonical import require_exact_keys, require_identifier, require_sha256, sha256_json
from .errors import ValidationError
from .grounding import validate_grounding_bundle

SCHEMA = 'uvlm.coherence.retrosynthesis-proposal.v1'


def validate_proposal(value, *, grounding_bundle=None):
    require_exact_keys(value, required={'schema_id', 'trigger', 'parent', 'alternatives', 'attribution'})
    if value['schema_id'] != SCHEMA or value['trigger'] not in {'CORRECTION', 'FAILURE', 'INSIGHT'}:
        raise ValidationError('RETROSYNTHESIS_CONTRACT_INVALID')
    require_exact_keys(value['attribution'], required={'actor_id', 'origin'})
    require_identifier(value['attribution']['actor_id'], '$.attribution.actor_id')
    if value['attribution']['origin'] not in {'USER_DECLARED', 'SCRIPTED'}:
        raise ValidationError('RETROSYNTHESIS_ATTRIBUTION_MUST_NOT_INVENT_MODEL_OR_HUMAN_AUTHORITY')
    parent = value['parent']
    require_exact_keys(parent, required={'record_id', 'request_sha256', 'response_sha256', 'decision_sha256'})
    require_identifier(parent['record_id'], '$.parent.record_id')
    for name in ('request_sha256', 'response_sha256', 'decision_sha256'):
        require_sha256(parent[name], '$.parent.'+name)
    alternatives = value['alternatives']
    if type(alternatives) is not list or not 2 <= len(alternatives) <= 4:
        raise ValidationError('RETROSYNTHESIS_COMPETING_ALTERNATIVES_REQUIRED')
    seen = set()
    segments = None if grounding_bundle is None else {
        s['segment_id']: s for s in validate_grounding_bundle(grounding_bundle)['segments']}
    for row in alternatives:
        require_exact_keys(row, required={'id', 'explanation', 'references', 'observable_test', 'falsification'})
        identifier = require_identifier(row['id'], '$.alternative.id')
        if identifier in seen:raise ValidationError('RETROSYNTHESIS_DUPLICATE_ALTERNATIVE')
        seen.add(identifier)
        for name in ('explanation', 'observable_test', 'falsification'):
            if type(row[name]) is not str or not 1 <= len(row[name].strip()) <= 2048:
                raise ValidationError('RETROSYNTHESIS_BOUNDED_DECLARATION_REQUIRED')
        if type(row['references']) is not list or len(row['references']) > 16:
            raise ValidationError('RETROSYNTHESIS_REFERENCE_POPULATION_INVALID')
        refs = set()
        for ref in row['references']:
            require_exact_keys(ref, required={'segment_id', 'segment_sha256', 'relation'})
            require_identifier(ref['segment_id'], '$.reference.segment_id')
            require_sha256(ref['segment_sha256'], '$.reference.segment_sha256')
            if ref['segment_id'] in refs or ref['relation'] not in {'PROPOSED_SUPPORT', 'PROPOSED_COUNTEREVIDENCE'}:
                raise ValidationError('RETROSYNTHESIS_REFERENCE_DUPLICATE_OR_RELATION_INVALID')
            refs.add(ref['segment_id'])
            if segments is not None and (ref['segment_id'] not in segments or ref['segment_sha256'] != segments[ref['segment_id']]['sha256']):
                raise ValidationError('RETROSYNTHESIS_SOURCE_REFERENCE_MISMATCH')
    return copy.deepcopy(value)


def evaluate_proposal(value, *, grounding_bundle):
    proposal = validate_proposal(value, grounding_bundle=grounding_bundle)
    bundle = validate_grounding_bundle(grounding_bundle)
    segments = {s['segment_id']: s for s in bundle['segments']}
    rows = []
    for alternative in proposal['alternatives']:
        refs = [{**ref, 'exact_source_text': segments[ref['segment_id']]['text']} for ref in alternative['references']]
        rows.append({**alternative, 'references': refs,
            'reference_status': 'BOUND' if refs else 'NO_SUPPLIED_EVIDENCE',
            'interpretation_status': 'NOT_ESTABLISHED', 'observable_test_executed': False})
    return {'schema_id': 'uvlm.coherence.retrosynthesis-result.v1',
        'proposal_sha256': sha256_json(proposal), 'source_sha256': bundle['manifest']['source_sha256'],
        'parent': proposal['parent'], 'attribution': proposal['attribution'],
        'alternatives': rows, 'selection': None, 'human_decision': 'PENDING',
        'hidden_thought_recovery_claimed': False, 'authority_effect': 'NONE',
        'automatic_dispatch': False, 'prior_write': False,
        'scope': 'New declared competing explanations over exact current source references; not recovered actual cognition.'}
