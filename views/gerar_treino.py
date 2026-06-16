import threading
import customtkinter as ctk
from tkinter import messagebox, ttk

from cores import *
from utils.api_treino import gerar_treino_completo


class GerarTreino(ctk.CTkFrame):
    def __init__(self, master, usuario_id: int):
        super().__init__(master)
        self.configure(fg_color=FUNDO)
        self.usuario_id = usuario_id
        self._treino_gerado = []

        self._objetivo = "saúde geral"
        self._nivel = "iniciante"
        self._carregar_perfil()

        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, corner_radius=12)
        centro.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.88)

        topo = ctk.CTkFrame(centro, height=65, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(10, 0))
        topo.pack_propagate(False)

        ctk.CTkLabel(
            topo, text="⚡ Gerador de Treino com IA",
            font=("Inter", 22, "bold"), text_color=VERDE,
        ).pack(side="left", pady=10)

        ctk.CTkButton(
            topo, text="← Voltar",
            font=("Inter", 14, "bold"),
            fg_color=FUNDO_INPUT, text_color=TEXTO, hover_color=BORDA,
            width=110, command=lambda: master.mostrar_menu(),
        ).pack(side="right", pady=10)

        frame_perfil = ctk.CTkFrame(centro, fg_color=FUNDO_INPUT, corner_radius=8)
        frame_perfil.pack(fill="x", padx=20, pady=(5, 10))

        ctk.CTkLabel(
            frame_perfil, text="Perfil do Aluno",
            font=("Inter", 14, "bold"), text_color=VERDE,
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.label_perfil = ctk.CTkLabel(
            frame_perfil, text=self._info_perfil,
            font=("Inter", 13), text_color=TEXTO, justify="left",
        )
        self.label_perfil.pack(anchor="w", padx=15, pady=(0, 10))

        self.btn_gerar = ctk.CTkButton(
            centro, text="🏋️  Gerar Treino com IA",
            font=("Inter", 16, "bold"),
            fg_color=VERDE, text_color="black", hover_color=VERDE_HOVER,
            height=48, command=self._iniciar_geracao,
        )
        self.btn_gerar.pack(fill="x", padx=20, pady=(0, 5))

        self.label_status = ctk.CTkLabel(
            centro, text="", font=("Inter", 13), text_color=TEXTO_MUTED,
        )
        self.label_status.pack()

        frame_tabela = ctk.CTkFrame(centro, fg_color="transparent")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=(5, 5))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treino.Treeview",
            background=FUNDO_INPUT, fieldbackground=FUNDO_INPUT,
            foreground=TEXTO, rowheight=30, font=("Inter", 12),
        )
        style.configure("Treino.Treeview.Heading",
            background=FUNDO_CARD, foreground=VERDE, font=("Inter", 12, "bold"),
        )
        style.map("Treino.Treeview", background=[("selected", VERDE_DARK)])

        colunas = ("exercicio", "musculo", "series", "reps", "observacoes")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", style="Treino.Treeview")

        self.tabela.heading("exercicio",   text="Exercício")
        self.tabela.heading("musculo",     text="Músculo")
        self.tabela.heading("series",      text="Séries")
        self.tabela.heading("reps",        text="Repetições")
        self.tabela.heading("observacoes", text="Observações")

        self.tabela.column("exercicio",   width=220, anchor="w")
        self.tabela.column("musculo",     width=120, anchor="center")
        self.tabela.column("series",      width=60,  anchor="center")
        self.tabela.column("reps",        width=80,  anchor="center")
        self.tabela.column("observacoes", width=250, anchor="w")

        scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.btn_salvar = ctk.CTkButton(
            centro, text="💾  Salvar Treino no Banco",
            font=("Inter", 15, "bold"),
            fg_color=AZUL, text_color="black", hover_color="#7DD3FC",
            height=44, state="disabled", command=self._salvar_treino,
        )
        self.btn_salvar.pack(fill="x", padx=20, pady=(8, 15))

    def _carregar_perfil(self):
        try:
            perfil = self.master.perfil_service.buscar_perfil(self.usuario_id)
            self._objetivo = perfil.objetivo or "saúde geral"
            self._nivel    = perfil.nivel    or "iniciante"
            self._info_perfil = (
                f"Peso: {perfil.peso} kg   |   Altura: {perfil.altura} cm   |   "
                f"Idade: {perfil.idade} anos   |   Objetivo: {self._objetivo}   |   Nível: {self._nivel}"
            )
        except Exception:
            self._objetivo    = "saúde geral"
            self._nivel       = "iniciante"
            self._info_perfil = "Perfil físico não encontrado. Usando configuração padrão."

    def _iniciar_geracao(self):
        self.btn_gerar.configure(state="disabled", text="⏳  Buscando exercícios...")
        self.btn_salvar.configure(state="disabled")
        self.label_status.configure(text="Conectando à API e montando seu treino...", text_color=AZUL)

        for row in self.tabela.get_children():
            self.tabela.delete(row)

        threading.Thread(target=self._gerar_thread, daemon=True).start()

    def _gerar_thread(self):
        try:
            treino = gerar_treino_completo(objetivo=self._objetivo, nivel=self._nivel)
            self.after(0, self._exibir_treino, treino)
        except Exception as e:
            self.after(0, self._erro_geracao, str(e))

    def _exibir_treino(self, treino: list):
        self._treino_gerado = treino

        if not treino:
            self.label_status.configure(
                text="Não foi possível buscar exercícios. Verifique sua conexão.",
                text_color=VERMELHO,
            )
            self.btn_gerar.configure(state="normal", text="🏋️  Gerar Treino com IA")
            return

        for i, ex in enumerate(treino):
            tag = "par" if i % 2 == 0 else "impar"
            self.tabela.insert("", "end", values=(
                ex["exercicio"], ex["musculo"],
                ex["series"], ex["repeticoes"], ex["observacoes"],
            ), tags=(tag,))

        self.tabela.tag_configure("par",   background=FUNDO_INPUT)
        self.tabela.tag_configure("impar", background=FUNDO_CARD)

        self.label_status.configure(
            text=f"✅ {len(treino)} exercícios gerados com sucesso!",
            text_color=VERDE,
        )
        self.btn_gerar.configure(state="normal", text="🔄  Gerar Novo Treino")
        self.btn_salvar.configure(state="normal")

    def _erro_geracao(self, msg: str):
        self.label_status.configure(text=f"Erro ao gerar treino: {msg}", text_color=VERMELHO)
        self.btn_gerar.configure(state="normal", text="🏋️  Gerar Treino com IA")

    def _salvar_treino(self):
        if not self._treino_gerado:
            return
        try:
            for ex in self._treino_gerado:
                self.master.treino_service.criar_treino(
                    usuario_id=self.usuario_id,
                    nome_treino=ex["nome_treino"],
                    exercicio=ex["exercicio"],
                    series=ex["series"],
                    repeticoes=ex["repeticoes"],
                    carga=ex.get("carga"),
                    observacoes=ex.get("observacoes"),
                )
            messagebox.showinfo("Treino Salvo!", f"✅ {len(self._treino_gerado)} exercícios salvos com sucesso!")
            self.btn_salvar.configure(state="disabled", text="✅  Treino Salvo!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o treino:\n{e}")
