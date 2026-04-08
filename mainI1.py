import customtkinter as ctk
# Importaciones de tu carpeta 'calculadora'
from calculadora.tokens import EstimadorTokens
from calculadora.precios import GestorPrecios 
from calculadora.proyecciones import ProyectorUso

# Configuración de apariencia
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

class CalculadoraCostesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- INICIALIZACIÓN DE LÓGICA ---
        # Dejamos estos valores vacíos al inicio
        self.gestor_precios = None
        self.proyector = None
        self.estimador = None
        
        # --- CONFIGURACIÓN VENTANA ---
        self.title("Calculadora de Costes de APIs de IA")
        self.geometry("700x750") # Aumentamos altura para el nuevo panel
        self.configure(fg_color="#f0f2f5")

        # ... (Mantener secciones de Modelo de IA y Texto a analizar igual que antes) ...
        
        # --- SECCIÓN: Modelo de IA ---
        self.label_modelo = ctk.CTkLabel(self, text="Modelo de IA", font=("Inter", 16, "bold"))
        self.label_modelo.pack(pady=(20, 5), padx=40, anchor="w")
        
        self.combo_modelo = ctk.CTkComboBox(self, values=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], width=620)
        self.combo_modelo.pack(pady=5, padx=40)

        # --- SECCIÓN: Texto a analizar ---
        self.label_texto = ctk.CTkLabel(self, text="Texto a analizar", font=("Inter", 16, "bold"))
        self.label_texto.pack(pady=(20, 5), padx=40, anchor="w")
        
        self.input_texto = ctk.CTkTextbox(self, height=120, width=620, border_width=1)
        self.input_texto.pack(pady=5, padx=40)

        # --- BOTONES ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        ctk.CTkButton(self.frame_botones, text="Calcular Costes", fg_color="#34495e", command=self.ejecutar_calculo).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botones, text="Limpiar", fg_color="#7f8c8d", command=self.limpiar_campos).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botones, text="Salir", fg_color="#e74c3c", command=self.quit).grid(row=0, column=2, padx=10)

        # --- SECCIÓN: Resultados ---
        self.frame_resultados = ctk.CTkFrame(self, fg_color="#ebedef", corner_radius=15)
        self.frame_resultados.pack(pady=10, padx=40, fill="both", expand=True)

        # Panel Tokens (Verde)
        self.panel_tokens = self.crear_panel(self.frame_resultados, "◇ Tokens", "#d5f5e3", "#1d8348")
        self.res_tokens = ctk.CTkLabel(self.panel_tokens, text="", text_color="black")
        self.res_tokens.pack(pady=5)

        # Panel Costes (Azul)
        self.panel_costes = self.crear_panel(self.frame_resultados, "📇 Costes", "#d6eaf8", "#21618c")
        self.res_costes = ctk.CTkLabel(self.panel_costes, text="", text_color="black")
        self.res_costes.pack(pady=5)

        # NUEVO: Panel Proyección (Naranja)
        self.panel_proy = self.crear_panel(self.frame_resultados, "📈 Proyección Mensual (30 días)", "#fef9e7", "#9a7d0a")
        self.res_proy = ctk.CTkLabel(self.panel_proy, text="", text_color="black", justify="left")
        self.res_proy.pack(pady=5)

    def crear_panel(self, parent, titulo, color_bg, color_txt):
        frame = ctk.CTkFrame(parent, fg_color=color_bg, corner_radius=10)
        frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(frame, text=titulo, font=("Inter", 13, "bold"), text_color=color_txt).pack(anchor="w", padx=10)
        return frame

    def ejecutar_calculo(self):
        texto = self.input_texto.get("1.0", "end-1c")
        modelo_seleccionado = self.combo_modelo.get()
        
        if not texto.strip(): 
            return

        # 1. Instanciar la lógica con el modelo elegido por el usuario
        self.estimador = EstimadorTokens(modelo_seleccionado)
        self.gestor_precios = GestorPrecios(modelo=modelo_seleccionado) # <-- Se añade el argumento 'modelo'
        self.proyector = ProyectorUso(self.gestor_precios)
        
        # 2. Calcular tokens
        tokens_input = self.estimador.contar(texto)
        
        # 3. Calcular costes (ajustado a la estructura de tu GestorPrecios)
        # Se asume que calcular_coste_llamada recibe tokens_input y tokens_output
        res_precio = self.gestor_precios.calcular_coste_llamada(tokens_input, 0)
        coste_usd = res_precio["coste_total_usd"]

        # 4. Calcular Proyección
        proyeccion = self.proyector.calcular_mensual(
            llamadas_dia=100, 
            input_promedio=tokens_input, 
            output_promedio=50 
        )
        
        # --- ACTUALIZAR UI ---
        self.res_tokens.configure(text=f"{tokens_input} tokens")
        self.res_costes.configure(text=f"${coste_usd:.6f} USD")
        self.res_proy.configure(text=(
            f"Llamadas totales: {proyeccion['total_llamadas']:.0f}\n"
            f"Coste mensual: ${proyeccion['coste_mensual_usd']:.2f} USD"
        ))
        
    def limpiar_campos(self):
        self.input_texto.delete("1.0", "end")
        self.res_tokens.configure(text="")
        self.res_costes.configure(text="")
        self.res_proy.configure(text="")

if __name__ == "__main__":
    app = CalculadoraCostesApp()
    app.mainloop()