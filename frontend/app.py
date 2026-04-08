import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

st.title("Chess Opening Analytics")

st.sidebar.header("Filtros")

start_year = st.sidebar.number_input("Ano inicial", value=2000)
end_year = st.sidebar.number_input("Ano final", value=2025)

metric_map = {
    "Games": "games",
    "Winrate Brancas": "white_winrate",
    "Winrate Pretas": "black_winrate",
    "Empates": "drawrate",
    "Score Médio": "avg_score",
    "Frequência": "frequency"
}

metric_label = st.sidebar.selectbox("Métrica", list(metric_map.keys()))
metric = metric_map[metric_label]

top_n = st.sidebar.slider("Top N respostas", 3, 12, 6)

params = {
    "start_year": int(start_year),
    "end_year": int(end_year)
}

def load(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", params=params)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

df_white = load("/white_moves")
df_e4 = load("/black_responses/e4")
df_d4 = load("/black_responses/d4")
df_c4 = load("/black_responses/c4")
df_nf3 = load("/black_responses/nf3")

def prepare(df, group_col):
    if df.empty:
        return df
    df = df[df[group_col] != "other"]
    top = (
        df.groupby(group_col)["games"]
        .sum()
        .nlargest(top_n)
        .index
    )
    return df[df[group_col].isin(top)].sort_values("decade")

def plot(df, title, group_col):
    if df.empty:
        st.warning("Sem dados")
        return
    fig = px.line(
        df,
        x="decade",
        y=metric,
        color=group_col,
        markers=True,
        title=title
    )
    fig.update_layout(
        height=400,
        legend_title_text="",
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

df_white = prepare(df_white, "white_move")
df_e4 = prepare(df_e4, "black_response")
df_d4 = prepare(df_d4, "black_response")
df_c4 = prepare(df_c4, "black_response")
df_nf3 = prepare(df_nf3, "black_response")

plot(df_white, "White First Moves", "white_move")

col1, col2 = st.columns(2)

with col1:
    plot(df_e4, "Respostas vs 1.e4", "black_response")
    plot(df_c4, "Respostas vs 1.c4", "black_response")

with col2:
    plot(df_d4, "Respostas vs 1.d4", "black_response")
    plot(df_nf3, "Respostas vs 1.Nf3", "black_response")

st.divider()

st.subheader("Resumo")

col3, col4 = st.columns(2)

with col3:
    st.dataframe(df_white, use_container_width=True)

with col4:
    st.dataframe(df_e4, use_container_width=True)