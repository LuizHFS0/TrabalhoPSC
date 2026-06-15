import customtkinter as ctk

from cores import *
from views.tela_login import *
from views.menu_principal import *
from views.informacoes import *
from views.cadastrar_aluno import *
from views.ver_treinos import *

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
    
    def mostrar_cadastrar_aluno(self):
        self.trocar_tela(CadastrarAluno)
    
    def mostrar_informacao_aluno(self):
        self.trocar_tela(InformacaoAluno)
    
    def mostrar_treinos(self):
        self.trocar_tela(VerTreinos)