import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from archive.chess_analysis_testes.stream_parser import process_pgn_stream

pgn_path = r"\data\caissapng_pre2013.pgn"
output_csv = r"\data\chess_gamespre2013.csv"

process_pgn_stream(
    pgn_path=pgn_path,
    output_csv=output_csv,
    block_size=10000,
    min_year=1600,
    max_year=2024,
    max_games=None
)