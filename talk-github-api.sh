#!/bin/bash

github-api="https://api.github.com"
owner=$1
reponame=$2

function helper{
	if [ $# -ne 2 ]
	then
		echo "Usage: $0 owner repo-name"
		exit 1
	fi
}

function call-github {
url="${github-api}/repos/$owner/$reponame/collaborators"

collaborators= "$(curl -s -u "${username}:${token}" "url") | jq -r '.[] | select(.permission.pulls==true) | .login'"

if [ -z "$collaborators" ]
then
	echo "No users with read access found for ${owner}/${reponame}"
else
	echo "User with read access to ${owner}/${reponame}:"
	echo "$collaborators"
fi
}

# Validate Arguments
helper "$@"

# Main Script

echo " Listing Users with read access to ${owner}/${reponame}..."

call-github



