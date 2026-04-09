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

        self.title("Calculadora de Costes Multi-Modelo")
        self.geometry("750x850") 
        self.configure(fg_color="#f0f2f5")

        # --- SECCIÓN: Modelo de IA ---
        self.label_modelo = ctk.CTkLabel(self, text="Modelo de IA", font=("Comic Sans MS", 16, "bold"))
        self.label_modelo.pack(pady=(20, 5), padx=40, anchor="w")
        
        # Lista actualizada con Claude y Gemini
        self.combo_modelo = ctk.CTkComboBox(
            self, 
            values=[
                "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", 
                "claude-3-sonnet", "gemini-1.5-flash", "gemini-1.5-pro"
            ], 
            width=620
        )
        self.combo_modelo.set("gpt-4o-mini") # Valor por defecto
        self.combo_modelo.pack(pady=5, padx=40)

        # --- SECCIÓN: Configuración de Parámetros ---
        self.frame_params = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_params.pack(pady=10, padx=40, fill="x")

        # Tokens de salida estimados
        self.label_out = ctk.CTkLabel(self.frame_params, text="Tokens Salida (Est.):", font=("Inter", 12))
        self.label_out.grid(row=0, column=0, padx=(0, 10))
        self.entry_output = ctk.CTkEntry(self.frame_params, width=100)
        self.entry_output.insert(0, "200")
        self.entry_output.grid(row=0, column=1)

        # Llamadas diarias para la proyección
        self.label_calls = ctk.CTkLabel(self.frame_params, text="Consultas/Día:", font=("Inter", 12))
        self.label_calls.grid(row=0, column=2, padx=(20, 10))
        self.entry_calls = ctk.CTkEntry(self.frame_params, width=100)
        self.entry_calls.insert(0, "100")
        self.entry_calls.grid(row=0, column=3)

        # --- SECCIÓN: Texto a analizar ---
        self.label_texto = ctk.CTkLabel(self, text="Prompt / Input de Texto", font=("Inter", 16, "bold"))
        self.label_texto.pack(pady=(10, 5), padx=40, anchor="w")
        
        self.input_texto = ctk.CTkTextbox(self, height=150, width=620, border_width=1)
        self.input_texto.pack(pady=5, padx=40)

        # --- BOTONES ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        ctk.CTkButton(self.frame_botones, text="Calcular Costes", fg_color="#34495e", command=self.ejecutar_calculo, width=150).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botones, text="Limpiar", fg_color="#7f8c8d", command=self.limpiar_campos, width=150).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botones, text="Salir", fg_color="#e74c3c", command=self.quit, width=150).grid(row=0, column=2, padx=10)

        # --- SECCIÓN: Resultados ---
        self.frame_resultados = ctk.CTkFrame(self, fg_color="#ebedef", corner_radius=15)
        self.frame_resultados.pack(pady=10, padx=40, fill="both", expand=True)

        self.panel_tokens = self.crear_panel(self.frame_resultados, "◇ Conteo de Tokens", "#d5f5e3", "#1d8348")
        self.res_tokens = ctk.CTkLabel(self.panel_tokens, text="", font=("Inter", 14, "bold"), text_color="black")
        self.res_tokens.pack(pady=5)

        self.panel_costes = self.crear_panel(self.frame_resultados, "📇 Coste por Consulta", "#d6eaf8", "#21618c")
        self.res_costes = ctk.CTkLabel(self.panel_costes, text="", font=("Inter", 14, "bold"), text_color="black")
        self.res_costes.pack(pady=5)

        self.panel_proy = self.crear_panel(self.frame_resultados, "📈 Proyección Mensual (30 días)", "#fef9e7", "#9a7d0a")
        self.res_proy = ctk.CTkLabel(self.panel_proy, text="", font=("Inter", 13), text_color="black", justify="left")
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

        # Validar entradas numéricas
        try:
            tokens_out_est = int(self.entry_output.get())
            calls_per_day = int(self.entry_calls.get())
        except ValueError:
            self.res_proy.configure(text="Error: Ingresa números válidos en configuración")
            return

        # 1. Instanciar lógica
        self.estimador = EstimadorTokens(modelo_seleccionado)
        self.gestor_precios = GestorPrecios(modelo=modelo_seleccionado)
        self.proyector = ProyectorUso(self.gestor_precios)
        
        # 2. Calcular tokens de entrada
        tokens_input = self.estimador.contar(texto)
        
        # 3. Calcular costes
        res_precio = self.gestor_precios.calcular_coste_llamada(tokens_input, tokens_out_est)
        coste_usd = res_precio["coste_total_usd"]

        # 4. Calcular Proyección
        proyeccion = self.proyector.calcular_mensual(
            llamadas_dia=calls_per_day, 
            input_promedio=tokens_input, 
            output_promedio=tokens_out_est 
        )
        
        # --- ACTUALIZAR UI ---
        self.res_tokens.configure(text=f"In: {tokens_input} | Out (Est): {tokens_out_est}")
        self.res_costes.configure(text=f"${coste_usd:.6f} USD")
        self.res_proy.configure(text=(
            f"Llamadas totales/mes: {proyeccion['total_llamadas']:,}\n"
            f"Coste estimado mensual: ${proyeccion['coste_mensual_usd']:.2f} USD"
        ))
        
    def limpiar_campos(self):
        self.input_texto.delete("1.0", "end")
        self.res_tokens.configure(text="")
        self.res_costes.configure(text="")
        self.res_proy.configure(text="")

if __name__ == "__main__":
    app = CalculadoraCostesApp()
    app.mainloop()