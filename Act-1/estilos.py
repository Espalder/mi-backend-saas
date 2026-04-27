import tkinter as tk
from tkinter import ttk
import os, json

tema_global = {'tema': 'claro'}

def set_tema_global(tema):
    tema_global['tema'] = tema

def get_tema_global():
    return tema_global['tema']

def cargar_tema_desde_configuracion():
    if os.path.exists('configuracion.json'):
        with open('configuracion.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('tema', 'claro')
    return 'claro'

def configurar_estilos(tema='claro'):
    style = ttk.Style()
    style.theme_use('clam')
    if tema == 'oscuro':
        bg = '#23272e'
        fg = '#e6e6e6'
        accent = '#1976D2'
        entry_bg = '#2c313a'
        entry_fg = '#e6e6e6'
        button_bg = '#1976D2'
        button_fg = 'white'
        error_fg = '#F44336'
        ok_fg = '#4CAF50'
    else:
        bg = '#e6f3ff'
        fg = '#1976D2'
        accent = '#2196F3'
        entry_bg = '#f8f9fa'
        entry_fg = '#222'
        button_bg = '#4CAF50'
        button_fg = 'white'
        error_fg = '#F44336'
        ok_fg = '#4CAF50'
    style.configure('TFrame', background=bg)
    style.configure('TLabel', background=bg, foreground=fg, font=('Segoe UI', 10))
    style.configure('TButton', background=button_bg, foreground=button_fg, font=('Segoe UI', 10, 'bold'))
    style.configure('TNotebook', background=bg)
    style.configure('TNotebook.Tab', background=accent, foreground='white', font=('Segoe UI', 10, 'bold'), padding=[20, 10])
    style.map('TNotebook.Tab', background=[('selected', '#FF9800'), ('active', '#FFC107')])
    style.configure('Treeview', background=entry_bg, fieldbackground=entry_bg, foreground=entry_fg, font=('Segoe UI', 9))
    style.configure('Treeview.Heading', background=accent, foreground='white', font=('Segoe UI', 10, 'bold'))
    style.configure('TLabelframe', background=bg)
    style.configure('TLabelframe.Label', background=bg, font=('Segoe UI', 11, 'bold'), foreground=fg)
    style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg, font=('Segoe UI', 10))
    style.configure('TCombobox', fieldbackground=entry_bg, foreground=entry_fg, font=('Segoe UI', 10))
    style.configure('TSpinbox', fieldbackground=entry_bg, foreground=entry_fg, font=('Segoe UI', 10))

def get_colores_tema(tema='claro'):
    if tema == 'oscuro':
        return {
            'bg': '#23272e',
            'fg': '#e6e6e6',
            'accent': '#1976D2',
            'entry_bg': '#2c313a',
            'entry_fg': '#e6e6e6',
            'button_bg': '#1976D2',
            'button_fg': 'white',
            'error_fg': '#F44336',
            'ok_fg': '#4CAF50',
            'frame_bg': '#23272e',
            'label_bg': '#23272e',
            'label_fg': '#e6e6e6',
            'tab_bg': '#23272e',
            'tab_fg': '#e6e6e6',
        }
    else:
        return {
            'bg': '#e6f3ff',
            'fg': '#1976D2',
            'accent': '#2196F3',
            'entry_bg': '#f8f9fa',
            'entry_fg': '#222',
            'button_bg': '#4CAF50',
            'button_fg': 'white',
            'error_fg': '#F44336',
            'ok_fg': '#4CAF50',
            'frame_bg': '#e6f3ff',
            'label_bg': '#e6f3ff',
            'label_fg': '#1976D2',
            'tab_bg': '#e6f3ff',
            'tab_fg': '#1976D2',
        } 