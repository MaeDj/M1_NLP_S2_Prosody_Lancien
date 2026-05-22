#!/home/mae/Documents/idmc/master1/university/s2/prosody/ruvoletto/projet/venv_prosody_project/bin/python

import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path("/home/mae/Documents/idmc/master1/university/s2/prosody/lancien/github_project/M1_NLP_S2_Prosody_Lancien")
CSV_PATH    = PROJECT_ROOT / "data/result/The-Very-Hungry-Caterpillar.csv"
OUTPUT_DIR  = PROJECT_ROOT / "harmonies_metrics_results"
OUTPUT_CSV  = OUTPUT_DIR / "results_global_level_metrics.csv"


def main():
    print(f"Loading {CSV_PATH.name}...")
    df = pd.read_csv(CSV_PATH)
    print(f"  {len(df)} frames total")

    row = {"source_file": CSV_PATH.name}

    for col, label in [
        ("mean_F0(Hz)", "F0"),
        ("mean_F1(Hz)", "F1"),
        ("mean_F2(Hz)", "F2"),
        ("mean_F3(Hz)", "F3"),
    ]:
        vals = pd.to_numeric(df[col], errors="coerce").dropna()
        if label == "F0":
            vals = vals[vals > 50]   # exclude unvoiced frames

        row[f"{label}_mean"]   = vals.mean()
        row[f"{label}_sd"]     = vals.std()
        row[f"{label}_median"] = vals.median()
        print(f"  {label}: {len(vals)} valid frames  "
              f"mean={row[f'{label}_mean']:.2f}  "
              f"sd={row[f'{label}_sd']:.2f}  "
              f"median={row[f'{label}_median']:.2f}")

    output_df = pd.DataFrame([row])[[
        "source_file",
        "F0_mean", "F0_sd", "F0_median",
        "F1_mean", "F1_sd", "F1_median",
        "F2_mean", "F2_sd", "F2_median",
        "F3_mean", "F3_sd", "F3_median",
    ]]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_CSV, index=False, float_format="%.4f")
    print(f"\nSaved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()