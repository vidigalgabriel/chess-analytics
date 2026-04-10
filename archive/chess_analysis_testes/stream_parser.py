# chess_analysis/stream_parser.py
import chess.pgn
import pandas as pd
import os

# Analisador de partidas em tempo real que extrai metadados de arquivos PGN e 
# utiliza uma lógica de árvore de decisão para classificar as aberturas com 
# base na sequência de lances. O script processa os dados em blocos para 
# otimizar o uso de memória e exporta os resultados filtrados diretamente para CSV.

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
                    if "Nc3" in m and "d4" in m:
                        return "Taimanov/Kan"
                    return "Sicilian e6"
                if m[3] == "g6":
                    return "Sicilian g6"
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
        if m[0] == "c4":
            if m[1] == "e5":
                return "English King"
            if m[1] == "c5":
                return "English Symmetrical"
            if m[1] == "Nf6":
                return "English Anglo-Indian"
            return "English Other"
        if m[0] == "Nf3":
            if m[1] == "d5":
                return "Reti d5"
            if m[1] == "Nf6":
                return "Reti Nf3"
            return "Reti Other"
    except:
        return "Unknown"
    return "Other"

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
    if len(moves) < 10:
        return None
    board = game.board()
    san_moves = []
    for move in moves[:10]:
        san_moves.append(board.san(move))
        board.push(move)
    opening = classify_opening(san_moves)
    return {
        "year": year,
        "result": result,
        "moves": " ".join(san_moves),
        "opening": opening
    }

def process_pgn_stream(pgn_path, output_csv, block_size=5000, min_year=None, max_year=None, max_games=None):
    data = []
    count = 0
    block_number = 1
    with open(pgn_path, encoding="utf-8", errors="ignore") as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            extracted = extract_game_data(game)
            if extracted:
                if min_year and extracted["year"] < min_year:
                    continue
                if max_year and extracted["year"] > max_year:
                    continue
                data.append(extracted)
                count += 1
                if max_games and count >= max_games:
                    break
            if len(data) >= block_size:
                df = pd.DataFrame(data)
                mode = "a" if os.path.exists(output_csv) else "w"
                header = not os.path.exists(output_csv)
                df.to_csv(output_csv, mode=mode, index=False, header=header)
                print(f"Bloco {block_number} processado, partidas neste bloco: {len(data)}")
                data = []
                block_number += 1
    if data:
        df = pd.DataFrame(data)
        mode = "a" if os.path.exists(output_csv) else "w"
        header = not os.path.exists(output_csv)
        df.to_csv(output_csv, mode=mode, index=False, header=header)
        print(f"Último bloco processado, partidas neste bloco: {len(data)}")
    print("Processamento finalizado, total de partidas:", count)