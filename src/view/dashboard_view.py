import customtkinter as ctk
from tkinter import ttk
from config.theme import BG, SURFACE, BORDER, ACCENT, TEXT, SUBTEXT, DANGER

_COLS = [
    "Funcionário", "CPF", "Tipo",
    "Jornadas", "Folgas", "Férias", "Extra (h)", "Faltas", "Atestados", "Diárias", "Infrações",
]
_WIDTHS = [190, 130, 100, 90, 75, 75, 85, 75, 90, 80, 90]

_SORT_KEY: dict[str, str] = {
    "Folgas":    "folgas",
    "Extra (h)": "extras",
    "Diárias":   "diarias",
    "Infrações": "infracoes",
}

class DashboardView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._todos_os_dados: list[dict]      = []
        self._sort_col:       str | None      = None
        self._sort_asc:       bool            = True

        self._build_ui()

    def _build_ui(self) -> None:
        self._build_cards()
        self._build_filters()
        self._build_table()

    def _build_cards(self) -> None:
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 8))

        self._card_values: dict[str, ctk.CTkLabel] = {}

        cards = [
            ("funcionarios", "Funcionários",   ACCENT,  "ativos no período"),
            ("jornadas",     "Total Jornadas", TEXT,    "registros carregados"),
            ("folgas",       "Folgas",          TEXT,    "no período"),
            ("infracoes",    "Infrações",       DANGER,  "detectadas"),
        ]

        for i, (key, label, color, sub) in enumerate(cards):
            frame.grid_columnconfigure(i, weight=1)

            card = ctk.CTkFrame(
                frame, fg_color=SURFACE, corner_radius=10,
                border_width=1, border_color=BORDER,
            )
            card.grid(row=0, column=i, padx=6, sticky="ew")

            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=SUBTEXT,
            ).pack(pady=(14, 4), padx=16, anchor="w")

            lbl = ctk.CTkLabel(
                card, text="—",
                font=ctk.CTkFont(family="Courier", size=28, weight="bold"),
                text_color=color,
            )
            lbl.pack(padx=16, anchor="w")
            self._card_values[key] = lbl

            ctk.CTkLabel(
                card, text=sub,
                font=ctk.CTkFont(size=10), text_color=SUBTEXT,
            ).pack(pady=(2, 14), padx=16, anchor="w")

    def _build_filters(self) -> None:
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 6))

        ctk.CTkLabel(
            bar, text="Funcionário:",
            font=ctk.CTkFont(size=12), text_color=SUBTEXT,
        ).pack(side="left", padx=(0, 6))

        self._entry_nome = ctk.CTkEntry(
            bar, placeholder_text="Digite o nome…",
            width=220, font=ctk.CTkFont(size=12),
        )
        self._entry_nome.pack(side="left", padx=(0, 12))
        # Filtra a cada tecla pressionada
        self._entry_nome.bind("<KeyRelease>", lambda _: self._aplicar_filtro())

        ctk.CTkButton(
            bar, text="Limpar", width=80, height=30,
            font=ctk.CTkFont(size=12), fg_color="transparent",
            border_width=1, border_color=BORDER,
            text_color=SUBTEXT, hover_color=BG,
            command=self._limpar_filtro,
        ).pack(side="left")

    def _build_table(self) -> None:
        panel = ctk.CTkFrame(
            self, fg_color=SURFACE, corner_radius=10,
            border_width=1, border_color=BORDER,
        )
        panel.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            panel, text="Resumo por Funcionário",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT,
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 6))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dashboard.Treeview",
            background=SURFACE, foreground=TEXT, rowheight=32,
            fieldbackground=SURFACE, font=("Helvetica", 11), borderwidth=0,
        )
        style.configure(
            "Dashboard.Treeview.Heading",
            background=BG, foreground=SUBTEXT,
            font=("Helvetica", 10, "bold"), relief="flat",
        )
        style.map(
            "Dashboard.Treeview",
            background=[("selected", "#D8F3DC")],
            foreground=[("selected", ACCENT)],
        )

        container = ctk.CTkFrame(panel, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            container, columns=_COLS, show="headings",
            style="Dashboard.Treeview", selectmode="browse",
        )

        for col, w in zip(_COLS, _WIDTHS):
            if col in _SORT_KEY:
                self.tree.heading(col, text=col,
                                  command=lambda c=col: self._ordenar(c))
            else:
                self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=60)
        self.tree.column("Funcionário", anchor="w")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

    def _dados_filtrados(self) -> list[dict]:
        termo = self._entry_nome.get().strip().lower()
        return [
            r for r in self._todos_os_dados
            if not termo or termo in r["nome"].lower()
        ]

    def _aplicar_filtro(self) -> None:
        self._renderizar(self._dados_filtrados())

    def _limpar_filtro(self) -> None:
        self._entry_nome.delete(0, "end")
        self._sort_col = None
        self._redefinir_cabecalhos()
        self._renderizar(self._todos_os_dados)

    def _ordenar(self, col: str) -> None:
        if self._sort_col == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_col = col
            self._sort_asc = False

        chave = _SORT_KEY[col]
        dados = sorted(
            self._dados_filtrados(),
            key=lambda r: r[chave],
            reverse=not self._sort_asc,
        )
        self._renderizar(dados)
        self._redefinir_cabecalhos()

    def _redefinir_cabecalhos(self) -> None:
        for c in _SORT_KEY:
            if c == self._sort_col:
                seta = " ↑" if self._sort_asc else " ↓"
                self.tree.heading(c, text=c + seta)
            else:
                self.tree.heading(c, text=c)

    def _renderizar(self, rows: list[dict]) -> None:
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=(
                row["nome"],      row["cpf"],      row["tipo"],
                row["jornadas"],  row["folgas"],   row["ferias"],
                row["extras"],    row["faltas"],   row["atestados"],
                row["diarias"],   row["infracoes"],
            ))

    def popular_funcionarios(self, nomes: list[str]) -> None:
        pass

    def atualizar_cards(self, dados: dict) -> None:
        for key, lbl in self._card_values.items():
            lbl.configure(text=str(dados.get(key, "—")))

    def atualizar_tabela(self, rows: list[dict]) -> None:
        self._todos_os_dados = rows
        self._sort_col = None
        self._redefinir_cabecalhos()
        self._renderizar(rows)
