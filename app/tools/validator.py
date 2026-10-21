def args_validator(args : dict , tool_schema : dict):
    required_args=set(tool_schema["function"]["parameters"]["required"])
    provided_args=set(args.keys())
    allowed_args = set(tool_schema["function"]["parameters"]["properties"].keys())

    missing_args=required_args-provided_args
    additional_args=provided_args-allowed_args

    if missing_args:
        return {
            "ok" : False,
            "error" : {
                "code" : "MISSING ARGUMENTS",
                "message" : f"expected {missing_args}"
            }
        }

    if additional_args:
        return {
            "ok" : False,
            "error" : {
                "code" : "INVALID ARGUMENTS",
                "message" : f"{additional_args} are not required"
            }
        }

    return {
        "ok": True
    }
