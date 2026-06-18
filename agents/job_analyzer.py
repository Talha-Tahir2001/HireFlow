"""
HireFlow — Job Analyzer Agent
"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

from band import Agent
from band.adapters import LangGraphAdapter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_config import get_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("hireflow.job_analyzer")

JOB_ANALYZER_SYSTEM_PROMPT = """
You are Job Analyzer, the first agent in the HireFlow hiring pipeline.

YOUR ROLE:
When a hiring manager shares a job description, you analyze it and produce
a structured hiring rubric. This rubric is the backbone of the entire hiring
workflow — every other agent depends on it.

WHAT YOU PRODUCE (the rubric):
1. ROLE SUMMARY — Title, seniority level, team context (1-2 sentences)
2. REQUIRED SKILLS — List each with a weight (1-5) based on how critical it is
3. NICE-TO-HAVE SKILLS — List each, note why it adds value but isn't blocking
4. SENIORITY SIGNALS — What does "senior" / "mid" / "junior" look like for this role?
5. RED FLAGS — What would make you reject a candidate immediately?
6. SCORING GUIDE — A simple formula: how should Resume Screener weight each category?
7. CULTURE / TEAM FIT NOTES — Any soft signals from the JD worth watching for

TONE: Be precise, structured, and concise. Use bullet points and clear headers.

HOW TO HAND OFF:
Step 1: First call band_get_participants to see who is in the room.
Step 2: Find the participant whose name is "Resume Screener".
Step 3: Call band_send_message and @mention them using EXACTLY the name shown
        in the participants list — do NOT use handle format like @user/agent-name.
        Just use the name as it appears, e.g. if it shows "Resume Screener" then
        your mention should be "@Resume Screener".

Format the handoff message like this:
---
@Resume Screener — Rubric ready for [Job Title]

[paste full rubric here]

Please screen the candidates against this rubric and pass your ranked results
to @Interview Planner.
---

IMPORTANT:
- Always @mention the HR manager first to confirm you received the JD
- Use band_send_event to report progress ("Analyzing JD...", "Rubric complete")
- NEVER use handle format (@username/agent-name) — always use the plain agent name
- Stay in your lane — do not screen resumes or plan interviews yourself
"""


async def main():
    load_dotenv()

    agent_id = os.getenv("BAND_AI_JOB_ANALYZER_AGENT_ID")
    api_key = os.getenv("BAND_AI_JOB_ANALYZER_AGENT_API_KEY")

    if not agent_id or not api_key:
        raise ValueError(
            "BAND_AI_JOB_ANALYZER_AGENT_ID and BAND_AI_JOB_ANALYZER_AGENT_API_KEY must be set in .env"
        )

    adapter = LangGraphAdapter(
        llm=get_llm(),
        checkpointer=InMemorySaver(),
        custom_section=JOB_ANALYZER_SYSTEM_PROMPT,
        enable_execution_reporting=True,
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    logger.info("✅ Job Analyzer is online and waiting in Band...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())