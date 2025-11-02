# Repository Guidelines

- This site is built with Hugo using the bundled `themes/researcher` theme.
- Use [`uv`](https://docs.astral.sh/uv/) for Python tooling; dependencies and scripts are defined in `pyproject.toml`.
- Run the local development server with `uv run preview` (also used by `preview.sh`).
- Prefer keeping shell scripts POSIX-friendly when possible and enable strict error handling (`set -euo pipefail`).
- When adding Hugo layouts or assets, follow the structure already in `themes/researcher`.
- Document any new build or preview commands you introduce in `README.md`.
