# Paz, Huey and Battle Gear spaces

## Keep source placement separate from intended use

Paz's architectural room is resident Medical-platform content. Her visit pack contains conditional actors, animations, book/photo props and state control; it is not the room shell. Preserve the real/phantom/bed/door/photo state variants and original visit triggers.

The Huey/Battle Gear hangar crosses coordinate frames: the inner hangar door is transformed through Command/plnt0, while the outer portal is transformed through Develop/plnt0. The mission pack also contains a fixed interior warp. Intended department, source-world anchor, interior frame, exit frame and target placement are separate facts. Do not relocate a shell using the portal offset alone.

Private editor inventory saved Paz and six hangar variants and curated 149 static model versions, reusing 98 existing versions and extracting 51 additional versions. This was editor-level inventory and reopen verification. It did not prove native export, physical relocation, collision, NPC navigation, streaming, lighting, LOD, story compatibility or performance. Twenty-four light orientation records and multiple runtime references remained unresolved in the source evidence.

## Future integration sequence

1. Confirm current platform grade, source coordinate frames, exact entry/exit anchors and footprint.
2. Check whether a shell already exists and only props or collision are conditional.
3. Preserve original cutscene and mission resources. If moving a room, account for every dependent camera, actor, trigger, warp and exit.
4. Keep stock room state and custom room state mutually exclusive through verified loading/visibility conditions.
5. Gate the room by the correct department grade; early grades need an explicit unavailable or fallback path.
6. Validate model/material import, collision, navigation, light, LOD, streaming, traversal, story behavior and FPS separately.
7. Only after the room shell and path pass should reused industrial furniture or room assets be placed in other interiors.

For target bounds, broad-phase AABB intersection is a reservation warning, not proof of render/collision overlap. Preserve static models separately from characters, Battle Gear state, cameras, triggers and cutscene controllers. Do not duplicate dynamic mission logic into a furniture library.

## Primary references

- [Community report: Battle Gear hangar location](https://www.reddit.com/r/metalgearsolid/comments/3o3idu/mgsv_battle_gear_hanger_is_not_on_rd_platform/) — discovery lead only; native source transforms are the stronger placement evidence.
- [FoxKit](https://mgsvmoddingwiki.github.io/FoxKit/)
- [FMDL Studio V2](https://mgsvmoddingwiki.github.io/FMDL_Studio_V2/)

The room transform and inventory findings are private source/editor observations. Game archives, room scenes, textures and placement manifests remain private and are not included.
