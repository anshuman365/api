from flask import Flask, request, jsonify
from resume_parser import extract_resume_data
from job_matcher import match_resume_with_job
from models import score_candidate  # Import AI scoring model

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Resume Screening API is running!"})

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """API endpoint to analyze resumes."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    job_description = request.form.get("job_description", "")

    if not job_description:
        return jsonify({"error": "Job description required"}), 400

    # Save and process file
    file_path = "uploaded_" + file.filename
    file.save(file_path)
    
    resume_data = extract_resume_data(file_path)
    job_match_score = match_resume_with_job(" ".join(resume_data.values()), job_description)
    ai_score = score_candidate(resume_data, job_match_score)  # Apply AI scoring

    response = {
        "resume_data": resume_data,
        "job_match_score": job_match_score,
        "ai_candidate_score": ai_score
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)