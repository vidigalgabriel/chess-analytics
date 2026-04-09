import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Chess Openings Dashboard")

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

df = load_data()

st.title("Chess Openings Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    metric = st.selectbox(
        "Metric",
        ["frequency", "white_winrate", "black_winrate", "drawrate", "avg_score"]
    )

with col2:
    chart_type = st.selectbox(
        "Chart Type",
        ["line", "bar", "area"]
    )

with col3:
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())

    if min_year == max_year:
        years = (min_year, max_year)
    else:
        years = st.slider(
            "Year Range",
            min_year,
            max_year,
            (min_year, max_year)
        )

filtered_df = df[(df["year"] >= years[0]) & (df["year"] <= years[1])]
stats = compute_stats(filtered_df)

def plot_category(title, openings):
    data = stats[stats["opening"].isin(openings)]
    if data.empty:
        return

    top_openings = (
        data.groupby("opening")["games"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .index
    )

    data = data[data["opening"].isin(top_openings)]

    data["frequency"] = data["games"] / data.groupby("decade")["games"].transform("sum") * 100

    if chart_type == "line":
        fig = px.line(
            data,
            x="decade",
            y=metric,
            color="opening",
            markers=True
        )
    elif chart_type == "bar":
        fig = px.bar(
            data,
            x="decade",
            y=metric,
            color="opening",
            barmode="group"
        )
    else:
        fig = px.area(
            data,
            x="decade",
            y=metric,
            color="opening"
        )

    fig.update_layout(
        template="plotly_dark",
        title=title,
        legend_title="Opening",
        yaxis_title=metric + " (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

tabs = st.tabs([
    "e4 e5",
    "Sicilian",
    "French",
    "Caro-Kann",
    "d4 Systems",
    "Data Table"
])

with tabs[0]:
    plot_category(
        "e4 e5",
        ["Ruy Lopez", "Italian Game", "Scotch Game", "Open Game Other", "e4 e5 Other"]
    )

with tabs[1]:
    plot_category(
        "Sicilian",
        ["Najdorf", "Sicilian Classical", "Sicilian Taimanov/Kan", "Sicilian Dragon", "Sicilian d6", "Sicilian Other"]
    )

with tabs[2]:
    plot_category(
        "French",
        ["French Classical", "French Tarrasch", "French Advance", "French Exchange", "French Other"]
    )

with tabs[3]:
    plot_category(
        "Caro-Kann",
        ["Caro-Kann Classical", "Caro Advance", "Caro Exchange", "Caro-Kann Other"]
    )

with tabs[4]:
    plot_category(
        "d4 Systems",
        ["QGD", "QGA", "Slav", "Nimzo-Indian", "Queen's Indian", "King's Indian", "Grunfeld", "Indian Other", "d4 d5 Other"]
    )

with tabs[5]:
    st.dataframe(
        stats.sort_values("games", ascending=False),
        use_container_width=True
    )