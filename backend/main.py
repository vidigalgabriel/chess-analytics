from fastapi import FastAPI, Query
from chess_analysis.analytics_fast import (
    load_data,
    aggregate_white_first_move,
    aggregate_black_response,
    filter_data
)

app = FastAPI()

df = load_data()

@app.get("/white-moves")
def get_white_moves(
    start_year: int = Query(None),
    end_year: int = Query(None)
):
    filtered = filter_data(df, start_year, end_year)
    result = aggregate_white_first_move(filtered)
    return result.to_dict(orient="records")

@app.get("/black-responses")
def get_black_responses(
    start_year: int = Query(None),
    end_year: int = Query(None)
):
    filtered = filter_data(df, start_year, end_year)
    result = aggregate_black_response(filtered)
    return result.to_dict(orient="records")