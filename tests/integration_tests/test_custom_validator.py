import re
import os
import pytest
from yamale import YamaleError
import yamale

def test_custom_validator():
    schema = yamale.make_schema("tests/fixtures/meta_test/schema.yaml", debug=True)
    data = yamale.make_data("tests/fixtures/meta_test/data1.yaml")
    yamale.validate(schema, data)
    assert False == True

"""
class Card(Validator):
    #Custom validator for testing purpose

    tag = "card"
    card_regex = re.compile(r"^(10|[2-9JQKA])[SHDC]$")

    def _is_valid(self, value):
        return re.match(self.card_regex, value)


class TestCustomValidator(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema_custom.yaml"
    yaml = "meta_test/data_custom.yaml"

    def runTest(self):
        validators = DefaultValidators.copy()
        validators["card"] = Card
        self.assertTrue(self.validate(validators))


class TestCustomValidatorWithIncludes(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema_custom_with_include.yaml"
    yaml = "meta_test/data_custom_with_include.yaml"

    def runTest(self):
        validators = DefaultValidators.copy()
        validators["card"] = Card
        self.assertTrue(self.validate(validators))

"""