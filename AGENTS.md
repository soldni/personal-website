# Repository Guidelines

## Project Structure & Module Organization
- `config.toml` holds site-wide settings (base URL, menus, theme, params).
- `content/` contains Markdown pages with TOML front matter (`+++`), e.g., `_index.md`, `publications.md`.
- `layouts/partials/` overrides theme partials when site-specific tweaks are needed.
- `themes/researcher/` is the vendored Hugo theme; avoid edits unless updating the theme.
- `static/` stores files served as-is (images, icons); `assets/` is for Hugo Pipes assets.
- `resources/` is Hugo’s generated cache; `archetypes/` defines templates for `hugo new`.

## Build, Test, and Development Commands
- `./preview.sh` runs `hugo server --disableFastRender -D` in a loop for local preview, including drafts.
- `hugo server -D` runs the dev server once without the script.
- `hugo` builds the production site into `public/` (Hugo default output directory).

## Coding Style & Naming Conventions
- Keep Markdown concise and consistent with existing pages; prefer short sections and clear headings.
- Use TOML front matter (`+++`) and match the indentation/style already present in the file.
- Name new assets with lowercase, hyphen-separated filenames (e.g., `new-hero.webp`).
- No repo-wide formatter or linter is configured; format by hand and keep diffs minimal.

## Testing Guidelines
- No automated tests are present. Validate changes by running `hugo` and checking output in the browser.
- For content edits, spot-check links, images, and layout on the relevant page.

## Commit & Pull Request Guidelines
- Commit history uses short, descriptive subject lines without prefixes (often sentence-case or lowercase).
- Keep commit subjects under ~72 characters and mention the primary change.
- PRs should include a brief summary, list touched pages, and provide screenshots for visual/layout changes.
- Link related issues or notes when applicable.

## Security & Configuration Tips
- Do not commit secrets. Keep verification tokens and analytics IDs in `config.toml` only if intended to be public.
- Change `baseURL` only when deliberately updating the production domain.
