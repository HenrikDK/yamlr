### Schema

To use Yamlr you must make a schema. A schema is a valid YAML file with one or more documents
inside. Each node terminates in a string which contains valid Yamlr syntax. For example, `str()`
represents a [String validator](./validators.md). 

The full list of all currently supported validators can be found [here](validators.md)

A basic schema:
```yaml
name: str()
age: int(max=200)
height: num()
awesome: bool()
```

And some YAML that validates:
```yaml
name: Bill
age: 26
height: 6.2
awesome: True
```

Take a look at the [Examples](./examples.md) section for more complex schema ideas.

#### Includes
Schema files may contain more than one YAML document (nodes separated by `---`). The first document
found will be the base schema. Any additional documents will be treated as Includes. Includes allow
you to define a valid structure once and use it several times. They also allow you to do recursion.

A schema with an Include validator:
```yaml
person1: include('person')
person2: include('person')
---
person:
    name: str()
    age: int()
```

Some valid YAML:
```yaml
person1:
    name: Bill
    age: 70

person2:
    name: Jill
    age: 20
```

Every root node not in the first YAML document will be treated like an include:
```yaml
person: include('friend')
group: include('family')
---
friend:
    name: str()
family:
    name: str()
```

Is equivalent to:
```yaml
person: include('friend')
group: include('family')
---
friend:
    name: str()
---
family:
    name: str()
```

##### Recursion
You can get recursion using the Include validator.

This schema:
```yaml
person: include('human')
---
human:
    name: str()
    age: int()
    friend: include('human', required=False)
```

Will validate this data:
```yaml
person:
    name: Bill
    age: 50
    friend:
        name: Jill
        age: 20
        friend:
            name: Will
            age: 10
```
