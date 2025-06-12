import requests
from urllib.parse import urlparse

def get_url(package_name):
    registry_url = f"https://registry.npmjs.org/{package_name}"

    try:
        response = requests.get(registry_url, timeout=10)
        response.raise_for_status()
        package_data = response.json()

        # 'repository' can be a dict or a string
        repository_info = package_data.get("repository")

        if isinstance(repository_info, dict):
            url = repository_info.get("url")
        elif isinstance(repository_info, str):
            url = repository_info
        else:
            return None

        if url and "github.com" in url:
            # Normalize the URL by stripping prefixes like git+
            url = url.replace("git+", "").replace(".git", "").strip()
            return url

    except (requests.RequestException, ValueError, KeyError):
        pass

    return None

def get_readme(github_url):
    readme_names = [
        'README.md', 'README.rst', 'README.txt', 'README',
        'readme.md', 'readme.rst', 'readme.txt', 'readme'
    ]

    # Parse the GitHub URL
    parsed_url = urlparse(github_url)
    path_parts = parsed_url.path.strip('/').split('/')

    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL. Expected format: 'https://github.com/owner/repo'")

    owner, repo = path_parts[0], path_parts[1]

    # Step 1: Get default branch using GitHub API
    api_url = f'https://api.github.com/repos/{owner}/{repo}'
    api_resp = requests.get(api_url)
    if api_resp.status_code != 200:
        raise ValueError(f"Could not access GitHub API: {api_resp.status_code}")

    default_branch = api_resp.json().get('default_branch', 'main')

    # Step 2: Try to download each possible README file
    for name in readme_names:
        raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/{name}'
        resp = requests.get(raw_url)
        if resp.status_code == 200:
            return resp.text
    return None