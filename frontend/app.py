import streamlit as st
import pandas as pd
import requests

st.title("Chess Analytics")

start = st.slider("Start Year", 1800, 2025, 1900)
end = st.slider("End Year", 1800, 2025, 2020)

if st.button("Load Data"):
    res = requests.get(
        "http://127.0.0.1:8000/metrics",
        params={"start_year": start, "end_year": end}
    )

    df = pd.DataFrame(res.json())

    st.write(df)

    if not df.empty:
        st.line_chart(df["avg_score"])