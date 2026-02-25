# 🤖 IA Provider Configuration Guide

## Current Status
✅ **Mock Mode** is configured in `.env`  
✅ Chat endpoint (`/api/ia/chat/`) works  
✅ Exercise generation works  
✅ No echo of user input  
✅ Always returns ≥1 exercise

## Switching Between Providers

### 1. **Mock Mode (for testing/development)**
```bash
# Edit .env file:
IA_PROVIDER=mock
OPENAI_API_KEY=         # Leave empty or remove

# Restart server:
cd "D:\Documents\Tuteur intelligent"
.\.venv\Scripts\python.exe manage.py runserver
```

**Features**: Fast, no API costs, always works offline  
**Limitation**: Generic responses (not context-aware)

### 2. **OpenAI Mode (production)**
```bash
# Edit .env file:
IA_PROVIDER=openai
OPENAI_API_KEY=sk-your-real-key-here

# Restart server:
cd "D:\Documents\Tuteur intelligent"
.\.venv\Scripts\python.exe manage.py runserver
```

**Features**: Smart responses using GPT-4/3.5  
**Requirement**: Valid OpenAI API key

### 3. **Test Your Configuration**
```bash
# Test mock endpoint (always works)
curl http://127.0.0.1:8000/api/ia/chat-test-mock/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'

# Test normal endpoint (uses .env provider)
curl http://127.0.0.1:8000/api/ia/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Bonjour"}'

# Check environment
curl http://127.0.0.1:8000/api/ia/diagnostic-env/
```

## Endpoints

### Chat
- **POST** `/api/ia/chat/`
- **Headers**: `Authorization: Bearer {token}`
- **Body**: `{"message": "text"}`
- **Response**: `{"response": "...", "exercises": [...], "conversation_id": X}`

### Exercise Generate
- **POST** `/api/ia/generer-exercices/`
- **Headers**: `Authorization: Bearer {token}`
- **Body**: `{"count": 2, "topic": "optional"}`
- **Response**: `{"exercises": [...]}`

## Key Files
- `.env` - Provider configuration
- `core/services/llm_service.py` - LLM implementations
- `core/ia_endpoints.py` - Chat endpoints
- `core/ia_test_endpoints.py` - Test/diagnostic endpoints

## Troubleshooting

**Error: "OPENAI_API_KEY non configurée"**
- You're in `openai` mode but key is missing
- Either: (1) Set valid key in `.env`, or (2) Switch to `mock` mode

**No exercises returned**
- Provider returned invalid JSON or empty array
- Fall back to `mock` mode to verify

**Server not picking up .env changes**
- Restart the server: `Ctrl+C` then `python manage.py runserver`

## Test Script
Run full integration test:
```bash
.\.venv\Scripts\python.exe test_openai_integration.py
```

Runs: Login → Chat "Bonjour" → Chat "formule volume" → Generate 2 exercises
