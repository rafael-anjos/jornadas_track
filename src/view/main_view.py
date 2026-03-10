import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from config.theme import BG, SURFACE, BORDER, ACCENT, ACCENT3, TEXT, SUBTEXT, SIDEBAR_W


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller   = None
        self._active_view = None
        self._views: dict = {}

        self.title("JornadaTrack")
        self.geometry("1280x780")
        self.minsize(1100, 680)
        self.configure(fg_color=BG)

        self._build_ui()

    def set_controller(self, controller) -> None:
        self.controller = controller

    def _build_ui(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content_area()

    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(
            self, fg_color=SURFACE, width=SIDEBAR_W,
            corner_radius=0, border_width=1, border_color=BORDER,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(2, weight=1)

        brand = ctk.CTkFrame(sidebar, fg_color=ACCENT, corner_radius=0, height=72)
        brand.grid(row=0, column=0, sticky="ew")
        brand.grid_propagate(False)
        ctk.CTkLabel(
            brand, text="⏱  JornadaTrack",
            font=ctk.CTkFont(family="Helvetica", size=15, weight="bold"),
            text_color=SURFACE,
        ).place(relx=0.5, rely=0.5, anchor="center")

        nav = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav.grid(row=1, column=0, sticky="ew", padx=12, pady=(16, 0))
        ctk.CTkLabel(
            nav, text="MENU",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=SUBTEXT,
        ).pack(anchor="w", padx=8, pady=(0, 6))

        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        nav_items = [
            ("dashboard",  "⊞  Dashboard"),
            ("jornadas",   "☰  Jornadas"),
            ("infracoes",  "⚠  Infrações"),
        ]
        for key, label in nav_items:
            btn = ctk.CTkButton(
                nav,
                text=label,
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                hover_color=ACCENT3,
                text_color=SUBTEXT,
                anchor="w",
                height=40,
                corner_radius=8,
                command=lambda k=key: self.navigate(k),
            )
            btn.pack(fill="x", pady=2)
            self._nav_buttons[key] = btn

        ctk.CTkLabel(
            sidebar, text="v1.0  ·  protótipo",
            font=ctk.CTkFont(size=10),
            text_color=SUBTEXT,
        ).grid(row=3, column=0, pady=16)

    def _build_content_area(self) -> None:
        self._content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self._content.grid(row=0, column=1, sticky="nsew")
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_rowconfigure(1, weight=1)

        topbar = ctk.CTkFrame(
            self._content, fg_color=SURFACE, height=56,
            corner_radius=0, border_width=1, border_color=BORDER,
        )
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)

        self._lbl_title = ctk.CTkLabel(
            topbar, text="Dashboard",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color=TEXT,
        )
        self._lbl_title.place(x=24, rely=0.5, anchor="w")

        self._lbl_desc = ctk.CTkLabel(
            topbar, text="Visão geral de todos os funcionários",
            font=ctk.CTkFont(size=12),
            text_color=SUBTEXT,
        )
        self._lbl_desc.place(x=170, rely=0.5, anchor="w")

        self._btn_import = ctk.CTkButton(
            topbar,
            text="📂  Importar planilha",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT3,
            text_color=SURFACE,
            height=34,
            width=170,
            corner_radius=8,
            command=self._importar,
        )
        self._btn_import.place(relx=1.0, rely=0.5, anchor="e", x=-16)

        self._lbl_arquivo = ctk.CTkLabel(
            topbar, text="",
            font=ctk.CTkFont(size=10),
            text_color=SUBTEXT,
        )
        self._lbl_arquivo.place(relx=1.0, rely=0.5, anchor="e", x=-196)

        self._view_container = ctk.CTkFrame(self._content, fg_color=BG, corner_radius=0)
        self._view_container.grid(row=1, column=0, sticky="nsew")
        self._view_container.grid_columnconfigure(0, weight=1)
        self._view_container.grid_rowconfigure(0, weight=1)

    def _importar(self) -> None:
        filepath = filedialog.askopenfilename(
            title="Selecionar planilha de jornadas",
            filetypes=[("Planilha Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
        )
        if not filepath:
            return

        try:
            self.controller.carregar(filepath)
            nome = os.path.basename(filepath)
            self.atualizar_arquivo(nome)
        except Exception as exc:
            messagebox.showerror(
                "Erro ao importar",
                f"Não foi possível carregar a planilha:\n\n{exc}",
            )

    def atualizar_arquivo(self, nome: str) -> None:
        self._lbl_arquivo.configure(text=f"📄 {nome}")
        self.title(f"JornadaTrack  —  {nome}")

    def navigate(self, key: str) -> None:
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(fg_color=ACCENT3, text_color=ACCENT)
            else:
                btn.configure(fg_color="transparent", text_color=SUBTEXT)

        titles = {
            "dashboard": ("Dashboard", "Visão geral de todos os funcionários"),
            "jornadas":  ("Jornadas",  "Todas as jornadas com filtros"),
            "infracoes": ("Infrações", "Todas as infrações detectadas"),
        }
        title, desc = titles.get(key, (key.capitalize(), ""))
        self._lbl_title.configure(text=title)
        self._lbl_desc.configure(text=desc)

        if self._active_view:
            self._active_view.grid_forget()

        self._active_view = self._views[key]
        self._active_view.grid(row=0, column=0, sticky="nsew")

    def register_views(self, views: dict) -> None:
        self._views = views
        self.navigate("dashboard")
