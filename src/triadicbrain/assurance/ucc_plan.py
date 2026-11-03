"""Bounded UCC plans over admitted data; no eval, imports, network or model calls.

The historical grammar, donor steps and Linux profile are distinct formats.
Translation is explicit and rejects unsupported semantics before activation.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
import json
import re

from .canonical import canonical_bytes, sha256_bytes

SCHEMA = 'control-anchor.ucc-plan.v1'
OPERATIONS = {
    'field_present': {'path'},
    'equals': {'path', 'expected'},
    'number_range': {'path', 'minimum', 'maximum'},
    'compare_amounts': {'left', 'right', 'tolerance'},
    'compare_total': {'terms', 'right', 'tolerance'},
    'date_order': {'earlier', 'later'},
    'required_sections': {'path', 'sections'},
    'text_contains': {'path', 'text'},
}
MISSING = object()


def _exact(value, fields, code):
    if type(value) is not dict or set(value) != set(fields):
        raise ValueError(code)


def _text(value, size, code):
    if (type(value) is not str or not value.strip() or len(value) > size
            or any(0xD800 <= ord(c) <= 0xDFFF or ord(c) < 32 for c in value)):
        raise ValueError(code)


def _pointer(value):
    _text(value, 256, 'UCC_PATH_INVALID')
    if (not re.fullmatch(r'/(source|evidence|event|response)(/[A-Za-z0-9_.-]{1,64}){0,8}', value)
            or any(part in {'.', '..'} for part in value.split('/'))):
        raise ValueError('UCC_PATH_OUTSIDE_ADMITTED_CONTEXT')
    return value


def _number(value):
    if type(value) not in (str, int) or isinstance(value, bool):
        raise ValueError('UCC_DECIMAL_STRING_OR_INTEGER_REQUIRED')
    if not re.fullmatch(r'-?(?:0|[1-9][0-9]{0,29})(?:\.[0-9]{1,12})?', str(value)):
        raise ValueError('UCC_BOUNDED_DECIMAL_REQUIRED')
    return Decimal(value)


def validate_plan(value):
    _exact(value, {'schema_id', 'plan_id', 'version', 'steps'}, 'UCC_PLAN_SHAPE_INVALID')
    if value['schema_id'] != SCHEMA:
        raise ValueError('UCC_PLAN_SCHEMA_UNSUPPORTED')
    if type(value['plan_id']) is not str or not re.fullmatch(r'[A-Z][A-Z0-9_-]{0,63}', value['plan_id']):
        raise ValueError('UCC_PLAN_ID_INVALID')
    if type(value['version']) is not int or not 1 <= value['version'] <= 1000000:
        raise ValueError('UCC_PLAN_VERSION_INVALID')
    steps = value['steps']
    if type(steps) is not list or not 1 <= len(steps) <= 64:
        raise ValueError('UCC_PLAN_STEPS_INVALID')
    seen = set()
    for step in steps:
        _exact(step, {'id', 'title', 'kind', 'phase', 'operation', 'arguments'}, 'UCC_STEP_SHAPE_INVALID')
        sid = step['id']
        if type(sid) is not str or not re.fullmatch(r'[A-Z][A-Z0-9_-]{0,63}', sid) or sid in seen:
            raise ValueError('UCC_STEP_ID_INVALID_OR_DUPLICATE')
        seen.add(sid)
        _text(step['title'], 512, 'UCC_TITLE_REQUIRED')
        if step['phase'] not in ('admission', 'result'):
            raise ValueError('UCC_PHASE_INVALID')
        kind = step['kind']
        args = step['arguments']
        if kind in ('human_procedure', 'advisory'):
            if step['operation'] is not None:
                raise ValueError('UCC_NONEXECUTABLE_OPERATION_FORBIDDEN')
            _exact(args, {'procedure'}, 'UCC_PROCEDURE_SHAPE_INVALID')
            _text(args['procedure'], 2048, 'UCC_PROCEDURE_REQUIRED')
            continue
        if kind != 'executable' or type(step['operation']) is not str or step['operation'] not in OPERATIONS:
            raise ValueError('UCC_UNKNOWN_EXECUTABLE_OPERATION')
        operation = step['operation']
        _exact(args, OPERATIONS[operation], 'UCC_OPERATION_ARGUMENTS_INVALID')
        for key in ('path', 'left', 'right', 'earlier', 'later'):
            if key in args:
                _pointer(args[key])
                if step['phase'] == 'admission' and args[key].startswith('/response'):
                    raise ValueError('UCC_ADMISSION_CANNOT_REQUIRE_FUTURE_RESPONSE')
        if operation == 'equals':
            expected = args['expected']
            if type(expected) not in (str, int, bool) or (type(expected) is str and len(expected) > 2048):
                raise ValueError('UCC_SCALAR_COMPARISON_REQUIRED')
        elif operation == 'number_range':
            if _number(args['minimum']) > _number(args['maximum']):
                raise ValueError('UCC_RANGE_REVERSED')
        elif operation in ('compare_amounts', 'compare_total'):
            if _number(args['tolerance']) < 0:
                raise ValueError('UCC_NEGATIVE_TOLERANCE')
            if operation == 'compare_total':
                terms = args['terms']
                if type(terms) is not list or not 2 <= len(terms) <= 16:
                    raise ValueError('UCC_TOTAL_TERMS_INVALID')
                for pointer in terms:
                    _pointer(pointer)
                    if step['phase'] == 'admission' and pointer.startswith('/response'):
                        raise ValueError('UCC_ADMISSION_CANNOT_REQUIRE_FUTURE_RESPONSE')
                if len(set(terms)) != len(terms):
                    raise ValueError('UCC_TOTAL_TERMS_INVALID')
        elif operation == 'required_sections':
            sections = args['sections']
            if type(sections) is not list or not 1 <= len(sections) <= 32:
                raise ValueError('UCC_SECTIONS_INVALID')
            for section in sections:
                _text(section, 256, 'UCC_SECTION_REQUIRED')
            if len(sections) != len(set(sections)):
                raise ValueError('UCC_DUPLICATE_SECTION')
        elif operation == 'text_contains':
            _text(args['text'], 256, 'UCC_LITERAL_TEXT_REQUIRED')
    return deepcopy(value)


def plan_digest(plan):
    return sha256_bytes(canonical_bytes(validate_plan(plan)))


def _at(context, pointer):
    value = context
    for part in pointer[1:].split('/'):
        if type(value) is not dict or part not in value:
            return MISSING
        value = value[part]
    return value


def _iso_date(value):
    if type(value) is not str or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('UCC_ISO_CALENDAR_DATE_REQUIRED')
    return date.fromisoformat(value)


def execute_plan(plan, context, *, phase):
    plan = validate_plan(plan)
    if phase not in ('admission', 'result') or type(context) is not dict or set(context) - {'source', 'evidence', 'event', 'response'}:
        raise ValueError('UCC_EXECUTION_CONTEXT_INVALID')
    # Canonical conversion bounds the observable data and rejects non-JSON values.
    if len(canonical_bytes(context)) > 256 * 1024:
        raise ValueError('UCC_CONTEXT_TOO_LARGE')
    rows = []
    for step in plan['steps']:
        if step['phase'] != phase:
            continue
        args, operation = step['arguments'], step['operation']
        row = {'control_id': step['id'], 'title': step['title'], 'kind': step['kind'],
               'phase': phase, 'plan_sha256': plan_digest(plan), 'plan_version': plan['version'],
               'operation': operation, 'result': 'NOT_EXECUTED', 'observation': None,
               'input_bindings': {}, 'human_procedure': 'NOT_EXECUTED'}
        if step['kind'] != 'executable':
            row['observation'] = 'HUMAN_PROCEDURE_PENDING' if step['kind'] == 'human_procedure' else 'ADVISORY_NOT_EXECUTED'
            row['procedure'] = args['procedure']
            rows.append(row)
            continue
        inputs = {key: _at(context, args[key]) for key in ('path', 'left', 'right', 'earlier', 'later') if key in args}
        if operation == 'compare_total':
            inputs.update({f'term{index}': _at(context, pointer) for index, pointer in enumerate(args['terms'])})
        input_paths = dict(args)
        if operation == 'compare_total':
            input_paths.update({f'term{index}': pointer for index, pointer in enumerate(args['terms'])})
        row['input_bindings'] = {input_paths[key]: {'present': value is not MISSING,
            'sha256': None if value is MISSING else sha256_bytes(canonical_bytes(value))}
            for key, value in inputs.items()}
        if any(value is MISSING for value in inputs.values()):
            row.update(result='HOLD', observation='REQUIRED_INPUT_MISSING')
            rows.append(row)
            continue
        try:
            value = inputs.get('path')
            if operation == 'field_present':
                passed = value is not None and not (type(value) is str and not value.strip())
            elif operation == 'equals':
                passed = type(value) is type(args['expected']) and value == args['expected']
            elif operation == 'number_range':
                passed = _number(args['minimum']) <= _number(value) <= _number(args['maximum'])
            elif operation == 'compare_amounts':
                # Accepted operands contain up to 42 digits. Ambient Decimal
                # precision must not round a discrepancy into a passing result.
                with localcontext() as precision:
                    precision.prec = 96
                    passed = abs(_number(inputs['left']) - _number(inputs['right'])) <= _number(args['tolerance'])
            elif operation == 'compare_total':
                with localcontext() as precision:
                    precision.prec = 96
                    total = sum((_number(inputs[f'term{i}']) for i in range(len(args['terms']))), Decimal(0))
                    passed = abs(total - _number(inputs['right'])) <= _number(args['tolerance'])
                    row['computed_total'] = str(total)
            elif operation == 'date_order':
                passed = _iso_date(inputs['earlier']) <= _iso_date(inputs['later'])
            elif operation == 'required_sections':
                from .ucc_primitives import check_required_sections
                metrics,flags=check_required_sections({'sections':value},'sections',args['sections'])
                row['section_observations']=metrics
                passed=flags['sections_complete']
            elif operation == 'text_contains':
                if type(value) is not str:
                    raise ValueError('UCC_TEXT_REQUIRED')
                passed = args['text'].casefold() in value.casefold()
            else:
                raise ValueError('UCC_UNKNOWN_EXECUTABLE_OPERATION')
            row.update(result='PASS' if passed else 'FAIL', observation='DETERMINISTIC_CHECK_SATISFIED' if passed else 'DETERMINISTIC_CHECK_NOT_SATISFIED')
        except (ValueError, InvalidOperation) as exc:
            row.update(result='FAIL', observation=str(exc))
        rows.append(row)
    return rows


def translate_grammar(module, *, plan_id, version):
    """Translate the supported donor grammar subset, never its two-call executor.

    Only exists(/source/...) validation expressions have executable semantics in
    this version. Narrative reasoning remains a human procedure. Other expressions
    must be rewritten as a supported structured plan by the policy author.
    """
    fields = {'meta', 'authorities', 'tasks', 'roles', 'reasoning_steps', 'evidence',
              'validation_rules', 'reporting', 'escalation_policy'}
    _exact(module, fields, 'UCC_GRAMMAR_SHAPE_UNSUPPORTED')
    if module['escalation_policy'] != []:
        raise ValueError('UCC_GRAMMAR_ESCALATION_REQUIRES_EXPLICIT_PLAN')
    steps = []
    rules = module['validation_rules']
    if type(rules) is not list:
        raise ValueError('UCC_GRAMMAR_RULES_INVALID')
    for index, rule in enumerate(rules, 1):
        _exact(rule, {'id', 'description', 'expression'}, 'UCC_GRAMMAR_RULE_INVALID')
        expression = rule['expression']
        match = re.fullmatch(r'exists\((/[^()]+)\)', expression) if type(expression) is str else None
        if not match:
            raise ValueError('UCC_GRAMMAR_EXPRESSION_NOT_IMPLEMENTED')
        steps.append({'id': 'GRAMMAR-CHECK-'+str(index), 'title': rule['description'],
                      'kind': 'executable', 'phase': 'result', 'operation': 'field_present',
                      'arguments': {'path': match[1]}})
    reasoning = module['reasoning_steps']
    if type(reasoning) is not list:
        raise ValueError('UCC_GRAMMAR_REASONING_INVALID')
    for index, procedure in enumerate(reasoning, 1):
        steps.append({'id': 'GRAMMAR-HUMAN-'+str(index), 'title': 'Declared grammar reasoning procedure',
                      'kind': 'human_procedure', 'phase': 'result', 'operation': None,
                      'arguments': {'procedure': procedure}})
    # Preserve every original field and the exact translation source binding.
    plan = validate_plan({'schema_id': SCHEMA, 'plan_id': plan_id, 'version': version, 'steps': steps})
    return {'plan': plan, 'source_schema': 'UCCModule-grammar',
            'source_sha256': sha256_bytes(canonical_bytes(module)), 'source': deepcopy(module),
            'unexecuted_context_fields': ['meta', 'authorities', 'tasks', 'roles', 'evidence', 'reporting'],
            'model_executor_invoked': False, 'authority_effect': 'NONE'}


def translate_steps(module,*,plan_id,version,input_root='/source'):
    """Compile the pinned UCC step-document subset onto admitted data only.

    The donor schema permits additional fields, research steps and path loaders.
    This supported translation deliberately rejects unknown semantics and file
    access; it does not execute the donor's full research dispatch loop.
    """
    _exact(module,{'ucc_version','module','steps'},'UCC_STEP_MODULE_SHAPE_UNSUPPORTED')
    _text(module['ucc_version'],64,'UCC_VERSION_REQUIRED')
    metadata=module['module']
    if type(metadata) is not dict or not {'id','version','title','intent'}<=set(metadata) or set(metadata)-{'id','version','title','intent','authors','license','safety'}:
        raise ValueError('UCC_STEP_MODULE_METADATA_UNSUPPORTED')
    for key in ('id','version','title','intent'):_text(metadata[key],2048,'UCC_STEP_MODULE_METADATA_INVALID')
    if input_root not in {'/source','/evidence','/event','/response'}:raise ValueError('UCC_ADMITTED_INPUT_ROOT_REQUIRED')
    if type(module['steps']) is not list or not 1<=len(module['steps'])<=64:raise ValueError('UCC_STEP_LIST_INVALID')
    steps=[];identifiers=set()
    for index,step in enumerate(module['steps'],1):
        _exact(step,{'id','type','params'},'UCC_DONOR_STEP_SHAPE_UNSUPPORTED')
        if type(step['id']) is not str or not re.fullmatch('[A-Za-z0-9_.-]+',step['id']) or step['id'] in identifiers:
            raise ValueError('UCC_DONOR_STEP_ID_INVALID_OR_DUPLICATE')
        identifiers.add(step['id'])
        if step['type']!='check_required_sections':raise ValueError('UCC_DONOR_STEP_NOT_IMPLEMENTED:'+str(step['type']))
        params=step['params'];_exact(params,{'sections_key','required_sections'},'UCC_DONOR_STEP_PARAMS_UNSUPPORTED')
        pointer=_pointer(input_root+'/'+params['sections_key'])
        steps.append({'id':'UCC-STEP-'+str(index),'title':'Required sections: '+', '.join(params['required_sections']),
            'kind':'executable','phase':'result','operation':'required_sections',
            'arguments':{'path':pointer,'sections':params['required_sections']}})
    plan=validate_plan({'schema_id':SCHEMA,'plan_id':plan_id,'version':version,'steps':steps})
    return {'plan':plan,'source_schema':'UCC-step-module','source_sha256':sha256_bytes(canonical_bytes(module)),
        'source':deepcopy(module),'step_id_map':dict(zip((s['id'] for s in steps),(s['id'] for s in module['steps']))),
        'unexecuted_context_fields':['module.authors','module.license','module.safety','module.intent'],
        'file_ingestion':'Not executed; input is the already admitted canonical object','authority_effect':'NONE'}
