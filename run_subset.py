import yamlr
from yamlr import display

schema = {}

schema = yamlr.make_schema('tests/fixtures/keyed/schema_keyed_any_with_include.yaml')

data = yamlr.make_data('tests/fixtures/keyed/data_keyed_any_with_include_bad.yaml')

results = yamlr.validate(schema, data, True, False)

for result in results:
    if len(result['errors']) == 0:
        print(f"{result['data_path']} 👍")
        continue
    
    print(f'{result['data_path']} ️‍🔥:\n')
    display.show_file_errors(result)
    exit(1)
