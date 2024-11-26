import re
import os
import pytest
from yamale import YamaleError
import yamale

def test_all_yaml():
    schema = yamale.make_schema("tests/fixtures/meta_test/schema.yaml", debug=True)
    data = yamale.make_data("tests/fixtures/meta_test/data1.yaml")
    yamale.validate(schema, data)

@pytest.mark.parametrize(
    "data_filename", ["data1.yaml", "data2.yaml", "data3.yaml", "data4.yaml"]
)
def test_bad_yaml(data_filename):
    with pytest.raises(YamaleError) as excinfo:
        schema = yamale.make_schema("tests/fixtures/meta_test/schema_bad.yaml")
        data = yamale.make_data(f"tests/fixtures/meta_test/{data_filename}")
        yamale.validate(schema, data)
    
    assert len(str(excinfo.value)) > 0

@pytest.mark.parametrize(
    "data_filename", ["data1.yaml", "some_data.yaml"]
)
def test_map_yaml(data_filename):
    schema = yamale.make_schema("tests/fixtures/meta_test/schema.yaml")
    data = yamale.make_data(f"tests/fixtures/meta_test/{data_filename}")
    yamale.validate(schema, data)

def test_schema_doesnt_validate_it_self():
    with pytest.raises(YamaleError) as excinfo:
        schema = yamale.make_schema("tests/fixtures/meta_test/schema.yaml")
        data = yamale.make_data(f"tests/fixtures/meta_test/schema.yaml")
        yamale.validate(schema, data)
    
    assert len(str(excinfo.value)) > 0

def test_bad_required_yaml():
    with pytest.raises(YamaleError) as excinfo:
        schema = yamale.make_schema("tests/fixtures/meta_test/schema_required_bad.yaml")
        data = yamale.make_data(f"tests/fixtures/meta_test/data_required_bad.yaml")
        yamale.validate(schema, data)
    
    assert len(str(excinfo.value)) > 0

def test_good_required_yaml():
    schema = yamale.make_schema("tests/fixtures/meta_test/schema_required_good.yaml")
    data = yamale.make_data(f"tests/fixtures/meta_test/data_required_good.yaml")
    yamale.validate(schema, data)
