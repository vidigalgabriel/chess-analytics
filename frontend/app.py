import pandas as pd
from dash import Dash, dcc, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("../chess_analysis/data/final_dataset.csv")
df["decade"] = (df["year"] // 10) * 10

def first_move(op):
    op=str(op)
    if "e4" in op: return "e4"
    if "d4" in op: return "d4"
    if "c4" in op or "English" in op: return "c4"
    if "Nf3" in op: return "Nf3"
    return "Other"

def vs_e4(op):
    op=str(op)
    if "e5" in op: return "e5"
    if "c5" in op or "Sicilian" in op: return "c5"
    if "c6" in op or "Caro" in op: return "c6"
    if "e6" in op or "French" in op: return "e6"
    return "Other"

def vs_d4(op):
    op=str(op)
    if "d5" in op: return "d5"
    if "Nf6" in op or "Indian" in op: return "Nf6"
    return "Other"

def e4e5(op):
    op=str(op)
    if "Ruy Lopez" in op: return "Ruy Lopez"
    if "Italian" in op: return "Italian"
    if "Scotch" in op: return "Scotch"
    if "e4 e5" in op: return "Other"
    return None

def sic2(op):
    op=str(op)
    if "Sicilian" not in op: return None
    if "d6" in op: return "d6"
    if "e6" in op: return "e6"
    if "Nc6" in op: return "Nc6"
    if "g6" in op: return "g6"
    return "Other"

def sic_open(op):
    op=str(op)
    if "Sicilian" not in op: return None
    if "Najdorf" in op: return "Najdorf"
    if "Classical" in op: return "Classical"
    if "Scheveningen" in op: return "Scheveningen"
    if "Dragon" in op and "Accelerated" not in op: return "Dragon"
    if "Sveshnikov" in op: return "Sveshnikov"
    if "Taimanov" in op or "Kan" in op: return "Taimanov/Kan"
    if "Accelerated Dragon" in op: return "Accelerated Dragon"
    return "Other"

def french(op):
    op=str(op)
    if "French" not in op: return None
    if "Classical" in op: return "Classical"
    if "Tarrasch" in op: return "Tarrasch"
    if "Advance" in op: return "Advance"
    if "Exchange" in op: return "Exchange"
    return "Other"

def caro(op):
    op=str(op)
    if "Caro" not in op: return None
    if "Classical" in op: return "Classical"
    if "Advance" in op: return "Advance"
    if "Exchange" in op: return "Exchange"
    return "Other"

def d4sys(op):
    op=str(op)
    if "Nimzo" in op: return "Nimzo"
    if "QGD" in op or "Queen" in op: return "QGD"
    if "QGA" in op: return "QGA"
    if "King's Indian" in op: return "KID"
    if "Grunfeld" in op: return "Grunfeld"
    if "Slav" in op: return "Slav"
    return "Other"

df["first"]=df["opening"].apply(first_move)
df["e4"]=df["opening"].apply(vs_e4)
df["d4r"]=df["opening"].apply(vs_d4)
df["e4e5"]=df["opening"].apply(e4e5)
df["sic2"]=df["opening"].apply(sic2)
df["sicopen"]=df["opening"].apply(sic_open)
df["french"]=df["opening"].apply(french)
df["caro"]=df["opening"].apply(caro)
df["d4sys"]=df["opening"].apply(d4sys)

def stats(df,col):
    g=df.groupby(["decade",col]).agg(
        games=("result","count"),
        w=("result",lambda x:(x=="1-0").sum()),
        b=("result",lambda x:(x=="0-1").sum()),
        d=("result",lambda x:(x=="1/2-1/2").sum())
    ).reset_index()
    g["freq"]=g["games"]/g.groupby("decade")["games"].transform("sum")*100
    g["wr"]=g["w"]/g["games"]*100
    g["br"]=g["b"]/g["games"]*100
    g["dr"]=g["d"]/g["games"]*100
    g["score"]=(g["w"]+0.5*g["d"])/g["games"]*100
    return g

maps={
"first":stats(df,"first"),
"e4":stats(df,"e4"),
"d4r":stats(df,"d4r"),
"e4e5":stats(df,"e4e5"),
"sic2":stats(df,"sic2"),
"sicopen":stats(df,"sicopen"),
"french":stats(df,"french"),
"caro":stats(df,"caro"),
"d4sys":stats(df,"d4sys"),
}

titles=[
"First Move",
"vs e4",
"vs d4",
"e4 e5",
"Sicilian move 2",
"Sicilian Open",
"French",
"Caro-Kann",
"d4 systems"
]

cols=list(maps.keys())
decades=sorted(df["decade"].unique())

games_year=df.groupby("year").size().reset_index(name="games")

app=Dash(__name__)

def fig(s,col,metric,title):
    f=go.Figure()
    for n,sub in s.groupby(col):
        f.add_trace(go.Scatter(x=sub["decade"],y=sub[metric],mode="lines",name=n))
    f.update_layout(template="plotly_dark",height=300,title=title)
    return f

app.layout=dmc.MantineProvider(
theme={"colorScheme":"dark","primaryColor":"violet"},
children=dmc.AppShell(
navbar={"width":320},
children=[
dmc.AppShellNavbar(
p="lg",
style={"background":"#0f172a","borderRight":"1px solid #1e293b"},
children=[
dmc.Title("Chess Dashboard",order=2),
dmc.Space(h=30),
dmc.Text("Decades",size="sm"),
dmc.RangeSlider(id="dec",min=0,max=len(decades)-1,value=[0,len(decades)-1]),
dmc.Space(h=25),
dmc.Text("Metric",size="sm"),
dmc.SegmentedControl(
id="metric",
value="freq",
data=[
{"label":"Freq","value":"freq"},
{"label":"Score","value":"score"},
{"label":"Draw","value":"dr"},
{"label":"White","value":"wr"},
{"label":"Black","value":"br"},
])
]),
dmc.AppShellMain(
dmc.Container(
fluid=True,
children=[
dmc.Grid([
dmc.GridCol(dmc.Paper(dcc.Graph(figure=px.line(games_year,x="year",y="games",template="plotly_dark")),p="md"),span=12),
]),
dmc.Space(h=20),
dmc.Grid([
dmc.GridCol(dmc.Paper(dcc.Graph(id=f"g{i}"),p="md"),span=4)
for i in range(len(cols))
])
]
)
)
]
)
)

@app.callback(
[Output(f"g{i}","figure") for i in range(len(cols))],
Input("dec","value"),
Input("metric","value")
)
def update(r,m):
    start=decades[r[0]]
    end=decades[r[1]]
    figs=[]
    for c,t in zip(cols,titles):
        s=maps[c]
        s=s[(s["decade"]>=start)&(s["decade"]<=end)]
        figs.append(fig(s,c,m,t))
    return figs

if __name__=="__main__":
    app.run(debug=False)