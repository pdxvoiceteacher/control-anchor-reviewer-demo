"""Data-driven behavior and strict rejection; no model or network calls."""
from copy import deepcopy
import pytest
from triadicbrain.assurance.ucc_plan import (validate_plan, execute_plan, plan_digest,
                                            translate_grammar)


def plan(operation='number_range', arguments=None, phase='result'):
    return {'schema_id':'control-anchor.ucc-plan.v1','plan_id':'COLD-CHAIN','version':1,
        'steps':[{'id':'TEMPERATURE','title':'Recorded shipment temperature is within the declared range',
                  'kind':'executable','phase':phase,'operation':operation,
                  'arguments': arguments or {'path':'/source/temperature','minimum':'2','maximum':'8'}}]}


def test_new_policy_changes_an_executed_check_without_source_changes():
    first=plan();second=deepcopy(first);second['version']=2
    second['steps'][0]['arguments']['maximum']='6'
    context={'source':{'temperature':'7'}}
    assert execute_plan(first,context,phase='result')[0]['result']=='PASS'
    assert execute_plan(second,context,phase='result')[0]['result']=='FAIL'
    assert plan_digest(first)!=plan_digest(second)
    assert execute_plan(first,{'source':{}},phase='result')[0]['result']=='HOLD'


@pytest.mark.parametrize('value',['7',7,'7.50','2','8'])
def test_bounded_decimal_values(value):
    assert execute_plan(plan(),{'source':{'temperature':value}},phase='result')[0]['result']=='PASS'


@pytest.mark.parametrize('value',[True,None,7.0,'NaN','Infinity','1e3','7 '*1000,[],{},'9'])
def test_invalid_or_out_of_range_data_does_not_pass(value):
    assert execute_plan(plan(),{'source':{'temperature':value}},phase='result')[0]['result']=='FAIL'


@pytest.mark.parametrize('operation,args,source,expected',[
    ('field_present',{'path':'/source/reference'},{'reference':None},'FAIL'),
    ('field_present',{'path':'/source/reference'},{'reference':'REF-1'},'PASS'),
    ('equals',{'path':'/source/ready','expected':True},{'ready':1},'FAIL'),
    ('equals',{'path':'/source/ready','expected':True},{'ready':True},'PASS'),
    ('compare_amounts',{'left':'/source/book','right':'/source/bank','tolerance':'0.01'}, {'book':'1.01','bank':'1.00'},'PASS'),
    ('compare_amounts',{'left':'/source/book','right':'/source/bank','tolerance':'0.01'}, {'book':'1.02','bank':'1.00'},'FAIL'),
    ('date_order',{'earlier':'/source/start','later':'/source/end'}, {'start':'2026-01-01','end':'2026-01-02'},'PASS'),
    ('date_order',{'earlier':'/source/start','later':'/source/end'}, {'start':'2026-02-30','end':'2026-03-01'},'FAIL'),
    ('required_sections',{'path':'/source/sections','sections':['finding']},{'sections':{'finding':None}},'FAIL'),
    ('required_sections',{'path':'/source/sections','sections':['finding']},{'sections':{'finding':'Observed exception'}},'PASS'),
    ('text_contains',{'path':'/source/status','text':'PENDING'},{'status':'Review pending'},'PASS'),
])
def test_supported_operations(operation,args,source,expected):
    row=execute_plan(plan(operation,args),{'source':source},phase='result')[0]
    assert row['result']==expected and row['input_bindings']


@pytest.mark.parametrize('kind',['human_procedure','advisory'])
def test_narrative_procedure_never_becomes_executed_pass(kind):
    value=plan();value['steps'][0].update(kind=kind,operation=None,arguments={'procedure':'Review the actual source and authorize if appropriate.'})
    row=execute_plan(value,{'source':{'approval':'approved'}},phase='result')[0]
    assert row['result']=='NOT_EXECUTED' and row['human_procedure']=='NOT_EXECUTED'


@pytest.mark.parametrize('change',['unknown-op','code','unknown-field','duplicate','bad-pointer','escape',
    'response-before-dispatch','reversed','negative-tolerance','bool-version','missing-title','wrong-kind'])
def test_rejections_before_activation(change):
    value=plan();step=value['steps'][0]
    if change=='unknown-op':step['operation']='arbitrary_new_operation'
    elif change=='code':step['arguments']['eval']='__import__("os")'
    elif change=='unknown-field':value['fallback']='PASS'
    elif change=='duplicate':value['steps'].append(deepcopy(step))
    elif change=='bad-pointer':step['arguments']['path']='file:///etc/passwd'
    elif change=='escape':step['arguments']['path']='/source/../../credentials'
    elif change=='response-before-dispatch':step.update(phase='admission');step['arguments']['path']='/response/text'
    elif change=='reversed':step['arguments'].update(minimum='8',maximum='2')
    elif change=='negative-tolerance':step.update(operation='compare_amounts',arguments={'left':'/source/a','right':'/source/b','tolerance':'-1'})
    elif change=='bool-version':value['version']=True
    elif change=='missing-title':step['title']=' '
    else:step['kind']='llm_asserted_pass'
    with pytest.raises(ValueError):validate_plan(value)


def test_grammar_translation_preserves_narrative_as_nonexecuted_context():
    module={'meta':{'module_id':'EXAMPLE'},'authorities':[],'tasks':[], 'roles':[],
        'reasoning_steps':['A reviewer must assess source truth.'],'evidence':{},
        'validation_rules':[{'id':'r1','description':'Required reference','expression':'exists(/source/reference)'}],
        'reporting':{},'escalation_policy':[]}
    translated=translate_grammar(module,plan_id='GRAMMAR-EXAMPLE',version=1)
    assert translated['source']==module and translated['model_executor_invoked'] is False
    rows=execute_plan(translated['plan'],{'source':{'reference':'R1'}},phase='result')
    assert [r['result'] for r in rows]==['PASS','NOT_EXECUTED']
    module['validation_rules'][0]['expression']='source is substantively true'
    with pytest.raises(ValueError,match='EXPRESSION_NOT_IMPLEMENTED'):
        translate_grammar(module,plan_id='GRAMMAR-EXAMPLE',version=1)


def test_real_donor_step_shape_translates_only_supported_admitted_data():
    from triadicbrain.assurance.ucc_plan import translate_steps
    value={'ucc_version':'0.1','module':{'id':'general.sections','version':'1.0','title':'Report completeness',
        'intent':'Check declared sections, not their truth.'},'steps':[{'id':'required-1','type':'check_required_sections',
        'params':{'sections_key':'sections','required_sections':['finding','uncertainty']}}]}
    translated=translate_steps(value,plan_id='NEW-POLICY',version=1)
    rows=execute_plan(translated['plan'],{'source':{'sections':{'finding':'Observed 7','uncertainty':'Not calibrated'}}},phase='result')
    assert rows[0]['result']=='PASS' and rows[0]['section_observations']['present_count']==2
    assert translated['source']==value and translated['step_id_map']=={'UCC-STEP-1':'required-1'}
    for bad in ('ingest_json','compute_lambdaT','verify_json_assertions','emit_report','new_plugin'):
        changed=deepcopy(value);changed['steps'][0]['type']=bad
        with pytest.raises(ValueError,match='NOT_IMPLEMENTED'):translate_steps(changed,plan_id='NEW-POLICY',version=1)
    for raw in (None,True,17,{},[]):
        result=execute_plan(translated['plan'],{'source':{'sections':{'finding':raw,'uncertainty':'pending'}}},phase='result')[0]
        assert result['result']=='FAIL' and result['section_observations']['missing_sections']==['finding']
    substituted=deepcopy(value);substituted['steps'][0]['params']['path']='/etc/passwd'
    with pytest.raises(ValueError):translate_steps(substituted,plan_id='NEW-POLICY',version=1)


def test_grammar_alias_and_unknown_escalation_are_not_silently_dropped():
    value={'meta':{},'authorities':[],'tasks':[],'roles':[],'reasoning_steps':[], 'evidence':{},
        'validation_rules':[],'reporting':{},'escalation':[]}
    with pytest.raises(ValueError,match='SHAPE_UNSUPPORTED'):translate_grammar(value,plan_id='X',version=1)
    value['escalation_policy']=[{'condition':'uncertain','action':'refuse'}];del value['escalation']
    with pytest.raises(ValueError,match='EXPLICIT_PLAN'):translate_grammar(value,plan_id='X',version=1)
