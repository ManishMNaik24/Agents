from tools.calendar.create_event import create_calender_event
from tools.calendar.list_events import list_calender_event
from tools.calendar.delete_event import delete_calender_event

from schemas.calendar import (
    create_calender_event_tool,
    list_calender_event_tool,
    delete_calender_event_tool
)


tool_registery = {
    "create_calender_event" : {
        "function" : create_calender_event,
        "schema" : create_calender_event_tool
    },
    "list_calender_event" : {
        "function" : list_calender_event,
        "schema" : list_calender_event_tool
    },
    "delete_calender_event" : {
        "function" : delete_calender_event,
        "schema" : delete_calender_event_tool
    }
}

