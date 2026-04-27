import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class AdministracionWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Gestión Administrativa y Reportes")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f9ff")
        self.setup_ui()
        self.load_registros()
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
        tk.Label(self.root, text="Gestión Administrativa y Reportes", font=fuente_titulo, bg="#f0f9ff", fg="#0ea5e9").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#f0f9ff")
        frame.pack(pady=5)
        tk.Label(frame, text="Tipo:", bg="#f0f9ff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Descripción:", bg="#f0f9ff").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Fecha:", bg="#f0f9ff").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.tipo_var, values=["Turno", "Personal", "Insumos", "Reporte", "Otro"], width=18).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.descripcion_var, width=30).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#f0f9ff")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_registro, bg="#7dd3fc", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_registro, bg="#93c5fd", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_registro, bg="#fca5a5", fg="#166534", font=fuente_boton, width=12, activebackground="#991b1b").grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "tipo", "descripcion", "fecha"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("fecha", text="Fecha")
        self.tree.column("id", width=40)
        self.tree.column("tipo", width=120)
        self.tree.column("descripcion", width=250)
        self.tree.column("fecha", width=120)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_registro)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_registro(self):
        tipo = self.tipo_var.get().strip()
        descripcion = self.descripcion_var.get().strip()
        fecha = self.fecha_var.get().strip()
        if not tipo or not descripcion:
            messagebox.showwarning("Validación", "Tipo y Descripción son obligatorios.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO administracion (tipo, descripcion, fecha) VALUES (?, ?, ?)",
                  (tipo, descripcion, fecha))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_registros()

    def actualizar_registro(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un registro para actualizar.")
            return
        tipo = self.tipo_var.get().strip()
        descripcion = self.descripcion_var.get().strip()
        fecha = self.fecha_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE administracion SET tipo=?, descripcion=?, fecha=? WHERE id=?",
                  (tipo, descripcion, fecha, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_registros()

    def eliminar_registro(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un registro para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM administracion WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_registros()

    def load_registros(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, tipo, descripcion, fecha FROM administracion")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_registro(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.tipo_var.set(values[1])
        self.descripcion_var.set(values[2])
        self.fecha_var.set(values[3])

    def limpiar_campos(self):
        self.tipo_var.set("")
        self.descripcion_var.set("")
        self.fecha_var.set("") 