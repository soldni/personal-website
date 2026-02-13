+++
title = "Blog Post Feature Reference"
date = "2026-02-13T09:00:00-08:00"
lastmod = "2026-02-13T09:00:00-08:00"
description = "Reference page showing the post features supported by this site."
tags = ["reference", "hugo", "markdown"]
draft = false
math = true
summary = "Use this file as a copy/paste reference when writing new blog posts."
aliases = ["/blog/post-feature-reference"]
slug = "post-feature-reference"
+++

This file is a reference for future blog posts. Copy the parts you need.

## Front matter template

```toml
+++
title = "Your post title"
date = "2026-02-13T09:00:00-08:00"
lastmod = "2026-02-13T09:00:00-08:00" # optional
description = "Short summary for SEO and blog list cards."
tags = ["tag-one", "tag-two"]
draft = false
math = true # set to true only when you need equations
summary = "Optional manual summary for list pages."
aliases = ["/old/url"] # optional redirects
slug = "custom-url-slug" # optional permalink override
+++
```

Notes:

- `description` appears in metadata and in blog list cards.
- Blog list cards use `description` first, then fallback to `.Summary`.
- Set `math = true` only for posts that contain equations.

## Summary break (`<!--more-->`)

Text above `<!--more-->` becomes the auto-summary when `description` is missing.

This paragraph is visible in list summaries if there is no `description`.

<!--more-->

This paragraph is only shown on the full post page.

## Sections and headings

# H1 (usually generated from `title`, avoid extra H1s)
## H2 section heading
### H3 subsection heading
#### H4 smaller subsection heading

## Text formatting

Use **bold**, *italics*, ~~strikethrough~~, and inline `code`.

Use links in two styles:

- Inline: [Ai2](https://allenai.org)
- Reference style: [Personal site][site]

[site]: https://soldaini.net/

## Lists

Unordered list:

- First item
- Second item
- Third item

Ordered list:

1. First step
2. Second step
3. Third step

Task list:

- [x] Done item
- [ ] Open item

## Blockquotes and badges

> This is a quote block for notes, highlights, or citations.

Custom badge classes (used elsewhere on the site):

- `<span class="call-in">preprint</span>` renders as <span class="call-in">preprint</span>
- `<span class="call-out">best paper award</span>` renders as <span class="call-out">best paper award</span>

## Code blocks

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))
```

```bash
uv run hugo-preview
uv run hugo-cli --minify
```

```json
{
  "name": "example",
  "enabled": true
}
```

## Equations (KaTeX)

Enable `math = true` in front matter.

Inline math: $E = mc^2$

Display math:

$$
\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}
$$

$$
\arg\max_{\theta} \sum_{(x, y) \in D} \log p_{\theta}(y \mid x)
$$

## Tables

| Field | Purpose | Example |
|---|---|---|
| `title` | Main page title | `"How I built this"` |
| `description` | SEO + blog card summary | `"A short write-up..."` |
| `tags` | Grouping and metadata keywords | `["hugo", "notes"]` |

## Images

Standard image markdown:

![A cat on a chair](/cats1.webp)

Image with title text:

![Espresso setup](/espresso.webp "My home espresso setup")

Optional raw HTML figure (allowed in this site):

<figure>
  <img src="/cats2.webp" alt="Cat relaxing on a couch.">
  <figcaption>A figure caption written in HTML.</figcaption>
</figure>

## Image grid shortcode

```md
{{</* image-grid columns="3" */>}}
![A cat on a chair](/cats1.webp)
![Another cat lounging](/cats2.webp)
![A quiet espresso moment](/espresso.webp)
{{</* /image-grid */>}}
```

Rendered example:

{{< image-grid columns="3" >}}
![A cat on a chair](/cats1.webp)
![Another cat lounging](/cats2.webp)
![A quiet espresso moment](/espresso.webp)
{{< /image-grid >}}

## Footnotes

This sentence includes a footnote reference.[^1] Here is another one.[^2]

[^1]: Footnotes are rendered in a notes block at the end of the post.
[^2]: In blog posts, hovering/focusing references shows a popover preview.

## Horizontal rules

Use three dashes to separate major sections:

---

## Raw HTML blocks

Raw HTML is allowed (`markup.goldmark.renderer.unsafe = true`), so this works:

<details>
  <summary>Expandable details block</summary>
  <p>Put optional deep-dive notes here.</p>
</details>

## Quick starter skeleton

````md
+++
title = "Post title"
date = "2026-02-13T09:00:00-08:00"
description = "One-sentence summary."
tags = ["tag-one"]
draft = false
+++

Intro paragraph.

## Section
Main content.

## Code
```python
print("hello")
```

## Footnote example
Reference sentence.[^1]

[^1]: Footnote text.
````
