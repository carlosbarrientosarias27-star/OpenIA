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

       # --- SECCIÓN: Botones (Alineados a la Izquierda y Rectangulares) ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(fill="x", pady=20, padx=25) # El padx alinea el bloque con el resto de la UI

        # Botón Calcular
        self.btn_calcular = ctk.CTkButton(
            self.frame_botones, 
            text="Calcular Costes", 
            fg_color="#34495e", 
            hover_color="#2c3e50",
            command=self.ejecutar_calculo, 
            width=120, 
            height=32,
            corner_radius=8,  # Valor bajo para que se vea rectangular
            font=("Comic Sans MS", 12, "bold")
        )
        self.btn_calcular.pack(side="left", padx=(0, 10)) # El 0 a la izquierda lo pega al borde

        # Botón Limpiar
        self.btn_limpiar = ctk.CTkButton(
            self.frame_botones, 
            text="Limpiar", 
            fg_color="#7f8c8d", 
            hover_color="#707b7c",
            command=self.limpiar_campos, 
            width=100, 
            height=32,
            corner_radius=8,
            font=("Comic Sans MS", 12, "bold")
        )
        self.btn_limpiar.pack(side="left", padx=10)

        # Botón Salir
        self.btn_salir = ctk.CTkButton(
            self.frame_botones, 
            text="Salir", 
            fg_color="#e74c3c", 
            hover_color="#c0392b",
            command=self.quit, 
            width=100, 
            height=32,
            corner_radius=8,
            font=("Comic Sans MS", 12, "bold")
        )
        self.btn_salir.pack(side="left", padx=10)

        # --- SECCIÓN: Resultados ---
        self.frame_resultados = ctk.CTkFrame(self, fg_color="#ebedef", corner_radius=20)
        self.frame_resultados.pack(pady=15, padx=30, fill="both", expand=True)

        # Título de la sección
        self.label_res_title = ctk.CTkLabel(self.frame_resultados, text="Resultados", font=("Comic Sans MS", 16, "bold"), text_color="#2c3e50")
        self.label_res_title.pack(anchor="w", padx=20, pady=(10, 5))

        # Paneles usando la nueva función
        self.panel_tokens = self.crear_panel(self.frame_resultados, "◇ Tokens", "#e8f5e9", "#1b5e20")
        self.res_tokens = ctk.CTkLabel(self.panel_tokens, text="Esperando cálculo...", font=("Comic Sans MS", 12), text_color="black",justify="left")
        self.res_tokens.pack(pady=10, padx=15, anchor="w")

        self.panel_costes = self.crear_panel(self.frame_resultados, "📇 Costes", "#e3f2fd", "#0d47a1")
        self.res_costes = ctk.CTkLabel(self.panel_costes, text="$ 0.00", font=("Comic Sans MS", 12), text_color="black",justify="left")
        self.res_costes.pack(pady=10, padx=15, anchor="w")

    def crear_panel(self, parent, titulo, color_bg, color_txt):
        # Frame exterior de color
        frame_fondo = ctk.CTkFrame(parent, fg_color=color_bg, corner_radius=15)
        frame_fondo.pack(pady=8, padx=20, fill="x")

        # Título del panel
        ctk.CTkLabel(frame_fondo, text=titulo, font=("Comic Sans MS", 13, "bold"), text_color=color_txt).pack(anchor="w", padx=15, pady=(5, 0))

        # Cuadro blanco interno (estilo empresa)
        cuadro_blanco = ctk.CTkFrame(frame_fondo, fg_color="#ffffff", corner_radius=10)
        cuadro_blanco.pack(pady=(5, 10), padx=10, fill="both", expand=True)
    
        return cuadro_blanco
    
    def ejecutar_calculo(self):
        texto = self.input_texto.get("1.0", "end-1c")
        modelo_seleccionado = self.combo_modelo.get()
        
        if not texto.strip(): 
            return

        # 1. Instanciar lógica (Aquí es donde ya tienes tus valores)
        self.estimador = EstimadorTokens(modelo_seleccionado)
        self.gestor_precios = GestorPrecios(modelo=modelo_seleccionado)
        self.proyector = ProyectorUso(self.gestor_precios)
        
        # 2. Obtener los valores automáticos de tus módulos
        # En lugar de .get() de un cuadro de texto, usamos los del estimador o valores por defecto del negocio
        tokens_input = self.estimador.contar(texto)
        tokens_out_est = 200  # O el valor que devuelva tu lógica interna
        calls_per_day = 50    # O el valor que devuelva tu lógica interna
        
        # 3. Calcular costes usando tu GestorPrecios
        res_precio = self.gestor_precios.calcular_coste_llamada(tokens_input, tokens_out_est)
        coste_usd = res_precio["coste_total_usd"]

        # --- CONVERSIONES PARA ESTILO EMPRESA ---
        tasa_euro = 0.92  # Tasa de cambio aproximada
        coste_eur = coste_usd * tasa_euro
        coste_cent = coste_usd * 100 # Valor en céntimos

        # 4. Calcular Proyección usando tu ProyectorUso
        proyeccion = self.proyector.calcular_mensual(
            llamadas_dia=calls_per_day, 
            input_promedio=tokens_input, 
            output_promedio=tokens_out_est 
        )
        
        # --- ACTUALIZAR UI (Sin errores de AttributeError) ---
        # Formato para TOKENS (Multilinea)
        texto_tokens = (
            f"📥 Entrada: {tokens_input} tokens\n"
            f"📤 Salida (Est.): {tokens_out_est} tokens\n"
            f"📊 Total: {tokens_input + tokens_out_est} tokens"
        )
        self.res_tokens.configure(text=texto_tokens, justify="left")

        # COSTES: Euros, Dólares y Céntimos (Estilo Empresa)
        texto_costes = (
            f"💶 Euros:{coste_eur:.3f} €\n"
            f"💵 Dollar:{coste_usd:.3f} $\n"
            f"🪙 Cent:{coste_cent:.3f} ¢"
        )
        self.res_costes.configure(text=texto_costes, justify="left")

        # Formato para PROYECCIÓN (Si existe el label)
        if hasattr(self, 'res_proy'):
            texto_proy = (
                f"📅 Mensual ({calls_per_day} llamadas/día):\n"
                f"💰 Total: ${proyeccion['coste_mensual_usd']:.2f} USD"
            )
            self.res_proy.configure(text=texto_proy, justify="left")
        
        # IMPORTANTE: Asegúrate de que res_proy esté creado en el __init__
        if hasattr(self, 'res_proy'):
            self.res_proy.configure(text=(
                f"Llamadas totales/mes: {proyeccion['total_llamadas']:,}\n"
                f"Coste estimado mensual: ${proyeccion['coste_mensual_usd']:.2f} USD"
            )
            )
    def limpiar_campos(self):
        self.input_texto.delete("1.0", "end")
        self.res_tokens.configure(text="")
        self.res_costes.configure(text="")
        self.res_proy.configure(text="")

if __name__ == "__main__":
    app = CalculadoraCostesApp()
    app.mainloop()