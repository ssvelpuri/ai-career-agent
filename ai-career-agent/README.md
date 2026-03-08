# AI Career Agent

**Candidate Name:** Sai Velpuri  
**Scenario Chosen:** Skill-Bridge Career Navigator  
**Estimated Time Spent:** 4 hours
Demo Video: https://www.youtube.com/watch?v=plfA__3VnA0
Design Doc: Included as pdf title design doc
Synthetic Jobs: In jobs.json file and skill_catalog.json file

## Overview
AI Career Agent is a lightweight web prototype that helps an early-career user compare a synthetic resume against a target role, identify skill gaps, generate a learning roadmap, and practice with tailored mock interview questions.

The application uses AI for skill extraction and content generation when available, while also including deterministic fallbacks for reliability and reviewer-friendly demo behavior.

## Quick Start
### Prerequisites
- Python 3.10+
- pip

### Run Commands
```bash
pip install -r requirements.txt
python app.py
```

Then open the local URL shown in your terminal.

### Test Commands
```bash
pytest
```

## Core Flow
1. Paste a resume into the app.
2. Select a target role.
3. Click **Analyze Resume**.
4. Review extracted skills, matched skills, and missing skills.
5. Optionally add manual skill corrections.
6. Review the generated learning roadmap and mock interview questions.
7. Use the fallback toggle to simulate AI downtime.

## Design and Tech Stack
- **Backend:** Flask
- **Frontend:** HTML/CSS with minimal JavaScript
- **AI:** Google Gemini API for skill extraction and content generation
- **Fallbacks:** Keyword extraction + rule-based roadmap/interview templates
- **Data:** synthetic JSON dataset bundled in the repository
- **Tests:** pytest

## Data Safety
This project uses only synthetic data. It does not scrape live sites or process real personal data.

## Security
- API keys are loaded from environment variables.
- `.env.example` is included.
- No secrets should be committed to the repository.

## AI Disclosure
- **Did you use an AI assistant (Copilot, ChatGPT, etc.)?** Yes
- **How did you verify the suggestions?** I manually reviewed the generated architecture, checked that the logic matched the requirements, ran tests for the happy path and validation edge case, and verified that the fallback path works without an API key.
- **Give one example of a suggestion you rejected or changed:** I intentionally avoided resume PDF upload and live job scraping so the project would remain within the timebox, use synthetic data only, and stay more reliable for demo purposes.

## Tradeoffs & Prioritization
- **What did you cut to stay within the 4–6 hour limit?** I did not build authentication, file upload, a database, deployment, or integrations with live job boards/GitHub.
- **What would you build next if you had more time?** I would add richer resume parsing, downloadable roadmap reports, stronger filtering/analytics, and persistent user profiles.
- **Known limitations:** AI output quality depends on prompt adherence and API availability. The fallback mode is intentionally simpler than the AI path. The sample dataset is small and synthetic, so insights are illustrative rather than exhaustive.

## Responsible AI Notes
- The system makes suggestions, not hiring decisions.
- The app clearly indicates whether AI or fallback logic was used.
- The fallback path ensures graceful degradation when AI is unavailable or incorrect.
- Because the dataset is synthetic, results are meant as a proof of concept rather than a real labor-market recommendation engine.

## Suggested Demo Script
1. Briefly explain the problem: early-career users often do not know what skills they are missing.
2. Paste in a sample resume.
3. Choose a target role such as Cloud Engineer.
4. Show extracted skills, missing skills, and the generated roadmap.
5. Show the mock interview questions.
6. Toggle fallback mode and run the same flow again.
7. Run `pytest` to demonstrate basic quality checks.

## Sample Resume for Demo
```text
Recent computer science graduate with experience in Python, SQL, Git, Linux, and REST API development. Built backend services for student projects and worked with basic Docker containers. Familiar with data analysis, debugging, and testing.
```
