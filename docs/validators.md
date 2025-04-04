# Validators
Here are all the validators Yamlr knows about. Every validator takes a `required` keyword telling
Yamlr whether or not that node must exist. By default every node is required. Example: `str(required=False)`

You can also require that an optional value is not `None` by using the `none` keyword. By default
Yamlr will accept `None` as a valid value for a key that's not required. Reject `None` values
with `none=False` in any validator. Example: `str(required=False, none=False)`.

Some validators take keywords and some take arguments, some take both. For instance the `enum()`
validator takes one or more constants as arguments and the `required` keyword:
`enum('a string', 1, False, required=False)`

### String - `str(min=int, max=int, equals=string, starts_with=string, ends_with=string, matches=regex, exclude=string, ignore_case=False, multiline=False, dotall=False)`
Validates strings.
- keywords
    - `min`: len(string) >= min
    - `max`: len(string) <= max
    - `equals`: string == value (add `ignore_case=True` for case-insensitive checking)
    - `starts_with`: Accepts only strings starting with given value (add `ignore_case=True` for
      case-insensitive checking)
    - `matches`: Validates the string against a given regex. Similar to the `regex()` validator,
      you can use `ignore_case`, `multiline` and `dotall`)
    - `ends_with`: Accepts only strings ending with given value (add `ignore_case=True` for case-insensitive checking)
    - `exclude`: Rejects strings that contains any character in the excluded value
    - `ignore_case`: Validates strings in a case-insensitive manner.
    - `multiline`: `^` and `$` in a pattern match at the beginning and end of each line in a string
       in addition to matching at the beginning and end of the entire string. (A pattern matches
       at [the beginning of a string](https://docs.python.org/3/library/re.html#re.match) even in
       multiline mode; see below for a workaround.); only allowed in conjunction with a `matches` keyword.
    - `dotall`: `.` in a pattern matches newline characters in a validated string in addition to
      matching every character that *isn't* a newline.; only allowed in conjunction with a `matches` keyword.

Examples:
- `str(max=10, exclude='?!')`: Allows only strings less than 11 characters that don't contain `?` or `!`.

### Regex - `regex([patterns], name=string, ignore_case=False, multiline=False, dotall=False)`
Validates strings against one or more regular expressions.
- arguments: one or more Python regular expression patterns
- keywords:
    - `name`: A friendly description for the patterns.
    - `ignore_case`: Validates strings in a case-insensitive manner.
    - `multiline`: `^` and `$` in a pattern match at the beginning and end of each line in a string
       in addition to matching at the beginning and end of the entire string. (A pattern matches
       at [the beginning of a string](https://docs.python.org/3/library/re.html#re.match) even in
       multiline mode; see below for a workaround.)
    - `dotall`: `.` in a pattern matches newline characters in a validated string in addition to
      matching every character that *isn't* a newline.

Examples:
- `regex('^[^?!]{,10}$')`: Allows only strings less than 11 characters that don't contain `?` or `!`.
- `regex(r'^(\d+)(\s\1)+$', name='repeated natural')`: Allows only strings that contain two or
  more identical digit sequences, each separated by a whitespace character. Non-matching strings
  like `sugar` are rejected with a message like `'sugar' is not a repeated natural.`
- `regex('.*^apples$', multiline=True, dotall=True)`: Allows the string `apples` as well
  as multiline strings that contain the line `apples`.

### Integer - `int(min=int, max=int)`
Validates integers.
- keywords
    - `min`: int >= min
    - `max`: int <= max

### Number - `num(min=float, max=float)`
Validates integers and floats.
- keywords
    - `min`: num >= min
    - `max`: num <= max

### Boolean - `bool()`
Validates booleans.

### Null - `null()`
Validates null values.

### Enum - `enum([primitives])`
Validates from a list of constants.
- arguments: constants to test equality with

Examples:
- `enum('a string', 1, False)`: a value can be either `'a string'`, `1` or `False`

### Day - `day(min=date, max=date)`
Validates a date in the form of YYYY-MM-DD.
- keywords
    - `min`: date >= min
    - `max`: date <= max

Examples:
- `day(min='2001-01-01', max='2100-01-01')`: Only allows dates between 2001-01-01 and 2100-01-01.

### Timestamp - `timestamp(min=time, max=time)`
Validates a timestamp in the form of YYYY-MM-DD HH:MM:SS.
- keywords
    - `min`: time >= min
    - `max`: time <= max

Examples:
- `timestamp(min='2001-01-01 01:00:00', max='2100-01-01 23:00:00')`: Only allows times between
  2001-01-01 01:00:00 and 2100-01-01 23:00:00.

### List - `list([validators], min=int, max=int)`
Validates lists. If one or more validators are passed to `list()` only nodes that pass at
least one of those validators will be accepted.

- arguments: one or more validators to test values with
- keywords
    - `min`: len(list) >= min
    - `max`: len(list) <= max

Examples:
- `list()`: Validates any list
- `list(include('custom'), int(), min=4)`: Only validates lists that contain the `custom` include
  or integers and contains a minimum of 4 items.

### Map - `map([validators], key=validator, min=int, max=int)`
Validates maps. Use when you want a node to contain freeform data. Similar to `List`, `Map` takes
one or more validators to run against the values of its nodes, and only nodes that pass at least
one of those validators will be accepted. By default, only the values of nodes are validated and
the keys aren't checked.
- arguments: one or more validators to test values with
- keywords
    - `key`: A validator for the keys of the map.
    - `min`: len(map) >= min
    - `max`: len(map) <= max

Examples:
- `map()`: Validates any map
- `map(str(), int())`: Only validates maps whose values are strings or integers.
- `map(str(), key=int())`: Only validates maps whose keys are integers and values are strings. `1: one` would be valid but `'1': one` would not.
- `map(str(), min=1)`: Only validates a non-empty map.

### IP Address - `ip()`
Validates IPv4 and IPv6 addresses.

- keywords
    - `version`: 4 or 6; explicitly force IPv4 or IPv6 validation

Examples:
- `ip()`: Allows any valid IPv4 or IPv6 address
- `ip(version=4)`: Allows any valid IPv4 address
- `ip(version=6)`: Allows any valid IPv6 address

### MAC Address - `mac()`
Validates MAC addresses.

Examples:
- `mac()`: Allows any valid MAC address

### SemVer (Semantic Versioning) - `semver()`
Validates [Semantic Versioning](https://semver.org/) strings.

Examples:
- `semver()`: Allows any valid SemVer string

### Any - `any([validators], key='field_name')`
Validates against a union of types. Use when a node **must** contain **one and only one** of several types. It is valid
if at least one of the listed validators is valid. If no validators are given, accept any value.
- arguments: validators to test values with (if none is given, allow any value; if one or more are given,
one must be present)

- keywords:
    - `key`: Used to limit the validation of includes, the any validator will check if the specified field matches whats specified by each include validator before running the validator. 

Examples:
- `any(int(), null())`: Validates either an integer **or** a null value.
- `any(num(), include('vector'))`: Validates **either** a number **or** an included 'vector' type.
- `any(str(min=3, max=3),str(min=5, max=5),str(min=7, max=7))`: validates to a string that is exactly 3, 5, or 7 characters long
- `any()`: Allows any value.

### Subset - `subset([validators], allow_empty=False, key='field_name')`
Validates against a subset of types. Unlike the `Any` validator, this validators allows **one or more** of several types.
As such, it *automatically validates against a list*. It is valid if all values can be validated against at least one
validator.
- arguments: validators to test with (at least one; if none is given, a `ValueError` exception will be raised)
- keywords:
    - `allow_empty`: Allow the subset to be empty (and is, therefore, also optional). This overrides the `required`
    - `key`: Limits the validation of includes, the subset validator will check if the specified field matches whats specified by each include validator before running the validator. 
flag.

Examples:
- `subset(int(), str())`: Validators against an integer, a string, or a list of either.
- `subset(int(), str(), allow_empty=True)`: Same as above, but allows the empty set and makes the subset optional.

### Include - `include(include_name)`
Validates included structures. Must supply the name of a valid include.
- arguments: single name of a defined include, surrounded by quotes.

Examples:
- `include('person')`

### Custom validators
It is also possible to add your own custom validators. This is an advanced topic, but here is an
example of adding a `Date` validator and using it in a schema as `date()`

```python
import yamlr
import datetime
from yamlr import validators as val

""" Custom Date validator """
def validate_date(c_sch, c_val, value):
     
    valid = isinstance(value, datetime.date)
    errors = []
    if not valid:
        error = "'%s' is not a valid date." % (value)
        errors.append(error)
    return errors

validators = val.default.copy() # This is a dictionary
validators['date'] = {'func': validate_date, 'constraints': [], '_type': 'validator'}

schema = yamlr.make_schema('./schema.yaml', validators=validators)
# Then use `schema` as normal
```

Examples
--------

### Using keywords
#### Schema:
```yaml
optional: str(required=False)
optional_min: int(min=1, required=False)
min: num(min=1.5)
max: int(max=100)
```
#### Valid Data:
```yaml
optional_min: 10
min: 1.6
max: 100
```

### Includes and recursion
#### Schema:
```yaml
customerA: include('customer')
customerB: include('customer')
recursion: include('recurse')
---
customer:
    name: str()
    age: int()
    custom: include('custom_type')

custom_type:
    integer: int()

recurse:
    level: int()
    again: include('recurse', required=False)
```
#### Valid Data:
```yaml
customerA:
    name: bob
    age: 900
    custom:
        integer: 1
customerB:
    name: jill
    age: 1
    custom:
        integer: 3
recursion:
    level: 1
    again:
        level: 2
        again:
            level: 3
            again:
                level: 4
```

### Lists
#### Schema:
```yaml
list_with_two_types: list(str(), include('variant'))
questions: list(include('question'))
---
variant:
  rsid: str()
  name: str()

question:
  choices: list(include('choices'))
  questions: list(include('question'), required=False)

choices:
  id: str()
```
#### Valid Data:
```yaml
list_with_two_types:
  - 'some'
  - rsid: 'rs123'
    name: 'some SNP'
  - 'thing'
  - rsid: 'rs312'
    name: 'another SNP'
questions:
  - choices:
      - id: 'id_str'
      - id: 'id_str1'
    questions:
      - choices:
        - id: 'id_str'
        - id: 'id_str1'
```

### The data is a list of items without a keyword at the top level
#### Schema:
```yaml
list(include('human'), min=2, max=2)

---
human:
  name: str()
  age: int(max=200)
  height: num()
  awesome: bool()
```
#### Valid Data:
```yaml
- name: Bill
  age: 26
  height: 6.2
  awesome: True

- name: Adrian
  age: 23
  height: 6.3
  awesome: True
```

