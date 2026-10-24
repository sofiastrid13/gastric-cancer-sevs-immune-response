"""Plot individual sEV protein concentrations and group medians.

Install dependencies: python -m pip install pandas openpyxl numpy matplotlib
Run without arguments to open the file and output-folder selection windows:
    python plot_sevs_protein.py
Optional command line: python plot_sevs_protein.py input.xlsx --output-dir figures

Input: Estadio and Highest_concentration (ug/mL), as in TABLA_TOTAL.
Values are plotted in their original ug/mL units (no conversion).
Peptic ulcer is excluded to match the reference figure.
"""

import argparse
from pathlib import Path
import re
import unicodedata

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

GROUPS = ["HC", "CG", "CGm", "GC I", "GC II", "GC III", "GC IV"]
COLORS = ["#858d92", "#509ebe", "#a06cb0", "#4caa85", "#d3a124", "#e58939", "#e66d79"]
DPI = 600


def normalize(value):
    text = unicodedata.normalize("NFKD", str(value).replace("µ", "u").replace("μ", "u"))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", text.lower())


ALIASES = {
    "HC": ["Healthy", "HC", "Healthy control", "Sano"],
    "CG": ["Gastritis_cronica", "Chronic gastritis", "CG"],
    "CGm": ["Gastritis_cronica_(metaplasia)", "Chronic gastritis (metaplasia)", "CGm"],
    "GC I": ["Estadio_I", "Stage I", "GC I"],
    "GC II": ["Estadio_II", "Stage II", "GC II"],
    "GC III": ["Estadio_III", "Stage III", "GC III"],
    "GC IV": ["Estadio_IV", "Stage IV", "GC IV"],
}
GROUP_MAP = {normalize(alias): group for group, aliases in ALIASES.items() for alias in aliases}


def choose_option(root, title, options):
    """Display an explicit choice instead of guessing an unknown column."""
    import tkinter as tk
    from tkinter import ttk
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry("680x180")
    window.attributes("-topmost", True)
    ttk.Label(window, text=title, wraplength=640).pack(padx=16, pady=14)
    choice = tk.StringVar(value=options[0])
    ttk.Combobox(window, values=options, textvariable=choice, state="readonly", width=85).pack(padx=16)
    selected = []
    def accept():
        selected.append(choice.get())
        window.destroy()
    ttk.Button(window, text="Continue", command=accept).pack(pady=18)
    window.grab_set()
    root.wait_window(window)
    if not selected:
        raise ValueError("Selection cancelled.")
    return selected[0]


def read_data(path, root=None):
    """Detect headers in the first 20 rows, with a manual GUI fallback."""
    group_names = {"estadio", "clinicalgroup", "stage", "clinicalstage", "group", "grupoclinico", "diseasestatus"}
    value_names = {"highestconcentrationugml", "highestconcentration", "sevsproteinconcentrationugml",
                   "proteinconcentrationugml", "concentracionugml", "concentrationugml"}
    candidates = []
    with pd.ExcelFile(path, engine="openpyxl") as workbook:
        for sheet in workbook.sheet_names:
            preview = pd.read_excel(workbook, sheet_name=sheet, header=None, nrows=20)
            for header_row, row in preview.iterrows():
                columns = {normalize(value): value for value in row.dropna()}
                groups = [columns[k] for k in columns if k in group_names]
                values = [columns[k] for k in columns if k in value_names]
                if len(groups) == 1 and len(values) == 1:
                    candidates.append((sheet, int(header_row), groups[0], values[0]))
        if len(candidates) == 1:
            sheet, header_row, group_col, value_col = candidates[0]
            frame = pd.read_excel(workbook, sheet_name=sheet, header=header_row)
        else:
            if root is None:
                raise ValueError("Column detection is ambiguous or incomplete. Run without arguments to choose the worksheet and columns in the selection windows.")
            from tkinter import simpledialog
            sheet = choose_option(root, "Select the worksheet with individual patient data", workbook.sheet_names)
            row_number = simpledialog.askinteger("Header row", "Excel row number containing the column names:", initialvalue=1, minvalue=1, parent=root)
            if row_number is None:
                raise ValueError("Selection cancelled.")
            header_row = row_number - 1
            frame = pd.read_excel(workbook, sheet_name=sheet, header=header_row)
            labels = [f"{i + 1}: {column}" for i, column in enumerate(frame.columns)]
            if len(labels) < 2:
                raise ValueError("The selected header row has fewer than two columns.")
            group_label = choose_option(root, "Select the clinical group / stage column", labels)
            value_label = choose_option(root, "Select sEV protein concentration in ug/mL (not sHLA-G or particles/mL)", labels)
            group_col = frame.columns[labels.index(group_label)]
            value_col = frame.columns[labels.index(value_label)]
            if group_col == value_col:
                raise ValueError("Select two different columns for clinical group and protein concentration.")
    result = pd.DataFrame({"Group": frame[group_col].map(lambda v: GROUP_MAP.get(normalize(v))),
                           "Concentration": pd.to_numeric(frame[value_col].astype(str).str.replace(",", ".", regex=False), errors="coerce")})
    excluded = frame.loc[result["Group"].isna(), group_col].value_counts(dropna=False)
    if not excluded.empty:
        print("Groups excluded from the reference figure:")
        print(excluded.to_string())
    included = result["Group"].notna()
    invalid = included & (~np.isfinite(result["Concentration"]) | (result["Concentration"] < 0))
    if invalid.any():
        raise ValueError(f"Invalid or missing concentrations in Excel rows: {(np.flatnonzero(invalid) + header_row + 2).tolist()}. Correct these entries before plotting.")
    result = result.loc[included].copy()
    missing = set(GROUPS) - set(result["Group"])
    if missing:
        raise ValueError("Missing reference groups: " + ", ".join(sorted(missing)))
    print(f"Worksheet: {sheet}")
    print(result.groupby("Group")["Concentration"].agg(["count", "median"]).reindex(GROUPS).to_string())
    return result


def create_figure(data, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    available_fonts = {f.name for f in font_manager.fontManager.ttflist}
    font = "Times New Roman" if "Times New Roman" in available_fonts else "STIXGeneral"
    plt.rcParams.update({"font.family": font, "font.size": 17, "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, ax = plt.subplots(figsize=(7.73, 4.25))
    fig.subplots_adjust(left=0.155, right=0.982, top=0.935, bottom=0.30)
    ax.set_facecolor("#f2f2f2")
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color="#dcdcdc", linewidth=1)
    rng = np.random.default_rng(2026)
    for position, (group, color) in enumerate(zip(GROUPS, COLORS)):
        values = data.loc[data["Group"] == group, "Concentration"].to_numpy(dtype=float)
        jitter = rng.uniform(-0.14, 0.14, len(values))
        ax.scatter(position + jitter, values, s=20, color=color, edgecolors="none", zorder=3)
        ax.hlines(np.median(values), position - 0.23, position + 0.23, color="#303a43", linewidth=1.8, zorder=4)
        ax.text(position, -0.18, f"n = {len(values)}", transform=ax.get_xaxis_transform(),
                ha="center", va="top", color="#555555", fontsize=17, clip_on=False)
    ax.set_xlim(-0.5, len(GROUPS) - 0.5)
    upper = max(50, 10 * np.ceil((data["Concentration"].max() + 2) / 10))
    ax.set_ylim(0, upper)
    ax.set_yticks(np.arange(0, upper + 1, 10))
    ax.set_xticks(range(len(GROUPS)), GROUPS)
    ax.tick_params(axis="both", length=0)
    ax.tick_params(axis="x", pad=10)
    ax.set_ylabel("sEVs protein\nconcentration (µg/mL)", fontsize=18)
    ax.set_xlabel("Clinical group", fontsize=18, labelpad=37)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#aab8c9")
    paths = []
    for extension in ["png", "pdf"]:
        target = output_dir / f"sEVs_protein_concentration.{extension}"
        fig.savefig(target, dpi=DPI, facecolor="white")
        if extension == "png" and target.stat().st_size == 0:
            # Fallback for environments with a nonfunctional PNG save hook.
            from PIL import Image
            fig.set_dpi(DPI)
            fig.canvas.draw()
            Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).save(target, dpi=(DPI, DPI))
        paths.append(target)
    plt.close(fig)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", nargs="?", help="Optional Excel file. If omitted, a file picker opens.")
    parser.add_argument("--output-dir", help="Optional folder for PNG and PDF outputs.")
    args = parser.parse_args()
    root = None
    try:
        if not args.input:
            import tkinter as tk
            from tkinter import filedialog, messagebox
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            args.input = filedialog.askopenfilename(parent=root, title="Select the Excel data file", filetypes=[("Excel workbooks", "*.xlsx *.xlsm")])
            if not args.input:
                print("Selection cancelled.")
                return
            if not args.output_dir:
                args.output_dir = filedialog.askdirectory(parent=root, title="Select the folder for PNG and PDF", initialdir=str(Path(args.input).parent))
                if not args.output_dir:
                    print("Selection cancelled.")
                    return
        data = read_data(Path(args.input), root=root)
        outputs = create_figure(data, args.output_dir or Path(args.input).parent / "figures")
        message = "Saved successfully:\n" + "\n".join(str(p.resolve()) for p in outputs)
        print(message)
        if root is not None:
            messagebox.showinfo("Figure exported", message, parent=root)
    except Exception as error:
        print(f"Error: {error}")
        if root is not None:
            messagebox.showerror("Unable to create the figure", str(error), parent=root)
        raise
    finally:
        if root is not None:
            root.destroy()


if __name__ == "__main__":
    main()
