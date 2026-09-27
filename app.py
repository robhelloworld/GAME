from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS if your frontend and backend run on different domains/ports
CORS(app)

# 1. SECRET SEAT ANSWERS (Hidden on server)
CHAIR_ANSWERS = {
    str(i): {"firstName": "NameFather305", "fatherName": "NameFather305"}
    for i in range(1, 29)
}

# 2. SECRET QUIZ ANSWERS (Hidden on server)
QUIZ_ANSWERS = {
    "q1": "none",
    "q2": "5",
    "q3": "3",
    "q4": "1",
    "q5": "N",
    "q6": ["305", "305"]
}

@app.route("/api/validate-seats", methods=["POST"])
def validate_seats():
    """Validates that all seat names are filled out by the user."""
    data = request.json or {}
    user_seats = data.get("seats", {})

    # Ensure all 28 chairs are submitted
    if len(user_seats) < 28:
        return jsonify({"valid": False, "message": "Fill every chair before continuing."}), 400

    # Validate that each seat's firstName and fatherName are not empty
    for chair_id in range(1, 29):  # Adjust range or keys based on your CHAIR_ANSWERS setup
        chair_key = str(chair_id) # or chair_id depending on your key type
        user_chair = user_seats.get(chair_key, {})
        
        user_first = str(user_chair.get("firstName", "")).strip()
        user_father = str(user_chair.get("fatherName", "")).strip()

        # Check if either field is empty
        if not user_first or not user_father:
            return jsonify({
                "valid": False,
                "message": f"Chair {chair_key} is missing name information."
            }), 200

    return jsonify({"valid": True, "message": "All seats are filled!"}), 200


@app.route("/api/submit-quiz", methods=["POST"])
def submit_quiz():
    """Validates quiz submissions and determines win/loss status."""
    data = request.json or {}
    
    q1 = str(data.get("q1", "")).strip()
    q2 = str(data.get("q2", "")).strip()
    q3 = str(data.get("q3", "")).strip()
    q4 = str(data.get("q4", "")).strip()
    q5 = str(data.get("q5", "")).strip()
    q6 = str(data.get("q6", "")).strip().lower()

    if not all([q1, q2, q3, q4, q5, q6]):
        return jsonify({"valid": False, "message": "Answer all six questions."}), 400

    # Perform secret check
    all_correct = (
        q1 == QUIZ_ANSWERS["q1"] and
        q2 == QUIZ_ANSWERS["q2"] and
        q3 == QUIZ_ANSWERS["q3"] and
        q4 == QUIZ_ANSWERS["q4"] and
        q5 == QUIZ_ANSWERS["q5"] and
        q6 in QUIZ_ANSWERS["q6"]
    )

    return jsonify({"won": all_correct}), 200

if __name__ == "__main__":
    # Run server locally on http://localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)