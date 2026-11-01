# Renders texas-region-scopes.png. Usage: python3 tools/render_map.py <us-counties.geojson> <out.png>
# County GeoJSON: https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json
import json, math, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, FancyBboxPatch
from shapely.geometry import shape
from shapely.ops import unary_union

d = json.load(open(sys.argv[1]))
feats = d["features"]
def geom(f): return shape(f["geometry"])
by_state = {}
tx = {}
for f in feats:
    st, co = f["properties"]["STATE"], f["properties"]["COUNTY"]
    by_state.setdefault(st, []).append(geom(f))
    if st == "48": tx[co] = geom(f)

# Five statewide regions (us-tx-<region>), county FIPS -> region, from the "Texas in Five" proposal
REGION = json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__) or ".", "tx_regions.json")))

DAL = ["085","113","121","139","231","257","397"] + ["181","147","467","213","349"]
FTW = ["251","367","439","497"] + ["097","237","363","221","425","217"]
AUS = ["021","055","209","453","491"] + ["053","031","287","331"]
HOU = ["015","039","071","157","167","201","291","339","407","473"] + ["471","185","477","089","481","321"]
SAT = ["013","019","029","091","187","259","325","493"] + ["265","171","163","255","177"]

K = math.cos(math.radians(31))
def xy(g):
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    return [[(x*K, y) for x, y in p.exterior.coords] for p in polys]

NAVY="#0a2a62"; INK="#12111a"
C = {"tx":"#ece8f7","north":"#dfe6f6","east":"#dcefe1","central":"#f5e2e8","south":"#e0f1f3","west":"#f3ead6","dal":"#6d4aff","ftw":"#a48bff","aus":"#1597a8","sat":"#5fd0dd","hou":"#f29e4c"}

fig = plt.figure(figsize=(14, 10), dpi=170)
fig.patch.set_facecolor("white")
ax = fig.add_axes([0.02, 0.05, 0.64, 0.84]); ax.set_aspect("equal"); ax.axis("off")

def draw(g, fc, ec="white", lw=0.4, z=1, a=ax):
    for ring in xy(g):
        a.add_patch(MPoly(ring, closed=True, fc=fc, ec=ec, lw=lw, zorder=z))

# neighbours for context
for st in ["35","40","05","22"]:
    draw(unary_union(by_state[st]), "#f6f6f8", "#d8d8de", 0.8, 0)
txu = unary_union(list(tx.values()))
for co, g in tx.items(): draw(g, C[REGION[co]], "#ffffff", 0.3, 1)
for r in ["north","east","central","south","west"]:
    draw(unary_union([g for co, g in tx.items() if REGION[co] == r]), "none", "#8f8aa8", 1.0, 1.5)
for lst, key in [(DAL,"dal"),(FTW,"ftw"),(AUS,"aus"),(SAT,"sat"),(HOU,"hou")]:
    for co in lst: draw(tx[co], C[key], "white", 0.5, 2)
for lst, col in [(DAL+FTW, NAVY),(AUS, NAVY),(SAT, NAVY),(HOU, NAVY)]:
    draw(unary_union([tx[c] for c in lst]), "none", col, 2.2, 3)
draw(txu, "none", NAVY, 1.6, 3)

def lab(lon, lat, tlon, tlat, txt, sub, ha):
    ax.plot([lon*K, tlon*K], [lat, tlat], color=INK, lw=0.8, zorder=5)
    ax.plot(lon*K, lat, "o", ms=4.5, mfc="white", mec=INK, mew=1.2, zorder=6)
    ax.text(tlon*K, tlat, f" {txt} ", ha=ha, va="center", fontsize=11, fontweight="bold", color=INK, zorder=6, family="monospace",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#c9c2e6", lw=0.8))
    ax.text(tlon*K, tlat-0.26, sub, ha=ha, va="center", fontsize=8.5, color="#4a4858", zorder=6)
lab(-96.80, 32.78, -95.2, 32.6, "us-tx-dal", "Dallas", "left")
lab(-97.33, 32.75, -98.75, 32.45, "us-tx-ftw", "Fort Worth", "right")
lab(-97.74, 30.27, -98.75, 31.55, "us-tx-aus", "Austin", "right")
lab(-98.49, 29.42, -99.85, 29.05, "us-tx-sat", "San Antonio", "right")
lab(-95.37, 29.76, -95.0, 28.75, "us-tx-hou", "Houston", "left")
ax.text(-96.6*K, 34.45, "us-tx-dfw", ha="center", fontsize=15, fontweight="bold", color=NAVY, zorder=6)
ax.text(-96.6*K, 34.22, "Dallas–Fort Worth", ha="center", fontsize=9, color=NAVY, zorder=6)
for r, lon, lat in [("west",-102.3,32.4),("north",-99.9,34.05),("east",-94.55,31.75),("central",-99.6,30.55),("south",-98.6,27.4)]:
    ax.text(lon*K, lat, f"us-tx-{r}", ha="center", fontsize=12, fontweight="bold", color="#4a4560", family="monospace", zorder=4,
            bbox=dict(boxstyle="round,pad=0.3", fc=C[r], ec="#8f8aa8", lw=0.8))
for name, lon, lat in [("NM",-105.6,33.4),("OK",-97.5,35.4),("AR",-93.9,34.2)]:
    ax.text(lon*K, lat, name, ha="center", fontsize=9, color="#b2b0bc", zorder=1)
ax.text(-94.3*K, 26.9, "Gulf of Mexico", ha="center", fontsize=9, style="italic", color="#9aa7c4")
minx, miny, maxx, maxy = txu.bounds
ax.set_xlim((minx-0.4)*K, (maxx+0.3)*K); ax.set_ylim(miny-0.3, maxy+0.3)

fig.text(0.04, 0.95, "Proposed MeshCore region scopes: Texas", fontsize=22, fontweight="bold", color=INK)
fig.text(0.04, 0.915, "Draft for discussion · five statewide regions + metro scopes (OMB MSA counties plus edge counties) · 2026-11-01", fontsize=11, color="#5d5b6a")

# hierarchy panel
px = fig.add_axes([0.67, 0.27, 0.31, 0.62]); px.axis("off"); px.set_xlim(0,1); px.set_ylim(0,1)
px.add_patch(FancyBboxPatch((0.0,0.0),1,1, boxstyle="round,pad=0,rounding_size=0.03", fc="#faf9ff", ec="#e2ddf5", lw=1))
px.text(0.06, 0.94, "HIERARCHY", fontsize=10, color="#6d4aff", fontweight="bold")
rows = [(0,"us-south","South (wide-area)","#ffffff"),(0,"us-gc","Gulf Coast (wide-area)","#ffffff"),(0,"us","United States","#ffffff"),(1,"tx","Texas (statewide)",C["tx"]),
        (2,"us-tx-north","North",C["north"]),(2,"us-tx-east","East",C["east"]),(2,"us-tx-central","Central",C["central"]),(2,"us-tx-south","South",C["south"]),(2,"us-tx-west","West",C["west"]),
        (2,"us-tx-dfw","Dallas–Fort Worth","#ffffff"),(3,"us-tx-dal","Dallas",C["dal"]),(3,"us-tx-ftw","Fort Worth",C["ftw"]),
        (2,"us-tx-aus","Austin",C["aus"]),(2,"us-tx-sat","San Antonio",C["sat"]),(2,"us-tx-hou","Houston",C["hou"])]
y = 0.875; prev = {}
for lvl, code, name, col in rows:
    x = 0.07 + lvl*0.07
    if lvl > 0:
        px.plot([x-0.045, x-0.045, x-0.01], [prev[lvl-1]-0.02, y, y], color="#b9b2d6", lw=1)
    w = max(0.10, 0.026*len(code)+0.03)
    px.add_patch(FancyBboxPatch((x, y-0.02), w, 0.04, boxstyle="round,pad=0,rounding_size=0.012",
                 fc=col, ec=NAVY if code in ("tx","us-tx-dfw","us-tx-aus","us-tx-sat","us-tx-hou") else "#c9c2e6", lw=1.4 if code in ("tx","us-tx-dfw","us-tx-aus","us-tx-sat","us-tx-hou") else 0.8))
    px.text(x+w/2, y, code, ha="center", va="center", fontsize=9, fontweight="bold",
            color="white" if code in ("us-tx-dal","us-tx-aus") else INK, family="monospace")
    px.text(x+w+0.025, y, name, va="center", fontsize=9, color=INK)
    prev[lvl] = y; y -= 0.0545

# config panel
cx = fig.add_axes([0.67, 0.03, 0.31, 0.225]); cx.axis("off"); cx.set_xlim(0,1); cx.set_ylim(0,1)
cx.add_patch(FancyBboxPatch((0,0),1,1, boxstyle="round,pad=0,rounding_size=0.03", fc="#12111a", ec="none"))
cx.text(0.06, 0.87, "EXAMPLE: A DALLAS REPEATER", fontsize=9, color="#a48bff", fontweight="bold")
cfg = ["region put us","region put us-south","region put us-gc","region put tx us","region put us-tx-north tx","region put us-tx-dfw tx","region put us-tx-dal us-tx-dfw","region save"]
for i, l in enumerate(cfg):
    cx.text(0.06, 0.75 - i*0.087, l, fontsize=9, color="#e8e6f2", family="monospace")
fig.savefig(sys.argv[2], facecolor="white")
