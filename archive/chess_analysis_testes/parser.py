import chess.pgn
import pandas as pd
from pathlib import Path
from typing import Optional
import io


# Responsável por realizar a leitura e o parsing de arquivos PGN, filtrando 
# partidas válidas e extraindo metadados cruciais como o ano, o resultado e 
# os primeiros lances de cada jogador em notação SAN (Standard Algebraic Notation).

def _extract_game_data(game: chess.pgn.Game) -> Optional[dict]:
    headers = game.headers
    result = headers.get("Result", "*")
    if result not in ("1-0", "0-1", "1/2-1/2"):
        return None

    date = headers.get("Date", "")
    try:
        year = int(date.split(".")[0])
        if year < 1800 or year > 2100:
            return None
    except (ValueError, IndexError):
        return None

    moves = list(game.mainline_moves())
    if len(moves) < 2:
        return None

    board = chess.Board()
    board.push(moves[0])
    white_move = moves[0].uci()
    board.push(moves[1])
    black_move = moves[1].uci()

    white_san = chess.Board().san(moves[0])
    board2 = chess.Board()
    board2.push(moves[0])
    black_san = board2.san(moves[1])

    return {
        "year": year,
        "white_first_move_san": white_san,
        "black_first_response_san": black_san,
        "result": result,
    }


def load_games(path: str) -> pd.DataFrame:
    data_path = Path(path)
    records = []

    pgn_files = list(data_path.glob("*.pgn")) if data_path.is_dir() else [data_path]

    for pgn_file in pgn_files:
        with open(pgn_file, encoding="utf-8", errors="ignore") as f:
            while True:
                try:
                    game = chess.pgn.read_game(f)
                    if game is None:
                        break
                    record = _extract_game_data(game)
                    if record is not None:
                        records.append(record)
                except Exception:
                    continue

    return pd.DataFrame(records)
