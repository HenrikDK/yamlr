import os
import pytest
from yamlr import YamlrError
import yamlr

def test_no_match_keyed_subset_should_fail_with_correct_message():
    with pytest.raises(YamlrError) as e:
        schema = yamlr.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml", debug=True)
        data = yamlr.make_data("tests/fixtures/keyed/data_keyed_subset_no_match.yaml")
        yamlr.validate(schema, data)

    errors = e.value.results[0]['errors']
    assert len(errors) == 1
    assert errors[0]['error'] == "No match for 'type: hub'"
    assert errors[0]['path'] == 'workloads'

def test_keyed_subset_with_include_should_fail_with_correct_message():
    with pytest.raises(YamlrError) as e:
        schema = yamlr.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml", debug=True)
        data = yamlr.make_data("tests/fixtures/keyed/data_keyed_subset_with_include_bad.yaml")
        yamlr.validate(schema, data)

    errors = e.value.results[0]['errors']

    assert len(errors) == 1
    assert errors[0]['error'] == 'Unexpected element'
    assert errors[0]['path'] == 'workloads.replicas'
    assert errors[0]['error'] != "'api' not in ('ui',)"
    assert errors[0]['path'] != 'workloads.type'

def test_keyed_subset_with_include_should_succeed():
    schema = yamlr.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml")
    data = yamlr.make_data("tests/fixtures/keyed/data_keyed_subset_with_include_good.yaml")
    result = yamlr.validate(schema, data)

    for r in result:
        assert r['is_valid']

def test_no_match_keyed_any_should_fail_with_correct_message():
    with pytest.raises(YamlrError) as e:
        schema = yamlr.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml", debug=True)
        data = yamlr.make_data("tests/fixtures/keyed/data_keyed_any_no_match.yaml")
        yamlr.validate(schema, data)
    
    errors = e.value.results[0]['errors']

    assert len(errors) == 1
    assert errors[0]['error'] == "No match for 'strategy: lobster'"
    assert errors[0]['path'] == 'deploy'

def test_keyed_any_with_include_should_fail_with_correct_message():
    with pytest.raises(YamlrError) as e:
        schema = yamlr.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml", debug=True)
        data = yamlr.make_data("tests/fixtures/keyed/data_keyed_any_with_include_bad.yaml")
        yamlr.validate(schema, data)
    
    errors = e.value.results[0]['errors']

    assert len(errors) == 1
    assert errors[0]['error'] == 'Unexpected element'
    assert errors[0]['path'] == 'deploy.branch'
    assert errors[0]['error'] != "'branch' not in ('preview',)"
    assert errors[0]['path'] != 'deploy.strategy'


def test_keyed_any_with_include_should_succeed():
    schema = yamlr.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml")
    data = yamlr.make_data("tests/fixtures/keyed/data_keyed_any_with_include_good.yaml")
    result = yamlr.validate(schema, data)

    for r in result:
        assert r['is_valid']
