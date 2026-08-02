---
name: bundle-artwork
description: >
  Download a mozz art post, identify its reference image via reverse image
  search, rewrite the SAUCE metadata, and stage MOZZ-*.XB/.png files for
  release. Use when the user wants to bundle, stage, or release artwork from
  ascii.mozz.us, or mentions preparing an art pack.
argument-hint: "[title or slug, e.g. 'Sketch 238']"
---

# Bundle artwork for release

Stage art posts from ascii.mozz.us as release-ready `MOZZ-*.XB` + `MOZZ-*.png`
file pairs in `~/Desktop/staging/`. The heavy lifting is done by
`scripts/bundle-post` (run it from the repo root). The user typically bundles
10+ posts in one sitting, so loop the whole procedure until they say they are
done.

Requires `ASCII_SERVER_BASE_URL` and `ASCII_SERVER_API_TOKEN` in the
environment (already set in the user's shell) and the `ansilove` CLI.

## Procedure (repeat per post)

### 1. Fetch

```
scripts/bundle-post fetch "<slug or title>"
```

This downloads the `.xb` file and reference image(s) into
`~/Desktop/staging/.work/<slug>/`, validates the XBIN is not corrupted,
prints the existing SAUCE record, and prints a Google Lens URL for each
reference image. If the lookup is ambiguous, it lists the matches; run
`scripts/bundle-post search "<term>"` to explore, then fetch an exact slug.

Moebius Beyond has a bug where it writes a fontsize of 0 in the XBIN header
even though a 16-scanline font is embedded; fetch repairs this automatically
(it prints a "Repaired XBIN header" line) and the staged file gets the
corrected header. Any other validation failure means the source file is
genuinely corrupt — stop and show the user the error.

### 2. Reverse image search

If the post has a reference image, open the printed Google Lens URL in Brave
so the user can identify the source artwork:

```
open -a "Brave Browser" "https://lens.google.com/uploadbyurl?url=..."
```

Do NOT open or analyze the reference image yourself — identifying the
source artwork (artist, title, year) is the user's job via the Lens
results. After opening the URL, ask the user what the search turned up.

If there is no reference attachment, skip this step and the SAUCE comment.

### 3. Ask the user for the metadata

Use AskUserQuestion (one call, three questions), building options from what
is known so far:

- **Title** — the SAUCE title, max 35 bytes. Offer the existing post title
  as one option, but the user usually renames the piece after the source
  artwork the reverse search turned up (e.g. "Arizona Cannonball").
- **Filename** — offer the full title slug and a shorter punchy variant.
  The convention is a 1-2 word stem: "Arizona Cannonball" became
  `MOZZ-CANNONBALL`, "After a Summer Rain" became `MOZZ-AFTER_RAIN`.
- **Comment** — the SAUCE attribution comment, max 64 bytes per line.
  House format: `Based on "On Bar Island" (ca 1944) by Andrew Wyeth.`
  Offer "no comment" for original works. Once the user has identified the
  source in step 2, construct the comment for them.

### 4. Finalize

```
scripts/bundle-post finalize <slug> \
    --title "Arizona Cannonball" \
    --filename CANNONBALL \
    --comment 'Based on "Arizona Cannonball" by Mark Maggiori (2025).'
```

This rewrites the SAUCE record (author `mozz`, group `mistigris`, date =
today), re-validates the XBIN, verifies the artwork bytes are untouched and
the SAUCE round-trips, writes `MOZZ-CANNONBALL.XB` + `MOZZ-CANNONBALL.png`
to `~/Desktop/staging/`, and opens the PNG in Preview for a spot check.
`--comment` is repeatable for multiple lines; `--force` overwrites already
staged files; `--date YYYYMMDD` overrides the SAUCE date.

### 5. Confirm and continue

Relay the verification summary, ask the user to spot-check the Preview
window, then ask which post is next (or fetch the next one if they gave a
list up front). If something looks wrong, the original download is still in
`~/Desktop/staging/.work/<slug>/` — the user can edit it in Moebius Beyond
(`open <file> -b org.michaellazar.moebius-beyond`) and finalize again with
`--force`.

## Notes

- `scripts/bundle-post verify <file.xb>` re-checks any staged file
  (XBIN structure, SAUCE consistency) if the user asks for an audit.
- The `.work/` directory is scratch space; it is safe to delete after the
  bundle ships.
- Never edit the artwork bytes; this workflow only touches SAUCE metadata
  (plus the fontsize header repair described in step 1).
