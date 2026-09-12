import json
import time
from datetime import datetime

import requests

from config import BASE_URL, HEADERS

def fetch_all_pages(url, max_pages=5):
    """Fetch multiple pages from the GitHub API."""

    results = []
    page_count = 0

    while url and page_count < max_pages:
        print(f"Fetching: {url}")

        response = requests.get(url, headers=HEADERS)

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        results.extend(response.json())

        page_count += 1
        url = response.links.get("next", {}).get("url")

        time.sleep(0.2)

    return results


def fetch_commits(owner, repo):
    """Fetch all commits from a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits?per_page=100"
    return fetch_all_pages(url)


def fetch_pulls(owner, repo):
    """Fetch all pull requests from a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls?state=all&per_page=100"
    return fetch_all_pages(url)


def fetch_issues(owner, repo):
    """Fetch all issues from a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues?state=all&per_page=100"
    return fetch_all_pages(url)

def save_raw(data, name):
    """Save API data as a timestamped JSON file."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    path = f"../data/raw/{name}_{timestamp}.json"

    with open(path, "w") as file:
        json.dump(data, file, indent=2)

    print(f"Saved {len(data)} records to {path}")

if __name__ == "__main__":

    REPOS = [
        ("psf", "requests"),
        ("pallets", "flask")
    ]

    for owner, repo in REPOS:

        print(f"\nProcessing repository: {owner}/{repo}")

        commits = fetch_commits(owner, repo)
        save_raw(commits, f"{owner}_{repo}_commits")

        pulls = fetch_pulls(owner, repo)
        save_raw(pulls, f"{owner}_{repo}_pulls")

        issues = fetch_issues(owner, repo)
        save_raw(issues, f"{owner}_{repo}_issues")
