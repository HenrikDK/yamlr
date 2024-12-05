import os
import pytest
from yamale import YamaleError
import yamale

def test_keyed_subset_with_include_should_fail_with_correct_message():
    with pytest.raises(YamaleError) as e:
        schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml", debug=True)
        data = yamale.make_data("tests/fixtures/keyed/data_keyed_subset_with_include_bad.yaml")
        yamale.validate(schema, data)

    errors = e.value.results[0]['errors']

    assert len(errors) == 1
    assert errors[0]['error'] == 'Unexpected element'
    assert errors[0]['path'] == 'workloads.replicas'
    assert errors[0]['error'] != "'api' not in ('ui',)"
    assert errors[0]['path'] != 'workloads.type'

def test_keyed_subset_with_include_should_succeed():
    schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml")
    data = yamale.make_data("tests/fixtures/keyed/data_keyed_subset_with_include_good.yaml")
    result = yamale.validate(schema, data)

    for r in result:
        assert r['is_valid']

def test_keyed_any_with_include_should_fail_with_correct_message():
    with pytest.raises(YamaleError) as e:
        schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml")
        data = yamale.make_data("tests/fixtures/keyed/data_keyed_any_with_include_bad.yaml")
        yamale.validate(schema, data)
    
    errors = e.value.results[0]['errors']

    assert len(errors) == 1
    assert errors[0]['error'] == 'Unexpected element'
    assert errors[0]['path'] == 'deploy.branch'
    assert errors[0]['error'] != "'branch' not in ('preview',)"
    assert errors[0]['path'] != 'deploy.strategy'


def test_keyed_any_with_include_should_succeed():
    schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml")
    data = yamale.make_data("tests/fixtures/keyed/data_keyed_any_with_include_good.yaml")
    result = yamale.validate(schema, data)

    for r in result:
        assert r['is_valid']
