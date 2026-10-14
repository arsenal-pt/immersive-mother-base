# Authored route resources — not enabled by default

250 owned waypoint definitions are in ../resources-authored/Route-Waypoints.json. AuthoredRoutes.cs starts an empty FoxLib RouteSet and writes only these routes; no game/template route archive is included. The coordinates and event IDs are editable source, not copied game packs.

The checked writer uses existing external FoxLib, FSharp.Core, CityHash and a .NET Framework C# compiler, passed explicitly. Binaries are not supplied. FoxKit hashing attribution/MIT notice is retained. Reviewed external projects: https://github.com/youarebritish/FoxKit and https://github.com/youarebritish/FoxLib. Matching tool builds are hash-gated by Build-Authored-Routes.py; dependency/source revision and notice completion for a combined native release remain open.

```powershell
python Build-Authored-Routes.py --foxlib "D:/Tools/FoxLib.dll" --fsharp "D:/Tools/FSharp.Core.dll" --cityhash "D:/Tools/CityHash.dll" --csc "D:/Tools/csc.exe"
```

Outputs go under ignored private-builds. This compiles/checks locally; it never downloads tools, installs a pack or starts MGSV. The XML pack list and disabled ImbRouteResources.lua are review templates. Native packing/admission, collision-safe routes, service motions and clean-package gameplay validation still need implementation. Do not enable the callback merely because serialization succeeds.
