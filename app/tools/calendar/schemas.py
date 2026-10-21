create_calender_event_tool = {
    "type": "function",
    "function": {
        "name": "create_calender_event",
        "description": "create a calender event on a particular data at a particular time",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the calendar event."
                },
                "event_date": {
                    "type": "string",
                    "description": "Calendar date in YYYY-MM-DD format."
                },
                "event_time": {
                    "type": "string",
                    "description": "Event time in HH:MM 24-hour format."
                }
            },
            "required": ["title", "event_date", "event_time"],
            "additionalProperties": False
        }
    }
}

list_calender_event_tool = {
    "type": "function",
    "function": {
        "name": "list_calender_event",
        "description": "list the calender events on a particular date",
        "parameters": {
            "type": "object",
            "properties": {
                "event_date": {
                    "type": "string",
                    "description": "Calendar date in YYYY-MM-DD format."
                }
            },
            "required": ["event_date"],
            "additionalProperties": False
        }
    }
}
