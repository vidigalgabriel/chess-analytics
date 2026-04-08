import chess.pgn
import pandas as pd
import os

def normalize_white_move(move):
    if move in ["e4", "d4", "c4", "Nf3"]:
        return move
    return "other"

def normalize_black_response_e4(move):
    if move in ["e5", "c5", "d5", "e6", "c6"]:
        return move
    return "other"

def normalize_black_response_d4(moves):
    if moves[:2] == ["d5", "e6"]:
        return "d5_e6"
    if moves[:2] == ["d5", "c6"]:
        return "d5_c6"
    if moves[:2] == ["Nf6", "e6"]:
        return "Nf6_e6"
    if moves[:2] == ["Nf6", "g6"]:
        return "Nf6_g6"
    return "other"

def normalize_black_response_generic(move):
    if move in ["e5", "c5", "d5", "e6", "c6", "Nf6", "g6"]:
        return move
    return "other"

def extract_game_data(game, min_year=None, max_year=None):
    headers = game.headers

    if "Date" not in headers or "Result" not in headers:
        return None

    try:
        year = int(headers["Date"].split(".")[0])
    except:
        return None

    if min_year and year < min_year:
        return None
    if max_year and year > max_year:
        return None

    result = headers["Result"]

    node = game
    moves = []

    while node.variations:
        node = node.variations[0]
        moves.append(node.move)

    if len(moves) < 12:
        return None

    board = game.board()
    san_moves = []

    for move in moves[:12]:
        san_moves.append(board.san(move))
        board.push(move)

    opening = classify_opening(san_moves)

    return {
        "year": year,
        "result": result,
        "opening": opening
    }

def classify_opening(m):
    try:
        if m[0] == "e4" and m[1] == "e5":
            if m[2] == "Nf3" and m[3] == "Nc6":
                if m[4] == "Bb5":
                    return "Ruy Lopez"
                if m[4] == "Bc4":
                    return "Italian Game"
                if m[4] == "d4":
                    return "Scotch Game"
                return "Open Game Other"
            return "e4 e5 Other"

        if m[0] == "e4" and m[1] == "c5":
            if m[2] == "Nf3":
                if m[3] == "d6":
                    if "a6" in m:
                        return "Najdorf"
                    return "Sicilian d6"
                if m[3] == "Nc6":
                    return "Sicilian Classical"
                if m[3] == "e6":
                    return "Sicilian Taimanov/Kan"
                if m[3] == "g6":
                    return "Sicilian Dragon"
                return "Sicilian Other"
            return "Sicilian Other"

        if m[0] == "e4" and m[1] == "e6":
            if m[2] == "d4" and m[3] == "d5":
                if m[4] == "Nc3":
                    return "French Classical"
                if m[4] == "Nd2":
                    return "French Tarrasch"
                if m[4] == "e5":
                    return "French Advance"
                if m[4] == "exd5":
                    return "French Exchange"
            return "French Other"

        if m[0] == "e4" and m[1] == "c6":
            if m[2] == "d4" and m[3] == "d5":
                if m[4] == "Nc3":
                    return "Caro-Kann Classical"
                if m[4] == "e5":
                    return "Caro Advance"
                if m[4] == "exd5":
                    return "Caro Exchange"
            return "Caro-Kann Other"

        if m[0] == "d4" and m[1] == "d5":
            if m[2] == "c4":
                if m[3] == "dxc4":
                    return "QGA"
                if m[3] == "e6":
                    return "QGD"
                if m[3] == "c6":
                    return "Slav"
            return "d4 d5 Other"

        if m[0] == "d4" and m[1] == "Nf6":
            if m[2] == "c4":
                if m[3] == "g6":
                    if "Bg7" in m:
                        if "d5" in m:
                            return "Grunfeld"
                        return "King's Indian"
                if m[3] == "e6":
                    if "Bb4" in m:
                        return "Nimzo-Indian"
                    return "Queen's Indian"
            return "Indian Other"

    except:
        return "Unknown"

    return "Other"
def process_pgn_stream(pgn_path, output_csv, max_games=None, min_year=None, max_year=None):
    data = []
    count = 0

    with open(pgn_path, encoding="utf-8") as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            extracted = extract_game_data(game, min_year, max_year)

            if extracted:
                data.append(extracted)
                count += 1

                if count % 2000 == 0:
                    print(count)

                if max_games and count >= max_games:
                    break

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print("finalizado:", game_count)