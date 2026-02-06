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

Preview locally (includes drafts):

```bash
uv run hugo-preview
```

Build production output into `public/`:

```bash
uv run hugo-cli
```

Pass any Hugo flags through either command, for example:

```bash
uv run hugo-preview --bind 0.0.0.0 --port 1313
uv run hugo-cli --minify
```
