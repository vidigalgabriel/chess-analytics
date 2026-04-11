import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/chess_gamespre2013.csv")
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "320px",
    "padding": "30px 25px",
    "backgroundColor": "#1e1e2f",
    "boxShadow": "4px 0 15px rgba(0,0,0,0.4)",
    "overflow": "hidden",
    "zIndex": 999
}

CONTENT_STYLE = {
    "marginLeft": "320px",
    "padding": "40px 50px",
    "backgroundColor": "#14141e",
    "minHeight": "100vh"
}

def make_kpi_card(title, id_str, color):
    return dbc.Card(
        dbc.CardBody([
            html.P(title, className="text-uppercase text-light fw-bold mb-1", style={"fontSize": "11px", "letterSpacing": "1.5px", "opacity": "0.7"}),
            html.H3(id=id_str, className=f"text-{color} m-0 fw-bolder")
        ]),
        style={"backgroundColor": "#27293d", "border": "none", "borderRadius": "10px", "boxShadow": "0 6px 12px rgba(0,0,0,0.15)"}
    )

def make_graph_card(id_str, height="450px"):
    return dbc.Card(
        dcc.Graph(id=id_str, style={"height": height, "width": "100%"}),
        className="mb-4",
        style={"backgroundColor": "#27293d", "border": "none", "borderRadius": "10px", "padding": "20px", "boxShadow": "0 6px 12px rgba(0,0,0,0.15)"}
    )

sidebar = html.Div([
    html.H2("Chess Analytics", className="fw-bolder text-info mb-0"),
    html.P("Analytics Platform", className="text-light mb-4", style={"fontSize": "12px", "letterSpacing": "2px", "opacity": "0.6"}),
    html.Hr(style={"borderColor": "#4b4b63"}),
    
    html.Div([
        html.Label("Período Analisado", className="text-light fw-bold text-uppercase mb-3", style={"fontSize": "12px", "letterSpacing": "1px"}),
        dcc.RangeSlider(
            id="year-slider",
            min=1850,
            max=2013,
            step=1,
            value=[1850, 2013],
            marks={y: {'label': str(y), 'style': {'color': '#8f8f9d', 'fontSize': '10px'}} for y in range(1850, 2020, 20)},
            className="mb-4"
        )
    ], className="mt-4"),
    
    html.Div([
        html.Label("Métrica de Visualização", className="text-light fw-bold text-uppercase mb-3", style={"fontSize": "12px", "letterSpacing": "1px"}),
        dbc.RadioItems(
            id="metric-select",
            options=[
                {"label": "Frequência Relativa (%)", "value": "freq"},
                {"label": "Vitórias Brancas (%)", "value": "white_win"},
                {"label": "Vitórias Pretas (%)", "value": "black_win"},
                {"label": "Taxa de Empates (%)", "value": "draw"},
                {"label": "Score Médio Brancas", "value": "score_white"},
                {"label": "Score Médio Pretas", "value": "score_black"}
            ],
            value="freq",
            className="d-flex flex-column gap-2",
            input_class_name="btn-check",
            label_class_name="btn btn-outline-info w-100 text-start py-2 px-3 fw-semibold shadow-sm",
            label_checked_class_name="active text-white border-info",
        )
    ], className="mt-5")
], style=SIDEBAR_STYLE)

content = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Painel de Aberturas Históricas", className="text-light fw-bold"),
            html.P("Monitoramento estratégico de partidas entre 1850 e 2013", className="text-light mb-4", style={"opacity": "0.7"}),
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col(make_kpi_card("Volume Total", "kpi-total", "info"), width=3),
        dbc.Col(make_kpi_card("Winrate Brancas", "kpi-white", "success"), width=3),
        dbc.Col(make_kpi_card("Winrate Pretas", "kpi-black", "danger"), width=3),
        dbc.Col(make_kpi_card("Taxa de Empates", "kpi-draw", "warning"), width=3),
    ], className="mb-4"),

    dcc.Loading(
        id="loading-content",
        type="circle",
        color="#38bdf8",
        children=[
            html.H4("Visão Macro", className="text-light mt-5 mb-4 fw-bold border-bottom pb-2", style={"borderColor": "#4b4b63"}),
            dbc.Row([
                dbc.Col(make_graph_card("pie-results", "400px"), width=5),
                dbc.Col(make_graph_card("bar-decades", "400px"), width=7)
            ]),
            
            html.H4("Top 10 Lances Iniciais", className="text-light mt-4 mb-4 fw-bold border-bottom pb-2", style={"borderColor": "#4b4b63"}),
            dbc.Card(
                dbc.CardBody(html.Div(id="top-table-container", className="px-2 py-1")),
                className="mb-5",
                style={"backgroundColor": "#27293d", "border": "none", "borderRadius": "10px", "boxShadow": "0 6px 12px rgba(0,0,0,0.15)"}
            ),

            html.H4("Evolução Linear por Aberturas", className="text-light mt-5 mb-4 fw-bold border-bottom pb-2", style={"borderColor": "#4b4b63"}),
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
        ]
    )
], style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content])

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
        pie_data, names="result", values="count", title="Resultados Globais", hole=0.6,
        color="result", color_discrete_map={"1-0": "#00f2c3", "0-1": "#fd5d93", "1/2-1/2": "#ff8d72"}
    )
    fig_pie.update_layout(
        template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
        margin=dict(t=50, b=20, l=20, r=20), font=dict(color="#ffffff")
    )

    decades_count = dff["decade"].value_counts().reset_index()
    decades_count.columns = ["decade", "count"]
    fig_bar = px.bar(
        decades_count, x="decade", y="count", title="Densidade de Partidas por Década",
        color_discrete_sequence=["#1d8cf8"]
    )
    fig_bar.update_layout(
        template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
        margin=dict(t=50, b=20, l=20, r=20), xaxis_title="", yaxis_title="", font=dict(color="#ffffff"),
        hovermode="x unified", hoverlabel=dict(bgcolor="#27293d", font_color="#ffffff")
    )

    top_moves = dff["first_2_moves"].value_counts().head(10).reset_index()
    top_moves.columns = ["Notação Inicial", "Volume Absoluto"]
    top_moves["Representatividade"] = (top_moves["Volume Absoluto"] / total).apply(lambda x: f"{x:.2%}") if total else "0%"
    
    table = dbc.Table.from_dataframe(top_moves, striped=True, bordered=False, hover=True, style={"color": "#ffffff", "margin": "0"})

    def build_line_fig(cat_col, title):
        d_sub = dff[dff[cat_col].notna()]
        if d_sub.empty:
            return px.line(title=title).update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        if metric == "freq":
            grouped = d_sub.groupby(["decade", cat_col]).size().reset_index(name="count")
            totals = grouped.groupby("decade")["count"].transform("sum")
            grouped["value"] = grouped["count"] / totals
            tickformat = '.2%'
            y_format = '%{y:.2%}'
        else:
            grouped = d_sub.groupby(["decade", cat_col])[metric].mean().reset_index(name="value")
            tickformat = None
            y_format = '%{y:.3f}'

        cat_order = grouped.groupby(cat_col)["value"].sum().sort_values(ascending=False).index.tolist()

        fig = px.line(
            grouped, x="decade", y="value", color=cat_col, title=title, 
            markers=True, color_discrete_sequence=px.colors.qualitative.Plotly,
            category_orders={cat_col: cat_order}
        )
        fig.update_traces(
            line=dict(width=3), 
            marker=dict(size=8), 
            hovertemplate=f'<b>%{{data.name}}</b>: {y_format}<extra></extra>'
        )
        fig.update_layout(
            template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
            margin=dict(l=40, r=40, t=60, b=40), xaxis_title="", yaxis_title="", 
            yaxis_tickformat=tickformat, hovermode="x unified",
            hoverlabel=dict(bgcolor="#27293d", font_color="#ffffff"),
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, title=""),
            font=dict(color="#ffffff")
        )
        return fig

    figs = [
        build_line_fig("g1", "1. Evolução do Primeiro Lance (Brancas)"),
        build_line_fig("g2", "2. Resposta Direta das Pretas a 1.e4"),
        build_line_fig("g3", "3. Resposta Direta das Pretas a 1.d4"),
        build_line_fig("g4", "4. Ramificações: e4 e5 Nf3 Nc6"),
        build_line_fig("g5", "5. Ramificações: e4 c5 Nf3"),
        build_line_fig("g6", "6. Sub-linhas da Siciliana Aberta"),
        build_line_fig("g7", "7. Estruturas da Defesa Francesa"),
        build_line_fig("g8", "8. Estruturas da Defesa Caro-Kann"),
        build_line_fig("g9", "9. Variantes do Gambito da Rainha (d4 d5 c4)"),
        build_line_fig("g10", "10. Sistemas Indianos (d4 Nf6 c4)"),
        build_line_fig("g11", "11. Respostas à Abertura Inglesa"),
        build_line_fig("g12", "12. Respostas à Abertura Reti")
    ]

    return str_total, str_w_wins, str_b_wins, str_draws, fig_pie, fig_bar, table, *figs

if __name__ == "__main__":
    app.run(debug=True)