#!/usr/bin/env python3
"""
GitHub API Integration
Fetch repository details, open issues, and contributors.
"""

import requests
import os
from prettytable import PrettyTable

# ------------------------------
# USER CONFIGURATION
# ------------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_PAT_HERE")  # Best practice: use environment variable
OWNER = "uzair-codes"  # Replace with your GitHub username/org
REPO = "Automated-Node-Health-Check"  # Replace with repo name

# ------------------------------
# API Setup
# ------------------------------
BASE_URL = "https://api.github.com"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}


def fetch_repo_info():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def fetch_open_issues():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def fetch_contributors():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/contributors"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def generate_report():
    print("\n📊 GitHub Repository Report")
    print("=" * 60)

    # 1. Repo Info
    repo = fetch_repo_info()
    print(f"📦 Repository: {repo['full_name']}")
    print(f"⭐ Stars: {repo['stargazers_count']} | 🍴 Forks: {repo['forks_count']} | 🐛 Open Issues: {repo['open_issues_count']}")

    # 2. Issues Table
    issues = fetch_open_issues()
    table = PrettyTable(["Issue #", "Title", "State", "Created By"])
    table.align = "l"
    for issue in issues:
        # GitHub API returns PRs as well in /issues endpoint, filter them out
        if "pull_request" not in issue:
            table.add_row([issue["number"], issue["title"], issue["state"], issue["user"]["login"]])
    print("\n🔧 Open Issues:")
    print(table)

    # 3. Contributors Table
    contributors = fetch_contributors()
    contrib_table = PrettyTable(["Contributor", "Contributions"])
    contrib_table.align = "l"
    for contrib in contributors:
        contrib_table.add_row([contrib["login"], contrib["contributions"]])
    print("\n👥 Contributors:")
    print(contrib_table)


if __name__ == "__main__":
    generate_report()
