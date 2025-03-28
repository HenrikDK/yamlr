import pytest
from pytest import raises
from yamlr.readers import parse_yaml

parsers = ["pyyaml", "PyYAML"]


@pytest.mark.parametrize("parser", parsers)
def test_reader_error(parser):
    with raises(IOError):
        parse_yaml("wat")
