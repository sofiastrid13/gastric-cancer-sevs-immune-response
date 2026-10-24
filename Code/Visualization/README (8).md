# Visualization

Outputs produced by the scripts in `Statical analysis/` and `Figures/` from the workbooks in `Input files/`.

## Tables (Excel)

| File | Produced by | Input | Content |
|---|---|---|---|
| `Clinical_Tables.xlsx` | `Statical analysis/Clinical_tables.py` | `Clinical_data.xlsx` | Table 1 (clinicopathological characteristics), Table 2 (Spearman sEV protein vs sHLA-G), calculation details, methods |
| `Processed_Data_recalculated.xlsx` | `Statical analysis/Processed_data_Checkpoints_and_Cytokines.py` | `Concentration Checkpoints and cytokines.xlsx` | Median ± SEM, quartiles and fold changes vs HC for each checkpoint and cytokine |

## Figures (PNG and PDF)

| File | Produced by | Input | Description |
|---|---|---|---|
| `sEVs_protein_concentration.png` / `.pdf` | `Figures/Plot_sevs_protein 3.py` | `Clinical_data.xlsx` | sEV protein concentration (µg/mL) per patient and group median, HC to GC IV |
| `checkpoints_log2FC_heatmap.png` / `.pdf` | `Figures/log2fc_heatmaps 3.py` | `Processed_Data_Checkpoins_and_Cytokines 1.xlsx` | log2FC vs HC of immune checkpoints at 24, 48 and 72 h |
| `cytokines_log2FC_heatmap.png` / `.pdf` | `Figures/log2fc_heatmaps 3.py` | `Processed_Data_Checkpoins_and_Cytokines 1.xlsx` | log2FC vs HC of cytokines at 6, 36 and 72 h |

PNG files are for quick viewing (600 dpi for the dot plot, 300 dpi for the heatmaps). PDF files are vector graphics for publication.

## Regenerating

These files are calculated outputs. If the input data change, rerun the scripts (see the main `README.md`) instead of editing the outputs by hand.
