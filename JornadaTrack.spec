# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec para JornadaTrack
# Gerado automaticamente — edite apenas se necessário.

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Coleta todos os arquivos de dados do customtkinter (temas, imagens, fontes)
ctk_datas = collect_data_files("customtkinter")

a = Analysis(
    ["main.py"],
    pathex=[str(Path("src").resolve())],
    binaries=[],
    datas=[
        # Recursos do customtkinter
        *ctk_datas,
    ],
    hiddenimports=[
        # Módulos internos do projeto
        "config.theme",
        "models.employee",
        "models.journey",
        "models.stats",
        "repository.employee_repository",
        "service.employee_service",
        "service.infraction_service",
        "controller.dashboard_controller",
        "view.main_view",
        "view.dashboard_view",
        "view.jornadas_view",
        "view.infracoes_view",
        "view.file_picker",
        # Dependências que o PyInstaller às vezes não detecta
        "customtkinter",
        "darkdetect",
        "openpyxl",
        "openpyxl.styles",
        "openpyxl.reader.excel",
        "pandas",
        "PIL",
        "PIL._tkinter_finder",
        "tkinter",
        "tkinter.ttk",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "numpy.testing", "scipy"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="JornadaTrack",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # sem janela de console — só a interface gráfica
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon="icon.ico",   # descomente e coloque seu .ico aqui se quiser ícone
)
