from chess_analysis.analytics_fast import load_data, aggregate_black_response

df = load_data()
result = aggregate_black_response(df)

print(result.head())