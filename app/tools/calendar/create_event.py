from datetime import date, time, datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import Event


async def create_calender_event(title : str, event_date : str, event_time : str,db : Session):
    try:
        parsed_date = date.fromisoformat(event_date)
    except ValueError:
        return {
            "ok" : False,
            "error" : {
                "code" : "INVALID_DATE",
                "message" : "Invalid date. Expected YYYY-MM-DD"
            }
        }

    try:
        parsed_time = time.fromisoformat(event_time)
    except ValueError:
        return {
            "ok" : False,
            "error" : {
                "code" : "INVALID_TIME",
                "message" : "Invalid time. Expected HH:MM."
            }
        }


    try:
        event_object=Event(
            title=title,
            event_date=parsed_date,
            event_time=parsed_time,
            created_at=datetime.utcnow()
        )

        db.add(event_object)
        db.commit()
        db.refresh(event_object)

        return {
            "ok": True,
            "event": {
                "id": event_object.id,
                "title": event_object.title,
                "date": event_object.event_date.isoformat(),
                "time": event_object.event_time.isoformat(),
                "created_at": event_object.created_at.isoformat()
            }
        }

    except SQLAlchemyError:
        db.rollback()
        return {
            "ok" : False,
            "error" : {
                "code" : "DATABASE_ERROR",
                "message" : "Error from database service"
            }
        }
