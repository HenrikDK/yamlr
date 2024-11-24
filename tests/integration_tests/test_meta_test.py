import re
import os
from tests.yamale_testcase import YamaleTestCase
#from yamale.wak_validators import DefaultValidators, Validator


data_folder = os.path.dirname(os.path.realpath(__file__))


class TestAllYaml(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema.yaml"
    yaml = "meta_test/data1.yaml"

    def runTest(self):
        self.assertTrue(self.validate())


class TestBadYaml(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema_bad.yaml"
    yaml = "meta_test/data*.yaml"

    def runTest(self):
        self.assertRaises(ValueError, self.validate)


class TestMapYaml(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema.yaml"
    yaml = [
        "meta_test/data1.yaml",
        "meta_test/some_data.yaml",
        # Make sure  schema doesn't validate itself
        "meta_test/schema.yaml",
    ]

    def runTest(self):
        self.assertTrue(self.validate())


class Card(Validator):
    """Custom validator for testing purpose"""

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


class TestBadRequiredYaml(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema_required_bad.yaml"
    yaml = "meta_test/data_required_bad.yaml"

    def runTest(self):
        self.assertRaises(ValueError, self.validate)


class TestGoodRequiredYaml(YamaleTestCase):
    base_dir = "tests/fixtures/"
    schema = "meta_test/schema_required_good.yaml"
    yaml = "meta_test/data_required_good.yaml"

    def runTest(self):
        self.assertTrue(self.validate())
