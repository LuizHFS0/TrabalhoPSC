from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_completo: Mapped[str] = mapped_column(String(150), nullable=False)
    data_nascimento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estado_civil: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    nacionalidade: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    telefone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    endereco: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contato_emergencia: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    nome_contato_emergencia: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    grau_parentesco: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    usuario: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    perfil: Mapped[Optional["PerfilFisico"]] = relationship(
        "PerfilFisico", back_populates="usuario", uselist=False, cascade="all, delete-orphan"
    )
    treinos: Mapped[list["Treino"]] = relationship(
        "Treino", back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} usuario='{self.usuario}' email='{self.email}'>"


class PerfilFisico(Base):
    __tablename__ = "perfis_fisicos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    objetivo: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    nivel: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    doencas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medicacoes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="perfil")

    def __repr__(self) -> str:
        return f"<PerfilFisico id={self.id} usuario_id={self.usuario_id} peso={self.peso}kg altura={self.altura}cm>"


class Treino(Base):
    __tablename__ = "treinos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    nome_treino: Mapped[str] = mapped_column(String(100), nullable=False)
    exercicio: Mapped[str] = mapped_column(String(150), nullable=False)
    series: Mapped[int] = mapped_column(Integer, nullable=False)
    repeticoes: Mapped[int] = mapped_column(Integer, nullable=False)
    carga: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    observacoes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="treinos")

    def __repr__(self) -> str:
        return f"<Treino id={self.id} nome='{self.nome_treino}' exercicio='{self.exercicio}'>"
