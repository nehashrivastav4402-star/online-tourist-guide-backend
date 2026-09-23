from flask import Blueprint, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

auth = Blueprint("auth", __name__)


# ============================================================
# DATABASE CONNECTION
# ============================================================

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
# REGISTER
# ============================================================

@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not name or not email or not password:
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 409

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, hashed_password, "user")
        )

        conn.commit()

        user_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "role": "user"
            }
        }), 201

    except Exception as e:
        print("REGISTER ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Registration failed",
            "error": str(e)
        }), 500


# ============================================================
# NORMAL LOGIN
# ============================================================

@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password, role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        if not check_password_hash(user["password"], password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    except Exception as e:
        print("LOGIN ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Login failed",
            "error": str(e)
        }), 500


# ============================================================
# GOOGLE LOGIN
# ============================================================

@auth.route("/google-login", methods=["POST"])
def google_login():
    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()

        if not name or not email:
            return jsonify({
                "success": False,
                "message": "Google account details are required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if Google email already exists
        cursor.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        # Existing user
        if user:
            cursor.close()
            conn.close()

            return jsonify({
                "success": True,
                "message": "Google login successful",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }), 200

        # New Google user
        cursor.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, "GOOGLE_USER", "user")
        )

        conn.commit()

        user_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Google registration and login successful",
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "role": "user"
            }
        }), 201

    except Exception as e:
        print("GOOGLE LOGIN ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Google login failed",
            "error": str(e)
        }), 500