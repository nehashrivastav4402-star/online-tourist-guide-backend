from flask import Blueprint, request, jsonify
import mysql.connector

auth = Blueprint("auth", __name__)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# ============================================================
# REGISTER
# ============================================================

@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "message": "Invalid request data"
            }), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({
                "message": "All fields are required"
            }), 400

        db = get_db_connection()
        cursor = db.cursor()

        # Check whether email already exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            cursor.close()
            db.close()

            return jsonify({
                "message": "Email already registered"
            }), 409

        # Create new normal user
        cursor.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, password, "user")
        )

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "message": "Registration successful"
        }), 201

    except Exception as e:
        print("REGISTER ERROR:", e)

        return jsonify({
            "message": "Registration failed",
            "error": str(e)
        }), 500


# ============================================================
# NORMAL EMAIL + PASSWORD LOGIN
# ============================================================

@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "message": "Invalid request data"
            }), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "message": "Email and password are required"
            }), 400

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE email = %s AND password = %s
            """,
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            return jsonify({
                "message": "Login successful",
                "user": user
            }), 200

        return jsonify({
            "message": "Invalid email or password"
        }), 401

    except Exception as e:
        print("LOGIN ERROR:", e)

        return jsonify({
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

        if not data:
            return jsonify({
                "message": "Invalid request data"
            }), 400

        google_id = data.get("google_id")
        name = data.get("name")
        email = data.get("email")

        # google_id is received from Flutter/Firebase.
        # We don't store it because the current users table
        # does not contain a google_id column.

        if not google_id:
            return jsonify({
                "message": "Google ID is required"
            }), 400

        if not email:
            return jsonify({
                "message": "Google email is required"
            }), 400

        if not name:
            name = "Google User"

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Check whether this email already exists
        cursor.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        # --------------------------------------------------------
        # New Google user
        # --------------------------------------------------------

        if not user:

            cursor.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    "",
                    "user"
                )
            )

            db.commit()

            user_id = cursor.lastrowid

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

        return jsonify({
            "message": "Google login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    except Exception as e:
        print("GOOGLE LOGIN ERROR:", e)

        return jsonify({
            "message": "Google login failed",
            "error": str(e)
        }), 500