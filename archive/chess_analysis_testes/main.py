import sys
from pathlib import Path

from archive.chess_analysis_testes.parser import load_games
from archive.chess_analysis_testes.processing import process_games
from archive.chess_analysis_testes.analytics import compute_metrics, export_csv, prepare_for_visualization


# Arquivo principal que coordena o pipeline completo: carrega arquivos PGN, 
# aplica o tratamento de dados e executa as análises estatísticas. Finaliza 
# exportando os resultados consolidados para arquivos CSV organizados por 
# década e ano, prontos para uso em ferramentas de visualização.

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


def main():
    print(f"Loading PGN files from: {DATA_DIR}")
    raw_df = load_games(str(DATA_DIR))

    if raw_df.empty:
        print("No valid games found. Place .pgn files in the /data folder and re-run.")
        sys.exit(0)

    print(f"Loaded {len(raw_df)} valid games.")

    processed_df = process_games(raw_df)
    print(f"Processed {len(processed_df)} games.")

    metrics_by_decade = compute_metrics(processed_df, group_by="decade")
    print("\n--- Metrics by Decade (sample) ---")
    print(metrics_by_decade.head(20).to_string(index=False))

    output_path = OUTPUT_DIR / "metrics_by_decade.csv"
    export_csv(metrics_by_decade, str(output_path))
    print(f"\nCSV exported to: {output_path}")

    metrics_by_year = compute_metrics(processed_df, group_by="year")
    export_csv(metrics_by_year, str(OUTPUT_DIR / "metrics_by_year.csv"))
    print(f"CSV exported to: {OUTPUT_DIR / 'metrics_by_year.csv'}")

    viz_data = prepare_for_visualization(processed_df, group_by="decade")
    print(f"\nVisualization-ready data: {len(viz_data['data'])} records across columns: {viz_data['columns']}")


if __name__ == "__main__":
    main()
