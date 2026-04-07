import pandas as pd
import numpy as np


WHITE_MOVES = {"e4", "d4", "c4", "Nf3"}

BLACK_RESPONSES = {
    "e4": {"e5", "c5", "d5", "e6", "c6"},
    "d4": None,
    "c4": {"e5", "c5", "d5", "e6", "c6", "Nf6", "g6"},
    "Nf3": {"e5", "c5", "d5", "e6", "c6", "Nf6", "g6"},
}

D4_TWO_MOVE_RESPONSES = {
    frozenset({"d5", "e6"}): "d5+e6",
    frozenset({"d5", "c6"}): "d5+c6",
    frozenset({"Nf6", "e6"}): "Nf6+e6",
    frozenset({"Nf6", "g6"}): "Nf6+g6",
}


def _classify_white_move(san: str) -> str:
    if san in WHITE_MOVES:
        return san
    return "Other"


def _classify_black_response(white_move: str, black_san: str, game_moves: list) -> str:
    if white_move == "Other":
        return "Other"

    if white_move == "d4":
        if len(game_moves) >= 4:
            black_move1 = black_san
            black_move2 = game_moves[3] if len(game_moves) > 3 else None
            if black_move2:
                pair = frozenset({black_move1, black_move2})
                for key, label in D4_TWO_MOVE_RESPONSES.items():
                    if pair == key:
                        return label
        return "Other"

    allowed = BLACK_RESPONSES.get(white_move, set())
    if black_san in allowed:
        return black_san
    return "Other"


def process_games(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["year", "decade", "white_first_move", "black_response", "result"])

    result = df.copy()

    result["white_first_move"] = result["white_first_move_san"].apply(_classify_white_move)
    result["black_response"] = result.apply(
        lambda row: _classify_black_response(
            row["white_first_move"],
            row["black_first_response_san"],
            [],
        ),
        axis=1,
    )
    result["decade"] = (result["year"] // 10 * 10).astype(int)

    return result[["year", "decade", "white_first_move", "black_response", "result"]]


def filter_data(
    df: pd.DataFrame,
    start_year: int,
    end_year: int,
    white_move: str = None,
) -> pd.DataFrame:
    mask = (df["year"] >= start_year) & (df["year"] <= end_year)
    if white_move is not None:
        mask &= df["white_first_move"] == white_move
    return df[mask].reset_index(drop=True)
