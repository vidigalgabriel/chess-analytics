import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_parquet("../data/dataset_processado.parquet")

for col in [f"g{i}" for i in range(1, 13)] + ['w1', 'b1', 'w2', 'result']:
    df[col] = df[col].astype('category')
df['decade'] = df['decade'].astype('int16')

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
    ]),
    html.Div([
        dcc.Loading(
            id="loading-sidebar",
            type="circle",
            color="#0dcaf0",
            children=html.Div(id="loading-output", style={"height": "50px"})
        )
    ], style={"marginTop": "auto", "textAlign": "center"})
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
    [Output(f"g{i}-plot", "figure") for i in range(1, 13)] +
    [Output("loading-output", "children")],
    [Input("start-decade", "value"), Input("end-decade", "value"), Input("metric-select", "value")]
)
def update_dashboard(start, end, metric):
    dff = df[(df["decade"] >= start) & (df["decade"] <= end)]
    total = len(dff)
    if total == 0: return ["0"]*19 + [None]
    
    w_p = dff['white_win'].mean()
    b_p = dff['black_win'].mean()
    d_p = dff['draw'].mean()

    pie_data = dff['result'].value_counts().reset_index()
    fig_pie = px.pie(pie_data, names="result", values="count", hole=0.5, template="plotly_dark", title="Resultados")
    fig_pie.update_traces(hovertemplate='%{label}: %{percent:.2%}')
    fig_pie.update_layout(margin=dict(t=50, b=50, l=20, r=20))
    
    bar_data = dff.groupby("decade", observed=True).size().reset_index(name="count")
    fig_bar = px.bar(bar_data, x="decade", y="count", template="plotly_dark", title="Partidas/Década")
    fig_bar.update_traces(hovertemplate='Década %{x}<br>Total: %{y}')
    fig_bar.update_layout(margin=dict(t=50, b=50, l=20, r=20))

    sb_data = dff.groupby(['w1', 'b1', 'w2'], observed=True).size().reset_index(name='count').sort_values("count", ascending=False).head(50)
    fig_sunburst = px.sunburst(sb_data, path=['w1', 'b1', 'w2'], values='count', template="plotly_dark", title="Árvore de Lances")
    fig_sunburst.update_layout(margin=dict(t=50, b=50, l=20, r=20))

    def build_line(col, title):
        sub = dff[dff[col].notna()]
        if sub.empty: return px.line(title=title, template="plotly_dark")
        
        if metric == "freq":
            counts = sub.groupby(["decade", col], observed=True).size().reset_index(name="v")
            totals = counts.groupby("decade", observed=True)["v"].transform("sum")
            counts["v"] = counts["v"] / totals
            y_format = "%{y:.2%}"
            y_axis_format = ".2%"
        else:
            counts = sub.groupby(["decade", col], observed=True)[metric].mean().reset_index(name="v")
            y_format = "%{y:.2f}"
            y_axis_format = ".2f"
            
        cat_order = counts.groupby(col, observed=True)["v"].sum().sort_values(ascending=False).index.tolist()
            
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
        
        fig.update_xaxes(tickformat="d", hoverformat="Década %{x}")
        
        for trace in fig.data:
            if "Other" in str(trace.name) or "Outros" in str(trace.name):
                trace.visible = "legendonly"
                
        return fig

    line_figs = [build_line(f"g{i}", TITLES[f"g{i}"]) for i in range(1, 13)]
    
    return (f"{total:,}", f"{w_p:.2%}", f"{b_p:.2%}", f"{d_p:.2%}", fig_pie, fig_bar, fig_sunburst, *line_figs, "")

if __name__ == "__main__":
    app.run(debug=False)