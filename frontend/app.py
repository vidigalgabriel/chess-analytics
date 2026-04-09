import pandas as pd
from dash import Dash, dcc, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("../chess_analysis/data/final_dataset.csv")
df["decade"] = (df["year"] // 10) * 10

def norm_e4e5(op):
    op = str(op)
    if op in ["Ruy Lopez", "Italian Game", "Scotch Game"]:
        return op
    if "Open Game" in op or op.startswith("e4 e5"):
        return "Other"
    return None

def norm_sic2(op):
    op = str(op)
    if "Sicilian" not in op:
        return None
    if "Najdorf" in op or "d6" in op:
        return "d6"
    if "Taimanov" in op or "Kan" in op or "e6" in op:
        return "e6"
    if "Classical" in op or "Nc6" in op or "Sveshnikov" in op:
        return "Nc6"
    if "Dragon" in op or "g6" in op:
        return "g6"
    return "Other"

def norm_sic_open(op):
    op = str(op)
    if "Sicilian" not in op:
        return None
    if "Najdorf" in op:
        return "Najdorf"
    if "Scheveningen" in op or "Scheveninguen" in op:
        return "Scheveningen"
    if "Sveshnikov" in op:
        return "Sveshnikov"
    if "Dragon" in op and "Accelerated" not in op:
        return "Dragon"
    if "Accelerated Dragon" in op:
        return "Accelerated Dragon"
    if "Classical" in op:
        return "Classical"
    if "Taimanov" in op or "Kan" in op:
        return "Taimanov/Kan"
    return "Other"

def norm_french(op):
    op = str(op)
    if "French" not in op:
        return None
    if "Advance" in op:
        return "Advance"
    if "Tarrasch" in op:
        return "Tarrasch"
    if "Exchange" in op:
        return "Exchange"
    if "Classical" in op:
        return "Classical"
    return "Other"

def norm_caro(op):
    op = str(op)
    if "Caro" not in op:
        return None
    if "Advance" in op:
        return "Advance"
    if "Exchange" in op:
        return "Exchange"
    if "Classical" in op:
        return "Classical"
    return "Other"

def norm_d4(op):
    op = str(op)
    if "Queen" in op or "QGD" in op:
        return "QGD"
    if "QGA" in op:
        return "QGA"
    if "Slav" in op:
        return "Slav"
    if "Nimzo" in op:
        return "Nimzo"
    if "King's Indian" in op:
        return "KID"
    if "Grunfeld" in op:
        return "Grunfeld"
    return None

df["e4e5"] = df["opening"].apply(norm_e4e5)
df["sic2"] = df["opening"].apply(norm_sic2)
df["sic_open"] = df["opening"].apply(norm_sic_open)
df["french"] = df["opening"].apply(norm_french)
df["caro"] = df["opening"].apply(norm_caro)
df["d4"] = df["opening"].apply(norm_d4)

def stats(df, col):
    g = (
        df[df[col].notna()]
        .groupby(["decade", col])
        .agg(
            games=("result", "count"),
            white_wins=("result", lambda x: (x == "1-0").sum()),
            black_wins=("result", lambda x: (x == "0-1").sum()),
            draws=("result", lambda x: (x == "1/2-1/2").sum()),
        )
        .reset_index()
    )
    g["white_winrate"] = g["white_wins"] / g["games"] * 100
    g["black_winrate"] = g["black_wins"] / g["games"] * 100
    g["drawrate"] = g["draws"] / g["games"] * 100
    g["avg_score"] = (g["white_wins"] + 0.5 * g["draws"]) / g["games"] * 100
    return g

stats_map = {
    "e4e5": stats(df, "e4e5"),
    "sic2": stats(df, "sic2"),
    "sic_open": stats(df, "sic_open"),
    "french": stats(df, "french"),
    "caro": stats(df, "caro"),
    "d4": stats(df, "d4"),
}

games_decade = df.groupby("decade").size().reset_index(name="games")
results_dist = df["result"].value_counts().reset_index()
results_dist.columns = ["result", "count"]
top_openings = df["opening"].value_counts().head(10).reset_index()
top_openings.columns = ["opening", "count"]

app = Dash(__name__)

titles = ["e4 e5","Sicilian move 2","Sicilian Open","French","Caro-Kann","d4 Systems"]
cols = ["e4e5","sic2","sic_open","french","caro","d4"]

decades = sorted(df["decade"].unique())

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark", "primaryColor": "cyan"},
    children=dmc.Container(
        size="lg",
        children=[
            dmc.Stack(
                gap="lg",
                children=[
                    dmc.Paper(
                        p="xl",
                        radius="xl",
                        shadow="xl",
                        children=[
                            dmc.Title("Chess Openings Intelligence", order=1),
                            dmc.Text("Large scale analysis of chess openings across decades. Explore how strategies evolved, which openings dominate, and performance trends for each variation."),
                        ],
                    ),
                    dmc.Paper(
                        p="xl",
                        radius="xl",
                        shadow="md",
                        children=[
                            dmc.Text("Select Decade Range"),
                            dmc.RangeSlider(
                                id="decade",
                                min=0,
                                max=len(decades)-1,
                                value=[0, len(decades)-1],
                                marks=[{"value": i, "label": str(decades[i])} for i in range(len(decades))],
                                size="xl",
                            ),
                            dmc.Space(h=20),
                            dmc.Select(
                                id="metric",
                                data=[
                                    {"label": "Frequency", "value": "frequency"},
                                    {"label": "White Winrate", "value": "white_winrate"},
                                    {"label": "Black Winrate", "value": "black_winrate"},
                                    {"label": "Draw Rate", "value": "drawrate"},
                                    {"label": "Average Score", "value": "avg_score"},
                                ],
                                value="frequency",
                                size="lg",
                            ),
                        ],
                    ),
                    dmc.Stack(
                        children=[dcc.Graph(id=f"graph-{i}") for i in range(6)]
                    ),
                    dmc.Grid(
                        children=[
                            dmc.GridCol(
                                span=12,
                                children=dcc.Graph(
                                    figure=px.bar(games_decade, x="decade", y="games", title="Games per Decade")
                                ),
                            ),
                            dmc.GridCol(
                                span=6,
                                children=dcc.Graph(
                                    figure=px.pie(results_dist, names="result", values="count", title="Results Distribution")
                                ),
                            ),
                            dmc.GridCol(
                                span=6,
                                children=dcc.Graph(
                                    figure=px.bar(top_openings, x="opening", y="count", title="Top Openings")
                                ),
                            ),
                        ]
                    ),
                ]
            )
        ],
    ),
)

@app.callback(
    [Output(f"graph-{i}", "figure") for i in range(6)],
    Input("decade", "value"),
    Input("metric", "value"),
)
def update(dec_range, metric):
    figs = []
    start_dec = decades[dec_range[0]]
    end_dec = decades[dec_range[1]]

    for col, title in zip(cols, titles):
        s = stats_map[col]
        s = s[(s["decade"] >= start_dec) & (s["decade"] <= end_dec)].copy()

        freq = s.groupby("decade")["games"].transform("sum")
        s["frequency"] = (s["games"] / freq) * 100

        fig = go.Figure()

        for name, sub in s.groupby(col):
            fig.add_trace(go.Scatter(
                x=sub["decade"],
                y=sub[metric],
                mode="lines+markers",
                name=name,
                hoverinfo="skip"
            ))

        hover_x = []
        hover_y = []
        hover_text = []

        for dec in sorted(s["decade"].unique()):
            sub = s[s["decade"] == dec][[col, metric]].dropna()
            sub = sub.sort_values(by=metric, ascending=False)
            text = f"Decade {dec}"
            for _, row in sub.iterrows():
                text += f"<br>{row[col]}: {row[metric]:.2f}%"
            hover_x.append(dec)
            hover_y.append(sub[metric].max())
            hover_text.append(text)

        fig.add_trace(go.Scatter(
            x=hover_x,
            y=hover_y,
            mode="markers",
            marker=dict(size=0),
            hovertemplate="%{text}<extra></extra>",
            text=hover_text,
            showlegend=False
        ))

        fig.update_layout(
            title=title,
            template="plotly_dark",
            height=400
        )

        figs.append(fig)

    return figs

if __name__ == "__main__":
    app.run(debug=False)