import pandas as pd
import tkinter as tk 
from tkinter import messagebox
import numpy as np

class CramerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolución de sistemas de ecuaciones lineales mediante la Regla de Cramer")
        self.root.geometry("650x400")
        
        # Variable para la dimensión seleccionada (por defecto 3x3)
        self.dim_var = tk.IntVar(value=3)
        
        # Matrices para almacenar las referencias a los Entry widgets
        self.entries_A = []
        self.entries_b = []
        self.entries_x = []
        
        self.crear_interfaz()
        self.actualizar_dimension() # Configurar estado inicial de las celdas

    def crear_interfaz(self):
        # --- PANEL IZQUIERDO: Dimensión ---
        frame_dim = tk.LabelFrame(self.root, text="Dimensión", padx=10, pady=10)
        frame_dim.place(x=20, y=20, width=100, height=120)
        
        tk.Radiobutton(frame_dim, text="2 x 2", variable=self.dim_var, value=2, command=self.actualizar_dimension).pack(anchor="w")
        tk.Radiobutton(frame_dim, text="3 x 3", variable=self.dim_var, value=3, command=self.actualizar_dimension).pack(anchor="w")
        tk.Radiobutton(frame_dim, text="4 x 4", variable=self.dim_var, value=4, command=self.actualizar_dimension).pack(anchor="w")

        # --- PANEL CENTRAL: Matrices A, b, x ---
        frame_matrices = tk.Frame(self.root)
        frame_matrices.place(x=140, y=20)
        
        # Etiquetas de encabezado
        tk.Label(frame_matrices, text="A", font=("Arial", 12, "bold")).grid(row=0, column=1, columnspan=4)
        tk.Label(frame_matrices, text="b", font=("Arial", 12, "bold")).grid(row=0, column=6)
        tk.Label(frame_matrices, text="x", font=("Arial", 12, "bold")).grid(row=0, column=8)
        
        # Etiquetas de columnas (0, 1, 2, 3)
        for j in range(4):
            tk.Label(frame_matrices, text=str(j)).grid(row=1, column=j+1)
            
        # Etiquetas de filas (0, 1, 2, 3) e inicialización de Entries
        for i in range(4):
            tk.Label(frame_matrices, text=str(i)).grid(row=i+2, column=0, padx=5)
            
            # Fila para matriz A
            fila_A = []
            for j in range(4):
                entry = tk.Entry(frame_matrices, width=8, justify="center")
                entry.grid(row=i+2, column=j+1, padx=2, pady=2)
                fila_A.append(entry)
            self.entries_A.append(fila_A)
            
            # Espaciador
            tk.Label(frame_matrices, text="  ").grid(row=i+2, column=5)
            
            # Fila para vector b
            entry_b = tk.Entry(frame_matrices, width=8, justify="center")
            entry_b.grid(row=i+2, column=6, padx=2, pady=2)
            self.entries_b.append(entry_b)
            
            # Espaciador
            tk.Label(frame_matrices, text="  ").grid(row=i+2, column=7)
            
            # Fila para vector x (solo lectura)
            entry_x = tk.Entry(frame_matrices, width=12, justify="center", state="readonly")
            entry_x.grid(row=i+2, column=8, padx=2, pady=2)
            self.entries_x.append(entry_x)

        # --- PANEL INFERIOR: Botones y Ayuda ---
        lbl_ayuda = tk.Label(self.root, text="Ayuda: el sistema de ecuaciones permite calcular A.x = b\nSe deben cargar los valores de A y b y luego,\nal calcular, se obtienen los valores de x", justify="center")
        lbl_ayuda.place(x=160, y=180)
        
        btn_borrar = tk.Button(self.root, text="Borrar valores", command=self.borrar_valores)
        btn_borrar.place(x=240, y=250)
        
        btn_calcular = tk.Button(self.root, text="Calcular", command=self.calcular_sistema)
        btn_calcular.place(x=350, y=250)
        
        tk.Label(self.root, text="Determinante:").place(x=150, y=300)
        self.entry_det = tk.Entry(self.root, width=15, justify="center", state="readonly")
        self.entry_det.place(x=240, y=300)
        
        btn_det = tk.Button(self.root, text="Calcular det.", command=self.mostrar_determinante)
        btn_det.place(x=350, y=295)

def actualizar_dimension(self):
        dim = self.dim_var.get()
        
        # Habilitar/Deshabilitar entradas según la dimensión seleccionada
        for i in range(4):
            for j in range(4):
                if i < dim and j < dim:
                    self.entries_A[i][j].config(state="normal")
                else:
                    self.entries_A[i][j].delete(0, tk.END)
                    self.entries_A[i][j].config(state="disabled")
            
            if i < dim:
                self.entries_b[i].config(state="normal")
            else:
                self.entries_b[i].delete(0, tk.END)
                self.entries_b[i].config(state="disabled")
            
            if i < dim:
                self.entries_x[i].config(state="normal")
                self.entries_x[i].delete(0, tk.END)
                self.entries_x[i].config(state="readonly")
            else:
                self.entries_x[i].delete(0, tk.END)
                self.entries_x[i].config(state="disabled")

def borrar_valores(self):
        # Borrar valores de la matriz A
        for fila in self.entries_A:
            for entry in fila:
                entry.config(state="normal")
                entry.delete(0, tk.END)

        # Borrar valores del vector b
        for entry in self.entries_b:
            entry.config(state="normal")
            entry.delete(0, tk.END)

        # Borrar resultados del vector x
        for entry in self.entries_x:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")

        # Borrar determinante
        self.entry_det.config(state="normal")
        self.entry_det.delete(0, tk.END)
        self.entry_det.config(state="readonly")

        # Restaurar la dimensión seleccionada
        self.actualizar_dimension()

def mostrar_determinante(self):
        dim = self.dim_var.get()

        try:
            # Obtener los valores de la matriz A
            matriz_A = []

            for i in range(dim):
                fila = []

                for j in range(dim):
                    valor = float(self.entries_A[i][j].get())
                    fila.append(valor)

                matriz_A.append(fila)

            # Convertir la matriz a un array de NumPy
            matriz_A = np.array(matriz_A)

            # Calcular el determinante
            determinante = np.linalg.det(matriz_A)

            # Mostrar el resultado
            self.entry_det.config(state="normal")
            self.entry_det.delete(0, tk.END)
            self.entry_det.insert(0, f"{determinante:.4f}")
            self.entry_det.config(state="readonly")

        except ValueError:
            messagebox.showerror(
                "Error",
                "Todos los valores de la matriz A deben ser numéricos."
            )