backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script,py.mako
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI entry point
│   │
│   ├── core/                        # Core configs & setup
│   │   ├── __init__.py
│   │   └── config.py                # App config (env vars, settings)
│   │
│   ├── api/                         # API endpoints
│   │   ├── __init__.py
│   │   ├── routes_user.py           # Authentication, user endpoints
│   │   │── routes_vision.py          # route for image upload + analysis
│   │   ├── vision_service.py         # handles image analysis + physique AI
│   │   └── routes_model.py
│   │
│   ├── services/                    # Core business logic / services
│   │   ├── __init__.py
│   │   └── llm_service.py           # Handles OpenAI + memory
│   │
│   ├── database/                    # Persistence layer
│   │   ├── __init__.py
│   │   ├── db_session.py            # SQLAlchemy engine, Base, get_db()
│   │   ├── models_chat.py           # Conversation, Message models
│   │   └── crud_chat.py             # CRUD for chat
│   │
│   ├── models/                      # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── request_models.py        # Input schemas (Requests)
│   │   └── response_models.py       # Output schemas (Responses)
│   │
│   ├── schema/                    
│   │   ├── __init__.py
│   │   ├── exercise_media_app.py 
│   │   └── fitness_schema.py      
│   │
│   ├── utils/                       # Helpers, small functions, external tools
│   │   ├── __init__.py
│   │   ├── helpers.py               # Generic utility functions
│   │   ├── summarize.py             # LLM-based summarization helper
│   │   ├── auth.py                  # User authentication
│   │   ├── system_message_fitness.py
│   │   ├── image_utils.py          # Image encoded 
│   │   ├── json_utils.py           # Clean text and extract and parse JSON objects from a string
│   │   ├── attach_media.py         # Attaching media in JSON and others objects
|   |   └── units_normalisation_and_bmi.py    
│   │
│   ├── model_cache/                 # Cached or downloaded models (optional)
│   │   └── data_store
|   |       └── exercise_data_cache.json   
│   │
│   ├── static/                 # Cached or downloaded models (optional)
│   │   ├── uploads/            # where uploaded images are stored
│   │       └── uuid image 
│   │   └── gifs
│   │       └── pushup.gif 
│   │ 
│   ├── vision/                         # optional folder for detailed CV logic
│   │    ├── body_analysis.py           # physique feature extraction, fat %, etc.
│   │    └── posture_assessment.py      # optional: for form correction late   
│   │
│   └── tests/                       # Unit & integration tests
│       ├── __init__.py
│       ├── test_db.py
|       └── test_llm.py
│
│
├── .env                             # Environment variables
├── alembic.ini
├── requirements.txt                 # Python dependencies
├── railway.toml                     # Deployment config
├── start.sh                         # Start script for deployment
└── README.md                        # Project documentation
