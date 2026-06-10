import customtkinter as ctk

from cores import *

class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color=FUNDO)
        
        # Frame do centro
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=600, width=800)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)
        
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")
        
        
        # Títulos
        ctk.CTkLabel(centro, text="INFORMAÇÕES", font=("Inter", 25, "bold")).place(relx=0.5, y=35, anchor="center")
        
        # informações
        # Nome
        ctk.CTkLabel(centro, text=f"Nome: (Nome da pessoa)").pack(padx=20, pady=10, anchor="w")
        # Objetivo
        ctk.CTkLabel(centro, text=f"Objetivo Atual: (Objetivo Atual)").pack(padx=20, pady=10, anchor="w")
        # Quantidade de trenos
        ctk.CTkLabel(centro, text=f"Treinos cadastrados: (Quantidade)").pack(padx=20, pady=10, anchor="w")
        
        frame_botoes = ctk.CTkFrame(centro, height=60, fg_color="transparent")
        frame_botoes.pack(side="bottom", fill="x", anchor="center")
        frame_botoes.pack_propagate(False)
        
        container = ctk.CTkFrame(frame_botoes, fg_color="transparent")
        container.pack(pady=10)

        """Criação de botões: Meu Perfil, Meus treinos, Gerar treinos, Sair"""
        # Meu perfil
        
        botoes = [
            ("Meu Perfil", lambda: print('oi')),
            ("Meus Treinos", lambda: print('oi')),
            ("Gerar treinos", lambda: print('oi')),
            ("Sair", lambda: self.master.destroy())
        ]
        
        for nome, comando in botoes:
            ctk.CTkButton(container, text=nome, height=75, width=50, command=comando).pack(side="left", fill="x", padx=20) # Esse botão acessa todas as informações pessoais do usuário
        