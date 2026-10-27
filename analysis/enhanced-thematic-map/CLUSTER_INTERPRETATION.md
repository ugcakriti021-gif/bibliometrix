# Cluster interpretation — enhanced thematic map

Companion document to `enhanced_thematic_map.html` (interactive map) and
`enhanced_thematic_map.R` (exact re-run from a Scopus export).

**Framework.** Strategic diagram of Cobo et al. (2011), as implemented by
`thematicMap()` in the **bibliometrix** R package (Aria & Cuccurullo, 2017;
Aria et al., 2026) and served by biblioshiny. Each keyword cluster is scored on
**centrality** (relevance: strength of interaction with the rest of the field)
and **density** (development: internal cohesion and maturity). The dashed cross
is the mean of both scores; quadrant membership gives the reading below.

**Provenance of the numbers.** Cluster positions, bubble sizes and the median
cross were digitised pixel-exactly from the biblioshiny screenshot
(colour-blob detection; the watermark logo in the lower-right corner was
identified and excluded). Coordinates are centred relative units
(0 = median cross, ±1 = panel edge); weights are bubble-area shares of the four
mapped themes. Quadrant membership is unambiguous — every cluster sits deep
inside its quadrant. For exact centrality/density/cardinality values, re-run
`enhanced_thematic_map.R` on the Scopus export.

---

## C1 · Humans & Health Care Quality — MOTOR theme (upper right)
*Keywords: human · health care quality · humans — centrality +0.75, density +0.25, weight ≈ 44% (dominant)*

**What the map shows.** Above the median on both axes and by far the largest
bubble: the cluster is strongly connected to every other theme *and*
internally cohesive.

**Interpretation.** The engine of this literature. Framing health-care quality
around human subjects/patients is simultaneously the most connected and the
most mature theme — shared definitions, accumulated evidence, dense internal
debate. A textbook motor theme: it drives the field and is well developed.

**What to do with it.** Monitor for saturation (is density still rising?) and
open the black box: which quality dimensions — safety, effectiveness,
timeliness, patient experience — carry the cluster? A per-year overlay shows
whether the motor is stable or shifting.

## C2 · Mortality & Time Factors — NICHE theme (upper left)
*Keywords: mortality · time factor · time factors — centrality −0.24, density +0.75, weight ≈ 17% (moderate)*

**What the map shows.** The highest density on the map with below-median
centrality and a mid-sized bubble.

**Interpretation.** A specialised, methodologically mature sub-field:
mortality endpoints, follow-up duration, timing of care — the time-to-event
toolkit. Internal ties are strong (own measures, own designs) but exchange
with the health-care-quality core is limited: a true niche, well developed yet
peripheral to the field's centre of gravity.

**What to do with it.** Bridging work is the high-value move: connect
mortality / time-to-event endpoints to quality-improvement frameworks and the
niche's rigour feeds the motor. If your question is outcome measurement, this
cluster is where the rigorous evidence base lives.

## C3 · Practice Guidelines & Protocol Compliance — EMERGING or DECLINING (lower left)
*Keywords: practice guideline · protocol compliance · clinical practice — centrality −0.75, density −0.25, weight ≈ 1% (marginal)*

**What the map shows.** Below the median on both axes and the smallest bubble
on the map.

**Interpretation.** The implementation-science angle — adherence to practice
guidelines, protocol compliance in routine clinical practice — is present but
marginal: few documents, weak internal structure, weak links to the rest. Two
readings are possible: an embryonic emerging front, or a fading topic. A
static map cannot separate them.

**What to do with it.** Decide with time: run `thematicEvolution()` or split
the corpus into two periods. Rising centrality would identify this as the
field's clearest opportunity space — the well-known "care gap" between what
guidelines recommend and what practice delivers. Falling centrality would
relegate it to background.

## C4 · Sex & Study-Type Descriptors — BASIC theme (lower right)
*Keywords: article · female · male — centrality +0.25, density −0.75, weight ≈ 30% (large)*

**What the map shows.** Above-median centrality with the lowest density on the
map, and the second-largest bubble.

**Interpretation.** Transversal foundations rather than a coherent
sub-literature. Sex/demographic descriptors (female, male) and
publication-type tags (article) appear across nearly every study — hence high
centrality — but no developed theory binds them — hence low density.
Practically: the field routinely reports sex-disaggregated samples without yet
having built a cohesive "sex/gender differences in care quality" literature.

**What to do with it.** Treat these terms as cross-cutting covariates when
reading or designing studies. Watch density: a rise here would mark the
maturation of a gender-equity research front within quality-of-care research.

---

## Synthesis — the shape of the field

The field shows a clear **core–periphery structure**. A single dominant motor
theme (human-centred health-care quality) carries almost half of the mapped
keyword mass and hubs the network; a mature methodological niche
(mortality/time factors) and a large transversal descriptor layer
(female/male/article) orbit it; guideline-compliance implementation sits at
the emerging/declining margin. In plain language: the community knows *that*
care quality matters and measures it in humans, has strong tools for
time-to-event outcomes, and reports sex-demographics routinely — but the
question that arguably matters most for patients, *whether practice actually
follows guidelines*, is still outside the core.

**Recommendations**
1. Bridge the niche to the core (time-to-event outcomes × quality improvement).
2. Test the guideline cluster over time before naming it emerging or declining.
3. Treat female/male/article as covariates, not as a theme; watch their density.
4. Monitor the motor for saturation with periodic re-mapping.
5. Replace digitised values with exact ones via `enhanced_thematic_map.R`.
