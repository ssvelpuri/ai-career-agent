from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List

from services.ai_service import AIService, AIServiceError
from services.fallback_service import (
    build_rule_based_interview_questions,
    build_rule_based_roadmap,
    extract_skills_by_keywords,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JOBS_PATH = DATA_DIR / "jobs.json"
SKILL_CATALOG_PATH = DATA_DIR / "skill_catalog.json"


def load_jobs() -> List[dict]:
    with JOBS_PATH.open("r", encoding="utf-8") as infile:
        return json.load(infile)


def load_skill_catalog() -> List[str]:
    with SKILL_CATALOG_PATH.open("r", encoding="utf-8") as infile:
        return json.load(infile)


def get_available_roles() -> List[str]:
    jobs = load_jobs()
    return sorted({job["title"] for job in jobs})


def _normalize_manual_skills(manual_skills: str) -> List[str]:
    if not manual_skills.strip():
        return []
    return sorted({part.strip() for part in manual_skills.split(",") if part.strip()})


def _required_skills_for_role(target_role: str, jobs: List[dict]) -> Dict[str, int]:
    filtered_jobs = [job for job in jobs if job["title"] == target_role]
    counter: Counter[str] = Counter()
    for job in filtered_jobs:
        counter.update(job["skills"])
    return dict(counter.most_common())

def classify_skill_demand(freq: int) -> str:
    if freq <= 2:
        return "occasionally requested"
    elif freq <= 4:
        return "common"
    else:
        return "high priority"
    
def analyze_resume_against_role(
    resume_text: str,
    target_role: str,
    manual_skills: str = "",
    simulate_ai_failure: bool = False,
) -> dict:
    roles = get_available_roles()
    if not resume_text.strip():
        return {"error": "Please paste resume text before running the analysis."}
    if target_role not in roles:
        return {"error": "Please select a valid target role."}

    jobs = load_jobs()
    skill_catalog = load_skill_catalog()
    ai_service = AIService()

    extraction_method = "AI"
    generation_method = "AI"
    warnings: List[str] = []

    if simulate_ai_failure:
        extracted_skills = extract_skills_by_keywords(resume_text, skill_catalog)
        extraction_method = "Fallback"
        generation_method = "Fallback"
        warnings.append("Developer mode forced the fallback path.")
    else:
        try:
            extracted_skills = ai_service.extract_skills(resume_text, skill_catalog)
            if not extracted_skills:
                raise AIServiceError("AI extraction returned no skills.")
        except Exception as e:
            print("AI extraction error:", e)
            extracted_skills = extract_skills_by_keywords(resume_text, skill_catalog)
            extraction_method = "Fallback"
            generation_method = "Fallback"
            warnings.append("AI extraction was unavailable, so the app used keyword-based fallback extraction.")

    extracted_skills = sorted(set(extracted_skills + _normalize_manual_skills(manual_skills)))

    required_skills = _required_skills_for_role(target_role, jobs)
    required_skill_names = list(required_skills.keys())

    matched_skills = sorted([skill for skill in extracted_skills if skill in required_skill_names])
    missing_skills = [skill for skill in required_skill_names if skill not in extracted_skills]

    if generation_method == "AI":
        try:
            roadmap = ai_service.generate_roadmap(target_role, matched_skills, missing_skills)
            interview_questions = ai_service.generate_interview_questions(target_role, matched_skills, missing_skills)
        except Exception as e:
            print("AI generation error:", e)
            roadmap = build_rule_based_roadmap(missing_skills)
            interview_questions = build_rule_based_interview_questions(missing_skills, matched_skills)
            generation_method = "Fallback"
            warnings.append("AI content generation was unavailable, so the app used rule-based outputs.")
    else:
        roadmap = build_rule_based_roadmap(missing_skills)
        interview_questions = build_rule_based_interview_questions(missing_skills, matched_skills)

    missing_skill_details = [
        {
            "skill": skill,
            "demand_label": classify_skill_demand(required_skills[skill])
        }
        for skill in missing_skills
    ]

    return {
        "target_role": target_role,
        "extracted_skills": extracted_skills,
        "matched_skills": matched_skills,
        "missing_skill_details": missing_skill_details,
        "roadmap": roadmap,
        "interview_questions": interview_questions,
        "extraction_method": extraction_method,
        "generation_method": generation_method,
        "warnings": warnings,
        "search_index": required_skill_names,
    }
