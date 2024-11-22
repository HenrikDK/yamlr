import yaml
from io import StringIO
from yamale import util, parser
from yamale.validators import validators as val

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
def process_schema(schema_dict, name="", validators=[], includes={}):
    result = {
        'validators': validators or val.DefaultValidators,
        'schema_data': schema_dict,
        'name': name,
        'includes': includes
    }

    result['schema'] = _process_schema('', schema_dict, validators)

    # if this schema is included it shares the includes with the top level
    # schema
    return result


def _add_include(self, type_dict):
    for include_name, custom_type in type_dict.items():
        t = Schema(custom_type, name=include_name, validators=self.validators, includes=self.includes)
        self.includes[include_name] = t


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
