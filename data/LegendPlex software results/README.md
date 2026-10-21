# LEGENDplex Multiplex Immunoassay Data

This folder contains two Excel workbooks with experimental results exported from **LEGENDplex™ multiplex bead-based assays**. The datasets cover soluble immune checkpoint proteins and inflammatory cytokines/chemokines and provide concentration estimates alongside fluorescence signals and assay-quality information.

## Files

| File | Assay | Analytes |
|---|---|---|
| `LEGENDplexTM Human Immune Checkpoint Panel 1 – TC (12-plex) with V-bottom Plate.xlsx` | Human Immune Checkpoint Panel 1 (12-plex) | sCD25 (IL-2Rα), 4-1BB, sCD27, B7.2 (CD86), free active TGF-β1, CTLA-4, PD-L1, PD-L2, PD-1, TIM-3, LAG-3, and galectin-9 |
| `LEGENDplexTM Human Inflammation Panel 1 (13-plex) with V-Bottom Plate.xlsx` | Human Inflammation Panel 1 (13-plex) | IL-1β, IFN-α2, IFN-γ, TNF-α, MCP-1, IL-6, IL-8, IL-10, IL-12p70, IL-17A, IL-18, IL-23, and IL-33 |

## Workbook structure

Each workbook contains the following worksheets:

- **`Experiment`** — Assay/run information and standard-curve fitting or detection/quantification parameters.
- **`predicted_conc`** — Estimated analyte concentrations, arranged by the sample identifiers and available experimental metadata (e.g., replicate, time, and/or stimulation condition).
- **`MFI`** — Median fluorescence intensity measurements.
- **`Counts`** — Bead/event counts associated with the reported measurements.
- **`CV (MFI)`** — Coefficients of variation for fluorescence intensity, when available.
- **`Std. Curves`** — Worksheet reserved for standard-curve output; it may be empty in these exports.
- **Analyte-specific worksheets** — Detailed well-level assay records, including standard/sample identifiers, expected and predicted concentrations, recovery, MFI, and counts when available.

## Recommended use

1. Open the desired Excel workbook.
2. Use `predicted_conc` for concentration-based summaries and `MFI`/`Counts` for signal and quality checks.
3. Consult the analyte-specific worksheets and `Experiment` sheet before interpreting values or excluding measurements.
4. Match sample identifiers, replicates, time points, and experimental conditions to the study's sample metadata before running comparative analyses.

## Data interpretation notes

- Values marked with `<` or `>` indicate results outside a reported assay threshold or measurement range; **do not automatically treat them as ordinary numeric values**.
- `ND`, `NA`, and blank cells should be assessed as missing or undefined metadata/results according to their context.
- Verify measurement units, sample dilutions, standard-curve quality, and detection limits in the assay documentation before combining results across panels.
- Technical replicates alone do not establish independent biological replication or support population-level statistical inference.

## Format

Microsoft Excel (`.xlsx`). The original workbook organization is preserved for traceability.

## Assay information

LEGENDplex™ is a multiplex bead-based immunoassay platform from BioLegend. Refer to the corresponding manufacturer's protocols for assay-specific procedures and interpretation guidance.
