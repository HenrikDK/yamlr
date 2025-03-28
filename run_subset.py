import yamlr

schema = {}

schema = yamlr.make_schema('tests/fixtures/keyed/schema_keyed_any_with_include.yaml')

data = yamlr.make_data('tests/fixtures/keyed/data_keyed_any_with_include_bad.yaml')

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
