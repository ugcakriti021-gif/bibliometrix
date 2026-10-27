"""Builds the publication-quality thematic map (strategic diagram) figure.

Pipeline (mirrors bibliometrix/biblioshiny, Cobo et al. 2011):
  1. Scopus CSV -> Index Keywords, lower-cased, split on ';'.
  2. Top n=250 terms; co-occurrence counts C; terms kept if occ >= minfreq
     (minfreq = max(2, floor(50 per-mille * N)) = 11 for N = 232).
  3. Themes = Louvain communities of the association-strength network
     S_assoc(i,j) = c_ij / (c_ii * c_jj)   (seed 1234).
  4. Cobo indices: centrality = sum of external link weights on the
     Salton/cosine-normalised network; density = mean internal
     association strength per keyword of the cluster (*100).
  5. Axes = centred ranks of the two indices (as in biblioshiny).
  6. Bubble area proportional to total keyword occurrences of the theme.

Outputs (paper-ready): thematic_map_figure.png (300 dpi), .tiff (600 dpi),
.pdf and .svg, plus clusters_final.csv with the underlying numbers.
"""
import collections
import csv
import sys

import numpy as np
import igraph as ig
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image

HERE = sys.path[0] if sys.path[0] else "."
SCOPUS = sys.argv[1] if len(sys.argv) > 1 else \
    "/tmp/arena-coding-uploads/scopus_export_Jul 16-2026_475def67-45cc-4a54-9797-6fa8c21fbbfa.csv"
OUT = sys.argv[2] if len(sys.argv) > 2 else "."

# ---------------------------------------------------------------- data
doc_terms, cnt = [], collections.Counter()
with open(SCOPUS, encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh):
        s = r.get("Index Keywords") or ""
        ts = sorted({t.strip().lower() for t in s.split(";") if t.strip()})
        if ts:
            doc_terms.append(ts)
            cnt.update(ts)
N = len(doc_terms)

N_TERMS, MINFREQ_PM, SEED = 250, 50, 1234
top = [t for t, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:N_TERMS]]
idx = {t: i for i, t in enumerate(top)}
C = np.zeros((N_TERMS, N_TERMS))
for ts in doc_terms:
    ks = [idx[t] for t in ts if t in idx]
    for a in ks:
        C[a, a] += 1
        for b in ks:
            if a != b:
                C[a, b] += 1

mf = max(2, int(np.floor(MINFREQ_PM * N / 1000)))
keep = np.diag(C) >= mf
C = C[np.ix_(keep, keep)]
terms = [t for t, k in zip(top, keep) if k]
m = len(terms)
Dg = np.diag(C).copy()
with np.errstate(divide="ignore", invalid="ignore"):
    S_assoc = np.nan_to_num(np.where(C > 0, C / np.outer(Dg, Dg), 0.0))
    S_salt = np.nan_to_num(np.where(C > 0, C / np.sqrt(np.outer(Dg, Dg)), 0.0))

# ------------------------------------------------- Louvain on association
edges = [(i, j) for i in range(m) for j in range(i + 1, m) if C[i, j] >= 1]
g = ig.Graph(n=m, edges=edges, directed=False)
g.vs["name"] = terms
g.delete_vertices([v.index for v in g.vs if v.degree() == 0])
names0 = g.vs["name"]
pos = {t: i for i, t in enumerate(terms)}
w = [S_assoc[pos[names0[a]], pos[names0[b]]] for a, b in g.get_edgelist()]
random.seed(SEED)
ig.set_random_number_generator(random)
mem = g.community_multilevel(weights=w).membership
names = g.vs["name"]
grp = {t: mem[i] for i, t in enumerate(names)}
pidx = [pos[t] for t in names]
Ca = S_assoc[np.ix_(pidx, pidx)]
Cs = S_salt[np.ix_(pidx, pidx)]

# ------------------------------------------------- Cobo centrality/density
acc = collections.defaultdict(lambda: [0.0, 0.0, 0])
ii = np.triu_indices(len(names), 1)
for a, b in zip(*ii):
    es, ea = Cs[a, b], Ca[a, b]
    if es <= 0 and ea <= 0:
        continue
    ta, tb = names[a], names[b]
    ga, gb = grp[ta], grp[tb]
    if ga != gb:
        acc[ga][0] += es
        acc[gb][0] += es
    else:
        acc[ga][1] += ea
    if ga == gb:
        acc[ga][2] += 1
rows = []
for gr, (ce, di, _npairs) in acc.items():
    ws = [t for t, gg in grp.items() if gg == gr]
    n = len(ws)
    kw = sorted(ws, key=lambda t: -cnt[t])
    rows.append(dict(
        cluster=gr, centrality=ce, density=di / n * 100, n_terms=n,
        occurrences=int(sum(cnt[t] for t in ws)),
        keywords="; ".join(kw[:3]), all_keywords="; ".join(kw)))
import pandas as pd
cdf = pd.DataFrame(rows)
cdf["rcentrality"] = cdf.centrality.rank()
cdf["rdensity"] = cdf.density.rank()
cdf["x"] = (cdf.rcentrality - cdf.rcentrality.mean()) / (cdf.rcentrality.max() - cdf.rcentrality.min()) * 1.5
cdf["y"] = (cdf.rdensity - cdf.rdensity.mean()) / (cdf.rdensity.max() - cdf.rdensity.min()) * 1.5
cdf["quadrant"] = np.where(cdf.x >= 0, np.where(cdf.y >= 0, "Motor themes", "Basic themes"),
                           np.where(cdf.y >= 0, "Niche themes", "Emerging or declining themes"))
cdf = cdf.sort_values("occurrences", ascending=False).reset_index(drop=True)
print(cdf[["keywords", "quadrant", "centrality", "density", "n_terms", "occurrences"]].to_string(index=False))
cdf.to_csv(f"{OUT}/clusters_final.csv", index=False)

# ------------------------------------------------- figure
QCOL = {"Motor themes": "#D55E00", "Niche themes": "#009E73",
        "Basic themes": "#0072B2", "Emerging or declining themes": "#CC79A7"}
QLAB = {"Motor themes": ("MOTOR THEMES", (1, 1)),
        "Niche themes": ("NICHE THEMES", (0, 1)),
        "Basic themes": ("BASIC THEMES", (1, 0)),
        "Emerging or declining themes": ("EMERGING OR DECLINING THEMES", (0, 0))}
LIM = 1.05
fig, ax = plt.subplots(figsize=(7.4, 6.1))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
# quadrant tints + corner names
ax.axvspan(0, LIM, ymin=0.5, ymax=1, color=QCOL["Motor themes"], alpha=.045, zorder=0)
ax.axvspan(-LIM, 0, ymin=0.5, ymax=1, color=QCOL["Niche themes"], alpha=.045, zorder=0)
ax.axvspan(-LIM, 0, ymin=0, ymax=0.5, color=QCOL["Emerging or declining themes"], alpha=.045, zorder=0)
ax.axvspan(0, LIM, ymin=0, ymax=0.5, color=QCOL["Basic themes"], alpha=.045, zorder=0)
for q, (txt, (hx, vy)) in QLAB.items():
    ax.text(LIM * (1 if hx else -1) * .985, LIM * (1 if vy else -1) * .965, txt,
            ha="right" if hx else "left", va="top" if vy else "bottom",
            fontsize=8.6, fontweight="bold", color="#555b63", alpha=.75)
# median cross
ax.axhline(0, color="#6b7280", ls=(0, (6, 4)), lw=.9, zorder=1)
ax.axvline(0, color="#6b7280", ls=(0, (6, 4)), lw=.9, zorder=1)
# bubbles
rmax = 0.155
occ = cdf.occurrences
rad = rmax * np.sqrt(occ / occ.max())
LABSIDE = {"Motor themes": -1, "Niche themes": -1, "Basic themes": 1,
           "Emerging or declining themes": 1}
for (x, y, q, r, kw) in zip(cdf.x, cdf.y, cdf.quadrant, rad, cdf.keywords):
    c = QCOL[q]
    ax.add_patch(Circle((x, y), r, facecolor=c, alpha=.40, edgecolor=c, lw=1.5, zorder=3))
    side = LABSIDE[q]
    lx0, lx1 = x + side * (r + .012), x + side * (r + .055)
    ax.plot([lx0, lx1], [y, y], color=c, lw=.9, zorder=2, solid_capstyle="round")
    words = kw.split("; ")
    for i, wd in enumerate(words):
        ax.text(lx1 + side * .02, y + (1 - i) * .062, wd,
                ha="left" if side > 0 else "right", va="center",
                fontsize=9.2, color="#22272e", zorder=4,
                bbox=dict(fc="white", ec="none", alpha=.72, pad=1.1))
# axes
# axes
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#33383f")
    ax.spines[s].set_linewidth(.9)
ax.set_xlim(-LIM, LIM)
ax.set_ylim(-LIM, LIM)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("Relevance degree  (Centrality)", fontsize=10.5, labelpad=7)
ax.set_ylabel("Development degree  (Density)", fontsize=10.5, labelpad=7)
ax.set_aspect("equal")
# size legend, true scale, in the empty mid-left band of the panel
leg_y = 0.30
for xo, o in zip([-0.82, -0.60, -0.30], [500, 1500, 2500]):
    r = rmax * np.sqrt(o / occ.max())
    ax.add_patch(Circle((xo, leg_y), r, facecolor="none", edgecolor="#8a919b", lw=.8, zorder=3))
    ax.text(xo, leg_y - r - 0.045, f"{o}", ha="center", va="top", fontsize=7.4, color="#6b7280")
ax.text(-0.89, leg_y + 0.24, "keyword occurrences", fontsize=7.6, color="#6b7280",
        ha="left", va="bottom", style="italic")
fig.tight_layout()
fig.savefig(f"{OUT}/thematic_map_figure.png", dpi=300, facecolor="white")
fig.savefig(f"{OUT}/thematic_map_figure.pdf", facecolor="white")
fig.savefig(f"{OUT}/thematic_map_figure.svg", facecolor="white")
img = Image.open(f"{OUT}/thematic_map_figure.png")
img.save(f"{OUT}/thematic_map_figure.tiff", dpi=(600, 600), compression="tiff_lzw")
print("figure written")
