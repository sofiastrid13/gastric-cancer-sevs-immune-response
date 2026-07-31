# LEGENDplex™ Data Processing

This document describes the procedure used to upload, review, and process flow cytometry files (`.fcs`) in the **LEGENDplex™ Data Analysis Software**, available at [https://legendplex.qognit.com/](https://legendplex.qognit.com/).

The software workflow is divided into five sections: **Beads**, **Standards**, **Samples**, **Review Gating**, and **Results**.

## 1. Assay panels used

The data were processed using the following kits:

### LEGENDplex™ Human Inflammation Panel 1 (13-plex)

This panel quantifies the following analytes:

- IL-1β
- IFN-α2
- IFN-γ
- TNF-α
- MCP-1
- IL-6
- IL-8
- IL-10
- IL-12p70
- IL-17A
- IL-18
- IL-23
- IL-33

### LEGENDplex™ Human Immune Checkpoint Panel 1 (12-plex)

This panel quantifies the following analytes:

- sCD25 (IL-2Rα)
- 4-1BB (CD137)
- sCD27
- B7.2 (CD86)
- Free Active TGF-β1
- CTLA-4
- PD-L1
- PD-L2
- PD-1
- TIM-3
- LAG-3
- Galectin-9

## 2. Required files

Before starting the analysis, the `.fcs` files were organized into three groups:

```text
legendplex_analysis/
├── beads/
│   ├── PE_beads.fcs
│   └── Raw_beads.fcs
├── standards/
│   ├── C0_rep1.fcs
│   ├── C0_rep2.fcs
│   ├── C1_rep1.fcs
│   └── ...
├── samples/
│   ├── sample_01_rep1.fcs
│   ├── sample_01_rep2.fcs
│   └── ...
└── results/
```

- **PE beads:** control used to verify the signal in the PE reporter channel.
- **Raw beads:** unstained bead control used to identify bead populations and establish the initial gating strategy.
- **Standards:** files corresponding to the blank and the standard-curve points.
- **Samples:** files corresponding to the experimental samples and their replicates.

Simple, unique, and consistent file names are recommended. File names should make it possible to identify the sample, experimental group, time point, and replicate.

Example:

```text
GC_I_R1_6h.fcs
GC_I_R2_6h.fcs
GC_IV_R1_36h.fcs
```

## 3. Accessing the software

1. Go to [https://legendplex.qognit.com/](https://legendplex.qognit.com/).
2. Sign in with the registered account.
3. Create a new experiment or workspace.
4. Proceed through the tabs in the following order:

```text
Beads → Standards → Samples → Review Gating → Results
```

## 4. Bead configuration

In the **Beads** tab, select the assay panel corresponding to the kit used.

The panel can be loaded using:

- **Lot Number**, when the kit lot number is available.
- **Name**, by selecting the corresponding BioLegend panel.
- **Custom**, when the analytes, bead IDs, maximum concentrations, and units must be entered manually.

For this analysis, concentrations were expressed in `pg/mL`.

Each analyte was verified against its corresponding bead ID in both the **A bead** and **B bead** populations. This assignment must match the kit configuration and should not be changed arbitrarily.

## 5. Uploading the standards

In the **Standards** tab, the standard curve was configured as follows:

- **Number of Curve Points:** 8.
- **Dilution factor:** 4.
- **Blank included:** enabled.
- **Replicates:**
  - 2 replicates for the Human Inflammation Panel 1.
  - 3 replicates for the Human Immune Checkpoint Panel 1.

The following procedure was then performed:

1. Click **Select Standards FCS file(s)**.
2. Upload the blank and all standard files.
3. Assign the files correctly to `C0`, `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, and `C7`.
4. Confirm that replicates from the same concentration have the same standard name.
5. Verify that all files display a valid status before continuing.

### Acquisition channels

The following channels were used:

- **PE Reporter Channel:** `B4-A`.
- **APC Bead Channel:** `R1-A`.

The **PE** channel represents the fluorescence intensity associated with the amount of analyte bound to each bead population. The **APC** channel distinguishes the different bead populations and links each population to its corresponding analyte.

Channel names may vary among flow cytometers. Therefore, before running the analysis, confirm that `B4-A` corresponds to the PE detector and that `R1-A` corresponds to the APC detector in the instrument configuration used.

## 6. Uploading the samples

In the **Samples** tab, upload the `.fcs` files corresponding to the experimental samples:

1. Click **Select Samples FCS file(s)**.
2. Upload all files corresponding to the samples.
3. Review the **FCS File List** table.
4. Edit the **Sample Name** field so that all replicates from the same sample have the same name.
5. Enter the dilution factor applied to each sample in the **Dilution** column.
6. Click **Set Replicates** to group the technical replicates correctly.
7. Click **Upload**.
8. Confirm that standards and samples display a valid status.
9. Click **Run Gating**.

Replicates should not be grouped only because their file names are similar. Confirm that they truly correspond to the same sample, experimental condition, and time point.

## 7. Gating review

Gating was reviewed in the **Review Gating** tab using the **Review** option.

Each file was inspected individually, including:

- Standards.
- PE beads.
- Raw beads.
- Experimental samples.

### 7.1. Initial bead separation

In the `FSC-A` versus `SSC-A` plot, the following bead regions were verified:

- **A beads**, corresponding to the smaller bead population.
- **B beads**, corresponding to the larger bead population.

The gates were adjusted to include the main bead populations while excluding debris, electronic noise, aggregates, and events outside the bead clouds.

The **Raw beads** control was used as a reference to identify the basal distribution of the A and B bead populations. The **PE beads** control was used to verify PE reporter detection and the expected location of beads showing PE signal.

### 7.2. Identification of bead populations by APC

After separating the A and B bead populations, the APC-channel histograms (`R1-A`) were reviewed.

Each peak should:

- Fall within its corresponding gate.
- Align with the bead ID assigned to the analyte.
- Maintain the expected order defined by the assay panel.
- Show sufficient separation from adjacent peaks.

The gates were adjusted when a peak was partially excluded, when two populations were incorrectly overlapped, or when the automatic selection did not match the observed distribution.

The identity of a bead population must not be changed simply to improve the results. The position and order of the peaks should remain consistent with the **PE beads**, **Raw beads**, standards, and kit-specific configuration.

### 7.3. Applying the gating strategy

Once the bead populations had been verified:

1. Click **Apply Gating**.
2. Confirm that the gating was applied correctly.
3. Mark the file as reviewed.
4. Continue with the next file.

When equivalent patterns were observed across files, **Convert Gates** or the gate-transfer function was used as a starting point. However, each file was inspected individually before approval.

Samples with very low event counts per bead population, insufficient peak separation, or abnormal distributions were flagged for additional review and possible technical exclusion.

## 8. Generation and optimization of standard curves

In the **Results** tab, the standard curve for each analyte was inspected. The software allows four-parameter or five-parameter logistic curve fitting, depending on the selected settings and the behavior of the data.

The following criteria were evaluated for each analyte:

- Distribution of the standard points.
- Agreement among replicates.
- Sigmoidal shape of the curve.
- Coefficient of determination (`R²`).
- Limit of detection (`LOD`).
- Useful quantification range.
- Number of samples whose concentrations could be calculated within the curve range.

The most technically appropriate standard points were selected to obtain curves with a high `R²` and to calculate the largest possible number of experimental concentrations.

Standard points were excluded only when there was evidence of technical failure, such as:

- Clearly discordant replicates.
- Insufficient event counts.
- Signal inconsistent with the expected concentration order.
- Extreme signal saturation.
- Acquisition or gating errors.

Points were not removed solely to artificially increase the `R²`. Every curve modification should be documented in a quality-control record, including the analyte, the excluded point, and the technical reason for exclusion.

Whenever possible, the selected curve fit prioritized the following criteria:

1. High `R²`.
2. Biologically and technically coherent sigmoidal behavior.
3. Consistent replicates.
4. Low residual error.
5. Broad coverage of the sample concentration range.
6. The lowest possible number of out-of-range results.

Samples below the quantification range should be reported as lower than the corresponding limit. Samples above the highest standard should be repeated using an additional dilution whenever sufficient sample volume is available.

## 9. Exporting the results

Once the curves had been approved:

1. Click **Report**.
2. Export the complete report.
3. Download the concentration table in Excel or CSV format.
4. Retain the MFI values, calculated concentrations, quality indicators, and out-of-range results.
5. Save an unmodified copy of the original report together with the table used for statistical analysis.

Recommended structure:

```text
results/
├── raw_export/
│   ├── LEGENDplex_report_original.xlsx
│   └── LEGENDplex_report_original.pdf
├── processed/
│   └── concentrations_cleaned.csv
└── quality_control/
    ├── excluded_standard_points.csv
    └── gating_notes.md
```

## 10. Quality control and traceability

To ensure reproducibility, the following information was recorded:

- Software name and version.
- Date of analysis.
- Kit name and lot number.
- Selected assay panel.
- PE and APC channels used.
- Number of standard-curve points and replicates.
- Dilution factors for standards and samples.
- Files included or excluded.
- Manual changes made during gating.
- Standard-curve points removed.
- Technical justification for each exclusion.
- Curve model used.
- `R²`, `LOD`, and quantification range for each analyte.

## 11. Suggested exclusion log

```csv
panel,analyte,standard_point,replicate,action,reason,date,analyst
Inflammation Panel 1,IL-17A,C6,2,Excluded,Low bead count,YYYY-MM-DD,Initials
Immune Checkpoint Panel 1,PD-L1,C7,1,Excluded,Signal saturation,YYYY-MM-DD,Initials
```

## 12. References

- BioLegend. *LEGENDplex™ Data Analysis Software User Guide*.
- BioLegend. *LEGENDplex™ Human Inflammation Panel 1 (13-plex)*.
- BioLegend. *LEGENDplex™ Human Immune Checkpoint Panel 1 (12-plex)*.
- Analysis platform: [https://legendplex.qognit.com/](https://legendplex.qognit.com/).

---

**Note:** This procedure documents the configuration applied in this project. Channel names, dilution factors, number of replicates, and bead assignments should always be verified against the lot-specific manual, the flow cytometer configuration, and the corresponding experimental design.
