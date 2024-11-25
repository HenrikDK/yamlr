import re
import json
import ipaddress
from datetime import date, datetime
from yamale import util

def validate_min(value, constraint, kwargs):
    errors = []
    min = kwargs['min']

    if isinstance(value, datetime):
        min = util.convert_to_datetime(min)
    elif isinstance(value, date):
        min = util.convert_to_date(min)

    valid = min <= value
    if not valid:
        message = constraint['fail'] % (value, min)
        errors.append(message)
    return errors

def validate_max(value, constraint, kwargs):
    errors = []
    max = kwargs['max']

    if isinstance(value, datetime):
        max = util.convert_to_datetime(max)
    elif isinstance(value, date):
        max = util.convert_to_date(max)

    valid = max >= value
    if not valid:
        message = constraint['fail'] % (value, max)
        errors.append(message)
    return errors

def validate_length_min(value, constraint, kwargs):
    errors = []
    min = int(kwargs['min'])
    c_value = value
    if isinstance(value, dict):
        c_value = json.loads(json.dumps(value))
        c_value.pop('_lineno', None)

    valid = min <= len(c_value)
    if not valid:
        message = constraint['fail'] % (c_value, min)
        errors.append(message)
    return errors

def validate_length_max(value, constraint, kwargs):
    errors = []
    max = int(kwargs['max'])
    valid = max >= len(value)
    if not valid:
        message = constraint['fail'] % (value, max)
        errors.append(message)
    return errors

def validate_str_equals(value, constraint, kwargs):
    errors = []
    ignore_case = bool(kwargs.get('ignore_case', False))
    equals = str(kwargs['equals'])
    
    valid = True
    if not ignore_case:
        valid = value == equals
    else:
        valid = value.casefold() == equals.casefold()
    
    if not valid:
        message = constraint['fail'] % (value, min)
        errors.append(message)
    
    return errors

def validate_str_starts_with(value, constraint, kwargs):
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
        message = constraint['fail'] % (value, min)
        errors.append(message)
    
    return errors

def validate_str_ends_with(value, constraint, kwargs):
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
        message = constraint['fail'] % (value, min)
        errors.append(message)
    
    return errors

def validate_str_matches(value, constraint, kwargs):
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
        message = constraint['fail'] % (value, matches)
        errors.append(message)
    
    return errors

def validate_character_exclude(value, constraint, kwargs):
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
        message = constraint['fail'] % (value, failed_char)
        errors.append(message)
    
    return errors

def validate_ip_version(value, constraint, kwargs):
    errors = []
    version = int(kwargs['version'])
    
    valid = True
    try:
        ip = ipaddress.ip_interface(util.to_unicode(value))
        valid = version == ip.version
    except ValueError:
        valid = False
    
    if not valid:
        message = constraint['fail'] % (value, version)
        errors.append(message)
    
    return errors

def validate_key(value, constraint, kwargs):
    errors = []
    key = kwargs['key']

    valid = True
    error_list = []
    for k in value.keys():
        val_err = key.validate(k)
        if val_err != []:
            error_list.extend(val_err)
            valid = False

    if not valid:
        errors = [constraint['fail'] % (e) for e in error_list]
    
    return errors

constraints = {
    'min': {'fail': "%s is less than %s", 'func': validate_min, '_type': 'constraint'},
    'max': {'fail': "%s is greater than %s", 'func': validate_max, '_type': 'constraint'},
    'length_min': {'fail': "Length of %s is less than %s", 'func': validate_length_min, '_type': 'constraint'},
    'length_max': {'fail': "Length of %s is greater than %s", 'func': validate_length_max, '_type': 'constraint'},
    'str_equals': {'fail': "%s does not equal %s", 'func': validate_str_equals, '_type': 'constraint'},
    'str_starts_with': {'fail': "%s does not start with %s", 'func': validate_str_starts_with, '_type': 'constraint'},
    'str_ends_with': {'fail': "%s does not end with %s", 'func': validate_str_ends_with, '_type': 'constraint'},
    'str_matches': {'fail': "%s does not match regex '%s'", 'func': validate_str_matches, '_type': 'constraint'},
    'str_exclude': {'fail': "'%s' contains excluded character '%s'", 'func': validate_character_exclude, '_type': 'constraint'},
    'ip_version': {'fail': "IP version of %s is not %s", 'func': validate_ip_version, '_type': 'constraint'},
    'key': {'fail': "Key error - %s", 'func': validate_key, '_type': 'constraint'}
}
