import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import tkinter.font as tkFont
from tkinter import PhotoImage

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')
ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

class FarmaciaWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Farmacia y Esterilización")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f9ff")
        self.setup_ui()
        self.load_medicamentos()
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
        tk.Label(self.root, text="Farmacia y Esterilización", font=fuente_titulo, bg="#f0f9ff", fg="#0ea5e9").pack(pady=(0, 10))
        frame = tk.Frame(self.root, bg="#f0f9ff")
        frame.pack(pady=5)
        tk.Label(frame, text="Medicamento:", bg="#f0f9ff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Stock:", bg="#f0f9ff").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Vencimiento:", bg="#f0f9ff").grid(row=1, column=0, padx=5, pady=5)
        self.medicamento_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.vencimiento_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.medicamento_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.stock_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.vencimiento_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        boton_frame = tk.Frame(self.root, bg="#f0f9ff")
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Agregar", command=self.agregar_medicamento, bg="#7dd3fc", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=0, padx=5)
        tk.Button(boton_frame, text="Actualizar", command=self.actualizar_medicamento, bg="#93c5fd", fg="#166534", font=fuente_boton, width=12, activebackground="#0ea5e9").grid(row=0, column=1, padx=5)
        tk.Button(boton_frame, text="Eliminar", command=self.eliminar_medicamento, bg="#fca5a5", fg="#166534", font=fuente_boton, width=12, activebackground="#991b1b").grid(row=0, column=2, padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id", "medicamento", "stock", "vencimiento"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("medicamento", text="Medicamento")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("vencimiento", text="Vencimiento")
        self.tree.column("id", width=40)
        self.tree.column("medicamento", width=180)
        self.tree.column("stock", width=80)
        self.tree.column("vencimiento", width=120)
        self.tree.pack(pady=10, fill=tk.X, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_medicamento)
        self.selected_id = None

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def agregar_medicamento(self):
        medicamento = self.medicamento_var.get().strip()
        stock = self.stock_var.get().strip()
        vencimiento = self.vencimiento_var.get().strip()
        if not medicamento or not stock:
            messagebox.showwarning("Validación", "Medicamento y Stock son obligatorios.")
            return
        conn = self.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO farmacia (medicamento, stock, vencimiento) VALUES (?, ?, ?)",
                  (medicamento, stock, vencimiento))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_medicamentos()

    def actualizar_medicamento(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un medicamento para actualizar.")
            return
        medicamento = self.medicamento_var.get().strip()
        stock = self.stock_var.get().strip()
        vencimiento = self.vencimiento_var.get().strip()
        conn = self.conectar()
        c = conn.cursor()
        c.execute("UPDATE farmacia SET medicamento=?, stock=?, vencimiento=? WHERE id=?",
                  (medicamento, stock, vencimiento, self.selected_id))
        conn.commit()
        conn.close()
        self.limpiar_campos()
        self.load_medicamentos()

    def eliminar_medicamento(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showwarning("Seleccionar", "Seleccione un medicamento para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este medicamento?"):
            conn = self.conectar()
            c = conn.cursor()
            c.execute("DELETE FROM farmacia WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.limpiar_campos()
            self.load_medicamentos()

    def load_medicamentos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = self.conectar()
        c = conn.cursor()
        c.execute("SELECT id, medicamento, stock, vencimiento FROM farmacia")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
        self.selected_id = None

    def seleccionar_medicamento(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, 'values')
        if not values:
            return
        self.selected_id = values[0]
        self.medicamento_var.set(values[1])
        self.stock_var.set(values[2])
        self.vencimiento_var.set(values[3])

    def limpiar_campos(self):
        self.medicamento_var.set("")
        self.stock_var.set("")
        self.vencimiento_var.set("") 