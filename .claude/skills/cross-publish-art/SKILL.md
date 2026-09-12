---
name: cross-publish-art
description: >
  Cross-publish plaintext ASCII art from the legacy static gallery
  (../mozz) to the ascii.mozz.us art gallery. Use when the user wants to
  cross-publish, sync, or mirror new ASCII art entries from the legacy
  site to the new site.
---

# Cross-publish ASCII art

Mirror new plaintext art entries from the legacy static site
(`../mozz/public/ascii-art/`) to the ascii.mozz.us gallery. The heavy
lifting is done by `scripts/cross-publish-art` (run it from the repo
root). The user publishes on the legacy site first with its
`tools/publish-art` script, so the pre-rendered `.txt` and `.png` files
already exist; this flow only uploads them.

Requires `ASCII_SERVER_BASE_URL` and `ASCII_SERVER_API_TOKEN` in the
environment (already set in the user's shell). The legacy project is
assumed to be a sibling checkout at `../mozz`; pass `--legacy-root` if
it lives elsewhere.

## Procedure

### 1. Diff

```
scripts/cross-publish-art diff
```

This parses the legacy scrollfile (`../mozz/public/ascii-art.txt`) and
lists the entries that do not yet exist as art posts on the new site,
newest first. If an entry is flagged `MISSING TXT` or `MISSING PNG`,
the legacy build is stale — stop and tell the user to run the legacy
`tools/publish-art` first.

If there are no new entries, report that and stop.

### 2. Publish each entry (oldest first)

Work through the new entries oldest → newest so the gallery ordering
matches the legacy site. For each entry, use AskUserQuestion (one call,
two questions):

- **Publish?** — show the date and title, ask whether to publish it now
  or skip it.
- **Reference image** — ask whether they have a local reference image.
  Offer "No reference image" as an option; they can supply one or more
  local paths via "Other".

Then, for entries the user approved:

```
scripts/cross-publish-art publish <slug> [--reference <path> ...]
```

This creates the art post (file type `text`, font `menlo`) with the
pre-rendered `.txt` as the file and `.png` as the display image, then
uploads each reference image as an attachment named "Reference #N". It
refuses to overwrite a post whose slug already exists — if that
happens, surface the conflict to the user instead of working around it.

Relay the printed public URL after each publish so the user can spot
check the post in their browser.

### 3. Sync the scrollfile

After all approved entries are published (even if some were skipped):

```
scripts/cross-publish-art sync-scrolls
```

This pushes the full text of the legacy `ascii-art.txt` to the
`scrollfile` scroll-file API endpoint, keeping
https://ascii.mozz.us/mozz/scroll/scrollfile.txt in step with the
legacy site.

### 4. Verify

Run `scripts/cross-publish-art diff` again — it should report no new
entries. Give the user a short summary: what was published (with public
URLs), what was skipped, and that the scroll files were synced.

## Notes

- Skipped entries keep showing up in the diff on later runs (the diff
  checks which art posts exist, not the scrollfile text), so skipping
  just defers a post until next time.
- Two legacy entries were imported under manually shortened slugs and
  will always appear in the diff — always skip them, never republish:
  `mushroom-hut-for-fungi-neocities-org` (exists as
  `mushroom-hut-neocities`) and
  `a-sunday-afternoon-on-the-island-of-la-grande-jatte-1884` (exists as
  `a-sunday-afternoon-on-the-island-of-la-grande`).
- Post metadata (title, date, slug) is derived from the legacy
  scrollfile the same way the legacy site derives it, so the two sites
  always agree on slugs.
- To fix a bad upload, delete the post in the Django admin (or via
  `DELETE /api/v1/mozz-art-posts/<slug>/`) and publish again.
