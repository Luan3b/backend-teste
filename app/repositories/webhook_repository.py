from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.webhook_event import WebhookEvent
from app.schemas.webhook_schema import WebhookPayload


class WebhookRepository:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------
    # READ (IDEMPOTÊNCIA)
    # ----------------------
    def get_by_event_id(self, event_id: str) -> Optional[WebhookEvent]:
        return (
            self.db.query(WebhookEvent)
            .filter_by(event_id=event_id)
            .first()
        )

    # ----------------------
    # CREATE EVENT
    # ----------------------
    def save_event(self, payload: WebhookPayload) -> WebhookEvent:

        event = WebhookEvent(
            event_id=payload.event_id,
            card_id=payload.card_id,
            cliente_email=payload.cliente_email
        )

        self.db.add(event)

        try:
            self.db.commit()
            self.db.refresh(event)

        except IntegrityError as e:
            self.db.rollback()
            raise e

        return event