from flask import Blueprint, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

contact = Blueprint("contact", __name__)


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
# USER - SUBMIT CONTACT MESSAGE
# ============================================================

@contact.route("/contact", methods=["POST"])
def submit_contact():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received"
            }), 400

        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        subject = str(data.get("subject", "")).strip()
        message = str(data.get("message", "")).strip()

        if not name or not email or not subject or not message:
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO contact
            (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
            """,
            (
                name,
                email,
                subject,
                message
            )
        )

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Contact message submitted successfully"
        }), 201

    except Exception as e:

        print("CONTACT SUBMIT ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# ADMIN - GET ALL CONTACT MESSAGES
# Supports both:
# /api/contact
# /api/admin/contact
# ============================================================

@contact.route("/contact", methods=["GET"])
@contact.route("/admin/contact", methods=["GET"])
def get_contact_messages():

    try:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                subject,
                message
            FROM contact
            ORDER BY id DESC
            """
        )

        messages = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "messages": messages
        }), 200

    except Exception as e:

        print("CONTACT FETCH ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500