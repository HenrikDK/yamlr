import re
import ipaddress
from yamale import util

def validate_min(value, constraint, kwargs):
    errors = []
    min = kwargs['min']
    valid = min <= value
    if not valid:
        message = constraint['fail'] % (value, min)
        errors.append(message)
    return errors

def validate_max(value, constraint, kwargs):
    errors = []
    max = kwargs['max']
    valid = max >= value
    if not valid:
        message = constraint['fail'] % (value, max)
        errors.append(message)
    return errors

def validate_length_min(value, constraint, kwargs):
    errors = []
    min = int(kwargs['min'])
    valid = min <= len(value)
    if not valid:
        message = constraint['fail'] % (value, min)
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

def validte_key(value, constraint, kwargs):
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
    'str_char_exclude': {'fail': "'%s' contains excluded character '%s'", 'func': validate_character_exclude, '_type': 'constraint'},
    'ip_version': {'fail': "IP version of %s is not %s", 'func': validate_ip_version, '_type': 'constraint'},
    'key': {'fail': "Key error - %s", 'func': validte_key, '_type': 'constraint'}
}

"""
class Constraint(object):
    keywords = {}  # Keywords and types accepted by this constraint
    is_active = False

    def __init__(self, value_type, kwargs):
        for kwarg, kwtype in self.keywords.items():
            value = self.get_kwarg(kwargs, kwarg, kwtype)
            setattr(self, kwarg, value)

    def get_kwarg(self, kwargs, key, kwtype):
        try:
            value = kwargs[key]
        except KeyError:
            return None

        # Activate this constraint
        self.is_active = True

        if isinstance(value, kwtype):
            # value already correct type, return
            return value

        try:  # Try to convert value
            # Is this value one of the datetime types?
            if kwtype == datetime.date:
                time = datetime.datetime.strptime(value, "%Y-%m-%d")
                return datetime.date(time.year, time.month, time.day)

            if kwtype == datetime.datetime:
                return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

            return kwtype(value)
        except (TypeError, ValueError):
            raise SyntaxError("%s is not a %s" % (key, kwtype))

    def is_valid(self, value):
        if not self.is_active:
            return None

        if not self._is_valid(value):
            return self._fail(value)

        return None

    def _fail(self, value):
        return "'%s' violates %s." % (value, self.__class__.__name__)


class Min(Constraint):
    fail = "%s is less than %s"

    def __init__(self, value_type, kwargs):
        self.keywords = {"min": value_type}
        super(Min, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return self.min <= value

    def _fail(self, value):
        return self.fail % (value, self.min)


class Max(Constraint):
    fail = "%s is greater than %s"

    def __init__(self, value_type, kwargs):
        self.keywords = {"max": value_type}
        super(Max, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return self.max >= value

    def _fail(self, value):
        return self.fail % (value, self.max)


class LengthMin(Constraint):
    keywords = {"min": int}
    fail = "Length of %s is less than %s"

    def _is_valid(self, value):
        return self.min <= len(value)

    def _fail(self, value):
        return self.fail % (value, self.min)


class LengthMax(Constraint):
    keywords = {"max": int}
    fail = "Length of %s is greater than %s"

    def _is_valid(self, value):
        return self.max >= len(value)

    def _fail(self, value):
        return self.fail % (value, self.max)


class StringEquals(Constraint):
    keywords = {"equals": str, "ignore_case": bool}
    fail = "%s does not equal %s"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.equals is not None:
            if self.ignore_case is not None:
                if not self.ignore_case:
                    return value == self.equals
                else:
                    return value.casefold() == self.equals.casefold()
            else:
                return value == self.equals
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self.equals)


class StringStartsWith(Constraint):
    keywords = {"starts_with": str, "ignore_case": bool}
    fail = "%s does not start with %s"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.starts_with is not None:
            if self.ignore_case is not None:
                if not self.ignore_case:
                    return value.startswith(self.starts_with)
                else:
                    length = len(self.starts_with)
                    if length <= len(value):
                        return value[:length].casefold() == self.starts_with.casefold()
                    else:
                        return False
            else:
                return value.startswith(self.starts_with)
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self.starts_with)


class StringEndsWith(Constraint):
    keywords = {"ends_with": str, "ignore_case": bool}
    fail = "%s does not end with %s"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.ends_with is not None:
            if self.ignore_case is not None:
                if not self.ignore_case:
                    return value.endswith(self.ends_with)
                else:
                    length = len(self.ends_with)
                    if length <= len(value):
                        return value[-length:].casefold() == self.ends_with.casefold()
                    else:
                        return False
            else:
                return value.endswith(self.ends_with)
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self.ends_with)


class StringMatches(Constraint):
    keywords = {"matches": str}
    fail = "%s is not a regex match."

    _regex_flags = {"ignore_case": re.I, "multiline": re.M, "dotall": re.S}

    def __init__(self, value_type, kwargs):
        self._flags = 0
        for k, v in util.get_iter(self._regex_flags):
            self._flags |= v if kwargs.pop(k, False) else 0

        super(StringMatches, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        if self.matches is not None:
            regex = re.compile(self.matches, self._flags)
            return regex.match(value)
        else:
            return True

    def _fail(self, value):
        return self.fail % (value)


class CharacterExclude(Constraint):
    keywords = {"exclude": str, "ignore_case": bool}
    fail = "'%s' contains excluded character '%s'"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.exclude is not None:
            for char in self.exclude:
                if self.ignore_case is not None:
                    if not self.ignore_case:
                        if char in value:
                            self._failed_char = char
                            return False
                    else:
                        if char.casefold() in value.casefold():
                            self._failed_char = char
                            return False
                else:
                    if char in value:
                        self._failed_char = char
                        return False
            return True
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self._failed_char)


class IpVersion(Constraint):
    keywords = {"version": int}
    fail = "IP version of %s is not %s"

    def _is_valid(self, value):
        try:
            ip = ipaddress.ip_interface(to_unicode(value))
        except ValueError:
            return False
        return self.version == ip.version

    def _fail(self, value):
        return self.fail % (value, self.version)


class Key(Constraint):
    keywords = {"key": Validator}
    fail = "Key error - %s"

    def _is_valid(self, value):
        for k in value.keys():
            if self.key.validate(k) != []:
                return False
        return True

    def _fail(self, value):
        error_list = []
        for k in value.keys():
            error_list.extend(self.key.validate(k))
        return [self.fail % (e) for e in error_list]

"""