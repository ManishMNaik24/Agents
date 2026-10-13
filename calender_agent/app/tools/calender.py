from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, time ,datetime
from app.db.models import Event


def create_calender_event(title : str, event_date : str, event_time : str,db : Session):
    try:
        parsed_date = date.fromisoformat(event_date)
    except ValueError:
        return {
            "ok" : False,
            "error" : {
                "code" : "VALUE_ERROR",
                "message" : "Invalid date. Expected YYYY-MM-DD"
            }
        }

    try:    
        parsed_time = time.fromisoformat(event_time)
    except ValueError:
        return {
            "ok" : False,
            "error" : {
                "code" : "Value_Error",
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
                "code" : "SQLAlchemyError",
                "message" : "Error from database service"
            }
        }


def list_calender_event(event_date : str , db : Session):
    try:
        parsed_date = date.fromisoformat(event_date)
        response=db.query(Event).filter(Event.event_date==parsed_date).all()

        event_list=[]
        for ele in response:
            obj={
                "title" : ele.title,
                "event_date" : ele.event_date.isoformat(),
                "event_time" : ele.event_time.isoformat()
            }
            event_list.append(obj)

        result={
            "ok" : True,
            "events" : event_list
        }

        return result
    
    except ValueError:
        return {
            "ok" : False,
            "error" : {
                "code" : "VALUE_ERROR",
                "message" : "Invalid date. Expected YYYY-MM-DD"
            }
        }

    except SQLAlchemyError:
        return {
            "ok" : False,
            "error" : {
                "code" : "SQLAlchemyError",
                "message" : "Error from database service"
            }
        }