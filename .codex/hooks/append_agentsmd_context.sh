#!/usr/bin/env bash
set -euo pipefail

project_dir="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"

echo "=== AGENTS.md Files Found ==="
find "$project_dir" -name "AGENTS.md" -type f | while read -r file; do
    echo "--- File: $file ---"
    cat "$file"
    echo ""
done
