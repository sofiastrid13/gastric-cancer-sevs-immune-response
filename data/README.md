# Data

This directory contains the de-identified and publication-authorized datasets
used in the study of plasma-derived small extracellular vesicles (sEVs) and
immune responses during gastric cancer progression.

## Directory Structure

- `raw/`: original data authorized for public release and preserved without modification.
- `processed/`: cleaned, organized, or transformed datasets used in the statistical analyses.
- `metadata/`: descriptions of samples, clinical groups, experimental conditions,
  variables, units, and coding conventions.

## Study Groups

The datasets may include the following clinical groups:

| Code | Description |
|------|-------------|
| HC | Healthy controls |
| CG | Chronic gastritis |
| GC_I | Gastric cancer stage I |
| GC_II | Gastric cancer stage II |
| GC_III | Gastric cancer stage III |
| GC_IV | Gastric cancer stage IV |

## Data Types

The available datasets may include:

- Small extracellular vesicle protein concentration
- Estimated sEV particle abundance
- Soluble HLA-G concentration
- Cytokine concentrations
- Soluble immune checkpoint concentrations
- PBMC stimulation conditions and time points
- De-identified clinicopathological variables
- Correlation matrices and statistical analysis inputs

## File Formats

Tabular data are preferably provided in `.csv` format to facilitate reuse and
compatibility with R, Python, and other statistical software.

Excel files may also be included when they contain multiple related sheets or
supplementary annotations.

## Data Processing

Files in `raw/` should not be modified. Any cleaning, normalization,
transformation, exclusion, or restructuring must be documented and saved in
`processed/`.

The scripts used to generate the processed datasets are available in the
`code/` directory.

## Missing Values

Missing or unavailable values should be represented consistently, preferably
as `NA`. Additional codes must be explained in the data dictionary located in:

`../docs/data_dictionary.md`

## Ethical and Privacy Considerations

Only de-identified, aggregated, or publication-authorized data are included.

This repository does not contain:

- Participant names
- Identification numbers
- Medical record numbers
- Contact information
- Exact identifying dates
- Restricted clinical information

Raw clinical data subject to ethical, institutional, or consent-related
restrictions are not publicly available.

## Available Files

| File | Description | Format |
|------|-------------|--------|
| `processed/sev_concentrations.csv` | sEV protein concentration by sample and clinical group | CSV |
| `processed/shla_g_concentrations.csv` | Soluble HLA-G concentrations | CSV |
| `processed/cytokine_concentrations.csv` | Cytokine concentrations by group and time point | CSV |
| `processed/immune_checkpoints.csv` | Soluble immune checkpoint concentrations | CSV |
| `metadata/sample_metadata.csv` | De-identified sample and experimental metadata | CSV |

## License

The datasets and metadata in this directory are licensed under the Creative
Commons Attribution 4.0 International License (CC BY 4.0), as described in the
`LICENSE-DATA` file located in the repository root.

Users must provide appropriate attribution, cite the repository and associated
publication, and indicate whether changes were made.
