# personal-website

Source code for my personal website.
Visit it at [soldaini.net](http://soldaini.net).

## Setup

1. Install `uv` ([docs](https://docs.astral.sh/uv/)).
2. Install project dependencies:
   ```bash
   uv sync
   ```

## Work on the site

- Pages are in [`content/`](content/)
- Assets are in [`static/`](static/)
- Publications are authored in [`content/publications.bib`](content/publications.bib) as BibTeX entries

### Home page and career timeline

- Main home page prose lives in [`content/_index.md`](content/_index.md).
- Career timeline entries live in [`content/career-timeline/_index.md`](content/career-timeline/_index.md). This is a headless Hugo content bundle, so it feeds the home page but does not publish its own page.
- The home page renders the timeline with `{{< career-timeline >}}`; the renderer is [`themes/soldaini/layouts/shortcodes/career-timeline.html`](themes/soldaini/layouts/shortcodes/career-timeline.html).
- Timeline styling lives in [`themes/soldaini/assets/sass/theme.scss`](themes/soldaini/assets/sass/theme.scss).

Each timeline entry is a TOML block in the Markdown file:

```toml
[[entries]]
period = "2022-2026"
role = "Lead Research Scientist"
organization = "Ai2"
team = "Olmo and Semantic Scholar"
url = "https://allenai.org/"
logo = "Ai2.svg"
summary = "One short Markdown-friendly placeholder about the work."
```

Use `logo` for a file in [`static/logos/`](static/logos/). Use `current = true` on the active role to add the animated current-role marker. `summary` supports inline Markdown links. The rendered timeline intentionally stays compact: role first, affiliation/team/period second, then one short description.

Preview locally (published content only):

```bash
uv run hugo-preview
```

Build production output into `public/`:

```bash
uv run hugo-build
```

Pass any Hugo flags through either command, for example:

```bash
uv run hugo-preview --bind 0.0.0.0 --port 1313
uv run hugo-build --baseURL https://example.com/
```

All commands automatically generate `data/generated/publications.json` from the `.bib` file before invoking Hugo.
