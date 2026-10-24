# Input files

Excel workbooks used by the scripts in `Statical analysis/` and `Figures/`.

| File | Used by | Content |
|---|---|---|
| `Clinical_data.xlsx` | `Clinical_tables.py`, `Plot_sevs_protein 3.py` | One row per patient (45 patients) |
| `Concentration Checkpoints and cytokines.xlsx` | `Processed_data_Checkpoints_and_Cytokines.py` | Raw concentrations (pg/mL) per group, replicate and time point |
| `Processed_Data_Checkpoins_and_Cytokines 1.xlsx` | `log2fc_heatmaps 3.py` | Summary statistics and fold changes vs HC |

## `Clinical_data.xlsx`

Single worksheet (`Hoja1`), one row per patient.

| Column | Description |
|---|---|
| `Patient_ID` | Unique patient identifier |
| `Sex` | `F` / `M` |
| `Age` | Years |
| `Malignant_pathology_type` | Lauren subtype: `Diffuse`, `Intestinal`, `Mixed` (GC only) |
| `Helicobacter_pylori` | `Yes`, `No` / `Absent`, or `No_data` |
| `Differentiation_grade` | `Well_differentiated`, `Moderately_differentiated`, `Poorly_differentiated` |
| `Lymph_node_involvement` | `Yes`, `No`, `No_data` |
| `Tumor_location` | e.g. `Cardia`, `Body`, `Antrum_and_pylorus` |
| `Metastatic_involvement` | `Yes` / `No` |
| `TNM` | TNM code (e.g. `T3N1M0`); T and N are parsed from it |
| `Stage` | `Healthy`, `Chronic_gastritis`, `Chronic_gastritis_(metaplasia)`, `Peptic_ulcer`, `Stage_I` … `Stage_IV` |
| `sHLA-G_level (ng/mL)` | Soluble HLA-G concentration |
| `Vital_status` | `Alive` / `Deceased` |
| `Fraction_number` | sEV fraction with the highest protein content |
| `Highest_concentration (µg/mL)` | sEV protein concentration |
| `Particles/mL` | sEV particle concentration |

Empty cells and `NA`, `ND`, `No_data` are read as missing values.

## `Concentration Checkpoints and cytokines.xlsx`

| Sheet | Columns |
|---|---|
| `Checkpoints` | `Stage`, `Replicate`, `Time` (0, 24, 48, 72 h) and 12 checkpoint markers (4-1BB, B7.2 (CD86), LAG-3, sCD25 (IL-2Ra), PD-L1, PD-1, PD-L2, CTLA-4, Tim-3, Galectin-9, sCD27, Free Active) |
| `Cytokines` | `Stage`, `Replicate`, `Time` (6, 36, 72 h), `Activation` (A / I) and 13 cytokines (TNF-α, IFN-γ, IL-10, IL-8, IFN-α2, MCP-1, IL-6, IL-1β, IL-12p70, IL-18, IL-23, IL-33, IL-17A) |
| `C & C 72 h` | Checkpoints and cytokines at 72 h together (reference only; not read by the scripts) |

Values are in pg/mL. Replicates are technical replicates, not independent donors. `Time = 0` in `Checkpoints` holds the sEV measurements.

> **Note on labels.** In this workbook the group labels are in the original coding (`CS`, `GA C`, `CG I`–`CG IV`, `Cel A`, `Cel I`, `E …` for sEVs) and the stimulation column is named `Activation`. `Processed_data_Checkpoints_and_Cytokines.py` expects the labels `HC`, `CG`, `GC I`–`GC IV`, `SC`, `UC`, `sEVs <group>` and a column named `Stimulation`. Recode the labels (or adapt the script) before running it on this file.

## `Processed_Data_Checkpoins_and_Cytokines 1.xlsx`

Same layout as the output of `Processed_data_Checkpoints_and_Cytokines.py` (sheets `Checkpoints` and `Cytokines`). See `Statical analysis/README.md` for the column definitions.
