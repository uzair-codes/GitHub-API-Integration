#!/bin/bash

# GitHub API base URL
GITHUB_API="https://api.github.com"

# Helper function: shows usage instructions if wrong input is given
helper() {
    echo "Usage: $0 <owner> <repo-name>"
    echo "Example: $0 uzair-codes AWS-Resource-Tracker"
    exit 1
}

# Validate input arguments
if [ $# -ne 2 ]; then
    helper
fi

OWNER=$1
REPO=$2

# Prompt user for GitHub credentials (username + PAT)
read -p "Enter your GitHub username: " USERNAME
read -s -p "Enter your GitHub Personal Access Token: " TOKEN
echo ""

# Function to call GitHub API and fetch collaborators with read access
call_github() {
    URL="${GITHUB_API}/repos/${OWNER}/${REPO}/collaborators"

    RESPONSE=$(curl -s -u "${USERNAME}:${TOKEN}" "$URL")

    # Extract collaborators with pull access
    COLLABORATORS=$(echo "$RESPONSE" | jq -r '.[] | select(.permissions.pull==true) | .login')

    if [ -z "$COLLABORATORS" ]; then
        echo -e "\033[31mNo users with read access found for ${OWNER}/${REPO}\033[0m"
    else
        echo -e "\033[32mUsers with read access to ${OWNER}/${REPO}:\033[0m"
        echo "$COLLABORATORS"
    fi
}

# Main Execution
echo "🔍 Fetching collaborators for ${OWNER}/${REPO}..."
call_github
