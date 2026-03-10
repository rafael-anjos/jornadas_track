# ⏱ JornadaTrack

Dashboard desktop para análise e fiscalização de jornadas de trabalho de motoristas, com detecção automática de infrações trabalhistas. Desenvolvido em Python com interface gráfica moderna.

---

## 📸 Visão geral

O sistema lê planilhas Excel no formato padrão da ficha de direção e apresenta três abas de análise:

- **Dashboard** — resumo consolidado por funcionário com cards de totais e tabela ordenável
- **Jornadas** — histórico detalhado de cada dia trabalhado, com filtros por nome e status
- **Infrações** — lista de todas as irregularidades detectadas automaticamente, com filtros por tipo

---

## ⚙️ Funcionalidades

- Importação de planilha `.xlsx` via botão na interface (sem caminho fixo em código)
- Detecção automática de **5 tipos de infração** por jornada:
  - **Jornada** — total de horas diárias acima de 12h
  - **Refeição** — intervalo acima de 2h ou ausente em jornadas acima de 6h
  - **Extra** — horas extras (100% + 50%) acima de 4h
  - **Disposição** — tempo em disposição acima de 8h
  - **Interjornada** — descanso entre jornadas abaixo de 11h
- Filtros por nome e status em todas as abas
- Ordenação de colunas clicáveis no Dashboard
- Estado vazio com orientação ao usuário enquanto nenhuma planilha foi importada
- Arquitetura **MVC** limpa: models, repository, service, controller e views separados

---

## 🗂️ Estrutura do projeto

```
JornadaTrack/
├── main.py                        # Entry point da aplicação
├── requirements.txt               # Dependências Python
├── JornadaTrack.spec              # Spec do PyInstaller (necessário para o instalador)
├── build_setup/                   # Ferramentas de build do instalador (uso do desenvolvedor)
│   ├── build_setup.py             # Gera o JornadaTrack_Setup.exe
│   └── setup_src/
│       └── setup_main.py          # Código do wizard de instalação
└── src/
    ├── config/
    │   └── theme.py               # Paleta de cores e constantes visuais
    ├── models/
    │   ├── employee.py            # Modelo de funcionário
    │   ├── journey.py             # Modelo de jornada diária
    │   └── stats.py               # Estatísticas de uma jornada
    ├── repository/
    │   └── employee_repository.py # Leitura do Excel via pandas
    ├── service/
    │   ├── employee_service.py    # Parsing e normalização dos dados
    │   └── infraction_service.py  # Motor de detecção de infrações
    ├── controller/
    │   └── dashboard_controller.py
    └── view/
        ├── main_view.py           # Janela principal, sidebar e topbar
        ├── dashboard_view.py      # Aba Dashboard
        ├── jornadas_view.py       # Aba Jornadas
        ├── infracoes_view.py      # Aba Infrações
        └── file_picker.py        # Diálogo de seleção de planilha
```

---

## 🚀 Instalação (usuário final — Windows)

1. Baixe o arquivo `JornadaTrack_Setup.exe`
2. O instalador fará tudo automaticamente:
   - Instala o Python 3.11 (com tkinter) se necessário
   - Instala todas as dependências
   - Gera e instala o `JornadaTrack.exe`
   - Cria atalho na Área de Trabalho
3. Clique em **Abrir agora** ao final

---

## 📋 Dependências

| Pacote | Versão | Uso |
|---|---|---|
| customtkinter | 5.2.2 | Interface gráfica moderna |
| pandas | 3.0.1 | Leitura e processamento do Excel |
| openpyxl | 3.1.5 | Engine de leitura `.xlsx` |
| pillow | 12.1.1 | Suporte a imagens no customtkinter |
| darkdetect | 0.8.0 | Detecção do tema do sistema |
| python-dateutil | 2.9.0 | Parsing de datas |

---

## 📊 Formato da planilha

A planilha deve estar no formato `.xlsx` com as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `CpfMotorista` | CPF do funcionário |
| `Funcionario` | Nome completo |
| `DataApuracao` | Data da jornada |
| `StatusFuncionario` | `""` (Trabalhou), `FOLGA`, `FERIAS`, `ATESTADO MÉDICO`, `FALTA`, `AFASTADO PELO INSS` |
| `PrimeiraLigada` | Horário de início |
| `UltimaDesligada` | Horário de fim |
| `TotalJornada` | Total de horas na jornada |
| `TotalDirecao` | Horas de direção |
| `TotalAdcNoturno` | Adicional noturno |
| `TotalDescanso` | Horas de descanso |
| `TotalExtra100` | Horas extras 100% |
| `TotalExtra50` | Horas extras 50% |
| `TotalInterjornada` | Intervalo entre jornadas |
| `TotalRefeicao` | Tempo de refeição |
| `TotalDisposicao` | Tempo em disposição |
| `TotalTrabalhoEfetivo` | Trabalho efetivo |
| `TeveDiaria` | Diária (`S`/`N`) |
| `DeslocamentoKmDia` | KM percorridos |
| `VelocidadeMedia` | Velocidade média |
| `Plantonista` | Indicador de plantonista |
| `Manobrista` | Indicador de manobrista |

---

## 🏗️ Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)**:

```
Excel (.xlsx)
     │
     ▼
EmployeeRepository        ← lê o arquivo e retorna DataFrame bruto
     │
     ▼
EmployeeService           ← converte para objetos Employee / Journey / Stats
     │
     ▼
InfractionService         ← aplica as 5 regras e retorna Infraction[]
     │
     ▼
DashboardController       ← orquestra os dados e popula as views
     │
     ├──▶ DashboardView
     ├──▶ JornadasView
     └──▶ InfracoesView
```

---

## 📄 Licença

Este projeto é de uso privado. Todos os direitos reservados.
