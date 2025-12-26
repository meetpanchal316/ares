from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # allows cross-origin if frontend calls backend directly

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
PHONE_RE = re.compile(r"^[0-9]{10}$")  # simple 10-digit phone validation


@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    age = data.get("age")
    message = (data.get("message") or "").strip()

    errors = []

    if not name:
        errors.append("Name is required.")

    if not email or not EMAIL_RE.match(email):
        errors.append("A valid email is required.")

    if not phone or not PHONE_RE.match(phone):
        errors.append("Phone number must be a valid 10-digit number.")

    try:
        age_int = int(age)
        if age_int <= 0:
            errors.append("Age must be a positive integer.")
    except Exception:
        errors.append("Age must be a number.")

    if not message:
        errors.append("Message is required.")

    if errors:
        return jsonify({
            "error": "validation_failed",
            "details": errors
        }), 400

    submission = {
        "name": name,
        "email": email,
        "phone": phone,
        "age": age_int,
        "message": message,
        "received_at": datetime.utcnow().isoformat() + "Z"
    }

    return jsonify({
        "message": "Form received",
        "submission": submission
    }), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Development only; production is handled by pm2 / gunicorn
    app.run(host="0.0.0.0", port=5000, debug=False)
