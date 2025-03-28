# Yamlr - Fork and refactor of Yamale (ya·ma·lē)
[![CI Build](https://github.com/HenrikDK/yamlr/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/HenrikDK/yamlr/actions/workflows/ci-build.yaml)
[![license](https://img.shields.io/github/license/HenrikDK/yamlr.svg)](https://github.com/HenrikDK/Yamlr/blob/main/LICENSE)

## Requirements
* Python 3.11+
* PyYAML

## Installation
1. Download latest version of Yamlr from: https://github.com/HenrikDK/yamlr/releases/
2. Unzip to a folder in you python path

## Usage
1. Make a [schema](docs/schema.md)
2. Make some data that conforms to that schema

Then all you need to do is supply the files' path:
```python
# Import Yamlr and make a schema object:
import yamlr
schema = yamlr.make_schema('./schema.yaml')

# Create a Data object
data = yamlr.make_data('./data.yaml')

# Validate data against the schema. Throws a ValueError if data is invalid.
yamlr.validate(schema, data)
```

You can also pass a string of YAML to `make_schema()` and `make_data()` instead of passing a file path
by using the `content=` parameter:

```python
data = yamlr.make_data(content="""
name: Bill
age: 26
height: 6.2
awesome: True
""")
```

If `data` is valid, nothing will happen. However, if `data` is invalid Yamlr will throw a
`YamlrError` with a message containing all the invalid nodes:
```python
try:
    yamlr.validate(schema, data)
    print('Validation success! 👍')
except ValueError as e:
    print('Validation failed!\n%s' % str(e))
    exit(1)
```
and an array of `ValidationResult`.
```python
try:
    yamlr.validate(schema, data)
    print('Validation success! 👍')
except YamlrError as e:
    print('Validation failed!\n')
    for result in e.results:
        print("Error validating data '%s' with '%s'\n\t" % (result.data, result.schema))
        for error in result.errors:
            print('\t%s' % error)
    exit(1)
```

### Adding external includes
After you construct a schema you can add extra, external include definitions by calling `schema.add_include(dict)`. This method takes a dictionary and adds each key as another include.

### Strict mode
By default Yamlr will provide errors for extra elements present in lists and maps that are not covered by the schema. Strict mode can be toggled by passing the strict=True/False flag to the validate function.

It is also possible to mix strict and non-strict mode by setting the strict=True/False flag in the include validator, setting the option only for the included validators.




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

