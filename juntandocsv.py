import pandas as pd


csv2 = "data/chess_gamespre1995.csv"
csv1 = "data/chess_gamespre2013.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)


df = pd.concat([df1, df2], ignore_index=True)

df.to_csv("data/final_dataset16002013.csv", index=False)

print("Arquivo gerado com sucesso em data/basefinal.csv")
