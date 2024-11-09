import yamale

try:
    schema = yamale.make_schema('./yamale/tests/keyed_fixtures/schema_keyed_any_with_include.yaml')
    data = yamale.make_data('./yamale/tests/keyed_fixtures/data_keyed_any_with_include_bad.yaml')

    yamale.validate(schema, data)

    print('Validation success! 👍')
except Exception as e:
    print('Validation failed!\n%s' % str(e))
    exit(1)