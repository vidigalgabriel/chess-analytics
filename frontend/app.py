import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/chess_gamespre1995.csv")
df = df.dropna(subset=["moves", "result"])
df["year"] = df["year"].astype(int)
df["decade"] = (df["year"] // 10) * 10

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

def make_graph_card(id_str):
    return dbc.Card(
        dcc.Graph(id=id_str, style={"height": "350px"}),
        className="shadow-lg mb-4",
        style={"backgroundColor": "#2b3035", "border": "none", "borderRadius": "15px", "padding": "10px"}
    )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Evolução das Aberturas (Linha do Tempo)", className="text-center text-light mb-4 mt-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtros", className="card-title text-info fw-bold"),
                    html.Hr(),
                    html.Label("Intervalo de Anos:", className="mt-2 text-light"),
                    dcc.RangeSlider(
                        id="year-slider",
                        min=df["year"].min(),
                        max=df["year"].max(),
                        step=1,
                        value=[1950, 2000],
                        marks={y: {'label': str(y), 'style': {'color': '#adb5bd'}} for y in range(1600, 2025, 40)},
                        className="mb-4 mt-2"
                    ),
                    html.Label("Métrica:", className="mt-4 text-light"),
                    dbc.RadioItems(
                        id="metric-select",
                        options=[
                            {"label": "Frequência (%)", "value": "freq"},
                            {"label": "Vitória Brancas (%)", "value": "white_win"},
                            {"label": "Vitória Pretas (%)", "value": "black_win"},
                            {"label": "Empates (%)", "value": "draw"},
                            {"label": "Score Brancas (%)", "value": "score_white"},
                            {"label": "Score Pretas (%)", "value": "score_black"}
                        ],
                        value="freq",
                        className="mb-3 text-light"
                    )
                ])
            ], className="shadow-lg h-100", style={"backgroundColor": "#2b3035", "border": "none", "borderRadius": "15px", "position": "sticky", "top": "20px"})
        ], width=3),
        dbc.Col([
            dbc.Row([dbc.Col(make_graph_card("g1-plot"), width=6), dbc.Col(make_graph_card("g2-plot"), width=6)]),
            dbc.Row([dbc.Col(make_graph_card("g3-plot"), width=6), dbc.Col(make_graph_card("g4-plot"), width=6)]),
            dbc.Row([dbc.Col(make_graph_card("g5-plot"), width=6), dbc.Col(make_graph_card("g6-plot"), width=6)]),
            dbc.Row([dbc.Col(make_graph_card("g7-plot"), width=6), dbc.Col(make_graph_card("g8-plot"), width=6)]),
            dbc.Row([dbc.Col(make_graph_card("g9-plot"), width=6), dbc.Col(make_graph_card("g10-plot"), width=6)]),
            dbc.Row([dbc.Col(make_graph_card("g11-plot"), width=6), dbc.Col(make_graph_card("g12-plot"), width=6)]),
        ], width=9)
    ], className="mb-4")
], fluid=True, style={"backgroundColor": "#212529", "minHeight": "100vh", "padding": "20px"})

@app.callback(
    [Output(f"g{i}-plot", "figure") for i in range(1, 13)],
    Input("year-slider", "value"),
    Input("metric-select", "value")
)
def update_graphs(year_range, metric):
    dff = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    def build_fig(cat_col, title):
        d_sub = dff.dropna(subset=[cat_col]).copy()
        if d_sub.empty:
            return px.line(title=title).update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        if metric == "freq":
            grouped = d_sub.groupby(["decade", cat_col]).size().reset_index(name="count")
            totals = grouped.groupby("decade")["count"].transform("sum")
            grouped["value"] = grouped["count"] / totals
        else:
            if metric == "white_win":
                d_sub["val"] = (d_sub["result"] == "1-0").astype(float)
            elif metric == "black_win":
                d_sub["val"] = (d_sub["result"] == "0-1").astype(float)
            elif metric == "draw":
                d_sub["val"] = (d_sub["result"] == "1/2-1/2").astype(float)
            elif metric == "score_white":
                d_sub["val"] = d_sub["result"].map({"1-0": 1.0, "1/2-1/2": 0.5, "0-1": 0.0}).fillna(0)
            elif metric == "score_black":
                d_sub["val"] = d_sub["result"].map({"0-1": 1.0, "1/2-1/2": 0.5, "1-0": 0.0}).fillna(0)
            
            grouped = d_sub.groupby(["decade", cat_col])["val"].mean().reset_index(name="value")

        fig = px.line(
            grouped, x="decade", y="value", color=cat_col, 
            title=title, markers=True, 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(
            hovertemplate='Valor: %{y:.2%}<extra>%{data.name}</extra>'
        )

        fig.update_layout(
            template="plotly_dark", 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)", 
            margin=dict(l=20, r=20, t=40, b=20), 
            xaxis_title="Década", 
            yaxis_title="", 
            yaxis_tickformat='.2%', 
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="#343a40",
                font_size=13,
                font_color="white",
                bordercolor="#495057"
            ),
            legend_title=""
        )
        return fig

    return (
        build_fig("g1", "1. Evolução Lance 1 Brancas"),
        build_fig("g2", "2. Resposta das Pretas a 1.e4"),
        build_fig("g3", "3. Resposta das Pretas a 1.d4"),
        build_fig("g4", "4. Após e4 e5 Nf3 Nc6"),
        build_fig("g5", "5. Após e4 c5 Nf3"),
        build_fig("g6", "6. Após Siciliana Aberta"),
        build_fig("g7", "7. Após e4 e6 d4 d5 (Francesa)"),
        build_fig("g8", "8. Após e4 c6 d4 d5 (Caro-Kann)"),
        build_fig("g9", "9. Após d4 d5 c4"),
        build_fig("g10", "10. Após d4 Nf6 c4"),
        build_fig("g11", "11. Após c4 (Inglesa)"),
        build_fig("g12", "12. Após Nf3 (Reti)"),
    )

if __name__ == "__main__":
    app.run(debug=True)