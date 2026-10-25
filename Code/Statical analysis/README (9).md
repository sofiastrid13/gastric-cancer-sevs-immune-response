# Statistical analysis

Python scripts that rebuild the clinical tables and the checkpoint/cytokine tables from the source Excel workbooks. Every statistic is computed from the input data each time a script runs. No values are hardcoded.

| Script | Input | Output |
|---|---|---|
| `Clinical_tables.py` | Patient-level clinical workbook (`TOTAL_TABLE.xlsx`) | Table 1 (clinicopathological characteristics) and Table 2 (sEV protein vs. sHLA-G Spearman correlations) |
| `Processed_data_Checkpoints_and_Cytokines.py` | Concentration workbook (checkpoints and cytokines) | Concentration summaries, fold changes and Spearman correlation tables |

## Requirements

- Python 3.9 or later
- `numpy`, `pandas`, `scipy`, `openpyxl`
- `tkinter` (optional; needed only for the file-picker dialogs)

```bash
python -m pip install numpy pandas scipy openpyxl
```

If a package is missing, `Processed_data_Checkpoints_and_Cytokines.py` prints the exact `pip install` command for the interpreter you are using.

---

## 1. `Clinical_tables.py`

### Input

An `.xlsx` workbook with **exactly one** worksheet that contains these columns (one row per patient, unique `Patient_ID`):

```
Patient_ID, Sex, Age, Malignant_pathology_type, Helicobacter_pylori,
Differentiation_grade, Lymph_node_involvement, Tumor_location,
Metastatic_involvement, TNM, Stage, sHLA-G_level (ng/mL),
Vital_status, Highest_concentration (µg/mL), Particles/mL
```

- `Stage` must be one of: `Healthy`, `Chronic_gastritis`, `Chronic_gastritis_(metaplasia)`, `Peptic_ulcer`, `Stage_I`, `Stage_II`, `Stage_III`, `Stage_IV`.
- Missing numeric values can be blank, `NA`, `ND`, `NaN` or `No_data`. Negative or infinite values cause an error.
- Patients are grouped as **HC** (healthy controls), **CG** (non-malignant gastric conditions) and **GC** (gastric cancer, stages I–IV).
- T and N are parsed from `TNM` (for example, `T1a` → T1, `T4b` → T4).

### Usage

```bash
# Native dialogs to select the input and output files
python Clinical_tables.py

# Command line
python Clinical_tables.py TOTAL_TABLE.xlsx -o Clinical_Tables.xlsx
```

If `-o` is omitted, the output is saved as `<input>_Clinical_Tables.xlsx` beside the input.

### Output sheets

| Sheet | Contents |
|---|---|
| `Table 1` | n and median (Q1–Q3) of sEV protein (µg/mL), sEV particles/mL and sHLA-G (ng/mL) by age, sex, clinical group, stage, Lauren subtype, nodal involvement and vital status, with block-level p-values |
| `Table 2` | Spearman ρ, n, 95% bootstrap CI and permutation p-value for sEV protein vs. sHLA-G, by subgroup |
| `Calculation details` | Unrounded median, Q1, Q3, test and p-value for each cell in Table 1 |
| `Methods` | Data source, grouping rules, statistical methods and a correlation audit trail |

### Statistical methods

- **Descriptives:** median and Q1/Q3 with linear interpolation. n is the number of available values for each measure.
- **Group comparisons:** two-sided Mann–Whitney U for two groups and Kruskal–Wallis for three or more groups (SciPy). Each p-value tests the whole block and appears on its first row. Unknown nodal status is excluded from the test.
- **Correlations:** Spearman ρ on paired, non-missing values.
  - n < 8: ρ is reported as descriptive only.
  - n ≥ 8: 10,000 paired bootstrap resamples (percentile 95% CI) and a two-sided permutation test on |ρ|. The test is exact for n ≤ 9 and uses 99,999 Monte Carlo permutations otherwise, with p = (b + 1)/(B + 1).
  - `NE` = not estimable (fewer than 2 pairs or a constant variable). `NR` = not reported.
- P-values are unadjusted and exploratory. Values below 0.05 are shown in bold.
- Seed: `20261024`.

---

## 2. `Processed_data_Checkpoints_and_Cytokines.py`

### Input

An `.xlsx` or `.xlsm` workbook with these sheets:

| Sheet | Key columns (in this order) | Then |
|---|---|---|
| `Checkpoints` | Group, `Replicate`, `Time` | One column per checkpoint marker |
| `Cytokines` | Group, `Replicate`, `Time`, `Stimulation` | One column per cytokine |
| `C & C 72 h` *(optional)* | Group, `Replicate`, `Time` | Checkpoints and cytokines at 72 h |

- Groups: `HC`, `CG`, `GC I`, `GC II`, `GC III`, `GC IV`, `SC`, `UC`. In `Checkpoints`, sEV rows use the label `sEVs <group>` with `Time = 0`.
- Checkpoint time points: 24, 48 and 72 h. Cytokine conditions: 6 h (U), 36 h (U and S) and 72 h (U), where `U` = unstimulated and `S` = stimulated.
- `ND`, `NA` and blank cells are treated as missing. Commas are accepted as decimal separators.
- Duplicate rows (same group, replicate, time and stimulation) cause an error.
- If `C & C 72 h` is missing, it is built by merging 72 h checkpoints with 72 h unstimulated cytokines. If it exists, it is checked against the other two sheets and any difference is reported.

### Usage

```bash
# File picker (or run "Run Python File" in VS Code)
python Processed_data_Checkpoints_and_Cytokines.py

# Command line
python Processed_data_Checkpoints_and_Cytokines.py concentrations.xlsx
python Processed_data_Checkpoints_and_Cytokines.py concentrations.xlsx -o results.xlsx
python Processed_data_Checkpoints_and_Cytokines.py concentrations.xlsx --n-boot 10000 --n-perm 10000 --seed 2026

# Optional: compare the change metrics with an earlier workbook
python Processed_data_Checkpoints_and_Cytokines.py concentrations.xlsx --reference original.xlsx
```

| Option | Default | Description |
|---|---|---|
| `-o`, `--output` | `Processed_Data_recalculated.xlsx` beside the input | Output path (`.xlsx`) |
| `--n-boot` | 10000 | Bootstrap resamples |
| `--n-perm` | 10000 | Monte Carlo permutations |
| `--seed` | 20261025 | Random seed |
| `--reference` | — | Original workbook used only for validation. Writes `<output>.validation.txt` |

Existing files are never overwritten. A suffix (`_2`, `_3`, …) is added instead.

### Output sheets

| Sheet | Contents |
|---|---|
| `Checkpoints` | Per marker and group at 24/48/72 h and in sEVs: n, median ± SEM, Q1–Q3, FC vs. HC, log2FC, % change, absolute and symmetric difference. Also includes PBMC vs. sEV Spearman correlations at 24/48/72 h |
| `Spearman checkpoints` | Checkpoint vs. checkpoint correlations by group at 24, 48 and 72 h |
| `Cytokines` | The same concentration metrics at 6 h, 36 h (SC), 36 h (UC) and 72 h |
| `Spearman Cytokines` | Cytokine vs. cytokine correlations by group at 6 h, 36 h UC, 36 h SC and 72 h |
| `Spearman 72 h` | Checkpoint and cytokine correlations at 72 h by group |
| `Methods` | Parameters, correlation counts and data-consistency warnings |

### Statistical methods

- **Summary:** median ± SEM (SEM = sample SD/√n; `ND` when n < 2). Q1/Q3 use linear interpolation, equivalent to Excel `PERCENTILE.INC`.
- **Change vs. HC** (calculated from group means):
  - FC = mean / mean<sub>HC</sub>
  - log2FC = log2(FC)
  - % change = 100 · (FC − 1)
  - Absolute difference = mean − mean<sub>HC</sub>
  - Symmetric difference = (mean − mean<sub>HC</sub>) / (mean + mean<sub>HC</sub>)
- **Spearman correlations:** average ranks for ties and pairwise deletion of missing values. Rows are paired by group and replicate (plus time and stimulation).
  - p: two-sided Monte Carlo permutation test, p = (b + 1)/(B + 1).
  - 95% CI: percentile bootstrap of pairs. Resamples with a constant variable are discarded.
  - ρ is `ND` when n < 2 or a variable is constant.
  - p < 0.05 is highlighted in yellow with bold red text.
- Each correlation uses its own seed, derived from the global seed and a label, so results are reproducible.
- With n = 3 the smallest possible two-sided p is about 0.33. With n = 2, ρ is always ±1. Replicate labels alone do not prove biological pairing.

---

## Reproducibility notes

- Both scripts use fixed random seeds. Running them on the same data gives the same results.
- Missing values are excluded and never replaced with zero. Results that cannot be calculated are reported as `ND`.
- Close the output workbook in Excel before running a script again, or saving will fail.
- After changing the source data, run the scripts again.
