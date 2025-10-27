FITNESS_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "bmi": {"type": ["number", "null"]},
        "plans": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "week": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "tips": {"type": "array", "items": {"type": "string"}},
                    "days": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "day": {"type": "string"},
                                "exercises": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "properties": {
                                            "name": {"type": "string"},
                                            "sets": {"type": "integer"},
                                            "reps": {"type": "string"},
                                            "description": {"type": "string"},
                                            "image": {"type": "string"},
                                            "gif": {"type": "string"},
                                        },
                                        "required": ["name", "sets", "reps", "description", "image", "gif"]
                                    }
                                },
                                "tips": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["day", "exercises", "tips"]
                        }
                    }
                },
                "required": ["week", "title", "description", "days", "tips"]
            }
        },
        "error": {"type": ["string", "null"]},
        "missing_info": {"type": ["string", "null"]}
    },
    # Required must include every property, even optional ones
    "required": ["title", "summary", "bmi", "plans", "error", "missing_info"]
}
