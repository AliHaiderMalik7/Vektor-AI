backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   ├── script,py.mako
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
│   │   ├── auth.py
│   │   ├── system_message_fitness.py
│   │   ├── attach_media.py
|   |   └── units_normalisation_and_bmi.py    
│   │
│   ├── model_cache/                 # Cached or downloaded models (optional)
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
