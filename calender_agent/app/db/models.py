from datetime import date, time, datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Event(Base):
    __tablename__ = "calendar_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    event_date: Mapped[date] = mapped_column(nullable=False)
    event_time: Mapped[time] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)