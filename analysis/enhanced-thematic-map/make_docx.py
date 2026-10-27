"""Builds the MS Word document with the paper-ready interpretation of the
thematic map: headed paragraphs (no tables), the figure with its caption, and
a methods sentence. Manuscript styling: Times New Roman 12 pt, 1.5 line
spacing, justified body text, black bold headings."""
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

HERE = sys.path[0] if sys.path[0] else "."
OUT = f"{HERE}/Thematic_map_interpretation.docx"
FIG = f"{HERE}/thematic_map_figure.png"

doc = Document()

# ---- base styles -----------------------------------------------------------
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.font.color.rgb = RGBColor(0, 0, 0)
pf = st.paragraph_format
pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
pf.space_after = Pt(12)
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
for h in ("Heading 1", "Heading 2"):
    hs = doc.styles[h]
    hs.font.name = "Times New Roman"
    hs.font.color.rgb = RGBColor(0, 0, 0)
    hs.font.bold = True
    hs.font.size = Pt(14 if h == "Heading 1" else 12)
    hs.paragraph_format.space_before = Pt(12)
    hs.paragraph_format.space_after = Pt(6)
    hs.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    hs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

def para(text):
    return doc.add_paragraph(text)

# ---- content ----------------------------------------------------------------
doc.add_heading("Interpretation of the Thematic Map (Strategic Diagram)", level=1)

para(
    "A thematic map (strategic diagram) was constructed following Cobo et al. "
    "(2011) from the keyword co-occurrence network of the 232 included "
    "documents (Scopus Index Keywords; top 250 terms, minimum frequency 50 per "
    "thousand). Themes were obtained by Louvain community detection on the "
    "association-strength network and positioned according to their "
    "centrality (relevance degree, i.e. the strength of a theme's links to the "
    "other themes) and density (development degree, i.e. the internal cohesion "
    "of the theme). Four themes emerged, one for each quadrant of the diagram "
    "(Figure 1); circle area is proportional to the total occurrences of the "
    "theme's keywords. Their interpretation follows."
)

doc.add_heading("Motor theme — human, health care quality, humans", level=2)
para(
    "The motor theme occupies the upper-right quadrant of the strategic "
    "diagram, with above-mean centrality (482.21) and density (14.36), and is "
    "by far the largest theme of the network (59 keywords, 2 611 keyword "
    "occurrences across the 232 documents). High centrality indicates that the "
    "theme is strongly linked to all other themes of the network, while high "
    "density shows that it is internally cohesive and conceptually mature. "
    "Research framing health-care quality around human subjects and patients "
    "is therefore both the most developed and the most central strand of this "
    "literature: the conceptual core that drives and structures the whole "
    "field, with shared definitions, accumulated evidence and dense internal "
    "debate. Because motor themes can saturate, periodic re-mapping is "
    "advisable to monitor whether its density keeps rising and which quality "
    "dimensions (safety, effectiveness, timeliness, patient experience) carry "
    "the theme."
)

doc.add_heading("Niche theme — mortality, time factor, time factors", level=2)
para(
    "The niche theme shows the highest density of the map (19.08) but "
    "below-mean centrality (381.81), with 31 keywords and 656 occurrences. "
    "This signature — strong internal cohesion with weak external connection "
    "— identifies a specialised sub-field: mortality endpoints, follow-up "
    "duration and timing of care, i.e. the time-to-event methodological "
    "toolkit. It is a mature, self-contained specialty with its own outcomes "
    "and study designs, yet it sits at the periphery of the field's centre of "
    "gravity, exchanging little with the health-care-quality core. The most "
    "valuable development for this theme is bridging work that connects its "
    "rigorous outcome measurement to the motor theme, transferring "
    "methodological rigour to the core of the field."
)

doc.add_heading("Basic theme — female, male, major clinical study", level=2)
para(
    "The basic theme combines above-mean centrality (423.57) with low density "
    "(10.63) and is the second largest theme of the map (27 keywords, 1 216 "
    "occurrences). Its keywords are transversal descriptors — sex and "
    "demographic categories together with the study-design tag major clinical "
    "study — that recur across most documents of the corpus, which explains "
    "their strong links to every other theme, but that do not constitute a "
    "coherent theory of their own, which explains the weak internal cohesion. "
    "Practically, this theme is the shared foundational vocabulary of the "
    "field rather than an independent research front, and should be read as "
    "cross-cutting covariates of the literature. Should its density grow in "
    "future periods, that would signal maturation into an autonomous "
    "sub-literature — for instance on sex/gender equity in the quality of "
    "care."
)

doc.add_heading(
    "Emerging or declining theme — practice guideline, protocol compliance, "
    "clinical practice", level=2)
para(
    "The smallest theme of the map (10 keywords, 207 occurrences) falls below "
    "the mean on both centrality (146.28) and density (7.58), placing it at "
    "the margin of the field. It captures the implementation-science angle — "
    "whether routine clinical practice adheres to practice guidelines and "
    "protocols — and is at present weakly developed and weakly connected to "
    "the core. A static map cannot separate an embryonic research front from a "
    "fading topic: longitudinal thematic-evolution analysis is required. If "
    "its centrality is rising, this theme marks the clearest opportunity space "
    "of the field — the well-known “care gap” between recommended and "
    "delivered practice; if it is falling, the topic should be treated as "
    "background."
)

doc.add_heading("Synthesis", level=2)
para(
    "Taken together, the four themes describe a core–periphery structure: a "
    "dominant human-centred health-care-quality motor hubs the network; a "
    "mature methodological niche (mortality and time factors) and a "
    "transversal descriptor layer (sex and study-design tags) orbit it; and "
    "the guideline-adherence question — arguably the most consequential for "
    "patients — still lies outside the core, awaiting either emergence or "
    "confirmation of decline."
)

# ---- figure + caption --------------------------------------------------------
doc.add_heading("Figure", level=1)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run().add_picture(FIG, width=Inches(6.0))
cap = doc.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r = cap.add_run("Figure 1. ")
r.bold = True
cap.add_run(
    "Thematic map (strategic diagram) of the research field, based on "
    "co-occurring Scopus Index Keywords in the 232 analysed documents. Themes "
    "(circles) are communities obtained by Louvain clustering of the "
    "association-strength keyword co-occurrence network (top 250 terms; terms "
    "with ≥ 11 occurrences retained). The horizontal axis reports centrality "
    "(relevance degree) and the vertical axis density (development degree), "
    "each expressed as centred ranks; dashed lines mark the mean of the two "
    "indices. Circle area is proportional to the total occurrences of the "
    "theme's keywords. Four themes were identified: the motor theme "
    "human–health care quality–humans, well developed and central to the "
    "field; the niche theme mortality–time factor–time factors, internally "
    "developed but peripheral; the basic theme female–male–major clinical "
    "study, transversal across studies yet conceptually undeveloped; and "
    "practice guideline–protocol compliance–clinical practice, at the "
    "emerging-or-declining margin of the field. Analysis followed Cobo et "
    "al. (2011) as implemented in the bibliometrix R package."
)

# ---- methods sentence ---------------------------------------------------------
doc.add_heading("Methods sentence (for the Methods section)", level=2)
para(
    "Keyword co-occurrence networks were constructed from Scopus Index "
    "Keywords of the 232 included documents (top 250 terms; minimum term "
    "frequency 50 per thousand, i.e. ≥ 11 occurrences). Themes were detected "
    "by Louvain community detection on the association-strength network; "
    "theme centrality (sum of external link weights on the cosine-normalised "
    "co-occurrence network) and density (mean internal association strength "
    "per keyword) were computed following Cobo et al. (2011) and plotted as a "
    "strategic diagram with the thematicMap workflow of the bibliometrix R "
    "package (Aria & Cuccurullo, 2017)."
)

doc.save(OUT)
print("saved", OUT)
