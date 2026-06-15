import customtkinter as ctk
from tkinter import messagebox

from cores import *


class InformacaoAluno(ctk.CTkFrame):
    def __init__(self, master, usuario_id: int):
        super().__init__(master)
        self.configure(bg_color=FUNDO)

        # Busca o aluno no banco usando o service do master
        # A view não cria service — usa o que o App já tem
        try:
            self._aluno = master.usuario_service.buscar_por_id(usuario_id)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o aluno: {e}")
            master.mostrar_menu()
            return

        # ── Frame central ──────────────────────────────────────────────
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=650, width=850)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)

        # ── Topo ───────────────────────────────────────────────────────
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo,
            text=f"Informações de {self._aluno.nome_completo}",
            font=("Inter", 18, "bold")
        ).place(anchor="center", relx=0.35, y=35)

        ctk.CTkButton(
            topo, text="Ver Treinos", font=("Inter", 15, "bold"),
            command=lambda: master.mostrar_treinos(usuario_id)
        ).place(anchor="center", relx=0.65, y=35)

        ctk.CTkButton(
            topo, text="Voltar", font=("Inter", 15, "bold"),
            command=lambda: master.mostrar_menu()
        ).place(anchor="center", relx=0.82, y=35)

        # ── Dados do aluno ─────────────────────────────────────────────
        a = self._aluno
        p = a.perfil  # pode ser None se o perfil físico não foi cadastrado

        data_nasc = a.data_nascimento.strftime("%d/%m/%Y") if a.data_nascimento else "—"

        # (label, valor) — coluna esquerda
        info_esquerda = [
            ("Nome completo:",       a.nome_completo),
            ("Data de Nascimento:",  data_nasc),
            ("Estado Civil:",        a.estado_civil or "—"),
            ("Nacionalidade:",       a.nacionalidade or "—"),
            ("Telefone:",            a.telefone or "—"),
            ("Endereço:",            a.endereco or "—"),
            ("Usuário:",             a.usuario),
            ("Membro desde:",        a.criado_em.strftime("%d/%m/%Y") if a.criado_em else "—"),
        ]

        # (label, valor) — coluna direita
        info_direita = [
            ("E-mail:",                     a.email),
            ("Contato de Emergência:",      a.contato_emergencia or "—"),
            ("Nome do Contato:",            a.nome_contato_emergencia or "—"),
            ("Grau de Parentesco:",         a.grau_parentesco or "—"),
            ("Peso:",                       f"{p.peso} kg" if p else "—"),
            ("Altura:",                     f"{p.altura} cm" if p else "—"),
            ("Doenças:",                    p.doencas or "—" if p else "—"),
            ("Medicações:",                 p.medicacoes or "—" if p else "—"),
        ]

        self._criar_coluna(centro, info_esquerda, x_label=20,  y_inicio=80)
        self._criar_coluna(centro, info_direita,  x_label=430, y_inicio=80)

    # ------------------------------------------------------------------

    def _criar_coluna(self, pai, itens, x_label, y_inicio):
        y = y_inicio
        for label_texto, valor in itens:
            ctk.CTkLabel(
                pai, text=label_texto, text_color=TEXTO,
                font=("Inter", 13, "bold")
            ).place(x=x_label, y=y)

            ctk.CTkLabel(
                pai, text=valor, text_color=TEXTO,
                font=("Inter", 13), wraplength=280, justify="left"
            ).place(x=x_label, y=y + 22)

            y += 68