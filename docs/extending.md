# Extending with Custom validators
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
