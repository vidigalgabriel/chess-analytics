import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("../chess_analysis/data/final_dataset.csv")
    df["decade"] = (df["year"] // 10) * 10
    return df

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

    grouped["white_winrate"] = grouped["white_wins"] / grouped["games"] * 100
    grouped["black_winrate"] = grouped["black_wins"] / grouped["games"] * 100
    grouped["drawrate"] = grouped["draws"] / grouped["games"] * 100
    grouped["avg_score"] = (
        (grouped["white_wins"] + 0.5 * grouped["draws"]) / grouped["games"]
    ) * 100

    return grouped

def plot_block(title, openings, stats):
    col1, col2 = st.columns([3, 1])

    with col2:
        metric = st.selectbox(
            f"Metric - {title}",
            ["frequency", "white_winrate", "black_winrate", "drawrate", "avg_score"],
            key=f"metric_{title}"
        )

        chart_type = st.selectbox(
            f"Chart - {title}",
            ["line", "bar", "area"],
            key=f"chart_{title}"
        )

    data = stats[stats["opening"].isin(openings)]

    top_openings = (
        data.groupby("opening")["games"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .index
    )

    data = data[data["opening"].isin(top_openings)]

    data["frequency"] = data["games"] / data.groupby("decade")["games"].transform("sum") * 100

    with col1:
        if chart_type == "line":
            fig = px.line(data, x="decade", y=metric, color="opening", markers=True)
        elif chart_type == "bar":
            fig = px.bar(data, x="decade", y=metric, color="opening", barmode="group")
        else:
            fig = px.area(data, x="decade", y=metric, color="opening")

        fig.update_layout(
            title=title,
            yaxis_title="%",
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

df = load_data()

min_year = int(df["year"].min())
max_year = int(df["year"].max())

years = st.slider("Year Range", min_year, max_year, (min_year, max_year))

filtered_df = df[(df["year"] >= years[0]) & (df["year"] <= years[1])]
stats = compute_stats(filtered_df)

st.title("Chess Openings Dashboard")

plot_block(
    "e4 e5",
    ["Ruy Lopez", "Italian Game", "Scotch Game", "Open Game Other", "e4 e5 Other"],
    stats
)

plot_block(
    "Sicilian",
    ["Najdorf", "Sicilian Classical", "Sicilian Taimanov/Kan", "Sicilian Dragon", "Sicilian d6", "Sicilian Other"],
    stats
)

plot_block(
    "French",
    ["French Classical", "French Tarrasch", "French Advance", "French Exchange", "French Other"],
    stats
)

plot_block(
    "Caro-Kann",
    ["Caro-Kann Classical", "Caro Advance", "Caro Exchange", "Caro-Kann Other"],
    stats
)

plot_block(
    "d4 Systems",
    ["QGD", "QGA", "Slav", "Nimzo-Indian", "Queen's Indian", "King's Indian", "Grunfeld", "Indian Other", "d4 d5 Other"],
    stats
)