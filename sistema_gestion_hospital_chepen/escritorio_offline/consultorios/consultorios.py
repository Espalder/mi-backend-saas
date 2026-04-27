import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class ConsultoriosWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Consultorios Externos")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f4fa")
        self.setup_ui()
        self.load_consultorios()
        self.root.mainloop()

    def setup_ui(self):
        fuente_titulo = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        fuente_boton = tkFont.Font(family="Segoe UI", size=10)
        logo_path = os.path.join(ASSETS_PATH, "logo_hospital.png")
        ascii_logo_path = os.path.join(ASSETS_PATH, "logo_hospital_ascii.txt")
        if os.path.exists(logo_path):
            logo_img = PhotoImage(file=logo_path)
            self.logo_img = logo_img
            tk.Label(self.root, image=logo_img, bg="#f0f4fa").pack(pady=(10, 2))
        elif os.path.exists(ascii_logo_path):
            with open(ascii_logo_path, "r", encoding="utf-8") as f:
                ascii_logo = f.read()
            tk.Label(self.root, text=ascii_logo, font=("Consolas", 10), fg="#0d47a1", bg="#f0f4fa", justify="center").pack(pady=(10, 2))
        tk.Label(self.root, text="Consultorios Externos", font=fuente_titulo, bg="#f0f4fa", fg="#1a237e").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#f0f4fa")
        frame.pack(pady=5)
        tk.Label(frame, text="Especialidad:", bg="#f0f4fa").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Médico:", bg="#f0f4fa").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Paciente ID:", bg="#f0f4fa").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Fecha:", bg="#f0f4fa").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(frame, text="Diagnóstico:", bg="#f0f4fa").grid(row=2, column=0, padx=5, pady=5)
        self.especialidad_var = tk.StringVar()
        self.medico_var = tk.StringVar()
        self.paciente_id_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.diagnostico_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.especialidad_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.medico_var, width=20).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.paciente_id_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_var, width=15).grid(row=1, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.diagnostico_var, width=30).grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#f0f4fa")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_consultorio, bg="#4CAF50", fg="white", font=fuente_boton, width=12).grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_consultorio, bg="#2196F3", fg="white", font=fuente_boton, width=12).grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_consultorio, bg="#F44336", fg="white", font=fuente_boton, width=12).grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "especialidad", "medico", "paciente_id", "fecha", "diagnostico"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("especialidad", text="Especialidad")
        self.tree.heading("medico", text="Médico")
        self.tree.heading("paciente_id", text="Paciente ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("diagnostico", text="Diagnóstico")
        self.tree.column("id", width=40)
        self.tree.column("especialidad", width=120)
        self.tree.column("medico", width=120)
        self.tree.column("paciente_id", width=80)
        self.tree.column("fecha", width=90)
        self.tree.column("diagnostico", width=180)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_consultorio)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_consultorio(self):
        especialidad = self.especialidad_var.get().strip()
        medico = self.medico_var.get().strip()
        paciente_id = self.paciente_id_var.get().strip()
        fecha = self.fecha_var.get().strip()
        diagnostico = self.diagnostico_var.get().strip()
        if not especialidad or not paciente_id:
            messagebox.showwarning("Validación", "Especialidad y Paciente ID son obligatorios.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO consultorios (especialidad, medico, paciente_id, fecha, diagnostico) VALUES (?, ?, ?, ?, ?)",
                  (especialidad, medico, paciente_id, fecha, diagnostico))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_consultorios()

    def actualizar_consultorio(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione una consulta para actualizar.")
            return
        especialidad = self.especialidad_var.get().strip()
        medico = self.medico_var.get().strip()
        paciente_id = self.paciente_id_var.get().strip()
        fecha = self.fecha_var.get().strip()
        diagnostico = self.diagnostico_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE consultorios SET especialidad=?, medico=?, paciente_id=?, fecha=?, diagnostico=? WHERE id=?",
                  (especialidad, medico, paciente_id, fecha, diagnostico, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_consultorios()

    def eliminar_consultorio(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione una consulta para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta consulta?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM consultorios WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_consultorios()

    def load_consultorios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, especialidad, medico, paciente_id, fecha, diagnostico FROM consultorios")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_consultorio(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.especialidad_var.set(values[1])
        self.medico_var.set(values[2])
        self.paciente_id_var.set(values[3])
        self.fecha_var.set(values[4])
        self.diagnostico_var.set(values[5])

    def limpiar_campos(self):
        self.especialidad_var.set("")
        self.medico_var.set("")
        self.paciente_id_var.set("")
        self.fecha_var.set("")
        self.diagnostico_var.set("") 