# run_stream.py
from chess_analysis.stream_parser import process_pgn_stream

pgn_path = r""
output_csv = r""

process_pgn_stream(
    pgn_path=pgn_path,
    output_csv=output_csv,
    block_size=5000,
    min_year=1600,
    max_year=2024,
    max_games=None
)