import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

st.title("Chess Opening Analytics")

# ----------------------
# Sidebar filtros
# ----------------------

st.sidebar.header("Filtros")

start_year = st.sidebar.number_input("Ano inicial", value=2000)
end_year = st.sidebar.number_input("Ano final", value=2025)

metric = st.sidebar.selectbox(
    "Métrica",
    ["games", "white_winrate", "black_winrate", "drawrate"]
)

top_n = st.sidebar.slider("Top respostas das pretas", 3, 10, 5)

if st.sidebar.button("Atualizar"):
    st.rerun()

# ----------------------
# Requests API
# ----------------------

params = {
    "start_year": int(start_year),
    "end_year": int(end_year)
}

try:
    white_resp = requests.get(f"{API_URL}/white_moves", params=params)
    black_resp = requests.get(f"{API_URL}/black_responses", params=params)

    df_white = pd.DataFrame(white_resp.json())
    df_black = pd.DataFrame(black_resp.json())

except Exception as e:
    st.error("Erro ao conectar com backend")
    st.stop()

# ----------------------
# Layout
# ----------------------

col1, col2 = st.columns(2)

# ----------------------
# White moves
# ----------------------

with col1:
    st.subheader("White First Moves")

    if not df_white.empty:
        df_white = df_white.sort_values("decade")

        fig1 = px.line(
            df_white,
            x="decade",
            y=metric,
            color="white_move",
            markers=True
        )

        st.plotly_chart(fig1, use_container_width=True)

        with st.expander("Ver dados"):
            st.dataframe(df_white)

        st.download_button(
            "Download CSV",
            df_white.to_csv(index=False),
            file_name="white_moves.csv"
        )
    else:
        st.warning("Sem dados")

# ----------------------
# Black responses
# ----------------------

with col2:
    st.subheader("Black Responses")

    if not df_black.empty:
        df_black = df_black.sort_values(["decade", "black_response"])

        top_responses = (
            df_black.groupby("black_response")["games"]
            .sum()
            .nlargest(top_n)
            .index
        )

        df_filtered = df_black[
            df_black["black_response"].isin(top_responses)
        ]

        fig2 = px.bar(
            df_filtered,
            x="decade",
            y=metric,
            color="black_response",
            barmode="group"
        )

        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("Ver dados"):
            st.dataframe(df_filtered)

        st.download_button(
            "Download CSV",
            df_filtered.to_csv(index=False),
            file_name="black_responses.csv"
        )
    else:
        st.warning("Sem dados")