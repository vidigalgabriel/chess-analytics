# run_stream.py
from chess_analysis.stream_parser import process_pgn_stream

pgn_path = "data/caissapng_pre1995.pgn"
output_csv = "chess_analysis/data/pre1995_dataset.csv"
block_size = 5000

process_pgn_stream(pgn_path, output_csv, block_size)