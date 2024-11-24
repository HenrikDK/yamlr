import re
import ipaddress
from datetime import date, datetime
from yamale import constraints as con
from yamale import util

# ABCs for containers were moved to their own module
try:
    from collections.abc import Sequence, Mapping
except ImportError:
    from collections import Sequence, Mapping

def validate_str(current_value, all_values, args = None, kw_args = None):
    valid = util.isstr(current_value)
    errors = []
    if not valid:
        error = "'%s' is not a string" % (current_value)
        errors.append(error)
    return errors

def validate_num(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, (int, float)) and not isinstance(current_value, bool)
    errors = []
    if not valid:
        error = "'%s' is not an int or float" % (current_value)
        errors.append(error)
    return errors

def validate_int(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, int) and not isinstance(current_value, bool)
    errors = []
    if not valid:
        error = "'%s' is not an int" % (current_value)
        errors.append(error)
    return errors

def validate_bool(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, bool)
    errors = []
    if not valid:
        error = "'%s' is not a bool" % (current_value)
        errors.append(error)
    return errors

def validate_enum(current_value, all_values, args = None, kw_args = None):
    valid = current_value in args
    errors = []
    if not valid:
        error = "'%s' not in %s" % (current_value, args)
        errors.append(error)
    return errors

def validate_day(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, date)
    errors = []
    if not valid:
        error = "'%s' is not a valid date (Format: YYYY-MM-DD)" % (current_value)
        errors.append(error)
    return errors

def validate_timestamp(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, datetime)
    errors = []
    if not valid:
        error = "'%s' is not a valid datetime (Format: YYYY-MM-DD HH:MM:SS)" % (current_value)
        errors.append(error)
    return errors

def validate_map(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, Mapping)
    errors = []
    if not valid:
        error = "'%s' is not a valid map" % (current_value)
        errors.append(error)
    return errors

    #key = kw_args.get('key', None)    
    #validators = [val for val in args if 'name' in val and isinstance(val, dict)]

def validate_list(current_value, all_values, args = None, kw_args = None):
    valid = isinstance(current_value, Sequence) and not util.isstr(current_value)
    errors = []
    if not valid:
        error = "'%s' is not a valid list" % (current_value)
        errors.append(error)
    return errors

def validate_include(current_value, all_values, args = None, kw_args = None):
    return []

def validate_any(current_value, all_values, args = None, kw_args = None):
    return []

def validate_subset(current_value, all_values, args = None, kw_args = None):
    allow_empty = bool(kw_args.get("allow_empty", False))
    validators = [val for val in args if isinstance(val, dict) and 'name' in val]
    if len(validators) == 0:
        raise ValueError("subset requires at least one validator!")

    valid = allow_empty or current_value is not None
    errors = []
    if not valid:
        error = "subset may not be an empty set."
        errors.append(error)
    return errors

def validate_null(current_value, all_values, args = None, kw_args = None):
    valid = current_value is None
    errors = []
    if not valid:
        error = "'%s' is not None" % (current_value)
        errors.append(error)
    return errors

def validate_regex(current_value, all_values, args = None, kw_args = None):
    valid = current_value is None
    regex_name = kw_args.get("name", 'any regex')
    regex_flags = {"ignore_case": re.I, "multiline": re.M, "dotall": re.S}
    flags = 0
    for k, v in util.get_iter(regex_flags):
        flags |= v if kw_args.get(k, False) else 0

    regexes = [re.compile(arg, flags) for arg in args if util.isstr(arg)]

    valid = util.isstr(current_value) and any(r.match(current_value) for r in regexes)

    errors = []
    if not valid:
        error = "'%s' did not match %s" % (current_value, regex_name)
        errors.append(error)
    return errors

def validate_ip(current_value, all_values, args = None, kw_args = None):
    valid = True
    try:
        ipaddress.ip_interface(util.to_unicode(current_value))
    except ValueError:
        valid = False
    
    errors = []
    if not valid:
        error = "'%s' is not a valid ip" % (current_value)
        errors.append(error)
    return errors

def validate_mac(current_value, all_values, args = None, kw_args = None):
    regexes = [
        re.compile(r"[0-9a-fA-F]{2}([-:]?)[0-9a-fA-F]{2}(\1[0-9a-fA-F]{2}){4}$"),
        re.compile(r"[0-9a-fA-F]{4}([-:]?)[0-9a-fA-F]{4}(\1[0-9a-fA-F]{4})$"),
    ]
    
    valid = util.isstr(current_value) and any(r.match(current_value) for r in regexes)
    
    errors = []
    if not valid:
        error = "'%s' is not a valid mac address" % (current_value)
        errors.append(error)
    return errors

def validate_semver(current_value, all_values, args = None, kw_args = None):
    regexes = [
        # https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
        re.compile(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"),
    ]
    
    valid = util.isstr(current_value) and any(r.match(current_value) for r in regexes)
    
    errors = []
    if not valid:
        error = "'%s' is not a valid mac address" % (current_value)
        errors.append(error)
    return errors


default = {
    'str': {'func': validate_str, 'constraints': ['length_min', 'length_max', 'str_char_exclude', 'str_equals', 'str_starts_with', 'str_ends_with', 'str_matches'] },
    'num': {'func': validate_num, 'constraints': ['min', 'max'] },
    'int': {'func': validate_int, 'constraints': ['min', 'max'] },
    'bool': {'func': validate_bool, 'constraints': [] },
    'enum': {'func': validate_bool, 'constraints': [] },
    'day': {'func': validate_day, 'constraints': ['min', 'max']},
    'timestamp': {'func': validate_timestamp, 'constraints':['min', 'max']},
    'map': {'func': validate_map, 'constraints': ['length_min', 'length_max', 'key']},
    'list': {'func': validate_list, 'constraints': ['length_min', 'length_max']},
    'include': {'func': validate_include, 'constraints': []},
    'any': {'func': validate_any, 'constraints': []},
    'subset': {'func': validate_subset, 'constraints': []},
    'null': {'func': validate_null, 'constraints': []},
    'regex': {'func': validate_regex, 'constraints': []},
    'ip': {'func': validate_ip, 'constraints': ['ip_version']},
    'mac': {'func': validate_mac, 'constraints': []},
    'semver': {'func': validate_semver, 'constraints': []}
}

def validate(validator, value, all_values, args, kw_args):
    errors = []

    # Make sure the type validates first.
    errors = validator['func'](value, all_values, args, kw_args)
    if len(errors) > 0:
        # todo: return line number, and message
        return errors

    constraints_inst = _create_constraints(validator['constraints'], validator['value_type'], validator['kw_args'])
    # Then validate all the constraints second.
    for constraint in constraints_inst:
        error = constraint.is_valid(value)
        if error:
            if isinstance(error, list):
                errors.extend(error)
            else:
                errors.append(error)

    return errors

def _create_constraints(constraint_classes, value_type, kwargs):
    constraints = []
    for constraint in constraint_classes:
        constraints.append(constraint(value_type, kwargs))
    return constraints
