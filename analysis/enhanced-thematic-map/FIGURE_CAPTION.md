# Figure caption & methods text — thematic map (strategic diagram)

**Files to attach to the paper** (same figure, four formats):
`thematic_map_figure.png` (300 dpi raster), `thematic_map_figure.tiff`
(600 dpi, LZW — for journals requiring TIFF), `thematic_map_figure.pdf` and
`thematic_map_figure.svg` (vector — preferred if the journal accepts EPS/PDF/SVG).

## Suggested caption

> **Figure X.** Thematic map (strategic diagram) of the research field, based on
> co-occurring Scopus Index Keywords in the 232 analysed documents. Themes
> (circles) are communities obtained by Louvain clustering of the
> association-strength keyword co-occurrence network (top 250 terms; terms with
> ≥ 11 occurrences retained). The horizontal axis reports centrality
> (relevance degree: strength of a theme's links to other themes) and the
> vertical axis density (development degree: internal cohesion of the theme),
> each expressed as centred ranks; dashed lines mark the mean of the two
> indices. Circle area is proportional to the total occurrences of the theme's
> keywords (legend). Four themes were identified: the **motor theme**
> *human–health care quality–humans*, well developed and central to the field;
> the **niche theme** *mortality–time factor–time factors*, internally
> developed but peripheral; the **basic theme** *female–male–major clinical
> study*, transversal across studies yet conceptually undeveloped; and
> *practice guideline–protocol compliance–clinical practice*, at the
> **emerging-or-declining** margin of the field. Analysis followed Cobo et
> al. (2011) as implemented in the bibliometrix R package.

## Cluster statistics (computed from the 232 documents)

| Theme (top keywords) | Quadrant | Centrality | Density | Keywords in theme | Keyword occurrences |
|---|---|---:|---:|---:|---:|
| human; health care quality; humans | Motor | 482.21 | 14.36 | 59 | 2 611 |
| female; male; major clinical study | Basic | 423.57 | 10.63 | 27 | 1 216 |
| mortality; time factor; time factors | Niche | 381.81 | 19.08 | 31 | 656 |
| practice guideline; protocol compliance; clinical practice | Emerging/declining | 146.28 | 7.58 | 10 | 207 |

Full per-cluster keyword lists: `clusters_final.csv`.

## Interpretation paragraphs (for the Results/Discussion)

**Motor theme — human, health care quality, humans.** The largest and most
central theme: it combines high centrality with high density, i.e. it is both
strongly connected to the rest of the network and internally cohesive.
Research framing health-care quality around human subjects/patients
constitutes the conceptual core that drives and structures this literature.

**Niche theme — mortality, time factor, time factors.** The highest density on
the map with below-average centrality: a specialised, methodologically mature
sub-field (mortality endpoints, follow-up time, time-to-event analysis) with
strong internal cohesion but limited exchange with the core — a well-developed
yet peripheral specialty.

**Basic theme — female, male, major clinical study.** High centrality with low
density: transversal demographic and study-design descriptors shared by most
documents. They function as cross-cutting foundations of the field rather
than as a coherent sub-literature of their own.

**Emerging or declining theme — practice guideline, protocol compliance,
clinical practice.** Low on both dimensions and the smallest theme: the
implementation-science angle (adherence to guidelines and protocols in routine
practice) sits at the margin of the field. Longitudinal analysis (thematic
evolution) is required to determine whether it is an embryonic front or a
fading topic; if emerging, it marks the most evident opportunity space — the
gap between recommended and delivered practice.

## Methods sentence (for the Methods section)

> Keyword co-occurrence networks were constructed from Scopus Index Keywords
> of the 232 included documents (top 250 terms; minimum term frequency 50 per
> thousand, i.e. ≥ 11 occurrences). Themes were detected by Louvain community
> detection on the association-strength network; theme centrality (sum of
> external link weights on the cosine-normalised co-occurrence network) and
> density (mean internal association strength per keyword) were computed
> following Cobo et al. (2011) and plotted as a strategic diagram with the
> thematicMap workflow of the bibliometrix R package (Aria & Cuccurullo, 2017;
> script `build_figure.py`, seed 1234).

## Reproducibility

`python3 build_figure.py <scopus_csv> <out_dir>` regenerates every format and
`clusters_final.csv` from the raw Scopus export.
