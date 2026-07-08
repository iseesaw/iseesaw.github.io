# CLAUDE.md

Personal academic homepage of Kaiyan Zhang (iseesaw.github.io), built on the al-folio Jekyll theme, heavily customized. Deployed via GitHub Actions (`.github/workflows/deploy.yml`).

## Build & serve (local)

The sandbox default shell picks system Ruby 2.6 and an ASCII locale — both break the build. Always use:

```bash
LC_ALL=en_US.UTF-8 PATH="/opt/homebrew/opt/ruby/bin:$PATH" bundle exec jekyll build
LC_ALL=en_US.UTF-8 PATH="/opt/homebrew/opt/ruby/bin:$PATH" bundle exec jekyll serve
```

- UTF-8 locale is required: `papers.bib` contains `†`/`*` author markers; ASCII locale crashes bibtex-ruby.
- Gems live under Homebrew Ruby 3.2 (`/opt/homebrew/opt/ruby`).
- `imagemagick.enabled: false` in `_config.yml` — the `convert` binary is not installed and this al-folio version's `figure.liquid` never referenced the webp srcset anyway (extension-compare bug). Do not re-enable without installing ImageMagick.
- Quick preview of `_site`: `.claude/launch.json` defines a `site-preview` static server (port 4173). Browsers cache `main.css` aggressively (static md5 bust param); force-reload CSS when verifying style changes.

## Content model

| Path | Role |
|---|---|
| `_pages/about.md` | Homepage: intro, news, selected publications |
| `_pages/publications.md` | Full-width plain list (`publications-plain` class hides badge/thumbnail column) |
| `_bibliography/papers.bib` | Only lead-author papers (first / co-first / corresponding). Non-lead papers live on Google Scholar only |
| `_includes/selected_papers.liquid` | Homepage selected list, grouped by `thread={machinery\|application}` |
| `_news/*.md` | Inline news items (homepage box scrolls at `max-height: 20rem`) |
| `assets/img/publication_preview/` | Paper thumbnails — uniform 1600×900 letterboxed JPEGs |

Adding/updating papers or thumbnails: follow the `add-publication` skill (`.claude/skills/add-publication/SKILL.md`) — it documents bib field conventions and the thumbnail normalization script.

## Design system (Frontis-VI derived)

Tokens in `_sass/_variables.scss` (`$frontis-*`), applied in `_sass/_themes.scss` / `_sass/_base.scss`:

- Links: 信息蓝 `#1A6FD4` (WCAG AA on white); hover: 流通青 `#0097B2`.
- 跃迁青 `#00C1D4` (`--global-edge-color`) is **structural only** — navbar 3px bottom line, thread-heading left borders. Never body/heading text (fails contrast; VI forbids it).
- 能量橙 `#FA5F26`: at most ONE occurrence per page (currently the "We are hiring interns!" line in about.md).
- Geometry: zero border-radius, zero box-shadow on profile photo, thumbnails, buttons, search input. Layers come from color and spacing, not shadows.
- Font: Inter (loaded in `_config.yml` google_fonts; body override in `_base.scss`). Footer background: pure black `#000000`.

## Conventions & gotchas

- Bib keys must be unique and semantic (`TTRL`, `MARTIMARS2`); preprint abbr is `arXiv` (not `Arxiv`).
- Deleted al-folio template content (Einstein pages, blog, projects, repositories, sample posts/images) — do not resurrect; keep new pages out of nav unless intentional.
- `selected={true}` entries need `thread=` + `preview=`; keep the homepage selection at ~8 papers.
- News entries: link the paper/repo; star badges via shields.io are acceptable in news only, never in bib entries.
