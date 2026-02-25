#!/usr/bin/env python
"""
Test direct OpenAI service
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from core.services.llm_service import LLMService

print("Testing OpenAI service directly...")
print(f"IA_PROVIDER from .env: {os.getenv('IA_PROVIDER')}")
print(f"OPENAI_API_KEY configured: {bool(os.getenv('OPENAI_API_KEY'))}")

try:
    llm = LLMService(provider='openai')
    print(f"✓ LLM Service initialized: {type(llm.service).__name__}")
    
    # Test simple chat
    print("\nTesting chat with OpenAI...")
    response = llm.service.chat(
        messages=[{"role": "user", "content": "Quelle est la formule du volume d'une sphère?"}],
        system_prompt="Tu es un professeur de mathématiques. Réponds en JSON avec {\"response\": \"...\"}"
    )
    print(f"Raw response:\n{response[:300]}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
