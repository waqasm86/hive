#!/usr/bin/env bash
# Usage: export GITHUB_TOKEN=NEW_PAT; ./scripts/create_prs.sh
set -euo pipefail
if [ -z "${GITHUB_TOKEN-}" ]; then
  echo "GITHUB_TOKEN not set. Export it locally before running this script." >&2
  exit 1
fi

PR_BODY=$(awk '{printf "%s\\n", $0}' PR_DESCRIPTION_ci_windows_fixes.md)

create_pr() {
  local repo=$1
  local title=$2
  local head=$3
  local body="$PR_BODY"
  payload=$(jq -n --arg t "$title" --arg h "$head" --arg b "$body" '{title:$t,head:$h,base:"main",body:$b}')
  curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
    -d "$payload" "https://api.github.com/repos/$repo/pulls" | jq -c '.'
}

echo "Creating PR on your fork (waqasm86/hive)..."
create_pr "waqasm86/hive" "ci: fix CI lint/test for Windows" "waqasm86:chore/fix-windows-tests-encoding-clean"

sleep 1

echo "Creating upstream PR to adenhq/hive (from your fork branch)..."
create_pr "adenhq/hive" "ci: Windows & CI fixes" "waqasm86:chore/fix-windows-tests-encoding-clean"

echo "Done."