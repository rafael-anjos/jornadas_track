from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, font as tkfont

_C_GREEN  = "#22723A"
_C_LGREEN = "#2E9E52"
_C_BG     = "#F5F5F5"
_C_WHITE  = "#FFFFFF"
_C_GRAY   = "#888888"
_C_DARK   = "#2C2C2C"
_C_BORDER = "#DCDCDC"
_C_ERROR  = "#C0392B"


class _FilePickerWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.result: str | None = None

        self.title("JornadaTrack — Selecionar planilha")
        self.resizable(False, False)
        self.configure(bg=_C_BG)
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        w, h = 500, 300
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self._build()

    def _build(self) -> None:
        banner = tk.Frame(self, bg=_C_GREEN, height=72)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(
            banner, text="⏱  JornadaTrack",
            font=("Segoe UI", 17, "bold"),
            bg=_C_GREEN, fg=_C_WHITE,
        ).place(x=20, y=10)
        tk.Label(
            banner, text="Selecione a planilha de jornadas para importar",
            font=("Segoe UI", 9),
            bg=_C_GREEN, fg="#C8EED5",
        ).place(x=22, y=46)

        body = tk.Frame(self, bg=_C_BG, padx=24)
        body.pack(fill="both", expand=True)

        tk.Label(
            body, text="Arquivo (.xlsx):",
            font=("Segoe UI", 9, "bold"),
            bg=_C_BG, fg=_C_DARK,
        ).pack(anchor="w", pady=(20, 4))

        row = tk.Frame(body, bg=_C_BG)
        row.pack(fill="x")

        self._path_var = tk.StringVar()
        self._entry = tk.Entry(
            row, textvariable=self._path_var,
            font=("Segoe UI", 9),
            bg=_C_WHITE, fg=_C_DARK,
            relief="flat",
            highlightthickness=1,
            highlightbackground=_C_BORDER,
            highlightcolor=_C_GREEN,
        )
        self._entry.pack(side="left", fill="x", expand=True, ipady=5)

        tk.Button(
            row, text="  Procurar…  ",
            font=("Segoe UI", 9),
            bg="#DCDCDC", fg=_C_DARK,
            relief="flat", cursor="hand2",
            activebackground="#C8C8C8",
            command=self._browse,
        ).pack(side="left", padx=(8, 0), ipady=5)

        self._lbl_error = tk.Label(
            body, text="",
            font=("Segoe UI", 8, "italic"),
            bg=_C_BG, fg=_C_ERROR,
        )
        self._lbl_error.pack(anchor="w", pady=(4, 0))

        tk.Label(
            body,
            text="Formatos aceitos: .xlsx  •  A planilha deve seguir o layout padrão do sistema.",
            font=("Segoe UI", 8),
            bg=_C_BG, fg=_C_GRAY,
            wraplength=452, justify="left",
        ).pack(anchor="w", pady=(8, 0))

        tk.Frame(self, bg=_C_BORDER, height=1).pack(fill="x")
        foot = tk.Frame(self, bg=_C_BG, padx=16, pady=10)
        foot.pack(fill="x")

        self._btn_open = tk.Button(
            foot, text="  Abrir  ",
            font=("Segoe UI", 9, "bold"),
            bg=_C_GREEN, fg=_C_WHITE,
            relief="flat", cursor="hand2",
            activebackground=_C_LGREEN, activeforeground=_C_WHITE,
            command=self._on_open,
        )
        self._btn_open.pack(side="right", ipady=5, ipadx=8)

        tk.Button(
            foot, text="Cancelar",
            font=("Segoe UI", 9),
            bg="#DCDCDC", fg=_C_DARK,
            relief="flat", cursor="hand2",
            activebackground="#C8C8C8",
            command=self._on_cancel,
        ).pack(side="right", padx=(0, 8), ipady=5, ipadx=6)

    def _browse(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecionar planilha de jornadas",
            filetypes=[("Planilha Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
        )
        if path:
            self._path_var.set(path)
            self._lbl_error.config(text="")

    def _validate(self) -> bool:
        path = self._path_var.get().strip()
        if not path:
            self._lbl_error.config(text="⚠  Nenhum arquivo selecionado.")
            return False
        if not os.path.isfile(path):
            self._lbl_error.config(text="⚠  Arquivo não encontrado.")
            return False
        if not path.lower().endswith(".xlsx"):
            self._lbl_error.config(text="⚠  O arquivo deve ser no formato .xlsx")
            return False
        return True

    def _on_open(self) -> None:
        if self._validate():
            self.result = self._path_var.get().strip()
            self.destroy()

    def _on_cancel(self) -> None:
        self.result = None
        self.destroy()

def ask_xlsx_file() -> str | None:
    win = _FilePickerWindow()
    win.mainloop()
    return win.result
