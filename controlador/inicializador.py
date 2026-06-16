import customtkinter as ctk

from cores import *
from views.tela_login import LoginFrame
from views.menu_principal import MenuPrincipal
from views.informacoes import InformacaoAluno
from views.cadastrar_aluno import CadastrarAluno
from views.ver_treinos import VerTreinos
from views.gerar_treino import GerarTreino

from database.database import db_manager
from services.auth_service import AuthService
from services.usuario_service import UsuarioService
from services.treino_service import TreinoService
from services.perfil_service import PerfilService


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Academia - TrabalhoPSC")
        self.geometry("1300x800")
        self.configure(fg_color=FUNDO)

        db_manager.create_tables()

        self._session = db_manager.get_raw_session()

        self.auth_service    = AuthService(self._session)
        self.usuario_service = UsuarioService(self._session)
        self.treino_service  = TreinoService(self._session)
        self.perfil_service  = PerfilService(self._session)

        self.usuario_logado = None

        self._criar_admin_padrao()

        self.frame_atual = None
        self.mostrar_login()

    def trocar_tela(self, classe_tela, **kwargs):
        if self.frame_atual:
            # Sinaliza para callbacks pendentes que o frame será destruído
            try:
                self.frame_atual.destroy()
            except Exception:
                pass
        self.frame_atual = classe_tela(self, **kwargs)
        self.frame_atual.pack(fill="both", expand=True)

    def mostrar_login(self):
        self.trocar_tela(LoginFrame)

    def mostrar_menu(self):
        self.trocar_tela(MenuPrincipal)

    def mostrar_cadastrar_aluno(self):
        self.trocar_tela(CadastrarAluno)

    def mostrar_informacao_aluno(self, usuario_id: int):
        self.trocar_tela(InformacaoAluno, usuario_id=usuario_id)

    def mostrar_treinos(self, usuario_id: int):
        self.trocar_tela(VerTreinos, usuario_id=usuario_id)

    def mostrar_gerar_treino(self, usuario_id: int):
        self.trocar_tela(GerarTreino, usuario_id=usuario_id)

    def _criar_admin_padrao(self):
        try:
            todos = self.usuario_service.listar()
            if not todos:
                self.usuario_service.cadastrar(
                    nome_completo="Administrador",
                    cpf="529.982.247-25",
                    email="admin@academia.com",
                    usuario="admin",
                    senha="admin123",
                )
                self._session.commit()
                print("✅ Admin padrão criado — usuário: admin | senha: admin123")
            else:
                print(f"ℹ️  Banco já tem {len(todos)} usuário(s), pulando admin padrão.")
        except Exception as e:
            self._session.rollback()
            print(f"❌ Falha ao criar admin padrão: {type(e).__name__}: {e}")

    def on_closing(self):
        self._session.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
