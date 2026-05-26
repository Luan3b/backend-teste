from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Client(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    cliente_nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    cliente_email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    tipo_solicitacao: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    valor_patrimonio: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Aguardando Análise",
        nullable=False
    )

    prioridade: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )