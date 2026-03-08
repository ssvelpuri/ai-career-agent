import json
import os
from typing import List

from google import genai


class AIServiceError(Exception):
    pass


class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print("Gemini key loaded:", api_key[:6] + "..." + api_key[-4:])
        else:
            print("Gemini key loaded: False")
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.model_name = "gemini-2.5-flash"

    def available(self) -> bool:
        return self.client is not None

    def _require_client(self):
        if not self.client:
            raise AIServiceError("Gemini API key not configured.")

    def extract_skills(self, resume_text: str, skill_catalog: List[str]) -> List[str]:
        self._require_client()

        prompt = f"""
    Extract technical skills from the following resume.

    Return ONLY valid JSON:

    {{"skills": ["skill1","skill2"]}}

    Rules:
    - Prefer skills from this catalog:
    {skill_catalog}
    - You may infer closely related skills if strongly implied
    - Avoid duplicates
    - Only include technical skills

    Resume:
    {resume_text}
    """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            text = (response.text or "").strip()

            if text.startswith("```json"):
                text = text.removeprefix("```json").removesuffix("```").strip()
            elif text.startswith("```"):
                text = text.removeprefix("```").removesuffix("```").strip()

            data = json.loads(text)
            skills = data.get("skills", [])

            if not isinstance(skills, list):
                raise AIServiceError("Gemini returned invalid skills format.")

            cleaned = sorted({str(skill).strip() for skill in skills if str(skill).strip()})
            return cleaned
        except json.JSONDecodeError as exc:
            print("Gemini raw response:", text)
            raise AIServiceError("Gemini returned non-JSON output for skill extraction.") from exc
        except Exception as exc:
            raise AIServiceError(f"Gemini skill extraction failed: {exc}") from exc

    def generate_roadmap(
        self,
        target_role: str,
        matched_skills: List[str],
        missing_skills: List[str],
    ) -> List[dict]:
        self._require_client()

        prompt = f"""
    You are a career mentor helping an early-career engineer become competitive for the role: {target_role}.

    The candidate already has these skills:
    {matched_skills}

    They are missing these important skills:
    {missing_skills}

    Return ONLY valid JSON in this exact format:
    [
    {{
        "skill": "Skill Name",
        "reason": "Why this skill matters for the target role",
        "actions": [
        "Concrete action 1",
        "Concrete action 2",
        "Concrete action 3"
        ]
    }}
    ]

    Requirements:
    - Choose the 3 most important missing skills
    - For each skill, explain why it matters
    - Each skill must have exactly 3 practical actions
    - Do not include markdown or code fences
    """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            text = (response.text or "").strip()

            if text.startswith("```json"):
                text = text.removeprefix("```json").removesuffix("```").strip()
            elif text.startswith("```"):
                text = text.removeprefix("```").removesuffix("```").strip()

            data = json.loads(text)

            if not isinstance(data, list):
                raise AIServiceError("Gemini roadmap output was not a list.")

            return data
        except Exception as exc:
            raise AIServiceError(f"Gemini roadmap generation failed: {exc}") from exc

    def generate_interview_questions(
        self,
        target_role: str,
        matched_skills: List[str],
        missing_skills: List[str],
    ) -> List[str]:
        self._require_client()

        prompt = f"""
    You are preparing an early-career candidate for an interview for the role: {target_role}.

    The candidate already knows:
    {matched_skills}

    They still need to improve in:
    {missing_skills}

    Return ONLY valid JSON in this exact format:
    [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
    ]

    Requirements:
    - Generate exactly 5 realistic interview questions
    - Focus mainly on the missing skills
    - Mix conceptual and practical questions
    - At least one should involve debugging or a real-world scenario
    - Do not include markdown or code fences
    """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            text = (response.text or "").strip()

            if text.startswith("```json"):
                text = text.removeprefix("```json").removesuffix("```").strip()
            elif text.startswith("```"):
                text = text.removeprefix("```").removesuffix("```").strip()

            data = json.loads(text)

            if not isinstance(data, list):
                raise AIServiceError("Gemini questions output was not a list.")

            return [str(q).strip() for q in data if str(q).strip()]
        except Exception as exc:
            raise AIServiceError(f"Gemini question generation failed: {exc}") from exc