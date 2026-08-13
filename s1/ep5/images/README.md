# Images for Episode 5

Drop the YANGSuite screenshots referenced by the episode README here. The main
[`../README.md`](../README.md) embeds them with relative links like
`![...](./images/<file>.png)` — match these filenames (or update the links) so
they render:

| Filename | Suggested screenshot |
|----------|----------------------|
| `yangsuite-device-profile.png` | The YANGSuite **Device Profile** for the Catalyst 8000v (host/port 830, NETCONF creds) — right after a successful connectivity test. |
| `yangsuite-module-load.png` | The **YANG module set** loaded, with `Cisco-IOS-XE-native` selected. |
| `yangsuite-hostname-node.png` | The explorer expanded to `native > hostname`, with the node selected. |
| `yangsuite-hostname-rpc.png` | The generated **`<edit-config>` RPC** XML for setting the hostname. |
| `yangsuite-interface-list.png` | The explorer expanded to `native > interface`, showing the interface **lists** (GigabitEthernet, Loopback, …). |
| `yangsuite-loopback-node.png` | `native > interface > Loopback` expanded to the `ip > address > primary` leaves. |
| `yangsuite-loopback-rpc.png` | The generated **`<edit-config>` RPC** XML that creates Loopback100. |
| `yangsuite-rpc-reply.png` | A device **`<rpc-reply>`** — an `<ok/>` after a write, or returned data after a `get-config`. |

> PNG or JPG both work. Keep them reasonably sized (a 1400px-wide capture is
> plenty) so the repo stays light.
