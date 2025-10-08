backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes_flight.py       # Flight routes
│   │   ├── routes_voice.py        # Voice routes
│   │   └── routes_model.py        # LLM routes
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── flight_service.py      # Flight logic
│   │   ├── llm_service.py         # LLM handling
│   │   └── voice_service.py       # Voice processing
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py      # Request schemas
│   │   └── response_models.py     # Response schemas
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_session.py          # SQLAlchemy engine + session
│   │   ├── models_chat.py         # Conversation + Message tables
│   │   └── crud_chat.py           # CRUD functions for chat history
│   └── utils/
│       ├── __init__.py
│       └── helpers.py             # Helper functions
├── model_cache/                   # Downloaded models
├── .env                           # Environment variables
├── requirements.txt
└── README.md