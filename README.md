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

### Home page

- Main home page prose lives in [`content/_index.md`](content/_index.md).
- Reusable homepage HTML lives in shortcodes under [`themes/soldaini/layouts/shortcodes/`](themes/soldaini/layouts/shortcodes/), including `avatar`, `visitor-greeting`, `contacts`, and `company`.
- Company/logo styles live in [`themes/soldaini/assets/sass/theme.scss`](themes/soldaini/assets/sass/theme.scss), and the logo masks live in [`static/logos/`](static/logos/).

Use shortcodes in the Markdown file:

```go-html-template
{{< avatar >}}
{{< visitor-greeting >}}
{{< company microsoft >}}
{{< contacts >}}
```

Current company keys with built-in labels and links: `microsoft`, `ai2`, `amazon`, and `georgetown`. You can override the label and URL with positional arguments, e.g. `{{< company microsoft "Microsoft AI" "https://microsoft.ai/" >}}`.

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
