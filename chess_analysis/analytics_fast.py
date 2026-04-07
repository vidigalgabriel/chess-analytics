import pandas as pd

def load_data(path="data/processed_games.csv"):
    df = pd.read_csv(path)

    df["white_win"] = (df["result"] == "1-0").astype(int)
    df["black_win"] = (df["result"] == "0-1").astype(int)
    df["draw"] = (df["result"] == "1/2-1/2").astype(int)

    df["score"] = df["white_win"] + 0.5 * df["draw"]

    df["decade"] = (df["year"] // 10) * 10

    return df

def aggregate_white_first_move(df):
    grouped = df.groupby(["decade", "white_move"])

    result = grouped.agg(
        games=("result", "count"),
        white_wins=("white_win", "sum"),
        black_wins=("black_win", "sum"),
        draws=("draw", "sum"),
        avg_score=("score", "mean")
    ).reset_index()

    result["frequency"] = result["games"] / result.groupby("decade")["games"].transform("sum")
    result["white_winrate"] = result["white_wins"] / result["games"]
    result["black_winrate"] = result["black_wins"] / result["games"]
    result["drawrate"] = result["draws"] / result["games"]

    return result

def aggregate_black_response(df):
    grouped = df.groupby(["decade", "white_move", "black_response"])

    result = grouped.agg(
        games=("result", "count"),
        white_wins=("white_win", "sum"),
        black_wins=("black_win", "sum"),
        draws=("draw", "sum"),
        avg_score=("score", "mean")
    ).reset_index()

    result["frequency"] = result["games"] / result.groupby(
        ["decade", "white_move"]
    )["games"].transform("sum")

    result["white_winrate"] = result["white_wins"] / result["games"]
    result["black_winrate"] = result["black_wins"] / result["games"]
    result["drawrate"] = result["draws"] / result["games"]

    return result



def filter_data(df, start_year=None, end_year=None):
    if start_year:
        df = df[df["year"] >= start_year]
    if end_year:
        df = df[df["year"] <= end_year]
    return df
   