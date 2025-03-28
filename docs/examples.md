# Examples
Here are some common examples of yamlr usage.

## Using keywords
### Schema:
```yaml
optional: str(required=False)
optional_min: int(min=1, required=False)
min: num(min=1.5)
max: int(max=100)
```
### Valid Data:
```yaml
optional_min: 10
min: 1.6
max: 100
```

## Includes and recursion
### Schema:
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
### Valid Data:
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

## Lists
### Schema:
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
### Valid Data:
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

## The data is a list of items without a keyword at the top level
### Schema:
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

