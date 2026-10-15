# Identity, hierarchy and changing rosters

## Stable identity before display name

A roster row, displayed actor number, face, rank and codename are not reliable identity keys by themselves. Use the native staff identity/generation as the key where observed; keep display-name changes separate from identity, needs, relationships and military appointments. Duplicate codenames can belong to different people. A missing or unsupported name should remain an honest unresolved label.

Private development source research observed native codename resolution for the tested game build using a read-only process reader with bounded pointers and checked signatures. The exact native name algorithm depended on staff identity, a unique-staff table or seeded language components and a gender bit. This is build-specific local observation, not a general public API or a recipe to read arbitrary game memory. The public project should prefer supported mod interfaces and fail closed when the installed build or data is unknown.

## Dynamic roster reconciliation

Treat the live roster as changing input. Actors can be absent, streamed out, captured, dead, replaced, or allocated into a new generation. Cache entries need identity, generation, mission/cluster and capture time. Drop observations on allocation/ownership change. An incomplete snapshot cannot promote a person to available. Validate current life/status again just before sending an engine action.

Keep persistent simulation state keyed to stable staff identity across roster ordering changes. A temporary missing native actor should not erase needs/history or allow its old command to target a replacement. On return, reconcile exact identity and restore only supported state.

## Rank and appointment ceilings

Simulated rank is separate from MGSV ability grade. Appointment is a position a qualified person holds; a vacant position remains vacant until a qualified person is available. The project's hierarchy rule is bounded by rank: privates serve as soldiers, corporals can lead teams, sergeants can lead squads, and officer ranks qualify for platoon leadership. Rank does not change just because a slot is vacant or the actor is absent.

This is an authored organizational model, not a claim that the game uses these appointments for its own combat ability. Never promote a native rank or ability value to make a simulation appointment fit.

## References and limits

The private native name work referenced V Framework's day3900 address map and MGSV Modding Wiki language/tool documentation. The work was tested against one owned executable and its matching language data; no address, native name catalogue or memory dump is included here.

- [V Framework address set, pinned revision](https://github.com/Yazed0071/V_Framework/blob/7d29e15ea1e370d750a3f1becb085c47d56ed20f/src/core/AddressSet_day3900.cpp)
- [MGSV language files](https://mgsvmoddingwiki.github.io/Lang_Files/)
- [LangTool](https://mgsvmoddingwiki.github.io/LangTool/)
