+++
title = "A small test post"
date = "2025-02-14T09:00:00-08:00"
description = "A short post to validate layout, images, and footnotes for the new blog section."
tags = ["notes", "test"]
draft = false
+++

This is a quick, content-first post to confirm the blog layout, typography, and metadata. It should read cleanly on its own and confirm that standard Markdown features render as expected.

## A small image grid

{{< image-grid columns="3" >}}
![A cat on a chair](/cats1.webp)
![Another cat lounging](/cats2.webp)
![A quiet espresso moment](/espresso.webp)
{{< /image-grid >}}

## Notes and footnotes

Here is a short paragraph with an inline footnote to confirm the popover behavior works as intended.[^1] Another note uses the same block to confirm multiple footnotes don’t collide.[^2]

[^1]: A footnote that should appear inline on hover or focus.
[^2]: Another footnote to validate spacing and accessibility.
