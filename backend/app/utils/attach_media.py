import json
import os
import re
from openai import OpenAI
from app.schema.exercise_media_map import EXERCISE_MEDIA_MAP

client = OpenAI()

# Cache setup
DATA_DIR = os.path.join(os.path.dirname(__file__), "../model_cache/data_store")
os.makedirs(DATA_DIR, exist_ok=True)
CACHE_PATH = os.path.join(DATA_DIR, "exercise_data_cache.json")

if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            EXERCISE_CACHE = json.load(f)
    except json.JSONDecodeError:
        EXERCISE_CACHE = {}
else:
    EXERCISE_CACHE = {}


def save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(EXERCISE_CACHE, f, indent=2, ensure_ascii=False)


def normalize_name(name: str) -> str:
    """Normalize names by removing symbols, plural 's', and spaces."""
    return re.sub(r'[^a-z]', '', name.lower().rstrip('s'))


def find_exercise_media(name: str):
    """Find matching GIF in EXERCISE_MEDIA_MAP by normalized name."""
    normalized_name = normalize_name(name)

    for key, value in EXERCISE_MEDIA_MAP.items():
        if normalize_name(key) == normalized_name:
            return value

    return None  # no match found


def enrich_exercise(name: str):
    """Get difficulty, rest, body_part, target, calories for exercise name."""
    norm = normalize_name(name)
    if norm in EXERCISE_CACHE:
        return EXERCISE_CACHE[norm]

    prompt = f"""
    For exercise "{name}", return ONLY valid JSON with:
    - difficulty: Beginner, Intermediate, or Advanced
    - body_part: main area trained
    - target: key muscles worked
    - rest: rest time between sets (in seconds or minutes)
    - calories: estimated calories burned per set or per minute
    - how_to_perform: 3–4 short, practical bullet points describing how to perform it safely and effectively.

    Example:
    {{
        "difficulty": "Intermediate",
        "body_part": "Chest",
        "target": "pectorals, triceps",
        "rest": "1 minute",
        "calories": "8 kcal per set",
        "how_to_perform": [
            "Keep your body straight from head to heels.",
            "Lower your chest until it nearly touches the floor.",
            "Push through your palms to return to the start."
        ]
    }}
    """


    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        raw = res.choices[0].message.content.strip()
        raw = re.sub(r"^```json|```$", "", raw).strip()
        data = json.loads(raw)

        info = {
            "difficulty": data.get("difficulty", "Beginner"),
            "body_part": data.get("body_part", "Full Body"),
            "target": data.get("target", "multiple muscles"),
            "rest": data.get("rest", "1 minute"),
            "calories": data.get("calories", "5 kcal per set"),
            "how_to_perform": data.get("how_to_perform", [
                "Maintain proper form throughout the movement.",
                "Perform each rep slowly and with control.",
                "Breathe consistently during the exercise."
            ])
}


    except Exception:
        info = {
            "difficulty": "Beginner",
            "body_part": "Full Body",
            "target": "multiple muscles",
            "rest": "1 minute",
            "calories": "5 kcal per set",
        }

    EXERCISE_CACHE[norm] = info
    save_cache()
    return info


def attach_media_and_enrich(plan_response: dict):
    """Attach valid GIFs + enrich all exercises + compute daily/weekly totals."""
    total_calories_weekly = 0
    total_exercises_weekly = 0

    for day in plan_response.get("plans", []):
        total_day_calories = 0
        total_day_exercises = 0

        for ex in day.get("exercises", []):
            name = ex.get("name")
            if not name:
                continue

            # ✅ Match GIF from map
            media = find_exercise_media(name)
            if media:
                ex["media"] = {"gif": media["gif"]}

            # ✅ Enrich exercise info
            info = enrich_exercise(name)
            ex.update(info)

            # ✅ Extract calories
            cal_match = re.search(r"\d+", info.get("calories", "0"))
            cal = int(cal_match.group()) if cal_match else 0
            total_day_calories += cal
            total_day_exercises += 1

        # ✅ Daily totals
        day["total_calories"] = f"{total_day_calories} kcal"
        day["total_exercises"] = total_day_exercises
        total_calories_weekly += total_day_calories
        total_exercises_weekly += total_day_exercises

    # ✅ Weekly totals
    plan_response["total_calories"] = f"{total_calories_weekly} kcal"
    plan_response["total_exercises"] = total_exercises_weekly

    return plan_response
