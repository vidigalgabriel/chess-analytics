import pandas as pd

csv1 = "chess_analysis/data/full_dataset_safe.csv"
csv2 = "chess_analysis/data/pre2013_dataset.csv"
csv3 = "chess_analysis/data/pre1995_dataset.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df3 = pd.read_csv(csv3)

df = pd.concat([df1, df2, df3], ignore_index=True)

df.to_csv("chess_analysis/data/final_dataset.csv", index=False)