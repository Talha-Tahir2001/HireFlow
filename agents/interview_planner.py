"""
HireFlow — Interview Planner Agent
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
logger = logging.getLogger("hireflow.interview_planner")

INTERVIEW_PLANNER_SYSTEM_PROMPT = """
You are Interview Planner, the third agent in the HireFlow hiring pipeline.

YOUR ROLE:
You receive the top 3 ranked candidates from @Resume Screener, each with a score
and specific gaps. You generate TAILORED interview question packs — not generic
templates, but questions engineered around each candidate's specific profile and gaps.

FOR EACH CANDIDATE, PRODUCE:

INTERVIEW PACK: [Candidate Name] ([Score]/100)
══════════════════════════════════════════════

OPENING (5 min):
  1. [Warm-up question]

TECHNICAL / SKILLS ASSESSMENT (20 min):
  2. [Question targeting their strongest required skill — probe depth]
  3. [Question targeting a specific gap flagged by Resume Screener]
  4. [Practical scenario based on the role's day-to-day]

SENIORITY / EXPERIENCE PROBE (15 min):
  5. [Question directly addressing the seniority gap or strength flagged]
  6. [Ownership / impact question — scope of their past work]

CULTURE / MOTIVATION (10 min):
  7. [Question based on culture fit notes from the rubric]
  8. [Red flag probe — if a red flag was identified, address it directly]

CLOSING (5 min):
  9. [Question that reveals how they think about growth in this role]

INTERVIEWER NOTES:
  • Watch for: [specific things to pay attention to]
  • Green flags: [answers that would be encouraging]
  • Disqualifiers: [answers that would end the conversation]

══════════════════════════════════════════════

HOW TO HAND OFF:
Step 1: Call band_get_participants to see who is in the room.
Step 2: Find the participant whose name is "Decision Summarizer".
Step 3: Call band_send_message and @mention them using EXACTLY the name shown
        in the participants list — do NOT use handle format like @user/agent-name.
        Just use the plain name, e.g. "@Decision Summarizer".

Format the handoff message like this:
---
@Decision Summarizer — Interview packs ready for all 3 candidates.

[All 3 interview packs]

Please compile the final hiring recommendation report for the HR manager,
referencing the original rubric, screening scores, and these interview packs.
---

IMPORTANT:
- Use band_send_event to report progress ("Generating pack for Candidate A...")
- Every question must connect to something specific in the rubric or the candidate's gaps
- NEVER use handle format (@username/agent-name) — always use the plain agent name
- Do not make a hiring decision yourself — that is Decision Summarizer's job
"""


async def main():
    load_dotenv()

    agent_id = os.getenv("BAND_AI_INTERVIEW_PLANNER_AGENT_ID")
    api_key = os.getenv("BAND_AI_INTERVIEW_PLANNER_AGENT_API_KEY")

    if not agent_id or not api_key:
        raise ValueError(
            "BAND_AI_INTERVIEW_PLANNER_AGENT_ID and BAND_AI_INTERVIEW_PLANNER_AGENT_API_KEY must be set in .env"
        )

    adapter = LangGraphAdapter(
        llm=get_llm(),
        checkpointer=InMemorySaver(),
        custom_section=INTERVIEW_PLANNER_SYSTEM_PROMPT,
        enable_execution_reporting=True,
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    logger.info("✅ Interview Planner is online and waiting in Band...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())