"""
Shared LLM configuration for all HireFlow agents.
Uses AI/ML API (OpenAI-compatible) so we only need the $10 AIML credit.
LangGraphAdapter accepts ChatOpenAI — we just swap the base_url.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def get_llm() -> ChatOpenAI:
    load_dotenv()
    """
    Returns a ChatOpenAI instance pointed at AI/ML API.
    All 4 agents share this config — swap the model string here to change
    the model for all agents at once.
    """
    api_key = os.getenv("AIML_API_KEY")
    if not api_key:
        raise ValueError("AIML_API_KEY not set in environment")

    return ChatOpenAI(
        model="gpt-4o",  # Strong, fast, cheap on AIML
        api_key=api_key,
        base_url="https://api.aimlapi.com/v1",
        temperature=0.3,  # Low temp for consistent structured outputs

    )