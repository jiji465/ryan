import React, { useState, useMemo, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Sector } from 'recharts';
import { 
  AlertTriangle, 
  Building2, 
  FileText, 
  DollarSign, 
  BarChart3, 
  PieChart as PieChartIcon,
  Printer,
  Download,
  ArrowUpDown,
  TrendingUp,
  ShieldCheck,
  ShieldAlert,
  Target,
  HelpCircle
} from 'lucide-react';

// --- Dados do Relatório ---
const reportData = {
  summary: {
    totalDebt: 30725.00,
    companiesWithDebt: 3,
    companiesWithoutDebt: 3,
    urgentPayment: {
      company: 'Instituto de Fisiologia Humana LTDA',
      dueDate: '30/06/2025',
      amount: 564.19
    },
  },
  companies: [
    { name: 'AGUIAR DUARTE S. MÉDICOS LTDA', cnpj: '27.165.774/0001-29', total: 2896.67, debts: [{ name: 'CSLL Quota 2 / 1º Trim', competence: '05/2025', competenceDate: '2025-05-01', principal: 2631.91, multa: 208.44, juros: 56.32, total: 2896.67 }] },
    { name: 'AVANTGARDE CURSOS LTDA', cnpj: '37.224.203/0001-71', total: 728.13, debts: [{ name: 'PIS', competence: '04/2025', competenceDate: '2025-04-01', principal: 106.63, multa: 20.76, juros: 2.28, total: 129.67 }, { name: 'COFINS', competence: '04/2025', competenceDate: '2025-04-01', principal: 492.12, multa: 95.81, juros: 10.53, total: 598.46 }] },
    { name: 'INSTITUTO DE FISIOLOGIA HUMANA LTDA', cnpj: '37.850.045/0001-65 (a confirmar)', total: 27100.20, debts: [{ name: 'PARCELAMENTOS', competence: 'Venc. 30/06/2025', competenceDate: '2025-06-30', principal: 514.54, multa: 0, juros: 49.65, total: 564.19, urgent: true }, { name: 'COFINS', competence: '03/2025', competenceDate: '2025-03-01', principal: 21820.59, multa: 4248.46, juros: 466.96, total: 26536.01 }] }
  ],
  companiesWithoutDebt: [
      { name: 'AVANT SPA LTDA', cnpj: '45.147.037/0001-85' },
      { name: 'AVANTGARDE GROUP LTDA', cnpj: '27.721.827/0001-40' },
      { name: 'MEDFY ESTRATÉGIA E GESTÃO DE MARKETING LTDA', cnpj: '44.432.984/0001-55' },
  ]
};

const formatCurrency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);

// --- Componentes do Dashboard Aprimorados ---

const ReportHeader = () => (
    <div className="text-center mb-10 print:hidden">
        <div>
            {/* Título principal com maior peso e espaçamento ajustado para elegância */}
            <h1 className="text-4xl font-bold text-sete-navy tracking-tight">Relatório de Inteligência Fiscal</h1>
            <div className="flex items-center justify-center gap-2 text-sm text-gray-500 mt-2 font-medium">
                <ShieldCheck className="w-4 h-4 text-green-600" />
                <span>Dados atualizados em 25 de junho de 2025</span>
            </div>
        </div>
    </div>
);

const RecommendedActions = ({ topDebtor, urgentPayment }) => (
    <div className="bg-white p-6 rounded-2xl shadow-xl border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center"><Target className="mr-2 text-sete-navy" /> Ações Recomendadas</h3>
        {/* Layout ajustado para 2 colunas em telas maiores */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="bg-orange-50/50 p-4 rounded-lg border border-orange-200">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-full bg-sete-orange text-white"><AlertTriangle size={20} /></div>
                    <div><p className="font-bold text-sm text-sete-orange">Pagar Vencimento Urgente</p><p className="text-xs text-gray-600">Débito de {formatCurrency(urgentPayment.amount)} vence em {urgentPayment.dueDate}.</p></div>
                </div>
            </div>
             <div className="bg-gold-50/50 p-4 rounded-lg border border-gold-200">
                <div className="flex items-center gap-3">
                     <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-full bg-sete-gold text-white"><TrendingUp size={20} /></div>
                    <div><p className="font-bold text-sm text-sete-gold">Analisar Maior Devedor</p><p className="text-xs text-gray-600">{topDebtor.name} representa {topDebtor.percentage} da dívida.</p></div>
                </div>
            </div>
        </div>
    </div>
);

const KpiCard = ({ title, value, icon, colorName, subtitle }) => (
  <div className={`relative overflow-hidden bg-white p-6 rounded-2xl shadow-xl border border-gray-100 flex flex-col justify-between hover:-translate-y-1 transition-all duration-300`}>
    <div className={`absolute top-0 right-0 -mr-4 -mt-4 w-20 h-20 rounded-full bg-sete-${colorName}/10`}></div>
    <div className="relative z-10">
      <div className={`w-12 h-12 flex items-center justify-center rounded-lg bg-sete-${colorName}/20 text-sete-${colorName} mb-4`}>{icon}</div>
      {/* Título do KPI com peso médio para hierarquia clara */}
      <h3 className="text-base font-medium text-gray-500">{title}</h3>
      {/* Valor do KPI com peso extra-bold para impacto */}
      <p className="text-3xl font-extrabold text-gray-800 mt-1">{value}</p>
      {subtitle && <p className="text-sm text-gray-400 mt-1">{subtitle}</p>}
    </div>
  </div>
);

const DebtByCompanyChart = () => {
  const chartData = reportData.companies.map(c => ({ name: c.name.split(' ')[0], Débito: c.total })).sort((a, b) => b.Débito - a.Débito);
  return (
    <div className="bg-white p-6 rounded-2xl shadow-xl border border-gray-100 h-full">
      {/* Títulos de seção com peso semibold */}
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center"><BarChart3 className="mr-2 text-sete-navy" /> Débito por Empresa</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <XAxis type="number" tickFormatter={(v) => `R$${(v/1000).toFixed(0)}k`} tick={{ fontSize: 12, fontFamily: 'Inter' }} axisLine={false} tickLine={false} />
          <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fontFamily: 'Inter' }} axisLine={false} tickLine={false} width={80} />
          <Tooltip formatter={(v) => formatCurrency(v)} cursor={{fill: 'rgba(0, 29, 61, 0.05)'}} contentStyle={{ background: 'white', borderRadius: '0.75rem', border: '1px solid #e5e7eb', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontFamily: 'Inter' }}/>
          <Bar dataKey="Débito" radius={[0, 5, 5, 0]}>{chartData.map((e, i) => (<Cell key={`cell-${i}`} fill={i === 0 ? "var(--sete-orange)" : "var(--sete-navy)"} opacity={i === 0 ? 1 : 0.7}/>))}</Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const ActiveShape = (props) => {
  const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent } = props;
  return (
    <g>
      <text x={cx} y={cy - 10} dy={8} textAnchor="middle" fill="#333" className="font-bold text-lg">{payload.name}</text>
      <text x={cx} y={cy + 10} dy={8} textAnchor="middle" fill="#666">{`${(percent * 100).toFixed(2)}%`}</text>
      <Sector cx={cx} cy={cy} innerRadius={innerRadius} outerRadius={outerRadius + 5} startAngle={startAngle} endAngle={endAngle} fill={fill} className="drop-shadow-lg" />
    </g>
  );
};

const DebtCompositionChart = () => {
    const [activeIndex, setActiveIndex] = useState(0);
    const onPieEnter = (_, index) => setActiveIndex(index);
    const totals = reportData.companies.reduce((acc, c) => ({ principal: acc.principal + c.debts.reduce((s, d) => s + d.principal, 0), multa: acc.multa + c.debts.reduce((s, d) => s + d.multa, 0), juros: acc.juros + c.debts.reduce((s, d) => s + d.juros, 0), }), { principal: 0, multa: 0, juros: 0 });
    const chartData = [ { name: 'Principal', value: totals.principal }, { name: 'Multa', value: totals.multa }, { name: 'Juros', value: totals.juros } ];
    const COLORS = ['var(--sete-navy)', 'var(--sete-orange)', 'var(--sete-gold)'];

    return (
        <div className="bg-white p-6 rounded-2xl shadow-xl border border-gray-100 h-full">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center"><PieChartIcon className="mr-2 text-sete-navy" /> Composição da Dívida</h3>
            <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                    <Pie activeIndex={activeIndex} activeShape={ActiveShape} data={chartData} cx="50%" cy="50%" innerRadius={70} outerRadius={95} dataKey="value" onMouseEnter={onPieEnter}>
                        {chartData.map((e, i) => <Cell key={`cell-${i}`} fill={COLORS[i]} strokeWidth={2} stroke={"#fff"} style={{filter: `brightness(${activeIndex === i ? 1.05 : 0.9})`}} />)}
                    </Pie>
                    <Tooltip formatter={(v) => formatCurrency(v)} />
                </PieChart>
            </ResponsiveContainer>
             <div className="flex justify-center flex-wrap gap-x-4 gap-y-2 mt-4">
                {chartData.map((e, i) => <div key={i} onClick={() => setActiveIndex(i)} className={`flex items-center text-sm cursor-pointer p-1 rounded-md transition-all font-medium ${activeIndex === i ? 'text-gray-900' : 'text-gray-600'}`}><span className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: COLORS[i] }}></span>{e.name}</div>)}
            </div>
        </div>
    );
};

const CompanyStatusList = ({ title, companies, icon, color, showTotal = false }) => (
    <div className="bg-white p-6 rounded-2xl shadow-xl border border-gray-100 h-full">
        <h3 className={`text-lg font-semibold mb-4 flex items-center text-${color}-600`}>{icon} {title}</h3>
        <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
            {companies.map((c, i) => (
                <div key={i} className="bg-gray-50 hover:bg-white p-3 rounded-lg transition-all duration-300 group border border-gray-100 hover:shadow-md">
                    <div className="flex justify-between items-center">
                        <div>
                           {/* Nome da empresa com maior peso para destaque */}
                           <p className="font-semibold text-gray-800 text-sm">{c.name}</p>
                           <p className="text-xs text-gray-500 font-mono">{c.cnpj}</p>
                        </div>
                        {showTotal && (<p className="font-semibold text-sm text-sete-navy font-mono">{formatCurrency(c.total)}</p>)}
                    </div>
                </div>
            ))}
        </div>
    </div>
);

const SortableTableHeader = ({ column, label, sortConfig, requestSort, className }) => {
  const isSorted = sortConfig.key === column;
  return (
    <th className={`px-6 py-3 cursor-pointer hover:bg-gray-100 transition-colors ${className}`} onClick={() => requestSort(column)}>
        <div className="flex items-center gap-2"><span className="font-semibold">{label}</span><ArrowUpDown className={`w-4 h-4 transition-all ${isSorted ? 'text-sete-navy' : 'text-gray-300'}`} /></div>
    </th>
  );
};

const DebtsTable = () => {
  const [tableData, setTableData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: 'total', direction: 'descending' });
  useEffect(() => { const data = reportData.companies.flatMap(c => c.debts.map(d => ({ companyName: c.name, cnpj: c.cnpj, ...d }))); setTableData(data); }, []);
  const sortedData = useMemo(() => { let items = [...tableData]; if (sortConfig.key) { items.sort((a, b) => { if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === 'ascending' ? -1 : 1; if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === 'ascending' ? 1 : -1; return 0; }); } return items; }, [tableData, sortConfig]);
  const requestSort = (key) => { let dir = 'ascending'; if (sortConfig.key === key && sortConfig.direction === 'ascending') dir = 'descending'; setSortConfig({ key, direction: dir }); };
  
  return (
    <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center"><FileText className="mr-2 text-sete-navy" /> Detalhamento de Débitos</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-gray-500">
          {/* Cabeçalho da tabela com fontes semibold e espaçamento para elegância */}
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 tracking-wider">
            <tr className="border-b">
              <SortableTableHeader column="companyName" label="Razão Social / CNPJ" sortConfig={sortConfig} requestSort={requestSort} />
              <th className="px-6 py-3 font-semibold">Débito</th>
              <SortableTableHeader column="competenceDate" label="Competência" sortConfig={sortConfig} requestSort={requestSort} />
              <SortableTableHeader column="total" label="Total" sortConfig={sortConfig} requestSort={requestSort} className="text-right" />
            </tr>
          </thead>
          <tbody>
            {sortedData.map((d, i) => (
              <tr key={i} className={`border-b last:border-b-0 ${d.urgent ? 'bg-orange-50/50' : ''} hover:bg-gray-50/70 transition-colors`}>
                <td className="px-6 py-4"><div><p className="font-semibold text-gray-800">{d.companyName}</p><p className="text-xs text-gray-400 font-mono">{d.cnpj}</p></div></td>
                <td className="px-6 py-4"><span className={`flex items-center font-medium ${d.urgent ? 'text-sete-orange' : ''}`}>{d.name}{d.urgent && <AlertTriangle className="ml-2 w-4 h-4 animate-pulse" />}</span></td>
                <td className="px-6 py-4 font-mono text-gray-600">{d.competence}</td>
                <td className="px-6 py-4 text-right font-semibold text-gray-700 font-mono">{formatCurrency(d.total)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default function App() {
  const totalDebtsCount = reportData.companies.reduce((acc, company) => acc + company.debts.length, 0);
  const averageDebt = reportData.summary.totalDebt / totalDebtsCount;
  const topDebtor = [...reportData.companies].sort((a,b) => b.total - a.total)[0];
  const debtConcentration = (topDebtor.total / reportData.summary.totalDebt) * 100;
  
  return (
    <>
      <style>{`
        /* Importando a fonte Inter com múltiplos pesos para um controle tipográfico total */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        :root {
          --sete-navy: #001D3D;
          --sete-navy-light: #1a365d;
          --sete-orange: #F79C04;
          --sete-gold: #D4A657;
        }
        body { 
          /* Definindo a fonte base para todo o documento, garantindo coerência */
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
          background-color: #f0f4f8; 
          background-image: radial-gradient(var(--sete-navy) 0.5px, transparent 0.5px), radial-gradient(var(--sete-navy) 0.5px, #f0f4f8 0.5px);
          background-size: 20px 20px;
          background-position: 0 0, 10px 10px;
        }
        @media print {
          body { background-image: none !important; }
          .print\\:hidden { display: none; }
          .print\\:shadow-none { box-shadow: none; }
          .print\\:border-none { border: none; }
          main { padding: 0 !important; }
        }
        .text-sete-navy { color: var(--sete-navy); }
        .border-sete-navy { border-color: var(--sete-navy); }
        .border-orange-200 { border-color: rgba(253, 230, 138, 0.5); }
        .border-gold-200 { border-color: rgba(254, 243, 199, 0.5); }
        .border-navy-200 { border-color: rgba(219, 234, 254, 0.5); }
        .text-sete-orange { color: var(--sete-orange); }
        .text-sete-gold { color: var(--sete-gold); }
        .bg-sete-navy { background-color: var(--sete-navy); }
        .bg-sete-orange { background-color: var(--sete-orange); }
        .bg-sete-gold { background-color: var(--sete-gold); }
        .bg-sete-navy\\/10 { background-color: rgba(0, 29, 61, 0.1); }
        .bg-sete-navy\\/20 { background-color: rgba(0, 29, 61, 0.2); }
        .bg-orange-50\\/50 { background-color: rgba(255, 251, 235, 0.5); }
        .bg-gold-50\\/50 { background-color: rgba(254, 249, 195, 0.5); }
        .bg-navy-50\\/50 { background-color: rgba(239, 246, 255, 0.5); }
        .bg-sete-orange\\/10 { background-color: rgba(247, 156, 4, 0.1); }
        .bg-sete-orange\\/20 { background-color: rgba(247, 156, 4, 0.2); }
        .bg-sete-gold\\/10 { background-color: rgba(212, 166, 87, 0.1); }
        .bg-sete-gold\\/20 { background-color: rgba(212, 166, 87, 0.2); }
        .bg-green-600\\/10 { background-color: rgba(22, 163, 74, 0.1); }
        .bg-green-600\\/20 { background-color: rgba(22, 163, 74, 0.2); }
        .text-green-600 { color: #16a34a; }
      `}</style>
      <main className="min-h-screen p-4 sm:p-8">
        <div className="max-w-7xl mx-auto bg-gray-50/80 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/50 print:shadow-none print:border-none">
            <ReportHeader />
            <div className="space-y-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <KpiCard title="Dívida Total" value={formatCurrency(reportData.summary.totalDebt)} icon={<DollarSign size={24}/>} colorName="navy" subtitle="Soma de todos os débitos"/>
                    <KpiCard title="Vencimento Urgente" value={formatCurrency(reportData.summary.urgentPayment.amount)} icon={<AlertTriangle size={24}/>} colorName="orange" subtitle={`Vence em ${reportData.summary.urgentPayment.dueDate}`}/>
                    <KpiCard title="Concentração da Dívida" value={`${debtConcentration.toFixed(1)}%`} icon={<TrendingUp size={24}/>} colorName="gold" subtitle={`Em ${topDebtor.name.split(' ')[0]}`} />
                    <KpiCard title="Empresas com Débitos" value={`${reportData.summary.companiesWithDebt}`} icon={<Building2 size={24}/>} colorName="navy" subtitle={`${reportData.summary.companiesWithoutDebt} empresas regulares`}/>
                </div>
                <RecommendedActions topDebtor={{name: topDebtor.name, percentage: `${debtConcentration.toFixed(1)}%`}} urgentPayment={reportData.summary.urgentPayment} />
                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                    <div className="lg:col-span-3"><DebtByCompanyChart /></div>
                    <div className="lg:col-span-2"><DebtCompositionChart /></div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <CompanyStatusList title="Empresas com Pendências" companies={reportData.companies} icon={<ShieldAlert className="mr-2" />} color="orange" showTotal={true}/>
                    <CompanyStatusList title="Empresas Regulares" companies={reportData.companiesWithoutDebt} icon={<ShieldCheck className="mr-2" />} color="green-600"/>
                </div>
                <DebtsTable />
            </div>
        </div>
      </main>
    </>
  );
}
