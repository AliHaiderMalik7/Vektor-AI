# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.services.vision_service import analyze_physique

# router = APIRouter()

# @router.post("/analyze-physique/")
# async def analyze_user_image(file: UploadFile = File(...)):
#     try:
#         result = await analyze_physique(file)
#         return result
#     except Exception as e:
#         raise HTTPException(status=500, detail=str(e))

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.vision_service import analyze_physique
from app.utils.attach_media import attach_media_and_enrich
from app.services.llm_service import LLMService
from typing import Optional
import json

router = APIRouter()
llm_service = LLMService()


@router.post("/analyze-physique/")
async def analyze_user_image(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):

    try:
        # Analyze physique
        result = await analyze_physique(file)
        analysis = result.get("analysis", {})
        physique = analysis.get("physique_analysis", {})
        recommended_exercises = analysis.get("recommended_exercises", [])

        # Build prompt for OpenAI to generate plan
        combined_prompt = f"""
        You are a fitness coach. A user has uploaded an image and here's the analysis:
        Physique Analysis: {physique}
        Recommended Exercises: {recommended_exercises}
        
        User's prompt: {prompt}

        Please generate a structured fitness plan including:
        - Number of days / weeks (decide appropriately based on physique)
        - Exercises per day
        - How to perform
        - Difficulty
        - Body part targeted
        - Reps / sets / duration
        - Tips per day
        - Daily & total calories
        
        Return only valid JSON in the following format:
        {{
            "title": "Plan Title",
            "summary": "Short summary",
            "bmi": null,
            "plans": [
                {{
                    "day": "Day 1",
                    "exercises": [ ... ],
                    "tips": [ ... ],
                    "total_calories": "..."
                }}
            ],
        "total_calories": "...",
        "total_exercises": ...
    }}
    """

        # Call LLMService
        llm_response = llm_service.generate_chatgpt_response(
            prompt=combined_prompt,
            model="gpt-4o",
        )

        # Ensure dict
        if isinstance(llm_response, str):
            try:
                llm_response = json.loads(llm_response)
            except json.JSONDecodeError:
                llm_response = {"text": llm_response}

        # Enrich with media, difficulty, calories
        enriched_plan = attach_media_and_enrich(llm_response)

        # Return structured JSON
        return {
            "status": 200,
            "image_id": result.get("image_id"),
            "path": result.get("path"),
            "response": enriched_plan
        }

    except Exception as e:
        raise HTTPException(status=500, detail=str(e))