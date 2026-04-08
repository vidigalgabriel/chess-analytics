from fastapi import FastAPI
from chess_analysis.analytics_fast import (
    load_data,
    aggregate_white_first_move,
    aggregate_black_response,
    filter_data
)

app = FastAPI()

df = load_data("data/processed_games.csv")


@app.get("/white_moves")
def get_white_moves(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_white_first_move(data)
    return result.to_dict(orient="records")


@app.get("/black_responses")
def get_black_responses(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_black_response(data)
    return result.to_dict(orient="records")

@app.get("/black_responses/e4")
def get_black_e4(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_black_response_by_white(data, "e4")
    return result.to_dict(orient="records")


@app.get("/black_responses/d4")
def get_black_d4(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_black_response_by_white(data, "d4")
    return result.to_dict(orient="records")


@app.get("/black_responses/c4")
def get_black_c4(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_black_response_by_white(data, "c4")
    return result.to_dict(orient="records")


@app.get("/black_responses/nf3")
def get_black_nf3(start_year: int = None, end_year: int = None):
    data = filter_data(df, start_year, end_year)
    result = aggregate_black_response_by_white(data, "Nf3")
    return result.to_dict(orient="records")

from chess_analysis.analytics_fast import aggregate_black_response_by_white