from flask import Blueprint, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

feedback = Blueprint("feedback", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tourist_guide"),
        ssl_disabled=False
    )


# =========================
# USER - ADD FEEDBACK
# =========================
@feedback.route("/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json()

    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({
            "message": "User ID and feedback message are required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (user_id, message)
        VALUES (%s, %s)
        """,
        (user_id, message)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Feedback submitted successfully"
    }), 201


# =========================
# ADMIN - GET ALL FEEDBACK
# =========================
@feedback.route("/admin/feedback", methods=["GET"])
def get_feedback():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            feedback.id,
            feedback.user_id,
            users.name AS user_name,
            users.email AS email,
            feedback.message,
            feedback.created_at
        FROM feedback
        JOIN users ON feedback.user_id = users.id
        ORDER BY feedback.created_at DESC
        """
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data), 200


# =========================
# ADMIN - EDIT FEEDBACK
# =========================
@feedback.route("/admin/feedback/<int:feedback_id>", methods=["PUT"])
def edit_feedback(feedback_id):
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({
            "message": "Feedback message is required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check if feedback exists
    cursor.execute(
        "SELECT id FROM feedback WHERE id = %s",
        (feedback_id,)
    )

    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Feedback not found"
        }), 404

    # Update feedback
    cursor.execute(
        """
        UPDATE feedback
        SET message = %s
        WHERE id = %s
        """,
        (message, feedback_id)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Feedback updated successfully"
    }), 200


# =========================
# ADMIN - DELETE FEEDBACK
# =========================
@feedback.route("/admin/feedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check if feedback exists
    cursor.execute(
        "SELECT id FROM feedback WHERE id = %s",
        (feedback_id,)
    )

    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Feedback not found"
        }), 404

    # Delete feedback
    cursor.execute(
        """
        DELETE FROM feedback
        WHERE id = %s
        """,
        (feedback_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Feedback deleted successfully"
    }), 200
