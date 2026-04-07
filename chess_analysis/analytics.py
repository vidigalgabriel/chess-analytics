import pandas as pd
import numpy as np
from pathlib import Path


def _compute_result_metrics(group: pd.DataFrame) -> dict:
    total = len(group)
    white_wins = (group["result"] == "1-0").sum()
    black_wins = (group["result"] == "0-1").sum()
    draws = (group["result"] == "1/2-1/2").sum()

    scores = group["result"].map({"1-0": 1.0, "1/2-1/2": 0.5, "0-1": 0.0})

    return {
        "total_games": total,
        "white_win_rate": round(white_wins / total * 100, 2) if total else 0.0,
        "black_win_rate": round(black_wins / total * 100, 2) if total else 0.0,
        "draw_rate": round(draws / total * 100, 2) if total else 0.0,
        "avg_score": round(scores.mean(), 4) if total else 0.0,
    }


def compute_metrics(df: pd.DataFrame, group_by: str = "decade") -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    valid_groups = {"decade", "year"}
    if group_by not in valid_groups:
        raise ValueError(f"group_by must be one of {valid_groups}")

    all_totals = len(df)
    records = []

    grouped = df.groupby([group_by, "white_first_move", "black_response"])

    for (period, white_move, black_resp), group in grouped:
        metrics = _compute_result_metrics(group)
        metrics["frequency_pct"] = round(len(group) / all_totals * 100, 4)
        metrics[group_by] = period
        metrics["white_first_move"] = white_move
        metrics["black_response"] = black_resp
        records.append(metrics)

    if not records:
        return pd.DataFrame()

    cols = [group_by, "white_first_move", "black_response", "total_games",
            "frequency_pct", "white_win_rate", "black_win_rate", "draw_rate", "avg_score"]

    return pd.DataFrame(records)[cols].sort_values(
        [group_by, "total_games"], ascending=[True, False]
    ).reset_index(drop=True)


def export_csv(df: pd.DataFrame, output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return str(path)


def prepare_for_visualization(df: pd.DataFrame, group_by: str = "decade") -> dict:
    metrics = compute_metrics(df, group_by=group_by)
    if metrics.empty:
        return {"data": [], "columns": [], "group_by": group_by}

    return {
        "data": metrics.to_dict(orient="records"),
        "columns": list(metrics.columns),
        "group_by": group_by,
    }


def filter_data(df, start_year, end_year):
    return df[(df["year"] >= start_year) & (df["year"] <= end_year)]