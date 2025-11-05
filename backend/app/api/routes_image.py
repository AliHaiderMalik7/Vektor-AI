# ------------ Previous Simple Image Analysis Endpoint --------------

# from fastapi import APIRouter, UploadFile, File, HTTPException # pyright: ignore[reportMissingImports]
# from app.services.image_service import analyze_physique

# router = APIRouter()

# @router.post("/analyze-physique/")
# async def analyze_user_image(file: UploadFile = File(...)):
#     try:
#         result = await analyze_physique(file)
#         return result
#     except Exception as e:
#         raise HTTPException(status=500, detail=str(e))


# ------------ For Picture Upload and Prompt Handling --------------

from fastapi import APIRouter, UploadFile, File, Form, HTTPException # pyright: ignore[reportMissingImports]
from app.services.image_service import analyze_physique
from app.utils.attach_media import attach_media_and_enrich
import json

router = APIRouter()


@router.post("/analyze-physique/")
async def analyze_user_image(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    """
    User uploads an image and provides a custom text prompt.
    Returns a personalized plan based on both.
    """
    try:
        # Step 1: analyze image + prompt with OpenAI Vision
        result = await analyze_physique(file, prompt)
        analysis = result.get("analysis", {})

        # Step 2: attach exercise media, calories, difficulty
        enriched_plan = attach_media_and_enrich(analysis)

        # Step 3: return structured plan
        return {
            "status": 200,
            "image_id": result.get("image_id"),
            "path": result.get("path"),
            "response": enriched_plan
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# # ------- Testing to Upload Images on Database -------

# from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends # pyright: ignore[reportMissingImports]
# from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]
# from app.database.db_session import get_db
# from app.database import crud_chat
# from app.services.image_service import analyze_physique
# from app.utils.auth import get_current_user
# from app.utils.attach_media import attach_media_and_enrich

# router = APIRouter()

# @router.post("/analyze-physique/")
# async def analyze_user_image(
#     file: UploadFile = File(...),
#     prompt: str = Form(...),
#     current_user = Depends(get_current_user),
#     # user_id: int = Form(...), 
#     conversation_id: int = Form(None),
#     db: Session = Depends(get_db)
# ):
#     user_id = current_user.id
#     """
#     User uploads an image and provides a custom text prompt.
#     The image is analyzed and stored in the database.
#     """
#     try:
#         # Analyze image + prompt
#         result = await analyze_physique(file, prompt)
#         analysis = result.get("analysis", {})
#         file_path = result.get("path")
#         file_name = result.get("image_id")

#         # Store image in DB
#         image_record = crud_chat.create_image_record(
#             db=db,
#             user_id=user_id,
#             file_path=file_path,
#             file_name=file_name,
#             conversation_id=conversation_id
#         )

#         # Enrich the generated plan
#         enriched_plan = attach_media_and_enrich(analysis)

#         # Return everything
#         return {
#             "status": 200,
#             "image_id": image_record.id,
#             "file_path": file_path,
#             "response": enriched_plan
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
