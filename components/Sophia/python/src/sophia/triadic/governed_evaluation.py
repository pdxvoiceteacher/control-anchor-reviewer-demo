"""Read-only evaluation of the Linux bridge's versioned derived input contract.

No provider, custody implementation, source rewrite, policy activation or human
decision is available here. Raw provider bodies and credentials are not inputs.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import unicodedata
from .totality_audit import audit_totality_run, _canonical_json_bytes, _parse_json, _parse_jsonl, INPUT_PATHS, OPTIONAL_INPUT_PATHS

SCHEMA='control-anchor.sophia-governed-evaluation.v1'
MAX_BYTES=32*1024*1024


def digest(raw):return hashlib.sha256(raw).hexdigest()


def read_member(root, name):
    part=PurePosixPath(name)
    if not name or part.is_absolute() or part.as_posix()!=name or any(p in ('','.','..') or ':' in p or '\\' in p for p in part.parts):
        raise ValueError('SOPHIA_INPUT_PATH_UNSAFE')
    path=root.joinpath(*part.parts)
    if any(p.is_symlink() for p in (path,*path.parents)):
        raise ValueError('SOPHIA_INPUT_LINK_FORBIDDEN')
    before=path.stat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or before.st_size>MAX_BYTES:
        raise ValueError('SOPHIA_INPUT_FILE_IDENTITY_INVALID')
    raw=path.read_bytes();after=path.stat()
    if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns):
        raise ValueError('SOPHIA_INPUT_CHANGED_DURING_READ')
    return raw


def authenticate_inputs(root, manifest):
    root=Path(root).absolute()
    if type(manifest) is not dict or set(manifest)!={'schema_id','record_id','files'} or manifest['schema_id']!='control-anchor.evaluator-inputs.v1':
        raise ValueError('SOPHIA_INPUT_MANIFEST_INVALID')
    if type(manifest['files']) is not list or not 1<=len(manifest['files'])<=len(INPUT_PATHS)+1:
        raise ValueError('SOPHIA_INPUT_MANIFEST_POPULATION_INVALID')
    names=[];contents={};total=0
    for row in manifest['files']:
        if type(row) is not dict or set(row)!={'path','bytes','sha256'} or type(row['bytes']) is not int:
            raise ValueError('SOPHIA_INPUT_MANIFEST_ROW_INVALID')
        name=row['path'];raw=read_member(root,name);total+=len(raw)
        if name in contents or row['bytes']!=len(raw) or row['sha256']!=digest(raw) or total>MAX_BYTES:
            raise ValueError('SOPHIA_INPUT_MANIFEST_BINDING_INVALID')
        names.append(name);contents[name]=raw
    if names!=sorted(names) or 'governed_context.json' not in contents:
        raise ValueError('SOPHIA_INPUT_ORDER_OR_CONTEXT_INVALID')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    if actual!=set(names):raise ValueError('SOPHIA_INPUT_EXTRA_OR_MISSING_FILE')
    context=_parse_json(contents['governed_context.json'],'governed_context.json')
    fields={'schema_id','record_id','request','admission','provider_state','policy_results','execution_context','native_analysis','analysis_binding'}
    if context.get('schema_id')=='control-anchor.evaluator-context.v2':
        fields|={'observation_profile','observation_assessment','custody_request_sha256','retained_response_sha256'}
    if set(context)!=fields or type(context['native_analysis']) is not bool:
        raise ValueError('SOPHIA_CONTEXT_SHAPE_INVALID')
    if context.get('schema_id') not in {'control-anchor.evaluator-context.v1','control-anchor.evaluator-context.v2'} or context.get('record_id')!=manifest['record_id']:
        raise ValueError('SOPHIA_CONTEXT_IDENTITY_MISMATCH')
    expected={'governed_context.json'}
    if context['native_analysis']:
        expected.update('native/'+name for name in INPUT_PATHS if name not in OPTIONAL_INPUT_PATHS or 'native/'+name in contents)
    if set(names)!=expected:raise ValueError('SOPHIA_INPUT_CONTRACT_MEMBERSHIP_INVALID')
    return context,contents


def _lookup(context,pointer):
    value=context
    if type(pointer) is not str or not pointer.startswith('/'):
        raise ValueError('SOPHIA_POLICY_POINTER_INVALID')
    for part in pointer[1:].split('/'):
        if type(value) is not dict or part not in value:return False,None
        value=value[part]
    return True,value


def _observation_bindings(context, pointers):
    result={}
    for pointer in pointers:
        present,value=_lookup(context,pointer)
        result[pointer]={'present':present,'sha256':digest(_canonical_json_bytes(value)) if present else None}
    return result


def _check_observation(context):
    """Independent input/identity recomputation, not a second semantic verdict.

    Native Sophia still performs its actual candidate audit. This additional
    check never calls the producer's assessor or trusts provider text as policy.
    """
    if context['schema_id']!='control-anchor.evaluator-context.v2':return None
    profile=context['observation_profile'];assessment=context['observation_assessment']
    admission=context['admission'];execution=context['execution_context']
    if (type(profile) is not dict or profile.get('schema_id')!='control-anchor.linux-profile.v4'
            or profile.get('business_control_effect')!='OBSERVE_AND_REPORT_ONLY'
            or digest(_canonical_json_bytes(profile))!=admission.get('observation_profile_sha256')
            or profile.get('ucc_plan')!=admission['ucc_plan']
            or admission.get('business_control_effect')!='OBSERVE_AND_REPORT_ONLY'
            or admission.get('admission_controls')!=[]
            or admission.get('compatibility_plan_execution')!='DEFINITION_ONLY_NOT_EXECUTED'
            or admission.get('custody_request_sha256')!=context['custody_request_sha256']
            or type(assessment) is not dict
            or assessment.get('transaction_id')!=context['record_id']
            or assessment.get('profile_sha256')!=admission['observation_profile_sha256']
            or assessment.get('profile_version')!=profile['version']
            or assessment.get('request_sha256')!=context['custody_request_sha256']
            or assessment.get('response_sha256')!=context['retained_response_sha256']
            or assessment.get('business_control_effect')!='OBSERVE_AND_REPORT_ONLY'):
        raise ValueError('SOPHIA_OBSERVATION_IDENTITY_SUBSTITUTION')
    if context['native_analysis'] and context['analysis_binding']['provider_raw_response_sha256']!=context['retained_response_sha256']:
        raise ValueError('SOPHIA_OBSERVATION_CAPTURE_SUBSTITUTION')
    compatibility_steps=[control['procedure'] for control in profile['controls'] if control['enabled']]
    if not compatibility_steps:
        compatibility_steps=[{'id':'NO-CONTROLS-ACTIVE',
            'title':'No organization controls activated','kind':'advisory',
            'phase':'admission','operation':None,'arguments':{'procedure':
                'No business-control criterion is executed by this empty definition. Retain capture and explicit scope limitations.'}}]
    if (profile['ucc_plan']['plan_id']!=profile['id'] or
            profile['ucc_plan']['version']!=profile['version'] or
            profile['ucc_plan']['steps']!=compatibility_steps or
            context.get('policy_results')!=[]):
        raise ValueError('SOPHIA_OBSERVATION_COMPATIBILITY_EXECUTION_OR_DEFINITION_CHANGED')
    if assessment.get('schema_id')=='control-anchor.observation-assessment-error.v1':
        if assessment.get('status')!='ERROR' or assessment.get('control_results')!=[] or assessment.get('framework_mappings')!=[]:
            raise ValueError('SOPHIA_ASSESSMENT_ERROR_PROMOTED')
        return digest(_canonical_json_bytes(assessment))
    if (assessment.get('schema_id')!='control-anchor.observation-assessment.v1'
            or assessment.get('execution_context_sha256')!=digest(_canonical_json_bytes(execution))
            or assessment.get('actual_external_actions_authorized') is not False
            or assessment.get('model_assessment_calls')!=0):
        raise ValueError('SOPHIA_OBSERVATION_CONTEXT_OR_AUTHORITY_CHANGED')
    actions=assessment['activity_context']['actions'];controls=profile['controls']
    if not 1<=len(actions)<=16 or len(controls)>32:
        raise ValueError('SOPHIA_OBSERVATION_POPULATION_BOUND')
    action_ids={a['id'] for a in actions};control_ids={c['id'] for c in controls}
    if len(action_ids)!=len(actions) or len(control_ids)!=len(controls):
        raise ValueError('SOPHIA_OBSERVATION_DUPLICATE_IDENTITY')
    declarations=execution['evidence'].get('_activity_observation',{}).get('declarations',[])
    if assessment['activity_context']['declarations']!=declarations:
        raise ValueError('SOPHIA_OBSERVATION_DECLARATION_CHANGED')
    by_action={a['id']:a for a in actions};by_control={c['id']:c for c in controls}
    supplied_actions=execution['evidence'].get('_activity_observation',{}).get('actions')
    if supplied_actions is not None:
        supplied={a['id']:a for a in supplied_actions}
        if len(supplied)!=len(supplied_actions) or set(supplied)!=action_ids:
            raise ValueError('SOPHIA_OBSERVATION_ACTION_POPULATION_CHANGED')
        for identifier,action in by_action.items():
            original=supplied[identifier]
            if any(action[key]!=original[key] for key in ('span','context_basis','context_evidence_paths')) or action['declared_context']!=original['context'] or action['declared_stage']!=original['stage']:
                raise ValueError('SOPHIA_OBSERVATION_ACTION_INPUT_CHANGED')
    else:
        expected_actions={'CAPTURED-REQUESTED'}|({'CAPTURED-DRAFTED'} if execution.get('response') else set())
        if action_ids!=expected_actions:raise ValueError('SOPHIA_OBSERVATION_DEFAULT_ACTION_POPULATION_CHANGED')
    for action in actions:
        span=action['span'];text=execution.get(span['field'])
        marker=execution['evidence'].get('_activity_observation',{}).get('schema_id')
        allowed_fields={'source','response'} | ({'prompt'} if marker in {None,'control-anchor.activity-observation.v2'} else set())
        if span['field'] not in allowed_fields:
            raise ValueError('SOPHIA_OBSERVATION_SPAN_VERSION_CHANGED')
        representation='CAPTURED_TEXT'
        if span['field']=='source' and type(text) is dict:
            text=_canonical_json_bytes(text).decode('utf-8');representation='CANONICAL_JSON_SOURCE_NOT_ORIGINAL_BYTES'
        if (type(text) is not str or type(span['start']) is not int or type(span['end']) is not int
                or not 0<=span['start']<span['end']<=len(text)
                or action.get('span_units')!='UNICODE_CODEPOINTS' or action.get('span_representation')!=representation
                or digest(text[span['start']:span['end']].encode())!=action['span_sha256']
                or action['stage']=='TOOL_OBSERVED'):
            raise ValueError('SOPHIA_OBSERVATION_SPAN_OR_EXTERNAL_ACTION_SUBSTITUTION')
        evidence=action['context_evidence_paths'];supported=action['context_basis']=='SOURCE_BOUND_CORROBORATION' and bool(evidence)
        records=[]
        for pointer in evidence:
            present,value=_lookup(execution,pointer)
            if (not present or type(value) is not dict or set(value)!={'context','source_id','source_version','reason'}
                    or value['context']!=action['declared_context']):supported=False;continue
            records.append({'pointer':pointer,'sha256':digest(_canonical_json_bytes(value))})
        contrary=any(d['label'] in {'WORK','PERSONAL_NONWORK'} and d['label']!=action['declared_context'] for d in declarations)
        expected=action['declared_context'] if supported and not contrary else 'UNDETERMINED'
        if action['context']!=expected or action['context_provenance']['evidence']!=records:
            raise ValueError('SOPHIA_OBSERVATION_CONTEXT_PROVENANCE_CHANGED')
        expected_stage=('USER_REPORTED' if action['declared_stage']=='TOOL_OBSERVED' or
            action['declared_stage']=='DRAFTED' and span['field']!='response' or
            action['declared_stage']=='REQUESTED' and span['field'] not in {'source','prompt'} else action['declared_stage'])
        if action['stage']!=expected_stage:raise ValueError('SOPHIA_OBSERVATION_REPORTED_ACTION_PROMOTED')
        expected_provenance={'kind':'RETAINED_SOURCE_ASSERTION' if supported else 'INSUFFICIENT_CONTEXT_EVIDENCE',
            'evidence':records,'source_truth':'NOT_ESTABLISHED','employment_intent':'NOT_INDEPENDENTLY_ESTABLISHED',
            'contradictory_declaration':contrary}
        if action['context_provenance']!=expected_provenance:
            raise ValueError('SOPHIA_OBSERVATION_PROVENANCE_AUTHORITY_CHANGED')
    labels={a['context'] for a in actions}
    expected_label='UNDETERMINED' if 'UNDETERMINED' in labels else 'MIXED' if len(labels)>1 else next(iter(labels))
    if assessment['activity_context']['label']!=expected_label:
        raise ValueError('SOPHIA_OBSERVATION_CONTEXT_SUMMARY_CHANGED')
    pairs=set();applied=[]
    for row in assessment['control_results']:
        pair=(row['action_id'],row['control_id'])
        if pair in pairs or pair[0] not in by_action or pair[1] not in by_control:
            raise ValueError('SOPHIA_OBSERVATION_RESULT_IDENTITY_CHANGED')
        pairs.add(pair);control=by_control[pair[1]];action=by_action[pair[0]]
        if (row['control_version']!=control['version'] or row['title']!=control['title']
                or row['action_span']!=action['span'] or row['action_span_sha256']!=action['span_sha256']
                or row['authority_effect']!='NONE' or row['units']!=control['units']
                or row['review_criteria']!=control['review_criteria']
                or row['required_evidence_bindings']!=_observation_bindings(execution,control['evidence_requirements'])):
            raise ValueError('SOPHIA_OBSERVATION_CONTROL_OR_EVIDENCE_SUBSTITUTION')
        units={};unit_source=execution['evidence'].get('_observed_units',{})
        for pointer,expected_unit in control['units'].items():
            value=unit_source.get(pointer) if type(unit_source) is dict else None
            valid=(type(value) is dict and set(value)=={'unit','source_id','source_version'}
                and all(type(value[k]) is str and value[k].strip() and len(value[k])<=128 for k in value))
            units[pointer]={'expected_unit':expected_unit,'observed_unit':value['unit'] if valid else None,
                'sha256':digest(_canonical_json_bytes(value)) if valid else None,
                'state':'EXACT_DECLARED_UNIT_MATCH' if valid and value['unit']==expected_unit else 'REVIEW_REQUIRED',
                'source_truth':'NOT_ESTABLISHED'}
        if row.get('unit_bindings')!=units or (row['result'] in {'COMPLIES','EXCEPTION'} and
                any(v['state']!='EXACT_DECLARED_UNIT_MATCH' for v in units.values())):
            raise ValueError('SOPHIA_OBSERVATION_UNITS_SUBSTITUTION')
        if row['applicability'] not in {'APPLICABLE','NOT_APPLICABLE','UNKNOWN'} or row['result'] not in {None,'COMPLIES','EXCEPTION','REVIEW_REQUIRED'}:
            raise ValueError('SOPHIA_OBSERVATION_RESULT_INVALID')
        scope=control['applicability'];predicates=row['applicability_procedures']
        evaluate_predicates=(control['enabled'] and action['context']!='UNDETERMINED' and
            action['context'] in scope['contexts'] and action['stage'] in scope['action_stages'])
        if not evaluate_predicates and predicates:raise ValueError('SOPHIA_UNEXECUTED_PREDICATE_PROMOTED')
        if not control['enabled']:expected_applicability='NOT_APPLICABLE'
        elif action['context']=='UNDETERMINED':expected_applicability='UNKNOWN'
        elif action['context'] not in scope['contexts']:expected_applicability='NOT_APPLICABLE'
        elif action['stage'] not in scope['action_stages']:
            expected_applicability='UNKNOWN' if action['stage']=='USER_REPORTED' and 'TOOL_OBSERVED' in scope['action_stages'] else 'NOT_APPLICABLE'
        else:
            if len(predicates)!=len(scope['predicates']):raise ValueError('SOPHIA_OBSERVATION_PREDICATE_POPULATION_CHANGED')
            for predicate,step in zip(predicates,scope['predicates']):
                args=step['arguments'];pointers=[args[k] for k in ('path','left','right','earlier','later') if k in args]
                if step['operation']=='compare_total':pointers.extend(args['terms'])
                plan={'schema_id':'control-anchor.ucc-plan.v1','plan_id':'OBSERVATION-PROCEDURE','version':1,'steps':[step]}
                if (predicate['control_id']!=step['id'] or predicate['input_bindings']!=_observation_bindings(execution,pointers)
                        or any(predicate[k]!=step[k] for k in ('phase','operation','kind'))
                        or predicate['plan_sha256']!=digest(_canonical_json_bytes(plan)) or predicate['plan_version']!=1
                        or predicate['result'] not in {'PASS','FAIL','HOLD','NOT_EXECUTED'}):
                    raise ValueError('SOPHIA_OBSERVATION_PREDICATE_BINDING_CHANGED')
            if any(p['result']=='HOLD' or p['observation'] not in {'DETERMINISTIC_CHECK_SATISFIED','DETERMINISTIC_CHECK_NOT_SATISFIED'} for p in predicates):expected_applicability='UNKNOWN'
            elif any(p['result']=='FAIL' for p in predicates):expected_applicability='NOT_APPLICABLE'
            else:expected_applicability='APPLICABLE'
        if row['applicability']!=expected_applicability:
            raise ValueError('SOPHIA_OBSERVATION_APPLICABILITY_CHANGED')
        if row['applicability']=='NOT_APPLICABLE' and (row['result'] is not None or row['mappings'] or row['procedure_result'] is not None):
            raise ValueError('SOPHIA_INAPPLICABLE_CONTROL_PROMOTED')
        if row['applicability']=='UNKNOWN' and (row['result']!='REVIEW_REQUIRED' or row['mappings']):
            raise ValueError('SOPHIA_UNKNOWN_CONTROL_PROMOTED')
        result=row['procedure_result'];step=control['procedure']
        if result is not None:
            plan={'schema_id':'control-anchor.ucc-plan.v1','plan_id':'OBSERVATION-PROCEDURE','version':1,'steps':[step]}
            if (any(result[k]!=step[k] for k in ('kind','phase','operation')) or result['control_id']!=control['id']
                    or result['plan_sha256']!=digest(_canonical_json_bytes(plan)) or result['plan_version']!=1):
                raise ValueError('SOPHIA_OBSERVATION_PROCEDURE_SUBSTITUTION')
            args=step['arguments'];pointers=[args[k] for k in ('path','left','right','earlier','later') if k in args]
            if step['operation']=='compare_total':pointers.extend(args['terms'])
            if result['input_bindings']!=_observation_bindings(execution,pointers):
                raise ValueError('SOPHIA_OBSERVATION_PROCEDURE_INPUT_SUBSTITUTION')
            if row['result']=='COMPLIES' and (result['result']!='PASS' or step['kind']!='executable'):
                raise ValueError('SOPHIA_OBSERVATION_UNPERFORMED_CHECK_PROMOTED')
            if row['result']=='EXCEPTION' and (result['result']!='FAIL' or result['observation']!='DETERMINISTIC_CHECK_NOT_SATISFIED'):
                raise ValueError('SOPHIA_OBSERVATION_UNKNOWN_PROMOTED_EXCEPTION')
        elif row['result'] in {'COMPLIES','EXCEPTION'}:
            raise ValueError('SOPHIA_OBSERVATION_CONCLUSION_WITHOUT_PROCEDURE')
        for mapping, expected in zip(row['mappings'], control['mappings']):
            for key,value in expected.items():
                if mapping.get(key)!=value:raise ValueError('SOPHIA_OBSERVATION_MAPPING_CHANGED')
            expected_evidence=_observation_bindings(execution,expected['evidence_paths'])
            expected_state='BOUND_ORGANIZATION_MAPPING' if all(v['present'] for v in expected_evidence.values()) else 'UNKNOWN_MISSING_MAPPING_EVIDENCE'
            if (mapping['evidence_bindings']!=expected_evidence or mapping['state']!=expected_state
                    or mapping['control_id']!=control['id'] or mapping['control_version']!=control['version']
                    or mapping['action_id']!=action['id'] or mapping['not_a_compliance_result'] is not True):
                raise ValueError('SOPHIA_OBSERVATION_MAPPING_EVIDENCE_CHANGED')
            if mapping['state']=='BOUND_ORGANIZATION_MAPPING':applied.append(mapping)
        if row['applicability']=='APPLICABLE' and len(row['mappings'])!=len(control['mappings']):
            raise ValueError('SOPHIA_OBSERVATION_MAPPING_POPULATION_CHANGED')
    if pairs!={(a,c) for a in action_ids for c in control_ids} or assessment['framework_mappings']!=applied:
        raise ValueError('SOPHIA_OBSERVATION_POPULATION_INCOMPLETE')
    return digest(_canonical_json_bytes(assessment))


def _check_reconstruction(request, admission, contents):
    """Recompute source-reference projection independently of its producer."""
    options=request['governance'].get('analysis') or {}
    proposal=options.get('retrosynthesis')
    actual=admission['native_request']['meta'].get('retrosynthesis')
    if proposal is None:
        if actual is not None:raise ValueError('SOPHIA_UNREQUESTED_RECONSTRUCTION')
        return None
    if (type(proposal) is not dict or set(proposal)!={'schema_id','trigger','parent','alternatives','attribution'}
            or proposal['schema_id']!='uvlm.coherence.retrosynthesis-proposal.v1'
            or proposal['trigger'] not in {'CORRECTION','FAILURE','INSIGHT'}
            or type(proposal['parent']) is not dict
            or set(proposal['parent'])!={'record_id','request_sha256','response_sha256','decision_sha256'}
            or request.get('repair',{}).get('parent_binding')!=proposal['parent']
            or request.get('repair',{}).get('parent_id')!=proposal['parent']['record_id']
            or type(proposal['attribution']) is not dict or set(proposal['attribution'])!={'origin','actor_id'}
            or type(proposal['attribution']['actor_id']) is not str or not proposal['attribution']['actor_id'].strip()
            or proposal['attribution']['origin'] not in {'USER_DECLARED','SCRIPTED'}
            or type(proposal['alternatives']) is not list or not 2<=len(proposal['alternatives'])<=4):
        raise ValueError('SOPHIA_RECONSTRUCTION_PARENT_OR_CONTRACT_INVALID')
    segments=_parse_jsonl(contents['native/grounding/segments.jsonl'],'grounding segments')
    by_id={s['segment_id']:s for s in segments};seen=set();rows=[]
    for row in proposal['alternatives']:
        if (type(row) is not dict or set(row)!={'id','explanation','references','observable_test','falsification'}
                or type(row['id']) is not str or not row['id'] or row['id'] in seen
                or any(type(row[k]) is not str or not 1<=len(row[k].strip())<=2048 for k in ('explanation','observable_test','falsification'))
                or type(row['references']) is not list or len(row['references'])>16):
            raise ValueError('SOPHIA_RECONSTRUCTION_ALTERNATIVE_INVALID')
        seen.add(row['id']);refs=[];ref_ids=set()
        for ref in row['references']:
            if (type(ref) is not dict or set(ref)!={'segment_id','segment_sha256','relation'}
                    or type(ref['segment_id']) is not str or ref['segment_id'] not in by_id or ref['segment_id'] in ref_ids
                    or ref['segment_sha256']!=by_id[ref['segment_id']]['sha256']
                    or ref['relation'] not in {'PROPOSED_SUPPORT','PROPOSED_COUNTEREVIDENCE'}):
                raise ValueError('SOPHIA_RECONSTRUCTION_REFERENCE_SUBSTITUTION')
            ref_ids.add(ref['segment_id'])
            refs.append({**ref,'exact_source_text':by_id[ref['segment_id']]['text']})
        rows.append({**row,'references':refs,'reference_status':'BOUND' if refs else 'NO_SUPPLIED_EVIDENCE',
            'interpretation_status':'NOT_ESTABLISHED','observable_test_executed':False})
    expected={'schema_id':'uvlm.coherence.retrosynthesis-result.v1',
        'proposal_sha256':digest(_canonical_json_bytes(proposal)),
        'source_sha256':admission['normalized_source_sha256'],'parent':proposal['parent'],
        'attribution':proposal['attribution'],'alternatives':rows,'selection':None,
        'human_decision':'PENDING','hidden_thought_recovery_claimed':False,
        'authority_effect':'NONE','automatic_dispatch':False,'prior_write':False,
        'scope':'New declared competing explanations over exact current source references; not recovered actual cognition.'}
    if actual!=expected:raise ValueError('SOPHIA_RECONSTRUCTION_PROJECTION_CHANGED')
    return expected


def evaluate_governed_input(root, manifest, output_directory):
    """Recompute bindings and invoke Sophia's independent native audit when applicable."""
    context,contents=authenticate_inputs(root,manifest)
    request=context['request'];admission=context['admission']
    if digest(_canonical_json_bytes(request))!=admission['request_canonical_sha256']:
        raise ValueError('SOPHIA_GOVERNED_REQUEST_SUBSTITUTION')
    if digest(request['source'].encode())!=admission['original_source_sha256']:
        raise ValueError('SOPHIA_GOVERNED_SOURCE_SUBSTITUTION')
    if digest(_canonical_json_bytes(admission['ucc_plan']))!=admission['ucc_plan_sha256']:
        raise ValueError('SOPHIA_GOVERNED_POLICY_SUBSTITUTION')
    if digest(_canonical_json_bytes(admission['native_request']))!=admission['native_request_sha256']:
        raise ValueError('SOPHIA_NATIVE_REQUEST_SUBSTITUTION')
    source=request['source']
    try:
        parsed=_parse_json(source.encode(),'admitted source')
        if type(parsed) is dict:source=parsed
    except ValueError:pass
    expected_context={'source':source,'evidence':request['evidence']}
    if context['schema_id']=='control-anchor.evaluator-context.v2':
        expected_context['prompt']=request['prompt']
    if request.get('event') is not None:expected_context['event']=request['event']
    reconstruction=None
    if context['native_analysis']:
        if context['provider_state']!='CAPTURED':raise ValueError('SOPHIA_NATIVE_CANDIDATE_STATE_INVALID')
        candidate=_parse_json(contents['native/candidate_packet.json'],'candidate')
        expected_context['response']=candidate['answer']
        source_bytes=(unicodedata.normalize('NFC',request['source'].replace('\r\n','\n').replace('\r','\n')).strip()+'\n').encode()
        if contents['native/request.json']!=_canonical_json_bytes(admission['native_request']) or contents['native/grounding/source.bin']!=source_bytes:
            raise ValueError('SOPHIA_NATIVE_GOVERNED_INPUT_MISMATCH')
        binding=context['analysis_binding']
        if binding['semantic_capture_sha256']!=candidate['raw_output_sha256'] or binding['requested_model']!=candidate['model_identity']:
            raise ValueError('SOPHIA_NATIVE_PROVIDER_LINEAGE_MISMATCH')
        # New options remain admitted data. Recompute their bindings here;
        # never trust a producer's claim that a different AHA case was selected.
        options=request['governance'].get('analysis')
        if options is not None:
            meta=admission['native_request']['meta']
            aha=_parse_json(contents['native/aha_result.json'],'aha result')
            if (request['governance'].get('schema_id')!='control-anchor.task-governance.v2'
                    or meta.get('analysis_options_sha256')!=digest(_canonical_json_bytes(options))
                    or meta.get('ucm_hypotheses')!=options.get('ucm_hypotheses')
                    or aha.get('case')!=options.get('aha_case')):
                raise ValueError('SOPHIA_ANALYTICAL_OPTION_SUBSTITUTION')
        reconstruction=_check_reconstruction(request,admission,contents)
    if context['execution_context']!=expected_context:
        raise ValueError('SOPHIA_EXECUTION_INPUT_SUBSTITUTION')
    observation_sha=_check_observation(context)
    plan=admission['ucc_plan']
    # Observation v4 executes the actual scoped action/control population above.
    # Its compatibility plan is authenticated definition only, never a second
    # unscoped population of applied business findings.
    expected={} if observation_sha is not None else {s['id']:s for s in plan['steps']}
    seen=set();nonpass=[]
    for row in context['policy_results']:
        # Legacy reference-presence rows are explicitly outside this new plan.
        if 'ucc_result' not in row:continue
        ucc=row['ucc_result'];identifier=ucc['control_id']
        if identifier not in expected or identifier in seen or ucc['plan_sha256']!=admission['ucc_plan_sha256'] or ucc['plan_version']!=plan['version']:
            raise ValueError('SOPHIA_POLICY_ROW_IDENTITY_INVALID')
        seen.add(identifier);step=expected[identifier]
        if ucc['kind']!=step['kind'] or ucc['phase']!=step['phase'] or ucc['operation']!=step['operation'] or row['result']!=ucc['result']:
            raise ValueError('SOPHIA_POLICY_ROW_SEMANTICS_INVALID')
        if ucc['result'] not in {'PASS','FAIL','HOLD','NOT_EXECUTED'} or step['kind']!='executable' and ucc['result']!='NOT_EXECUTED':
            raise ValueError('SOPHIA_UNPERFORMED_PROCEDURE_PROMOTED')
        expected_bindings={}
        pointers=[step['arguments'][key] for key in ('path','left','right','earlier','later') if key in step['arguments']]
        if step['operation']=='compare_total':
            # Recompute every term's binding independently. This authenticates
            # declared inputs; it does not rerun UCC or adopt its conclusion.
            terms=step['arguments'].get('terms')
            if (type(terms) is not list or not 2<=len(terms)<=16
                    or any(type(term) is not str for term in terms)
                    or len(set(terms))!=len(terms)):
                raise ValueError('SOPHIA_TOTAL_INPUT_CONTRACT_INVALID')
            pointers.extend(terms)
        for pointer in pointers:
            present,value=_lookup(context['execution_context'],pointer)
            expected_bindings[pointer]={'present':present,'sha256':digest(_canonical_json_bytes(value)) if present else None}
        if ucc['input_bindings']!=expected_bindings:
            raise ValueError('SOPHIA_POLICY_INPUT_BINDING_INVALID')
        if ucc['result']!='PASS':nonpass.append(identifier)
    if seen!=set(expected):raise ValueError('SOPHIA_POLICY_ROW_POPULATION_INCOMPLETE')
    native=None
    if context['native_analysis']:
        output=Path(output_directory);output.mkdir(parents=True,exist_ok=False)
        native=audit_totality_run(Path(root)/'native',output/'sophia_audit_packet.json')
        disposition=native['disposition']
    else:
        if request['governance']['processing_kind']=='NON_MODEL_EVENT':
            if context['provider_state']!='EVENT_RECORDED' or json.loads(request['source'])!=request['event']:
                raise ValueError('SOPHIA_EVENT_RECORD_BINDING_INVALID')
            disposition='HOLD' if nonpass else 'PASS'
        else:
            disposition='HOLD' # A failed/refused/unknown request has no completed candidate audit.
    if nonpass and disposition=='PASS':disposition='HOLD'
    # Repeat actual file identity reads; no source byte is rewritten.
    _,after=authenticate_inputs(root,manifest)
    if contents!=after:raise ValueError('SOPHIA_INPUT_CHANGED_DURING_EVALUATION')
    result={'schema_id':SCHEMA,'record_id':manifest['record_id'],
        'input_manifest_sha256':digest(_canonical_json_bytes(manifest)),
        'disposition':disposition,'native_audit':native,'native_audit_executed':native is not None,
        'policy_input_bindings_recomputed':True,'policy_predicates_reexecuted_by_sophia':False,
        'nonpass_policy_controls':nonpass,'input_files_unchanged':True,
        'human_decision':'PENDING','memory_write':False,'model_request':False,
        'limitations':['File/claim binding and declared bounded algorithms are not source truth or an assurance opinion.',
            'UCC input bindings and procedure population are independently checked; its policy predicates are not relabeled a second independent execution.',
            'Raw provider quarantine is deliberately outside evaluator access.']}
    if reconstruction is not None:
        result.update(schema_id='control-anchor.sophia-governed-evaluation.v2',retrosynthesis=reconstruction)
    if observation_sha is not None:
        result.update(schema_id='control-anchor.sophia-governed-evaluation.v3',
            observation_assessment_sha256=observation_sha,observation_input_bindings_recomputed=True,
            business_control_effect='OBSERVE_AND_REPORT_ONLY',assessment_results_are_business_authority=False,
            compatibility_plan='DEFINITION_ONLY_NOT_EXECUTED',policy_input_bindings_recomputed=False)
        result['limitations'].append('Observation context and input bindings are independently checked; neither declared source context nor UCC conclusions are independent source truth or business authority.')
    return result
