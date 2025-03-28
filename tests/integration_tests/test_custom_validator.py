import re
import os
import pytest
from yamlr import validators as val
import yamlr

def validate_card(c_sch, c_val, value):
    card_regex = re.compile(r"^(10|[2-9JQKA])[SHDC]$")
     
    valid = re.match(card_regex, value)
    errors = []
    if not valid:
        error = "'%s' is not a valid card." % (value)
        errors.append(error)
    return errors

def test_custom_validator():
    validators = val.default.copy()
    validators['card'] = {'func': validate_card, 'constraints': [], '_type': 'validator'}

    schema = yamlr.make_schema("tests/fixtures/meta_test/schema_custom.yaml", validators=validators, debug=True)
    data = yamlr.make_data("tests/fixtures/meta_test/data_custom.yaml")
    yamlr.validate(schema, data)

def test_custom_validator_with_include():
    validators = val.default.copy()
    validators['card'] = {'func': validate_card, 'constraints': [], '_type': 'validator'}

    schema = yamlr.make_schema("tests/fixtures/meta_test/schema_custom_with_include.yaml", validators=validators, debug=True)
    data = yamlr.make_data("tests/fixtures/meta_test/data_custom_with_include.yaml")
    yamlr.validate(schema, data)
