import io
import pytest
from yamlr import readers as yaml_reader

parsers = ["pyyaml", "PyYAML"]
TYPES = "tests/fixtures/types.yaml"
NESTED = "tests/fixtures/nested.yaml"
KEYWORDS = "tests/fixtures/keywords.yaml"


@pytest.mark.parametrize("parser", parsers)
@pytest.mark.parametrize("use_string", [True, False])
def test_parse(parser, use_string):
    if use_string:
        with io.open(TYPES, encoding="utf-8") as f:
            content = f.read()
        a = yaml_reader.parse_yaml(content=content)[0]
    else:
        a = yaml_reader.parse_yaml(TYPES)[0]
    assert a["string"] == "str()"


def test_parse_validates_arguments():
    with pytest.raises(TypeError):
        yaml_reader.parse_yaml(path=TYPES, content="name: Bob")
    with pytest.raises(TypeError):
        yaml_reader.parse_yaml(path=None, content=None)


@pytest.mark.parametrize("parser", parsers)
def test_types(parser):
    t = yaml_reader.parse_yaml(TYPES)[0]
    assert t["string"] == "str()"
    assert t["number"] == "num()"
    assert t["boolean"] == "bool()"
    assert t["integer"] == "int()"


@pytest.mark.parametrize("parser", parsers)
def test_keywords(parser):
    t = yaml_reader.parse_yaml(KEYWORDS)[0]
    assert t["optional_min"] == "int(min=1, required=False)"


@pytest.mark.parametrize("parser", parsers)
def test_nested(parser):
    t = yaml_reader.parse_yaml(NESTED)[0]
    assert t["list"][-1]["string"] == "str()"
