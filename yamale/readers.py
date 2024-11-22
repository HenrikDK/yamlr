from io import StringIO
import yaml

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
