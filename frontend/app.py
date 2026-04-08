import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("../chess_analysis/data/test_sample.csv")

df["decade"] = (df["year"] // 10) * 10

def compute_stats(df):
    grouped = (
        df.groupby(["decade", "opening"])
        .agg(
            games=("result", "count"),
            white_wins=("result", lambda x: (x == "1-0").sum()),
            black_wins=("result", lambda x: (x == "0-1").sum()),
            draws=("result", lambda x: (x == "1/2-1/2").sum()),
        )
        .reset_index()
    )

    grouped["white_winrate"] = grouped["white_wins"] / grouped["games"]
    grouped["black_winrate"] = grouped["black_wins"] / grouped["games"]
    grouped["drawrate"] = grouped["draws"] / grouped["games"]
    grouped["avg_score"] = (
        grouped["white_wins"] + 0.5 * grouped["draws"]
    ) / grouped["games"]

    grouped["frequency"] = grouped["games"] / grouped.groupby("decade")["games"].transform("sum")

    return grouped

stats = compute_stats(df)

metric = st.selectbox(
    "",
    ["frequency", "white_winrate", "black_winrate", "drawrate", "avg_score"]
)

min_year = int(df["year"].min())
max_year = int(df["year"].max())

if min_year == max_year:
    years = (min_year, max_year)
else:
    years = st.slider(
        "",
        min_year,
        max_year,
        (min_year, max_year)
    )

filtered_df = df[(df["year"] >= years[0]) & (df["year"] <= years[1])]
filtered_stats = compute_stats(filtered_df)

def plot_category(title, openings):
    data = filtered_stats[filtered_stats["opening"].isin(openings)]
    if data.empty:
        return
    fig = px.line(
        data,
        x="decade",
        y=metric,
        color="opening",
        markers=True,
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)

st.title("Chess Openings Analysis")

plot_category(
    "e4 e5",
    ["Ruy Lopez", "Italian Game", "Scotch Game", "Open Game Other", "e4 e5 Other"]
)

plot_category(
    "Sicilian",
    ["Najdorf", "Sicilian Classical", "Sicilian Taimanov/Kan", "Sicilian Dragon", "Sicilian d6", "Sicilian Other"]
)

plot_category(
    "French",
    ["French Classical", "French Tarrasch", "French Advance", "French Exchange", "French Other"]
)

plot_category(
    "Caro-Kann",
    ["Caro-Kann Classical", "Caro Advance", "Caro Exchange", "Caro-Kann Other"]
)

plot_category(
    "d4 systems",
    ["QGD", "QGA", "Slav", "Nimzo-Indian", "Queen's Indian", "King's Indian", "Grunfeld", "Indian Other", "d4 d5 Other"]
)

st.dataframe(
    filtered_stats.sort_values("games", ascending=False),
    use_container_width=True
)