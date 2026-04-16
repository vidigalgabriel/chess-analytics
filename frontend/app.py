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

decades_list = sorted(df["decade"].unique())
default_start = 1930 if 1930 in decades_list else decades_list[0]
default_end = 2010 if 2010 in decades_list else decades_list[-1]

TITLES = {
    "g1": "1. Evolução do Primeiro Lance (Brancas)",
    "g2": "2. Resposta Direta das Pretas a 1.e4",
    "g3": "3. Resposta Direta das Pretas a 1.d4",
    "g4": "4. Ramificações: e4 e5 Nf3 Nc6",
    "g5": "5. Ramificações: e4 c5 Nf3",
    "g6": "6. Sub-linhas da Siciliana Aberta",
    "g7": "7. Estruturas da Defesa Francesa",
    "g8": "8. Estruturas da Defesa Caro-Kann",
    "g9": "9. Variantes do Gambito da Rainha (d4 d5 c4)",
    "g10": "10. Sistemas Indianos (d4 Nf6 c4)",
    "g11": "11. Respostas à Abertura Inglesa",
    "g12": "12. Respostas à Abertura Reti"
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "280px",
    "padding": "2rem 1.5rem", "backgroundColor": "#1e1e2f", "borderRight": "1px solid #2b2b40",
    "display": "flex", "flexDirection": "column", "zIndex": 999
}

CONTENT_STYLE = {
    "marginLeft": "280px", "padding": "2rem 3rem", "backgroundColor": "#14141e", "minHeight": "100vh"
}

def make_kpi_card(title, id_str, color):
    return dbc.Card(
        dbc.CardBody([
            html.P(title, className="text-uppercase text-light fw-bold mb-1", style={"fontSize": "11px", "opacity": "0.7"}),
            html.H3(id=id_str, className=f"text-{color} m-0 fw-bolder")
        ]),
        style={"backgroundColor": "#27293d", "border": "none", "borderRadius": "8px"}
    )

def make_graph_card(id_str, height="480px"):
    return dbc.Card(
        dcc.Graph(id=id_str, style={"height": height, "width": "100%"}),
        className="mb-4",
        style={"backgroundColor": "#27293d", "border": "none", "borderRadius": "8px", "padding": "15px"}
    )

sidebar = html.Div([
    html.Div([
        html.H4("Chess Analytics", className="fw-bolder text-info mb-0"),
        html.P("Dashboard Histórico", className="text-light mb-0", style={"fontSize": "12px", "opacity": "0.6"}),
    ], className="mb-4"),
    html.Hr(style={"borderColor": "#4b4b63"}),
    html.Div([
        html.Label("Início do Período", className="text-light fw-bold small mb-2"),
        dcc.Dropdown(
            id="start-decade",
            options=[{"label": str(d), "value": d} for d in decades_list],
            value=default_start,
            clearable=False,
            className="mb-3",
            style={"color": "#000000"}
        ),
        html.Label("Fim do Período", className="text-light fw-bold small mb-2"),
        dcc.Dropdown(
            id="end-decade",
            options=[{"label": str(d), "value": d} for d in decades_list],
            value=default_end,
            clearable=False,
            className="mb-4",
            style={"color": "#000000"}
        ),
    ]),
    html.Div([
        html.Label("Métrica", className="text-light fw-bold small mb-3"),
        dbc.RadioItems(
            id="metric-select",
            options=[
                {"label": "Frequência (%)", "value": "freq"},
                {"label": "Vitórias Brancas", "value": "white_win"},
                {"label": "Vitórias Pretas", "value": "black_win"},
                {"label": "Empates", "value": "draw"},
                {"label": "Score Brancas", "value": "score_white"}
            ],
            value="freq",
            input_class_name="btn-check",
            label_class_name="btn btn-outline-info w-100 text-start mb-2",
            label_checked_class_name="active",
        )
    ])
], style=SIDEBAR_STYLE)

content = html.Div([
    dbc.Row([
        dbc.Col(make_kpi_card("Volume Total", "kpi-total", "info"), width=3),
        dbc.Col(make_kpi_card("Winrate Brancas", "kpi-white", "success"), width=3),
        dbc.Col(make_kpi_card("Winrate Pretas", "kpi-black", "danger"), width=3),
        dbc.Col(make_kpi_card("Empates", "kpi-draw", "warning"), width=3),
    ], className="mb-4"),
    dbc.Tabs([
        dbc.Tab(label="Geral", children=[
            dbc.Row([dbc.Col(make_graph_card("sunburst-moves", "500px"), width=12)]),
            dbc.Row([dbc.Col(make_graph_card("g1-plot", "550px"), width=12)]),
            dbc.Row([dbc.Col(make_graph_card("pie-results", "450px"), width=5), dbc.Col(make_graph_card("bar-decades", "450px"), width=7)]),
        ], tab_id="tab-1"),
        dbc.Tab(label="Aberturas e4", children=[
            dbc.Row([dbc.Col(make_graph_card(f"g{i}-plot", "550px"), width=12) for i in [2, 4, 5, 6, 7, 8]])
        ], tab_id="tab-2"),
        dbc.Tab(label="Aberturas d4", children=[
            dbc.Row([dbc.Col(make_graph_card(f"g{i}-plot", "550px"), width=12) for i in [3, 9, 10]])
        ], tab_id="tab-3"),
        dbc.Tab(label="Outras", children=[
            dbc.Row([dbc.Col(make_graph_card(f"g{i}-plot", "550px"), width=12) for i in [11, 12]])
        ], tab_id="tab-4"),
    ], id="tabs", active_tab="tab-1")
], style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content])

@app.callback(
    [Output("kpi-total", "children"), Output("kpi-white", "children"), Output("kpi-black", "children"), Output("kpi-draw", "children"),
     Output("pie-results", "figure"), Output("bar-decades", "figure"), Output("sunburst-moves", "figure")] +
    [Output(f"g{i}-plot", "figure") for i in range(1, 13)],
    [Input("start-decade", "value"), Input("end-decade", "value"), Input("metric-select", "value")]
)
def update_dashboard(start, end, metric):
    dff = df[(df["decade"] >= start) & (df["decade"] <= end)]
    total = len(dff)
    if total == 0: return ["0"]*20
    
    w_p = dff['white_win'].mean()
    b_p = dff['black_win'].mean()
    d_p = dff['draw'].mean()

    pie_data = dff['result'].value_counts().reset_index()
    fig_pie = px.pie(pie_data, names="result", values="count", hole=0.5, template="plotly_dark", title="Resultados")
    fig_pie.update_traces(hovertemplate='%{label}: %{percent:.2%}')
    fig_pie.update_layout(margin=dict(t=50, b=50, l=20, r=20))
    
    bar_data = dff.groupby("decade").size().reset_index(name="count")
    fig_bar = px.bar(bar_data, x="decade", y="count", template="plotly_dark", title="Partidas/Década")
    fig_bar.update_traces(hovertemplate='Década %{x}<br>Total: %{y}')
    fig_bar.update_layout(margin=dict(t=50, b=50, l=20, r=20))

    sb_data = dff.groupby(['w1', 'b1', 'w2']).size().reset_index(name='count').sort_values("count", ascending=False).head(50)
    fig_sunburst = px.sunburst(sb_data, path=['w1', 'b1', 'w2'], values='count', template="plotly_dark", title="Árvore de Lances")
    fig_sunburst.update_layout(margin=dict(t=50, b=50, l=20, r=20))

    def build_line(col, title):
        sub = dff[dff[col].notna()]
        if sub.empty: return px.line(title=title, template="plotly_dark")
        
        if metric == "freq":
            counts = sub.groupby(["decade", col]).size().reset_index(name="v")
            totals = counts.groupby("decade")["v"].transform("sum")
            counts["v"] = counts["v"] / totals
            y_format = "%{y:.2%}"
            y_axis_format = ".2%"
        else:
            counts = sub.groupby(["decade", col])[metric].mean().reset_index(name="v")
            y_format = "%{y:.2f}"
            y_axis_format = ".2f"
            
        cat_order = counts.groupby(col)["v"].sum().sort_values(ascending=False).index.tolist()
            
        fig = px.line(counts, x="decade", y="v", color=col, title=title, markers=True, 
                      template="plotly_dark", category_orders={col: cat_order})
        
        fig.update_traces(hovertemplate=y_format)
        
        fig.update_layout(
            margin=dict(t=50, b=80, l=20, r=20),
            legend=dict(orientation="h", yanchor="top", y=-0.15, title=""),
            hovermode="x unified",
            yaxis_tickformat=y_axis_format,
            xaxis_title="Década",
            yaxis_title=""
        )
        
        fig.update_xaxes(tickformat="d", hoverformat="d")
        
        for trace in fig.data:
            if "Other" in str(trace.name) or "Outros" in str(trace.name):
                trace.visible = "legendonly"
                
        return fig

    line_figs = [build_line(f"g{i}", TITLES[f"g{i}"]) for i in range(1, 13)]
    
    return (f"{total:,}", f"{w_p:.2%}", f"{b_p:.2%}", f"{d_p:.2%}", fig_pie, fig_bar, fig_sunburst, *line_figs)

if __name__ == "__main__":
    app.run(debug=True)