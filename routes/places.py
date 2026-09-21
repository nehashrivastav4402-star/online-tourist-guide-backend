from flask import Blueprint, request, jsonify
import mysql.connector

places = Blueprint("places", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# =========================
# IMAGE URL VALIDATION
# =========================

def valid_image_url(url):
    if not url:
        return True

    return url.startswith("http://") or url.startswith("https://")


# =========================
# GET ALL TOURIST PLACES
# =========================

@places.route("/places", methods=["GET"])
def get_places():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM places ORDER BY id ASC")

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)


# =========================
# ADD TOURIST PLACE
# =========================

@places.route("/places", methods=["POST"])
def add_place():
    data = request.get_json() or {}

    name = data.get("name")
    state = data.get("state")
    description = data.get("description")
    location = data.get("location")
    category = data.get("category")
    rating = data.get("rating")

    image_url = data.get("image_url")
    image_url2 = data.get("image_url2")
    image_url3 = data.get("image_url3")
    image_url4 = data.get("image_url4")
    image_url5 = data.get("image_url5")
    image_url6 = data.get("image_url6")

    # -------------------------
    # REQUIRED FIELD VALIDATION
    # -------------------------

    if not name:
        return jsonify({"message": "Place name is required"}), 400

    if not state:
        return jsonify({"message": "State is required"}), 400

    if not description:
        return jsonify({"message": "Description is required"}), 400

    if not location:
        return jsonify({"message": "Location is required"}), 400

    if rating is None:
        return jsonify({"message": "Rating is required"}), 400

    # -------------------------
    # RATING VALIDATION
    # -------------------------

    try:
        rating = float(rating)
    except (ValueError, TypeError):
        return jsonify({"message": "Rating must be a number"}), 400

    if rating < 0 or rating > 5:
        return jsonify({
            "message": "Rating must be between 0 and 5"
        }), 400

    # -------------------------
    # MAIN IMAGE VALIDATION
    # -------------------------

    if not image_url:
        return jsonify({
            "message": "Main image URL is required"
        }), 400

    if not valid_image_url(image_url):
        return jsonify({
            "message": "Invalid main image URL"
        }), 400

    # -------------------------
    # EXTRA IMAGE VALIDATION
    # -------------------------

    extra_images = [
        image_url2,
        image_url3,
        image_url4,
        image_url5,
        image_url6
    ]

    for index, image in enumerate(extra_images, start=2):
        if image and not valid_image_url(image):
            return jsonify({
                "message": f"Invalid image URL {index}"
            }), 400

    # -------------------------
    # DATABASE INSERT
    # -------------------------

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO places
        (
            name,
            state,
            description,
            location,
            category,
            rating,
            image_url,
            image_url2,
            image_url3,
            image_url4,
            image_url5,
            image_url6
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            name,
            state,
            description,
            location,
            category,
            rating,
            image_url,
            image_url2,
            image_url3,
            image_url4,
            image_url5,
            image_url6
        )
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Place added successfully"
    }), 201


# =========================
# UPDATE TOURIST PLACE
# =========================

@places.route("/places/<int:id>", methods=["PUT"])
def update_place(id):
    data = request.get_json() or {}

    name = data.get("name")
    state = data.get("state")
    description = data.get("description")
    location = data.get("location")
    category = data.get("category")
    rating = data.get("rating")

    image_url = data.get("image_url")
    image_url2 = data.get("image_url2")
    image_url3 = data.get("image_url3")
    image_url4 = data.get("image_url4")
    image_url5 = data.get("image_url5")
    image_url6 = data.get("image_url6")

    # -------------------------
    # REQUIRED FIELD VALIDATION
    # -------------------------

    if not name:
        return jsonify({
            "message": "Place name is required"
        }), 400

    if not state:
        return jsonify({
            "message": "State is required"
        }), 400

    if not description:
        return jsonify({
            "message": "Description is required"
        }), 400

    if not location:
        return jsonify({
            "message": "Location is required"
        }), 400

    if rating is None:
        return jsonify({
            "message": "Rating is required"
        }), 400

    # -------------------------
    # RATING VALIDATION
    # -------------------------

    try:
        rating = float(rating)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Rating must be a number"
        }), 400

    if rating < 0 or rating > 5:
        return jsonify({
            "message": "Rating must be between 0 and 5"
        }), 400

    # -------------------------
    # MAIN IMAGE VALIDATION
    # -------------------------

    if not image_url:
        return jsonify({
            "message": "Main image URL is required"
        }), 400

    if not valid_image_url(image_url):
        return jsonify({
            "message": "Invalid main image URL"
        }), 400

    # -------------------------
    # EXTRA IMAGE VALIDATION
    # -------------------------

    extra_images = [
        image_url2,
        image_url3,
        image_url4,
        image_url5,
        image_url6
    ]

    for index, image in enumerate(extra_images, start=2):
        if image and not valid_image_url(image):
            return jsonify({
                "message": f"Invalid image URL {index}"
            }), 400

    # -------------------------
    # DATABASE UPDATE
    # -------------------------

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE places
        SET
            name=%s,
            state=%s,
            description=%s,
            location=%s,
            category=%s,
            rating=%s,
            image_url=%s,
            image_url2=%s,
            image_url3=%s,
            image_url4=%s,
            image_url5=%s,
            image_url6=%s
        WHERE id=%s
        """,
        (
            name,
            state,
            description,
            location,
            category,
            rating,
            image_url,
            image_url2,
            image_url3,
            image_url4,
            image_url5,
            image_url6,
            id
        )
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Place not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Place updated successfully"
    }), 200


# =========================
# DELETE TOURIST PLACE
# =========================

@places.route("/places/<int:id>", methods=["DELETE"])
def delete_place(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM places WHERE id=%s",
        (id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Place not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Place deleted successfully"
    }), 200


# =========================
# SEARCH TOURIST PLACES
# =========================

@places.route("/places/search", methods=["GET"])
def search_places():
    search = request.args.get("q", "")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM places
        WHERE name LIKE %s
        OR location LIKE %s
        OR category LIKE %s
        OR state LIKE %s
        """,
        (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)