import customtkinter as ctk
from tkinter import ttk, messagebox

from cores import *


class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color=FUNDO)

        # Guarda referência ao service — recebido via master (App)
        # A view NÃO cria o service, só usa
        self._usuario_service = master.usuario_service

        # Todos os alunos carregados (usado para a pesquisa local)
        self._todos_alunos = []

        # ── Frame central ──────────────────────────────────────────────
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=700, width=1000)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)

        # Título
        ctk.CTkLabel(centro, text="ALUNOS", font=("Inter", 25, "bold")).place(
            relx=0.5, y=35, anchor="center"
        )

        # ── Barra de botões + pesquisa ─────────────────────────────────
        frame_botoes = ctk.CTkFrame(centro, height=60, fg_color="transparent")
        frame_botoes.pack(side="top", fill="x", anchor="center", pady=(60, 0))
        frame_botoes.pack_propagate(False)

        # Campo de pesquisa
        frame_pesquisa = ctk.CTkFrame(frame_botoes, fg_color="transparent")
        frame_pesquisa.pack(side="left", padx=20)

        ctk.CTkLabel(frame_pesquisa, text="Pesquisar:", font=("Inter", 14, "bold")).pack(anchor="w")

        self.entrada_pesquisa = ctk.CTkEntry(frame_pesquisa, width=250, height=40)
        self.entrada_pesquisa.pack()
        # Pesquisa a cada tecla digitada
        self.entrada_pesquisa.bind("<KeyRelease>", lambda e: self._filtrar())

        # Botões de ação
        botoes = [
            ("+ Novo Aluno", lambda: master.mostrar_cadastrar_aluno(), AZUL),
            ("Informações", self._abrir_informacoes, AZUL),
            ("Ver Treinos", self._abrir_treinos, AZUL),
            ("Sair", master.destroy, VERMELHO),
        ]

        for nome, comando, cor in botoes:
            ctk.CTkButton(
                frame_botoes, text=nome, height=50, fg_color=cor,
                width=50, command=comando, text_color="black"
            ).pack(side="left", fill="x", padx=10)

        # ── Tabela ────────────────────────────────────────────────────
        style = ttk.Style()
        style.theme_use("clam")

        colunas = ("id", "nome", "contato", "email", "datansc", "peso", "altura")
        self.tabela = ttk.Treeview(centro, columns=colunas, show="headings")

        self.tabela.tag_configure("par", background="#F0F0F0")
        self.tabela.tag_configure("impar", background="#A5A5A5")

        cabecalhos = {
            "id": ("ID", 40),
            "nome": ("Nome", 200),
            "contato": ("Contato", 100),
            "email": ("Email", 180),
            "datansc": ("Data de Nasc.", 110),
            "peso": ("Peso", 70),
            "altura": ("Altura", 70),
        }

        for col, (texto, largura) in cabecalhos.items():
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=largura, anchor="center", stretch=(col == "nome"))

        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        # Carrega os dados reais do banco ao abrir a tela
        self._carregar_alunos()

    # ------------------------------------------------------------------
    # Métodos privados
    # ------------------------------------------------------------------

    def _carregar_alunos(self):
        """Busca todos os usuários no banco e preenche a tabela."""
        self._todos_alunos = self._usuario_service.listar()
        self._preencher_tabela(self._todos_alunos)

    def _preencher_tabela(self, alunos):
        """Limpa a tabela e insere a lista de alunos recebida."""
        # Apaga todas as linhas atuais
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for i, aluno in enumerate(alunos):
            tag = "par" if i % 2 == 0 else "impar"

            # Pega peso e altura do perfil se existir
            peso = ""
            altura = ""
            if aluno.perfil:
                peso = f"{aluno.perfil.peso} kg"
                altura = f"{aluno.perfil.altura} cm"

            data_nasc = aluno.data_nascimento.strftime("%d/%m/%Y") if aluno.data_nascimento else ""

            self.tabela.insert(
                "", "end",
                iid=str(aluno.id),   # usa o ID do banco como identificador da linha
                values=(
                    aluno.id,
                    aluno.nome_completo,
                    aluno.telefone or "",
                    aluno.email,
                    data_nasc,
                    peso,
                    altura,
                ),
                tags=(tag,),
            )

    def _filtrar(self):
        """Filtra a tabela localmente pelo texto digitado (sem ir ao banco)."""
        texto = self.entrada_pesquisa.get().strip().lower()
        if not texto:
            self._preencher_tabela(self._todos_alunos)
            return

        filtrados = [
            a for a in self._todos_alunos
            if texto in a.nome_completo.lower() or texto in (a.email or "").lower()
        ]
        self._preencher_tabela(filtrados)

    def _get_id_selecionado(self) -> int | None:
        """Retorna o ID do aluno selecionado na tabela, ou None."""
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um aluno primeiro!")
            return None
        # O iid da linha é o ID do banco (definimos assim em _preencher_tabela)
        return int(selecao[0])

    def _abrir_informacoes(self):
        usuario_id = self._get_id_selecionado()
        if usuario_id is not None:
            self.master.mostrar_informacao_aluno(usuario_id)

    def _abrir_treinos(self):
        usuario_id = self._get_id_selecionado()
        if usuario_id is not None:
            self.master.mostrar_treinos(usuario_id)