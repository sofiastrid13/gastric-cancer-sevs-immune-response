# Figures

Two scripts that draw the publication figures. Each figure is saved as PNG and PDF.

```bash
python -m pip install numpy pandas matplotlib scipy openpyxl
```

Both scripts open a file-selection window when run without arguments.

---

## `Plot_sevs_protein 3.py`

Dot plot of sEV protein concentration per patient, with the group median as a horizontal line and the n of each group under the axis.

**Input:** `Input files/Clinical_data.xlsx` (columns `Stage` and `Highest_concentration (µg/mL)`)
**Output:** `sEVs_protein_concentration.png` (600 dpi) and `sEVs_protein_concentration.pdf`

```bash
python "Plot_sevs_protein 3.py" "../Input files/Clinical_data.xlsx" --output-dir ../Visualization
```

Without `--output-dir`, the files go to a `figures/` folder next to the input.

- Groups, in order: HC, CG, CGm, GC I, GC II, GC III, GC IV.
- Peptic ulcer is excluded; the console lists the excluded rows.
- Values are plotted in µg/mL without conversion. Horizontal jitter uses a fixed seed (2026).
- The group and concentration columns are detected automatically (English or Spanish names). If detection is ambiguous, the script asks for the sheet, header row and columns.
- Font: Times New Roman, or STIXGeneral if it is not installed.

---

## `log2fc_heatmaps 3.py`

Heatmaps of log2 fold change vs HC with a hierarchical-clustering dendrogram over the markers.

**Input:** `Input files/Processed_Data_Checkpoins_and_Cytokines 1.xlsx` (or a workbook produced by `Processed_data_Checkpoints_and_Cytokines.py`)
**Output** (300 dpi), in a `figures/` folder next to the input:

| File | Rows (time blocks) |
|---|---|
| `checkpoints_log2FC_heatmap.png` / `.pdf` | 24 h, 48 h, 72 h |
| `cytokines_log2FC_heatmap.png` / `.pdf` | 6 h (unstimulated), 36 h (stimulated), 36 h (unstimulated), 72 h (unstimulated) |

```bash
python "log2fc_heatmaps 3.py" "../Input files/Processed_Data_Checkpoins_and_Cytokines 1.xlsx"
```

### Method

- Values come from the `log2FC` column of each time block. If it is empty but `FC vs HC` is positive, log2(FC) is used.
- Only markers with at least one |log2FC| ≥ 1 are plotted.
- Groups with no value in a block are dropped from that block.
- Markers (columns) are ordered by hierarchical clustering: Euclidean distance, complete linkage, on rows without missing values.
- Colour scale is symmetric around 0 (blue = lower than HC, red = higher than HC). Cells with |log2FC| ≥ 1 are bold with a coloured border; `ND` cells are grey.

### Customisation

Edit the constants at the top of the script: `GROUPS`, `THRESHOLD`, the `blocks` in `FIGURES` (sheet headers, labels and band colours) and `rename` (display names of markers).
