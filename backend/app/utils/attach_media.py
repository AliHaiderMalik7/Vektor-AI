import re
from app.schema.exercise_media_map import EXERCISE_MEDIA_MAP


def normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r'[-_]', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    name = ' '.join([w[:-1] if len(w) > 1 and w.endswith('s') else w for w in name.split()])
    return name

def find_media_for_exercise(ex_name: str):
    
    norm_ex = normalize_name(ex_name)
    ex_words = set(norm_ex.split())

    for key, media in EXERCISE_MEDIA_MAP.items():
        norm_key = normalize_name(key)
        key_words = set(norm_key.split())

        if ex_words == key_words:
            return media

    return None

def attach_media_to_plan(parsed_response: dict):
    try:
        if not isinstance(parsed_response, dict) or "plans" not in parsed_response:
            return parsed_response

        for plan in parsed_response["plans"]:
            if "days" in plan:
                for day in plan["days"]:
                    exercises = day.get("exercises", [])
                    for ex in exercises:
                        ex_name = ex.get("name", "")
                        media = find_media_for_exercise(ex_name)
                        if media:
                            ex["media"] = media

            elif "exercises" in plan:
                exercises = plan.get("exercises", [])
                for ex in exercises:
                    ex_name = ex.get("name", "")
                    media = find_media_for_exercise(ex_name)
                    if media:
                        ex["media"] = media

        return parsed_response

    except Exception as e:
        print(f"❌ Error in attach_media_to_plan: {e}")
        return parsed_response