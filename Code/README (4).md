# sEVs, immune checkpoints and cytokines in gastric disease

Analysis code and data for the study of small extracellular vesicles (sEVs), soluble HLA-G, immune checkpoints and cytokines across clinical groups of gastric disease: healthy controls (HC), chronic gastritis (CG / CGm) and gastric cancer (GC, stages I–IV).

The repository holds the input data, two statistical-analysis scripts, two figure scripts, and the outputs they produce.

## Repository structure

```
.
├── Input files/          Excel workbooks used as inputs
├── Statical analysis/    Scripts that compute the statistical tables
├── Figures/              Scripts that draw the figures
└── Visualization/        Outputs (Excel tables, PNG and PDF figures)
```

Each folder has its own README with details.

## Workflow

| Input (`Input files/`) | Script | Output (`Visualization/`) |
|---|---|---|
| `Clinical_data.xlsx` | `Statical analysis/Clinical_tables.py` | `Clinical_Tables.xlsx` |
| `Concentration Checkpoints and cytokines.xlsx` | `Statical analysis/Processed_data_Checkpoints_and_Cytokines.py` | `Processed_Data_recalculated.xlsx` |
| `Clinical_data.xlsx` | `Figures/Plot_sevs_protein 3.py` | `sEVs_protein_concentration.png` / `.pdf` |
| `Processed_Data_Checkpoins_and_Cytokines 1.xlsx` | `Figures/log2fc_heatmaps 3.py` | `checkpoints_log2FC_heatmap.png` / `.pdf`, `cytokines_log2FC_heatmap.png` / `.pdf` |

`Processed_Data_Checkpoins_and_Cytokines 1.xlsx` is the processed workbook that feeds the heatmaps. It has the same layout as the output of `Processed_data_Checkpoints_and_Cytokines.py`, so the heatmaps can also be drawn from a freshly recalculated workbook.

## Requirements

Python 3.9 or newer.

```bash
python -m pip install numpy pandas scipy openpyxl matplotlib
```

`tkinter` (bundled with most Python installers) is only needed for the file-selection windows.

## Quick start

Every script can be run with no arguments; it then opens windows to pick the input file and, where relevant, the output location. Command-line use, from the repository root:

```bash
# Statistical tables
python "Statical analysis/Clinical_tables.py" "Input files/Clinical_data.xlsx" -o "Visualization/Clinical_Tables.xlsx"
python "Statical analysis/Processed_data_Checkpoints_and_Cytokines.py" "Input files/Concentration Checkpoints and cytokines.xlsx" -o "Visualization/Processed_Data_recalculated.xlsx"

# Figures
python "Figures/Plot_sevs_protein 3.py" "Input files/Clinical_data.xlsx" --output-dir Visualization
python "Figures/log2fc_heatmaps 3.py" "Input files/Processed_Data_Checkpoins_and_Cytokines 1.xlsx"
```

`log2fc_heatmaps 3.py` always writes to a `figures/` folder next to the input workbook; move the files to `Visualization/` afterwards.

## Clinical group abbreviations

| Code | Meaning |
|---|---|
| HC | Healthy controls |
| CG | Chronic gastritis (in some analyses including peptic ulcer, see `Statical analysis/README.md`) |
| CGm | Chronic gastritis with intestinal metaplasia |
| GC I–IV | Gastric cancer, clinical stage I–IV |
| SC / UC | Stimulated / unstimulated culture condition (cytokines at 36 h) |
| sEVs | Small extracellular vesicles |
| ND | Not determined |

## Reproducibility notes

- Bootstrap and permutation procedures use fixed seeds, so reruns give identical results.
- Missing values are excluded, never replaced with zero.
- P-values are unadjusted and exploratory.
