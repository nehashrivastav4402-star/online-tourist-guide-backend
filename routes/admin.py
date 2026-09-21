from flask import Blueprint, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

admin = Blueprint("admin", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tourist_guide"),
        ssl_disabled=False
    )

# =========================================================
# ADMIN TEST
# =========================================================

@admin.route("/admin/test", methods=["GET"])
def admin_test():
    return jsonify({
        "message": "Admin route is working"
    })


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin.route("/admin/dashboard", methods=["GET"])
def dashboard():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM places")
    places_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reviews")
    reviews_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback")
    feedback_count = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return jsonify({
        "users": users_count,
        "places": places_count,
        "reviews": reviews_count,
        "feedback": feedback_count
    })


# =========================================================
# ADMIN - PLACES
# =========================================================

# ADD PLACE
@admin.route("/admin/places", methods=["POST"])
def add_place():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    name = str(data.get("name", "")).strip()
    location = str(data.get("location", "")).strip()
    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip()

    if not name:
        return jsonify({
            "message": "Name is required"
        }), 400

    if len(name) < 2:
        return jsonify({
            "message": "Name must contain at least 2 characters"
        }), 400

    if not location:
        return jsonify({
            "message": "Location is required"
        }), 400

    if not category:
        return jsonify({
            "message": "Category is required"
        }), 400

    if not description:
        return jsonify({
            "message": "Description is required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO places
        (name, location, category, description)
        VALUES (%s, %s, %s, %s)
    """, (
        name,
        location,
        category,
        description
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Tourist place added successfully"
    }), 201


# VIEW ALL PLACES
@admin.route("/admin/places", methods=["GET"])
def get_places():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, location, category, description
        FROM places
        ORDER BY id
    """)

    places = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(places)


# UPDATE PLACE
@admin.route("/admin/places/<int:place_id>", methods=["PUT"])
def update_place(place_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    name = str(data.get("name", "")).strip()
    location = str(data.get("location", "")).strip()
    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip()

    if not name:
        return jsonify({
            "message": "Name is required"
        }), 400

    if len(name) < 2:
        return jsonify({
            "message": "Name must contain at least 2 characters"
        }), 400

    if not location:
        return jsonify({
            "message": "Location is required"
        }), 400

    if not category:
        return jsonify({
            "message": "Category is required"
        }), 400

    if not description:
        return jsonify({
            "message": "Description is required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM places WHERE id = %s",
        (place_id,)
    )

    existing_place = cursor.fetchone()

    if not existing_place:

        cursor.close()
        db.close()

        return jsonify({
            "message": "Tourist place not found"
        }), 404

    cursor.execute("""
        UPDATE places
        SET name = %s,
            location = %s,
            category = %s,
            description = %s
        WHERE id = %s
    """, (
        name,
        location,
        category,
        description,
        place_id
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Tourist place updated successfully"
    })


# DELETE PLACE
@admin.route("/admin/places/<int:place_id>", methods=["DELETE"])
def delete_place(place_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM places WHERE id = %s",
        (place_id,)
    )

    db.commit()

    if cursor.rowcount == 0:

        cursor.close()
        db.close()

        return jsonify({
            "message": "Tourist place not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Tourist place deleted successfully"
    })


# =========================================================
# ADMIN - USERS
# =========================================================

# VIEW ALL USERS
@admin.route("/admin/users", methods=["GET"])
def get_users():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY id
    """)

    users = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(users)


# SEARCH USERS
@admin.route("/admin/users/search", methods=["GET"])
def search_users():

    keyword = request.args.get("keyword", "").strip()

    if not keyword:
        return jsonify({
            "message": "Search keyword is required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        WHERE name LIKE %s
           OR email LIKE %s
           OR role LIKE %s
        ORDER BY id
    """, (
        search_value,
        search_value,
        search_value
    ))

    users = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(users)


# UPDATE USER
@admin.route("/admin/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    role = str(data.get("role", "")).strip().lower()

    # NAME VALIDATION
    if not name:
        return jsonify({
            "message": "Name is required"
        }), 400

    if len(name) < 2:
        return jsonify({
            "message": "Name must contain at least 2 characters"
        }), 400

    if len(name) > 100:
        return jsonify({
            "message": "Name cannot exceed 100 characters"
        }), 400

    # EMAIL VALIDATION
    if not email:
        return jsonify({
            "message": "Email is required"
        }), 400

    if len(email) > 150:
        return jsonify({
            "message": "Email cannot exceed 150 characters"
        }), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({
            "message": "Enter a valid email address"
        }), 400

    # ROLE VALIDATION
    if role not in ["user", "admin"]:
        return jsonify({
            "message": "Role must be either user or admin"
        }), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # CHECK USER
    cursor.execute("""
        SELECT id, role
        FROM users
        WHERE id = %s
    """, (user_id,))

    existing_user = cursor.fetchone()

    if not existing_user:

        cursor.close()
        db.close()

        return jsonify({
            "message": "User not found"
        }), 404

    # ADMIN PROTECTION
    if existing_user["role"] == "admin" and role != "admin":

        cursor.close()
        db.close()

        return jsonify({
            "message": "Admin role cannot be changed"
        }), 403

    # DUPLICATE EMAIL CHECK
    cursor.execute("""
        SELECT id
        FROM users
        WHERE email = %s
          AND id != %s
    """, (
        email,
        user_id
    ))

    duplicate_email = cursor.fetchone()

    if duplicate_email:

        cursor.close()
        db.close()

        return jsonify({
            "message": "Email already exists"
        }), 409

    # UPDATE USER
    cursor.execute("""
        UPDATE users
        SET name = %s,
            email = %s,
            role = %s
        WHERE id = %s
    """, (
        name,
        email,
        role,
        user_id
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "User updated successfully"
    })


# DELETE USER
@admin.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    db = get_db_connection()
    cursor = db.cursor()

    # ADMIN CANNOT BE DELETED
    cursor.execute("""
        DELETE FROM users
        WHERE id = %s
          AND role != 'admin'
    """, (user_id,))

    db.commit()

    if cursor.rowcount == 0:

        cursor.close()
        db.close()

        return jsonify({
            "message": "User not found or admin cannot be deleted"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "User deleted successfully"
    })


# =========================================================
# ADMIN - REVIEWS
# =========================================================

# VIEW ALL REVIEWS
@admin.route("/admin/reviews", methods=["GET"])
def get_reviews():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            reviews.id,
            reviews.rating,
            reviews.comment,
            reviews.user_id,
            users.name AS user_name
        FROM reviews
        JOIN users
            ON reviews.user_id = users.id
        ORDER BY reviews.id DESC
    """)

    reviews = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(reviews)


# DELETE REVIEW
@admin.route("/admin/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM reviews WHERE id = %s",
        (review_id,)
    )

    db.commit()

    if cursor.rowcount == 0:

        cursor.close()
        db.close()

        return jsonify({
            "message": "Review not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Review deleted successfully"
    })


# =========================================================
# ADMIN - FEEDBACK
# =========================================================

# VIEW ALL FEEDBACK
@admin.route("/admin/feedback", methods=["GET"])
def get_feedback():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            feedback.id,
            feedback.message,
            feedback.user_id,
            users.name AS user_name,
            users.email
        FROM feedback
        JOIN users
            ON feedback.user_id = users.id
        ORDER BY feedback.id DESC
    """)

    feedback_list = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(feedback_list)
# =========================================================
# ADMIN - CONTACT MESSAGES
# =========================================================

# VIEW ALL CONTACT MESSAGES
@admin.route("/admin/contacts", methods=["GET"])
def get_contacts():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            subject,
            message,
            created_at
        FROM contact
        ORDER BY id DESC
    """)

    contacts = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(contacts)