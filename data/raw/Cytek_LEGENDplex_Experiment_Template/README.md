# Cytek LEGENDplex Experiment Template

This directory contains the raw flow cytometry data generated for the LEGENDplex assays.

## Directory Structure

```text
data/raw/Cytek_LEGENDplex_Experiment_Template/
├── checkpoints/
│   ├── samples/
│   ├── setup/
│   └── standards/
└── cytokines/
    ├── samples/
    ├── setup/
    └── standards/
```

The `checkpoints/` and `cytokines/` directories contain the corresponding `.fcs` files organized into:

* `samples/`: Experimental sample files.
* `setup/`: Instrument setup and assay configuration files.
* `standards/`: Standard files used to generate the calibration curves.

Detailed instructions for importing, gating, reviewing, and processing these data in the LEGENDplex Data Analysis Software are available in:

```text
protocols/legendplex_analysis.md
```

The raw `.fcs` files should remain unchanged to preserve data integrity and reproducibility.
