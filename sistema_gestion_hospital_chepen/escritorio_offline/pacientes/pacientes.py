import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class PacientesWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestión de Pacientes")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f4fa")
        self.setup_ui()
        self.load_pacientes()
        self.root.mainloop()

    def setup_ui(self):
        fuente_titulo = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        fuente_boton = tkFont.Font(family="Segoe UI", size=10)
        # Logo si existe
        logo_path = os.path.join(ASSETS_PATH, "logo_hospital.png")
        ascii_logo_path = os.path.join(ASSETS_PATH, "logo_hospital_ascii.txt")
        if os.path.exists(logo_path):
            logo_img = PhotoImage(file=logo_path)
            self.logo_img = logo_img  # Guardar referencia
            tk.Label(self.root, image=logo_img, bg="#f0f4fa").pack(pady=(10, 2))
        elif os.path.exists(ascii_logo_path):
            with open(ascii_logo_path, "r", encoding="utf-8") as f:
                ascii_logo = f.read()
            tk.Label(self.root, text=ascii_logo, font=("Consolas", 10), fg="#0d47a1", bg="#f0f4fa", justify="center").pack(pady=(10, 2))
        tk.Label(self.root, text="Gestión de Pacientes", font=fuente_titulo, bg="#f0f4fa", fg="#1a237e").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#f0f4fa")
        frame.pack(pady=5)
        tk.Label(frame, text="Nombre:", bg="#f0f4fa").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="DNI:", bg="#f0f4fa").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Fecha Nacimiento:", bg="#f0f4fa").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Sexo:", bg="#f0f4fa").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(frame, text="Dirección:", bg="#f0f4fa").grid(row=2, column=0, padx=5, pady=5)
        self.nombre_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.fecha_nacimiento_var = tk.StringVar()
        self.sexo_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.nombre_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.dni_var, width=15).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_nacimiento_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.sexo_var, values=["M", "F"], width=13).grid(row=1, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.direccion_var, width=30).grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#f0f4fa")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_paciente, bg="#4CAF50", fg="white", font=fuente_boton, width=12).grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_paciente, bg="#2196F3", fg="white", font=fuente_boton, width=12).grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_paciente, bg="#F44336", fg="white", font=fuente_boton, width=12).grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "nombre", "dni", "fecha_nacimiento", "sexo", "direccion"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("fecha_nacimiento", text="Fecha Nacimiento")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("direccion", text="Dirección")
        self.tree.column("id", width=40)
        self.tree.column("nombre", width=120)
        self.tree.column("dni", width=80)
        self.tree.column("fecha_nacimiento", width=100)
        self.tree.column("sexo", width=60)
        self.tree.column("direccion", width=180)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_paciente)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_paciente(self):
        nombre = self.nombre_var.get().strip()
        dni = self.dni_var.get().strip()
        fecha = self.fecha_nacimiento_var.get().strip()
        sexo = self.sexo_var.get().strip()
        direccion = self.direccion_var.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO pacientes (nombre, dni, fecha_nacimiento, sexo, direccion) VALUES (?, ?, ?, ?, ?)",
                  (nombre, dni, fecha, sexo, direccion))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_pacientes()

    def actualizar_paciente(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un paciente para actualizar.")
            return
        nombre = self.nombre_var.get().strip()
        dni = self.dni_var.get().strip()
        fecha = self.fecha_nacimiento_var.get().strip()
        sexo = self.sexo_var.get().strip()
        direccion = self.direccion_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE pacientes SET nombre=?, dni=?, fecha_nacimiento=?, sexo=?, direccion=? WHERE id=?",
                  (nombre, dni, fecha, sexo, direccion, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_pacientes()

    def eliminar_paciente(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un paciente para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este paciente?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM pacientes WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_pacientes()

    def load_pacientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, nombre, dni, fecha_nacimiento, sexo, direccion FROM pacientes")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_paciente(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.nombre_var.set(values[1])
        self.dni_var.set(values[2])
        self.fecha_nacimiento_var.set(values[3])
        self.sexo_var.set(values[4])
        self.direccion_var.set(values[5])

    def limpiar_campos(self):
        self.nombre_var.set("")
        self.dni_var.set("")
        self.fecha_nacimiento_var.set("")
        self.sexo_var.set("")
        self.direccion_var.set("")
        self.selected_id = None 