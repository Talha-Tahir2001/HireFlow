# HireFlow — AI Hiring Intelligence

> A multi-agent hiring pipeline built on [Band](https://band.ai) for the Band of Agents Hackathon.

HireFlow turns a raw job description and a pile of resumes into a structured hiring
recommendation — through a relay of 4 specialized AI agents that collaborate in a
Band chat room.

---

## The Story

A hiring manager is drowning. Three open roles, 47 resumes, interviews to schedule.

They paste a job description into Band and @mention the HireFlow team.
Four agents take it from there — each doing one job, handing off structured
context to the next. The HR manager gets a final report they can act on immediately.

---

## The Pipeline

```
HR Manager pastes JD into Band chat
        │
        ▼
┌─────────────────┐
│  Job Analyzer   │  Turns raw JD into a structured rubric:
│                 │  required skills (weighted), seniority signals,
│                 │  red flags, scoring guide
└────────┬────────┘
         │  @Resume Screener — here's the rubric
         ▼
┌─────────────────┐
│ Resume Screener │  Scores every candidate against the rubric.
│                 │  Not gut feel — the rubric's criteria, applied
│                 │  consistently. Ranks and flags specific gaps.
└────────┬────────┘
         │  @Interview Planner — top 3 with scores + gaps
         ▼
┌─────────────────┐
│ Interview       │  Generates tailored question packs.
│ Planner         │  Not generic templates — questions engineered
│                 │  around each candidate's specific gaps.
└────────┬────────┘
         │  @Decision Summarizer — interview packs ready
         ▼
┌─────────────────┐
│ Decision        │  Compiles the final report: comparison table,
│ Summarizer      │  recommendation with reasoning, next steps,
│                 │  and a full audit trail of the pipeline.
└────────┬────────┘
         │  @HR Manager — your hiring report is ready
         ▼
    HR Manager gets a report they can act on immediately
```

The rubric created in step 1 is the backbone of everything that follows.
Every score, every interview question, every recommendation traces back to it.
That's what makes HireFlow a workflow, not a feature list.

---

## Setup

### 1. Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- A [Band account](https://app.band.ai) with 4 External Agents created
- An [AI/ML API](https://aimlapi.com) key

### 2. Install
```bash
git clone https://github.com/yourusername/hireflow
cd hireflow
uv sync
```

### 3. Configure
```bash
cp .env.example .env
# Fill in your credentials in .env
```

Create 4 External Agents on [app.band.ai](https://app.band.ai/agents) and name them:
- `Job Analyzer`
- `Resume Screener`
- `Interview Planner`
- `Decision Summarizer`

Paste each agent's UUID and API key into `.env`.

### 4. Run
```bash
uv run python run_all.py
```

All 4 agents connect to Band and wait. You'll see:
```
✅ Job Analyzer is online and waiting in Band...
✅ Resume Screener is online and waiting in Band...
✅ Interview Planner is online and waiting in Band...
✅ Decision Summarizer is online and waiting in Band...
```

---

## Using HireFlow

1. Open [app.band.ai](https://app.band.ai) and create a new chat room
2. Add all 4 HireFlow agents as participants (under Remote)
3. Paste a job description and @mention Job Analyzer:

```
@Job Analyzer here's the JD for Senior Backend Engineer:

[paste job description]
```

4. Paste candidate resumes and @mention Resume Screener:

```
@Resume Screener here are our 5 candidates:

Candidate 1 — Alice Chen
[resume text]

Candidate 2 — Bob Malik
[resume text]

...
```

5. Watch the pipeline run. Agents hand off to each other automatically.
6. Receive your hiring report from @Decision Summarizer.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent coordination | [Band](https://band.ai) |
| Agent framework | LangGraph via Band SDK |
| LLM | Meta Llama 3.1 70B via [AI/ML API](https://aimlapi.com) |
| Language | Python 3.11+ |

---

## Built for Band of Agents Hackathon
June 12–19, 2026 · Track 1: Internal Enterprise Workflows