import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from services.analysis_service import analyze_resume_against_role, get_available_roles

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    @app.route("/", methods=["GET", "POST"])
    def index():
        roles = get_available_roles()
        result = None
        form_data = {
            "resume_text": "",
            "target_role": roles[0] if roles else "",
            "manual_skills": "",
            "simulate_ai_failure": False,
        }

        if request.method == "POST":
            form_data = {
                "resume_text": request.form.get("resume_text", "").strip(),
                "target_role": request.form.get("target_role", "").strip(),
                "manual_skills": request.form.get("manual_skills", "").strip(),
                "simulate_ai_failure": request.form.get("simulate_ai_failure") == "on",
            }

            result = analyze_resume_against_role(
                resume_text=form_data["resume_text"],
                target_role=form_data["target_role"],
                manual_skills=form_data["manual_skills"],
                simulate_ai_failure=form_data["simulate_ai_failure"],
            )

        return render_template(
            "index.html",
            roles=roles,
            result=result,
            form_data=form_data,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)