import axios from 'axios';
import Plotly from 'plotly.js-dist-min';
import { useEffect, useState } from 'react';
import ReactPlotly from 'react-plotly.js/factory';

const Plot = typeof ReactPlotly === "function" ? ReactPlotly(Plotly) : (ReactPlotly as any).default(Plotly);

interface DashboardData {
  kpis: { total: number; white_wins: number; black_wins: number; draws: number };
  pie: { result: string; value: number }[];
  bar: { decade: number; value: number }[];
  top_moves: { 'Lances Iniciais': string; Quantidade: number; Porcentagem: string }[];
  lines: Record<string, { decade: number; [key: string]: any; value: number }[]>;
}

const professionalStyles = `
  * { box-sizing: border-box; }
  body { 
    background-color: #14141e; 
    color: #f1f5f9; 
    font-family: 'Inter', system-ui, -apple-system, sans-serif; 
    margin: 0; 
    padding: 0; 
    overflow-x: hidden; 
  }

  .app-container {
    display: flex;
    min-height: 100vh;
  }

  .sidebar {
    width: 320px;
    background-color: #1e1e2f;
    padding: 30px 25px;
    display: flex;
    flex-direction: column;
    gap: 30px;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    z-index: 999;
    box-shadow: 4px 0 15px rgba(0,0,0,0.4);
  }

  .brand h1 { font-size: 1.5rem; font-weight: 800; margin: 0; color: #38bdf8; }
  .brand p { font-size: 0.75rem; color: #94a3b8; margin: 4px 0 0 0; text-transform: uppercase; letter-spacing: 2px; opacity: 0.6; }
  .brand hr { border-color: #4b4b63; margin-top: 1.5rem; }

  .control-item {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }

  .control-item label {
    font-weight: 700;
    font-size: 0.75rem;
    color: #f8fafc;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .range-slider-wrapper {
    position: relative;
    width: 100%;
    height: 30px;
    display: flex;
    align-items: center;
  }

  .range-track {
    position: absolute;
    width: 100%;
    height: 4px;
    background: #4b4b63;
    border-radius: 2px;
    z-index: 1;
  }

  .range-fill {
    position: absolute;
    height: 4px;
    background: #38bdf8;
    border-radius: 2px;
    z-index: 2;
  }

  .range-input {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-appearance: none;
    appearance: none;
    background: transparent;
    pointer-events: none;
    z-index: 3;
    margin: 0;
    outline: none;
  }

  .range-input::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    pointer-events: auto;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #38bdf8;
    cursor: pointer;
    box-shadow: 0 0 5px rgba(0,0,0,0.5);
    border: none;
  }

  .range-input::-moz-range-thumb {
    pointer-events: auto;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #38bdf8;
    cursor: pointer;
    box-shadow: 0 0 5px rgba(0,0,0,0.5);
    border: none;
  }

  .slider-values {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #8f8f9d;
    font-weight: 600;
  }

  .ui-input {
    background: #27293d;
    border: 1px solid #4b4b63;
    color: #f8fafc;
    padding: 12px;
    border-radius: 6px;
    outline: none;
    font-size: 0.9rem;
    width: 100%;
  }

  .ui-input:focus { border-color: #38bdf8; }

  .main-wrapper {
    flex: 1;
    margin-left: 320px;
    max-width: calc(100% - 320px);
    padding: 40px 50px;
  }

  .dashboard-card {
    background: #27293d;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
  }

  .kpi-section {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 25px;
  }

  .kpi-label { font-size: 0.7rem; color: #f8fafc; text-transform: uppercase; font-weight: 700; letter-spacing: 1.5px; opacity: 0.7; margin-bottom: 4px; }
  .kpi-value { font-size: 1.8rem; font-weight: 800; line-height: 1.1; margin: 0; }
  .text-info { color: #00f2c3; }
  .text-success { color: #28a745; }
  .text-danger { color: #fd5d93; }
  .text-warning { color: #ff8d72; }

  .divider-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 40px 0 20px 0;
    color: #f8fafc;
    border-bottom: 1px solid #4b4b63;
    padding-bottom: 10px;
  }

  .overview-grid {
    display: grid;
    grid-template-columns: 40% 1fr;
    gap: 20px;
  }

  .chart-container-standard {
    height: 400px;
    width: 100%;
  }

  .chart-container-wide {
    height: 450px;
    width: 100%;
    margin-bottom: 20px;
  }

  .data-table { width: 100%; border-collapse: collapse; margin: 0; }
  .data-table th { text-align: left; padding: 12px; color: #94a3b8; border-bottom: 1px solid #4b4b63; font-size: 0.8rem; text-transform: uppercase; }
  .data-table td { padding: 12px; border-bottom: 1px solid #4b4b63; color: #ffffff; font-size: 0.95rem; }
  .data-table tbody tr:hover td { background-color: rgba(255,255,255,0.05); }
`;

export default function App() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [minYear, setMinYear] = useState(1920);
  const [maxYear, setMaxYear] = useState(2014);
  const [metric, setMetric] = useState('freq');

  const SLIDER_MIN = 1850;
  const SLIDER_MAX = 2013;
  const getPercent = (value: number) => ((value - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN)) * 100;

  useEffect(() => {
    axios.get(`http://localhost:8000/api/dashboard?min_year=${minYear}&max_year=${maxYear}&metric=${metric}`)
      .then(res => setData(res.data));
  }, [minYear, maxYear, metric]);

  if (!data) return <div style={{ background: '#14141e', height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', color: '#38bdf8', fontSize: '1.2rem', fontFamily: 'Inter' }}>Processando dados...</div>;

  const kpiTotal = data.kpis.total;
  const getPercStr = (val: number) => kpiTotal ? `${(val / kpiTotal * 100).toFixed(1)}%` : "0%";

  const plotBaseLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#ffffff', family: 'Inter', size: 11 },
    margin: { t: 60, b: 40, l: 40, r: 40 },
    hovermode: 'x unified' as const,
    hoverlabel: { bgcolor: '#1e1e2f', font: { color: '#f8fafc', size: 12 }, bordercolor: '#4b4b63' },
    xaxis: { gridcolor: '#4b4b63', zerolinecolor: '#4b4b63', tickfont: { size: 11, color: '#94a3b8' } },
    yaxis: { gridcolor: '#4b4b63', zerolinecolor: '#4b4b63', tickfont: { size: 11, color: '#94a3b8' } }
  };

  const lineTitles = [
    "1. Evolução do Primeiro Lance (Brancas)", "2. Resposta Direta das Pretas a 1.e4", "3. Resposta Direta das Pretas a 1.d4",
    "4. Ramificações: e4 e5 Nf3 Nc6", "5. Ramificações: e4 c5 Nf3", "6. Sub-linhas da Siciliana Aberta",
    "7. Estruturas da Defesa Francesa", "8. Estruturas da Defesa Caro-Kann", "9. Variantes do Gambito da Rainha (d4 d5 c4)",
    "10. Sistemas Indianos (d4 Nf6 c4)", "11. Respostas à Abertura Inglesa", "12. Respostas à Abertura Reti"
  ];

  const generateLineTracesWithTextAnnotations = (colData: any[], colName: string) => {
    const categories = Array.from(new Set(colData.map(d => d[colName])));
    const traces: any[] = [];
    const annotations: any[] = [];
    const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'];

    categories.forEach((cat, index) => {
      const filtered = colData.filter(d => d[colName] === cat);
      if (filtered.length === 0) return;
      const color = colors[index % colors.length];

      traces.push({
        x: filtered.map(d => d.decade),
        y: filtered.map(d => d.value),
        type: 'scatter',
        mode: 'lines+markers',
        name: cat,
        line: { width: 3, shape: 'linear', color: color },
        marker: { size: 8 }
      });

      const lastPoint = filtered[filtered.length - 1];
      if (lastPoint) {
        const valStr = `${(lastPoint.value * 100).toFixed(1)}%`;
        annotations.push({
          xref: 'x', yref: 'y',
          x: lastPoint.decade, y: lastPoint.value,
          xanchor: 'left', yanchor: 'middle',
          text: ` ${cat} | ${valStr}`,
          font: { family: 'Inter, sans-serif', size: 11, color: color, weight: 'bold' },
          showarrow: false
        });
      }
    });

    return { traces, annotations };
  };

  return (
    <div className="app-container">
      <style>{professionalStyles}</style>
      
      <aside className="sidebar">
        <div className="brand">
          <h1>Chess Analytics</h1>
          <p>Analytics Platform</p>
          <hr />
        </div>
        
        <div className="control-item">
          <label>Período Analisado</label>
          <div className="range-slider-wrapper">
            <div className="range-track"></div>
            <div className="range-fill" style={{ left: `${getPercent(minYear)}%`, right: `${100 - getPercent(maxYear)}%` }}></div>
            <input type="range" className="range-input" min={SLIDER_MIN} max={SLIDER_MAX} value={minYear} onChange={e => setMinYear(Math.min(Number(e.target.value), maxYear - 1))} style={{ zIndex: 4 }} />
            <input type="range" className="range-input" min={SLIDER_MIN} max={SLIDER_MAX} value={maxYear} onChange={e => setMaxYear(Math.max(Number(e.target.value), minYear + 1))} style={{ zIndex: 5 }} />
          </div>
          <div className="slider-values">
            <span>{minYear}</span>
            <span>{maxYear}</span>
          </div>
        </div>
        
        <div className="control-item mt-4">
          <label>Métrica de Visualização</label>
          <select className="ui-input" value={metric} onChange={e => setMetric(e.target.value)}>
            <option value="freq">Frequência Relativa (%)</option>
            <option value="white_win">Vitórias Brancas (%)</option>
            <option value="black_win">Vitórias Pretas (%)</option>
            <option value="draw">Taxa de Empates (%)</option>
            <option value="score_white">Score Médio Brancas</option>
            <option value="score_black">Score Médio Pretas</option>
          </select>
        </div>
      </aside>

      <main className="main-wrapper">
        <h2 style={{ color: '#ffffff', fontWeight: 'bold', margin: '0 0 10px 0' }}>Painel de Aberturas Históricas</h2>
        <p style={{ color: '#f8fafc', opacity: 0.7, marginBottom: '30px' }}>Monitoramento estratégico de partidas entre {minYear} e {maxYear}</p>

        <section className="kpi-section">
          <div className="dashboard-card">
            <div className="kpi-label">Volume Total</div>
            <div className="kpi-value text-info">{kpiTotal.toLocaleString('pt-BR')}</div>
          </div>
          <div className="dashboard-card">
            <div className="kpi-label">Winrate Brancas</div>
            <div className="kpi-value text-success">{getPercStr(data.kpis.white_wins)}</div>
          </div>
          <div className="dashboard-card">
            <div className="kpi-label">Winrate Pretas</div>
            <div className="kpi-value text-danger">{getPercStr(data.kpis.black_wins)}</div>
          </div>
          <div className="dashboard-card">
            <div className="kpi-label">Taxa de Empates</div>
            <div className="kpi-value text-warning">{getPercStr(data.kpis.draws)}</div>
          </div>
        </section>

        <h4 className="divider-title">Visão Macro</h4>
        
        <section className="overview-grid">
          <div className="dashboard-card chart-container-standard">
            <Plot
              data={[{
                values: data.pie.map(d => d.value),
                labels: data.pie.map(d => d.result),
                type: 'pie',
                hole: 0.6,
                marker: { colors: ['#00f2c3', '#fd5d93', '#ff8d72'] },
                textinfo: 'percent',
                textfont: { size: 14, color: '#ffffff' },
                hoverinfo: 'label+value+percent'
              }]}
              layout={{ 
                ...plotBaseLayout, 
                title: { text: 'Resultados Globais', font: { color: '#ffffff', size: 16 } }, 
                showlegend: true
              }}
              useResizeHandler style={{ width: '100%', height: '100%' }}
            />
          </div>
          <div className="dashboard-card chart-container-standard">
            <Plot
              data={[{
                x: data.bar.map(d => d.decade),
                y: data.bar.map(d => d.value),
                type: 'bar',
                marker: { color: '#1d8cf8' }
              }]}
              layout={{ 
                ...plotBaseLayout, 
                title: { text: 'Densidade de Partidas por Década', font: { color: '#ffffff', size: 16 } },
                hovermode: 'closest'
              }}
              useResizeHandler style={{ width: '100%', height: '100%' }}
            />
          </div>
        </section>

        <h4 className="divider-title">Top 10 Lances Iniciais</h4>
        
        <section className="dashboard-card mb-5" style={{ padding: '10px' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '40%' }}>Notação Inicial</th>
                <th style={{ width: '30%' }}>Volume Absoluto</th>
                <th style={{ width: '30%' }}>Representatividade</th>
              </tr>
            </thead>
            <tbody>
              {data.top_moves.slice(0, 10).map((row, i) => (
                <tr key={i}>
                  <td>{row['Lances Iniciais']}</td>
                  <td>{row.Quantidade.toLocaleString('pt-BR')} partidas</td>
                  <td>{row.Porcentagem}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <h4 className="divider-title">Evolução Linear por Aberturas</h4>

        <section>
          {lineTitles.map((title, i) => {
            const chartData = generateLineTracesWithTextAnnotations(data.lines[`g${i+1}`] || [], `g${i+1}`);
            if (chartData.traces.length === 0) return null;
            return (
              <div className="dashboard-card chart-container-wide" key={i}>
                <Plot
                  data={chartData.traces as any}
                  layout={{ 
                    ...plotBaseLayout, 
                    title: { text: title, font: { color: '#ffffff', size: 16 } },
                    yaxis: { ...plotBaseLayout.yaxis, tickformat: '.2%' },
                    legend: { orientation: 'h', y: 1.05, x: 1, xanchor: 'right' },
                    annotations: chartData.annotations
                  }}
                  useResizeHandler style={{ width: '100%', height: '100%' }}
                />
              </div>
            );
          })}
        </section>

      </main>
    </div>
  );
}