import yaml, json
from io import StringIO
from yamale import util, parser
from yamale import wak_validators as val

"""
Read yaml file using pyaml.
"""
def _parse_yaml(f):
    try:
        Loader = yaml.CSafeLoader
    except AttributeError:  # System does not have libyaml
        Loader = yaml.SafeLoader
    return list(yaml.load_all(f, Loader=Loader))

def parse_yaml(path=None, content=None):
    if (path is None and content is None) or (path is not None and content is not None):
        raise TypeError("Pass either path= or content=, not both")

    if path is not None:
        with open(path) as f:
            return _parse_yaml(f)
    else:
        return _parse_yaml(StringIO(content))

"""
Go through a schema and map validators.
"""
def process_schema(raw_schema, name="", validators=[], includes={}):
    result = {
        'validators': validators or val.default,
        'raw_schema': raw_schema,
        'name': name,
        'includes': includes
    }

    schemas = json.loads(json.dumps(raw_schema))

    result['schema'] = _process_schema('', schemas[0], validators)

    # Additional documents contain Includes.
    for schema in schemas[1:]:
        _add_include(includes, schema, validators)

    return result


def _add_include(includes, schema, validators):
    for include_name, custom_type in schema.items():
        includes[include_name] = _process_schema(include_name, custom_type, validators)


def _process_schema(path, schema_data, validators):
    if util.is_map(schema_data) or util.is_list(schema_data):
        for key, data in util.get_iter(schema_data):
            sub_path = util.get_path(path, key)
            schema_data[key] = _process_schema(sub_path, data, validators)
    else:
        schema_data = _parse_schema_item(path, schema_data, validators)
    return schema_data


def _parse_schema_item(path, expression, validators):
    try:
        return parser.parse(expression, validators)
    except SyntaxError as e:
        # Tack on some more context and rethrow.
        error = str(e) + " at node '%s'" % str(path)
        raise SyntaxError(error)
