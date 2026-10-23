from datetime import date, time, datetime
from sqlalchemy.orm import Session
from db.models import Event

def delete_calender_event(title : str , event_date : str , event_time : str , db : Session):
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
        event_obj=db.query(Event).filter(Event.title == title , Event.event_date == parsed_date , Event.event_time == parsed_time).first()

        if event_obj:
            db.delete(event_obj)
            db.commit()

            return {
                "ok" : True , 
                "message" : "Event deleted"
            }
        else:
            return {
                "ok" : False , 
                "error" : {
                    "code" : "RESOURCE_NOT_FOUND",
                    "message" : "The data with given title , date , time is not found"
                }
            }

    except:
        return { 
            "ok" : False ,
            "error" : { 
                "code" : "DATABASE_ERROR",
                "message" : "Error from database service"
            }
        }