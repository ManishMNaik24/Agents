from datetime import date

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import Event


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
                "code" : "INVALID_DATE",
                "message" : "Invalid date. Expected YYYY-MM-DD"
            }
        }

    except SQLAlchemyError:
        return {
            "ok" : False,
            "error" : {
                "code" : "DATABASE_ERROR",
                "message" : "Error from database service"
            }
        }
