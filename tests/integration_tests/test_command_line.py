import os
import contextlib

import pytest

from yamale import __main__ as command_line
from yamale import YamaleError

dir_path = os.path.dirname(os.path.realpath(__file__))

parsers = ["pyyaml", "PyYAML", "ruamel"]


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
        print(repr(e))
    assert "map.bad: '12.5' is not a str." in e.value.message


@pytest.mark.parametrize("parser", parsers)
def test_required_keys_yaml(parser):
    with pytest.raises(ValueError) as e:
        command_line._router(
            "tests/fixtures/command_line/yamls/required_keys_bad.yaml",
            "tests/fixtures/command_line/schemas/required_keys_schema.yaml",
            1,
            parser,
        )
    assert "map.key: Required field missing" in e.value.message


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
            "PyYAML",
            strict=True,
        )
    assert "map.key2: Unexpected element" in e.value.message


def test_bad_issue_54():
    with pytest.raises(YamaleError) as e:
        command_line._router(
            "tests/fixtures/nested_issue_54.yaml",
            "tests/fixtures/nested.yaml",
            4,
            "PyYAML",
            strict=True,
        )
    assert "string: Required field missing" in e.value.message
    assert "number: Required field missing" in e.value.message
    assert "integer: Required field missing" in e.value.message
    assert "boolean: Required field missing" in e.value.message
    assert "date: Required field missing" in e.value.message
    assert "datetime: Required field missing" in e.value.message
    assert "nest: Required field missing" in e.value.message
    assert "list: Required field missing" in e.value.message


def test_nested_schema_issue_69():
    command_line._router(
        "tests/fixtures/command_line/nestedYaml", 
        "schema.yaml", 
        1, 
        "PyYAML"
    )
