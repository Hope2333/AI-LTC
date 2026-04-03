#!/usr/bin/env bash
# AI-LTC Framework Check Script
# Validates that consumer repos are aligned with the correct AI-LTC version.
# Usage: bash scripts/framework-check.sh [REPO_ROOT]
# If REPO_ROOT is not given, checks all repos listed in cross-repo-registry.json.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AI_LTC_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY="$AI_LTC_ROOT/cross-repo-registry.json"

if [ ! -f "$REGISTRY" ]; then
	echo "ERROR: cross-repo-registry.json not found at $REGISTRY"
	exit 1
fi

FRAMEWORK_VERSION=$(cat "$AI_LTC_ROOT/VERSION" | tr -d '[:space:]')
EXIT_CODE=0

check_repo() {
	local repo_name="$1"
	local repo_path="$2"
	local config_path="$3"
	local expected_branch="$4"
	local expected_version="$5"

	if [ ! -d "$repo_path" ]; then
		echo "SKIP  $repo_name: path $repo_path not found"
		return 0
	fi

	local config_file="$repo_path/$config_path"
	if [ ! -f "$config_file" ]; then
		echo "SKIP  $repo_name: config $config_path not found"
		return 0
	fi

	# Extract version and branch from consumer config
	local actual_version
	actual_version=$(grep -o '"framework_version"[[:space:]]*:[[:space:]]*"[^"]*"' "$config_file" | head -1 | sed 's/.*"framework_version"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

	local actual_repo_ref
	actual_repo_ref=$(grep -o '"repo_ref"[[:space:]]*:[[:space:]]*"[^"]*"' "$config_file" | head -1 | sed 's/.*"repo_ref"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

	local installed_tag
	installed_tag=$(grep -o '"installed_framework_tag"[[:space:]]*:[[:space:]]*"[^"]*"' "$config_file" | head -1 | sed 's/.*"installed_framework_tag"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

	local ok=true

	# Check version match
	if [ "$actual_version" != "$expected_version" ]; then
		echo "MISMATCH $repo_name: framework_version=$actual_version (expected $expected_version)"
		ok=false
	fi

	# Check installed tag matches framework version
	if [ "$installed_tag" != "$expected_version" ]; then
		echo "MISMATCH $repo_name: installed_framework_tag=$installed_tag (expected $expected_version)"
		ok=false
	fi

	# Check repo_ref matches expected branch
	if [ "$actual_repo_ref" != "$expected_branch" ]; then
		echo "MISMATCH $repo_name: repo_ref=$actual_repo_ref (expected $expected_branch)"
		ok=false
	fi

	if $ok; then
		echo "OK    $repo_name: $expected_version @ $expected_branch"
	else
		EXIT_CODE=1
	fi
}

echo "AI-LTC Framework Check"
echo "======================"
echo "Framework version: $FRAMEWORK_VERSION"
echo ""

# If a specific repo root is given, check only that one
if [ $# -ge 1 ]; then
	repo_root="$1"
	# Find matching entry in registry
	while IFS= read -r line; do
		repo_name=$(echo "$line" | cut -d'|' -f1)
		repo_path=$(echo "$line" | cut -d'|' -f2)
		config_path=$(echo "$line" | cut -d'|' -f3)
		branch=$(echo "$line" | cut -d'|' -f4)
		version=$(echo "$line" | cut -d'|' -f5)
		if [ "$repo_root" = "$repo_path" ]; then
			check_repo "$repo_name" "$repo_path" "$config_path" "$branch" "$version"
			exit $EXIT_CODE
		fi
	done < <(python3 -c "
import json, sys
with open('$REGISTRY') as f:
    reg = json.load(f)
for name, info in reg.get('consumer_repos', {}).items():
    print(f\"{name}|{info['path']}|{info['config']}|{info['branch']}|{info['expected_version']}\")
")
	echo "WARN  No registry entry found for $repo_root"
	exit 0
fi

# Check all registered repos
while IFS= read -r line; do
	repo_name=$(echo "$line" | cut -d'|' -f1)
	repo_path=$(echo "$line" | cut -d'|' -f2)
	config_path=$(echo "$line" | cut -d'|' -f3)
	branch=$(echo "$line" | cut -d'|' -f4)
	version=$(echo "$line" | cut -d'|' -f5)
	check_repo "$repo_name" "$repo_path" "$config_path" "$branch" "$version"
done < <(python3 -c "
import json
with open('$REGISTRY') as f:
    reg = json.load(f)
for name, info in reg.get('consumer_repos', {}).items():
    print(f\"{name}|{info['path']}|{info['config']}|{info['branch']}|{info['expected_version']}\")
")

echo ""
if [ $EXIT_CODE -eq 0 ]; then
	echo "All consumer repos aligned."
else
	echo "Some consumer repos are out of sync. Run framework check after updating AI-LTC."
fi

exit $EXIT_CODE
