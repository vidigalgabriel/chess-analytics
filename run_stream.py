from chess_analysis.stream_parser import process_pgn_stream

process_pgn_stream(
    pgn_path="data/caissapng.pgn",
    output_csv="data/processed_games.csv",
    max_games=50000
)