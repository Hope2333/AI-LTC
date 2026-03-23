#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="/home/miao/develop/AI-LTC/examples/collaboration-system/project-template"
TARGET_DIR="${1:-}"

if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: $0 <target-repo-root>" >&2
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory does not exist: $TARGET_DIR" >&2
  exit 1
fi

cp -R "$SOURCE_DIR"/. "$TARGET_DIR"/

echo "Copied collaboration-system template into: $TARGET_DIR"
echo "Next: open /home/miao/develop/AI-LTC/examples/collaboration-system/bootstrap-checklist.md"
echo "Then rewrite 00_HANDOFF.md and the placeholder files under .ai/active-lane/."
