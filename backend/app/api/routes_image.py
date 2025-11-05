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
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]
from app.database.db_session import get_db
from app.services.image_service import analyze_physique
from app.utils.attach_media import attach_media_and_enrich
from app.database import models_chat as models
import json

router = APIRouter()

@router.post("/analyze-physique/")
async def analyze_user_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    conversation_id: int | None = Form(None),
    db: Session = Depends(get_db)
):
    """
    Handles:
    - Image upload
    - Fitness-related prompt
    - Contextual conversation memory
    - Returns structured AI fitness plan
    """

    try:
        # Load previous conversation context if exists
        context_text = ""
        if conversation_id:
            prev_msgs = (
                db.query(models.Message)
                .filter(models.Message.conversation_id == conversation_id)
                .order_by(models.Message.id.desc())
                .limit(3)
                .all()
            )
            context_text = " ".join([m.content for m in reversed(prev_msgs)])

        # Analyze image + prompt + context
        result = await analyze_physique(file, prompt, context_text)
        analysis = result.get("analysis", {})

        # Enrich the plan with media, calories, difficulty
        enriched_plan = attach_media_and_enrich(analysis)

        # If conversation doesn’t exist, create new one
        if not conversation_id:
            new_convo = models.Conversation(title="Fitness Conversation")
            db.add(new_convo)
            db.commit()
            db.refresh(new_convo)
            conversation_id = new_convo.id

        # Save user prompt and AI response to DB
        user_msg = models.Message(
            conversation_id=conversation_id,
            role="user",
            content=prompt
        )
        ai_msg = models.Message(
            conversation_id=conversation_id,
            role="assistant",
            content=json.dumps(enriched_plan)
        )
        db.add_all([user_msg, ai_msg])
        db.commit()

        # Return structured response
        return {
            "status": 200,
            "conversation_id": conversation_id,
            "image_id": result.get("image_id"),
            "path": result.get("path"),
            "response": enriched_plan,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )



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
