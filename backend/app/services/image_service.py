import os, re, uuid, json
from openai import OpenAI
from fastapi import UploadFile
from app.utils.image_utils import get_image_base64

client = OpenAI()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def analyze_physique(file: UploadFile, user_prompt: str):
    """
    Analyze user's physique using OpenAI Vision (GPT-4o) and their custom prompt.
    Returns a structured fitness plan in JSON.
    """
    # Save uploaded image
    file_id = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, file_id)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Convert to base64 for OpenAI Vision
    base64_image = get_image_base64(file_path)

    # Combine AI instructions + user prompt
    full_prompt = f"""
    You are a professional fitness coach and physique expert.
    A user uploaded their body image and gave this request:
    "{user_prompt}"

    Analyze their physique visually and generate a structured workout plan
    that suits their current body composition, goals, and prompt intent.

    Return ONLY valid JSON in this exact structure:
    {{
        "title": "Plan title",
        "summary": "Brief description of physique and focus",
        "plan_duration": "Number of days or weeks (decide based on physique and prompt)",
        "plans": [
            {{
                "day": "Day 1",
                "exercises": [
                    {{
                        "name": "Exercise name",
                        "duration": "3 sets of 12 reps or minutes",
                        "description": "Purpose of exercise",
                        "difficulty": "Beginner / Intermediate / Advanced",
                        "body_part": "Chest / Legs / Full Body",
                        "calories": "Estimated calories burned"
                    }}
                ],
                "tips": ["Tip 1", "Tip 2"],
                "total_calories": "..."
            }}
        ],
        "total_exercises": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # supports image + text
            messages=[
                {"role": "system", "content": "You are a fitness expert analyzing body images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": full_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                },
            ],
        )

        # Extract content safely
        raw_output = response.choices[0].message.content.strip()
        raw_output = re.sub(r"^```json|```$", "", raw_output).strip()
        parsed_output = json.loads(raw_output)

    except Exception as e:
        parsed_output = {
            "title": "Default Fitness Plan",
            "summary": "Could not fully parse AI response. Basic plan generated.",
            "plans": [
                {
                    "day": "Day 1",
                    "exercises": [
                        {"name": "Walking", "duration": "30 minutes"},
                        {"name": "Push-ups", "duration": "3 sets of 10 reps"},
                    ],
                    "tips": ["Stay hydrated", "Stretch before workouts"],
                    "total_calories": "300",
                }
            ],
            "total_exercises": 2,
        }

    return {
        "status": 200,
        "image_id": file_id,
        "path": file_path.replace("\\", "/"),
        "analysis": parsed_output,
    }
