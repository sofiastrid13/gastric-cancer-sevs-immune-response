# Clinical and sEV-Related Dataset in Gastric Cancer and Chronic Gastritis

## Overview

This repository contains Excel datasets used to characterize clinical features and measurements related to small extracellular vesicles (sEVs) and soluble human leukocyte antigen G (sHLA-G) in plasma samples from healthy controls, patients with chronic gastritis, and patients with gastric cancer.

The study dataset includes **45 samples** distributed across three clinical groups:

| Clinical group | Abbreviation | Samples |
|---|---|---:|
| Healthy controls | HC | 5 |
| Chronic gastritis | CG | 20 |
| Gastric cancer | GC | 20 |
| **Total** | | **45** |

The files provide clinical and clinicopathological variables alongside sHLA-G levels and sEV-related measurements. They may be used for exploratory analyses, comparisons between clinical groups, and investigation of associations between clinical characteristics and the reported measurements.

## Repository files

| File | Description | Data records |
|---|---|---:|
| [`HEALTHY(1).xlsx`](HEALTHY.xlsx) | Healthy-control sample characteristics and measurements. | 5 |
| [`CHRONIC_GASTRITIS(1).xlsx`](CHRONIC_GASTRITIS.xlsx) | Chronic-gastritis sample characteristics, benign pathology and measurements. | 20 |
| [`GASTRIC_CANCER(1).xlsx`](GASTRIC_CANCER.xlsx) | Gastric-cancer clinicopathological characteristics, including tumor stage and associated measurements. | 20 |
| [`TOTAL_TABLE.xlsx`](TOTAL_TABLE.xlsx) | Consolidated dataset containing all three clinical groups. | 45 |

**Note:** The group-specific spreadsheets and consolidated file do not have identical column structures. The healthy-control workbook also contains blank formatted rows; only five rows contain sample records.

## Data dictionary

The following fields appear in one or more spreadsheets. Column names can differ slightly between the group-specific files and the consolidated dataset.

| Variable | Description |
|---|---|
| `Patient_ID` | Sample or participant identifier as recorded in the dataset. |
| `Sex` | Recorded sex (e.g., M/F or Male/Female). |
| `Age` | Age in years. |
| `Benign_pathology_type` | Benign pathological diagnosis, where applicable to chronic gastritis. |
| `Malignant_pathology_type` | Gastric-cancer histological classification, where available. |
| `Helicobacter_pylori` | Recorded *Helicobacter pylori* status. |
| `Differentiation_grade` | Tumor differentiation grade. |
| `Lymph_node_involvement` | Recorded lymph-node involvement status. |
| `Tumor_location` | Recorded anatomical location of the gastric tumor. |
| `Metastatic_involvement` | Recorded metastatic involvement status. |
| `TNM` | Recorded tumor–node–metastasis classification. |
| `T`, `N`, `M` | Separate TNM components provided in the gastric-cancer-specific file. |
| `Stage` | Clinical group in the consolidated file, or cancer stage in the gastric-cancer-specific file. **Interpret according to the source file.** |
| `sHLA-G_level (ng/mL)` / `sHLA-G_level` | Measured soluble HLA-G level. The chronic-gastritis workbook omits the unit from the column header; consult the study methods when interpreting units. |
| `Vital_status` | Recorded vital status, when available. |
| `Fraction_number` | Number of the recorded fraction associated with the measurement. |
| `Highest_concentration (µg/mL)` | Recorded protein concentration (µg/mL), as labeled in the dataset. |
| `Particles/mL` | Recorded particle concentration per milliliter. |

### Missing values and coding conventions

- `NA`, `No_data`, and `No data` appear in the source files and should be treated according to the intended analysis as missing or unavailable information, rather than automatically as negative findings.
- Categorical labels and sex encodings are not completely standardized across all files.
- For cancer-stage analyses, use the actual GC stage labels (e.g., `Stage_I`–`Stage_IV`) and do not interpret `Healthy` or `Chronic_gastritis` as cancer stages.
- Some TNM entries are retained as originally recorded; validate and harmonize them before stage-based calculations.

## Suggested use

1. Download the required `.xlsx` file or clone this repository.
2. Use `TOTAL_TABLE.xlsx` for cross-group analyses, or the group-specific files for analyses requiring their additional clinical variables.
3. Verify category labels, missing values, units, and participant identifiers before applying statistical tests.
4. Use appropriate statistical methods and distinguish independent biological samples from technical replicates.

## Study context and interpretation

The measurements were collected as part of research into sEVs and sHLA-G in the context of gastric disease. The files contain **sample-level data**, not measurements for each technical replicate or results of the downstream functional PBMC assays. The entries should not be interpreted as diagnostic thresholds or as evidence of causal effects.

## Data availability

The Excel workbooks in this repository constitute the datasets documented here. Additional code, figures, or supplementary tables, if deposited elsewhere in the repository, should be consulted separately; they are not described by these four spreadsheets.

## Citation

If you use these data, please cite the associated thesis or publication once its full bibliographic information is available.

## Contact

For questions about the dataset, please open an issue in this repository.
