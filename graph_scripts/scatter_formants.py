"""
2D scatter plots of formant pairs from frame-level data:
  - F1 vs F2
  - F1 vs F3
  - F2 vs F3
Input : data/result/The-Very-Hungry-Caterpillar.csv
Output: graph/scatter_F1_F2.png, scatter_F1_F3.png, scatter_F2_F3.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "result" / "The-Very-Hungry-Caterpillar.csv"
OUT_DIR = ROOT / "graph"
OUT_DIR.mkdir(exist_ok=True)

RAW_COLS = {
    "F1": "mean_F1(Hz)",
    "F2": "mean_F2(Hz)",
    "F3": "mean_F3(Hz)",
}

COLORS = {
    ("F1", "F2"): "#DD8452",
    ("F1", "F3"): "#C44E52",
    ("F2", "F3"): "#55A868",
}


def load_formants(path: Path) -> dict[str, pd.Series]:
    df = pd.read_csv(path)
    return {
        label: pd.to_numeric(df[col], errors="coerce")
        for label, col in RAW_COLS.items()
    }


def make_scatter(x: pd.Series, y: pd.Series, x_label: str, y_label: str,
                 color: str, filepath: Path):
    mask = x.notna() & y.notna()
    xv, yv = x[mask], y[mask]

    slope, intercept, r_value, p_value, _ = stats.linregress(xv, yv)
    x_line = np.linspace(xv.min(), xv.max(), 300)
    y_line = slope * x_line + intercept

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(xv, yv, s=4, alpha=0.15, color=color, linewidths=0)
    ax.plot(x_line, y_line, color="black", linewidth=1.5,
            label=f"y = {slope:.2f}x + {intercept:.0f}  (R²={r_value**2:.3f}, p={p_value:.2e})")
    ax.legend(fontsize=9, loc="upper left")

    ax.set_xlabel(f"{x_label} (Hz)", fontsize=12)
    ax.set_ylabel(f"{y_label} (Hz)", fontsize=12)
    ax.set_title(f"{x_label} vs {y_label} — global-level ({len(xv):,} frames)",
                 fontsize=13, fontweight="bold")
    ax.grid(linestyle="--", alpha=0.4)
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}  (R²={r_value**2:.3f}, p={p_value:.2e})")


def main():
    formants = load_formants(DATA_RAW)

    pairs = [("F1", "F2"), ("F1", "F3"), ("F2", "F3")]
    for x_label, y_label in pairs:
        make_scatter(
            x=formants[x_label],
            y=formants[y_label],
            x_label=x_label,
            y_label=y_label,
            color=COLORS[(x_label, y_label)],
            filepath=OUT_DIR / f"scatter_{x_label}_{y_label}.png",
        )


if __name__ == "__main__":
    main()