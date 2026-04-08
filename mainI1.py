import customtkinter as ctk
# Importamos la lógica de tus archivos internos
from calculadora.tokens import contar_tokens 
from calculadora.precios import obtener_precio

# Configuración de apariencia
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

class CalculadoraCostesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Costes de APIs de IA")
        self.geometry("700x600")
        self.configure(fg_color="#f0f2f5") # Fondo gris claro de la imagen

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

        # --- SECCIÓN: Botones ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        self.btn_calcular = ctk.CTkButton(self.frame_botones, text="Calcular Costes", 
                                          fg_color="#34495e", hover_color="#2c3e50",
                                          command=self.ejecutar_calculo)
        self.btn_calcular.grid(row=0, column=0, padx=10)

        self.btn_limpiar = ctk.CTkButton(self.frame_botones, text="Limpiar", 
                                         fg_color="#7f8c8d", hover_color="#95a5a6",
                                         command=self.limpiar_campos)
        self.btn_limpiar.grid(row=0, column=1, padx=10)

        self.btn_salir = ctk.CTkButton(self.frame_botones, text="Salir", 
                                       fg_color="#e74c3c", hover_color="#c0392b",
                                       command=self.quit)
        self.btn_salir.grid(row=0, column=2, padx=10)

        # --- SECCIÓN: Resultados ---
        self.frame_resultados = ctk.CTkFrame(self, fg_color="#ebedef", corner_radius=15)
        self.frame_resultados.pack(pady=10, padx=40, fill="both", expand=True)

        # Sub-panel Tokens (Verde)
        self.panel_tokens = ctk.CTkFrame(self.frame_resultados, fg_color="#d5f5e3", corner_radius=10)
        self.panel_tokens.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.panel_tokens, text="◇ Tokens", font=("Inter", 14, "bold"), text_color="#1d8348").pack(anchor="w", padx=10)
        self.res_tokens = ctk.CTkLabel(self.panel_tokens, text="", text_color="black")
        self.res_tokens.pack(pady=5)

        # Sub-panel Costes (Azul)
        self.panel_costes = ctk.CTkFrame(self.frame_resultados, fg_color="#d6eaf8", corner_radius=10)
        self.panel_costes.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.panel_costes, text="📇 Costes", font=("Inter", 14, "bold"), text_color="#21618c").pack(anchor="w", padx=10)
        self.res_costes = ctk.CTkLabel(self.panel_costes, text="", text_color="black")
        self.res_costes.pack(pady=5)

    def ejecutar_calculo(self):
        texto = self.input_texto.get("1.0", "end-1c")
        modelo = self.combo_modelo.get()
        
        # Aquí llamarías a tus funciones de la carpeta 'calculadora'
        num_tokens = contar_tokens(texto, modelo) 
        coste = obtener_precio(num_tokens, modelo)
        
        self.res_tokens.configure(text=f"{num_tokens} tokens")
        self.res_costes.configure(text=f"{coste} $")

    def limpiar_campos(self):
        self.input_texto.delete("1.0", "end")
        self.res_tokens.configure(text="")
        self.res_costes.configure(text="")

if __name__ == "__main__":
    app = CalculadoraCostesApp()
    app.mainloop()