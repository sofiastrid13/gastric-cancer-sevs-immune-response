#!/usr/bin/env python3
"""
log2FC heatmaps (checkpoints and cytokines) from the processed Excel workbook.

When run, a file dialog opens to select the Excel file
(e.g. "Processed_Data_Checkpoins_and_Cytokines.xlsx").
Two figures are produced, each saved as PNG and PDF in a "figures" folder
created next to the selected Excel file:

    checkpoints_log2FC_heatmap.png / .pdf
    cytokines_log2FC_heatmap.png   / .pdf

Expected sheet layout (as in the processed workbook):
    Row 1  : time-point headers (e.g. "24 h (pg/mL)"), one per block of columns
    Row 2  : metric headers ("n", "median ± SEM", ..., "log2FC", ...)
    Col A  : marker name rows followed by clinical-group rows (HC, CG, GC I...)

Method
    * Values shown are the "log2FC" (vs HC) column of each time-point block.
    * Only markers with at least one |log2FC| >= 1 are plotted.
    * Group rows with no available value inside a block are dropped.
    * Columns are ordered by hierarchical clustering (Euclidean distance,
      complete linkage) on the rows without missing values.

Requirements: pandas, numpy, matplotlib, scipy, openpyxl (tkinter for the dialog).
Usage:  python log2fc_heatmaps.py            (opens the file dialog)
        python log2fc_heatmaps.py file.xlsx  (skips the dialog)
"""

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import openpyxl
import matplotlib

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Patch, Rectangle
from scipy.cluster.hierarchy import dendrogram, linkage

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
GROUPS = ["CG", "GC I", "GC II", "GC III", "GC IV", "SC", "UC"]
REFERENCE_GROUP = "HC"
VALUE_COLUMN = "log2FC"
THRESHOLD = 1.0                  # |log2FC| >= THRESHOLD is highlighted
MISSING_LABEL = "ND"             # text shown in cells without a value


FIGURES = [
    {
        "sheet": "Checkpoints",
        "output": "checkpoints_log2FC_heatmap",
        # (header in row 1 of the sheet, label shown on the figure, band colour)
        "blocks": [
            ("24 h (pg/mL)", "24 h", "#dfe8f3"),
            ("48 h (pg/mL)", "48 h", "#ece3f3"),
            ("72 h (pg/mL)", "72 h", "#e0eee6"),
        ],
        # Optional display names for markers
        "rename": {"B7.2": "B7.2 (CD86)", "sCD25 (IL-2Rα)": "sCD25 (IL-2Ra)"},
    },
    {
        "sheet": "Cytokines",
        "output": "cytokines_log2FC_heatmap",
        "blocks": [
            ("6 h (pg/mL)", "6 h | Activation I", "#dfe8f3"),
            ("36 h (SC) (pg/mL)", "36 h | Activation A", "#ece3f3"),
            ("36 h (UC) (pg/mL)", "36 h | Activation I", "#e0eee6"),
            ("72 h (pg/mL)", "72 h | Activation I", "#fbe9d9"),
        ],
        "rename": {},
    },
]

# Colours
CMAP = LinearSegmentedColormap.from_list(
    "log2fc", ["#2166ac", "#f7f7f7", "#b2182b"])
NEUTRAL_FACE = "#f5f5f5"
NEUTRAL_TEXT = "#5f5f5f"
NA_FACE = "#d3d7de"
NA_TEXT = "#6b7280"
UP_EDGE, UP_TEXT = "#b2182b", "#8b1023"
DOWN_EDGE, DOWN_TEXT = "#2166ac", "#174a7c"
LINE_COLOR = "#4a5a70"

# Geometry (inches)
CELL_H = 0.30
HEATMAP_W = 4.9
STRIP_W = 0.78
ROW_LABEL_W = 0.75
LEFT_PAD = 0.05
DENDRO_H = 1.15
TOP_PAD = 0.15
BOTTOM_PAD = 1.45
CBAR_GAP, CBAR_W, RIGHT_PAD = 0.75, 0.16, 1.0


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------
def select_excel_file():
    """Open a file dialog (or use the command-line argument)."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Select the processed Excel file",
        filetypes=[("Excel files", "*.xlsx *.xlsm *.xls"), ("All files", "*.*")],
    )
    root.destroy()
    if not path:
        sys.exit("No file selected. Exiting.")
    return Path(path)


def to_float(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return np.nan  # "ND", empty, text...


def norm_text(value):
    """Normalise a header for tolerant matching (case, spaces, units, unicode)."""
    text = unicodedata.normalize("NFKC", str(value)).lower()
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\(\s*pg\s*/\s*ml\s*\)", "", text)   # drop "(pg/mL)"
    return re.sub(r"\s+", "", text)


def find_metric_row(ws, max_scan=15):
    """Row that contains the metric headers (the one with 'log2FC')."""
    target = norm_text(VALUE_COLUMN)
    for r in range(1, min(max_scan, ws.max_row) + 1):
        for c in range(1, ws.max_column + 1):
            v = ws.cell(r, c).value
            if v is not None and norm_text(v) == target:
                return r
    raise ValueError(f"No '{VALUE_COLUMN}' header found in the first {max_scan} rows "
                   f"of sheet '{ws.title}'.")


def block_header_of(ws, col, metric_row):
    """Nearest non-empty header to the left of `col` in the rows above metric_row."""
    for r in range(metric_row - 1, 0, -1):
        for c in range(col, 0, -1):
            v = ws.cell(r, c).value
            if v is not None and str(v).strip():
                return str(v).strip()
    return None


def find_value_columns(ws, block_headers):
    """Return ({block header: log2FC column}, metric_row)."""
    metric_row = find_metric_row(ws)
    target = norm_text(VALUE_COLUMN)
    found = {}                                   # original header -> column
    for c in range(1, ws.max_column + 1):
        v = ws.cell(metric_row, c).value
        if v is not None and norm_text(v) == target:
            header = block_header_of(ws, c, metric_row)
            if header is not None and header not in found:
                found[header] = c

    result = {}
    for header in block_headers:
        key = norm_text(header)
        exact = [h for h in found if norm_text(h) == key]
        partial = [h for h in found if key in norm_text(h) or norm_text(h) in key]
        match = exact or (partial if len(partial) == 1 else [])
        if not match:
            available = "\n  - ".join(found) or "(none)"
            raise ValueError(
                f"Block '{header}' not found in sheet '{ws.title}'.\n"
                f"Time-point headers found in the file:\n  - {available}\n"
                f"Edit the 'blocks' entries in FIGURES so they match these names.")
        result[header] = found[match[0]]
    return result, metric_row


def find_fc_column(ws, value_col, metric_row, max_back=10):
    """'FC vs HC' column belonging to the same block as value_col."""
    for c in range(value_col - 1, max(value_col - max_back, 0), -1):
        v = ws.cell(metric_row, c).value
        if v is not None and norm_text(v).startswith("fcvs"):
            return c
    return None


def read_sheet(ws, block_headers):
    """Return data[block][marker][group] = log2FC (NaN if not determined).

    If the log2FC cell is empty/'ND' but the 'FC vs HC' cell of the same
    block holds a positive number, log2(FC) is used instead.
    """
    cols, metric_row = find_value_columns(ws, block_headers)
    fc_cols = {b: find_fc_column(ws, cols[b], metric_row) for b in block_headers}
    group_lookup = {norm_text(g): g for g in GROUPS + [REFERENCE_GROUP]}
    data = {b: {} for b in block_headers}
    markers = []
    current = None
    n_from_fc = 0
    for r in range(metric_row + 1, ws.max_row + 1):
        label = ws.cell(r, 1).value
        if label is None or str(label).strip() == "":
            continue
        label = str(label).strip()
        group = group_lookup.get(norm_text(label))
        if group is None:
            current = label
            markers.append(current)
            for b in block_headers:
                data[b][current] = {}
            continue
        if current is None or group == REFERENCE_GROUP:
            continue
        for b in block_headers:
            value = to_float(ws.cell(r, cols[b]).value)
            if np.isnan(value) and fc_cols[b] is not None:
                fc = to_float(ws.cell(r, fc_cols[b]).value)
                if fc > 0:
                    value = float(np.log2(fc))
                    n_from_fc += 1
            data[b][current][group] = value

    # Report how many values are missing, so differences between files are visible
    n_nd = sum(np.isnan(v) for b in block_headers for m in markers
               for v in data[b][m].values())
    print(f"[{ws.title}] {len(markers)} markers read; {n_nd} cells without log2FC (shown as "
          f"{MISSING_LABEL}); {n_from_fc} taken from 'FC vs HC'.")
    return data, markers


def build_matrix(data, markers, blocks):
    """Stack blocks vertically into a (rows x markers) matrix."""
    rows, row_blocks, matrix = [], [], []
    for header, _label, _color in blocks:
        for g in GROUPS:
            values = [data[header][m].get(g, np.nan) for m in markers]
            if np.all(np.isnan(values)):
                continue  # group not measured at this time point
            rows.append(g)
            row_blocks.append(header)
            matrix.append(values)
    return np.array(matrix, dtype=float), rows, row_blocks


# --------------------------------------------------------------------------
# Plotting
# --------------------------------------------------------------------------
def plot_heatmap(matrix, rows, row_blocks, markers, cfg, out_base):
    # Keep markers with at least one highlighted value
    keep = np.nanmax(np.abs(np.nan_to_num(matrix, nan=0.0)), axis=0) >= THRESHOLD
    matrix = matrix[:, keep]
    markers = [m for m, k in zip(markers, keep) if k]
    # Alphabetical starting order (sets leaf order inside the dendrogram)
    alpha = sorted(range(len(markers)), key=lambda k: markers[k])
    matrix = matrix[:, alpha]
    markers = [markers[k] for k in alpha]
    n_rows, n_cols = matrix.shape
    if n_cols == 0:
        print(f"[{cfg['sheet']}] no marker reaches |log2FC| >= {THRESHOLD}; skipped.")
        return

    # Column clustering (rows with complete data only)
    complete = matrix[~np.isnan(matrix).any(axis=1)]
    if complete.shape[0] == 0:
        complete = np.nan_to_num(matrix, nan=0.0)
    Z = None
    if n_cols > 1:
        Z = linkage(complete.T, method="complete", metric="euclidean")
        order = dendrogram(Z, no_plot=True)["leaves"]
    else:
        order = [0]
    matrix = matrix[:, order]
    markers = [markers[i] for i in order]
    labels = [cfg["rename"].get(m, m) for m in markers]

    # Colour scale symmetric around 0
    vmax = np.nanmax(np.abs(matrix))
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)

    # Figure geometry
    heat_h = n_rows * CELL_H
    heat_x0 = LEFT_PAD + STRIP_W + ROW_LABEL_W
    fig_w = heat_x0 + HEATMAP_W + CBAR_GAP + CBAR_W + RIGHT_PAD
    fig_h = BOTTOM_PAD + heat_h + 0.15 + DENDRO_H + TOP_PAD
    fig = plt.figure(figsize=(fig_w, fig_h))

    def axes(x, y, w, h):
        return fig.add_axes([x / fig_w, y / fig_h, w / fig_w, h / fig_h])

    ax = axes(heat_x0, BOTTOM_PAD, HEATMAP_W, heat_h)
    ax_strip = axes(LEFT_PAD, BOTTOM_PAD, STRIP_W, heat_h)
    ax_dendro = axes(heat_x0, BOTTOM_PAD + heat_h + 0.15, HEATMAP_W, DENDRO_H)
    ax_cbar = axes(heat_x0 + HEATMAP_W + CBAR_GAP, BOTTOM_PAD + heat_h * 0.18,
                   CBAR_W, heat_h * 0.60)

    # --- heatmap cells
    font_size = 10 if n_cols <= 5 else 9.5
    for i in range(n_rows):
        for j in range(n_cols):
            v = matrix[i, j]
            x, y = j, i
            if np.isnan(v):
                face, text, color, weight = NA_FACE, MISSING_LABEL, NA_TEXT, "normal"
            elif abs(v) >= THRESHOLD:
                face = CMAP(norm(v))
                text = f"{v:.2f}"
                strong = abs(v) / vmax > 0.6
                color = "white" if strong else (UP_TEXT if v > 0 else DOWN_TEXT)
                weight = "bold"
            else:
                face, text, color, weight = NEUTRAL_FACE, f"{v:.2f}", NEUTRAL_TEXT, "normal"
            ax.add_patch(Rectangle((x, y), 1, 1, facecolor=face,
                                   edgecolor="white", linewidth=1.0))
            if not np.isnan(v) and abs(v) >= THRESHOLD:
                ax.add_patch(Rectangle((x + 0.03, y + 0.06), 0.94, 0.88, fill=False,
                                       edgecolor=UP_EDGE if v > 0 else DOWN_EDGE,
                                       linewidth=1.3))
            ax.text(x + 0.5, y + 0.5, text, ha="center", va="center",
                    fontsize=font_size, color=color, fontweight=weight)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(n_rows, 0)
    ax.set_xticks(np.arange(n_cols) + 0.5)
    ax.set_xticklabels(labels, rotation=45, ha="right", rotation_mode="anchor", fontsize=10)
    ax.set_yticks(np.arange(n_rows) + 0.5)
    ax.set_yticklabels(rows, fontsize=10)
    ax.tick_params(length=0, pad=6)
    for spine in ax.spines.values():
        spine.set_color("#222222")
        spine.set_linewidth(0.8)

    # --- block separators and the left colour strip
    ax_strip.set_xlim(0, 1)
    ax_strip.set_ylim(n_rows, 0)
    ax_strip.axis("off")
    start = 0
    block_info = {h: (lab, col) for h, lab, col in cfg["blocks"]}
    for k in range(1, n_rows + 1):
        if k == n_rows or row_blocks[k] != row_blocks[start]:
            label, color = block_info[row_blocks[start]]
            ax_strip.add_patch(Rectangle((0, start), 1, k - start,
                                         facecolor=color, edgecolor="none"))
            ax_strip.text(0.5, (start + k) / 2, label, rotation=90,
                          ha="center", va="center", fontsize=10)
            if k < n_rows:
                ax.axhline(k, color=LINE_COLOR, linewidth=1.5)
            start = k

    # --- dendrogram
    if Z is not None:
        dendrogram(Z, ax=ax_dendro, no_labels=True, color_threshold=0,
                   above_threshold_color=LINE_COLOR,
                   link_color_func=lambda _k: LINE_COLOR)
        for coll in ax_dendro.collections:
            coll.set_linewidth(1.5)
        ax_dendro.set_xlim(0, 10 * n_cols)
        top = Z[:, 2].max()
        ax_dendro.set_ylim(0, top * 1.05)
        ax_dendro.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5, integer=True))
        ax_dendro.set_ylabel("Euclidean\ndistance", fontsize=7.5)
        ax_dendro.tick_params(axis="y", labelsize=7.5, length=3)
        ax_dendro.set_xticks([])
        for side in ("top", "right", "bottom", "left"):
            ax_dendro.spines[side].set_visible(False)
    else:
        ax_dendro.axis("off")

    # --- colour bar
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
    cb = fig.colorbar(sm, cax=ax_cbar)
    cb.set_ticks(np.arange(-np.floor(vmax), np.floor(vmax) + 1, 1))
    cb.set_label("log2 fold change vs HC (highlighted cells)", fontsize=9.5)
    cb.ax.tick_params(labelsize=9)

    # --- legend
    handles = [
        Patch(facecolor=UP_EDGE, edgecolor=UP_EDGE,
              label=f"log2FC ≥ {THRESHOLD:g}: bold + red border"),
        Patch(facecolor=DOWN_EDGE, edgecolor=DOWN_EDGE,
              label=f"log2FC ≤ −{THRESHOLD:g}: bold + blue border"),
        Patch(facecolor=NEUTRAL_FACE, edgecolor="#bbbbbb",
              label=f"|log2FC| < {THRESHOLD:g}: regular text"),
        Patch(facecolor=NA_FACE, edgecolor=NA_FACE, label=f"{MISSING_LABEL}: not determined"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
               fontsize=8.5, handlelength=2.5, columnspacing=2.0,
               bbox_to_anchor=((heat_x0 + HEATMAP_W / 2) / fig_w, 0.05 / fig_h))

    for ext in ("png", "pdf"):
        path = out_base.with_suffix(f".{ext}")
        fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"Saved: {path}")
    plt.close(fig)


# --------------------------------------------------------------------------
def main():
    excel_path = select_excel_file()
    out_dir = excel_path.parent / "figures"
    out_dir.mkdir(exist_ok=True)

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    for cfg in FIGURES:
        sheet = next((n for n in wb.sheetnames
                      if norm_text(n) == norm_text(cfg["sheet"])), None)
        if sheet is None:
            print(f"Sheet '{cfg['sheet']}' not found (available: {wb.sheetnames}); skipped.")
            continue
        headers = [b[0] for b in cfg["blocks"]]
        data, markers = read_sheet(wb[sheet], headers)
        matrix, rows, row_blocks = build_matrix(data, markers, cfg["blocks"])
        plot_heatmap(matrix, rows, row_blocks, markers, cfg, out_dir / cfg["output"])

    print(f"\nDone. Figures saved in: {out_dir}")


if __name__ == "__main__":
    main()
