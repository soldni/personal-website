#! /usr/bin/env bash
set -euo pipefail

# get script directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  # if $SOURCE was a relative symlink, we need to resolve it
  # relative to the path where the symlink file was located
  [[ $SOURCE != /* ]] && SOURCE="$SCRIPT_DIR/$SOURCE"
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

CURRENT=$(pwd)

cd "${SCRIPT_DIR}"

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
    cd "${CURRENT}"
    exit
}

UV_BIN=${UV:-uv}
if ! command -v "${UV_BIN}" >/dev/null 2>&1; then
    echo "error: uv is required but was not found in PATH" >&2
    cd "${CURRENT}"
    exit 127
fi

while true; do
    "${UV_BIN}" run preview "$@"
done
