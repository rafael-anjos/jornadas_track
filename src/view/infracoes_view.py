import customtkinter as ctk
from tkinter import ttk
from config.theme import BG, SURFACE, BORDER, ACCENT, TEXT, SUBTEXT, DANGER
from service.infraction_service import TODOS_TIPOS

_IDX_NOME = 0
_IDX_TIPO = 2

_COLS   = ["Funcionário", "Data", "Tipo", "Descrição"]
_WIDTHS = [200, 100, 110, 500]

class InfracoesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._todos_os_dados: list[tuple] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_ui()
        self._mostrar_estado_vazio()

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
            header, text="Infrações",
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
            bar, text="Tipo:",
            font=ctk.CTkFont(size=12), text_color=SUBTEXT,
        ).pack(side="left", padx=(0, 4))

        self._filtro_tipo = ctk.CTkComboBox(
            bar,
            values=["Todos"] + TODOS_TIPOS,
            width=140, font=ctk.CTkFont(size=12),
            command=lambda _: self._aplicar_filtros(),
        )
        self._filtro_tipo.set("Todos")
        self._filtro_tipo.pack(side="left", padx=(0, 16), pady=12)

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
            "Infracoes.Treeview",
            background=SURFACE, foreground=TEXT, rowheight=30,
            fieldbackground=SURFACE, font=("Helvetica", 11), borderwidth=0,
        )
        style.configure(
            "Infracoes.Treeview.Heading",
            background=BG, foreground=SUBTEXT,
            font=("Helvetica", 10, "bold"), relief="flat",
        )
        style.map(
            "Infracoes.Treeview",
            background=[("selected", "#FFE0E0")],
            foreground=[("selected", DANGER)],
        )

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            container, columns=_COLS, show="headings",
            style="Infracoes.Treeview", selectmode="browse",
        )

        for col, w in zip(_COLS, _WIDTHS):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=60)
        self.tree.column("Funcionário", anchor="w", width=200)
        self.tree.column("Descrição",   anchor="w", width=500)

        self.tree.tag_configure("Jornada",      background="#FFF3E0", foreground="#7B3F00")
        self.tree.tag_configure("Refeição",     background="#FEF9E7", foreground="#7D6608")
        self.tree.tag_configure("Extra",        background="#FEE8E8", foreground="#C0392B")
        self.tree.tag_configure("Disposição",   background="#F3E5F5", foreground="#6A1B9A")
        self.tree.tag_configure("Interjornada", background="#EBF0FF", foreground="#2B4DB3")
        self.tree.tag_configure("par",          background="#F9F8F5")
        self.tree.tag_configure("impar",        background=SURFACE)

        vsb = ttk.Scrollbar(container, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

    def _aplicar_filtros(self) -> None:
        termo = self._entry_nome.get().strip().lower()
        tipo  = self._filtro_tipo.get()
        filtrado = [
            r for r in self._todos_os_dados
            if (not termo or termo in r[_IDX_NOME].lower()) and
               (tipo == "Todos" or r[_IDX_TIPO] == tipo)
        ]
        self._renderizar(filtrado)

    def _limpar_filtros(self) -> None:
        self._entry_nome.delete(0, "end")
        self._filtro_tipo.set("Todos")
        self._renderizar(self._todos_os_dados)

    def _renderizar(self, rows: list[tuple]) -> None:
        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = r[_IDX_TIPO] if r[_IDX_TIPO] in TODOS_TIPOS else ("par" if i % 2 == 0 else "impar")
            self.tree.insert("", "end", values=r, tags=(tag,))
        self._lbl_count.configure(text=f"{len(rows)} registros")

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
