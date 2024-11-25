import re
import json
import ipaddress
from datetime import date, datetime
from yamale import util
from yamale import validators as val

def validate_min(c_sch, value, args, kwargs):
    errors = []
    min = kwargs['min']

    if isinstance(value, datetime):
        min = util.convert_to_datetime(min)
    elif isinstance(value, date):
        min = util.convert_to_date(min)

    valid = min <= value
    if not valid:
        message = "%s is less than %s" % (value, min)
        errors.append(message)
    return errors

def validate_max(c_sch, value, args, kwargs):
    errors = []
    max = kwargs['max']

    if isinstance(value, datetime):
        max = util.convert_to_datetime(max)
    elif isinstance(value, date):
        max = util.convert_to_date(max)

    valid = max >= value
    if not valid:
        message = "%s is greater than %s" % (value, max)
        errors.append(message)
    return errors

def validate_length_min(c_sch, value, args, kwargs):
    errors = []
    min = int(kwargs['min'])
    c_value = value
    if isinstance(value, dict):
        c_value = json.loads(json.dumps(value))
        c_value.pop('_lineno', None)

    valid = min <= len(c_value)
    if not valid:
        message = "Length of %s is less than %s" % (c_value, min)
        errors.append(message)
    return errors

def validate_length_max(c_sch, value, args, kwargs):
    errors = []
    max = int(kwargs['max'])
    valid = max >= len(value)
    if not valid:
        message = "Length of %s is greater than %s" % (value, max)
        errors.append(message)
    return errors

def validate_str_equals(c_sch, value, args, kwargs):
    errors = []
    ignore_case = bool(kwargs.get('ignore_case', False))
    equals = str(kwargs['equals'])
    
    valid = True
    if not ignore_case:
        valid = value == equals
    else:
        valid = value.casefold() == equals.casefold()
    
    if not valid:
        message = "%s does not equal %s" % (value, min)
        errors.append(message)
    
    return errors

def validate_str_starts_with(c_sch, value, args, kwargs):
    errors = []
    ignore_case = bool(kwargs.get('ignore_case', False))
    starts_with = str(kwargs['starts_with'])

    valid = True
    if not ignore_case:
        valid = value.startswith(starts_with)
    else:
        length = len(starts_with)
        if length <= len(value):
            valid = value[:length].casefold() == starts_with.casefold()
        else:
            valid = False

    if not valid:
        message = "%s does not start with %s" % (value, min)
        errors.append(message)
    
    return errors

def validate_str_ends_with(c_sch, value, args, kwargs):
    errors = []
    ignore_case = bool(kwargs.get('ignore_case', False))
    ends_with = str(kwargs['ends_with'])

    valid = True
    if not ignore_case:
        valid = value.endswith(ends_with)
    else:
        length = len(ends_with)
        if length <= len(value):
            valid = value[-length:].casefold() == ends_with.casefold()
        else:
            valid = False
    
    if not valid:
        message = "%s does not end with %s" % (value, min)
        errors.append(message)
    
    return errors

def validate_str_matches(c_sch, value, args, kwargs):
    errors = []
    matches = str(kwargs['matches'])
    regex_flags = {"ignore_case": re.I, "multiline": re.M, "dotall": re.S}
    
    flags = 0
    for k, v in util.get_iter(regex_flags):
        flags |= v if kwargs.get(k, False) else 0

    valid = True
    if matches is not None:
        regex = re.compile(matches, flags)
        valid = regex.match(value)

    if not valid:
        message = "%s does not match regex '%s'" % (value, matches)
        errors.append(message)
    
    return errors

def validate_character_exclude(c_sch, value, args, kwargs):
    errors = []
    ignore_case = kwargs.get('ignore_case', False)
    exclude = str(kwargs['exclude'])

    valid = True
    failed_char = []
    for char in exclude:
        if ignore_case:
            char = char.casefold()
            value = value.casefold()

        if char in value:
            failed_char.append(char)
            valid = False

    if not valid:
        message = "'%s' contains excluded character '%s'" % (value, failed_char)
        errors.append(message)
    
    return errors

def validate_ip_version(c_sch, value, args, kwargs):
    errors = []
    version = int(kwargs['version'])
    
    valid = True
    try:
        ip = ipaddress.ip_interface(util.to_unicode(value))
        valid = version == ip.version
    except ValueError:
        valid = False
    
    if not valid:
        message = "IP version of %s is not %s" % (value, version)
        errors.append(message)
    
    return errors

def validate_key(c_sch, value, args, kw_args):
    errors = []
    key = kw_args['key']

    valid = True
    error_list = []
    for k in value.keys():
        if k == '_lineno':
            continue
        print(k)
        val_err = val.validate(c_sch, key, k)
        if val_err != []:
            error_list.extend(val_err)
            valid = False

    if not valid:
        errors = ["Key error - %s" % (e) for e in error_list]
    
    return errors

default = {
    'min': {'func': validate_min, '_type': 'constraint'},
    'max': {'func': validate_max, '_type': 'constraint'},
    'length_min': {'func': validate_length_min, '_type': 'constraint'},
    'length_max': {'func': validate_length_max, '_type': 'constraint'},
    'str_equals': {'func': validate_str_equals, '_type': 'constraint'},
    'str_starts_with': {'func': validate_str_starts_with, '_type': 'constraint'},
    'str_ends_with': {'func': validate_str_ends_with, '_type': 'constraint'},
    'str_matches': {'func': validate_str_matches, '_type': 'constraint'},
    'str_exclude': {'func': validate_character_exclude, '_type': 'constraint'},
    'ip_version': {'func': validate_ip_version, '_type': 'constraint'},
    'key': {'func': validate_key, '_type': 'constraint'}
}
