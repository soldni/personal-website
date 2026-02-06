#!/usr/bin/env bash

# Find all AGENTS.md files in current directory and subdirectories
# This is a temporay solution for case that Claude Code not satisfies with AGENTS.md usage case.
echo "=== AGENTS.md Files Found ==="
find "$CLAUDE_PROJECT_DIR" -name "AGENTS.md" -type f | while read -r file; do
    echo "--- File: $file ---"
    cat "$file"
    echo ""
done
