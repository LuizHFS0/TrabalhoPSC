import customtkinter as ctk
from tkinter import messagebox

from cores import *
from utils.exceptions import CPFJaExisteError, EmailJaExisteError, UsuarioJaExisteError


class CadastrarAluno(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color=FUNDO)

        # Service recebido via master — a view não cria nada
        self._usuario_service = master.usuario_service

        # ── Frame central ──────────────────────────────────────────────
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=650, width=850)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)

        # ── Topo ───────────────────────────────────────────────────────
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")

        ctk.CTkLabel(topo, text="Cadastro de Aluno", font=("Inter", 20, "bold")).place(
            anchor="center", relx=0.3, y=35
        )
        ctk.CTkButton(
            topo, text="Salvar", font=("Inter", 17, "bold"),
            command=self._salvar
        ).place(anchor="center", relx=0.6, y=35)

        ctk.CTkButton(
            topo, text="Voltar", font=("Inter", 17, "bold"),
            command=lambda: master.mostrar_menu()
        ).place(anchor="center", relx=0.8, y=35)

        # ── Labels + Entradas ──────────────────────────────────────────
        # Cada item: (chave_interna, label_exibido, coluna_x, entrada_x)
        # Coluna esquerda: x_label=20, x_entry=20
        # Coluna direita:  x_label=430, x_entry=430

        campos_esquerda = [
            ("nome_completo",   "Nome completo:"),
            ("cpf",             "CPF:"),
            ("data_nascimento", "Data de Nascimento (DD/MM/AAAA):"),
            ("estado_civil",    "Estado Civil:"),
            ("nacionalidade",   "Nacionalidade:"),
            ("telefone",        "Telefone:"),
            ("endereco",        "Endereço:"),
            ("usuario",         "Usuário (login):"),
        ]

        campos_direita = [
            ("email",                   "E-mail:"),
            ("contato_emergencia",      "Contato de Emergência:"),
            ("nome_contato_emergencia", "Nome do Contato de Emergência:"),
            ("grau_parentesco",         "Grau de Parentesco:"),
            ("senha",                   "Senha:"),
            ("peso",                    "Peso (kg):"),
            ("altura",                  "Altura (cm):"),
            ("objetivo",                "Objetivo:"),
        ]

        # Dicionário que mapeia chave → widget CTkEntry
        self.campos: dict[str, ctk.CTkEntry] = {}

        self._criar_coluna(centro, campos_esquerda, x_label=20, x_entry=20, y_inicio=80)
        self._criar_coluna(centro, campos_direita, x_label=430, x_entry=430, y_inicio=80)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _criar_coluna(self, pai, campos, x_label, x_entry, y_inicio):
        """Cria labels e entradas de uma coluna."""
        y = y_inicio
        for chave, label_texto in campos:
            ctk.CTkLabel(
                pai, text=label_texto, text_color=TEXTO, font=("Inter", 13, "bold")
            ).place(x=x_label, y=y)

            # Campo de senha fica oculto
            show = "*" if chave == "senha" else ""
            entry = ctk.CTkEntry(
                pai, font=("Inter", 13), width=300, fg_color="DarkGrey",
                text_color="black", show=show
            )
            entry.place(x=x_entry, y=y + 25)

            # Guarda o widget pelo nome da chave
            self.campos[chave] = entry
            y += 70

    def _salvar(self):
        """Lê os campos, valida e chama o UsuarioService."""
        dados = {chave: entry.get().strip() for chave, entry in self.campos.items()}

        # Validação mínima dos obrigatórios
        obrigatorios = ["nome_completo", "cpf", "email", "usuario", "senha"]
        faltando = [k for k in obrigatorios if not dados[k]]
        if faltando:
            messagebox.showwarning("Aviso", f"Preencha os campos obrigatórios: {', '.join(faltando)}")
            return

        # Converte data de nascimento se preenchida
        from datetime import datetime
        data_nasc = None
        if dados["data_nascimento"]:
            try:
                data_nasc = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y").date()
            except ValueError:
                messagebox.showerror("Erro", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
                return

        try:
            self._usuario_service.cadastrar(
                nome_completo=dados["nome_completo"],
                cpf=dados["cpf"],
                email=dados["email"],
                usuario=dados["usuario"],
                senha=dados["senha"],
                # Campos opcionais passados como kwargs
                data_nascimento=data_nasc,
                estado_civil=dados["estado_civil"] or None,
                nacionalidade=dados["nacionalidade"] or None,
                telefone=dados["telefone"] or None,
                endereco=dados["endereco"] or None,
                contato_emergencia=dados["contato_emergencia"] or None,
                nome_contato_emergencia=dados["nome_contato_emergencia"] or None,
                grau_parentesco=dados["grau_parentesco"] or None,
            )
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.master.mostrar_menu()

        except CPFJaExisteError:
            messagebox.showerror("Erro", "Este CPF já está cadastrado.")
        except EmailJaExisteError:
            messagebox.showerror("Erro", "Este e-mail já está cadastrado.")
        except UsuarioJaExisteError:
            messagebox.showerror("Erro", "Este nome de usuário já existe.")
        except ValueError as e:
            messagebox.showerror("Erro de validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))