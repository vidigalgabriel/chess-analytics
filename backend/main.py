from fastapi import FastAPI
import pandas as pd

app = FastAPI()

df = pd.read_csv("chess_analysis/data/test_sample.csv")

def filter_data(df, start_year, end_year):
    if start_year:
        df = df[df["year"] >= start_year]
    if end_year:
        df = df[df["year"] <= end_year]
    return df

def aggregate_openings(df):
    df["decade"] = (df["year"] // 10) * 10

    grouped = (
        df.groupby(["decade", "opening"])
        .agg(
            games=("result", "count"),
            white_wins=("result", lambda x: (x == "1-0").sum()),
            black_wins=("result", lambda x: (x == "0-1").sum()),
            draws=("result", lambda x: (x == "1/2-1/2").sum()),
        )
        .reset_index()
    )

    grouped["white_winrate"] = grouped["white_wins"] / grouped["games"]
    grouped["black_winrate"] = grouped["black_wins"] / grouped["games"]
    grouped["drawrate"] = grouped["draws"] / grouped["games"]
    grouped["avg_score"] = (
        grouped["white_wins"] + 0.5 * grouped["draws"]
    ) / grouped["games"]

    grouped["frequency"] = grouped["games"] / grouped.groupby("decade")["games"].transform("sum")

    return grouped


@app.get("/openings")
def get_openings(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_openings(data)
    return result.to_dict(orient="records")