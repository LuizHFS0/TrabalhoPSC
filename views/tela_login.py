import customtkinter as ctk
import time

from cores import *
from utils.exceptions import LoginInvalidoError

data = time.strftime("%d/%m/%Y")


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame do centro
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=500, width=400, corner_radius=12)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)

        ctk.CTkLabel(centro, text="LOGIN", font=("Inter", 20, "bold")).pack(pady=20)

        ctk.CTkLabel(centro, text="Usuário:", font=("Inter", 13), text_color=TEXTO).pack(pady=(20, 0))
        self.entrada_usuario = ctk.CTkEntry(centro)
        self.entrada_usuario.pack(pady=10)

        ctk.CTkLabel(centro, text="Senha:", font=("Inter", 13), text_color=TEXTO).pack(pady=(20, 0))
        # show="*" esconde a senha com asteriscos
        self.entrada_senha = ctk.CTkEntry(centro, show="*")
        self.entrada_senha.pack(pady=10)

        # Label de erro — fica invisível até acontecer um erro
        self.label_erro = ctk.CTkLabel(centro, text="", text_color="red", font=("Inter", 12))
        self.label_erro.pack(pady=(5, 0))

        ctk.CTkButton(
            centro, text="Entrar", text_color="black", fg_color=VERDE,
            command=self._fazer_login
        ).pack(pady=20)

        ctk.CTkButton(
            centro, text="Sair", text_color="black", fg_color=VERMELHO,
            command=master.destroy
        ).pack(pady=10)

        ctk.CTkLabel(
            self, text="Feito por: Luiz Henrique, Gabriel Messias, Lucas Batista"
        ).place(relx=0.5, rely=0.97, anchor="center")

        # Permite pressionar Enter para logar
        self.entrada_senha.bind("<Return>", lambda e: self._fazer_login())

    def _fazer_login(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not usuario or not senha:
            self.label_erro.configure(text="Preencha usuário e senha.")
            return

        try:
            # Usa o AuthService que já está no master (App)
            # A view não cria o service — só usa o que recebeu
            usuario_obj = self.master.auth_service.autenticar(usuario, senha)

            # Salva o usuário logado no App para as outras telas acessarem
            self.master.usuario_logado = usuario_obj

            self.master.mostrar_menu()

        except LoginInvalidoError:
            self.label_erro.configure(text="Usuário ou senha inválidos.")
        except Exception as e:
            self.label_erro.configure(text=f"Erro inesperado: {e}")