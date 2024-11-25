import os
import pytest
from yamale import YamaleError
import yamale

def test_keyed_subset_with_include_should_fail_with_correct_message():
    valid_msg = "workloads.replicas: Unexpected element"
    invalid_msg = "workloads.type: 'api' not in ('ui',)"
    
    with pytest.raises(YamaleError) as excinfo:
        schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml")
        data = yamale.make_data("tests/fixtures/keyed/data_keyed_subset_with_include_bad.yaml")
        yamale.validate(schema, data)
   
    assert valid_msg in str(excinfo.value)
    assert invalid_msg not in str(excinfo.value)


def test_keyed_subset_with_include_should_succeed():
    schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_subset_with_include.yaml")
    data = yamale.make_data("tests/fixtures/keyed/data_keyed_subset_with_include_good.yaml")
    result = yamale.validate(schema, data)

    assert len(result) == 0


def test_keyed_any_with_include_should_fail_with_correct_message():
    valid_msg = "deploy.branch: Unexpected element"
    invalid_msg = "deploy.strategy: 'branch' not in ('preview',)"

    with pytest.raises(YamaleError) as excinfo:
        schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml")
        data = yamale.make_data("tests/fixtures/keyed/data_keyed_any_with_include_bad.yaml")
        yamale.validate(schema, data)
    
    assert valid_msg in str(excinfo.value)
    assert invalid_msg not in str(excinfo.value)


def test_keyed_any_with_include_should_succeed():
    schema = yamale.make_schema("tests/fixtures/keyed/schema_keyed_any_with_include.yaml")
    data = yamale.make_data("tests/fixtures/keyed/data_keyed_any_with_include_good.yaml")
    result = yamale.validate(schema, data)

    assert len(result) == 0
