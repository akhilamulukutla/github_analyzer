import json
import os
import pandas as pd


def load_json_file(filepath):
    """Load and return data from a JSON file."""

    with open(filepath, "r") as file:
        data = json.load(file)

    return data


def transform_commits(commits):
    """Transform raw commit data into a clean DataFrame."""

    cleaned_data = []

    for commit in commits:
        cleaned_data.append({
            "sha": commit.get("sha"),
            "author": commit.get("commit", {}).get("author", {}).get("name"),
            "date": commit.get("commit", {}).get("author", {}).get("date"),
            "message": commit.get("commit", {}).get("message")
        })

    return pd.DataFrame(cleaned_data)


if __name__ == "__main__":
    filepath = "data/raw/psf_requests_commits_20260912_112046.json"

    commits = load_json_file(filepath)

    commits_df = transform_commits(commits)

    print(commits_df.head())