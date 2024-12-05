from yamale import util
from yamale import validators as val

class FatalValidationError(Exception):
    def __init__(self, error):
        super().__init__()
        self.error = error

# validate schema
def validate(c_sch, data, data_name, strict):
    c_sch['log'].append(f"{'s-V':10} - state: {c_sch.keys()}")

    path = util.get_path()
    try:
        errors = _validate(c_sch, c_sch['schema'], data, path, strict, 0)
    except FatalValidationError as e:
        errors = [{'error': e.error, 'path': '', 'lineno': None}]
    result = {'data_name':data_name, 'name': c_sch['name'], 'errors': errors, 'is_valid': len(errors) == 0}
    return result

# Validate data with validator, returns an array of errors.
def _validate(c_sch, c_val, data, path, strict, prev_lineno: None):
    c_sch['log'].append(f"{'s-v':10} - {c_val} - {data}")

    if (util.is_list(c_val) or util.is_map(c_val)) and '_type' not in c_val:
        return _validate_static_map_list(c_sch, c_val, data, path, strict, prev_lineno)

    errors = []
    # Optional field with optional value? Who cares.
    is_required = bool(c_val['kw_args'].get("required", True))
    can_be_none = bool(c_val['kw_args'].get("none", True))

    if data is None and not is_required and can_be_none:
        return errors

    lineno = util.get_lineno(data, prev_lineno)
    errors += _validate_primitive(c_sch, c_val, data, path, lineno)
    c_sch['log'].append(f"{'s-v|e':10} - {errors}")

    if errors:
        return errors

    if c_val['name'] == 'include': #isinstance(validator, val.Include)
        errors += _validate_include(c_sch, c_val, data, path, strict, lineno)
    
    elif c_val['name'] in ['map', 'list']: #isinstance(validator, (val.Map, val.List))
        errors += _validate_map_list(c_sch, c_val, data, path, strict, lineno)

    elif c_val['name'] == 'any': # isinstance(validator, val.Any):
        errors += _validate_any(c_sch, c_val, data, path, strict, lineno)

    elif c_val['name'] == 'subset': #isinstance(validator, val.Subset):
        errors += _validate_subset(c_sch, c_val, data, path, strict, lineno)

    return errors

# Fetch item from data at the position key and validate with validator. Returns an array of errors.
def _validate_item(c_sch, c_val, data, path, strict, key, prev_lineno=None):
    c_sch['log'].append(f"{'s-vit':10} - {c_val} - {data}")

    errors = []
    lineno = util.get_lineno(data, prev_lineno)
    path = util.get_path(path, key)
    try:  # Pull value out of data. Data can be a map or a list/sequence
        data_item = data[key]
    except (KeyError, IndexError):  # Oops, that field didn't exist.
        # Optional? Who cares.
        required = True 
        if 'kw_args' in c_val:
            required = c_val['kw_args'].get('required', True)
            if 'allow_empty' in c_val['kw_args']:
                allow_empty = c_val['kw_args'].get('allow_empty', False)
                required = not allow_empty

        if 'name' in c_val and c_val['name'] in c_sch['validators'] and not required:
            return errors
        # SHUT DOWN EVERYTHING
        errors.append({'path': path, 'error': f"Required field missing", 'lineno': lineno})
        return errors
    
    errors = _validate(c_sch, c_val, data_item, path, strict, lineno)
    c_sch['log'].append(f"{'s-vit|e':10} - {errors}")
    return errors

def _validate_static_map_list(c_sch, c_val, data, path, strict, prev_lineno=None):
    c_sch['log'].append(f"{'s-vsml':10} - {c_val} - {data} - {strict}")
    
    if util.is_map(c_val) and not util.is_map(data):
        return [{'error': f"{data}: is not a map", 'path': path, 'lineno': None}]

    if util.is_list(c_val) and not util.is_list(data):
        return [{'error': f"{data}: is not a list", 'path': path, 'lineno': None}]

    errors = []
    lineno = util.get_lineno(data, prev_lineno)
    if strict:
        data_keys = set(util.get_keys(data))
        validator_keys = set(util.get_keys(c_val))
        diff_keys = data_keys - validator_keys
        for key in diff_keys:
            if key == '_lineno':
                continue
            error_path = util.get_path(path, key)

            errors += [{'error': f'Unexpected element', 'path': error_path, 'lineno': lineno}]

    for key, s_val in util.get_iter(c_val):
        errors += _validate_item(c_sch, s_val, data, path, strict, key, lineno)
    
    c_sch['log'].append(f"{'s-vsml|e':10} - {errors}")
    return errors
        
def _validate_map_list(c_sch, c_val, data, path, strict, prev_lineno=None):
    c_sch['log'].append(f"{'s-vml':10} - {c_val} - {data}")
    errors = []

    if not c_val['children']:
        return errors # No validators, user just wanted a map.
    
    lineno = util.get_lineno(data, prev_lineno)
    for key in util.get_keys(data):
        if key == '_lineno':
            continue

        sub_errors = []
        for s_val in c_val['children']:
            err = _validate_item(c_sch, s_val, data, path, strict, key, lineno)
            if len(err) > 0:
                sub_errors.extend(err)

        if len(sub_errors) >= len(c_val['children']): # All validators failed, add to errors
            errors.extend(sub_errors)

    c_sch['log'].append(f"{'s-vml|e':10} - {errors}")
    return errors

def _validate_include(c_sch, c_val, data, path, strict, prev_lineno=None):
    c_sch['log'].append(f"{'s-vinc':10} - {c_val} - {data}")
    
    strict = c_val['kw_args'].get('strict', True)
    include_name = c_val['args'][0]
    include_schema = c_sch['includes'].get(include_name)
    lineno = util.get_lineno(data, prev_lineno)
    if not include_schema:
        raise FatalValidationError("Include '%s' has not been defined." % include_name)
    
    c_sch['log'].append(f"{'s-vinc|s':10} - {include_name} - {include_schema}")
    return _validate(c_sch, include_schema, data, path, strict, lineno)

def _validate_any(c_sch, c_val, data, path, strict, prev_lineno=None):
    c_sch['log'].append(f"{'s-vany':10} - {c_val} - {data}")
    
    if len(c_val['children']) == 0:
        return []

    lineno = util.get_lineno(data, prev_lineno)
    errors = []
    validators = _get_include_validators_for_key(c_sch, c_val, data)
    sub_errors = []
    for s_val in validators:
        err = _validate(c_sch, s_val, data, path, strict, lineno)
        if err:
            sub_errors.append(err)

    if len(sub_errors) == len(validators):
        # All validators failed, add to errors
        for err in sub_errors:
            errors += err

    c_sch['log'].append(f"{'s-vany|e':10} - {errors}")
    return errors

def _validate_subset(c_sch, c_val, data, path, strict, prev_lineno=None):
    c_sch['log'].append(f"{'s-vsub':10} - {c_val} - {data}")

    def _internal_validate(internal_data):
        allow_empty = bool(c_val['kw_args'].get("allow_empty", False))
        if allow_empty and data is None:
            return []

        lineno = util.get_lineno(data, prev_lineno)
        validators = _get_include_validators_for_key(c_sch, c_val, internal_data, lineno)
        sub_errors = []
        for s_val in validators:
            err = _validate(c_sch, s_val, internal_data, path, strict, lineno)
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
            if k == '_lineno':
                continue
            errors += _internal_validate({k: v})
    elif util.is_list(data):
        for k in data:
            errors += _internal_validate(k)
    else:
        errors += _internal_validate(data)
    
    c_sch['log'].append(f"{'s-vsub|e':10} - {errors}")
    return errors

def _get_include_validators_for_key(c_sch, c_val, internal_data, prev_lineno=None):
    c_sch['log'].append(f"{'s-givfk':10} - {c_val} - {internal_data}")

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
        lineno = util.get_lineno(field_value, prev_lineno)
        errors = _validate_primitive(c_sch, field_validator, field_value, '', lineno)
        if len(errors) == 0:
            result.append(s_val)
    
    c_sch['log'].append(f"{'s-givfk|r':10} - {result}")
    return result

def _validate_primitive(c_sch, c_val, data, path, prev_lineno):
    c_sch['log'].append(f"{'s-vp':10} - {c_val} - {data}")

    lineno = util.get_lineno(data, prev_lineno)
    errors = val.validate(c_sch, c_val, data)
    errors = [{'error': e, 'path': path, 'lineno': lineno} for e in errors]

    c_sch['log'].append(f"{'s-vp|e':10} - {errors}")
    return errors
