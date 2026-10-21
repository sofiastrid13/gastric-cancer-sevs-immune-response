# LEGENDplex™ Immune Checkpoint and Inflammation Panel Data

## Overview

This folder contains two Excel workbooks with assay output from the **LEGENDplex™ Human Immune Checkpoint Panel 1 – TC (12-plex)** and the **LEGENDplex™ Human Inflammation Panel 1 (13-plex)**, both performed using V-bottom plates. The workbooks provide measurement data and assay-level information for exploring soluble immune checkpoint proteins and inflammatory cytokines/chemokines.

## Files

| File | Description |
| --- | --- |
| [`Immune_Checkpoint_Panel_English(1).xlsx`](Immune_Checkpoint_Panel_English%281%29.xlsx) | Data for 12 soluble immune checkpoint–related markers. |
| [`Inflammation_Panel_English(1).xlsx`](Inflammation_Panel_English%281%29.xlsx) | Data for 13 inflammation-related analytes. |

### Immune checkpoint panel (12-plex)

Analytes: **sCD25 (IL-2Rα), 4-1BB, sCD27, B7.2 (CD86), free active TGF-β1, CTLA-4, PD-L1, PD-L2, PD-1, TIM-3, LAG-3,** and **galectin-9**.

### Inflammation panel (13-plex)

Analytes: **IL-1β, IFN-α2, IFN-γ, TNF-α, MCP-1, IL-6, IL-8, IL-10, IL-12p70, IL-17A, IL-18, IL-23,** and **IL-33**.

## Workbook organization

Both workbooks include the following sheets:

| Sheet | Contents |
| --- | --- |
| `Experiment` | Experiment metadata and assay details. |
| `predicted_conc` | Predicted analyte concentrations, organized by measurement/sample identifiers. |
| `MFI` | Median fluorescence intensity measurements. |
| `Counts` | Recorded bead/event counts. |
| `CV (MFI)` | Coefficient-of-variation information for MFI. |
| `Std. Curves` | Standard-curve-related information. |
| Analyte-specific sheets | Detailed results for each marker, including standard/sample identifiers and available concentration, recovery, fluorescence, and count fields. |

The immune checkpoint workbook has **18 sheets**; the inflammation workbook has **19 sheets**.

## Data interpretation

- **MFI**: median fluorescence intensity.
- **CV**: coefficient of variation.
- **ND**: not determined / no data available. Do not interpret ND as a measured zero.
- **`<` and `>`**: values reported below or above an assay/reporting limit, respectively; these should not be treated as exact numeric concentrations.
- **Replicate and sample labels**: retain their meanings as recorded in each workbook; consult the experimental protocol for mapping to biological conditions.

For quantitative analyses, verify the concentration units, calibration range, quality-control criteria, sample dilution factors, and treatment of censored values against the corresponding assay documentation before comparing markers or experiments.

## Suggested use

1. Open the relevant Excel workbook.
2. Inspect `Experiment` for assay context and `Std. Curves` for calibration details.
3. Use `predicted_conc` for reported concentration values and `MFI`/`Counts` for supporting measurement-level review.
4. Consult the analyte-specific sheets when checking replicate-level results or investigating out-of-range values.
5. Document any filtering, normalization, or statistical procedures in downstream analyses.

## Notes

These workbooks are shared as assay data files. Their inclusion does not by itself imply that every reported measurement passed quality control or that any biological or statistical conclusion has been validated. Interpret results in conjunction with the experimental design and assay manufacturer's instructions.
