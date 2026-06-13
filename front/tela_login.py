import customtkinter as ctk
import time

from cores import *
from front.menu_principal import *
from front.editar_perfil import EditarPerfil

data = time.strftime("%d/%m/%Y")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Academia - TrabalhoPSC")
        self.geometry("1300x800")
        self.configure(fg_color=FUNDO)
        
        self.frame_atual = None
        
        self.mostrar_login()

    def trocar_tela(self, nova_tela):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = nova_tela(self)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_login(self):
        self.trocar_tela(LoginFrame)
    
    def mostrar_menu(self):
        self.trocar_tela(MenuPrincipal)
    
    def mostrar_editar_perfil(self):
        self.trocar_tela(EditarPerfil)
    

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        
        # Frame do centro
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=500, width=400, corner_radius=12)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(centro, text="LOGIN", font=("Inter", 20, "bold")).pack(pady=20) # Titulo
        centro.pack_propagate(False) # Impede que o recurso pack altere q sua largura
        # Títulos / Entradas
        
        ctk.CTkLabel(centro, text="Usuário:", font=("Inter", 13), text_color=TEXTO).pack(pady=20)
        
        self.entrada_usuario = ctk.CTkEntry(centro)
        self.entrada_usuario.pack(pady=10)
        
        ctk.CTkLabel(centro, text="Senha:", font=("Inter", 13), text_color=TEXTO).pack(pady=20)

        self.entrada_senha = ctk.CTkEntry(centro)
        self.entrada_senha.pack(pady=10)
        
        # Botões
        
        """Botão que valida o login e da acesso ao app caso o login esteja certo"""
        ctk.CTkButton(centro, text="Entrar", text_color='black', fg_color=VERDE, command= lambda: master.mostrar_menu()).pack(pady=20)
        
        """Botão para a saída do app"""
        ctk.CTkButton(centro, text="Sair", text_color='black', fg_color=VERMELHO).pack(pady=20) 
        
        # Label dos créditos
        ctk.CTkLabel(self, text="Feito por: Luiz Henrique, Gabriel Messias, Lucas Batista").place(relx=0.5, rely=0.97, anchor="center")