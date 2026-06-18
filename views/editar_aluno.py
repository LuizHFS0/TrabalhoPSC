import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from cores import *


class EditarAluno(ctk.CTkFrame):
    """Tela de edição de dados do aluno — fecha o 'U' do CRUD."""

    def __init__(self, master, usuario_id: int):
        super().__init__(master)
        self.configure(bg_color=FUNDO)

        self._usuario_id = usuario_id
        self._usuario_service = master.usuario_service
        self._perfil_service  = master.perfil_service

        # Carrega aluno do banco
        try:
            self._aluno = self._usuario_service.buscar_por_id(usuario_id)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o aluno: {e}")
            master.mostrar_menu()
            return

        self._perfil = None
        try:
            self._perfil = self._perfil_service.buscar_perfil(usuario_id)
        except Exception:
            pass  # perfil pode não existir ainda

        # ── Frame central ──────────────────────────────────────────────
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=650, width=850)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)

        # ── Topo ───────────────────────────────────────────────────────
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo, text=f"Editar: {self._aluno.nome_completo}",
            font=("Inter", 18, "bold")
        ).place(anchor="center", relx=0.3, y=35)

        ctk.CTkButton(
            topo, text="Salvar", font=("Inter", 17, "bold"),
            fg_color=VERDE, text_color="black",
            command=self._salvar
        ).place(anchor="center", relx=0.6, y=35)

        ctk.CTkButton(
            topo, text="Voltar", font=("Inter", 17, "bold"),
            command=lambda: master.mostrar_informacao_aluno(usuario_id)
        ).place(anchor="center", relx=0.8, y=35)

        # ── Campos ────────────────────────────────────────────────────
        # Coluna esquerda: dados pessoais
        campos_esquerda = [
            ("nome_completo",   "Nome completo:"),
            ("cpf",             "CPF:"),
            ("data_nascimento", "Data de Nascimento (DD/MM/AAAA):"),
            ("estado_civil",    "Estado Civil:"),
            ("nacionalidade",   "Nacionalidade:"),
            ("telefone",        "Telefone:"),
            ("endereco",        "Endereço:"),
            ("email",           "E-mail:"),
        ]

        # Coluna direita: contato emergência + perfil físico
        campos_direita = [
            ("contato_emergencia",      "Contato de Emergência:"),
            ("nome_contato_emergencia", "Nome do Contato:"),
            ("grau_parentesco",         "Grau de Parentesco:"),
            ("peso",                    "Peso (kg):"),
            ("altura",                  "Altura (cm):"),
            ("objetivo",                "Objetivo:"),
            ("nivel",                   "Nível (iniciante/intermediário/avançado):"),
            ("doencas",                 "Doenças / Condições:"),
        ]

        self.campos: dict[str, ctk.CTkEntry] = {}

        self._criar_coluna(centro, campos_esquerda, x_label=20,  x_entry=20,  y_inicio=80)
        self._criar_coluna(centro, campos_direita,  x_label=430, x_entry=430, y_inicio=80)

        # Preenche os campos com os valores atuais do banco
        self._preencher_valores()

    # ------------------------------------------------------------------

    def _criar_coluna(self, pai, campos, x_label, x_entry, y_inicio):
        y = y_inicio
        for chave, label_texto in campos:
            ctk.CTkLabel(
                pai, text=label_texto, text_color=TEXTO, font=("Inter", 13, "bold")
            ).place(x=x_label, y=y)

            entry = ctk.CTkEntry(
                pai, font=("Inter", 13), width=300,
                fg_color="DarkGrey", text_color="black"
            )
            entry.place(x=x_entry, y=y + 25)
            self.campos[chave] = entry
            y += 70

    def _preencher_valores(self):
        """Insere os dados atuais do aluno em cada campo."""
        a = self._aluno
        p = self._perfil

        # Dados do usuário
        mapa_usuario = {
            "nome_completo":           a.nome_completo,
            "cpf":                     a.cpf,
            "data_nascimento":         a.data_nascimento.strftime("%d/%m/%Y") if a.data_nascimento else "",
            "estado_civil":            a.estado_civil or "",
            "nacionalidade":           a.nacionalidade or "",
            "telefone":                a.telefone or "",
            "endereco":                a.endereco or "",
            "email":                   a.email,
            "contato_emergencia":      a.contato_emergencia or "",
            "nome_contato_emergencia": a.nome_contato_emergencia or "",
            "grau_parentesco":         a.grau_parentesco or "",
        }

        # Dados do perfil físico (se existir)
        mapa_perfil = {
            "peso":     str(p.peso)        if p else "",
            "altura":   str(p.altura)      if p else "",
            "objetivo": p.objetivo or ""   if p else "",
            "nivel":    p.nivel    or ""   if p else "",
            "doencas":  p.doencas  or ""   if p else "",
        }

        for chave, valor in {**mapa_usuario, **mapa_perfil}.items():
            if chave in self.campos:
                self.campos[chave].delete(0, "end")
                self.campos[chave].insert(0, valor)

    def _calcular_idade(self, data_nasc) -> int:
        hoje = datetime.today().date()
        idade = hoje.year - data_nasc.year
        if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
            idade -= 1
        return idade

    def _salvar(self):
        dados = {chave: entry.get().strip() for chave, entry in self.campos.items()}

        # Valida obrigatórios
        obrigatorios = ["nome_completo", "cpf", "email"]
        faltando = [k for k in obrigatorios if not dados[k]]
        if faltando:
            messagebox.showwarning("Aviso", f"Preencha os campos obrigatórios: {', '.join(faltando)}")
            return

        # Converte data de nascimento
        data_nasc = None
        if dados["data_nascimento"]:
            try:
                data_nasc = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y").date()
            except ValueError:
                messagebox.showerror("Erro", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
                return

        try:
            # ── Atualiza dados do usuário ──────────────────────────────
            self._usuario_service.atualizar(
                self._usuario_id,
                nome_completo=dados["nome_completo"],
                cpf=dados["cpf"],
                email=dados["email"],
                data_nascimento=data_nasc,
                estado_civil=dados["estado_civil"] or None,
                nacionalidade=dados["nacionalidade"] or None,
                telefone=dados["telefone"] or None,
                endereco=dados["endereco"] or None,
                contato_emergencia=dados["contato_emergencia"] or None,
                nome_contato_emergencia=dados["nome_contato_emergencia"] or None,
                grau_parentesco=dados["grau_parentesco"] or None,
            )
            # Commit dos dados do usuário
            self._usuario_service._session.commit()

            # ── Atualiza ou cria o perfil físico ──────────────────────
            campos_perfil = {}
            if dados["peso"]:
                try:
                    campos_perfil["peso"] = float(dados["peso"])
                except ValueError:
                    messagebox.showerror("Erro", "Peso deve ser um número (ex: 72.5).")
                    return
            if dados["altura"]:
                try:
                    campos_perfil["altura"] = float(dados["altura"])
                except ValueError:
                    messagebox.showerror("Erro", "Altura deve ser um número (ex: 175.0).")
                    return
            if dados["objetivo"]:
                campos_perfil["objetivo"] = dados["objetivo"]
            if dados["nivel"]:
                campos_perfil["nivel"] = dados["nivel"]
            if dados["doencas"]:
                campos_perfil["doencas"] = dados["doencas"]

            if campos_perfil:
                if self._perfil:
                    # Perfil já existe → atualiza
                    self._perfil_service.atualizar_perfil(self._usuario_id, **campos_perfil)
                else:
                    # Perfil ainda não existe → cria
                    idade = self._calcular_idade(data_nasc) if data_nasc else 18
                    self._perfil_service.cadastrar_perfil(
                        usuario_id=self._usuario_id,
                        idade=idade,
                        peso=campos_perfil.get("peso", 70.0),
                        altura=campos_perfil.get("altura", 170.0),
                        objetivo=campos_perfil.get("objetivo"),
                        nivel=campos_perfil.get("nivel"),
                        doencas=campos_perfil.get("doencas"),
                    )

            messagebox.showinfo("Sucesso", "Dados do aluno atualizados com sucesso!")
            self.master.mostrar_informacao_aluno(self._usuario_id)

        except ValueError as e:
            messagebox.showerror("Erro de validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))