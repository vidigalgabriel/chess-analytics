from chess_analysis.stream_parser import process_pgn_stream

process_pgn_stream(
    pgn_path="data/caissapng.pgn",
    output_csv="chess_analysis/data/test_sample.csv",
    max_games=100000,
    min_year=2020,
    max_year=2024
)