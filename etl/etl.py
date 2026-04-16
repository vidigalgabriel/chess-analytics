import pandas as pd

df = pd.read_csv("../data/final_dataset16002013.csv")
df = df.dropna(subset=["moves", "result"])
df["year"] = df["year"].astype(int)
df["decade"] = (df["year"] // 10) * 10

df["first_2_moves"] = df["moves"].apply(lambda x: " ".join(str(x).split()[:2]) if len(str(x).split()) >= 2 else str(x))

df['white_win'] = (df['result'] == '1-0').astype(float)
df['black_win'] = (df['result'] == '0-1').astype(float)
df['draw'] = (df['result'] == '1/2-1/2').astype(float)
df['score_white'] = df['white_win'] + (df['draw'] * 0.5)
df['score_black'] = df['black_win'] + (df['draw'] * 0.5)

df['w1'] = df['moves'].apply(lambda x: str(x).split()[0] if len(str(x).split()) > 0 else None)
df['b1'] = df['moves'].apply(lambda x: str(x).split()[1] if len(str(x).split()) > 1 else None)
df['w2'] = df['moves'].apply(lambda x: str(x).split()[2] if len(str(x).split()) > 2 else None)

def cat_g1(m):
    p = str(m).split()
    if not p: return "Outros"
    return p[0] if p[0] in ["e4", "d4", "c4", "Nf3"] else "Outros"

def cat_g2(m):
    if not m.startswith("e4 "): return None
    p = m.split()
    return p[1] if len(p) > 1 and p[1] in ["e5", "c5", "c6", "e6"] else "Outros"

def cat_g3(m):
    if not m.startswith("d4 "): return None
    p = m.split()
    return p[1] if len(p) > 1 and p[1] in ["d5", "Nf6"] else "Outros"

def cat_g4(m):
    if not m.startswith("e4 e5"): return None
    if m.startswith("e4 e5 Nf3 Nc6 Bb5"): return "Ruy Lopez"
    if m.startswith("e4 e5 Nf3 Nc6 Bc4"): return "Italiana"
    if m.startswith("e4 e5 Nf3 Nc6 d4"): return "Escocesa"
    return "e4 e5 Other"

def cat_g5(m):
    if not m.startswith("e4 c5"): return None
    if m.startswith("e4 c5 Nf3 d6"): return "Siciliana d6"
    if m.startswith("e4 c5 Nf3 e6"): return "Siciliana e6"
    if m.startswith("e4 c5 Nf3 Nc6"): return "Siciliana Nc6"
    if m.startswith("e4 c5 Nf3 g6"): return "Siciliana g6"
    return "Siciliana Other"

def cat_g6(m):
    if m.startswith("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6"): return "Najdorf"
    if m.startswith("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 Nc6"): return "Classica"
    if m.startswith("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 e6"): return "Scheveninguen"
    if m.startswith("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6"): return "Dragao"
    if m.startswith("e4 c5 Nf3 e6 d4 cxd4 Nxd4 a6"): return "Kan"
    if m.startswith("e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6"): return "Taimanov"
    if m.startswith("e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e5"): return "Sveshnikov"
    if m.startswith("e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6"): return "Dragao acelerada"
    return None

def cat_g7(m):
    if not m.startswith("e4 e6 d4 d5"): return None
    if m.startswith("e4 e6 d4 d5 Nc3 Nf6"): return "Francesa Clássica"
    if m.startswith("e4 e6 d4 d5 Nd2"): return "Francesa Tarrasch"
    if m.startswith("e4 e6 d4 d5 exd5"): return "Francesa das Trocas"
    if m.startswith("e4 e6 d4 d5 e5"): return "Francesa do avanço"
    return "Francesas Other"

def cat_g8(m):
    if not m.startswith("e4 c6 d4 d5"): return None
    if m.startswith("e4 c6 d4 d5 Nc3 dxe4 Nxe4 Bf5"): return "Caro-Kann Clássica"
    if m.startswith("e4 c6 d4 d5 exd5 cxd5"): return "Caro-Kann das Trocas"
    if m.startswith("e4 c6 d4 d5 e5"): return "Caro-Kann do Avanço"
    return "Caro Kann Other"

def cat_g9(m):
    if not m.startswith("d4 d5 c4"): return None
    if m.startswith("d4 d5 c4 e6"): return "QGD"
    if m.startswith("d4 d5 c4 dxc4"): return "QGA"
    if m.startswith("d4 d5 c4 c6 Nf3 Nf6 Nc3 dxc4"): return "Eslava"
    if m.startswith("d4 d5 c4 c6 e3 Nf6 Nc3 e6"): return "Semi-Eslava"
    return None

def cat_g10(m):
    if not m.startswith("d4"): return None
    if m.startswith("d4 Nf6 c4 e6 Nc3 Bb4"): return "Nimzo-Índia"
    if m.startswith("d4 Nf6 c4 g6 Nc3 d5"): return "Grunfeld"
    if m.startswith("d4 Nf6 c4 g6 Nc3 Bg7 e4 d6"): return "KID"
    return "d4 Other"

def cat_g11(m):
    if not m.startswith("c4"): return None
    if m.startswith("c4 e5"): return "Inglesa Rei"
    if m.startswith("c4 c5"): return "Simétrica"
    if m.startswith("c4 Nf6"): return "Anglo-Índia"
    return "Other c4"

def cat_g12(m):
    if not m.startswith("Nf3"): return None
    if m.startswith("Nf3 d5"): return "Reti d5"
    if m.startswith("Nf3 Nf6"): return "Reti Nf6"
    return "Other Nf3"

df["g1"] = df["moves"].apply(cat_g1)
df["g2"] = df["moves"].apply(cat_g2)
df["g3"] = df["moves"].apply(cat_g3)
df["g4"] = df["moves"].apply(cat_g4)
df["g5"] = df["moves"].apply(cat_g5)
df["g6"] = df["moves"].apply(cat_g6)
df["g7"] = df["moves"].apply(cat_g7)
df["g8"] = df["moves"].apply(cat_g8)
df["g9"] = df["moves"].apply(cat_g9)
df["g10"] = df["moves"].apply(cat_g10)
df["g11"] = df["moves"].apply(cat_g11)
df["g12"] = df["moves"].apply(cat_g12)

df = df.drop(columns=["moves"])

df.to_parquet("../data/dataset_processado.parquet", index=False)