from flask import Blueprint, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

profile = Blueprint("profile", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tourist_guide"),
        ssl_disabled=False
    )
# ============================================================
# GET PROFILE
# ============================================================

@profile.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, name, email, role
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        return jsonify(user), 200

    return jsonify({
        "message": "User not found"
    }), 404


# ============================================================
# UPDATE PROFILE
# ============================================================

@profile.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not name:
        return jsonify({
            "message": "Name is required"
        }), 400

    if not email:
        return jsonify({
            "message": "Email is required"
        }), 400

    # --------------------------------------------------------
    # Database connection
    # --------------------------------------------------------

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check user exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        cursor.close()
        db.close()

        return jsonify({
            "message": "User not found"
        }), 404

    # --------------------------------------------------------
    # Update only Name and Email
    # Role will NOT be changed
    # --------------------------------------------------------

    cursor.execute(
        """
        UPDATE users
        SET name = %s,
            email = %s
        WHERE id = %s
        """,
        (name, email, user_id)
    )

    db.commit()

    # --------------------------------------------------------
    # Get updated profile
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT id, name, email, role
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    updated_user = cursor.fetchone()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Profile updated successfully",
        "user": updated_user
    }), 200