# Current asset-library plan - 16 October 2026

The reviewed library now has 10 parent models and 19 actual preview views: original three seating families/all12LODviews, plus five user-generated and two earlier shelf references at LOD0. Higher native LOD inventory for the seven imports is metadata, not completed previews. All existing clean sources/media are preserved; no new extraction or rendering is required to publish this batch.

Continue using the seven practical categories below, semantic search tags, plain-English descriptions, exact retained paths/hashes, central/detail credits, zero-image index, at most12static thumbnails/table page, and a single full GIF per selected detail view. Native model components must not be described as complete assembled or interactive objects without evidence.

The new whole-game goal supersedes the earlier parked status: first catalogue the as-installed archive/member metadata with explicit known/unknown paths/types and membership, then join native dependencies and process user-sized preview batches. Catalogue coverage and preview/assembly coverage must remain separate. Source API/read-only feasibility research precedes implementation approval. No full-game unpack/render has begun. The current local automatic queue still covers149retained versions only.

## Original bounded pilot plan (historical scope)

# Asset reference library plan

Status: three selected Furniture > Seating reference entries prepared and reviewed offline (16 October 2026); category completeness is not established. This is a visual reference library, not a downloadable asset pack. The separate full-game catalogue was parked at this pilot checkpoint; the current plan above supersedes that status.

## Scope and working order

1. Reuse a small, explicitly selected set of already retained private models and textures. No new game extraction is authorized for this pilot.
2. Record the real native model path, SHA256, chosen variant/LOD, texture bindings and container evidence while reading the source. Unknown locations stay null; historical receipts do not certify current installed archive contents.
3. Render one textured still and four small review angles; inspect the sample before batching.
4. Complete exactly three references: one still, one full360 camera-orbit GIF and one small static thumbnail per asset. Preserve clean stills/frames before any labels or overlays. This turntable is a reference-camera movement, not an animation supplied by the game.
5. Publish only previews, descriptive metadata and authored recipes after review. Do not publish Konami models, textures, archives, decoded geometry, blends or tool binaries.
6. Save the plan, coverage/remaining IDs, provenance, limitations and bounded verification in the project history. Stop after this selected set. A larger category or new extraction needs a later assignment.

## Taxonomy

Primary categories describe what an asset is. Tags describe useful traits and possible uses; a use tag is not proof that a native game interaction exists. Preserve the game's path/variant identity independently of friendly names.

| Category | Example subcategories |
|---|---|
| Architecture | platform sections; walls/floors/ceilings; doorways/windows; stairs/ladders/railings |
| Furniture | seating; beds/bedding; tables/desks; lockers/storage |
| Equipment | radios/electronics; tools/workstations; medical equipment; lighting/fixtures |
| Logistics | crates/pallets; fuel/water; cargo/supply handling |
| Vehicles | ground vehicles; aircraft; boats; components |
| Characters | bodies/uniforms; heads; wearable gear; assembled variants |
| Environment and markings | vegetation; rocks; signs; decals |

Start with Furniture > Seating: retained mtbs_char002, cypr_char001 and cypr_whch001. Their intended friendly labels must be confirmed from visuals. These three do not establish completeness of Seating, the retained private library, or the game.

## Browsing and visual budget

The category index contains zero images. A category table loads static 160px thumbnails only, with at most 12 rows per page; links open a larger per-asset page. Each detail page contains one clean 768px still and one 480px turntable GIF (48 angles at 7.5degree increments,100 ms/frame,4.8-second loop). No animated thumbnail is loaded by the index or default table. Do not rely on a collapsed HTML section to prevent image loading. Prefer light neutral/white backgrounds; change to contrasting gray when a pale model needs it. Keep one fixed scale/framing through each orbit and include the whole silhouette.

Use existing Blender/Python tooling and retained decoded LOD0 geometry. Actual base-color DDS textures and UVs should be used; native material/shader equivalence remains a separate claim. Stop and label missing or ambiguous textures instead of substituting a guessed texture or silently showing inspection colors.

## Data and evidence

Each record keeps stable native path+full SHA256 identity, friendly title, Category, semantic Tags, plain-English Description, source namespace and observed uses, native bounds, selected LOD, model path and container chain with verification status. Material entries record sampler/hash identity and the exact selected DDS content hash; public metadata does not include texture pixels.

Source ownership/tool credits live centrally and on detail/source pages, not in browsing table columns. Separate direct source checks, historical extraction receipts, dictionary-resolved names, authored visual labels and unknowns. Current DAT membership must never be inferred from a copied loose file. Keep private local paths, raw inputs and clean render receipts out of public records.

The public format should remain portable JSON/CSV/Markdown so it can later move into a separate reference project. That separate repository is not created by this pilot.

## Completion checks

Verify exactly three selected identities, original/retained-input hashes unchanged, texture content/UV mapping, expected LOD0 counts, clean still/frame hashes, full orbit/loop/frame timing, readable thumbnails, every relative link, UTF8/JSON consistency and absence of raw asset files/private paths. Check software build inventories exclude preview media without rebuilding releases. Review source/preview claims separately from native gameplay acceptance; no game launch, install or native model modification belongs to this task.

## Existing-three quality continuation -16October2026

This selected continuation adds all9lower native LOD references for the existing three asset identities, reuses their accepted LOD0media unchanged and completes12nativeLODviews. It does not start a new asset family. Per asset: static four-LOD comparison, separately linked still/360GIF for each distinct native face set, Quality/LOD/triangle annotations and actual texture pixels/native mips. Hold source bounds/camera/base texture fixed so the comparison isolates geometry. No new extraction, synthetic higher detail, upscaling, mip Cartesian product or shader recreation.

Measured scope: chair358/270/196/150triangles; stool196/160/140/128; wheelchair1588/1452/1384/1344. Each family has one retained native model content identity despite duplicate source records; all fourLODface sets differ. Retained base maps are512x256/8mips,256x128/7mips and1024x1024/9mips respectively. Source headers/LODs were checked directly and exact retained mappings are in quality-provenance.json. No larger retained alternative was found within these inspected inputs. Whole-game completeness and native runtime selection remain unverified.

The default index remains image-free; category table still loads only3static parent thumbnails. Parent detail pages show a static comparison/table and only their existing LOD0GIF; each lower-LOD child page loads its own selected GIF. New assets wait until this exact selected quality scope is finished or explicitly reprioritized.
