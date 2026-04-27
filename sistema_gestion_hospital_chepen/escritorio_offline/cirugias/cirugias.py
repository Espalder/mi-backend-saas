import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class CirugiasWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cirugías")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f9ff")
        self.setup_ui()
        self.load_cirugias()
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
        tk.Label(self.root, text="Cirugías", font=fuente_titulo, bg="#f0f9ff", fg="#475569").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#f0f9ff")
        frame.pack(pady=5)
        tk.Label(frame, text="Paciente ID:", bg="#f0f9ff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Tipo:", bg="#f0f9ff").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Fecha:", bg="#f0f9ff").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Sala:", bg="#f0f9ff").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(frame, text="Equipo:", bg="#f0f9ff").grid(row=2, column=0, padx=5, pady=5)
        self.paciente_id_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.sala_var = tk.StringVar()
        self.equipo_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.paciente_id_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.tipo_var, width=20).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.fecha_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.sala_var, width=15).grid(row=1, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.equipo_var, width=20).grid(row=2, column=1, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#f0f9ff")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_cirugia, bg="#7dd3fc", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_cirugia, bg="#93c5fd", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_cirugia, bg="#0ea5e9", fg="#166534", font=fuente_boton, width=12, activebackground="#fca5a5").grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "paciente_id", "tipo", "fecha", "sala", "equipo"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("paciente_id", text="Paciente ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("sala", text="Sala")
        self.tree.heading("equipo", text="Equipo")
        self.tree.column("id", width=40)
        self.tree.column("paciente_id", width=80)
        self.tree.column("tipo", width=100)
        self.tree.column("fecha", width=100)
        self.tree.column("sala", width=100)
        self.tree.column("equipo", width=120)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_cirugia)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_cirugia(self):
        paciente_id = self.paciente_id_var.get().strip()
        tipo = self.tipo_var.get().strip()
        fecha = self.fecha_var.get().strip()
        sala = self.sala_var.get().strip()
        equipo = self.equipo_var.get().strip()
        if not paciente_id or not tipo:
            messagebox.showwarning("Validación", "Paciente ID y Tipo son obligatorios.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO cirugias (paciente_id, tipo, fecha, sala, equipo) VALUES (?, ?, ?, ?, ?)",
                  (paciente_id, tipo, fecha, sala, equipo))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_cirugias()

    def actualizar_cirugia(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione una cirugía para actualizar.")
            return
        paciente_id = self.paciente_id_var.get().strip()
        tipo = self.tipo_var.get().strip()
        fecha = self.fecha_var.get().strip()
        sala = self.sala_var.get().strip()
        equipo = self.equipo_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE cirugias SET paciente_id=?, tipo=?, fecha=?, sala=?, equipo=? WHERE id=?",
                  (paciente_id, tipo, fecha, sala, equipo, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_cirugias()

    def eliminar_cirugia(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione una cirugía para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta cirugía?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM cirugias WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_cirugias()

    def load_cirugias(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, paciente_id, tipo, fecha, sala, equipo FROM cirugias")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_cirugia(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.paciente_id_var.set(values[1])
        self.tipo_var.set(values[2])
        self.fecha_var.set(values[3])
        self.sala_var.set(values[4])
        self.equipo_var.set(values[5])

    def limpiar_campos(self):
        self.paciente_id_var.set("")
        self.tipo_var.set("")
        self.fecha_var.set("")
        self.sala_var.set("")
        self.equipo_var.set("") 