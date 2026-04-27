import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class HospitalizacionWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Hospitalización")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f9ff")
        self.setup_ui()
        self.load_hospitalizaciones()
        self.root.mainloop()

    def setup_ui(self):
        fuente_titulo = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        fuente_boton = tkFont.Font(family="Segoe UI", size=10)
        logo_path = os.path.join(ASSETS_PATH, "logo_hospital.png")
        ascii_logo_path = os.path.join(ASSETS_PATH, "logo_hospital_ascii.txt")
        if os.path.exists(logo_path):
            logo_img = PhotoImage(file=logo_path)
            self.logo_img = logo_img
            tk.Label(self.root, image=logo_img, bg="#f0f9ff").pack(pady=(10, 2))
        elif os.path.exists(ascii_logo_path):
            with open(ascii_logo_path, "r", encoding="utf-8") as f:
                ascii_logo = f.read()
            tk.Label(self.root, text=ascii_logo, font=("Consolas", 10), fg="#475569", bg="#f0f9ff", justify="center").pack(pady=(10, 2))
        tk.Label(self.root, text="Hospitalización", font=fuente_titulo, bg="#f0f9ff", fg="#0ea5e9").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#f0f9ff")
        frame.pack(pady=5)
        tk.Label(frame, text="Paciente ID:", bg="#f0f9ff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Fecha Ingreso:", bg="#f0f9ff").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Fecha Egreso:", bg="#f0f9ff").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Área:", bg="#f0f9ff").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(frame, text="Cama:", bg="#f0f9ff").grid(row=2, column=0, padx=5, pady=5)
        self.paciente_id_var = tk.StringVar()
        self.fecha_ingreso_var = tk.StringVar()
        self.fecha_egreso_var = tk.StringVar()
        self.area_var = tk.StringVar()
        self.cama_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.paciente_id_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_ingreso_var, width=15).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_egreso_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.area_var, width=20).grid(row=1, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.cama_var, width=10).grid(row=2, column=1, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#f0f9ff")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_hospitalizacion, bg="#7dd3fc", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_hospitalizacion, bg="#93c5fd", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_hospitalizacion, bg="#fca5a5", fg="#166534", font=fuente_boton, width=12, activebackground="#991b1b").grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "paciente_id", "fecha_ingreso", "fecha_egreso", "area", "cama"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("paciente_id", text="Paciente ID")
        self.tree.heading("fecha_ingreso", text="Fecha Ingreso")
        self.tree.heading("fecha_egreso", text="Fecha Egreso")
        self.tree.heading("area", text="Área")
        self.tree.heading("cama", text="Cama")
        self.tree.column("id", width=40)
        self.tree.column("paciente_id", width=80)
        self.tree.column("fecha_ingreso", width=100)
        self.tree.column("fecha_egreso", width=100)
        self.tree.column("area", width=120)
        self.tree.column("cama", width=80)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_hospitalizacion)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_hospitalizacion(self):
        paciente_id = self.paciente_id_var.get().strip()
        fecha_ingreso = self.fecha_ingreso_var.get().strip()
        fecha_egreso = self.fecha_egreso_var.get().strip()
        area = self.area_var.get().strip()
        cama = self.cama_var.get().strip()
        if not paciente_id or not area:
            messagebox.showwarning("Validación", "Paciente ID y Área son obligatorios.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO hospitalizacion (paciente_id, fecha_ingreso, fecha_egreso, area, cama) VALUES (?, ?, ?, ?, ?)",
                  (paciente_id, fecha_ingreso, fecha_egreso, area, cama))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_hospitalizaciones()

    def actualizar_hospitalizacion(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un registro para actualizar.")
            return
        paciente_id = self.paciente_id_var.get().strip()
        fecha_ingreso = self.fecha_ingreso_var.get().strip()
        fecha_egreso = self.fecha_egreso_var.get().strip()
        area = self.area_var.get().strip()
        cama = self.cama_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE hospitalizacion SET paciente_id=?, fecha_ingreso=?, fecha_egreso=?, area=?, cama=? WHERE id=?",
                  (paciente_id, fecha_ingreso, fecha_egreso, area, cama, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_hospitalizaciones()

    def eliminar_hospitalizacion(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un registro para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM hospitalizacion WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_hospitalizaciones()

    def load_hospitalizaciones(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, paciente_id, fecha_ingreso, fecha_egreso, area, cama FROM hospitalizacion")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_hospitalizacion(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.paciente_id_var.set(values[1])
        self.fecha_ingreso_var.set(values[2])
        self.fecha_egreso_var.set(values[3])
        self.area_var.set(values[4])
        self.cama_var.set(values[5])

    def limpiar_campos(self):
        self.paciente_id_var.set("")
        self.fecha_ingreso_var.set("")
        self.fecha_egreso_var.set("")
        self.area_var.set("")
        self.cama_var.set("") 