# IH, native actors and bridge safety

## Treat IH as a provider with capabilities

Infinite Heaven owns resources, allocation and many actor controllers. Immersive Mother Base can observe and adapt supported records, but should not assume every IH actor accepts the same commands as a normal Soldier2. Later private inspection observed additional adults as Hostage2; named story characters and children retained protected controllers. The provider family and capability must be explicit. A successful-looking API return is not proof of movement, work, service use or animation.

Adoption should be a capability-gated sequence: observe exact identity and generation; classify actor family; test read-only availability; request a single narrowly scoped action; observe position/status over time; then release ownership and prove return to the original controller. Keep automatic physical ownership off until each family/action pair passes. Logical identity or needs adoption alone does not establish physical control.

The later private IH provider recorded 16 logical adult/named records with no physical owners or proofs. Named Miller/Ocelot controllers and child records remained excluded. A mixed-group 0.2.5 candidate failed addressing preflight before movement; it must not be described as a walking trial or reinstalled unchanged. A later 5-second recorder sample did not identify animation IDs or verify a demonstration. These are evidence boundaries, not shipping features in alpha 0.1.0-alpha.1.

## Shared IHHook pipe hazard

Pinned IHHook r25 source at commit 924278894bab056e7d035abc3fbfe4bd726ad4ce was found to run output workers that can spin while idle, retain handlers after clients disconnect, and block on synchronous output/FlushFileBuffers when a client does not read. The paired local recovery measurement removed 32 workers and showed 59.775 rendered FPS in that same process. This identifies a real shared-pipe hazard; it does not prove every reported FPS incident has that cause.

An idle Sleep(10) plus disconnect checks addresses idle spin/disconnect polling only. It does not bound synchronous writes or flushes. The more complete output design uses a consistently overlapped output handle, a valid operation/event for connect/read/write, bounded waits, cancellation followed by observing terminal completion, and no flush as a delivery acknowledgement. Do not free an in-flight buffer or operation structure after merely requesting cancellation. Keep input polling behavior separate and nonblocking.

The full acceptance case is a connected client that remains open and unread while output becomes pending, then shutdown is requested. Measure exit and CPU; also test pending connect, both connection races, normal message framing, reconnect cleanup and input-empty behavior. A worker fix does not prove safe whole-DLL unload when synchronous input operations remain.

The project-source build repaired the development IHHook pipe lifecycle, but its DLL is not distributed in the public mod. Users should use the upstream IHHook release supported by their installed IH version and report the exact build when diagnosing performance.

## Safe native bridge recipe

Use the bridge as a bounded snapshot/command channel, not as implicit proof of action completion.

1. Send a small read-only observation request with an explicit response deadline.
2. Require matching request/session identity, mission-ready state and freshness metadata.
3. Reject stale, partial or wrong-generation observations.
4. Before an action, re-check current actor identity, native life and status on the game thread.
5. Correlate the response with a command sequence and observe the resulting state transition; a successful write or Lua return alone is insufficient.
6. Close both ends on success, timeout and error; serialize clients unless the transport explicitly isolates per-client queues.
7. Log only sanitized status and counts in public artifacts; keep raw process state and memory reads private.

## Upstream references

- [IHHook r25 PipeServer.cpp](https://github.com/kapuragu/IHHook/blob/924278894bab056e7d035abc3fbfe4bd726ad4ce/IHHook/PipeServer.cpp)
- [IHHook r25 SafeQueue.h](https://github.com/kapuragu/IHHook/blob/924278894bab056e7d035abc3fbfe4bd726ad4ce/IHHook/SafeQueue.h)
- Microsoft: [named-pipe modes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes), [overlapped server example](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-server-using-overlapped-i-o), [ConnectNamedPipe](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-connectnamedpipe), [CancelIoEx](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-cancelioex)

The source findings and recovery result above are private development observations. IHHook authorship and license remain governed by upstream; no IHHook source or binary is included here.
