import customtkinter as ctk

from cores import *

class CadastrarAluno(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color=FUNDO)
        
        # Frame do centro
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=600, width=800)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)
        
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")
        
        ctk.CTkLabel(topo, text="Cadastro de Aluno", font=("Inter", 20, "bold")).place(anchor="center", relx=0.3, y=30)

        btn_salvar = ctk.CTkButton(topo, text="Salvar", font=("Inter", 17, "bold"))
        btn_salvar.place(anchor="center", relx=0.6, y=30)
        
        btn_voltar = ctk.CTkButton(topo, text="Voltar", font=("Inter", 17, "bold"), command= lambda: master.mostrar_menu())
        btn_voltar.place(anchor="center", relx=0.8, y=30)
        
        """Tela que cadastra os dados pessoais, nessa parte iremos cadastrar os dados: 
        Nome completo, Data de Nascimento, Estado Civil, Nacionalidade, CPF, Contato, Endereço, Telefone, E-mail,
        Contato de emergência, Nome do contato de emergencia, Grau de parentesco, Doenças, Medicações, Peso, Altura, Objetivo"""
        
        # Labels da esquerda
        labels_esquerda = [
            ("Nome completo:"),
            ("Data de Nascimento:"),
            ("Estado Civil:"),
            ("Nacionalidade:"),
            ("Contato:"),
            ("Telefone:"),
            ("Endereço:"),
            ("Objetivo:")
        ]
        y = 80
        # Laço for das labels da esquerda
        for nome in labels_esquerda:
            ctk.CTkLabel(centro, text=nome, text_color=TEXTO, font=("Inter", 16, "bold")).place(x=20, y=y)
            y += 60
        
        # Labels da direita
        labels_direita = [
            ("E-mail:"),
            ("Contato de Emergência:"),
            ("Nome do contato de emegência:"),
            ("Grau de Parentesco:"),
            ("Doenças:"),
            ("Medicações:"),
            ("Peso:"),
            ("Altura:")
        ]
        
        # Laço for das labels da direita
        y = 80
        for nome in labels_direita:
            ctk.CTkLabel(centro, text=nome, text_color=TEXTO, font=("Inter", 16, "bold")).place(x=400, y=y)
            y += 60
        
        campos = {}
        
        entradas_esquerda= [
            ("Nome"),
            ("DataNsc"),
            ("EstadoCivil"),
            ("Nacionalidade"),
            ("Contato"),
            ("Telefone"),
            ("Endereco"),
            ("Objetivo"),
            ]
        
        y = 110
        
        for nome in entradas_esquerda:
            entry = ctk.CTkEntry(centro, text_color="black", font=("Inter", 14),
                                width=300, fg_color="DarkGrey")
            entry.place(x=20, y=y)
            y += 60
            campos[nome] = entry
        
        entradas_direita = [
            ("E-mail:"),
            ("Contato de Emergência:"),
            ("Nome do contato de emegência:"),
            ("Grau de Parentesco:"),
            ("Doenças:"),
            ("Medicações:"),
            ("Peso:"),
            ("Altura:")
        ]

        y = 110
        for nome in entradas_esquerda:
            entry = ctk.CTkEntry(centro, text_color="black", font=("Inter", 14),
                                width=300, fg_color="DarkGrey")
            entry.place(x=400, y=y)
            y += 60
            campos[nome] = entry
        