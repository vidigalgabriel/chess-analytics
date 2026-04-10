import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

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

def make_kpi_card(title, id_str, icon_color):
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="card-title text-muted text-uppercase"),
            html.H3(id=id_str, className=f"text-{icon_color} fw-bold")
        ])
    ], className="shadow-sm mb-4", style={"backgroundColor": "#2b3035", "border": "none", "borderRadius": "10px"})

def make_graph_card(id_str, height="400px"):
    return dbc.Card(
        dcc.Graph(id=id_str, style={"height": height}),
        className="shadow-lg mb-4",
        style={"backgroundColor": "#2b3035", "border": "none", "borderRadius": "15px", "padding": "10px"}
    )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard de Aberturas de Xadrez Históricas", className="text-light mt-4 fw-bold"),
            html.P("Análise completa da evolução de aberturas de xadrez de 1600 a 1994. Explore tendências, popularidade e eficiência através das décadas.", className="text-muted fs-5 mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col(make_kpi_card("Total de Partidas", "kpi-total", "info"), width=3),
        dbc.Col(make_kpi_card("Vitórias Brancas", "kpi-white", "success"), width=3),
        dbc.Col(make_kpi_card("Vitórias Pretas", "kpi-black", "danger"), width=3),
        dbc.Col(make_kpi_card("Empates", "kpi-draw", "warning"), width=3),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Controles de Análise", className="card-title text-info fw-bold"),
                    html.Hr(),
                    html.Label("Intervalo de Anos:", className="mt-2 text-light fw-bold"),
                    dcc.RangeSlider(
                        id="year-slider",
                        min=df["year"].min(),
                        max=df["year"].max(),
                        step=1,
                        value=[1920, 2014],
                        marks={y: {'label': str(y), 'style': {'color': '#adb5bd', 'fontSize': '10px'}} for y in range(1600, 2025, 40)},
                        className="mb-4 mt-2"
                    ),
                    html.Label("Métrica dos Gráficos de Linha:", className="mt-4 text-light fw-bold"),
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
            dcc.Loading(
                id="loading-content",
                type="dot",
                color="#17a2b8",
                children=[
                    html.H4("Visão Geral do Período", className="text-light mb-3 mt-2 fw-bold"),
                    dbc.Row([
                        dbc.Col(make_graph_card("pie-results", "350px"), width=4),
                        dbc.Col(make_graph_card("bar-decades", "350px"), width=8)
                    ]),
                    
                    html.H4("Evolução Detalhada por Abertura", className="text-light mb-3 mt-4 fw-bold"),
                    dbc.Row([dbc.Col(make_graph_card("g1-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g2-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g3-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g4-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g5-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g6-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g7-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g8-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g9-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g10-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g11-plot"), width=12)]),
                    dbc.Row([dbc.Col(make_graph_card("g12-plot"), width=12)]),
                    
                    html.H4("Top 10 Inícios Mais Populares (2 Lances)", className="text-light mb-3 mt-4 fw-bold"),
                    dbc.Card(
                        dbc.CardBody(html.Div(id="top-table-container")),
                        className="shadow-lg mb-4",
                        style={"backgroundColor": "#2b3035", "border": "none", "borderRadius": "15px"}
                    )
                ]
            )
        ], width=9)
    ], className="mb-4")
], fluid=True, style={"backgroundColor": "#212529", "minHeight": "100vh", "padding": "20px"})

@app.callback(
    Output("kpi-total", "children"),
    Output("kpi-white", "children"),
    Output("kpi-black", "children"),
    Output("kpi-draw", "children"),
    Output("pie-results", "figure"),
    Output("bar-decades", "figure"),
    Output("top-table-container", "children"),
    [Output(f"g{i}-plot", "figure") for i in range(1, 13)],
    Input("year-slider", "value"),
    Input("metric-select", "value")
)
def update_dashboard(year_range, metric):
    dff = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    total = len(dff)
    w_wins = int(dff['white_win'].sum())
    b_wins = int(dff['black_win'].sum())
    draws = int(dff['draw'].sum())

    str_total = f"{total:,}".replace(",", ".")
    str_w_wins = f"{w_wins:,}".replace(",", ".") + f" ({w_wins/total:.1%} )" if total else "0"
    str_b_wins = f"{b_wins:,}".replace(",", ".") + f" ({b_wins/total:.1%} )" if total else "0"
    str_draws = f"{draws:,}".replace(",", ".") + f" ({draws/total:.1%} )" if total else "0"

    pie_data = dff['result'].value_counts().reset_index()
    pie_data.columns = ['result', 'count']
    fig_pie = px.pie(
        pie_data, names="result", values="count", title="Distribuição de Resultados",
        color="result", color_discrete_map={"1-0": "#28a745", "0-1": "#dc3545", "1/2-1/2": "#ffc107"}
    )
    fig_pie.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))

    decades_count = dff["decade"].value_counts().reset_index()
    decades_count.columns = ["decade", "count"]
    fig_bar = px.bar(
        decades_count, x="decade", y="count", title="Volume de Partidas por Década",
        color_discrete_sequence=["#17a2b8"]
    )
    fig_bar.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10), xaxis_title="Década", yaxis_title="Partidas")

    top_moves = dff["first_2_moves"].value_counts().head(10).reset_index()
    top_moves.columns = ["Lances Iniciais", "Quantidade"]
    top_moves["Porcentagem"] = (top_moves["Quantidade"] / total).apply(lambda x: f"{x:.2%}") if total else "0%"
    
    table = dbc.Table.from_dataframe(top_moves, striped=True, bordered=False, hover=True, color="dark", style={"color": "white", "margin": "0"})

    def build_line_fig(cat_col, title):
        d_sub = dff[dff[cat_col].notna()]
        if d_sub.empty:
            return px.line(title=title).update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        if metric == "freq":
            grouped = d_sub.groupby(["decade", cat_col]).size().reset_index(name="count")
            totals = grouped.groupby("decade")["count"].transform("sum")
            grouped["value"] = grouped["count"] / totals
        else:
            grouped = d_sub.groupby(["decade", cat_col])[metric].mean().reset_index(name="value")

        fig = px.line(grouped, x="decade", y="value", color=cat_col, title=title, markers=True, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(hovertemplate='Valor: %{y:.2%}<extra>%{data.name}</extra>')
        fig.update_layout(
            template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
            margin=dict(l=20, r=20, t=40, b=20), xaxis_title="Década", yaxis_title="", 
            yaxis_tickformat='.2%', hovermode="x unified",
            hoverlabel=dict(bgcolor="#343a40", font_size=13, font_color="white", bordercolor="#495057"), legend_title=""
        )
        return fig

    figs = [
        build_line_fig("g1", "1. Evolução Lance 1 Brancas"),
        build_line_fig("g2", "2. Resposta das Pretas a 1.e4"),
        build_line_fig("g3", "3. Resposta das Pretas a 1.d4"),
        build_line_fig("g4", "4. Após e4 e5 Nf3 Nc6"),
        build_line_fig("g5", "5. Após e4 c5 Nf3"),
        build_line_fig("g6", "6. Após Siciliana Aberta"),
        build_line_fig("g7", "7. Após e4 e6 d4 d5 (Francesa)"),
        build_line_fig("g8", "8. Após e4 c6 d4 d5 (Caro-Kann)"),
        build_line_fig("g9", "9. Após d4 d5 c4"),
        build_line_fig("g10", "10. Após d4 Nf6 c4"),
        build_line_fig("g11", "11. Após c4 (Inglesa)"),
        build_line_fig("g12", "12. Após Nf3 (Reti)")
    ]

    return str_total, str_w_wins, str_b_wins, str_draws, fig_pie, fig_bar, table, *figs

if __name__ == "__main__":
    app.run(debug=True)