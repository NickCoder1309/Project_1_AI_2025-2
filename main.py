import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk  # pip install pillow

# Importar algoritmos
import breadth_first_search
import depth_first_search
import uniform_cost_search
import a_star_search
import greedy_best_first_search
from objects import Problem
from aux_functions import reconstruct_path


# ==============================
# Ventana principal de la app
# ==============================
class SmartAstronautApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Astronaut")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Variables para los combobox
        self.tipo_busqueda = tk.StringVar()
        self.sub_tipo_busqueda = tk.StringVar()

        # Variables para el mundo y algoritmos
        self.world_map = None
        self.samples = []
        self.initial_position = None
        self.solution_path = None

        # ---------- Fondo de inicio ----------
        self.bg_inicio = self.cargar_imagen("img/fondo_inicio.png", (700, 600))
        lbl_fondo = tk.Label(self.root, image=self.bg_inicio)
        lbl_fondo.place(relwidth=1, relheight=1)

        # ---------- Botón para subir archivo ----------
        self.btn_cargar = tk.Button(
            self.root,
            text="Seleccionar Archivo",
            font=("Arial", 11),
            command=self.subir_archivo,
            bg="black",
            fg="white",
        )
        self.btn_cargar.place(x=100, y=280)

        # --- Menú desplegable para tipo de búsqueda ---
        tk.Label(
            self.root,
            text="Tipo de Búsqueda:",
            font=("Arial", 10, "bold"),
            bg="black",
            fg="white",
        ).place(x=110, y=350)

        opciones_busqueda = ["No Informada", "Informada"]
        self.combo_tipo = ttk.Combobox(
            self.root,
            values=opciones_busqueda,
            textvariable=self.tipo_busqueda,
            state="readonly",
            width=25,
        )
        self.combo_tipo.set("Selecciona tipo de búsqueda")
        self.combo_tipo.place(x=90, y=380)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.mostrar_submenu)

        # Menú de algoritmos
        self.label_algoritmo = tk.Label(
            self.root,
            text="Algoritmo:",
            font=("Arial", 10, "bold"),
            bg="black",
            fg="white",
        )
        self.combo_subtipo = ttk.Combobox(
            self.root, textvariable=self.sub_tipo_busqueda, state="readonly", width=25
        )

        # ---------- Botón para continuar ----------
        btn_inicio = tk.Button(
            self.root,
            text="Iniciar Misión",
            font=("Arial", 14),
            command=self.abrir_tablero,
            bg="black",
            fg="white",
        )
        btn_inicio.place(x=110, y=500)

        self.ruta_txt = None
        self.root.mainloop()

    # ---------------------------
    def cargar_imagen(self, ruta, size=None):
        img = Image.open(ruta)
        if size:
            img = img.resize(size)
        return ImageTk.PhotoImage(img)

    # ---------------------------
    def subir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de mundo", filetypes=[("Text files", "*.txt")]
        )
        if ruta:
            self.ruta_txt = ruta
            # Cambiar texto del botón y mostrar nombre del archivo
            self.btn_cargar.config(text="✓ Archivo Cargado")
            nombre = ruta.split("/")[-1] if "/" in ruta else ruta.split("\\")[-1]

            self.label_archivo.place(x=60, y=305)

    # ---------------------------
    def mostrar_submenu(self, event=None):
        """Mostrar el submenu de algoritmos según el tipo de búsqueda seleccionado"""
        tipo = self.tipo_busqueda.get()

        if tipo == "No Informada":
            algoritmos = [
                "Búsqueda por Amplitud",
                "Costo Uniforme",
                "Profundidad evitando ciclos",
            ]
        elif tipo == "Informada":
            algoritmos = ["Avara", "A*"]
        else:
            algoritmos = []

        if algoritmos:
            self.combo_subtipo.config(values=algoritmos)
            self.combo_subtipo.set("Selecciona algoritmo")
            self.label_algoritmo.place(x=135, y=420)
            self.combo_subtipo.place(x=90, y=450)
        else:
            # Ocultar si no hay algoritmos
            self.label_algoritmo.place_forget()
            self.combo_subtipo.place_forget()

    # ============================
    # Ventana del tablero
    # ============================
    def abrir_tablero(self):
        if not self.ruta_txt:
            messagebox.showwarning(
                "Advertencia", "Primero carga un archivo .txt con la matriz del mundo."
            )
            return

        if (
            not self.sub_tipo_busqueda.get()
            or self.sub_tipo_busqueda.get() == "Selecciona algoritmo"
        ):
            messagebox.showwarning(
                "Advertencia", "Debes seleccionar un tipo de búsqueda y un algoritmo."
            )
            return

        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cambiar título de la ventana
        self.root.title(f"Mars Explorer - {self.sub_tipo_busqueda.get()}")

        # ---------- Fondo del tablero ----------
        fondo = self.cargar_imagen("img/fondo_mapa.png", (700, 600))
        lbl_fondo = tk.Label(self.root, image=fondo)
        lbl_fondo.place(relwidth=1, relheight=1)
        self.root.fondo = fondo  # mantener referencia

        # ---------- Canvas para el mapa (centrado y más grande) ----------
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=2)
        self.canvas.place(x=150, y=100, width=400, height=400)

        # Cargar y procesar matriz desde el archivo
        with open(self.ruta_txt, "r") as f:
            matriz = [list(map(int, linea.split())) for linea in f if linea.strip()]

        # Procesar el mundo para extraer información importante
        self.world_map = matriz
        self.samples = []
        self.initial_position = None

        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if matriz[i][j] == 2:  # Astronauta
                    self.initial_position = (i, j)
                elif matriz[i][j] == 6:  # Muestra científica
                    self.samples.append((i, j))

        print("Matriz leída:", matriz)
        print(f"Posición inicial: {self.initial_position}")
        print(f"Muestras encontradas: {self.samples}")

        self.dibujar_mundo(matriz)

        # ----------  botón de ejecutar  ----------
        tk.Button(
            self.root,
            text="🚀 Ejecutar Búsqueda",
            font=("Arial", 12, "bold"),
            command=self.ejecutar_algoritmo,
            bg="black",
            fg="white",
            width=20,
            height=2,
        ).place(x=176, y=530)

        # Botón Reiniciar para volver a empezar desde la pantalla inicial
        tk.Button(
            self.root,
            text="🔄 Reiniciar",
            font=("Arial", 12, "bold"),
            command=self.reiniciar_app,
            bg="black",
            fg="white",
            width=10,
            height=2,
        ).place(x=420, y=530)

    def ejecutar_algoritmo(self):
        """Ejecutar el algoritmo seleccionado"""
        if not self.world_map or not self.initial_position:
            messagebox.showerror("Error", "No se pudo cargar correctamente el mundo.")
            return

        algoritmo = self.sub_tipo_busqueda.get()

        try:
            messagebox.showinfo("Ejecutando", f"Ejecutando algoritmo: {algoritmo}...")

            resultado = None

            # Ejecutar según el algoritmo seleccionado

            import time

            problem = Problem(self.world_map, self.samples, self.initial_position)

            # medir tiempo de ejecución
            start_time = time.time()

            if algoritmo == "Búsqueda por Amplitud":
                resultado_nodo = breadth_first_search.breadth_first_search(problem)

            elif algoritmo == "Costo Uniforme":
                resultado_nodo = uniform_cost_search.uniform_cost_search(problem)

            elif algoritmo == "Profundidad evitando ciclos":
                resultado_nodo = depth_first_search.depth_first_search(problem)

            elif algoritmo == "A*":
                resultado_nodo = a_star_search.a_star_search(problem)

            elif algoritmo == "Avara":
                resultado_nodo = greedy_best_first_search.greedy_search(problem)

            else:
                messagebox.showerror("Error", f"Algoritmo '{algoritmo}' no reconocido.")
                return

            end_time = time.time()
            elapsed = end_time - start_time

            # métricas
            expanded = len(problem.reached)

            # profundidad máxima: recorrer padres para cada nodo alcanzado
            max_depth = 0
            for node in problem.reached.values():
                depth = 0
                cur = node
                while cur.parent is not None:
                    depth += 1
                    cur = cur.parent
                if depth > max_depth:
                    max_depth = depth

            # Si el algoritmo devolvió un nodo objetivo, reconstruir el camino
            if resultado_nodo:
                resultado = reconstruct_path(resultado_nodo)
            else:
                resultado = None

            # costo: solo para A* y Costo Uniforme
            costo = (
                resultado_nodo.path_cost
                if (resultado_nodo and algoritmo in ("A*", "Costo Uniforme"))
                else 0
            )

            # mostrar un mensaje final con métricas
            if resultado:
                self.solution_path = resultado
                mensaje_resultado = (
                    f"¡Solución encontrada!\n"
                    f"Algoritmo: {algoritmo}\n"
                    f"Pasos totales: {len(resultado)}\n"
                    f"Costo de la solución: {costo:.2f}\n"
                    f"Nodos expandidos: {expanded}\n"
                    f"Profundidad del árbol: {max_depth}\n"
                    f"Tiempo de cómputo (s): {elapsed:.4f}"
                )
                messagebox.showinfo("¡Éxito!", mensaje_resultado)
                self.dibujar_solucion()
            else:
                messagebox.showwarning(
                    "Sin solución",
                    f"No se encontró una solución con el algoritmo {algoritmo}\n"
                    f"Nodos expandidos: {expanded}\n"
                    f"Profundidad máxima: {max_depth}\n"
                    f"Tiempo (s): {elapsed:.4f}",
                )

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al ejecutar el algoritmo {algoritmo}:\n{str(e)}"
            )

    def dibujar_solucion(self):
        """Animar el astronauta moviéndose por el camino de la solución"""
        if not self.solution_path:
            return

        # Inicializar variables de animación
        self.animation_step = 0
        self.celda = 40
        self.usando_nave = False  # Inicializar estado de la nave

        # Comenzar la animación
        self.animar_movimiento()

    def animar_movimiento(self):
        """Animar el movimiento paso a paso del astronauta"""
        if self.animation_step >= len(self.solution_path):
            # Animación completada
            messagebox.showinfo("¡Completado!", f"El astronauta completó su misión!\n")

            return

        # Obtener posición actual
        fila, col = self.solution_path[self.animation_step]

        # Calcular coordenadas del canvas
        x = col * self.celda + self.celda // 2
        y = fila * self.celda + self.celda // 2

        # Limpiar elementos anteriores de animación
        self.canvas.delete("astronaut_animation")

        # En el primer paso, eliminar el astronauta original de la posición inicial
        if self.animation_step == 0 and self.initial_position:
            fila_inicial, col_inicial = self.initial_position
            self.eliminar_astronauta_en_posicion(fila_inicial, col_inicial)
            print(
                f"Primer paso: Eliminando astronauta original de posición inicial ({fila_inicial}, {col_inicial})"
            )

        # Verificar el estado actual y anterior para detectar cambios
        valor_casilla_actual = self.world_map[fila][col]

        # Determinar si está usando la nave o no
        if not hasattr(self, "usando_nave"):
            self.usando_nave = False

        # Recolectar muestra si está en una casilla con muestra (valor 6)
        if valor_casilla_actual == 6:
            # Eliminar la imagen de la muestra del canvas
            self.eliminar_muestra_en_posicion(fila, col)
            print(f"Paso {self.animation_step}: Muestra recolectada en ({fila}, {col})")

        # Detectar cuándo toma una nave
        if valor_casilla_actual == 5 and not self.usando_nave:
            # El astronauta acaba de llegar a una nave - cambiar a modo nave PERMANENTE
            self.usando_nave = True
            # Eliminar la imagen original de la nave de esta posición
            self.eliminar_nave_en_posicion(fila, col)
            print(
                f"Paso {self.animation_step}: Astronauta toma la nave - eliminando nave original en ({fila}, {col})"
            )
        elif valor_casilla_actual == 5 and self.usando_nave:
            # El astronauta (navegando) llega a otra nave - puede reaparecer
            self.usando_nave = False
            print(f"Paso {self.animation_step}: Astronauta deja la nave - reaparece")

        # Dibujar según el modo actual
        if self.usando_nave:
            # Mostrar la nave moviéndose (en lugar del astronauta)
            self.canvas.create_image(
                x, y, image=self.img_cohete, anchor="center", tags="astronaut_animation"
            )
        else:
            # Mostrar el astronauta normalmente
            self.canvas.create_image(
                x,
                y,
                image=self.img_astronauta,
                anchor="center",
                tags="astronaut_animation",
            )

        # Incrementar paso
        self.animation_step += 1

        # Programar siguiente paso (velocidad de animación: 500ms)
        self.root.after(500, self.animar_movimiento)

    def eliminar_muestra_en_posicion(self, fila, col):
        """Eliminar la imagen de muestra en una posición específica"""
        # Calcular las coordenadas de la casilla
        x0, y0 = col * self.celda, fila * self.celda
        x1, y1 = x0 + self.celda, y0 + self.celda

        # Buscar y eliminar elementos en esa área (exceptuando animaciones)
        items_en_area = self.canvas.find_overlapping(x0, y0, x1, y1)
        for item in items_en_area:
            tags = self.canvas.gettags(item)
            # Solo eliminar si no es una animación y no es el rectángulo base
            if "astronaut_animation" not in tags and self.canvas.type(item) == "image":
                self.canvas.delete(item)

        # Redibujar solo el rectángulo de fondo blanco para esa casilla
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    def eliminar_astronauta_en_posicion(self, fila, col):
        """Eliminar la imagen del astronauta original en una posición específica"""
        # Calcular las coordenadas de la casilla
        x0, y0 = col * self.celda, fila * self.celda
        x1, y1 = x0 + self.celda, y0 + self.celda

        # Buscar y eliminar elementos en esa área (exceptuando animaciones)
        items_en_area = self.canvas.find_overlapping(x0, y0, x1, y1)
        for item in items_en_area:
            tags = self.canvas.gettags(item)
            # Solo eliminar si no es una animación y es una imagen
            if "astronaut_animation" not in tags and self.canvas.type(item) == "image":
                self.canvas.delete(item)

        # Redibujar solo el rectángulo de fondo blanco para esa casilla
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    def eliminar_nave_en_posicion(self, fila, col):
        """Eliminar la imagen de la nave original en una posición específica"""
        # Calcular las coordenadas de la casilla
        x0, y0 = col * self.celda, fila * self.celda
        x1, y1 = x0 + self.celda, y0 + self.celda

        # Buscar y eliminar elementos en esa área (exceptuando animaciones)
        items_en_area = self.canvas.find_overlapping(x0, y0, x1, y1)
        for item in items_en_area:
            tags = self.canvas.gettags(item)
            # Solo eliminar si no es una animación y es una imagen
            if "astronaut_animation" not in tags and self.canvas.type(item) == "image":
                self.canvas.delete(item)

        # Redibujar solo el rectángulo de fondo blanco para esa casilla
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    # ---------------------------
    def dibujar_mundo(self, matriz):
        """Dibujar el mundo en el canvas"""
        self.canvas.delete("all")
        filas = 10
        columnas = 10
        celda = 40

        # Configurar el canvas con el tamaño correcto
        canvas_width = columnas * celda
        canvas_height = filas * celda
        self.canvas.config(width=canvas_width, height=canvas_height)

        # ----- Cargar imágenes -----
        img_size = (celda - 5, celda - 5)  # Ajustar tamaño de imágenes
        self.img_astronauta = self.cargar_imagen("img/astronauta.png", img_size)
        self.img_rocoso = self.cargar_imagen("img/rocoso.png", img_size)
        self.img_volcan = self.cargar_imagen("img/volcan.png", img_size)
        self.img_cohete = self.cargar_imagen("img/cohete.png", img_size)
        self.img_muestra = self.cargar_imagen("img/muestra.png", img_size)

        # Guardar referencias para evitar que se liberen
        self.canvas.img_astronauta = self.img_astronauta
        self.canvas.img_rocoso = self.img_rocoso
        self.canvas.img_volcan = self.img_volcan
        self.canvas.img_cohete = self.img_cohete
        self.canvas.img_muestra = self.img_muestra

        for f in range(filas):
            for c in range(columnas):
                x0, y0 = c * celda, f * celda
                x1, y1 = x0 + celda, y0 + celda
                valor = matriz[f][c]

                # Dibujar según el valor
                if valor == 0:
                    # Casilla libre - blanco
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="white"
                    )
                elif valor == 1:
                    # Obstáculo - negro
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="black"
                    )
                elif valor == 2:
                    # Astronauta
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="white"
                    )
                    self.canvas.create_image(
                        x0 + celda / 2, y0 + celda / 2, image=self.img_astronauta
                    )
                elif valor == 3:
                    # Terreno rocoso
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="white"
                    )
                    self.canvas.create_image(
                        x0 + celda / 2, y0 + celda / 2, image=self.img_rocoso
                    )
                elif valor == 4:
                    # Terreno volcánico
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="white"
                    )
                    self.canvas.create_image(
                        x0 + celda / 2, y0 + celda / 2, image=self.img_volcan
                    )
                elif valor == 5:
                    # Nave
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="white"
                    )
                    self.canvas.create_image(
                        x0 + celda / 2, y0 + celda / 2, image=self.img_cohete
                    )
                elif valor == 6:
                    # Muestra científica
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, outline="black", fill="white"
                    )
                    self.canvas.create_image(
                        x0 + celda / 2, y0 + celda / 2, image=self.img_muestra
                    )

    def reiniciar_app(self):
        """Cerrar la ventana actual y crear una nueva instancia de la app para reiniciar."""
        try:
            # destruir la raíz actual
            self.root.destroy()
        except Exception:
            pass

        # Crear una nueva instancia (esto abrirá la ventana desde cero)
        SmartAstronautApp()


# ==============================
# Ejecutar aplicación
# ==============================
if __name__ == "__main__":
    SmartAstronautApp()
