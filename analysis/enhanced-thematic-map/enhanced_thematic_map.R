# ---------------------------------------------------------------------------
# Enhanced thematic map (strategic diagram) from a Scopus export
# ---------------------------------------------------------------------------
# Companion to enhanced_thematic_map.html. Rebuilds the biblioshiny thematic
# map with the improvements biblioshiny does not offer:
#   * tinted quadrants with plain-language meanings printed on the plot
#   * numeric, centred axes (0 = mean centrality / mean density)
#   * bubbles sized by cluster cardinality (documents), with a size legend
#   * non-overlapping cluster labels (ggrepel)
#   * an interactive plotly version saved as HTML
#   * an automatically written interpretation file (interpretation_auto.md)
#
# Usage:
#   Rscript enhanced_thematic_map.R <scopus_file.txt|.csv> [out_dir] [field]
# Example:
#   Rscript enhanced_thematic_map.R my_scopus_export.txt . ID
#
# `field`: textual field used for the co-occurrence network.
#   "ID" = Scopus Index Keywords (what your biblioshiny map used),
#   "DE" = Author Keywords, "TI"/"AB" = titles/abstracts.
# ---------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(bibliometrix)
  library(ggplot2)
  library(dplyr)
})

args      <- commandArgs(trailingOnly = TRUE)
file      <- args[1]
outdir    <- if (length(args) >= 2) args[2] else "."
field     <- if (length(args) >= 3) args[3] else "ID"
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

fmt <- if (grepl("\\.csv$", file, ignore.case = TRUE)) "csv" else "plaintext"
cat("\n>> Reading", file, "as Scopus", fmt, "\n")
M <- convert2df(file, dbsource = "scopus", format = fmt)
cat(">>", nrow(M), "documents\n")

# --- thematic map with the same engine biblioshiny uses --------------------
tm <- thematicMap(
  M,
  field     = field,
  n         = 250,
  minfreq   = 5,      # per thousand documents, as in bibliometrix
  size      = 0.5,
  n.labels  = 3,      # three keywords per cluster label, as on your map
  repel     = TRUE,
  cluster   = "louvain",
  seed      = 1234
)
if (is.null(tm)) stop("thematicMap() returned nothing: check minfreq / network size.")

cl     <- tm$clusters                       # one row per cluster
origin <- tm$axisOrigin                     # c(mean centrality, mean density)
limits <- tm$axisLimits                     # c(xmin, xmax, ymin, ymax)

# --- centre the coordinates (improvement: numeric, interpretable axes) -----
cl <- cl %>%
  mutate(
    cx = rcentrality - origin[1],
    cy = rdensity    - origin[2],
    quadrant = case_when(
      cx >= 0 & cy >= 0 ~ "Motor themes",
      cx <  0 & cy >= 0 ~ "Niche themes",
      cx >= 0 & cy <  0 ~ "Basic themes",
      TRUE              ~ "Emerging or declining themes"
    ),
    label = gsub("\n", "\n", name_full)
  )
xl <- limits[1:2] - origin[1]
yl <- limits[3:4] - origin[2]
inset_x <- 0.02 * diff(xl); inset_y <- 0.03 * diff(yl)

quad_cols <- c(
  "Motor themes" = "#d76a78", "Niche themes" = "#5d9e63",
  "Basic themes" = "#5f93c4", "Emerging or declining themes" = "#9678ad"
)

# --- enhanced static plot ---------------------------------------------------
g <- ggplot(cl, aes(x = cx, y = cy)) +
  annotate("rect", xmin = 0, xmax = xl[2], ymin = 0, ymax = yl[2],
           fill = quad_cols[["Motor themes"]], alpha = .05) +
  annotate("rect", xmin = xl[1], xmax = 0, ymin = 0, ymax = yl[2],
           fill = quad_cols[["Niche themes"]], alpha = .05) +
  annotate("rect", xmin = xl[1], xmax = 0, ymin = yl[1], ymax = 0,
           fill = quad_cols[["Emerging or declining themes"]], alpha = .05) +
  annotate("rect", xmin = 0, xmax = xl[2], ymin = yl[1], ymax = 0,
           fill = quad_cols[["Basic themes"]], alpha = .05) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey45") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey45") +
  geom_point(
    aes(size = fuzzy_cardinality, fill = quadrant,
        text = paste0("<b>", name, "</b><br>", gsub("\n", " - ", words),
                      "<br>centrality (rank): ", rcentrality,
                      "<br>density (rank): ", rdensity,
                      "<br>documents: ", round(fuzzy_cardinality))),
    shape = 21, color = "white", stroke = 1.4, alpha = .9
  ) +
  scale_fill_manual(values = quad_cols, name = NULL) +
  scale_size_continuous(name = "Documents\n(fuzzy cardinality)", range = c(6, 20)) +
  {
    if (requireNamespace("ggrepel", quietly = TRUE))
      ggrepel::geom_label_repel(
        aes(label = label), size = 3.4, lineheight = .95,
        box.padding = .9, point.padding = .5, segment.color = "grey60",
        max.overlaps = Inf, seed = 42,
        fill = "white", color = "grey25", alpha = .85
      )
    else
      geom_text(aes(label = label), size = 3.2, vjust = -1.2, color = "grey25")
  } +
  annotate("text", x = xl[2] - inset_x, y = yl[2] - inset_y, hjust = 1, vjust = 1,
           label = "MOTOR THEMES\nwell developed & driving the field",
           color = quad_cols[["Motor themes"]], fontface = "bold", size = 4.2, alpha = .8) +
  annotate("text", x = xl[1] + inset_x, y = yl[2] - inset_y, hjust = 0, vjust = 1,
           label = "NICHE THEMES\nwell developed, peripheral specialties",
           color = quad_cols[["Niche themes"]], fontface = "bold", size = 4.2, alpha = .8) +
  annotate("text", x = xl[1] + inset_x, y = yl[1] + inset_y, hjust = 0, vjust = 0,
           label = "EMERGING OR DECLINING\nmargin of the field",
           color = quad_cols[["Emerging or declining themes"]], fontface = "bold", size = 4.2, alpha = .8) +
  annotate("text", x = xl[2] - inset_x, y = yl[1] + inset_y, hjust = 1, vjust = 0,
           label = "BASIC THEMES\ntransversal, still undeveloped",
           color = quad_cols[["Basic themes"]], fontface = "bold", size = 4.2, alpha = .8) +
  coord_cartesian(xlim = xl, ylim = yl) +
  scale_x_continuous(name = "Relevance degree (Centrality, centred rank)") +
  scale_y_continuous(name = "Development degree (Density, centred rank)") +
  theme_minimal(base_size = 13) +
  theme(
    panel.border     = element_rect(fill = NA, colour = "grey75"),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(colour = "grey92"),
    legend.position  = "right",
    legend.background = element_rect(fill = "white", colour = NA)
  )

ggsave(file.path(outdir, "enhanced_thematic_map.png"), g,
       width = 10.5, height = 7.4, dpi = 300, bg = "white")
ggsave(file.path(outdir, "enhanced_thematic_map.svg"), g,
       width = 10.5, height = 7.4, bg = "white")
cat(">> saved enhanced_thematic_map.png / .svg\n")

# --- interactive version ----------------------------------------------------
if (requireNamespace("plotly", quietly = TRUE) &&
    requireNamespace("htmlwidgets", quietly = TRUE)) {
  gp <- plotly::ggplotly(g, tooltip = "text") %>%
    plotly::config(displayModeBar = FALSE)
  htmlwidgets::saveHTML(gp, file = file.path(outdir, "enhanced_thematic_map_interactive.html"))
  cat(">> saved enhanced_thematic_map_interactive.html\n")
}

# --- export the cluster table ----------------------------------------------
out <- cl %>%
  select(name, words, quadrant, centrality, density, rcentrality, rdensity,
         cx, cy, freq, fuzzy_cardinality, color) %>%
  arrange(desc(fuzzy_cardinality))
write.csv(out, file.path(outdir, "clusters_enhanced.csv"), row.names = FALSE)

# --- automatic interpretation ------------------------------------------------
tpl <- list(
  "Motor themes" = c(
    "MOTOR theme: both centrality and density are above the mean. The theme is strongly linked to the rest of the keyword network AND internally cohesive: it is well developed and it drives the research field.",
    "Monitor for saturation and unpack its internal structure (which sub-dimensions carry it?). Position new work here only with a clearly differentiated angle."),
  "Niche themes" = c(
    "NICHE theme: high density, low centrality. A specialised sub-field, methodologically mature and internally cohesive, but peripheral to the centre of gravity of the literature.",
    "Bridging studies that connect this niche to the motor theme(s) are the highest-value gap: they transfer rigour to the core."),
  "Basic themes" = c(
    "BASIC theme: high centrality, low density. Transversal, cross-cutting terms that appear across the whole literature without forming a coherent sub-field of their own: foundations rather than a research front.",
    "Treat as cross-cutting descriptors/covariates. Watch density over time: if it rises, the transversal topic is maturing into its own front."),
  "Emerging or declining themes" = c(
    "EMERGING OR DECLINING theme: low centrality and low density. The topic sits at the margin of the field, weakly developed and weakly connected; a static map cannot separate an embryonic front from a fading one.",
    "Decide with time: run thematicEvolution() or split the corpus into two periods. Rising centrality marks it as the next opportunity space; falling centrality relegates it to background.")
)

lines <- c("# Automatic cluster interpretation", "",
           sprintf("Generated %s from `%s` (field = %s, %d documents, %d clusters).",
                   format(Sys.Date()), basename(file), field, nrow(M), nrow(cl)),
           "Centrality/density below are the raw cluster scores; `cx`/`cy` are centred ranks (0 = mean).", "")
for (i in seq_len(nrow(out))) {
  r <- out[i, ]
  top <- paste(head(strsplit(r$words, "\n")[[1]], 5), collapse = ", ")
  lines <- c(lines,
    sprintf("## %d. %s — %s", i, r$name, r$quadrant),
    sprintf("- Keywords: %s", top),
    sprintf("- Centrality %.4f (centred rank %+.2f) · Density %.4f (centred rank %+.2f)",
            r$centrality, r$cx, r$density, r$cy),
    sprintf("- Size: %s term occurrences; ~%s documents (fuzzy cardinality)",
            format(r$freq), format(round(r$fuzzy_cardinality))),
    sprintf("- Reading: %s", tpl[[r$quadrant]][1]),
    sprintf("- Next step: %s", tpl[[r$quadrant]][2]), "")
}
writeLines(lines, file.path(outdir, "interpretation_auto.md"))
cat(">> saved interpretation_auto.md and clusters_enhanced.csv\n\n")
print(out %>% select(name, quadrant, rcentrality, rdensity, fuzzy_cardinality))
