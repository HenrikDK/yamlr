import re
import ipaddress
from datetime import date, datetime
from yamale import util

# ABCs for containers were moved to their own module
try:
    from collections.abc import Sequence, Mapping
except ImportError:
    from collections import Sequence, Mapping

def validate_str(c_sch, value, args = None, kw_args = None):
    valid = util.isstr(value)
    errors = []
    if not valid:
        error = "'%s' is not a str." % (value)
        errors.append(error)
    return errors

def validate_num(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, (int, float)) and not isinstance(value, bool)
    errors = []
    if not valid:
        error = "'%s' is not a num." % (value)
        errors.append(error)
    return errors

def validate_int(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, int) and not isinstance(value, bool)
    errors = []
    if not valid:
        error = "'%s' is not an int." % (value)
        errors.append(error)
    return errors

def validate_bool(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, bool)
    errors = []
    if not valid:
        error = "'%s' is not a bool." % (value)
        errors.append(error)
    return errors

def validate_enum(c_sch, value, args = None, kw_args = None):
    valid = value in args
    errors = []
    if not valid:
        error = "'%s' not in %s." % (value, args)
        errors.append(error)
    return errors

def validate_day(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, date)
    errors = []
    if not valid:
        error = "'%s' is not a valid date (Format: YYYY-MM-DD)." % (value)
        errors.append(error)
    return errors

def validate_timestamp(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, datetime)
    errors = []
    if not valid:
        error = "'%s' is not a valid datetime (Format: YYYY-MM-DD HH:MM:SS)." % (value)
        errors.append(error)
    return errors

def validate_map(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, Mapping)
    errors = []
    if not valid:
        error = "'%s' is not a valid map." % (value)
        errors.append(error)
    return errors

def validate_list(c_sch, value, args = None, kw_args = None):
    valid = isinstance(value, Sequence) and not util.isstr(value)
    errors = []
    if not valid:
        error = "'%s' is not a valid list." % (value)
        errors.append(error)
    return errors

def validate_include(c_sch, value, args = None, kw_args = None):
    return []

def validate_any(c_sch, value, args = None, kw_args = None):
    return []

def validate_subset(c_sch, value, args = None, kw_args = None):
    allow_empty = bool(kw_args.get("allow_empty", False))
    validators = [val for val in args if isinstance(val, dict) and 'name' in val]
    if len(validators) == 0:
        raise ValueError("subset requires at least one validator!")

    print(f'vs - {value}')
    valid = allow_empty or value is not None
    errors = []
    if not valid:
        error = "'subset' may not be an empty set."
        errors.append(error)
    return errors

def validate_null(c_sch, value, args = None, kw_args = None):
    valid = value is None
    errors = []
    if not valid:
        error = "'%s' is not None." % (value)
        errors.append(error)
    return errors

def validate_regex(c_sch, value, args = None, kw_args = None):
    valid = value is None
    regex_name = kw_args.get("name", 'regex match')
    regex_flags = {"ignore_case": re.I, "multiline": re.M, "dotall": re.S}
    flags = 0
    for k, v in util.get_iter(regex_flags):
        flags |= v if kw_args.get(k, False) else 0

    regexes = [re.compile(arg, flags) for arg in args if util.isstr(arg)]

    valid = util.isstr(value) and any(r.match(value) for r in regexes)

    errors = []
    if not valid:
        error = "'%s' is not a %s." % (value, regex_name)        
        errors.append(error)
    return errors

def validate_ip(c_sch, value, args = None, kw_args = None):
    valid = True
    try:
        ipaddress.ip_interface(util.to_unicode(value))
    except ValueError:
        valid = False
    
    errors = []
    if not valid:
        error = "'%s' is not a valid ip." % (value)
        errors.append(error)
    return errors

def validate_mac(c_sch, value, args = None, kw_args = None):
    regexes = [
        re.compile(r"[0-9a-fA-F]{2}([-:]?)[0-9a-fA-F]{2}(\1[0-9a-fA-F]{2}){4}$"),
        re.compile(r"[0-9a-fA-F]{4}([-:]?)[0-9a-fA-F]{4}(\1[0-9a-fA-F]{4})$"),
    ]
    
    valid = util.isstr(value) and any(r.match(value) for r in regexes)
    
    errors = []
    if not valid:
        error = "'%s' is not a valid mac address." % (value)
        errors.append(error)
    return errors

def validate_semver(c_sch, value, args = None, kw_args = None):
    # https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
    regexes = [
        re.compile(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"),
    ]
    
    valid = util.isstr(value) and any(r.match(value) for r in regexes)
    
    errors = []
    if not valid:
        error = "'%s' is not a valid mac address." % (value)
        errors.append(error)
    return errors


default = {
    'str': {'func': validate_str, 'constraints': ['length_min', 'length_max', 'str_exclude', 'str_equals', 'str_starts_with', 'str_ends_with', 'str_matches'], '_type': 'validator'},
    'num': {'func': validate_num, 'constraints': ['min', 'max'], '_type': 'validator'},
    'int': {'func': validate_int, 'constraints': ['min', 'max'], '_type': 'validator'},
    'bool': {'func': validate_bool, 'constraints': [], '_type': 'validator'},
    'enum': {'func': validate_enum, 'constraints': [], '_type': 'validator'},
    'day': {'func': validate_day, 'constraints': ['min', 'max'], '_type': 'validator'},
    'timestamp': {'func': validate_timestamp, 'constraints':['min', 'max'], '_type': 'validator'},
    'map': {'func': validate_map, 'constraints': ['length_min', 'length_max', 'key'], '_type': 'validator'},
    'list': {'func': validate_list, 'constraints': ['length_min', 'length_max'], '_type': 'validator'},
    'include': {'func': validate_include, 'constraints': [], '_type': 'validator'},
    'any': {'func': validate_any, 'constraints': [], '_type': 'validator'},
    'subset': {'func': validate_subset, 'constraints': [], '_type': 'validator'},
    'null': {'func': validate_null, 'constraints': [], '_type': 'validator'},
    'regex': {'func': validate_regex, 'constraints': [], '_type': 'validator'},
    'ip': {'func': validate_ip, 'constraints': ['ip_version'], '_type': 'validator'},
    'mac': {'func': validate_mac, 'constraints': [], '_type': 'validator'},
    'semver': {'func': validate_semver, 'constraints': [], '_type': 'validator'}
}

def validate(c_sch, c_val, value):
    validator_name = c_val['name']
    validator = c_sch['validators'][validator_name]

    args = c_val['args']
    kw_args = c_val['kw_args']
    errors = []
    print(f'vv   - {value} - na - {args} - {kw_args}')

    # Make sure the type validates first.
    errors = validator['func'](c_sch, value, args, kw_args)
    print(f'vv   - {errors}')
    if len(errors) > 0:
        # todo: return line number, and message
        return errors

    # Then validate all the constraints second.
    for c_name in validator['constraints']:
        c_key = c_name
        index = c_name.find('_')
        if index > 0:
            c_key = c_name[index + 1:]
        
        if c_key not in kw_args:
            continue

        constraint = c_sch['constraints'][c_name]

        error = constraint['func'](c_sch, value, args, kw_args)
        if len(error) > 0:
            errors.extend(error)
    
    return errors
