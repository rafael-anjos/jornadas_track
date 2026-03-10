import customtkinter as ctk
from tkinter import ttk
from config.theme import BG, SURFACE, BORDER, ACCENT, TEXT, SUBTEXT

_IDX_NOME   = 0
_IDX_STATUS = 2

_TAGS_STATUS: dict[str, str] = {
    "Folga":     "folga",
    "Férias":    "ferias",
    "Atestado":  "atestado",
    "Falta":     "falta",
    "Afastado":  "afastado",
}

_COLS = [
    "Funcionário", "Data", "Status", "Início", "Fim",
    "Total", "Direção", "Disp.", "Trab. Ef.", "Interjornada",
    "Extra (h)", "Adc. Not.", "Diária",
    "Desloc. (km)", "Vel. Média", "Infrações",
]
_WIDTHS = [160, 90, 90, 70, 70, 65, 70, 65, 80, 100, 80, 75, 65, 90, 80, 80]

class JornadasView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.controller:      object      = None
        self._todos_os_dados: list[tuple] = []
        self._nomes:          list[str]   = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_ui()
        self._mostrar_estado_vazio()

    def set_controller(self, controller) -> None:
        self.controller = controller

    def _build_ui(self) -> None:
        panel = ctk.CTkFrame(
            self, fg_color=SURFACE, corner_radius=10,
            border_width=1, border_color=BORDER,
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        self._build_header(panel)
        self._build_filters(panel)
        self._build_table(panel)

    def _build_header(self, parent) -> None:
        header = ctk.CTkFrame(parent, fg_color="transparent", height=44)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="Jornadas",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT,
        ).pack(side="left")

        self._lbl_count = ctk.CTkLabel(
            header, text="0 registros",
            font=ctk.CTkFont(size=11), text_color=SUBTEXT,
        )
        self._lbl_count.pack(side="left", padx=12)

    def _build_filters(self, parent) -> None:
        bar = ctk.CTkFrame(parent, fg_color=BG, corner_radius=0, height=52)
        bar.grid(row=1, column=0, sticky="ew")
        bar.grid_propagate(False)

        ctk.CTkLabel(
            bar, text="Funcionário:",
            font=ctk.CTkFont(size=12), text_color=SUBTEXT,
        ).pack(side="left", padx=(16, 4), pady=12)

        self._entry_nome = ctk.CTkEntry(
            bar, placeholder_text="Digite o nome…",
            width=200, font=ctk.CTkFont(size=12),
        )
        self._entry_nome.pack(side="left", padx=(0, 16), pady=12)
        self._entry_nome.bind("<KeyRelease>", lambda _: self._aplicar_filtros())

        ctk.CTkLabel(
            bar, text="Status:",
            font=ctk.CTkFont(size=12), text_color=SUBTEXT,
        ).pack(side="left", padx=(0, 4))

        self._filtro_status = ctk.CTkComboBox(
            bar,
            values=["Todos", "Trabalhou", "Folga", "Férias", "Atestado", "Falta", "Afastado"],
            width=140, font=ctk.CTkFont(size=12),
            command=lambda _: self._aplicar_filtros(),
        )
        self._filtro_status.set("Todos")
        self._filtro_status.pack(side="left", padx=(0, 16), pady=12)

        ctk.CTkButton(
            bar, text="Limpar filtros", width=110, height=30,
            font=ctk.CTkFont(size=12), fg_color="transparent",
            border_width=1, border_color=BORDER,
            text_color=SUBTEXT, hover_color=BG,
            command=self._limpar_filtros,
        ).pack(side="left", pady=12)

    def _build_table(self, parent) -> None:
        style = ttk.Style()
        style.configure(
            "Jornadas.Treeview",
            background=SURFACE, foreground=TEXT, rowheight=30,
            fieldbackground=SURFACE, font=("Courier", 10), borderwidth=0,
        )
        style.configure(
            "Jornadas.Treeview.Heading",
            background=BG, foreground=SUBTEXT,
            font=("Helvetica", 10, "bold"), relief="flat",
        )
        style.map(
            "Jornadas.Treeview",
            background=[("selected", "#D8F3DC")],
            foreground=[("selected", ACCENT)],
        )

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            container, columns=_COLS, show="headings",
            style="Jornadas.Treeview", selectmode="browse",
        )

        for col, w in zip(_COLS, _WIDTHS):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=50)
        self.tree.column("Funcionário", anchor="w", width=160)

        # Tags de cor por status
        self.tree.tag_configure("folga",    background="#EBF0FF", foreground="#2B4DB3")
        self.tree.tag_configure("ferias",   background="#E8F5E9", foreground="#1B5E20")
        self.tree.tag_configure("atestado", background="#FEE8E8", foreground="#C0392B")
        self.tree.tag_configure("falta",    background="#FFF3E0", foreground="#7B3F00")
        self.tree.tag_configure("afastado", background="#F3E5F5", foreground="#6A1B9A")
        self.tree.tag_configure("par",      background="#F9F8F5")
        self.tree.tag_configure("impar",    background=SURFACE)

        vsb = ttk.Scrollbar(container, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

    def _aplicar_filtros(self) -> None:
        termo  = self._entry_nome.get().strip().lower()
        status = self._filtro_status.get()

        filtrado = [
            r for r in self._todos_os_dados
            if (not termo or termo in r[_IDX_NOME].lower()) and
               (status == "Todos" or r[_IDX_STATUS] == status)
        ]
        self._renderizar(filtrado)

    def _limpar_filtros(self) -> None:
        self._entry_nome.delete(0, "end")
        self._filtro_status.set("Todos")
        self._renderizar(self._todos_os_dados)

    def _renderizar(self, rows: list[tuple]) -> None:
        self.tree.delete(*self.tree.get_children())

        for i, r in enumerate(rows):
            tag = _TAGS_STATUS.get(r[_IDX_STATUS], "par" if i % 2 == 0 else "impar")
            self.tree.insert("", "end", values=r, tags=(tag,))

        self._lbl_count.configure(text=f"{len(rows)} registros")

    def popular_funcionarios(self, nomes: list[str]) -> None:
        self._nomes = nomes

    def _mostrar_estado_vazio(self) -> None:
        self._overlay = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        ctk.CTkLabel(
            self._overlay,
            text="📂",
            font=ctk.CTkFont(size=48),
            text_color=SUBTEXT,
        ).place(relx=0.5, rely=0.42, anchor="center")
        ctk.CTkLabel(
            self._overlay,
            text="Nenhuma planilha importada",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=SUBTEXT,
        ).place(relx=0.5, rely=0.52, anchor="center")
        ctk.CTkLabel(
            self._overlay,
            text="Use o botão  📂 Importar planilha  no topo da tela para carregar os dados.",
            font=ctk.CTkFont(size=11),
            text_color=SUBTEXT,
        ).place(relx=0.5, rely=0.59, anchor="center")

    def atualizar_tabela(self, rows: list[tuple]) -> None:
        if hasattr(self, "_overlay"):
            self._overlay.destroy()
            del self._overlay
        self._todos_os_dados = rows
        self._renderizar(rows)
