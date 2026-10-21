from app.tools.calendar.create_event import create_calender_event
from app.tools.calendar.list_events import list_calender_event
from app.tools.calendar.schemas import (
    create_calender_event_tool,
    list_calender_event_tool,
)


tool_registery = {
    "create_calender_event": {
        "function": create_calender_event,
        "schema": create_calender_event_tool
    },
    "list_calender_event": {
        "function": list_calender_event,
        "schema": list_calender_event_tool
    }
}
