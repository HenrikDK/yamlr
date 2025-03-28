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
    print('Validation failed! ️‍🔥\n')
    for result in e.results:
        print(f'{result['data_path']}:')
        for e in result['errors']:
            print(f"{e['path']}: {e['error']}")
    
    exit(1)
```

### Adding external includes
After you construct a schema you can add extra, external include definitions by calling `schema.add_include(dict)`. This method takes a dictionary and adds each key as another include.

### Strict mode
By default Yamlr will provide errors for extra elements present in lists and maps that are not covered by the schema. Strict mode can be toggled by passing the strict=True/False flag to the validate function.

It is also possible to mix strict and non-strict mode by setting the strict=True/False flag in the include validator, setting the option only for the included validators.

# Documentation
[Installation](#installation)
[Usage](#usage)
[Examples](docs/examples.md)
[Extending](docs/extending.md)
[Schema](docs/schema.md)
[Validators](docs/validators.md)