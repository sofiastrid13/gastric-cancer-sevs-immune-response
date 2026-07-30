# Plasma-Derived Small Extracellular Vesicles in Gastric Cancer

## Overview

This repository contains the supplementary data, analysis scripts, protocols, tables, and figures generated during the study of plasma-derived small extracellular vesicles (sEVs) and their effects on immune responses during gastric cancer progression.

The study compared healthy controls, patients with chronic gastritis, and patients with gastric cancer stages I–IV. The analyses included sEV characterization, protein concentration, estimated particle abundance, soluble HLA-G levels, clinicopathological associations, cytokine responses, and soluble immune checkpoint profiles.

## Repository Structure

```text
data/          Raw, processed, and metadata files
code/          Data processing, statistical analysis, and visualization scripts
results/       Supplementary tables and figures
protocols/     Experimental and analytical protocols
docs/          Data dictionary and additional documentation
```

## Study Groups

| Code   | Clinical group           |
| ------ | ------------------------ |
| HC     | Healthy controls         |
| CG     | Chronic gastritis        |
| GC_I   | Gastric cancer stage I   |
| GC_II  | Gastric cancer stage II  |
| GC_III | Gastric cancer stage III |
| GC_IV  | Gastric cancer stage IV  |

## Data Description

The repository includes de-identified and aggregated research data related to:

* Plasma-derived sEV protein concentration
* Estimated sEV particle abundance
* Soluble HLA-G concentration
* Clinicopathological variables
* Cytokine concentrations
* Soluble immune checkpoint concentrations
* Statistical analyses and correlation matrices

A complete description of the variables, units, missing-value codes, and experimental groups is available in `docs/data_dictionary.md`.

## Experimental Methods

Small extracellular vesicles were isolated from plasma using size-exclusion chromatography and characterized by transmission electron microscopy and the detection of CD63, CD81, and CD9. Peripheral blood mononuclear cells from healthy donors were exposed to pooled sEVs from the different clinical groups. Cytokines and soluble immune checkpoints were quantified using LEGENDplex assays.

Detailed procedures are available in the `protocols/` directory.

## Reproducing the Analysis

1. Clone the repository:

```bash
git clone https://github.com/USERNAME/REPOSITORY-NAME.git
cd REPOSITORY-NAME
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the scripts following the numerical order indicated in the `code/` directory.

The processed data required to reproduce the figures and statistical analyses are available in `data/processed/`.

## Data Availability

Only de-identified, aggregated, or publication-authorized data are included in this repository. Information that could identify participants is not publicly available.

Raw clinical data subject to ethical, institutional, or consent-related restrictions are not included. Requests for controlled data access should be directed to the corresponding author and will be evaluated according to the applicable ethical and institutional requirements.

## Citation

Please cite this repository and the associated publication when using these data or scripts.

Repository citation information is provided in the `CITATION.cff` file.

Associated publication:

> Espinosa Hernández, S. A., et al. “ARTICLE TITLE.” JOURNAL, YEAR. DOI: PENDING.

## Licenses

The source code contained in the `code/` directory is licensed under the MIT License.

The datasets, tables, figures, protocols, and documentation are licensed under the Creative Commons Attribution 4.0 International License.

Users must provide appropriate attribution, indicate whether changes were made, and cite the associated publication and repository.

## Authors

* Sofía Astrid Espinosa Hernández — ORCID: [[**0009-0009-9581-9337**](https://orcid.org/0009-0009-9581-9337)]
* Josefa Rodríguez — [add affiliation and ORCID]
* Luz Dary Gutiérrez — [add affiliation and ORCID]
* Additional contributors — [add names and affiliations]

## Funding

This research was funded by Instituto Nacional de Cancerología Grant Number XRPM: C19010300-408, (to J. Rodriguez).

## Ethics Statement

The study was conducted in accordance with the Declaration of Helsinki and approved by the Ethics Committee of The Instituto Nacional de Cancerología (protocol C19010300-408 January 19th, 2017).” for studies involving humans. 

## Contact

For questions about the repository, data, or analyses, contact:

Sofía Astrid Espinosa Hernández
Email: [[sespinosah@ucentral.edu.co](mailto:sespinosah@ucentral.edu.co)]
ORCID: [[**0009-0009-9581-9337**](https://orcid.org/0009-0009-9581-9337)]

