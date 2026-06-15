import customtkinter as ctk

from cores import *
from tkinter import ttk, messagebox

class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color=FUNDO)
        
        # Frame do centro
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=700, width=1000)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)
        
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")
        
        
        # Títulos
        ctk.CTkLabel(centro, text="INFORMAÇÕES", font=("Inter", 25, "bold")).place(relx=0.5, y=35, anchor="center")
        
        frame_botoes = ctk.CTkFrame(centro, height=60, fg_color="transparent")
        frame_botoes.pack(side="top", fill="x", anchor="center")
        frame_botoes.pack_propagate(False)
        
        frame_pesquisa = ctk.CTkFrame(frame_botoes, fg_color="transparent")
        frame_pesquisa.pack(side="left", padx=20)

        ctk.CTkLabel(
            frame_pesquisa,
            text="Pesquisar:",
            font=("Inter", 14, "bold")
        ).pack(anchor="w")

        self.entrada_pesquisa = ctk.CTkEntry(
            frame_pesquisa,
            width=250,
            height=40
        )
        self.entrada_pesquisa.pack()
        

        """Criação de botões: Meu Perfil, Meus treinos, Gerar treinos, Sair"""
        # Meu perfil
        
        botoes = [
            ("+ Novo Aluno", lambda: self.master.mostrar_cadastrar_aluno(), AZUL),
            ("Informações", lambda: self.master.mostrar_informacao_aluno(), AZUL),
            ("Meus Treinos", lambda: print("Bonjour")),
            ("Sair", lambda: self.master.destroy(), VERMELHO)
        ]
        
        for nome, comando, cor in botoes:
            ctk.CTkButton(frame_botoes, text=nome, height=50, fg_color=cor, width=50, command=comando, text_color="black").pack(side="left", fill="x", padx=20) # Esse botão acessa todas as informações pessoais do usuário
        
        style = ttk.Style()
        style.theme_use("clam")
        
        colunas = ("id", "nome", "contato", "email", "datansc", "peso", "altura")
        self.tabela = ttk.Treeview(centro, columns=colunas, show="headings")
        
        self.tabela.tag_configure("par", background="#F0F0F0")
        self.tabela.tag_configure("impar", background="#A5A5A5")
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("contato", text="Contato")
        self.tabela.heading("email", text="Email")
        self.tabela.heading("datansc", text="Data de Nasc.")
        self.tabela.heading("peso", text="Peso")
        self.tabela.heading("altura", text="Altura")
        
        self.tabela.column("id", width=40, anchor="center", stretch=False)
        self.tabela.column("nome", width=200, minwidth=150, anchor="center")
        self.tabela.column("contato", width=75, anchor="center")
        self.tabela.column("email", width=75, anchor="center")
        self.tabela.column("datansc", width=75, minwidth=150, anchor="center")
        self.tabela.column("peso", width=75, anchor="center")
        self.tabela.column("altura", width=75, anchor="center")
        
        self.tabela.insert('', 'end', text='Listbox', values=('1', '15KB Yesterday', 'teste'))
        self.tabela.insert('', 'end', text='Listbox', values=('2', '15KB Yeste', 'teste'))
        
        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)
        
    def abrir_informacoes(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione alguma maquina para ver as informações!")
            return
