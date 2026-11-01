# MeshCore region scopes for Texas: draft proposal

_Draft for discussion · updated 2026-11-01 · adapted and simplified from the PNW region strategy at https://gessaman.com/meshcore/regions/_

![Texas region scope map](texas-region-scopes.png)

## Hierarchy

`us-south` and `us-gc` are top-level scopes on the same level as `us`, with no parent. They're broad scopes for wide-area traffic, and the names match what mesh groups in neighboring states already use. `us-tx` sits under `us` and covers the whole state. Under `us-tx` are five statewide regions that together cover every county, and each metro scope sits under the region it's in.

| Scope | Name | Parent | Covers |
|---|---|---|---|
| `us` | United States | (root) | Whole country |
| `us-south` | South | (root) | Broad, high-level scope for wide-area communication across southern states. Shared with neighboring states' meshes |
| `us-gc` | Gulf Coast | (root) | Broad, high-level scope for wide-area communication along the Gulf Coast. Shared with neighboring states' meshes |
| `us-tx` | Texas | `us` | All of Texas |
| `us-tx-north` | North | `us-tx` | The Metroplex and the Red River towns (29 counties) |
| `us-tx-east` | East | `us-tx` | Piney Woods plus the Gulf Coast from Galveston to the Golden Triangle (53 counties) |
| `us-tx-central` | Central | `us-tx` | I-35 corridor from Waco through Austin to San Antonio, Hill Country and Brazos Valley (47 counties) |
| `us-tx-south` | South | `us-tx` | Coastal Bend, the border and the Rio Grande Valley (35 counties) |
| `us-tx-west` | West | `us-tx` | Panhandle, South Plains, Permian Basin, Big Bend and Big Country, Amarillo to El Paso (90 counties) |
| `us-tx-dfw` | Dallas–Fort Worth | `us-tx-north` | DFW metro plus edge counties (22 counties) |
| `us-tx-dal` | Dallas | `us-tx-dfw` | Collin, Dallas, Denton, Ellis, Hunt, Kaufman, Rockwall · edge: Fannin, Grayson, Henderson, Navarro, Van Zandt |
| `us-tx-ftw` | Fort Worth | `us-tx-dfw` | Johnson, Parker, Tarrant, Wise · edge: Cooke, Hill, Hood, Jack, Palo Pinto, Somervell |
| `us-tx-aus` | Austin | `us-tx-central` | Bastrop, Caldwell, Hays, Travis, Williamson · edge: Blanco, Burnet, Lee, Milam |
| `us-tx-sat` | San Antonio | `us-tx-central` | Atascosa, Bandera, Bexar, Comal, Guadalupe, Kendall, Medina, Wilson · edge: Frio, Gillespie, Gonzales, Karnes, Kerr |
| `us-tx-hou` | Houston | `us-tx-east` | Austin, Brazoria, Chambers, Fort Bend, Galveston, Harris, Liberty, Montgomery, San Jacinto, Waller · edge: Colorado, Grimes, Matagorda, Walker, Washington, Wharton |

Each metro starts from its OMB Metropolitan Statistical Area counties (Dallas and Fort Worth use the two MSA divisions) and adds the outlying counties along its edge, so repeaters on the fringe join the metro instead of only their region. The edge counties are a first pass and easy to adjust. El Paso, the Valley and other areas without a metro scope use their region scope until a local community asks for a metro scope.

The five regions come from the "Texas in Five" proposal. Every county belongs to exactly one region, and the core counties of each metro are never split between regions. Each metro sits under the region that holds its core counties, but a few of the edge counties added above fall in a neighboring region: Van Zandt and Henderson (`us-tx-dal`) are in East, Navarro (`us-tx-dal`) and Hill (`us-tx-ftw`) are in Central, Frio and Karnes (`us-tx-sat`) are in South, and Grimes, Washington and Colorado (`us-tx-hou`) are in Central. A repeater in one of those counties carries its own region plus the metro's full chain, including the metro's region. For example, a Henderson County repeater carries `us-tx-east`, then `us-tx-north`, `us-tx-dfw` and `us-tx-dal`.

## What can sit under `us-tx`

Only the five statewide regions sit directly under `us-tx`: `us-tx-north`, `us-tx-east`, `us-tx-central`, `us-tx-south` and `us-tx-west`. Together they cover every county.

Every other Texas scope sits under the region it's in (or under a metro in that region, like `us-tx-dal` under `us-tx-dfw`), and has to be one of these kinds:

1. **A major metro area.** This is a metro scope named for the whole area, such as `us-tx-dfw` for Dallas–Fort Worth.
2. **A grouping of IATA codes.** This joins neighboring airport-code areas under one scope, such as a future `us-tx-rgv` grouping the Harlingen (HRL), McAllen (MFE) and Brownsville (BRO) areas.
3. **A single IATA code.** This is one city or area named by its airport code, such as `us-tx-hou`, `us-tx-dal`, `us-tx-ftw`, `us-tx-aus` or `us-tx-sat`.

Areas that don't fit one of these stay in their region until they do. Future scopes follow the same rule, for example `us-tx-elp` (El Paso) under `us-tx-west`, and `us-tx-crp` (Corpus Christi) or `us-tx-rgv` (Rio Grande Valley) under `us-tx-south`.

## What we kept from the PNW document

- **Flat, lowercase names.** Use only a–z, 0–9 and `-`. Every scope below `us-tx` is named `us-tx-` plus one short code: a region name (`us-tx-north`), a metro or grouping code (`us-tx-dfw`) or an IATA code (`us-tx-hou`). The name never spells out the full chain, so Dallas is `us-tx-dal` even though it sits under `us-tx-dfw` and `us-tx-north`. The hierarchy comes from the parent field, not the name. Above `us-tx`, names match the ones neighboring meshes already use (`us-south`, `us-gc`). Names have to be unique across the mesh.
- **Every repeater carries its full ancestry.** Firmware matches traffic on each region's own key and never looks at the parent. A repeater with only `us-tx-dal` won't forward `us-tx-dfw`, `us-tx-north` or `us-tx` traffic, so each level needs its own `region put`.
- **Scope to your audience.** Use the smallest scope that reaches the people you're talking to. Local chat goes on `us-tx-dal`/`us-tx-ftw`/`us-tx-aus`/`us-tx-sat`/`us-tx-hou`, metro-wide traffic on `us-tx-dfw`, regional traffic on a `us-tx-<region>` scope, and statewide traffic on `us-tx`. Bots should flood on a scope, never unscoped.
- **No airtime cost.** Region names never go over the air. Packets carry only small transport codes derived from the region name.

## Example repeater configs

Dallas repeater (firmware 1.15.0+):

```
region put us
region put us-south
region put us-gc
region put us-tx us
region put us-tx-north us-tx
region put us-tx-dfw us-tx-north
region put us-tx-dal us-tx-dfw
region save
```

San Antonio repeater:

```
region put us
region put us-south
region put us-gc
region put us-tx us
region put us-tx-central us-tx
region put us-tx-sat us-tx-central
region save
```

Every Texas repeater carries `us`, `us-south`, `us-gc` and `us-tx`, so wide-area traffic on the broad scopes reaches the whole state. Every Texas repeater also carries the one region its county is in. A rural repeater outside any metro stops after its region, for example `region put us-tx-west us-tx`. A Houston repeater ends with `region put us-tx-east us-tx` and `region put us-tx-hou us-tx-east`. On firmware 1.14.x and earlier, add `region allowf <name>` after each `put`.

**Keep unscoped traffic for now.** Unscoped traffic uses the reserved root region `*`, and repeaters allow flood on it by default. Do not remove or deny flood on `*` on any repeater yet. Many nodes run older firmware or haven't set a region scope, and they still depend on unscoped flood. We'll decide on a later date for removing `*` once region scopes are widely adopted.

**Config tooling comes later.** Once there's enough agreement on the rules for how regions work and how they're defined, we can build tooling to generate the exact list of commands each user needs to enter on their repeater. Until then, use the examples above as a template.

## Scoping per channel

Repeaters carry the region tags, but the scope a message is sent on is chosen by the sender. Companions (phones) don't hold region tags themselves. Instead, each channel can have its own scope (Set Region Scope on the channel), and there's an app-wide default for everything else in the main Settings screen under Network Settings.

This lets each channel match its audience:

| Channel | Suggested scope | Why |
|---|---|---|
| Public | `us-tx` or unscoped (`*`) | General chat that anyone in the state should be able to see |
| `#weather` | Local metro or city, e.g. `us-tx-dfw` or `us-tx-aus` | Alerts for Houston aren't useful in Dallas |
| `#bot` | Local metro or city, e.g. `us-tx-hou` or `us-tx-sat` | Bot replies and automated posts stay near the people using them |

A Fort Worth user might keep Public on `us-tx`, set `#weather` to `us-tx-dfw` and set `#bot` to `us-tx-ftw`. They still see statewide chat, but they won't get weather updates or bot output from Austin or Houston.

**Not every area needs its own scope.** Most conversation can stay in a metro scope, a region scope or `us-tx`. An area only needs its own scope once it starts seeing excessive unwanted traffic from elsewhere. Until then, it's simpler to use its region scope and add a local scope later if it's needed.

## Open questions

1. **Aligning with neighbors on `us-south` and `us-gc`.** Both are broad, high-level scopes for wide-area communication, not local traffic, and are already in use by mesh groups in neighboring states. Every Texas repeater carries both. We should confirm with those groups that the names and intended use match.
2. **Uppercase vs lowercase.** The original ask used DFW. The convention is lowercase, so this draft uses `us-tx-dfw`.
3. **Edge counties.** Are the right outlying counties included? Bell (Killeen–Temple) and Jefferson (Beaumont) have no metro scope yet and use their region (Central and East).
4. **Next metros.** Likely candidates for the next scopes are El Paso (`us-tx-elp`), the Rio Grande Valley (`us-tx-rgv`) and Corpus Christi (`us-tx-crp`). Should `us-tx-hou` get sub-regions?
5. **Ratification.** Who signs off on new scopes, so names stay unique and agreed?
