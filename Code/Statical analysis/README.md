# Statistical analysis

Two scripts that turn the input workbooks into statistical tables saved as Excel files.

```bash
python -m pip install numpy pandas scipy openpyxl
```

Both scripts open file-selection windows when run without arguments.

---

## `Clinical_tables.py`

**Input:** `Input files/Clinical_data.xlsx`
**Output:** `Clinical_Tables.xlsx` (default name `<input>_Clinical_Tables.xlsx` from the command line)

```bash
python Clinical_tables.py "../Input files/Clinical_data.xlsx" -o "../Visualization/Clinical_Tables.xlsx"
```

### Output sheets

| Sheet | Content |
|---|---|
| `Table 1` | Clinicopathological characteristics: n and median (Q1–Q3) of sEV protein (µg/mL), sEV particles (particles/mL) and sHLA-G (ng/mL), with a p-value per block |
| `Table 2` | Spearman correlation between sEV protein and sHLA-G for each subgroup: n, rho, 95 % bootstrap CI, p-value |
| `Calculation details` | Unrounded medians and quartiles for every cell of Table 1 |
| `Methods` | Methods text and, for each correlation, the p-value method and number of valid bootstrap resamples |

### Groups

- **HC** = `Healthy`; **GC** = `Stage_I`–`Stage_IV`; **CG** = all other nonmalignant conditions.
- In Table 1, CG (chronic gastritis + peptic ulcer) is compared with CGm (gastritis with metaplasia). Table 2 shows peptic ulcer separately.
- Unknown *H. pylori* status is shown as its own group, never counted as negative.

### Methods

- **Table 1:** medians with linear-interpolation quartiles. Two groups → two-sided Mann–Whitney U; more than two → Kruskal–Wallis. Unknown nodal status is excluded from the test.
- **Table 2:** Spearman rho on paired nonmissing values.
  - n < 8: rho reported as descriptive only.
  - n ≥ 8: 95 % CI from 10,000 paired bootstrap resamples (percentile method).
  - Two-sided permutation p-value: exact enumeration for n ≤ 9, otherwise 99,999 Monte Carlo permutations.
- Seed: `20261024`. P-values are unadjusted; values < 0.05 are shown in bold.
- `NE` = not estimable; `NR` = not reported; `ND` = no data.

---

## `Processed_data_Checkpoints_and_Cytokines.py`

**Input:** `Input files/Concentration Checkpoints and cytokines.xlsx`
**Output:** `Processed_Data_recalculated.xlsx` next to the input (existing files are never overwritten; `_2`, `_3`… is added)

```bash
python Processed_data_Checkpoints_and_Cytokines.py "../Input files/Concentration Checkpoints and cytokines.xlsx" -o "../Visualization/Processed_Data_recalculated.xlsx"

# Optional: compare the recalculated metrics against an existing workbook
python Processed_data_Checkpoints_and_Cytokines.py input.xlsx --reference "../Input files/Processed_Data_Checkpoins_and_Cytokines 1.xlsx"
```

### Output sheets

| Sheet | Blocks (one per condition) |
|---|---|
| `Checkpoints` | 24 h, 48 h, 72 h (PBMCs) and sEVs, plus Spearman rho PBMCs vs sEVs at 24, 48 and 72 h |
| `Cytokines` | 6 h, 36 h (SC), 36 h (UC), 72 h |

For each marker and group (HC, CG, GC I–IV, SC, UC), every block contains:

| Column | Definition |
|---|---|
| `n` | Number of technical replicates with a value |
| `median ± SEM` | SEM = sample SD / √n (ND if n < 2) |
| `Q1 - Q3` | Linear interpolation (= Excel `PERCENTILE.INC`) |
| `FC vs HC` | group mean / HC mean |
| `log2FC` | log2(FC) |
| `Percentage change` | 100 × (FC − 1) |
| `Absolute difference` | group mean − HC mean |
| `Symmetric difference` | (group mean − HC mean) / (group mean + HC mean) |

### Notes

- No significance tests are performed in this script.
- Undefined results are `ND`; missing measurements are excluded, never set to zero.
- PBMC–sEV correlations pair rows by replicate label. Confirm the experimental pairing before interpreting them.
- `--reference` writes a `.validation.txt` report listing any differences in the five change metrics.
- Expected labels and column names are listed in `Input files/README.md`.
