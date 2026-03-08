from __future__ import annotations

from typing import Iterable, List


QUESTION_TEMPLATES = {
    "AWS": "How would you design a simple, scalable service on AWS for a small web application?",
    "Kubernetes": "What problems does Kubernetes solve, and when would you choose it over simpler deployment options?",
    "Terraform": "Why is infrastructure as code useful, and how would you structure a Terraform project for maintainability?",
    "Docker": "How are containers different from virtual machines, and why is Docker useful in modern development workflows?",
    "Linux": "What are some Linux commands and troubleshooting steps you would use when a backend service fails in production?",
    "REST APIs": "What makes an API RESTful, and how would you design endpoints for a basic CRUD service?",
    "Testing": "How would you test a backend service to make sure it handles both normal traffic and edge cases?",
    "Security": "What are common security risks in web applications, and how would you mitigate them?",
    "SQL": "How would you optimize a slow SQL query and investigate database bottlenecks?",
    "Machine Learning": "Describe the high-level steps you would take to build and evaluate a machine learning model for a real-world problem.",
}


DEFAULT_INTERVIEW_QUESTION = (
    "Explain your understanding of {skill} and describe how you would apply it in a real project."
)


def extract_skills_by_keywords(resume_text: str, skill_catalog: Iterable[str]) -> List[str]:
    lowered_resume = resume_text.lower()
    matches = []
    for skill in skill_catalog:
        if skill.lower() in lowered_resume:
            matches.append(skill)
    return sorted(set(matches))


def build_rule_based_roadmap(missing_skills: List[str]) -> List[dict]:
    roadmap = []
    for skill in missing_skills[:3]:
        roadmap.append(
            {
                "skill": skill,
                "reason": f"This skill appears frequently in target-role postings and is currently missing from the profile.",
                "actions": [
                    f"Learn the fundamentals of {skill} through a short tutorial or course.",
                    f"Build one mini-project that clearly demonstrates {skill}.",
                    f"Practice explaining {skill} in interview-style answers.",
                ],
            }
        )
    return roadmap


def build_rule_based_interview_questions(missing_skills: List[str], matched_skills: List[str]) -> List[str]:
    prioritized = missing_skills[:4] + matched_skills[:1]
    questions = []
    for skill in prioritized:
        questions.append(QUESTION_TEMPLATES.get(skill, DEFAULT_INTERVIEW_QUESTION.format(skill=skill)))
    return questions[:5]
