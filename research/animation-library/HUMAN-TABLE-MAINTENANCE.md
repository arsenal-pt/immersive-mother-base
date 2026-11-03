# Maintaining the single-table animation library

The public browser is static HTML/CSS/JavaScript. It loads a compact metadata index containing every original field-name/scalar search token, then one original-record shard when Details is opened. Search terms combine with AND across the entire original entry. Repeated or substring-contained tokens are deduplicated; a shared token dictionary avoids repeating common metadata text in every row. The browser hydrates the same substring-search strings in memory. Preview opens one still; Play GIF explicitly replaces it with the original titled GIF. Media URLs and technical links point at an immutable, reviewed GitHub commit. The browser includes no analytics, external fonts, application server or account system.

## Source of truth and update sequence

1. Preserve `catalogue.json`, `catalogue.csv`, original records, media, credits and all legacy clip/table/source-group URLs. The browser reorganizes this data; it grants no extraction, rendering or native-test authority.
2. For a newly reviewed catalogue, update the exact source commit, catalogue SHA256/Git blob/byte count and expected entry count in `human-table-config.json`. The current baseline is 1,299 IDs at `3e1ed2fbe3886604cf84fa6ae7d4118b7dbb6e3f`. Do not inherit old pins when catalogue data changes. Character/moveset stay Unknown unless the authoritative schema gains directly evidenced fields and the mapper is reviewed.
3. Generate into a new directory, without reading or copying media:

   ```console
   python -B research/animation-library/build-human-table.py --catalogue research/animation-library/catalogue.json --config research/animation-library/human-table-config.json --output <absent-output>/animation-library
   node research/animation-library/test-human-table.mjs <absent-output>/animation-library --full-metadata-only
   ```

   The builder checks exact source pins, one-to-one IDs and complete original-entry/header roundtrips. Its build report lists every retained media reference without opening media files. The current focused contracts prove all1,299 IDs, every original key/scalar search token, a unique nested originalRecords hash and an evidence-key/boolean AND query. Earlier contracts/browser evidence cover numeric ordering, unknowns, pagination and shared URL state; rerun affected suites when behavior changes. The retired organizer's previous test suite is not part of this build.
4. Review the code and generated file allowlist/hashes. Keep `BUILD-REPORT.json` as evidence outside the public website. Publish only `index.html`, `style.css`, `app.mjs`, `core.mjs`, `.nojekyll` and `data/*.json`; source files remain in this repository. Serve via HTTPS. Do not upload raw game files, source scenes, native binaries, saves, local control files or cache.
5. Confirm a live public URL before setting the README's **Open Library** link. GitHub Markdown does not execute this browser's JavaScript. GitHub Pages supports these static files; confirm the repository's Pages setting rather than assuming it is enabled. A static host can also serve the exact reviewed output while GitHub remains authoritative for data and media. The app works at the root or a subpath; all local fetches are relative.
6. Verify the deployed URL on desktop/mobile, search, filters, numeric sort, URL reload, row details and keyboard/Escape. Network should show zero initial image/GIF requests, a single still after Preview, then one GIF after Play. Preserve practical limitations: native timing/character compatibility/all-game completeness are not established, and sampled review is not continuous review.

## Cloud generation and publication

`.github/workflows/animation-library-human-table.yml` generates a reviewable artifact for the scoped same-repository PR. It sparse-fetches metadata and authored browser sources only, runs the new dataset contracts and uploads a static overlay plus report. It has read-only repository permissions and does not push or deploy. Root reviews the exact artifact against the output manifest, then publishes/configures the selected host separately.

For GitHub Pages deployment, upload the reviewed static directory using GitHub's `upload-pages-artifact` and `deploy-pages` actions in a separately reviewed workflow with `pages: write`, `id-token: write` and the `github-pages` environment. Choose trusted, explicitly pinned action revisions and use the already configured Pages source. Do not enable Pages, add a custom domain, change a repository's website or overwrite an unrelated existing site by assumption.

## Superseded navigation

`organize-library.py` is retained for history/reference but its command-line entry point is retired. Its old cloud workflow only reports retirement. New updates use `build-human-table.py`; they do not regenerate 29 source directories and hundreds of separate GIF/still browse pages. The short library README is maintained directly after the host URL is verified. If the older extraction builder is needed for a separately authorized catalogue update, review its generated documentation and retain the short README; do not publish a verbose generated README or rerun the retired organizer. Original media, source records and existing legacy pages remain unchanged.

Implementation follows [GitHub Pages static hosting](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) and [W3C's semantic sortable-table guidance](https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/). Keyboard and responsive browser QA is recorded separately; no screen-reader-specific certification or native gameplay proof is claimed.
