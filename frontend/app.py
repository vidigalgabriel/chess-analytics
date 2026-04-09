import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.express as px

df = pd.read_csv("../chess_analysis/data/final_dataset.csv")
df["decade"] = (df["year"] // 10) * 10

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

stats_full = compute_stats(df)

categories = {
    "e4 e5": ["Ruy Lopez", "Italian Game", "Scotch Game", "Open Game Other", "e4 e5 Other"],
    "Sicilian": ["Najdorf", "Sicilian Classical", "Sicilian Taimanov/Kan", "Sicilian Dragon", "Sicilian d6", "Sicilian Other"],
    "French": ["French Classical", "French Tarrasch", "French Advance", "French Exchange", "French Other"],
    "Caro-Kann": ["Caro-Kann Classical", "Caro Advance", "Caro Exchange", "Caro-Kann Other"],
    "d4 Systems": ["QGD", "QGA", "Slav", "Nimzo-Indian", "Queen's Indian", "King's Indian", "Grunfeld", "Indian Other", "d4 d5 Other"]
}

app = Dash(__name__)

def create_card(title, idx):
    return dmc.Paper(
        children=[
            dmc.Group(
                [
                    dmc.Title(title, order=3),
                    dmc.Select(
                        id=f"metric-{idx}",
                        data=[
                            {"label": "Frequency", "value": "frequency"},
                            {"label": "White Winrate", "value": "white_winrate"},
                            {"label": "Black Winrate", "value": "black_winrate"},
                            {"label": "Draw Rate", "value": "drawrate"},
                            {"label": "Avg Score", "value": "avg_score"},
                        ],
                        value="frequency",
                        style={"width": 180}
                    ),
                ],
                justify="space-between",
                mb=10
            ),
            dcc.Graph(id=f"graph-{idx}")
        ],
        p="md",
        radius="md",
        shadow="sm",
        style={"backgroundColor": "white"}
    )

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=dmc.Container(
        size="xl",
        children=[
            dmc.Title("Chess Openings Dashboard", order=1, mb=20),

            dmc.Grid(
                children=[
                    dmc.GridCol(
                        span=3,
                        children=[
                            dmc.Paper(
                                children=[
                                    dmc.Title("Filters", order=4),
                                    dmc.Space(h=10),
                                    dmc.Text("Year Range"),
                                    dmc.RangeSlider(
                                        id="year-slider",
                                        min=df["year"].min(),
                                        max=df["year"].max(),
                                        value=[df["year"].min(), df["year"].max()],
                                    ),
                                ],
                                p="md",
                                radius="md",
                                shadow="sm"
                            )
                        ]
                    ),

                    dmc.GridCol(
                        span=9,
                        children=dmc.SimpleGrid(
                            cols=2,
                            spacing="lg",
                            children=[
                                create_card(name, i)
                                for i, name in enumerate(categories.keys())
                            ]
                        )
                    )
                ]
            )
        ]
    )
)

@app.callback(
    [Output(f"graph-{i}", "figure") for i in range(5)],
    [Input("year-slider", "value")] +
    [Input(f"metric-{i}", "value") for i in range(5)]
)
def update_graphs(year_range, *metrics):
    stats = stats_full[
        (stats_full["decade"] >= (year_range[0] // 10) * 10) &
        (stats_full["decade"] <= (year_range[1] // 10) * 10)
    ]

    figures = []

    for (name, openings), metric in zip(categories.items(), metrics):
        data = stats[stats["opening"].isin(openings)].copy()

        if data.empty:
            figures.append(px.line())
            continue

        top_openings = (
            data.groupby("opening")["games"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .index
        )

        data = data[data["opening"].isin(top_openings)].copy()
        freq = data.groupby("decade")["games"].transform("sum")
        data["frequency"] = (data["games"] / freq) * 100

        fig = px.line(
            data,
            x="decade",
            y=metric,
            color="opening",
            markers=True
        )

        fig.update_layout(
            template="simple_white",
            height=300,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        figures.append(fig)

    return figures

if __name__ == "__main__":
    app.run(debug=False)