from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, time ,datetime
from app.db.models import Event


def create_calender_event(title : str, event_date : str, event_time : str,db : Session):
    try:
        parsed_date = date.fromisoformat(event_date)
    except ValueError:
        raise ValueError("Invalid date. Expected YYYY-MM-DD")

    try:    
        parsed_time = time.fromisoformat(event_time)
    except ValueError:
        raise ValueError("Invalid time. Expected HH:MM.")

    
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
            "status": "success",
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
        raise


def list_calender_event(event_date : str , db : Session):
    try:
        parsed_date = date.fromisoformat(event_date)
        response=db.query(Event).filter(Event.event_date==parsed_date).all()

        result=[]
        for ele in response:
            obj={
                "title" : ele.title,
                "event_date" : ele.event_date.isoformat(),
                "event_time" : ele.event_time.isoformat()
            }
            result.append(obj)

        return result
    
    except ValueError:
        raise ValueError("Invalid date. Expected YYYY-MM-DD")

    except SQLAlchemyError:
        raise