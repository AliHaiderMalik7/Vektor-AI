fitness_plan_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "bmi": {"type": "number"},
        "plans": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "day": {"type": "string"},
                    "week": {"type": "string"},
                    "month": {"type": "string"},
                    "phase": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "goal": {"type": "string"}
                        },
                        "required": ["name"]
                    },
                    "exercises": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "duration": {"type": "string"},
                                "sets": {"type": ["integer", "string"]},
                                "reps": {"type": ["integer", "string"]},
                                "intensity": {"type": "string"},
                                "difficulty": {"type": "string"},
                                "body_part": {"type": "string"},
                                "target": {"type": "string"},
                                "rest": {"type": "string"},
                                "calories": {"type": "string"},
                                "media": {
                                    "type": "object",
                                    "properties": {
                                        "gif": {"type": "string"}
                                    },
                                    "required": ["gif"]
                                }
                            },
                            "required": ["name"]
                        }
                    },
                    "tips": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "total_calories": {"type": "string"},
                    "total_exercises": {"type": ["integer", "string"]}
                },
                "required": ["exercises"]
            }
        },
        "error": {"type": ["string", "null"]},
        "missing_info": {"type": ["string", "null"]},
        "total_calories": {"type": "string"},
        "total_exercises": {"type": ["integer", "string"]}
    },
    "required": ["title", "plans"]
}
