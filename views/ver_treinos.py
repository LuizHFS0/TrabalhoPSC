import customtkinter as ctk
from tkinter import ttk, messagebox

from cores import *


class VerTreinos(ctk.CTkFrame):
    def __init__(self, master, usuario_id: int):
        super().__init__(master)
        self.configure(bg_color=FUNDO)

        self._usuario_id = usuario_id
        self._treino_service = master.treino_service

        # Busca o nome do aluno para exibir no título
        try:
            aluno = master.usuario_service.buscar_por_id(usuario_id)
            nome_aluno = aluno.nome_completo
        except Exception:
            nome_aluno = "Aluno"

        # ── Frame central ──────────────────────────────────────────────
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=650, width=950)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)

        # ── Topo ───────────────────────────────────────────────────────
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo, text=f"Treinos de {nome_aluno}",
            font=("Inter", 18, "bold")
        ).place(anchor="center", relx=0.3, y=35)

        ctk.CTkButton(
            topo, text="+ Novo Treino", font=("Inter", 14, "bold"),
            command=self._abrir_form_novo
        ).place(anchor="center", relx=0.55, y=35)

        ctk.CTkButton(
            topo, text="Excluir", font=("Inter", 14, "bold"), fg_color=VERMELHO,
            command=self._excluir_treino, text_color="black"
        ).place(anchor="center", relx=0.7, y=35)

        ctk.CTkButton(
            topo, text="Voltar", font=("Inter", 14, "bold"),
            command=lambda: master.mostrar_menu()
        ).place(anchor="center", relx=0.85, y=35)

        # ── Tabela de treinos ─────────────────────────────────────────
        style = ttk.Style()
        style.theme_use("clam")

        colunas = ("id", "nome_treino", "exercicio", "series", "repeticoes", "carga", "obs")
        self.tabela = ttk.Treeview(centro, columns=colunas, show="headings")

        self.tabela.tag_configure("par", background="#F0F0F0")
        self.tabela.tag_configure("impar", background="#A5A5A5")

        cabecalhos = {
            "id":          ("ID", 40),
            "nome_treino": ("Treino", 120),
            "exercicio":   ("Exercício", 200),
            "series":      ("Séries", 60),
            "repeticoes":  ("Reps", 60),
            "carga":       ("Carga (kg)", 80),
            "obs":         ("Observações", 200),
        }

        for col, (texto, largura) in cabecalhos.items():
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=largura, anchor="center", stretch=(col in ("exercicio", "obs")))

        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        # Carrega os treinos do aluno
        self._carregar_treinos()

    # ------------------------------------------------------------------

    def _carregar_treinos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        treinos = self._treino_service.listar_treinos(self._usuario_id)

        for i, t in enumerate(treinos):
            tag = "par" if i % 2 == 0 else "impar"
            self.tabela.insert(
                "", "end",
                iid=str(t.id),
                values=(
                    t.id,
                    t.nome_treino,
                    t.exercicio,
                    t.series,
                    t.repeticoes,
                    f"{t.carga} kg" if t.carga else "—",
                    t.observacoes or "—",
                ),
                tags=(tag,),
            )

    def _excluir_treino(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um treino para excluir.")
            return

        treino_id = int(selecao[0])
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este treino?")
        if not confirmar:
            return

        try:
            self._treino_service.excluir_treino(treino_id)
            self._carregar_treinos()
            messagebox.showinfo("Sucesso", "Treino excluído.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _abrir_form_novo(self):
        """Abre janela modal para cadastrar novo treino."""
        modal = ctk.CTkToplevel(self)
        modal.title("Novo Treino")
        modal.geometry("400x480")
        modal.grab_set()  # bloqueia a janela principal enquanto o modal está aberto

        campos_config = [
            ("nome_treino",  "Nome do Treino (ex: Treino A):"),
            ("exercicio",    "Exercício:"),
            ("series",       "Séries:"),
            ("repeticoes",   "Repetições:"),
            ("carga",        "Carga (kg) — opcional:"),
            ("observacoes",  "Observações — opcional:"),
        ]

        entradas = {}
        for chave, label_txt in campos_config:
            ctk.CTkLabel(modal, text=label_txt, font=("Inter", 13, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
            entry = ctk.CTkEntry(modal, width=360)
            entry.pack(padx=20)
            entradas[chave] = entry

        def salvar():
            dados = {k: e.get().strip() for k, e in entradas.items()}

            obrigatorios = ["nome_treino", "exercicio", "series", "repeticoes"]
            if any(not dados[k] for k in obrigatorios):
                messagebox.showwarning("Aviso", "Preencha nome do treino, exercício, séries e repetições.", parent=modal)
                return

            try:
                self._treino_service.criar_treino(
                    usuario_id=self._usuario_id,
                    nome_treino=dados["nome_treino"],
                    exercicio=dados["exercicio"],
                    series=int(dados["series"]),
                    repeticoes=int(dados["repeticoes"]),
                    carga=float(dados["carga"]) if dados["carga"] else None,
                    observacoes=dados["observacoes"] or None,
                )
                modal.destroy()
                self._carregar_treinos()
                messagebox.showinfo("Sucesso", "Treino cadastrado!")
            except ValueError as e:
                messagebox.showerror("Erro", f"Dados inválidos: {e}", parent=modal)
            except Exception as e:
                messagebox.showerror("Erro inesperado", str(e), parent=modal)

        ctk.CTkButton(modal, text="Salvar", command=salvar, fg_color=AZUL, text_color="black").pack(pady=20)