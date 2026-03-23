# Repository Guidelines

## Project Structure & Module Organization
- `config.toml` holds site-wide settings (base URL, menus, theme, params).
- `content/` contains Markdown pages with TOML front matter (`+++`), e.g., `_index.md`.
- `content/publications.bib` is the BibTeX source for all publications; see **Publications pipeline** below.
- `content/publications/_index.md` is the front matter + intro text for the publications section page.
- `themes/soldaini/` is the custom Hugo theme (layouts, partials, and Sass live here).
- `themes/soldaini/layouts/publications/list.html` renders the publications page from generated JSON data.
- `themes/soldaini/data/publication_topics.json` defines topic display order and maps topics to SVG icon filenames.
- `layouts/partials/` is currently unused; prefer theme partials unless a one-off override is needed.
- `static/` stores files served as-is (images, icons). `static/logos/` holds SVG masks used for icon styling (including per-topic publication icons).
- `assets/` is for Hugo Pipes assets at the site root; theme-specific Sass lives in `themes/soldaini/assets/`.
- `resources/` is Hugo’s generated cache; `archetypes/` defines templates for `hugo new`.
- `data/generated/` is written at build time by the Python preprocessing step; do not edit files here by hand.
- `pyproject.toml` defines the `uv`-managed Python project and CLI entrypoints for Hugo commands.
- `src/personal_website/` contains Python modules:
  - `cli.py` — CLI entrypoints (`hugo-cli`, `hugo-preview`, `hugo-build`, `preview-png`); each calls `generate_publications_data()` before invoking Hugo.
  - `publications.py` — orchestrator that reads `.bib`, validates entries, and writes `data/generated/publications.json`.
  - `bibtex.py` — thin wrapper around `bibtexparser` to parse `.bib` files into dicts.
  - `authors.py` — formats author lists as HTML with highlight, equal-contribution (α) and core-contributor (ω) markers, and collapsible `.hide-authors` spans.
  - `venues.py` — maps full venue names to short abbreviations and renders venue text lines.

## Repository Philosophy (Comprehensive)

### Core philosophy
- This repository is a hand-crafted personal knowledge/artifact site, not a generic blog scaffold.
- Content is the product; theming exists to support readability, personality, and long-term maintainability.
- Prefer simple, explicit Hugo templates and Markdown over abstractions, generators, or heavy frameworks.
- Keep pages durable: stable links, static assets, and source documents should keep working for years.

### Authoring model
- Markdown with TOML front matter is the default authoring surface; keep it human-readable.
- Raw HTML in Markdown is intentionally allowed (`markup.goldmark.renderer.unsafe = true`) and used for bespoke layout/content blocks.
- `archetypes/default.md` is intentionally minimal and defaults to `draft = false`; new content is expected to be publish-ready unless explicitly marked otherwise.
- Page structure is intentionally shallow: base template + containerized content, with minimal template branching.

### Design and UX intent (from `themes/soldaini`)
- The visual direction is warm, typographic, and editorial: paper-like backgrounds, muted ink, restrained accent color.
- Typography prioritizes legibility (Atkinson Hyperlegible variable font, conservative line-height, bounded content width).
- Dark mode support is first-class via CSS custom properties and `prefers-color-scheme`.
- Motion is expressive but optional: animated avatar glow and author-list transitions should respect `prefers-reduced-motion`.
- Interactions should remain lightweight, direct, and content-oriented; avoid adding UI chrome that competes with the writing.

### Progressive enhancement and accessibility
- JavaScript is intentionally minimal and targeted (avatar toggle, collapsible long author lists, minor text normalization).
- Core content must remain usable without JavaScript; JS should enhance, not gate content.
- Maintain semantic HTML and meaningful alt text for images.
- Preserve accessibility attributes and behavior in interactive elements (`aria-hidden` toggles, reduced-motion checks).

### Asset and branding strategy (from `static/`)
- `static/` is a curated, long-lived asset library: photos, PDFs, icons, fonts, and favicon variants are deliberate and should not be casually removed.
- Keep both source-like assets (e.g., raw favicon variants, `.sketch` files) and web-ready derivatives when they document the design pipeline.
- Social/license/icon rendering uses SVG masks in `static/logos/`; add new iconography in this style unless there is a strong reason not to.
- Favicon coverage is intentionally broad (legacy + current assets) for cross-platform compatibility.
- Prefer local static assets for core identity and content durability.

### Publications pipeline
- Publications are authored in `content/publications.bib`; each BibTeX entry requires `title`, `author`, `year`, `order`, `url`, and `topic` fields.
- Optional fields: `author_equal` / `author_core` (names joined with ` and `), `team_prefix`, `badge` (e.g. `preprint`, `technical report`), `venue_note`, `booktitle`, `journal`, `school`, `archiveprefix` + `eprint`.
- Before Hugo runs, `generate_publications_data()` parses the `.bib` file, renders author HTML (with highlight/markers/collapsible spans) and venue text, and writes `data/generated/publications.json`.
- The Hugo template `themes/soldaini/layouts/publications/list.html` reads this JSON to render year-grouped entries with a topic filter bar.
- Badge styling: `call-out` (accent background) for most badges; `call-in` (muted background) for `preprint` and `technical report`.
- Topic icons live in `static/logos/` as SVGs and are referenced by `themes/soldaini/data/publication_topics.json`.
- To add a new publication, add a BibTeX entry to `publications.bib` with all required fields; to add a new topic, add the topic name and icon filename to `publication_topics.json` and place the SVG in `static/logos/`.

### Content-specific interaction conventions
- Publications author lists use `.hide-authors` spans for long author lists; this is generated by the Python pipeline, not hand-edited.
- Use existing callout vocabulary (`call-in`, `call-out`) for publication metadata badges.
- Home page avatar behavior depends on `#avatar-container`, `#front-avatar`, and `#back-avatar`; preserve these IDs if changing markup.

### Operational guardrails for agents
- Prefer surgical edits over broad rewrites; this codebase is intentionally custom and compact.
- Keep dependencies minimal; avoid introducing bundlers/frameworks unless explicitly requested.
- When changing styles, update `themes/soldaini/assets/sass/variables.scss` and `theme.scss` coherently to preserve the design system.
- When changing head/footer behavior, account for analytics, favicon links, math opt-in behavior, and licensing markup.
- Do not remove legacy/static files unless you have verified they are unused and replacement coverage exists.

## Build, Test, and Development Commands
- `uv sync` installs project dependencies (including pinned Hugo and `bibtexparser`).
- `uv run hugo-preview` runs `hugo server --disableFastRender` for local preview of published content.
- `uv run hugo-cli` runs Hugo directly (e.g., production build to `public/` by default).
- `uv run hugo-build` runs `hugo --minify` (used by CI); accepts pass-through flags.
- `uv run preview-png -- <page path>` starts a temporary Hugo server and saves a full-page screenshot to `.artifacts/preview-<slug>.png` (example: `uv run preview-png -- /publications/`).
- All commands automatically run `generate_publications_data()` before invoking Hugo, so `data/generated/publications.json` is always fresh.
- Pass-through flags are supported, e.g., `uv run hugo-cli --minify`.


## Agent Hooks (Claude + Codex)
- Claude hook is configured in `.claude/settings.json` and runs `.claude/hooks/append_agentsmd_context.sh` at `SessionStart`.
- Codex hook script is at `.codex/hooks/append_agentsmd_context.sh`; use it from project config with `codex --config .codex/config.toml`.
- The Codex config uses `notify` to run the hook command and print `AGENTS.md` context after each turn.

## Coding Style & Naming Conventions
- Keep Markdown concise and consistent with existing pages; prefer short sections and clear headings.
- Use TOML front matter (`+++`) and match the indentation/style already present in the file.
- Name new assets with lowercase, hyphen-separated filenames (e.g., `new-hero.webp`).
- No repo-wide formatter or linter is configured; format by hand and keep diffs minimal.
- The author list expand/collapse logic is defined in `themes/soldaini/layouts/partials/footer.html`; adjust animation behavior there.
- Author rendering logic (markers, highlighting, `.hide-authors` spans) lives in `src/personal_website/authors.py`.
- Venue abbreviation mapping lives in `src/personal_website/venues.py`; add new entries to `VENUE_SHORT_NAMES` there.

## Testing Guidelines
- No automated tests are present. Validate changes by running `uv run hugo-cli` and checking output in the browser.
- For content edits, spot-check links, images, and layout on the relevant page.

## Commit & Pull Request Guidelines
- Commit history uses short, descriptive subject lines without prefixes (often sentence-case or lowercase).
- Keep commit subjects under ~72 characters and mention the primary change.
- PRs should include a brief summary, list touched pages, and provide screenshots for visual/layout changes.
- Link related issues or notes when applicable.

## Security & Configuration Tips
- Do not commit secrets. Keep verification tokens and analytics IDs in `config.toml` only if intended to be public.
- Change `baseURL` only when deliberately updating the production domain.
