#!/home/mae/Documents/idmc/master1/university/s2/prosody/ruvoletto/projet/venv_prosody_project/bin/python

import os
import sys
import torch
import librosa
import numpy as np
import pandas as pd
from pathlib import Path

RESPIRO_PATH = "/home/mae/Documents/stage_L3_software/respiro_en/Respiro-en"
sys.path.insert(0, RESPIRO_PATH)

from modules import DetectionNet, BreathDetector

PROJECT_ROOT = Path("/home/mae/Documents/idmc/master1/university/s2/prosody/lancien/github_project/M1_NLP_S2_Prosody_Lancien")
WAV_PATH    = PROJECT_ROOT / "data/wav/The-Very-Hungry-Caterpillar.wav"
CSV_PATH    = PROJECT_ROOT / "data/result/The-Very-Hungry-Caterpillar.csv"
OUTPUT_DIR  = PROJECT_ROOT / "harmonies_metrics_results"
OUTPUT_CSV  = OUTPUT_DIR / "results_features_metrics_global.csv"

# Speech segments shorter than this (seconds) are discarded
MIN_SPEECH_DURATION = 0.5


def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DetectionNet().to(device)
    checkpoint = torch.load(os.path.join(RESPIRO_PATH, "respiro-en.pt"), map_location=device)
    model.load_state_dict(checkpoint["model"])
    model.eval()
    return model, device


def get_sentence_timestamps(wav_path, model, device):
    detector = BreathDetector(model, device=device)
    breath_tree = detector(str(wav_path))

    wav, sr = librosa.load(str(wav_path), sr=16000)
    duration = len(wav) / sr

    breath_intervals = sorted(breath_tree, key=lambda x: x.begin)

    segments = []
    cursor = 0.0
    for interval in breath_intervals:
        if interval.begin - cursor >= MIN_SPEECH_DURATION:
            segments.append((round(cursor, 3), round(interval.begin, 3)))
        cursor = interval.end

    if duration - cursor >= MIN_SPEECH_DURATION:
        segments.append((round(cursor, 3), round(duration, 3)))

    return segments


def aggregate_segment(df, seg_start, seg_end):
    mask = (df["start_time"] >= seg_start) & (df["end_time"] <= seg_end)
    sub = df[mask]
    if sub.empty:
        return None

    row = {"seg_start": seg_start, "seg_end": seg_end}

    for col, label in [
        ("mean_F0(Hz)", "F0"),
        ("mean_F1(Hz)", "F1"),
        ("mean_F2(Hz)", "F2"),
        ("mean_F3(Hz)", "F3"),
    ]:
        vals = pd.to_numeric(sub[col], errors="coerce").dropna()
        if label == "F0":
            vals = vals[vals > 50]   # exclude unvoiced frames

        row[f"{label}_mean"]   = vals.mean()   if len(vals) > 0 else np.nan
        row[f"{label}_sd"]     = vals.std()    if len(vals) > 0 else np.nan
        row[f"{label}_median"] = vals.median() if len(vals) > 0 else np.nan

    return row


def main():
    print("Loading Respiro-EN model...")
    model, device = load_model()

    print(f"Detecting breath segments in {WAV_PATH.name}...")
    sentences = get_sentence_timestamps(WAV_PATH, model, device)
    print(f"  → {len(sentences)} speech segments extracted")

    print("Loading acoustic feature CSV...")
    df = pd.read_csv(CSV_PATH)
    df["start_time"] = pd.to_numeric(df["start_time"], errors="coerce")
    df["end_time"]   = pd.to_numeric(df["end_time"],   errors="coerce")

    print("Computing per-sentence metrics (F0/F1/F2/F3 mean, sd, median)...")
    rows = []
    for i, (start, end) in enumerate(sentences, start=1):
        result = aggregate_segment(df, start, end)
        if result is not None:
            result["sentence_id"] = i
            rows.append(result)
            print(f"  Sentence {i:3d}  [{start:.3f}s – {end:.3f}s]  "
                  f"F0_mean={result['F0_mean']:.1f} Hz" if not np.isnan(result['F0_mean']) else
                  f"  Sentence {i:3d}  [{start:.3f}s – {end:.3f}s]  F0=undefined")

    output_df = pd.DataFrame(rows)[[
        "sentence_id", "seg_start", "seg_end",
        "F0_mean", "F0_sd", "F0_median",
        "F1_mean", "F1_sd", "F1_median",
        "F2_mean", "F2_sd", "F2_median",
        "F3_mean", "F3_sd", "F3_median",
    ]]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_CSV, index=False, float_format="%.4f")
    print(f"\nSaved {len(output_df)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()