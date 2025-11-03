import os, re, uuid, json
from openai import OpenAI
from fastapi import UploadFile
from app.utils.image_utils import get_image_base64
from app.utils.attach_media import attach_media_and_enrich

client = OpenAI()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def analyze_physique(file: UploadFile):
    # Save the uploaded file locally
    file_id = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, file_id)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Convert image to base64 for API call
    base64_image = get_image_base64(file_path)

    # Ask model for physique + workout plan (structured JSON)
    prompt = """
    You are a professional fitness coach analyzing a physique image.
    Analyze the physique and return ONLY valid JSON in this structure:

    {
        "title": "2-Day Beginner Muscle Gain Plan",
        "summary": "Short summary about the physique and recommended approach.",
        "bmi": null,
        "plans": [
            {
                "day": "Day 1",
                "exercises": [
                    {
                        "name": "Bodyweight Squats",
                        "duration": "3 sets of 12 reps",
                        "description": "Strengthens legs and glutes.",
                        "frequency": "3 times a week"
                    },
                    {
                        "name": "Push-ups",
                        "duration": "3 sets of 10 reps",
                        "description": "Improves upper body strength."
                    }
                ],
                "tips": ["Warm up first", "Focus on correct posture"]
            },
            {
                "day": "Day 2",
                "exercises": [
                    {
                        "name": "Lunges",
                        "duration": "3 sets of 10 reps per leg",
                        "description": "Tones legs and core"
                    },
                    {
                        "name": "Plank",
                        "duration": "3 sets of 30 seconds",
                        "description": "Improves core stability"
                    }
                ],
                "tips": ["Breathe steadily", "Cool down after workout"]
            }
        ]
    }
    """

    try:
        # Call GPT-4o-mini with vision support
        response = client.responses.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fitness expert analyzing physique images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                },
            ],
        )

        # Extract and clean JSON
        raw_output = response.choices[0].message.content.strip()
        raw_output = re.sub(r"^```json|```$", "", raw_output).strip()
        parsed_output = json.loads(raw_output)

    except Exception as e:
        # Fallback response if parsing fails
        parsed_output = {
            "title": "Beginner Fitness Plan",
            "summary": "Based on the physique, here’s a plan to improve body composition.",
            "plans": [
                {
                    "day": "Day 1",
                    "exercises": [
                        {"name": "Walking", "duration": "30 minutes", "description": "Improves cardiovascular endurance"},
                        {"name": "Bodyweight Squats", "duration": "3 sets of 12 reps"},
                    ],
                    "tips": ["Start light and increase gradually", "Focus on proper breathing"],
                }
            ],
        }

    # Attach GIFs + enrich exercise info using attach_media.py
    enriched_output = attach_media_and_enrich(parsed_output)

    # Final response (same format as llm_service)
    final_response = {
        "status": 200,
        "image_id": file_id,
        "path": file_path.replace("\\", "/"),
        "analysis": enriched_output,
    }

    return final_response