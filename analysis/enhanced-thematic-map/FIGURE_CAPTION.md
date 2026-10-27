# Figure caption & interpretation — thematic map (strategic diagram)

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
> keywords. Four themes were identified: the **motor theme**
> *human–health care quality–humans*, well developed and central to the field;
> the **niche theme** *mortality–time factor–time factors*, internally
> developed but peripheral; the **basic theme** *female–male–major clinical
> study*, transversal across studies yet conceptually undeveloped; and
> *practice guideline–protocol compliance–clinical practice*, at the
> **emerging-or-declining** margin of the field. Analysis followed Cobo et
> al. (2011) as implemented in the bibliometrix R package.

## Interpretation of the themes

**Motor theme — human, health care quality, humans.** The motor theme occupies
the upper-right quadrant of the strategic diagram, with above-mean centrality
(482.21) and density (14.36), and is by far the largest theme of the network
(59 keywords, 2 611 keyword occurrences across the 232 documents). High
centrality indicates that the theme is strongly linked to all other themes of
the network, while high density shows that it is internally cohesive and
conceptually mature. Research framing health-care quality around human
subjects and patients is therefore both the most developed and the most central
strand of this literature: the conceptual core that drives and structures the
whole field, with shared definitions, accumulated evidence and dense internal
debate. Because motor themes can saturate, periodic re-mapping is advisable to
monitor whether its density keeps rising and which quality dimensions
(safety, effectiveness, timeliness, patient experience) carry the theme.

**Niche theme — mortality, time factor, time factors.** The niche theme shows
the highest density of the map (19.08) but below-mean centrality (381.81), with
31 keywords and 656 occurrences. This signature — strong internal cohesion with
weak external connection — identifies a specialised sub-field: mortality
endpoints, follow-up duration and timing of care, i.e. the time-to-event
methodological toolkit. It is a mature, self-contained specialty with its own
outcomes and study designs, yet it sits at the periphery of the field's centre
of gravity, exchanging little with the health-care-quality core. The most
valuable development for this theme is bridging work that connects its rigorous
outcome measurement to the motor theme, transferring methodological rigour to
the core of the field.

**Basic theme — female, male, major clinical study.** The basic theme combines
above-mean centrality (423.57) with low density (10.63) and is the second
largest theme of the map (27 keywords, 1 216 occurrences). Its keywords are
transversal descriptors — sex and demographic categories together with the
study-design tag *major clinical study* — that recur across most documents of
the corpus, which explains their strong links to every other theme, but that
do not constitute a coherent theory of their own, which explains the weak
internal cohesion. Practically, this theme is the shared foundational vocabulary
of the field rather than an independent research front, and should be read as
cross-cutting covariates of the literature. Should its density grow in future
periods, that would signal maturation into an autonomous sub-literature — for
instance on sex/gender equity in the quality of care.

**Emerging or declining theme — practice guideline, protocol compliance,
clinical practice.** The smallest theme of the map (10 keywords, 207
occurrences) falls below the mean on both centrality (146.28) and density
(7.58), placing it at the margin of the field. It captures the
implementation-science angle — whether routine clinical practice adheres to
practice guidelines and protocols — and is at present weakly developed and
weakly connected to the core. A static map cannot separate an embryonic
research front from a fading topic: longitudinal thematic-evolution analysis is
required. If its centrality is rising, this theme marks the clearest
opportunity space of the field — the well-known "care gap" between recommended
and delivered practice; if it is falling, the topic should be treated as
background.

**Synthesis.** Taken together, the four themes describe a core–periphery
structure: a dominant human-centred health-care-quality motor hubs the network;
a mature methodological niche (mortality and time factors) and a transversal
descriptor layer (sex and study-design tags) orbit it; and the
guideline-adherence question — arguably the most consequential for patients —
still lies outside the core, awaiting either emergence or confirmation of
decline.

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

`python3 build_figure.py <scopus_csv> <out_dir>` regenerates every figure
format and `clusters_final.csv` (per-theme centrality, density, keyword lists
and occurrence counts) from the raw Scopus export.
