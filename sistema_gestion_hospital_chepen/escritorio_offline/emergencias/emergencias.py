import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class EmergenciasWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Emergencias y Tópicos")
        self.root.geometry("800x500")
        self.root.configure(bg="#e3f2fd")
        self.setup_ui()
        self.load_emergencias()
        self.root.mainloop()

    def setup_ui(self):
        fuente_titulo = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        fuente_boton = tkFont.Font(family="Segoe UI", size=10)
        logo_path = os.path.join(ASSETS_PATH, "logo_hospital.png")
        ascii_logo_path = os.path.join(ASSETS_PATH, "logo_hospital_ascii.txt")
        if os.path.exists(logo_path):
            logo_img = PhotoImage(file=logo_path)
            self.logo_img = logo_img
            tk.Label(self.root, image=logo_img, bg="#e3f2fd").pack(pady=(10, 2))
        elif os.path.exists(ascii_logo_path):
            with open(ascii_logo_path, "r", encoding="utf-8") as f:
                ascii_logo = f.read()
            tk.Label(self.root, text=ascii_logo, font=("Consolas", 10), fg="#0d47a1", bg="#e3f2fd", justify="center").pack(pady=(10, 2))
        tk.Label(self.root, text="Emergencias y Tópicos", font=fuente_titulo, bg="#e3f2fd", fg="#1565c0").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#e3f2fd")
        frame.pack(pady=5)
        tk.Label(frame, text="Paciente ID:", bg="#e3f2fd").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Fecha:", bg="#e3f2fd").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Motivo:", bg="#e3f2fd").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Triaje:", bg="#e3f2fd").grid(row=1, column=2, padx=5, pady=5)
        self.paciente_id_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.motivo_var = tk.StringVar()
        self.triaje_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.paciente_id_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_var, width=15).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.motivo_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.triaje_var, values=["Rojo", "Amarillo", "Verde", "Azul"], width=13).grid(row=1, column=3, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#e3f2fd")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_emergencia, bg="#42a5f5", fg="white", font=fuente_boton, width=12, activebackground="#1976d2").grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_emergencia, bg="#29b6f6", fg="white", font=fuente_boton, width=12, activebackground="#0288d1").grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_emergencia, bg="#0288d1", fg="white", font=fuente_boton, width=12, activebackground="#01579b").grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "paciente_id", "fecha", "motivo", "triaje"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("paciente_id", text="Paciente ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("motivo", text="Motivo")
        self.tree.heading("triaje", text="Triaje")
        self.tree.column("id", width=40)
        self.tree.column("paciente_id", width=80)
        self.tree.column("fecha", width=100)
        self.tree.column("motivo", width=180)
        self.tree.column("triaje", width=80)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_emergencia)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_emergencia(self):
        paciente_id = self.paciente_id_var.get().strip()
        fecha = self.fecha_var.get().strip()
        motivo = self.motivo_var.get().strip()
        triaje = self.triaje_var.get().strip()
        if not paciente_id or not motivo:
            messagebox.showwarning("Validación", "Paciente ID y Motivo son obligatorios.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO emergencias (paciente_id, fecha, motivo, triaje) VALUES (?, ?, ?, ?)",
                  (paciente_id, fecha, motivo, triaje))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_emergencias()

    def actualizar_emergencia(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione una emergencia para actualizar.")
            return
        paciente_id = self.paciente_id_var.get().strip()
        fecha = self.fecha_var.get().strip()
        motivo = self.motivo_var.get().strip()
        triaje = self.triaje_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE emergencias SET paciente_id=?, fecha=?, motivo=?, triaje=? WHERE id=?",
                  (paciente_id, fecha, motivo, triaje, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_emergencias()

    def eliminar_emergencia(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione una emergencia para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta emergencia?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM emergencias WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_emergencias()

    def load_emergencias(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, paciente_id, fecha, motivo, triaje FROM emergencias")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_emergencia(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.paciente_id_var.set(values[1])
        self.fecha_var.set(values[2])
        self.motivo_var.set(values[3])
        self.triaje_var.set(values[4])

    def limpiar_campos(self):
        self.paciente_id_var.set("")
        self.fecha_var.set("")
        self.motivo_var.set("")
        self.triaje_var.set("") 