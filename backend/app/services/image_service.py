import os, re, uuid, json
from openai import OpenAI
from fastapi import UploadFile, HTTPException, status # pyright: ignore[reportMissingImports]
from app.utils.image_utils import get_image_base64

client = OpenAI()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def analyze_physique(file: UploadFile, user_prompt: str, context: str = ""):
    """
    Analyze user's physique using OpenAI Vision (GPT-4o-mini) with optional conversation context.
    """

    # Save image locally
    file_id = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, file_id)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    base64_image = get_image_base64(file_path)

    # Fast prompt validation (skip if context already exists)
    FITNESS_KEYWORDS = [
        "fitness", "exercise", "workout", "gym", "training", "plan",
        "gain", "lose", "muscle", "fat", "body", "strength", "diet"
    ]
    if not context and not any(k in user_prompt.lower() for k in FITNESS_KEYWORDS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "I am only assisted to Fitness and Exercise"},
        )

    # Vision relevance check (run only if new prompt)
    image_relevant = True
    if not context:
        try:
            image_check = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI that identifies image categories."},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Does this image show a human body, physique, workout, "
                                    "gym activity, or fitness-related content? Answer only 'yes' or 'no'."
                                ),
                            },
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        ],
                    },
                ],
            )
            image_relevant = "yes" in image_check.choices[0].message.content.lower()
        except Exception:
            image_relevant = False

        if not image_relevant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "I am only assisted to Fitness and Exercise"},
            )

    # Merge context + prompt
    if context:
        user_prompt = f"Previous context:\n{context}\nUser update:\n{user_prompt}"

    # Main structured fitness plan generation
    full_prompt = f"""
    You are a professional fitness coach and physique expert.
    A user uploaded their body image and said:
    "{user_prompt}"

    Analyze their physique visually and generate a structured workout plan
    that suits their current body composition, goals, and prompt intent.

    Return ONLY valid JSON in this exact structure:
    {{
        "title": "Plan title",
        "summary": "Brief description of physique and focus",
        "plan_duration": "Number of days or weeks",
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
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fitness expert analyzing body images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": full_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}" }},
                    ],
                },
            ],
        )

        raw_output = response.choices[0].message.content.strip()
        raw_output = re.sub(r"^```json|```$", "", raw_output).strip()
        parsed_output = json.loads(raw_output)

    except Exception:
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
