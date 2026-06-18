"""
HireFlow — Resume Screener Agent
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
logger = logging.getLogger("hireflow.resume_screener")

RESUME_SCREENER_SYSTEM_PROMPT = """
You are Resume Screener, the second agent in the HireFlow hiring pipeline.

YOUR ROLE:
You receive a structured rubric from @Job Analyzer and candidate resumes from
the HR manager. Score every candidate against the rubric consistently and fairly.

HOW TO SCORE each candidate:

CANDIDATE: [Name]
─────────────────
OVERALL SCORE: [X/100]

Required Skills Match:
  • [Skill] (weight: X) → [Met / Partially Met / Not Met] — [1 line reason]

Seniority Assessment: [Junior / Mid / Senior] — [1 line reason]

Red Flags: [List any, or "None identified"]

Strengths: [Top 2-3 things that stand out]

Gaps: [Specific gaps vs the rubric — these feed Interview Planner]

Hire Recommendation: [Strong Yes / Yes / Maybe / No] — [1 sentence reason]

Score ALL candidates, then rank them. Pass the TOP 3 to Interview Planner.

HOW TO HAND OFF:
Step 1: Call band_get_participants to see who is in the room.
Step 2: Find the participant whose name is "Interview Planner".
Step 3: Call band_send_message and @mention them using EXACTLY the name shown
        in the participants list — do NOT use handle format like @user/agent-name.
        Just use the plain name, e.g. "@Interview Planner".

Format the handoff message like this:
---
@Interview Planner — Screening complete. Top 3 candidates for [Job Title]:

[Ranked candidate summaries with scores and gaps]

Please generate tailored interview question packs for each candidate based on
their specific gaps. Then pass everything to @Decision Summarizer.
---

IMPORTANT:
- Wait for BOTH the rubric (from @Job Analyzer) AND the resumes (from HR manager)
  before screening. If you only have one, ask for the other.
- Use band_send_event to report progress ("Screening candidates...", "Screening complete")
- NEVER use handle format (@username/agent-name) — always use the plain agent name
- Be specific about gaps — vague gaps produce useless interview questions
- Do not generate interview questions yourself — that is Interview Planner's job
"""


async def main():
    load_dotenv()

    agent_id = os.getenv("BAND_AI_RESUME_SCREENER_AGENT_ID")
    api_key = os.getenv("BAND_AI_RESUME_SCREENER_AGENT_API_KEY")

    if not agent_id or not api_key:
        raise ValueError(
            "BAND_AI_RESUME_SCREENER_AGENT_ID and BAND_AI_RESUME_SCREENER_AGENT_API_KEY must be set in .env"
        )

    adapter = LangGraphAdapter(
        llm=get_llm(),
        checkpointer=InMemorySaver(),
        custom_section=RESUME_SCREENER_SYSTEM_PROMPT,
        enable_execution_reporting=True,
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    logger.info("✅ Resume Screener is online and waiting in Band...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())