#!/usr/bin/env python3
"""
generate_charts.py

Generate basic PNG charts from the MindsEye ledger exports.

Reads:
- exports/nodes_sample_export.csv
- exports/runs_sample_export.csv

Outputs:
- charts/runs_per_day.png
- charts/runs_by_prompt_type.png
- charts/runs_by_run_context.png

Requires:
- pandas
- matplotlib

Install via:

    pip install pandas matplotlib
"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS_DIR = os.path.join(ROOT, "exports")
CHARTS_DIR = os.path.join(ROOT, "charts")

NODES_CSV = os.path.join(EXPORTS_DIR, "nodes_sample_export.csv")
RUNS_CSV = os.path.join(EXPORTS_DIR, "runs_sample_export.csv")


def parse_date_safe(s: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def ensure_charts_dir():
    if not os.path.exists(CHARTS_DIR):
        os.makedirs(CHARTS_DIR, exist_ok=True)


def plot_runs_per_day(runs: pd.DataFrame):
    if "run_time" not in runs.columns:
        print("[charts] No run_time column; skipping runs_per_day chart.")
        return

    runs["run_time_parsed"] = runs["run_time"].apply(parse_date_safe)
    runs["run_date"] = runs["run_time_parsed"].dt.date
    runs_per_day = (
        runs.groupby("run_date")["run_id"]
        .count()
        .sort_index()
    )

    if runs_per_day.empty:
        print("[charts] No data for runs_per_day.")
        return

    plt.figure()
    runs_per_day.plot(kind="line")
    plt.xlabel("Date")
    plt.ylabel("Run count")
    plt.title("MindsEye Runs per Day")
    plt.tight_layout()

    path = os.path.join(CHARTS_DIR, "runs_per_day.png")
    plt.savefig(path)
    plt.close()
    print(f"[charts] Wrote {path}")


def plot_runs_by_prompt_type(nodes: pd.DataFrame, runs: pd.DataFrame):
    if "node_id" not in runs.columns:
        print("[charts] No node_id column; skipping runs_by_prompt_type chart.")
        return

    merged = runs.merge(
        nodes[["node_id", "prompt_type"]],
        on="node_id",
        how="left"
    )
    runs_by_prompt = (
        merged.groupby("prompt_type")["run_id"]
        .count()
        .sort_values(ascending=False)
    )

    if runs_by_prompt.empty:
        print("[charts] No data for runs_by_prompt_type.")
        return

    plt.figure()
    runs_by_prompt.plot(kind="bar")
    plt.xlabel("Prompt type")
    plt.ylabel("Run count")
    plt.title("Runs by Prompt Type")
    plt.tight_layout()

    path = os.path.join(CHARTS_DIR, "runs_by_prompt_type.png")
    plt.savefig(path)
    plt.close()
    print(f"[charts] Wrote {path}")


def plot_runs_by_run_context(runs: pd.DataFrame):
    if "run_context" not in runs.columns:
        print("[charts] No run_context column; skipping runs_by_run_context chart.")
        return

    usage = (
        runs.groupby("run_context")["run_id"]
        .count()
        .sort_values(ascending=False)
    )

    if usage.empty:
        print("[charts] No data for runs_by_run_context.")
        return

    plt.figure()
    usage.plot(kind="bar")
    plt.xlabel("Run context")
    plt.ylabel("Run count")
    plt.title("Runs by Surface (run_context)")
    plt.tight_layout()

    path = os.path.join(CHARTS_DIR, "runs_by_run_context.png")
    plt.savefig(path)
    plt.close()
    print(f"[charts] Wrote {path}")


def main():
    ensure_charts_dir()

    nodes = pd.read_csv(NODES_CSV)
    runs = pd.read_csv(RUNS_CSV)

    plot_runs_per_day(runs)
    plot_runs_by_prompt_type(nodes, runs)
    plot_runs_by_run_context(runs)


if __name__ == "__main__":
    main()
