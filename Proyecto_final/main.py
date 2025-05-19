import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class Donantes:
    def __init__(self, root):
        self.root = root
        self.root.title("Donacion de sangre")
        self.root.geometry("600x400")

        self.archivo_datos = "datos.csv"
        #Creacion del archivo datos
        if os.path.exists(self.archivo_datos):
            self.df = pd.read_csv(self.archivo_datos)
        else:
            self.df = pd.DataFrame(columns=["Nombre", "Apellido", "Tipo_sangre", "Fecha_donacion"])

        # Estilos y colores
        self.root.configure(bg="light blue")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='blue', foreground='white', font=('Helvetica', 12, 'bold'), padding=8)
        style.map('TButton', background=[('active', 'dark blue')])

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="light blue")
        self.canvas.pack(fill="both", expand=True)

        #Fondo principal
        self.imagen_original = Image.open("C:\\Users\\arria\\OneDrive - Benemérita Universidad Autónoma de Puebla\\Documentos\\escuela\\Proyecto_final\\fondo_lateral.jpg")
        self.imagen_tk = ImageTk.PhotoImage(self.imagen_original)
        self.fondo_id = self.canvas.create_image(0, 0, anchor="nw", image=self.imagen_tk)

        self.frame_botones = tk.Frame(self.canvas, bg='light blue', highlightthickness=0)
        
        self.frame_botones_window = self.canvas.create_window(300, 200, window=self.frame_botones)

        # Botones
        btn_registro = ttk.Button(self.frame_botones, text="Registro de donantes", command=self.abrir_registro)
        btn_registro.pack(pady=(10, 5), fill='x')

        btn_busqueda = ttk.Button(self.frame_botones, text="Busqueda", command=self.abrir_busqueda)
        btn_busqueda.pack(pady=5, fill='x')

        btn_reportes = ttk.Button(self.frame_botones, text="Reporte de datos", command=self.abrir_reportes)
        btn_reportes.pack(pady=5, fill='x')

        # Texto
        self.texto_id = self.canvas.create_text(300, 50, text="Bienvenido al Registro de Donantes", font=("Helvetica", 22, "bold"), fill="navy")  # azul oscuro

        self.root.bind("<Configure>", self.redimensionar_fondo)

    #Para redimencionar el fondo si se expande
    def redimensionar_fondo(self, event):
        if event.width > 0 and event.height > 0:
            nueva_imagen = self.imagen_original.resize((event.width, event.height), Image.LANCZOS)
            self.imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            self.canvas.itemconfig(self.fondo_id, image=self.imagen_tk)
            self.canvas.config(width=event.width, height=event.height)
            # Reposicionar los botoners
            self.canvas.coords(self.frame_botones_window, event.width // 2, event.height // 2)

    #Ventana de registro
    def abrir_registro(self):
        ventana_registro = tk.Toplevel(self.root)
        ventana_registro.title("Registro de Donantes")
        ventana_registro.geometry("400x300")
        ventana_registro.configure(bg="light blue")

        tipos_sangre = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        ttk.Label(ventana_registro, text="Nombre:", background="light blue", font=("Helvetica", 11)).pack(pady=5)
        entrada_nombre = ttk.Entry(ventana_registro)
        entrada_nombre.pack()

        ttk.Label(ventana_registro, text="Apellido:", background="light blue", font=("Helvetica", 11)).pack(pady=10)
        entrada_apellido = ttk.Entry(ventana_registro)
        entrada_apellido.pack()

        ttk.Label(ventana_registro, text="Tipo de Sangre:", background="light blue", font=("Helvetica", 11)).pack(pady=5)
        entrada_tipo = ttk.Combobox(ventana_registro, values=tipos_sangre, state="readonly")
        entrada_tipo.pack()

        ttk.Label(ventana_registro, text="Fecha de Donación (DD/MM/AAAA):", background="light blue", font=("Helvetica", 11)).pack(pady=5)
        entrada_fecha = ttk.Entry(ventana_registro)
        entrada_fecha.pack()
        #Para guardar los datos
        def guardar_donante():
            nombre = entrada_nombre.get().strip()
            apellido = entrada_apellido.get().strip()
            tipo = entrada_tipo.get().strip()
            fecha = entrada_fecha.get().strip()

            if not nombre or not apellido or not tipo or not fecha:
                messagebox.showerror("Error", "Completa todos los campos.")
                return

            try:
                datetime.strptime(fecha, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Error", "La fecha debe estar en formato DD/MM/AAAA.")
                return

            nuevo_dato = {"Nombre": nombre, "Apellido": apellido, "Tipo_sangre": tipo, "Fecha_donacion": fecha}
            nuevo_df = pd.DataFrame([nuevo_dato])
            self.df = pd.concat([self.df, nuevo_df], ignore_index=True)
            self.df.to_csv(self.archivo_datos, index=False)
            messagebox.showinfo("Exito", "Donante registrado exitosamente :)")
            ventana_registro.destroy()

        ttk.Button(ventana_registro, text="Guardar", command=guardar_donante).pack(pady=20)

    #Buscador
    def abrir_busqueda(self):
        ventana_busqueda = tk.Toplevel(self.root)
        ventana_busqueda.title("Búsqueda de Donantes")
        ventana_busqueda.geometry("800x400")
        ventana_busqueda.configure(bg="light blue")

        ttk.Label(ventana_busqueda, text="Buscar por nombre, apellido y tipo de sangre:", background="light blue", font=("Helvetica", 11)).pack(pady=10)
        self.entrada_busqueda = ttk.Entry(ventana_busqueda, width=40)
        self.entrada_busqueda.pack(pady=5)

        self.tree = ttk.Treeview(ventana_busqueda, columns=("Nombre", "Apellido", "Tipo de sangre", "Fecha de donacion"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both", pady=10)

        def buscar():
            termino = self.entrada_busqueda.get().strip().lower()
            if not termino:
                messagebox.showwarning("Búsqueda vacía", "Por favor ingresa un término para buscar.")
                return

            resultados = self.df[self.df.apply(lambda row: termino in row.astype(str).str.lower().values, axis=1)]

            for item in self.tree.get_children():
                self.tree.delete(item)

            for _, fila in resultados.iterrows():
                self.tree.insert("", tk.END, values=list(fila))

        ttk.Button(ventana_busqueda, text="Buscar", command=buscar).pack(pady=5)

    def abrir_reportes(self):

        ventana_reportes = tk.Toplevel(self.root)
        ventana_reportes.title("Reportes de Donación de Sangre")
        ventana_reportes.geometry("800x600")

        notebook = ttk.Notebook(ventana_reportes)
        notebook.pack(expand=True, fill="both")

        #Pestaña 1 Donantes más frecuentes
        frame_frecuentes = ttk.Frame(notebook)
        notebook.add(frame_frecuentes, text="Donantes más frecuentes")

        #Contar donaciones por nombre y apellido
        self.df['Donante'] = self.df['Nombre'] + " " + self.df['Apellido']
        conteo_donantes = self.df['Donante'].value_counts().head(10)

        texto_frecuentes = tk.Text(frame_frecuentes, height=15)
        texto_frecuentes.pack(expand=True, fill="both")
        texto_frecuentes.insert(tk.END, "Top 10 Donantes más frecuentes:\n\n")
        for donante, cant in conteo_donantes.items():
            texto_frecuentes.insert(tk.END, f"{donante}: {cant} donaciones\n")
        texto_frecuentes.config(state=tk.DISABLED)

        #Pestaña 2 Inventario de sangre por tipo
        frame_inventario = ttk.Frame(notebook)
        notebook.add(frame_inventario, text="Inventario de Sangre")

        inventario = self.df['Tipo_sangre'].value_counts()

        texto_inventario = tk.Text(frame_inventario, height=15)
        texto_inventario.pack(expand=True, fill="both")
        texto_inventario.insert(tk.END, "Inventario de Sangre por Tipo:\n\n")
        for tipo, cant in inventario.items():
            texto_inventario.insert(tk.END, f"{tipo}: {cant} unidades\n")
        texto_inventario.config(state=tk.DISABLED)

        #Pestaña 3 Alertas de inventario bajo
        frame_alertas = ttk.Frame(notebook)
        notebook.add(frame_alertas, text="Alertas Inventario")

        alerta_texto = tk.Text(frame_alertas, height=15)
        alerta_texto.pack(expand=True, fill="both")

        # Definimos cuanto es poco
        cantidad_baja = 3
        alertas = inventario[inventario < cantidad_baja]

        if alertas.empty:
            alerta_texto.insert(tk.END, "No hay alertas de inventario bajo.\n")
        else:
            alerta_texto.insert(tk.END, "Inventario bajo para los siguientes tipos:\n\n")
            for tipo, cant in alertas.items():
                alerta_texto.insert(tk.END, f"{tipo}: {cant} unidades restantes\n")
        alerta_texto.config(state=tk.DISABLED)

        #Pestaña 4 Gráficos de distribución
        frame_graficos = ttk.Frame(notebook)
        notebook.add(frame_graficos, text="Gráficos")

        fig, axs = plt.subplots(2, 1, figsize=(6, 8))

        # Gráfico Distribución por tipo de sangre
        inventario.plot(kind='bar', ax=axs[0], color='skyblue')
        axs[0].set_title("Distribución de Donaciones por Tipo de Sangre")
        axs[0].yaxis.set_major_locator(MaxNLocator(integer=True))
        axs[0].set_xlabel("Tipo de sangre")

        # Gráfico Tendencia de donaciones
        try:
            self.df['Fecha_donacion_dt'] = pd.to_datetime(self.df['Fecha_donacion'], format="%d/%m/%Y", errors='coerce')
            datos_tiempo = self.df.dropna(subset=['Fecha_donacion_dt']).copy()

            if not datos_tiempo.empty:
                datos_tiempo['Año'] = datos_tiempo['Fecha_donacion_dt'].dt.year
                conteo_por_ano = datos_tiempo.groupby('Año').size()

                #Del 2015 hasta ano actual
                año_actual = datetime.now().year
                rango_años = list(range(2015, año_actual + 1))

                conteo_por_ano = conteo_por_ano.reindex(rango_años, fill_value=0)

                # Graficar
                axs[1].plot(conteo_por_ano.index, conteo_por_ano.values, color='orange', marker='o')
                axs[1].set_title("Tendencia anual de donaciones")
                axs[1].set_xlabel("Año")
                axs[1].set_ylabel("Cantidad de donaciones")

                #Eje y con limite de 10
                axs[1].set_ylim(0, 10)
                axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))  # Mostrar solo números enteros en Y

                #Eje x para mostrar los anos
                axs[1].set_xticks(rango_años)
                axs[1].set_xticklabels(rango_años, rotation=45)

            else:
                axs[1].text(0.5, 0.5, "No hay datos de fecha válidos para mostrar tendencia", ha='center')

        except Exception as e:
            axs[1].text(0.5, 0.5, f"Error al procesar fechas: {e}", ha='center')

        plt.tight_layout()
        #Mostrar
        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    app = Donantes(root)
    root.mainloop()
