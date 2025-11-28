from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # safe: allows cross-origin if frontend calls backend directly

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    age = data.get("age")
    message = (data.get("message") or "").strip()

    errors = []

    if not name:
        errors.append("Name is required.")
    if not email or not EMAIL_RE.match(email):
        errors.append("A valid email is required.")
    try:
        age_int = int(age)
        if age_int <= 0:
            errors.append("Age must be a positive integer.")
    except Exception:
        errors.append("Age must be a number.")

    if not message:
        errors.append("Message is required.")

    if errors:
        return jsonify({"error": "validation_failed", "details": errors}), 400

    # Example "processing": here you would save to DB / queue / etc.
    submission = {
        "name": name,
        "email": email,
        "age": age_int,
        "message": message,
        "received_at": datetime.utcnow().isoformat() + "Z"
    }

    # For demonstration we just echo back the submission
    return jsonify({"message": "Form received", "submission": submission}), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Development only; in Docker we'll use gunicorn
    app.run(host="0.0.0.0", port=5000, debug=False)
