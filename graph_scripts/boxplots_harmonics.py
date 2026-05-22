"""
Boxplot generation for harmonic features:
  - The-Very-Hungry-Caterpillar.csv : 1 boxplot per harmonic (F0, F1, F2, F3)
  - results_features_metrics_sentence.csv : 1 boxplot for mean, 1 for sd, 1 for median
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "result" / "The-Very-Hungry-Caterpillar.csv"
DATA_SENT = ROOT / "harmonies_metrics_results" / "results_features_metrics_sentence.csv"
OUT_DIR = ROOT / "graph"
OUT_DIR.mkdir(exist_ok=True)

HARMONICS = ["F0", "F1", "F2", "F3"]
RAW_COLS = {
    "F0": "mean_F0(Hz)",
    "F1": "mean_F1(Hz)",
    "F2": "mean_F2(Hz)",
    "F3": "mean_F3(Hz)",
}
STAT_SUFFIXES = ["mean", "sd", "median"]
STAT_LABELS = {"mean": "Mean", "sd": "Std Dev", "median": "Median"}

COLORS = {
    "F0": "#4C72B0",
    "F1": "#DD8452",
    "F2": "#55A868",
    "F3": "#C44E52",
}


def load_raw(path: Path) -> dict[str, pd.Series]:
    df = pd.read_csv(path)
    result = {}
    for harm, col in RAW_COLS.items():
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        result[harm] = series
    return result


def load_sentence(path: Path) -> dict[str, dict[str, pd.Series]]:
    df = pd.read_csv(path)
    result = {stat: {} for stat in STAT_SUFFIXES}
    for harm in HARMONICS:
        for stat in STAT_SUFFIXES:
            col = f"{harm}_{stat}"
            if col in df.columns:
                result[stat][harm] = pd.to_numeric(df[col], errors="coerce").dropna()
    return result


def make_boxplot_single(series: pd.Series, title: str, ylabel: str, filepath: Path):
    fig, ax = plt.subplots(figsize=(5, 6))
    harm = title.split()[0]
    bp = ax.boxplot(
        series,
        patch_artist=True,
        widths=0.5,
        medianprops=dict(color="black", linewidth=2),
    )
    bp["boxes"][0].set_facecolor(COLORS.get(harm, "#7F7F7F"))
    bp["boxes"][0].set_alpha(0.7)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xticks([])
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}")


def make_boxplot_multi(data: dict[str, pd.Series], title: str, ylabel: str, filepath: Path):
    labels = [h for h in HARMONICS if h in data]
    values = [data[h].values for h in labels]

    fig, ax = plt.subplots(figsize=(7, 6))
    bp = ax.boxplot(
        values,
        tick_labels=labels,
        patch_artist=True,
        widths=0.5,
        medianprops=dict(color="black", linewidth=2),
    )
    for patch, label in zip(bp["boxes"], labels):
        patch.set_facecolor(COLORS.get(label, "#7F7F7F"))
        patch.set_alpha(0.7)

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel("Harmonic", fontsize=11)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}")


def main():
    # --- The-Very-Hungry-Caterpillar: one boxplot per harmonic ---
    raw_data = load_raw(DATA_RAW)
    for harm in HARMONICS:
        series = raw_data[harm]
        print(f"{harm}: {len(series)} valid frames, median={series.median():.1f} Hz")
        make_boxplot_single(
            series,
            title=f"{harm} — frame-level distribution",
            ylabel="Frequency (Hz)",
            filepath=OUT_DIR / f"boxplot_raw_{harm}.png",
        )

    # --- results_features_metrics_sentence: one boxplot per stat ---
    sent_data = load_sentence(DATA_SENT)
    for stat in STAT_SUFFIXES:
        for harm, s in sent_data[stat].items():
            print(f"{harm}_{stat}: {len(s)} sentences, median={s.median():.1f} Hz")
        make_boxplot_multi(
            sent_data[stat],
            title=f"Sentence-level {STAT_LABELS[stat]} per harmonic",
            ylabel="Frequency (Hz)",
            filepath=OUT_DIR / f"boxplot_sentence_{stat}.png",
        )


if __name__ == "__main__":
    main()