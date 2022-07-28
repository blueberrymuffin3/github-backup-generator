import requests
import os
import json
from pathlib import Path

backup_dir=Path("./backup")
backup_meta=backup_dir / "meta.txt"
backup_data_dir=backup_dir / "data"

def main():
    token = os.environ["GITHUB_TOKEN"]
    headers = { "Authorization": f"token {token}" }
    r = requests.get("https://api.github.com/user/repos?affiliation=owner&per_page=100", headers=headers)
    if not r.ok:
        print("Error:", r.text)
        return

    repos = r.json()
    print("Got", len(repos), "repos")

    if(len(repos) >= 100):
        raise ValueError("Paging for >100 repos not supported yet")

    backup_dir.mkdir(exist_ok=True)

    with open(backup_meta, 'w') as meta_file:
        total_size = sum(map(lambda repo: repo['size'], repos))
        print(f"{'full_name': <50} {'node_id': <32} ({total_size: >8} KB)", file=meta_file)
        print("-------------------------------------------------------------------------------------------------", file=meta_file)

        for repo in repos:
            print(f"Backing up {repo['full_name']}")
            print(f"{repo['full_name']: <50} {repo['node_id']: <32} ({repo['size']: >8} KB)", file=meta_file)
            try:
                backup_repo(repo)
            except Exception as e:
                print(f"Error backing up {repo['full_name']}: {e}")

def backup_repo(repo):
    path = backup_dir / repo['node_id']
    if path.exists():
        print("Backup exists, updating")
        # git remote update
    else:
        print("Backup does not exist, creating")
        # git clone --mirror

if __name__=="__main__":
    main()