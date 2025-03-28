import sys, os, requests, json
sys.path.append("./")
from yamlr import util

gh_token = os.getenv("GITHUB_TOKEN")
gh_headers =  {
    "Accept": "application/vnd.github+json", 
    "Authorization": f"Bearer {gh_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}


def create_release(org, repo, tag = 'latest'):
    if gh_token == 'debug': return None

    url = f"https://api.github.com/repos/{org}/{repo}/releases"

    body = {
        "tag_name": tag,
        "target_commitish": os.getenv('GIT_REF_NAME', 'main'),
        "name": tag,
        "draft": False,
        "prerelease": False,
        "generate_release_notes": True
    }

    response = requests.post(url, data=json.dumps(body), headers=gh_headers)
    print(f"http post: {url} - {response}")

    if response.status_code not in [200, 201]: 
        response.raise_for_status()

    result = response.json()
    print(f"Result: {result}")

    return result['id']


def upload_release_asset(org, repo, release_id, file, file_name):
    if gh_token == 'debug': return None

    upload_headers =  {
        "Accept": "application/vnd.github+json", 
        "Authorization": f"Bearer {gh_token}",
        "Content-Type": "application/zip",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    url = f'https://uploads.github.com/repos/{org}/{repo}/releases/{release_id}/assets?name={file_name}'

    content = b''
    with open(file, 'rb') as f:
        content = f.read()

    response = requests.post(url, data=content, headers=upload_headers)
    print(f"http post: {url} - {response}")

    if response.status_code not in [200, 201]: 
        response.raise_for_status()


def get_current_version():
    content = util.read_file('./pyproject.toml')
    element = 'version ='
    lines = content.splitlines()
    value = ''
    for l in lines:
        if element not in l:
            continue

        value = l.split('=')[1]
        value = value.replace('"','').replace(' ','')
        break

    run_number = os.getenv('GITHUB_RUN_NUMBER', '123')
    value = f'{value}.{run_number}'
    return value


def main():
    repo = str(os.getenv('GITHUB_REPOSITORY', 'HenrikDK/unknown_repo')).split('/')[1]
    org = str(os.getenv('GITHUB_REPOSITORY', 'HenrikDK/unknown_repo')).split('/')[0]
    print(gh_headers)

    version = get_current_version()

    id = create_release(org, repo, version)

    upload_release_asset(org, repo, id, 'yamlr.zip', f'yamlr-{version}.zip')


if __name__ == "__main__":  
   main()
