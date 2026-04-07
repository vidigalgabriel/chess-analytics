from fastapi import FastAPI
from chess_analysis.parser import load_games
from chess_analysis.processing import process_games
from chess_analysis.analytics import compute_metrics, filter_data

app = FastAPI()

df_global = None

@app.on_event("startup")
def startup():
    global df_global
    df = load_games("chess_analysis/data")
    df = process_games(df)
    df_global = df

@app.get("/metrics")
def metrics(start_year: int = 1800, end_year: int = 2025):
    df = filter_data(df_global, start_year, end_year)
    result = compute_metrics(df)
    return result.to_dict(orient="records")