from yamale import schema, readers

class YamaleError(ValueError):
    def __init__(self, results):
        super(YamaleError, self).__init__("\n".join([str(x) for x in list(filter(lambda x: not x.isValid(), results))]))
        self.message = self.args[0]
        self.results = results


def make_schema(path=None, validators=None, content=None, constraints=None):
    # validators = None means use default.
    raw_schema = readers.parse_yaml(path=path, content=content, type='schema')
    if not raw_schema:
        raise ValueError("{} is an empty file!".format(path))

    # First document is the base schema
    try:
        s = readers.process_schema(raw_schema, path, validators=validators, constraints=constraints)
    except (TypeError, SyntaxError) as e:
        error = "Schema error in file %s\n" % path
        error += str(e)
        raise SyntaxError(error)

    return s


def make_data(path=None, content=None):
    raw_data = readers.parse_yaml(path, content, type='data')
    if len(raw_data) == 0:
        return [({}, path)]
    return [(d, path) for d in raw_data]


def validate(c_sch, data, strict=True, _raise_error=True):
    results = []
    is_valid = True
    for d, path in data:
        result = schema.validate(c_sch, d, path, strict)
        results.append(result)
        is_valid = is_valid and result.isValid()
    if _raise_error and not is_valid:
        raise YamaleError(results)
    return results
