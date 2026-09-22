---
name: cross-publish-art
description: >
  Cross-publish plaintext ASCII art from the legacy static gallery
  (../mozz) to the ascii.mozz.us art gallery. Use when the user wants to
  cross-publish, sync, mirror, or republish ASCII art entries from the
  legacy site to the new site.
---

# Cross-publish ASCII art

Mirror new plaintext art entries from the legacy static site
(`../mozz/public/ascii-art/`) to the ascii.mozz.us gallery. The heavy
lifting is done by `scripts/cross-publish-art` (run it from the repo
root). The user publishes on the legacy site first with its
`tools/publish-art` script, so the pre-rendered `.txt` files already
exist; this flow uploads the `.txt` and renders a fresh PNG display
image from it (Menlo, 2x retina, black on white — the legacy site's own
`.png` screenshots are NOT used because they contain TextEdit window
chrome).

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
reports up to three groups:

- **New entries to publish** — no art post exists on the new site yet.
- **Modified entries to republish** — the post exists but the entry's
  text changed since the last sync (compared against the live
  scrollfile served at /mozz/scroll/scrollfile.txt).
- **Published entries missing from the live scrollfile** — the post
  exists but the server's scrollfile hasn't been synced since it was
  published; fixed by sync-scrollfile in step 3.

If an entry is flagged `MISSING TXT`, the legacy build is stale — stop
and tell the user to run the legacy `tools/publish-art` first. If
everything is in sync, report that and stop.

### 2. Publish and republish (oldest first)

Work through the new entries oldest → newest so the gallery ordering
matches the legacy site. Before prompting, look for likely reference
images on the user's Desktop — reference images usually live there,
named after the entry:

```
ls -lt ~/Desktop/*.png ~/Desktop/*.jpg ~/Desktop/*.jpeg 2>/dev/null
```

Match candidates to entries by filename: the slug or title words
(`giraffe.png` for "Giraffe"), or an abbreviation of them (`p1.png` for
"Pose 1"). Recent modification times are a good tiebreaker — reference
images are typically saved around the legacy publish date.

Then, for each entry, use AskUserQuestion (one call, two questions):

- **Publish?** — show the date and title, ask whether to publish it now
  or skip it.
- **Reference image** — if a likely Desktop candidate was found, present
  it as the first option (label it with the filename and mark it
  "(Recommended)"), alongside "No reference image". If no candidate was
  found, just offer "No reference image". Either way the user can supply
  one or more other local paths via "Other" by typing or pasting the
  path. Dragging the file onto the terminal window does NOT work — it
  sends the raw file contents rather than the path, and a pasted image
  is equally unusable: the upload needs a real file path on disk. Note
  AskUserQuestion requires at least two options per question.

If the user answers with a bare filename (e.g. `p3.png`), check
`~/Desktop/` for it before giving up on the path.

Then, for entries the user approved:

```
scripts/cross-publish-art publish <slug> [--reference <path> ...]
```

This creates the art post (file type `text`, font `menlo`, visible)
with the pre-rendered `.txt` as the file and a freshly rendered PNG as
the display image, then uploads each reference image as an attachment
named "Reference #N". It refuses to overwrite a post whose slug already
exists — if that happens, surface the conflict to the user instead of
working around it.

For modified entries (or whenever the user tweaked an existing post's
artwork and wants it re-uploaded):

```
scripts/cross-publish-art republish <slug>
```

This re-uploads the `.txt` and a re-rendered PNG to the existing post,
leaving all other fields and attachments untouched.

Relay the printed public URL after each publish/republish so the user
can spot check the post in their browser.

### 3. Sync the scrollfile

After all approved entries are published (even if some were skipped):

```
scripts/cross-publish-art sync-scrollfile
```

This uploads the legacy `ascii-art.txt` to the server through the API
(a `ScrollFile` row in the database). It goes live immediately at
https://ascii.mozz.us/mozz/scroll/scrollfile.txt — no commit or deploy
is needed. The diff compares against this live copy to detect modified
entries.

### 4. Verify

Run `scripts/cross-publish-art diff` again — pending work should be
gone (skipped entries will still be listed). Give the user a short
summary: what was published or republished (with public URLs), what
was skipped, and that the scrollfile was synced.

## Notes

- Skipped entries keep showing up in the diff on later runs (the diff
  checks which art posts exist, not the scrollfile text), so skipping
  just defers a post until next time.
- Two legacy entries were imported under manually shortened slugs; the
  script's `SLUG_ALIASES` map resolves them to the existing posts so
  the diff skips them and `publish` refuses their legacy slugs.
- Post metadata (title, date, slug) is derived from the legacy
  scrollfile the same way the legacy site derives it, so the two sites
  always agree on slugs.
- To fix a bad upload, `republish <slug>` replaces the file and image;
  deleting the post (Django admin or
  `DELETE /api/v1/mozz-art-posts/<slug>/`) and publishing again is the
  fallback for bad metadata.
