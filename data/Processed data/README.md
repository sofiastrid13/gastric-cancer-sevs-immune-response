# Immune Checkpoint and Cytokine Data

This folder contains concentration measurements and processed summaries of immune checkpoint proteins and cytokines associated with the study of small extracellular vesicles (sEVs) and PBMC immune responses in healthy controls, chronic gastritis, and gastric cancer.

## Files

| File | Contents |
| --- | --- |
| [Concentration_Checkpoints_and_Cytokines.xlsx](Concentration_Checkpoints_and_Cytokines.xlsx) | Replicate-level concentrations, experimental conditions, and a combined checkpoint–cytokine dataset at 72 h. |
| [Processed_Data.xlsx](Processed_Data.xlsx) | Descriptive summaries, comparisons against HC, quartile formulas, and Spearman correlation summaries. |

## Workbook structure

### Concentration_Checkpoints_and_Cytokines.xlsx

| Worksheet | Description |
| --- | --- |
| `Checkpoints` | Immune checkpoint measurements organized by clinical group/stage, replicate, and time. Includes 24, 48, and 72 h observations and sEV-labelled entries recorded at time 0. |
| `Cytokines` | Cytokine measurements organized by clinical group/stage, replicate, time, and stimulation condition. Recorded times are 6, 36, and 72 h. |
| `C & C 72 h` | Combined checkpoint and cytokine measurements at 72 h. |

The checkpoint panel contains 4-1BB, B7.2 (CD86), LAG-3, sCD25 (IL-2Rα), PD-L1, PD-1, PD-L2, CTLA-4, Tim-3, Galectin-9, sCD27, and a column labelled `Free Active` (free active TGF-β1 in the study).

The cytokine panel contains TNF-α, IFN-γ, IL-10, IL-8, IFN-α2, MCP-1, IL-6, IL-1β, IL-12p70, IL-18, IL-23, IL-33, and IL-17A. Not every analyte has a value for every condition or replicate.

### Processed_Data.xlsx

| Worksheet | Description |
| --- | --- |
| `Checkpoints` | PBMC-associated summaries at 24, 48, and 72 h; sEV-associated summaries; HC-referenced changes; and PBMC–sEV Spearman coefficients and interpretations. |
| `Spearman checkpoints` | Lists of checkpoint pairs under columns labelled `rho = 1` and `rho = - 1`, grouped by clinical condition and time. |
| `Cytokines` | Summaries at 6 h, 36 h (SC), 36 h (UC), and 72 h, with HC-referenced changes. |
| `Spearman Cytokines` | Lists of cytokine pairs under columns labelled `rho = 1` and `rho = - 1`, grouped by clinical condition and time/stimulation condition. |
| `Spearman 72 h` | Correlation summaries for the combined checkpoint and cytokine panel at 72 h. |

The Spearman summary sheets are selected pair listings, not complete numerical correlation matrices.

## Abbreviations and data fields

| Label | Meaning |
| --- | --- |
| HC | Healthy controls; reference group for fold-change comparisons. |
| CG | Chronic gastritis. |
| GC I–IV | Gastric cancer, clinical stages I–IV. |
| SC / UC | Stimulated / unstimulated control or condition, according to the worksheet context. |
| S / U | Stimulated / unstimulated, in the `Stimulation` column. |
| R1–R3 | Technical replicate identifiers. |
| PBMCs | Peripheral blood mononuclear cells. |
| sEVs | Small extracellular vesicles. |
| Time | Sampling time in hours. |
| n | Number of available observations in the corresponding summary; not necessarily the number of independent donors. |
| SD | Standard deviation, as labelled in the workbook. |
| Q1 / Q3 | First and third quartiles. |
| FC / log2FC | Fold change / base-2 logarithm of fold change. |
| rho (ρ) | Spearman rank correlation coefficient. |

Concentration units are **pg/mL**, as indicated in the processed workbook. `ND` and blank cells must not be interpreted as zero. The files do not provide a cell-specific reason for every missing value; in correlation listings, `ND` does not establish that an analyte was below its detection limit.

## HC-referenced comparison columns

The processed workbook provides `FC vs HC`, `log2FC`, `Percentage change`, `Absolute difference`, and `Symmetric difference`.

For a group concentration summary **X** and its matched HC reference **H**, the comparison columns follow these relationships:

| Metric | Relationship |
| --- | --- |
| FC vs HC | X / H |
| log2FC | log₂(X / H) |
| Percentage change | 100 × (X / H − 1) |
| Absolute difference | X − H; this column is signed despite its name. |
| Symmetric difference | (X − H) / (X + H); reported as a fraction. |

FC > 1 and positive log2FC indicate an increase relative to HC; FC < 1 and negative log2FC indicate a decrease. Match the analyte, time, stimulation condition, and sample type before making comparisons. These measures describe changes, not statistical significance.

The displayed descriptive statistic is labelled `median ± SD`. Do not assume the comparison columns were calculated from that displayed median: replicate means can differ from medians, and the stored comparison values are not consistently reproduced by ratios of displayed medians. Consult the original calculation workflow before recomputing these columns.

## Use and interpretation

1. Keep both Excel files alongside this README so the relative links work on GitHub.
2. Use the concentration workbook for replicate-level inspection and the processed workbook for the existing summaries.
3. Preserve the distinction between clinical group, cancer stage, stimulation condition, and technical replicate.
4. When importing into Python or R, handle decimal-comma strings explicitly, particularly in `C & C 72 h` and formatted summary cells. Ignore empty formatting-only rows and parse summary labels separately from numeric measurements.

The processed workbook contains Q1–Q3 formulas that reference an external workbook using the original Spanish sheet names (`Puntos de control todos los dat` and `Citoquinas todos los datos`). Merely placing these two supplied files together does not resolve those links. Recalculation requires the original source or an explicit remapping to the corresponding data. The spreadsheets are documented here as supplied; their formulas and values have not been modified or independently recalculated.

The functional assay uses PBMCs from a single donor with technical replicates and pooled sEV preparations. Technical replicates do not constitute independent biological replicates. Interpret these summaries and correlations descriptively; they do not establish population-level differences or biological reproducibility. Perfect rank correlations in small technical-replicate sets require particular caution.
