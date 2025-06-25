# --- Dashboard Fiscal Pro - UI/UX Profissional ---
#
# 1. PRÉ-REQUISITO: Instale as bibliotecas (necessário apenas uma vez no seu ambiente):
#    pip install fastapi uvicorn pandas
#
# 2. Execute o servidor:
#    uvicorn main:app --reload
#
# 3. Acesse: http://127.0.0.1:8000

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from typing import Optional

app = FastAPI(
    title="Dashboard Fiscal Pro",
    description="Dashboard fiscal com visual profissional e gráficos avançados.",
    version="3.0.0",
    docs_url=None,
    redoc_url=None,
)

def load_and_process_data():
    data_lp = {
        "tributo": ["COFINS","PIS","COFINS","COFINS","IRPJ DIVIDA ATIVA","PIS","PIS","PIS","COFINS","PIS","COFINS","COFINS","PIS","PIS","PIS","COFINS","PIS","COFINS","PIS","COFINS","COFINS","PIS","PIS","PIS","PIS","COFINS","COFINS","PIS","COFINS","COFINS","PIS","COFINS","PIS","COFINS","PIS","PIS","PIS","PIS","PIS","COFINS","PIS","COFINS","PIS","COFINS","PIS","COFINS","COFINS","COFINS","PIS","PIS","COFINS","COFINS","COFINS","PIS","COFINS","COFINS","PIS","IRPJ DIVIDA ATIVA","PIS","PIS","PIS","PIS","PIS","COFINS","COFINS","COFINS","COFINS","COFINS","PIS","PIS","COFINS","COFINS","COFINS","PIS","PIS","PIS","PIS","COFINS","PIS","PIS","COFINS","PIS","PIS","COFINS","COFINS","PIS","IRPJ DIVIDA ATIVA","COFINS","COFINS","PIS","IRPJ DIVIDA ATIVA","PIS","COFINS","PIS"],
        "situacao": ["RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","PENDENTE","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","PENDENTE","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","PENDENTE","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","PENDENTE","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO","PENDENTE","RESTITUÍDO","RESTITUÍDO","RESTITUÍDO"],
        "valor": [3315.61,707.58,3767.31,4131.76,548.03,894.61,688.08,730.33,3657.39,720.91,3422.03,2921.0,627.57,553.56,976.75,3327.27,741.44,2989.73,781.72,4669.64,2724.56,577.23,498.02,933.15,732.91,4128.96,4636.63,1011.75,3175.86,4352.4,632.88,4508.06,792.43,3265.73,837.95,840.29,1034.64,997.1,832.73,2955.05,1050.71,2980.41,895.21,4306.87,647.76,4849.46,2664.13,3843.4,689.61,756.61,4624.65,3554.66,3244.74,2635.41,853.13,3800.79,3370.76,2554.85,632.86,2920.91,4602.05,932.11,5251.25,657.73,816.24,703.02,926.93,823.49,3015.99,3492.08,3320.21,3382.66,3035.7,718.38,790.25,2896.51,3878.33,3937.5,645.76,1004.6,640.25,4775.33,770.17,2863.76,4302.12,3867.53,653.46,9080.38,2290.57,4278.14,296.49,1644.09,1002.02,3647.36,496.28],
        "perdcomp": ["00756.48251.270325.1.2.04-9198","01123.20375.270325.1.2.04-8100","01478.67600.270325.1.2.04-9929","01917.88040.270325.1.2.04-3110","01977.08057.280325.1.2.04-8129","02472.31484.270325.1.2.04-7443","03138.86854.270325.1.2.04-4579","04783.25381.270325.1.2.04-1696","05196.88078.270325.1.2.04-7755","05582.40983.270325.1.2.04-9158","06294.00981.270325.1.2.04-7696","06315.17916.270325.1.2.04-3780","06495.71284.270325.1.2.04-1089","07011.86861.270325.1.2.04-7230","07645.60732.270325.1.2.04-9223","07900.99048.270325.1.2.04-0673","08248.31024.270325.1.2.04-7266","08729.87215.270325.1.2.04-3781","08862.13592.270325.1.2.04-0086","08862.41949.270325.1.2.04-9762","09057.01954.270325.1.2.04-6142","09545.07988.270325.1.2.04-2895","09692.41492.270325.1.2.04-9711","10163.37115.270325.1.2.04-4194","10532.43386.270325.1.2.04-4450","10575.56176.270325.1.2.04-7498","10753.99028.270325.1.2.04-6921","11083.55885.270325.1.2.04-0270","11145.07743.270325.1.2.04-4785","11616.83268.270325.1.2.04-7299","11777.69827.270325.1.2.04-3140","12193.78031.270325.1.2.04-8173","12402.83740.270325.1.2.04-6975","12518.06320.270325.1.2.04-2289","13082.91890.270325.1.2.04-5133","13110.82064.270325.1.2.04-1606","14122.82180.270325.1.2.04-8770","14789.79686.270325.1.2.04-5059","15089.96141.270325.1.2.04-1294","15385.58251.270325.1.2.04-9805","16400.48309.270325.1.2.04-0053","17053.72265.270325.1.2.04-0902","18255.59088.270325.1.2.04-5719","18985.13071.270325.1.2.04-0069","20305.70641.270325.1.2.04-7343","21288.20684.270325.1.2.04-7413","21618.84225.270325.1.2.04-3996","22163.29720.270325.1.2.04-9107","22419.58900.270325.1.2.04-9871","22821.85843.270325.1.2.04-4934","23378.57296.270325.1.2.04-2690","23847.28949.270325.1.2.04-4745","24259.58732.270325.1.2.04-8885","24550.32736.270325.1.2.04-1543","24631.57216.270325.1.2.04-1242","24921.95608.270325.1.2.04-6182","25531.98928.270325.1.2.04-0148","26385.04842.270325.1.2.04-9960","27841.53720.270325.1.2.04-0630","27943.34518.270325.1.2.04-1630","28446.42834.270325.1.2.04-6604","28997.32686.270325.1.2.04-8735","29271.18254.270325.1.2.04-6567","29971.88087.270325.1.2.04-4139","30108.42298.270325.1.2.04-7024","30574.78834.270325.1.2.04-7956","30942.14102.270325.1.2.04-7985","31196.56577.270325.1.2.04-5079","31267.24207.270325.1.2.04-8002","31900.91777.270325.1.2.04-7200","32445.65349.270325.1.2.04-2060","32786.31667.270325.1.2.04-4632","32952.26968.270325.1.2.04-5752","33020.10721.270325.1.2.04-5172","33472.89572.270325.1.2.04-6132","33932.39935.270325.1.2.04-2236","34097.96500.270325.1.2.04-1330","34193.10679.270325.1.2.04-0193","34243.64417.270325.1.2.04-0303","35091.60230.270325.1.2.04-4336","35139.10338.270325.1.2.04-8010","35621.39187.270325.1.2.04-9883","36134.13958.270325.1.2.04-7521","36878.31357.270325.1.2.04-7907","37063.92724.270325.1.2.04-1321","37118.58002.270325.1.2.04-7200","37227.27578.270325.1.2.04-0241","38553.15842.270325.1.2.04-0071","39300.44357.270325.1.2.04-5689","40048.67925.270325.1.2.04-9491","40462.03849.270325.1.2.04-1566","40683.70404.280325.1.2.04-4087","41982.64726.270325.1.2.04-1311","42033.30830.270325.1.2.04-2881","42636.36081.270325.1.2.04-0127"]
    }
    # Garante que todas as listas tenham o mesmo tamanho
    min_len = min(len(data_lp["tributo"]), len(data_lp["situacao"]), len(data_lp["valor"]), len(data_lp["perdcomp"]))
    for key in data_lp:
        data_lp[key] = data_lp[key][:min_len]
    df_lp = pd.DataFrame(data_lp)

    data_sn = {
        "mes": ["01/2023","02/2023","03/2023","04/2023","05/2023","06/2023","08/2023","09/2023","10/2023","11/2023","12/2023"],
        "pis": [88.58,104.34,131.76,138.23,169.33,177.22,198.07,143.29,172.3,188.99,195.56],
        "cofins": [408.88,481.65,608.17,638.07,781.62,818.06,914.22,661.41,795.34,872.38,902.72],
        "processo": ["10320-722.770/2025-12","10320-722.771/2025-59","10320-722.772/2025-01","10320-722.773/2025-48","10320-722.774/2025-92","10320-722.775/2025-37","10320-722.776/2025-81","10320-722.777/2025-26","10320-722.778/2025-71","10320-722.780/2025-40","10320-722.781/2025-94"],
    }
    df_sn_raw = pd.DataFrame(data_sn)
    df_lp['regime'] = 'Lucro Presumido'
    df_sn_pis = df_sn_raw[['processo']].copy()
    df_sn_pis['tributo'] = 'PIS'
    df_sn_pis['valor'] = df_sn_raw['pis']
    df_sn_cofins = df_sn_raw[['processo']].copy()
    df_sn_cofins['tributo'] = 'COFINS'
    df_sn_cofins['valor'] = df_sn_raw['cofins']
    df_sn = pd.concat([df_sn_pis, df_sn_cofins])
    df_sn['regime'] = 'Simples Nacional'
    df_sn['situacao'] = 'PENDENTE'
    df_sn.rename(columns={'processo': 'perdcomp'}, inplace=True)
    master_df = pd.concat([df_lp, df_sn], ignore_index=True)
    master_df['valor'] = master_df['valor'].astype(float)
    return master_df.fillna('')

master_df = load_and_process_data()

@app.get("/api/processes")
def get_processes(
    regime: Optional[str] = Query(None),
    tributo: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("valor"),
    sort_dir: str = Query("desc"),
):
    df = master_df.copy()
    if regime: df = df[df['regime'] == regime]
    if tributo: df = df[df['tributo'] == tributo]
    if status: df = df[df['situacao'] == status]
    if search:
        search_lower = search.lower()
        df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_lower).any(), axis=1)]
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(sort_dir == 'asc'))
    return df.to_dict('records')

@app.get("/api/kpis")
def get_kpis(
    regime: Optional[str] = Query(None), tributo: Optional[str] = Query(None),
    status: Optional[str] = Query(None), search: Optional[str] = Query(None),
):
    df = pd.DataFrame(get_processes(regime, tributo, status, search))
    if df.empty:
        return {"total_apurado": {"valor": 0, "processos": 0}, "total_recuperado": {"valor": 0, "processos": 0}, "potencial_recuperacao": {"valor": 0, "processos": 0}, "taxa_sucesso_valor": 0}
    restituido_df = df[df['situacao'] == 'RESTITUÍDO']
    pendente_df = df[df['situacao'] == 'PENDENTE']
    total_apurado = df['valor'].sum()
    total_recuperado = restituido_df['valor'].sum()
    taxa_sucesso = (total_recuperado / total_apurado * 100) if total_apurado > 0 else 0
    return {
        "total_apurado": {"valor": total_apurado, "processos": len(df)},
        "total_recuperado": {"valor": total_recuperado, "processos": len(restituido_df)},
        "potencial_recuperacao": {"valor": pendente_df['valor'].sum(), "processos": len(pendente_df)},
        "taxa_sucesso_valor": taxa_sucesso,
    }

@app.get("/api/chart-data")
def get_chart_data(
    regime: Optional[str] = Query(None), tributo: Optional[str] = Query(None),
    status: Optional[str] = Query(None), search: Optional[str] = Query(None),
):
    df = pd.DataFrame(get_processes(regime, tributo, status, search))
    if df.empty:
        return {"tribute_chart": {"labels": [], "series": []}, "status_chart": {"labels": [], "restituido": [], "pendente": []}}
    tribute_data = df.groupby('tributo')['valor'].sum().sort_values(ascending=False)
    status_by_tribute = df.groupby(['tributo', 'situacao'])['valor'].sum().unstack(fill_value=0)
    sorted_status_by_tribute = status_by_tribute.loc[status_by_tribute.sum(axis=1).sort_values(ascending=False).index]
    return {
        "tribute_chart": {"labels": tribute_data.index.tolist(), "series": tribute_data.values.tolist()},
        "status_chart": {
            "labels": sorted_status_by_tribute.index.tolist(),
            "restituido": sorted_status_by_tribute.get('RESTITUÍDO', pd.Series(0, index=sorted_status_by_tribute.index)).tolist(),
            "pendente": sorted_status_by_tribute.get('PENDENTE', pd.Series(0, index=sorted_status_by_tribute.index)).tolist(),
        }
    }

# --- HTML Frontend Profissional ---
html_content = """
<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
    <meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Dashboard Fiscal Pro</title>
    <script src=\"https://cdn.tailwindcss.com\"></script>
    <script src=\"https://cdn.jsdelivr.net/npm/apexcharts\"></script>
    <script src=\"https://unpkg.com/lucide@0.395.0/dist/umd/lucide.js\"></script>
    <script>
      tailwind.config = {
        theme: { extend: { colors: { primary: { '50': '#f6f7f5', '100': '#e9ebe8', '200': '#d3d8cf', '300': '#bdc5b7', '400': '#a6b29e', '500': '#90a086', '600': '#73806b', '700': '#566050', '800': '#3a4036', '900': '#1d201b', '950': '#0e100d' }, moss: { 'DEFAULT': '#73806b', 'dark': '#566050', 'light': '#a6b29e' }}}}
      }
    </script>
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"><link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin><link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap\" rel=\"stylesheet\">
    <style>
        body { font-family: 'Inter', sans-serif; background: linear-gradient(120deg, #f6f7f5 0%, #e9ebe8 100%); }
        .card { box-shadow: 0 4px 24px 0 rgba(86,96,80,0.08); border-radius: 1.2rem; }
        .kpi-label { color: #566050; font-weight: 600; }
        .kpi-value { font-size: 2.5rem; font-weight: 800; color: #566050; }
        .kpi-sub { color: #a6b29e; font-size: 1rem; }
        .apexcharts-tooltip { background: #566050 !important; color: #fff !important; border-radius: 8px !important; }
        .apexcharts-tooltip-title { border-bottom: 1px solid #a6b29e !important; }
        .btn-moss { background: #73806b; color: #fff; font-weight: 600; border-radius: 0.7rem; transition: background 0.2s; }
        .btn-moss:hover { background: #566050; }
        .filter-select { border: 1.5px solid #a6b29e; border-radius: 0.7rem; padding: 0.5rem 1rem; }
        .table-head { background: #f6f7f5; color: #566050; font-weight: 700; }
        .table-row:hover { background: #e9ebe8; }
        @media (max-width: 900px) { .kpi-value { font-size: 1.5rem; } }
    </style>
</head>
<body class=\"text-slate-800 antialiased\">
    <div class=\"min-h-screen flex flex-col bg-primary-50\">
        <header class=\"bg-white shadow-sm py-6 px-8 flex flex-col md:flex-row items-center justify-between\">
            <div class=\"flex items-center gap-4\">
                <div class=\"bg-gradient-to-br from-primary-700 to-primary-800 p-3 rounded-xl shadow-lg\"><i data-lucide=\"bar-chart-3\" class=\"text-white w-8 h-8\"></i></div>
                <div>
                    <h1 class=\"text-2xl md:text-3xl font-extrabold text-primary-800\">Dashboard Fiscal Pro</h1>
                    <p class=\"text-primary-400 font-medium\">Visualização profissional de processos fiscais</p>
                </div>
            </div>
            <a href=\"https://github.com/jiji465/ryan\" target=\"_blank\" class=\"btn-moss px-5 py-2 mt-4 md:mt-0 flex items-center gap-2\"><i data-lucide=\"github\" class=\"w-5 h-5\"></i> GitHub</a>
        </header>
        <main class=\"flex-1 w-full max-w-7xl mx-auto px-4 py-8\">
            <section class=\"grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10\">
                <div class=\"card p-6\"><div class=\"kpi-label\">Total Geral Apurado</div><div class=\"kpi-value\" id=\"kpi-geral-valor\">R$ 0,00</div><div class=\"kpi-sub\" id=\"kpi-geral-proc\">0 processos</div></div>
                <div class=\"card p-6\"><div class=\"kpi-label\">Valor Recuperado</div><div class=\"kpi-value text-emerald-600\" id=\"kpi-recuperado-valor\">R$ 0,00</div><div class=\"kpi-sub\" id=\"kpi-recuperado-proc\">0 processos</div></div>
                <div class=\"card p-6\"><div class=\"kpi-label\">Potencial de Recuperação</div><div class=\"kpi-value text-amber-600\" id=\"kpi-potencial-valor\">R$ 0,00</div><div class=\"kpi-sub\" id=\"kpi-potencial-proc\">0 processos</div></div>
                <div class=\"card p-6\"><div class=\"kpi-label\">Taxa de Sucesso (Valor)</div><div class=\"kpi-value text-primary-700\" id=\"kpi-success-rate\">0%</div><div class=\"kpi-sub\">(Recuperado / Total)</div></div>
            </section>
            <section class=\"grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10\">
                <div class=\"card p-6 min-h-[380px]\"><h3 class=\"text-xl font-bold text-primary-800 mb-4\">Valores por Tributo</h3><div id=\"tributeChart\"></div></div>
                <div class=\"card p-6 min-h-[380px]\"><h3 class=\"text-xl font-bold text-primary-800 mb-4\">Composição de Status por Tributo</h3><div id=\"statusChart\"></div></div>
            </section>
            <section class=\"card p-6 sm:p-8\">
                <div class=\"flex flex-col md:flex-row justify-between items-center gap-4 mb-6\">
                    <h3 class=\"text-2xl font-bold text-primary-800\">Consulta Detalhada de Processos</h3>
                    <div class=\"flex items-center gap-2 flex-wrap justify-center\">
                        <div class=\"relative\"><i data-lucide=\"search\" class=\"absolute left-3 top-1/2 -translate-y-1/2 text-primary-400 w-4 h-4\"></i><input type=\"text\" id=\"searchInput\" placeholder=\"Pesquisar...\" class=\"filter-select pl-9 pr-3 py-2 text-sm\"></div>
                        <select id=\"regimeFilter\" class=\"filter-select text-sm\"><option value=\"\">Todos Regimes</option></select>
                        <select id=\"tributoFilter\" class=\"filter-select text-sm\"><option value=\"\">Todos Tributos</option></select>
                        <select id=\"statusFilter\" class=\"filter-select text-sm\"><option value=\"\">Todas Situações</option></select>
                        <button id=\"clearFiltersBtn\" class=\"btn-moss px-4 py-2 flex items-center gap-2 text-sm\"><i data-lucide=\"rotate-ccw\" class=\"w-4 h-4\"></i> Limpar</button>
                    </div>
                </div>
                <div class=\"overflow-x-auto\"><table id=\"dataTable\" class=\"w-full text-left\"><thead class=\"table-head\"><tr><th class=\"p-4 cursor-pointer\" data-column=\"tributo\">Tributo <i data-lucide=\"arrow-up-down\" class=\"inline w-4 h-4\"></i></th><th class=\"p-4 cursor-pointer\" data-column=\"situacao\">Status <i data-lucide=\"arrow-up-down\" class=\"inline w-4 h-4\"></i></th><th class=\"p-4 cursor-pointer text-right\" data-column=\"valor\">Valor <i data-lucide=\"arrow-up-down\" class=\"inline w-4 h-4\"></i></th><th class=\"p-4 cursor-pointer\" data-column=\"regime\">Regime <i data-lucide=\"arrow-up-down\" class=\"inline w-4 h-4\"></i></th><th class=\"p-4 cursor-pointer\" data-column=\"perdcomp\">PER/DCOMP <i data-lucide=\"arrow-up-down\" class=\"inline w-4 h-4\"></i></th></tr></thead><tbody></tbody></table><div id=\"no-results\" class=\"hidden text-center p-10 text-primary-400\"><i data-lucide=\"inbox\" class=\"mx-auto w-12 h-12 mb-4 text-primary-200\"></i><p class=\"font-semibold text-lg\">Nenhum resultado encontrado.</p><p class=\"text-sm\">Tente ajustar seus filtros ou limpar a pesquisa.</p></div></div>
            </section>
        </main>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function () {
        let state = {
            sortConfig: { column: 'valor', direction: 'desc' },
            filters: { regime: '', tributo: '', status: '', search: '' },
            charts: { tributeChart: null, statusChart: null },
        };
        const formatCurrency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value || 0);
        const buildQueryString = () => {
            const params = new URLSearchParams();
            Object.entries(state.filters).forEach(([key, value]) => { if (value) params.append(key, value); });
            params.append('sort_by', state.sortConfig.column);
            params.append('sort_dir', state.sortConfig.direction);
            return params.toString();
        };
        const fetchData = async () => {
            const query = buildQueryString();
            try {
                const [kpisRes, chartDataRes, processesRes] = await Promise.all([
                    fetch(`/api/kpis?${query}`), fetch(`/api/chart-data?${query}`), fetch(`/api/processes?${query}`)
                ]);
                const [kpis, chartData, processes] = await Promise.all([kpisRes.json(), chartDataRes.json(), processesRes.json()]);
                updateAll(kpis, chartData, processes);
            } catch (error) { console.error("Erro ao buscar dados da API:", error); }
        };
        const updateKPIs = (data) => {
            document.getElementById('kpi-geral-valor').textContent = formatCurrency(data.total_apurado.valor);
            document.getElementById('kpi-geral-proc').textContent = `${data.total_apurado.processos} processos`;
            document.getElementById('kpi-recuperado-valor').textContent = formatCurrency(data.total_recuperado.valor);
            document.getElementById('kpi-recuperado-proc').textContent = `${data.total_recuperado.processos} processos`;
            document.getElementById('kpi-potencial-valor').textContent = formatCurrency(data.potencial_recuperacao.valor);
            document.getElementById('kpi-potencial-proc').textContent = `${data.potencial_recuperacao.processos} processos`;
            document.getElementById('kpi-success-rate').textContent = `${data.taxa_sucesso_valor.toFixed(1).replace('.', ',')}%`;
        };
        const updateCharts = (data) => {
            state.charts.tributeChart.updateOptions({
                series: data.tribute_chart.series,
                labels: data.tribute_chart.labels,
                colors: ['#73806b', '#a6b29e', '#566050', '#90a086', '#22c55e', '#64748b', '#3b82f6']
            });
            state.charts.statusChart.updateOptions({
                series: [
                    { name: 'Recuperado', data: data.status_chart.restituido, color: '#22c55e' },
                    { name: 'Pendente', data: data.status_chart.pendente, color: '#f59e0b' }
                ],
                xaxis: { categories: data.status_chart.labels }
            });
        };
        const populateTable = (processes) => {
            const tbody = document.querySelector('#dataTable tbody');
            const noResultsDiv = document.getElementById('no-results');
            tbody.innerHTML = '';
            if (processes.length === 0) { noResultsDiv.classList.remove('hidden'); return; }
            noResultsDiv.classList.add('hidden');
            tbody.innerHTML = processes.map(item => {
                const statusClass = item.situacao === 'RESTITUÍDO' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800';
                return `<tr class=\"table-row border-b border-primary-100\">
                    <td class=\"p-4 text-sm font-medium text-primary-900\">${item.tributo}</td>
                    <td class=\"p-4\"><span class=\"px-3 py-1 text-xs font-bold rounded-full ${statusClass}\">${item.situacao}</span></td>
                    <td class=\"p-4 text-right font-mono text-sm text-primary-700\">${formatCurrency(item.valor)}</td>
                    <td class=\"p-4 text-sm text-primary-700\">${item.regime}</td>
                    <td class=\"p-4 font-mono text-xs text-primary-400\">${item.perdcomp}</td>
                </tr>`;
            }).join('');
        };
        const updateSortIcons = () => {
            document.querySelectorAll('#dataTable th[data-column]').forEach(th => {
                const icon = th.querySelector('i[data-lucide]');
                if (icon) { icon.setAttribute('data-lucide', 'arrow-up-down'); icon.classList.remove('active'); }
            });
            const currentTh = document.querySelector(`#dataTable th[data-column="${state.sortConfig.column}"]`);
            if (currentTh) {
                const icon = currentTh.querySelector('i[data-lucide]');
                if (icon) { icon.setAttribute('data-lucide', state.sortConfig.direction === 'asc' ? 'arrow-up' : 'arrow-down'); icon.classList.add('active'); }
            }
            lucide.createIcons();
        };
        const updateAll = (kpis, chartData, processes) => { updateKPIs(kpis); updateCharts(chartData); populateTable(processes); updateSortIcons(); };
        const setupEventListeners = () => {
            document.querySelectorAll('#searchInput, #regimeFilter, #tributoFilter, #statusFilter').forEach(el => {
                el.addEventListener('input', (e) => {
                    state.filters[e.target.id.replace('Filter', '')] = e.target.value;
                    setTimeout(fetchData, 300);
                });
            });
            document.getElementById('clearFiltersBtn').addEventListener('click', () => {
                ['searchInput', 'regimeFilter', 'tributoFilter', 'statusFilter'].forEach(id => document.getElementById(id).value = '');
                state.filters = { regime: '', tributo: '', status: '', search: '' };
                fetchData();
            });
            document.querySelectorAll('#dataTable th[data-column]').forEach(th => {
                th.addEventListener('click', () => {
                    const column = th.dataset.column;
                    if (state.sortConfig.column === column) {
                        state.sortConfig.direction = state.sortConfig.direction === 'asc' ? 'desc' : 'asc';
                    } else {
                        state.sortConfig.column = column;
                        state.sortConfig.direction = 'desc';
                    }
                    fetchData();
                });
            });
        };
        const init = () => {
            const commonChartOptions = { chart: { fontFamily: 'Inter, sans-serif', toolbar: { show: false }, animations: { easing: 'easeinout', speed: 500 } }, tooltip: { theme: 'dark' } };
            state.charts.tributeChart = new ApexCharts(document.querySelector("#tributeChart"), {
                ...commonChartOptions, series: [], labels: [], chart: {...commonChartOptions.chart, type: 'donut', height: 320 },
                plotOptions: { pie: { expandOnClick: true, donut: { size: '70%', labels: { show: true, value: { formatter: (val) => formatCurrency(parseFloat(val)), fontSize: '22px', fontWeight: 700, color: '#566050'}, total: { show: true, showAlways: true, label: 'Total Apurado', fontSize: '14px', color: '#64748b', formatter: (w) => formatCurrency(w.globals.seriesTotals.reduce((a, b) => a + b, 0))} } } } },
                dataLabels: { enabled: true, formatter: (val) => `${val.toFixed(1)}%`, style: { fontSize: '12px' }, dropShadow: { enabled: false } },
                legend: { position: 'bottom', fontSize: '13px', fontWeight: 500, itemMargin: { horizontal: 8, vertical: 5 } },
                colors: ['#73806b', '#a6b29e', '#566050', '#90a086', '#22c55e', '#64748b', '#3b82f6'], stroke: { show: true, width: 4, colors: ['#ffffff'] },
            });
            state.charts.statusChart = new ApexCharts(document.querySelector("#statusChart"), {
                ...commonChartOptions, series: [], chart: { ...commonChartOptions.chart, type: 'bar', height: 320, stacked: true },
                plotOptions: { bar: { horizontal: false, columnWidth: '45%', borderRadius: 6 } },
                dataLabels: { enabled: false },
                xaxis: { categories: [], labels: { style: { colors: '#64748b', fontWeight: 500 } } },
                yaxis: { labels: { formatter: (val) => `R$${val/1000}k`, style: { colors: '#64748b' } } },
                colors: ['#22c55e', '#f59e0b'], grid: { borderColor: '#e2e8f0', strokeDashArray: 4, xaxis: { lines: { show: false } } },
                legend: { position: 'top', horizontalAlign: 'right', fontWeight: 500 },
            });
            Promise.all([state.charts.tributeChart.render(), state.charts.statusChart.render()]).then(() => {
                setupEventListeners();
                fetchData();
            });
            lucide.createIcons();
        };
        init();
    });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content
