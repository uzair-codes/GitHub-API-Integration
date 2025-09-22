#!/usr/bin/env python3
"""
GitHub API Integration Script (Fixed Version)
Author: Uzair
Date: 2025-09-22
Description: Fetch GitHub repo info, issues, contributors with authentication.
"""

import requests
from prettytable import PrettyTable

# ------------------------------
# Get user input
# ------------------------------
GITHUB_TOKEN = input("Enter your GitHub PAT: ").strip()
OWNER = input("Enter GitHub Username/org: ").strip()
REPO = input("Enter repo name: ").strip()

# ------------------------------
# API Setup
# ------------------------------
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_repo_info():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 401:
        print("❌ Authentication failed! Check your PAT.")
        print("🔑 Go to https://github.com/settings/tokens to create a valid PAT with 'repo' and 'read:user' scopes.")
        exit(1)
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
        if "pull_request" not in issue:  # filter PRs
            table.add_row([issue["number"], issue["title"], issue["state"], issue["user"]["login"]])
    print("\n🔧 Open Issues:")
    if table.rowcount > 0:
        print(table)
    else:
        print("✅ No open issues found.")

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
