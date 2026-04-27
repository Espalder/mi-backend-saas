import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

# Inicialización de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'hospital.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Tablas base para cada módulo (solo estructura mínima, se puede ampliar)
    c.execute('''CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dni TEXT,
        fecha_nacimiento TEXT,
        sexo TEXT,
        direccion TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS consultorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        especialidad TEXT NOT NULL,
        medico TEXT,
        paciente_id INTEGER,
        fecha TEXT,
        diagnostico TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS emergencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha TEXT,
        motivo TEXT,
        triaje TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS hospitalizacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha_ingreso TEXT,
        fecha_egreso TEXT,
        area TEXT,
        cama TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS cirugias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        tipo TEXT,
        fecha TEXT,
        sala TEXT,
        equipo TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS farmacia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicamento TEXT,
        stock INTEGER,
        vencimiento TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS laboratorio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        tipo_examen TEXT,
        resultado TEXT,
        fecha TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS inmunizaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        vacuna TEXT,
        fecha TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS nutricion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        plan TEXT,
        fecha TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        especialidad TEXT,
        fecha TEXT,
        estado TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS administracion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        descripcion TEXT,
        fecha TEXT
    )''')
    conn.commit()
    conn.close()

# Ventanas de cada módulo (implementación básica, se puede ampliar)
def abrir_pacientes():
    from pacientes.pacientes import PacientesWindow
    PacientesWindow()

def abrir_consultorios():
    from consultorios.consultorios import ConsultoriosWindow
    ConsultoriosWindow()

def abrir_emergencias():
    from emergencias.emergencias import EmergenciasWindow
    EmergenciasWindow()

def abrir_hospitalizacion():
    from hospitalizacion.hospitalizacion import HospitalizacionWindow
    HospitalizacionWindow()

def abrir_cirugias():
    from cirugias.cirugias import CirugiasWindow
    CirugiasWindow()

def abrir_farmacia():
    from farmacia.farmacia import FarmaciaWindow
    FarmaciaWindow()

def abrir_laboratorio():
    from laboratorio.laboratorio import LaboratorioWindow
    LaboratorioWindow()

def abrir_inmunizaciones():
    from inmunizaciones.inmunizaciones import InmunizacionesWindow
    InmunizacionesWindow()

def abrir_nutricion():
    from nutricion.nutricion import NutricionWindow
    NutricionWindow()

def abrir_citas():
    from citas.citas import CitasWindow
    CitasWindow()

def abrir_administracion():
    from administracion.administracion import AdministracionWindow
    AdministracionWindow()

# Menú principal
def main():
    init_db()
    root = tk.Tk()
    root.title("Sistema de Gestión Hospitalaria - Chepén")
    root.geometry("520x700")
    root.configure(bg="#f0f4fa")  # Fondo suave

    # Fuente moderna
    fuente_titulo = tkFont.Font(family="Segoe UI", size=16, weight="bold")
    fuente_boton = tkFont.Font(family="Segoe UI", size=11)

    # Logo si existe
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo_hospital.png")
    if os.path.exists(logo_path):
        logo_img = PhotoImage(file=logo_path)
        tk.Label(root, image=logo_img, bg="#f0f4fa").pack(pady=(15, 5))
    else:
        logo_img = None

    tk.Label(
        root,
        text="Sistema de Gestión Integral para la Red Hospitalaria de Chepén",
        font=fuente_titulo,
        wraplength=480,
        pady=10,
        bg="#f0f4fa",
        fg="#1a237e"
    ).pack()
    
    # Botones ordenados alfabéticamente
    botones = [
        ("Cirugías", abrir_cirugias, "#e3f2fd"),
        ("Citas Médicas y Horarios", abrir_citas, "#ffe0b2"),
        ("Consultorios Externos", abrir_consultorios, "#e8f5e9"),
        ("Emergencias y Tópicos", abrir_emergencias, "#ffebee"),
        ("Farmacia y Esterilización", abrir_farmacia, "#f3e5f5"),
        ("Gestión Administrativa y Reportes", abrir_administracion, "#fffde7"),
        ("Gestión de Pacientes", abrir_pacientes, "#e1f5fe"),
        ("Hospitalización", abrir_hospitalizacion, "#fce4ec"),
        ("Inmunizaciones y Programas Preventivos", abrir_inmunizaciones, "#f9fbe7"),
        ("Laboratorio e Imágenes", abrir_laboratorio, "#ede7f6"),
        ("Nutrición", abrir_nutricion, "#f1f8e9"),
    ]
    botones.sort(key=lambda x: x[0])

    for texto, comando, color in botones:
        tk.Button(
            root,
            text=texto,
            width=40,
            height=2,
            command=comando,
            font=fuente_boton,
            bg=color,
            fg="#263238",
            activebackground="#90caf9",
            activeforeground="#1a237e",
            relief=tk.RAISED,
            bd=2
        ).pack(pady=6)

    tk.Button(
        root,
        text="Salir",
        width=20,
        command=root.destroy,
        bg="#d32f2f",
        fg="white",
        font=fuente_boton,
        activebackground="#b71c1c",
        relief=tk.RAISED,
        bd=2
    ).pack(pady=20)

    # Pie de página
    tk.Label(
        root,
        text="Desarrollado por tu equipo | 2024",
        font=("Segoe UI", 9),
        bg="#f0f4fa",
        fg="#607d8b"
    ).pack(side=tk.BOTTOM, pady=8)

    root.mainloop()

if __name__ == "__main__":
    main() 