# run_stream.py
from chess_analysis.stream_parser import process_pgn_stream

pgn_path = r"C:\Users\vidig\Desktop\Data-Analyst-Python\data\caissapng_pre2013.pgn"
output_csv = r"C:\Users\vidig\Desktop\Data-Analyst-Python\data\chess_gamespre2013.csv"

process_pgn_stream(
    pgn_path=pgn_path,
    output_csv=output_csv,
    block_size=5000,
    min_year=1600,
    max_year=2024,
    max_games=None
)