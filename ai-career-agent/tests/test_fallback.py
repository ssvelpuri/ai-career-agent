from services.analysis_service import analyze_resume_against_role
from services.fallback_service import extract_skills_by_keywords


def test_keyword_extraction_detects_known_skills():
    catalog = ["Python", "Docker", "AWS"]
    resume = "Worked with Python services and deployed Docker containers."
    skills = extract_skills_by_keywords(resume, catalog)
    assert skills == ["Docker", "Python"]


def test_manual_skill_override_is_merged_into_results():
    resume = "Experience with Python and Git."
    result = analyze_resume_against_role(
        resume_text=resume,
        target_role="Cloud Engineer",
        manual_skills="AWS, Terraform",
        simulate_ai_failure=True,
    )
    assert "AWS" in result["extracted_skills"]
    assert "Terraform" in result["matched_skills"]
