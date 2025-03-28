from yamlr import util

def show_errors(results):
    for result in results:

        show_file_errors(result)

#        data = util.read_file(result[''])
#        contents = data.splitlines()

def show_file_errors(result):
    for e in result['errors']:
        #lines[e['lineno']] = e
        print(f"line {e['lineno']}: {e['path']}: {e['error']}")
