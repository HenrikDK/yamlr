import yamale, json
import traceback

try:
    schema = yamale.make_schema('tests/fixtures/keyed/schema_keyed_any_with_include.yaml')
    print(repr(schema))
    data = yamale.make_data('tests/fixtures/keyed/data_keyed_any_with_include_bad.yaml')

    yamale.validate(schema, data)

    #print('Validation success! 👍')
except Exception as e:
    print(traceback.format_exc())
    print('Validation failed!\n%s' % str(e))
    exit(1)