from yamale.validation_results import ValidationResult
from yamale import util
from yamale import validators as val

class FatalValidationError(Exception):
    def __init__(self, error):
        super().__init__()
        self.error = error

# validate schema
def validate(c_sch, data, data_name, strict):
    c_sch['data'] = data
    print(f'V    - state: {c_sch.keys()}')
    path = util.get_path()
    try:
        errors = _validate(c_sch, c_sch['schema'], data, path, strict)
    except FatalValidationError as e:
        errors = [e.error]
    return ValidationResult(data_name, c_sch['name'], errors)

# Validate data with validator, returns an array of errors.
def _validate(c_sch, c_val, data, path, strict):
    print(f"v    - {c_val} - {data}")
    if (util.is_list(c_val) or util.is_map(c_val)) and '_type' not in c_val: # does not work, since we now use dicts for everything
        return _validate_static_map_list(c_sch, c_val, data, path, strict)

    errors = []
    # Optional field with optional value? Who cares.
    is_required = bool(c_val['kw_args'].get("required", True))
    can_be_none = bool(c_val['kw_args'].get("none", True))

    if data is None and not is_required and can_be_none:
        return errors

    errors += _validate_primitive(c_sch, c_val, data, path)

    if errors:
        return errors

    if c_val['name'] == 'include': #isinstance(validator, val.Include)
        errors += _validate_include(c_sch, c_val, data, path, strict)
    
    elif c_val['name'] in ['map', 'list']: #isinstance(validator, (val.Map, val.List))
        errors += _validate_map_list(c_sch, c_val, data, path, strict)

    elif c_val['name'] == 'any': # isinstance(validator, val.Any):
        errors += _validate_any(c_sch, c_val, data, path, strict)

    elif c_val['name'] == 'subset': #isinstance(validator, val.Subset):
        errors += _validate_subset(c_sch, c_val, data, path, strict)

    return errors

# Fetch item from data at the position key and validate with validator. Returns an array of errors.
def _validate_item(c_sch, c_val, data, path, strict, key):
    print(f'vit  - {key} - {c_val}')
    errors = []
    path = util.get_path(path, key)
    try:  # Pull value out of data. Data can be a map or a list/sequence
        data_item = data[key]
    except (KeyError, IndexError):  # Oops, that field didn't exist.
        # Optional? Who cares.
        required = True 
        if 'kw_args' in c_val:
            required = c_val['kw_args'].get('required', True)
        
        if 'name' in c_val and c_val['name'] in val.default and not required:
            return errors
        # SHUT DOWN EVERYTHING
        errors.append("%s: Required field missing" % path)
        return errors

    return _validate(c_sch, c_val, data_item, path, strict)

def _validate_static_map_list(c_sch, c_val, data, path, strict):
    print(f'vsml - {c_val} - {data}')
    if util.is_map(c_val) and not util.is_map(data):
        return ["%s : '%s' is not a map" % (path, data)]

    if util.is_list(c_val) and not util.is_list(data):
        return ["%s : '%s' is not a list" % (path, data)]

    errors = []

    if strict:
        data_keys = set(util.get_keys(data))
        validator_keys = set(util.get_keys(c_val))
        for key in data_keys - validator_keys:
            if key == '_lineno':
                continue
            error_path = util.get_path(path, key)
            errors += ["%s: Unexpected element" % error_path]

    for key, s_val in util.get_iter(c_val):
        errors += _validate_item(c_sch, s_val, data, path, strict, key)
    
    print(f'vsml - errors - {errors}')
    return errors

def _validate_map_list(c_sch, c_val, data, path, strict):
    print(f'vml  - {c_val} - {data}')
    errors = []

    if not c_val['children']:
        return errors  # No validators, user just wanted a map.

    for key in util.get_keys(data):
        if key == '_lineno':
            continue
        sub_errors = []
        for s_val in c_val['children']:
            err = _validate_item(c_sch, s_val, data, path, strict, key)
            if err:
                sub_errors.append(err)

        if len(sub_errors) == len(c_val['children']):
            # All validators failed, add to errors
            for err in sub_errors:
                errors += err

    return errors

def _validate_include(c_sch, c_val, data, path, strict):
    print(f'vinc - {c_val} - {data}')
    include_name = c_val['args'][0]
    include_schema = c_sch['includes'].get(include_name)
    print(repr(include_schema))
    if not include_schema:
        raise FatalValidationError("Include '%s' has not been defined." % c_val.include_name)
    
    return _validate(c_sch, include_schema, data, path, strict)

def _validate_any(c_sch, c_val, data, path, strict):
    print(f'vany - {c_val.keys()} - {data}')
    
    if len(c_val['children']) == 0:
        return []

    errors = []

    validators = _get_include_validators_for_key(c_sch, c_val, data)
    sub_errors = []
    for s_val in validators:
        err = _validate(c_sch, s_val, data, path, strict)
        if err:
            sub_errors.append(err)

    if len(sub_errors) == len(validators):
        # All validators failed, add to errors
        for err in sub_errors:
            errors += err

    return errors

def _validate_subset(c_sch, c_val, data, path, strict):
    print(f'vsub - {c_val.keys()} - {data}')

    def _internal_validate(internal_data):
        validators = _get_include_validators_for_key(c_sch, c_val, internal_data)
        sub_errors = []
        for v in validators:
            err = _validate(v, internal_data, path, strict)
            if not err:
                break
            sub_errors += err
        else:
            return sub_errors
        return []

    if len(c_val['children']) == 0:
        return []

    errors = []
    if util.is_map(data):
        for k, v in data.items():
            errors += _internal_validate({k: v})
    elif util.is_list(data):
        for k in data:
            errors += _internal_validate(k)
    else:
        errors += _internal_validate(data)
    return errors

def _get_include_validators_for_key(c_sch, c_val, internal_data):
    print(f'vfk  - {c_val}')
    key = c_val['kw_args'].get('key', None)

    if not key or key not in internal_data: 
        return c_val['children']
    
    field_value = internal_data[key]
    result = []
    for s_val in c_val['children']:
        if s_val['name'] != 'include':
            continue

        include_name = s_val['args'][0]
        inc_validator = c_sch['includes'].get(include_name)
        if key not in inc_validator:
            continue

        field_validator = inc_validator[key]
        errors = _validate_primitive(c_sch, field_validator, field_value, '')
        if len(errors) == 0:
            result.append(s_val)
    
    return result

def _validate_primitive(c_sch, c_val, data, path):
    print(f'vp   - {c_val} - {data}')
    errors = val.validate(c_sch, c_val, data)

    for i, error in enumerate(errors):
        errors[i] = ("%s: " % path) + error

    return errors
