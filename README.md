# Personal Portfolio

A small Flask portfolio and blog that can also be exported as a static site for GitHub Pages. The repository targets Python 3.12+ and uses `uv` to install the locked dependencies.

## Run Locally

```sh
uv sync --locked
uv run flask --app app:create_app run
```

Flask prints the local URL, usually `http://127.0.0.1:5000`. The app factory is in `app/__init__.py`; it registers the main, blog, and games blueprints.

## Build Static Site

```sh
uv run python freeze.py
```

Frozen-Flask writes the deployable site to the repository-root `build/` directory. That directory is generated and git-ignored. The freezer uses relative URLs so the site can work at a domain root or under a GitHub Pages repository path. It generates the home page, research page, blog index, each Markdown post, games index, and each game detail route.

`.github/workflows/pages.yml` runs on pushes to `main` and can also be started manually from GitHub Actions. It installs dependencies with `uv sync --locked`, freezes the site, and deploys `build/` to GitHub Pages. For the first deployment, set the repository's **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. The workflow does not automatically enable Pages for a repository that has never had Pages configured.

## Pages And Code

| Path | Purpose | Implementation |
| --- | --- | --- |
| `/` | Home, short bio, recent writing and games | `app/main/routes.py`, `app/templates/index.html` |
| `/research/` | Research interests and publication links | `app/main/routes.py`, `app/templates/research.html` |
| `/blog/` | Collapsible series list and sort control | `app/blog/routes.py`, `app/templates/blog/index.html` |
| `/blog/<slug>/` | Individual Markdown article | `app/blog/routes.py`, `app/templates/blog/post.html` |
| `/games/` | Game listing | `app/games/routes.py`, `app/templates/games/index.html` |
| `/games/<slug>/` | Game detail page | `app/games/routes.py`, `app/templates/games/game.html` |

`app/templates/base.html` provides the shared navigation. It currently loads `app/static/css/style_candidate2.css`, the light-lavender terminal theme. `style_candidate1.css` is an inactive alternative. Blog sorting behavior is in `app/static/js/blog-index.js`; images and other static assets are under `app/static/`.

## Writing Posts

Each file in `app/blog/posts/` is a Markdown article with YAML front matter. That folder is the blog's source of truth; post metadata is loaded at startup, and `freeze.py` discovers the post slugs automatically.

```markdown
---
title: "A New Article"
slug: "a-new-article"
date: 2026-09-28
updated: 2026-09-28
series: "Notes"
part: "Part 1"
tags:
	- topic
	- notes
---

Write the article here in Markdown.
```

The metadata fields are:

- `title`: display title.
- `slug`: unique URL component; the example becomes `/blog/a-new-article/`.
- `date`: original publication date.
- `updated`: date used for latest-updated ordering.
- `series`: heading for the collapsible group on the blog index.
- `part`: optional series position or subtitle.
- `tags`: list of topic labels displayed on the index.

Use standard Markdown for headings, links, images, emphasis, and lists. To link to a sibling post, use a relative URL such as `[Next](../next-slug/)`. From a post URL, static images are typically reached with paths like `../../static/blog/frog/styleganim.png`; keep these relative so they work on GitHub Pages project sites. Use descriptive image alt text for new media. Section anchors use Markdown Extra syntax, for example `## Commentary {#Commentary}`. Poem line breaks use two trailing spaces. Videos are currently represented as regular links to YouTube rather than embedded players.

The blog index has two sort modes. **Last updated** sorts series and posts by their `updated` metadata. **Series name** sorts groups alphabetically and then article titles alphabetically within each group. The JavaScript applies sorting in the browser, which also makes it work in the frozen site; query strings do not cause Frozen-Flask to generate separate pages.

## Current State And Decisions

- Ten articles have been migrated to Markdown: six in “This Frog Does Not Exist” and four in “Cinepoetry.” The old full-page HTML article copies and their HTML-fragment parser were removed.
- `BlogPost` in `app/blog/routes.py` represents the loaded post data. Dates are parsed as `datetime.date`; tags are stored as a tuple.
- The existing publication dates were used as `updated` dates during migration because the old pages did not record a separate last-modified date. Until you set meaningful `updated` values in front matter, “Last updated” is effectively ordered by publication date.
- The games section currently contains one sample entry and a placeholder detail page; it is site structure, not a finished game catalog.
- The home page currently says “I was a computer science student at Marshall University.” Review that wording for accuracy before publishing.
- Markdown output is inserted into the shared template as trusted HTML. This is suitable for repository-authored posts; if posts later come from users or other untrusted sources, sanitize rendered HTML before displaying it.
- No automated test suite is currently included. The routes and static export have been smoke-tested during development, but adding repeatable tests for metadata parsing, page routes, links, and freezing would be a useful next step.

## Useful Checks

```sh
uv run ruff check app
uv run python freeze.py
```
