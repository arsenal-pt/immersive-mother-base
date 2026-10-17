# Readable asset names and presentation

The public category tables and the configured local tool use the same pure formatter and naming registry. This is descriptive metadata, separate from model/render/completion identity. The public repository contains this standalone library generator; newer configured whole-game tool integration remains local development until separately released.

## Refresh the public library locally

After cloning this repository, use an installed Python 3 interpreter:

```text
python research/asset-library/build-library.py
python research/asset-library/build-library.py --check
```

The generator reads existing catalogue.json and naming-registry.json and writes readable Markdown plus display-catalogue.json/display-catalogue.csv. It neither extracts game assets nor launches converters/Blender, copies media, writes a processing database or changes accepted source/proof records. No AI, MCP, server or network is needed. The published media must already be present for local image viewing.

The original catalogue.json/catalogue.csv and source/provenance/completion files remain unchanged technical evidence. Readable JSON/CSV are separate views. Editing a friendly name does not rename a Library ID, game filename, variant, LOD or media file.

## Update a readable label

Edit naming-registry.json. An exact Library ID override wins, then an exact native-path override, then the most specific approved folder/family rule. Preserve reviewed overrides; never replace them automatically with a weaker rule. Each entry has display_name, category/subcategory, tags, plain description, naming_status, confidence and evidence.

Use reviewed for a confirmed preview label, path-derived for conservative source-folder inference and unidentified when the object has not been identified. Naming review is separate from render status: unknown names do not fail, reset or repeat completed jobs.

Keep descriptions about evidenced appearance/component scope. Do not claim folding, movement, climbing, collision, interaction or complete assembly from a static preview. A broad folder rule never supplies an unreviewed color/purpose. Exact variant tokens remain separate from native LOD.

## Shared module

The pure interface is presentation.present(record, registry), render_table(views, context), render_detail(view, context) and render_index(views, category_links, context). It accepts either library source.nativePath or pipeline modelPath records, creates separate views and never mutates inputs. Callers supply existing local or verified remote media/detail links. Tables enforce at most twelve static thumbnails; the index has no images.

The configured local integration writes friendly accumulated/current-batch pages outside immutable raw bundles and points to their existing media. O/A should open those friendly pages; original bundles remain source/advanced links. This does not make local unreleased tool code downloadable from the public library.

Credits and source limits remain in [central credits](sources-and-credits.md) and each reference's technical view. [Browse categories](README.md).
