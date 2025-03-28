import os
import contextlib
import pytest

from yamlr import __main__ as command_line
from yamlr import YamlrError

parsers = ["pyyaml", "PyYAML"]


@contextlib.contextmanager
def scoped_change_dir(new_dir):
    cwd = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(cwd)


@pytest.mark.parametrize("parser", parsers)
def test_bad_yaml(parser):
    with pytest.raises(ValueError) as e:
        command_line._router(
            "tests/fixtures/command_line/yamls/bad.yaml",
            "tests/fixtures/command_line/schemas/map_schema.yaml",
            1,
            parser,
        )
    errors = e.value.results[0]['errors']
    errors = [x for x in errors if x['error'] == "'12.5' is not a str." and x['path'] == "map.bad"]
    assert len(errors) == 1

@pytest.mark.parametrize("parser", parsers)
def test_required_keys_yaml(parser):
    with pytest.raises(ValueError) as e:
        command_line._router(
            "tests/fixtures/command_line/yamls/required_keys_bad.yaml",
            "tests/fixtures/command_line/schemas/required_keys_schema.yaml",
            1,
            parser,
        )
    errors = e.value.results[0]['errors']
    errors = [x for x in errors if x['error'] == "Required field missing" and x['path'] == "map.key"]
    assert len(errors) == 1

@pytest.mark.parametrize("parser", parsers)
def test_good_yaml(parser):
    command_line._router(
        "tests/fixtures/command_line/yamls/good.yaml", 
        "tests/fixtures/command_line/schemas/map_schema.yaml", 
        1, 
        parser
    )


@pytest.mark.parametrize("parser", parsers)
def test_good_relative_yaml(parser):
    command_line._router(
        "tests/fixtures/command_line/yamls/good.yaml",
        "tests/fixtures/command_line/schemas/external.yaml",
        1,
        parser,
    )


@pytest.mark.parametrize("parser", parsers)
def test_good_relative_schema_in_subfolder(parser):
    with scoped_change_dir("tests/fixtures/command_line/schemas"):
        command_line._router(
            "tests/fixtures/command_line/yamls/good.yaml", 
            "tests/fixtures/command_line/schemas/external.yaml", 
            1, 
            parser
        )


@pytest.mark.parametrize("parser", parsers)
def test_external_glob_schema(parser):
    command_line._router(
        "tests/fixtures/command_line/yamls/good.yaml",
        "tests/fixtures/command_line/schemas/ex*.yaml",
        1,
        parser,
    )


def test_empty_schema_file():
    with pytest.raises(ValueError, match="is an empty file!"):
        command_line._router(
            "tests/fixtures/command_line/empty_schema/data.yaml",
            "tests/fixtures/command_line/empty_schema/empty_schema.yaml",
            1,
            "PyYAML",
        )


def test_external_schema():
    command_line._router(
        "tests/fixtures/command_line/yamls/good.yaml",
        "tests/fixtures/command_line/schemas/external.yaml",
        1,
        "PyYAML",
    )


def test_bad_dir():
    with pytest.raises(ValueError):
        command_line._router(
            "tests/fixtures/command_line/yamls", 
            "tests/fixtures/command_line/schemas/map_schema.yaml", 
            4, 
            "PyYAML"
        )


def test_bad_strict():
    with pytest.raises(ValueError) as e:
        command_line._router(
            "tests/fixtures/command_line/yamls/required_keys_extra_element.yaml",
            "tests/fixtures/command_line/schemas/required_keys_schema.yaml",
            4,
            strict=True,
        )
    errors = e.value.results[0]['errors']
    errors = [x for x in errors if x['error'] == "Unexpected element" and x['path'] == "map.key2"]
    assert len(errors) == 1


def test_bad_issue_54():
    with pytest.raises(YamlrError) as e:
        command_line._router(
            "tests/fixtures/nested_issue_54.yaml",
            "tests/fixtures/nested.yaml",
            4,
            strict=True,
        )
    errors = e.value.results[0]['errors']
    errors = [f"{x['path']}: {x['error']}" for x in errors]
    assert "string: Required field missing" in errors
    assert "number: Required field missing" in errors
    assert "integer: Required field missing" in errors
    assert "boolean: Required field missing" in errors
    assert "date: Required field missing" in errors
    assert "datetime: Required field missing" in errors
    assert "nest: Required field missing" in errors
    assert "list: Required field missing" in errors


def test_nested_schema_issue_69():
    command_line._router(
        "tests/fixtures/command_line/nestedYaml", 
        "schema.yaml", 
        1
    )
