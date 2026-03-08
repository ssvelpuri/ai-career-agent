from services.analysis_service import analyze_resume_against_role


def test_happy_path_backend_engineer_analysis():
    resume = (
        "Recent computer science graduate with experience in Python, SQL, Git, Linux, "
        "REST APIs, and debugging backend services. Built projects with unit testing."
    )
    result = analyze_resume_against_role(
        resume_text=resume,
        target_role="Backend Engineer",
        simulate_ai_failure=True,
    )

    assert "error" not in result
    assert "Python" in result["extracted_skills"]
    assert "SQL" in result["matched_skills"]
    missing_names = [item["skill"] for item in result["missing_skill_details"]]
    assert "Docker" in missing_names


def test_empty_resume_returns_validation_error():
    result = analyze_resume_against_role(
        resume_text="   ",
        target_role="Backend Engineer",
        simulate_ai_failure=True,
    )
    assert result["error"] == "Please paste resume text before running the analysis."
