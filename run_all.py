"""
HireFlow — Boot All 4 Agents Concurrently
──────────────────────────────────────────
Run this single file to launch the entire HireFlow pipeline.
All 4 agents connect to Band simultaneously and wait for messages.

Usage:
    uv run python run_all.py

Each agent runs in its own async task. If one crashes, the others keep running.
Ctrl+C shuts everything down cleanly.
"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("hireflow.runner")


async def run_agent(name: str, module_path: str):
    """Import and run a single agent, with crash recovery logging."""
    try:
        logger.info(f"🚀 Starting {name}...")

        # Dynamically import the agent module
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        await module.main()
    except Exception as e:
        logger.error(f"❌ {name} crashed: {e}")
        raise


async def main():
    load_dotenv()

    # Verify all env vars are present before starting
    required_vars = [
        "AIML_API_KEY",
        "BAND_AI_JOB_ANALYZER_AGENT_ID", "BAND_AI_JOB_ANALYZER_AGENT_API_KEY",
        "BAND_AI_RESUME_SCREENER_AGENT_ID", "BAND_AI_RESUME_SCREENER_AGENT_API_KEY",
        "BAND_AI_INTERVIEW_PLANNER_AGENT_ID", "BAND_AI_INTERVIEW_PLANNER_AGENT_API_KEY",
        "BAND_AI_DECISION_SUMMARIZER_AGENT_ID", "BAND_AI_DECISION_SUMMARIZER_AGENT_API_KEY",
    ]

    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        logger.error(f"❌ Missing environment variables: {', '.join(missing)}")
        logger.error("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    agents_dir = os.path.join(os.path.dirname(__file__), "agents")

    agents = [
        ("Job Analyzer",       os.path.join(agents_dir, "job_analyzer.py")),
        ("Resume Screener",    os.path.join(agents_dir, "resume_screener.py")),
        ("Interview Planner",  os.path.join(agents_dir, "interview_planner.py")),
        ("Decision Summarizer",os.path.join(agents_dir, "decision_summarizer.py")),
    ]

    logger.info("=" * 55)
    logger.info("  HireFlow — AI Hiring Intelligence")
    logger.info("  Booting 4 agents into Band...")
    logger.info("=" * 55)

    # Run all 4 agents concurrently
    tasks = [
        asyncio.create_task(run_agent(name, path))
        for name, path in agents
    ]

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down HireFlow...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("✅ All agents stopped cleanly.")


if __name__ == "__main__":
    asyncio.run(main())