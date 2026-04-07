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

def extract_game_data(game):
    headers = game.headers

    if "Date" not in headers or "Result" not in headers:
        return None

    try:
        year = int(headers["Date"].split(".")[0])
    except:
        return None

    result = headers["Result"]

    node = game
    moves = []

    while node.variations:
        node = node.variations[0]
        moves.append(node.move)

    if len(moves) < 2:
        return None

    board = game.board()
    san_moves = []

    for move in moves[:4]:
        san_moves.append(board.san(move))
        board.push(move)

    white_move = normalize_white_move(san_moves[0])

    if white_move == "e4":
        black_response = normalize_black_response_e4(san_moves[1])
    elif white_move == "d4":
        black_response = normalize_black_response_d4(san_moves[1:3])
    elif white_move in ["c4", "Nf3"]:
        black_response = normalize_black_response_generic(san_moves[1])
    else:
        black_response = "other"

    return {
        "year": year,
        "result": result,
        "white_move": white_move,
        "black_response": black_response
    }

def process_pgn_stream(pgn_path, output_csv, max_games=None):
    if os.path.exists(output_csv):
        os.remove(output_csv)

    with open(pgn_path, encoding="utf-8", errors="ignore") as pgn_file:
        game_count = 0
        buffer = []

        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            data = extract_game_data(game)
            if data:
                buffer.append(data)

            game_count += 1

            if game_count % 10000 == 0:
                pd.DataFrame(buffer).to_csv(
                    output_csv,
                    mode="a",
                    header=not os.path.exists(output_csv),
                    index=False
                )
                buffer = []
                print(game_count)

            if max_games and game_count >= max_games:
                break

        if buffer:
            pd.DataFrame(buffer).to_csv(
                output_csv,
                mode="a",
                header=not os.path.exists(output_csv),
                index=False
            )

    print("finalizado:", game_count)