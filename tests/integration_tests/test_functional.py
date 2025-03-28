import io
import pytest
import re
from yamlr import yamlr

from tests import get_fixture
from yamlr import validators as val

types = {"schema": "types.yaml", "bad": "types_bad_data.yaml", "good": "types_good_data.yaml"}

nested = {"schema": "nested.yaml", "bad": "nested_bad_data.yaml", "good": "nested_good_data.yaml"}

custom = {"schema": "custom_types.yaml", "bad": "custom_types_bad.yaml", "good": "custom_types_good.yaml"}

keywords = {"schema": "keywords.yaml", "bad": "keywords_bad.yaml", "good": "keywords_good.yaml"}

lists = {"schema": "lists.yaml", "bad": "lists_bad.yaml", "bad2": "lists_bad2.yaml", "good": "lists_good.yaml"}

maps = {"schema": "map.yaml", "bad": "map_bad.yaml", "bad2": "map_bad2.yaml", "good": "map_good.yaml"}

anys = {"schema": "any.yaml", "bad": "any_bad.yaml", "good": "any_good.yaml"}

any_undefined = {"schema": "any_undefined_schema.yaml", "bad": "any_undefined.yaml"}

list_include = {"schema": "list_include.yaml", "good": "list_include_good.yaml"}

issue_22 = {"schema": "issue_22.yaml", "good": "issue_22_good.yaml"}

issue_50 = {"schema": "issue_50.yaml", "good": "issue_50_good.yaml"}

regexes = {"schema": "regex.yaml", "bad": "regex_bad.yaml", "good": "regex_good.yaml"}

ips = {"schema": "ip.yaml", "bad": "ip_bad.yaml", "good": "ip_good.yaml"}

macs = {"schema": "mac.yaml", "bad": "mac_bad.yaml", "good": "mac_good.yaml"}

nested_map = {"schema": "nested_map.yaml", "good": "nested_map_good.yaml"}

top_level_map = {"schema": "top_level_map.yaml", "good": "top_level_map_good.yaml"}

semver = {"schema": "semver_schema.yaml", "good": "semver_good.yaml", "bad": "semver_bad.yaml"}


include_validator = {
    "schema": "include_validator.yaml",
    "good": "include_validator_good.yaml",
    "bad": "include_validator_bad.yaml",
}

strict_map = {"schema": "strict_map.yaml", "good": "strict_map_good.yaml", "bad": "strict_map_bad.yaml"}

mixed_strict_map = {
    "schema": "mixed_strict_map.yaml",
    "good": "mixed_strict_map_good.yaml",
    "bad": "mixed_strict_map_bad.yaml",
}

strict_list = {"schema": "strict_list.yaml", "good": "strict_list_good.yaml", "bad": "strict_list_bad.yaml"}

nested_map2 = {"schema": "nested_map2.yaml", "good": "nested_map2_good.yaml", "bad": "nested_map2_bad.yaml"}

static_list = {"schema": "static_list.yaml", "good": "static_list_good.yaml", "bad": "static_list_bad.yaml"}

nested_issue_54 = {"schema": "nested.yaml", "bad": "nested_issue_54.yaml", "good": "nested_good_data.yaml"}

map_key_constraint = {
    "schema": "map_key_constraint.yaml",
    "good": "map_key_constraint_good.yaml",
    "bad_base": "map_key_constraint_bad_base.yaml",
    "bad_nest": "map_key_constraint_bad_nest.yaml",
    "bad_nest_con": "map_key_constraint_bad_nest_con.yaml",
}

numeric_bool_coercion = {
    "schema": "numeric_bool_coercion.yaml",
    "good": "numeric_bool_coercion_good.yaml",
    "bad": "numeric_bool_coercion_bad.yaml",
}

subset = {
    "schema": "subset.yaml",
    "good": "subset_good.yaml",
    "good2": "subset_good2.yaml",
    "bad": "subset_bad.yaml",
    "bad2": "subset_bad2.yaml",
    "bad3": "subset_bad3.yaml",
}

subset_empty = {"schema": "subset_empty.yaml", "good": "subset_empty_good.yaml", "good2": "subset_empty_good2.yaml"}

subset_nodef = {"schema": "subset_nodef.yaml"}

test_data = [
    types,
    nested,
    custom,
    keywords,
    lists,
    maps,
    anys,
    any_undefined,
    list_include,
    issue_22,
    issue_50,
    regexes,
    ips,
    macs,
    nested_map,
    top_level_map,
    include_validator,
    strict_map,
    mixed_strict_map,
    strict_list,
    nested_map2,
    static_list,
    nested_issue_54,
    map_key_constraint,
    numeric_bool_coercion,
    semver,
    subset,
    subset_empty,
]

def test_flat_make_schema():
    c_sch = yamlr.make_schema(get_fixture(types["schema"]))
    
    keys = c_sch['schema'].keys()
    assert len(keys) == 9
    for key in keys:
        assert c_sch['schema'][key]['_type'] == 'call'


def test_nested_schema():
    c_sch = yamlr.make_schema(get_fixture(nested["schema"]))

    nested_schema = c_sch['schema']

    assert nested_schema["string"]['name'] == 'str'
    assert isinstance(nested_schema["list"], (list, tuple))
    assert nested_schema["list"][0]['name'] == 'str'

@pytest.mark.parametrize("data_map", test_data)
def test_good(data_map):
    for k in data_map.keys():

        if not k.startswith("good"):
            continue
        print()
        schema = yamlr.make_schema(get_fixture(data_map['schema']), debug=True)
        data = yamlr.make_data(get_fixture(data_map[k]))

        yamlr.validate(schema, data)

def test_bad_validate():
    assert count_exception_lines(types["schema"], types["bad"]) == 9

def test_bad_nested():
    assert count_exception_lines(nested["schema"], nested["bad"]) == 2

def test_bad_nested_issue_54():
    exp = [
        "Required field missing",
        "Required field missing",
        "Required field missing",
        "Required field missing",
        "Required field missing",
        "Required field missing",
        "Required field missing",
        "Required field missing",
    ]
    paths = ['string', 'number', 'integer', 'boolean', 'date', 'datetime', 'nest', 'list']
    match_exception_lines(nested_issue_54["schema"], nested_issue_54["bad"], exp)

def test_bad_custom():
    assert count_exception_lines(custom["schema"], custom["bad"]) == 1

def test_bad_lists():
    assert count_exception_lines(lists["schema"], lists["bad"]) == 6

def test_bad2_lists():
    assert count_exception_lines(lists["schema"], lists["bad2"]) == 2

def test_bad_maps():
    assert count_exception_lines(maps["schema"], maps["bad"]) == 7

def test_bad_maps2():
    assert count_exception_lines(maps["schema"], maps["bad2"]) == 1

def test_bad_keywords():
    assert count_exception_lines(keywords["schema"], keywords["bad"]) == 9

def test_bad_anys():
    assert count_exception_lines(anys["schema"], anys["bad"]) == 5

def test_undefined_include():
    assert count_exception_lines(any_undefined["schema"], any_undefined["bad"]) == 1

def test_bad_semver():
    assert count_exception_lines(semver["schema"], semver["bad"]) == 1

def test_bad_regexes():
    assert count_exception_lines(regexes["schema"], regexes["bad"]) == 4

def test_bad_include_validator():
    exp = ["'a_string' is not an int."]
    paths = ['key1']
    match_exception_lines(include_validator["schema"], include_validator["bad"], exp, paths)

def test_bad_schema():
    with pytest.raises(SyntaxError) as excinfo:
        yamlr.make_schema(get_fixture("bad_schema.yaml"))
    assert "fixtures/bad_schema.yaml" in str(excinfo.value)

def test_empty_schema():
    with pytest.raises(ValueError) as e:
        yamlr.make_schema(get_fixture("empty_schema.yaml"))
    
    assert 'empty_schema.yaml' in e.value.args[0]['path']
    assert e.value.args[0]['error'] == "is an empty file!"

@pytest.mark.parametrize(
    "schema_filename", ["bad_schema_rce.yaml", "bad_schema_rce2.yaml", "bad_schema_rce3.yaml", "bad_schema_rce4.yaml"]
)
def test_vulnerable_schema(schema_filename):
    with pytest.raises(SyntaxError) as excinfo:
        yamlr.make_schema(get_fixture(schema_filename))
    assert schema_filename in str(excinfo.value)

def test_list_is_not_a_map():
    exp = ["[1, 2] is not a map"]
    match_exception_lines(strict_map["schema"], strict_list["good"], exp)

def test_bad_strict_map():
    exp = ["Unexpected element"]
    paths = ['extra']
    match_exception_lines(strict_map["schema"], strict_map["bad"], exp, paths, strict=True)

def test_bad_mixed_strict_map():
    exp = ["Unexpected element"]
    paths = ['field3.extra']
    match_exception_lines(mixed_strict_map["schema"], mixed_strict_map["bad"], exp, paths)

def test_bad_strict_list():
    exp = ["Unexpected element"]
    paths = ['2']
    match_exception_lines(strict_list["schema"], strict_list["bad"], exp, paths, strict=True)

def test_bad_nested_map2():
    exp = ["Required field missing"]
    paths = ['field1.field1_1']
    match_exception_lines(nested_map2["schema"], nested_map2["bad"], exp, paths)

def test_bad_static_list():
    exp = ["Required field missing"]
    paths = ['0']
    match_exception_lines(static_list["schema"], static_list["bad"], exp, paths)

def test_bad_map_key_constraint_base():
    exp = ["Key error - 'bad' is not an int."]
    match_exception_lines(map_key_constraint["schema"], map_key_constraint["bad_base"], exp)

def test_bad_map_key_constraint_nest():
    exp = ["Key error - '100' is not a str."]
    paths = ['1.0']
    match_exception_lines(map_key_constraint["schema"], map_key_constraint["bad_nest"], exp, paths)

def test_bad_map_key_constraint_nest_con():
    exp = [
        "Key error - '100' is not a str.",
        "Key error - 'baz' contains excluded character 'z'",
    ]
    paths = ['1.0', '1.0']
    match_exception_lines(map_key_constraint["schema"], map_key_constraint["bad_nest_con"], exp, paths)

def test_bad_numeric_bool_coercion():
    exp = [
        "'False' is not an int.",
        "'True' is not an int.",
        "'False' is not a num.",
        "'True' is not a num.",
    ]
    paths = ['integers.0', 'integers.1', 'numbers.0', 'numbers.1']
    match_exception_lines(numeric_bool_coercion["schema"], numeric_bool_coercion["bad"], exp, paths)

def test_bad_subset():
    exp = ["'subset' may not be an empty set."]
    paths = ['subset_list']
    match_exception_lines(subset["schema"], subset["bad"], exp, paths)

def test_bad_subset2():
    exp = ["'[1]' is not an int.", "'[1]' is not a str."]
    paths = ['subset_list', 'subset_list']
    match_exception_lines(subset["schema"], subset["bad2"], exp, paths)

def test_bad_subset3():
    exp = ["'{'a': 1}' is not an int.", "'{'a': 1}' is not a str."]
    paths = ['subset_list', 'subset_list']
    match_exception_lines(subset["schema"], subset["bad3"], exp, paths)

def test_nodef_subset_schema():
    with pytest.raises(ValueError) as e:
        schema = yamlr.make_schema(get_fixture(subset_nodef["schema"]), debug=True)
        data = yamlr.make_data(get_fixture(subset_nodef["schema"]))
        yamlr.validate(schema, data)

    assert "subset requires at least one validator!" in str(e.value)

# TODO: new test to verify new error messages
"""
@pytest.mark.parametrize(
    "use_schema_string,use_data_string,expected_message_re",
    [
        (False, False, "^Error validating data '.*?' with schema '.*?'\n\t"),
        (True, False, "^Error validating data '.*?'\n\t"),
        (False, True, "^Error validating data with schema '.*?'\n\t"),
        (True, True, "^Error validating data\n\t"),
    ],
)
def test_validate_errors(use_schema_string, use_data_string, expected_message_re):
    schema_path = get_fixture("types.yaml")
    data_path = get_fixture("types_bad_data.yaml")
    if use_schema_string:
        with io.open(schema_path, encoding="utf-8") as f:
            schema = yamlr.make_schema(content=f.read())
    else:
        schema = yamlr.make_schema(schema_path)
    if use_data_string:
        with io.open(data_path, encoding="utf-8") as f:
            data = yamlr.make_data(content=f.read())
    else:
        data = yamlr.make_data(data_path)
    with pytest.raises(yamlr.YamlrError) as excinfo:
        yamlr.validate(schema, data)
    assert re.match(expected_message_re, excinfo.value.message, re.MULTILINE), "Message {} should match {}".format(
        excinfo.value.message, expected_message_re
    )
"""

def match_exception_lines(schema, data, expected=[], paths=[], strict=False):
    c_sch = yamlr.make_schema(get_fixture(schema), debug=True)
    c_data = yamlr.make_data(get_fixture(data))

    with pytest.raises(ValueError) as e:
        yamlr.validate(c_sch, c_data, strict)

    got = e.value.results[0]['errors']

    if len(expected) > 0:
        result_errors = [x['error'] for x in got]
        result_errors.sort()
        expected.sort()
        assert result_errors == expected
    
    if len(paths) > 0:
        result_paths = [x['path'] for x in got]
        result_paths.sort()
        paths.sort()
        assert result_paths == paths


def count_exception_lines(schema, data, strict=False):
    c_sch = yamlr.make_schema(get_fixture(schema))
    c_data = yamlr.make_data(get_fixture(data))

    with pytest.raises(ValueError) as e:
        yamlr.validate(c_sch, c_data, strict)
    
    print('value: ' + repr(e.value.results))
    result = e.value.results[0]
    return len(result['errors'])
