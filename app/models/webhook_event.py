from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    # ----------------------
    # PRIMARY KEY (IDEMPOTÊNCIA)
    # ----------------------
    event_id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        index=True,
        nullable=False
    )

    # ----------------------
    # DADOS DO EVENTO
    # ----------------------
    card_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    cliente_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    # ----------------------
    # TIMESTAMP (AJUSTADO PROFISSIONAL)
    # ----------------------
    processed_at: Mapped[str] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )