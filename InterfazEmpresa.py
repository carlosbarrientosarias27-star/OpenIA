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

        self.title("Calculadora de Costes de APIs de IA")
        self.geometry("750x850") 
        self.configure(fg_color="#f0f2f5")

        # --- SECCIÓN: Modelo de IA ---
        self.label_modelo = ctk.CTkLabel(self, text="Modelo de IA", font=("Comic Sans MS", 16, "bold"))
        self.label_modelo.pack(pady=(5, 2), padx=20, anchor="w")
        
        # Lista actualizada con Claude y Gemini
        self.combo_modelo = ctk.CTkComboBox(
            self, 
            values=[
                "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", 
                "claude-3-sonnet", "gemini-1.5-flash", "gemini-1.5-pro"
            ], 
            width=550,
            height=28,
            corner_radius=12,  
            border_width=1,
            button_color= "#949da5",
            button_hover_color="#7e878f",
            border_color="#949da5",
            fg_color="#ffffff",
            text_color="#000000",
            font=("Comic Sans MS", 12,)
        )
        self.combo_modelo.set("gpt-4o-mini") # Valor por defecto
        self.combo_modelo.pack(pady=(0, 10), padx=20,fill="x")

        # --- SECCIÓN: Texto a analizar ---
        self.label_texto = ctk.CTkLabel(self, text="Texto a analizar", font=("Comic Sans MS", 16, "bold"),text_color="#2c3e50")
        self.label_texto.pack(pady=(5, 2), padx=25, anchor="w")
        
        self.input_texto = ctk.CTkTextbox(self, height=70, width=550, border_width=0,corner_radius=15,fg_color="#ffffff", font=("Comic Sans MS", 12))
        self.input_texto.pack(pady=(0, 10), padx=20,fill="x")

        # --- BOTONES ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(fill="x", pady=20, padx=20)

        ctk.CTkButton(self.frame_botones, text="Calcular Costes", fg_color="#34495e", command=self.ejecutar_calculo, width=100).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botones, text="Limpiar", fg_color="#7f8c8d", command=self.limpiar_campos, width=100).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botones, text="Salir", fg_color="#e74c3c", command=self.quit, width=100).grid(row=0, column=2, padx=10)

        # --- SECCIÓN: Resultados ---
        self.frame_resultados = ctk.CTkFrame(self, fg_color="#ebedef", corner_radius=20)
        self.frame_resultados.pack(pady=15, padx=30, fill="both", expand=True)

        # Título de la sección
        self.label_res_title = ctk.CTkLabel(self.frame_resultados, text="Resultados", font=("Comic Sans MS", 16, "bold"), text_color="#2c3e50")
        self.label_res_title.pack(anchor="w", padx=20, pady=(10, 5))

        # Paneles usando la nueva función
        self.panel_tokens = self.crear_panel(self.frame_resultados, "◇ Tokens", "#e8f5e9", "#1b5e20")
        self.res_tokens = ctk.CTkLabel(self.panel_tokens, text="Esperando cálculo...", font=("Comic Sans MS", 12), text_color="black")
        self.res_tokens.pack(pady=10)

        self.panel_costes = self.crear_panel(self.frame_resultados, "📇 Costes", "#e3f2fd", "#0d47a1")
        self.res_costes = ctk.CTkLabel(self.panel_costes, text="$ 0.00", font=("Comic Sans MS", 12), text_color="black")
        self.res_costes.pack(pady=10)

    def crear_panel(self, parent, titulo, color_bg, color_txt):
        # Contenedor principal del color suave
        frame_principal = ctk.CTkFrame(parent, fg_color=color_bg, corner_radius=15)
        frame_principal.pack(pady=8, padx=15, fill="x") # Más pady para separar

        # Etiqueta del título (Tokens / Costes)
        ctk.CTkLabel(
            frame_principal, 
            text=titulo, 
            font=("Comic Sans MS", 13, "bold"), 
            text_color=color_txt
        ).pack(anchor="w", padx=15, pady=(5, 0))

         # El cuadro blanco interno (donde aparecerá el número)
        cuadro_blanco = ctk.CTkFrame(frame_principal, fg_color="#ffffff", corner_radius=10)
        cuadro_blanco.pack(pady=10, padx=10, fill="both", expand=True)
    
        return cuadro_blanco # Ahora devolvemos el cuadro blanco para poner el texto dentro

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