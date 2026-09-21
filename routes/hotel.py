from flask import Blueprint, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

hotel = Blueprint("hotel", __name__)


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
# USER SIDE - Get hotels for a particular tourist place
# =========================================================
@hotel.route("/hotels/<int:place_id>", methods=["GET"])
def get_hotels(place_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            place_id,
            name,
            location,
            category,
            rating,
            price_range,
            contact,
            description,
            image_url,
            image_url2,
            image_url3,
            image_url4
        FROM hotels
        WHERE place_id = %s
        ORDER BY id
    """, (place_id,))

    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(hotels), 200


# =========================================================
# ADMIN SIDE - Get all hotels
# =========================================================
@hotel.route("/hotels", methods=["GET"])
def get_all_hotels():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            place_id,
            name,
            location,
            category,
            rating,
            price_range,
            contact,
            description,
            image_url,
            image_url2,
            image_url3,
            image_url4
        FROM hotels
        ORDER BY id
    """)

    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(hotels), 200


# =========================================================
# ADMIN SIDE - Add hotel
# =========================================================
@hotel.route("/hotels", methods=["POST"])
def add_hotel():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    place_id = data.get("place_id")
    name = data.get("name")
    location = data.get("location")
    category = data.get("category")
    rating = data.get("rating")
    price_range = data.get("price_range")
    contact = data.get("contact")
    description = data.get("description")

    image_url = data.get("image_url")
    image_url2 = data.get("image_url2")
    image_url3 = data.get("image_url3")
    image_url4 = data.get("image_url4")

    # -------------------------
    # Place ID validation
    # -------------------------
    if place_id is None:
        return jsonify({
            "message": "Place ID is required"
        }), 400

    try:
        place_id = int(place_id)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Place ID must be a number"
        }), 400

    if place_id <= 0:
        return jsonify({
            "message": "Place ID must be greater than 0"
        }), 400

    # -------------------------
    # Name validation
    # -------------------------
    if not name or not name.strip():
        return jsonify({
            "message": "Hotel name is required"
        }), 400

    if len(name.strip()) < 2:
        return jsonify({
            "message": "Hotel name must contain at least 2 characters"
        }), 400

    # -------------------------
    # Location
    # -------------------------
    if not location or not location.strip():
        return jsonify({
            "message": "Location is required"
        }), 400

    # -------------------------
    # Category
    # -------------------------
    if not category or not category.strip():
        return jsonify({
            "message": "Category is required"
        }), 400

    # -------------------------
    # Rating validation
    # -------------------------
    if rating is None or rating == "":
        return jsonify({
            "message": "Rating is required"
        }), 400

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
    # Price range
    # -------------------------
    if not price_range or not price_range.strip():
        return jsonify({
            "message": "Price range is required"
        }), 400

    # -------------------------
    # Contact
    # -------------------------
    if not contact or not contact.strip():
        return jsonify({
            "message": "Contact is required"
        }), 400

    # -------------------------
    # Description
    # -------------------------
    if not description or not description.strip():
        return jsonify({
            "message": "Description is required"
        }), 400

    if len(description.strip()) < 10:
        return jsonify({
            "message": "Description must contain at least 10 characters"
        }), 400

    # -------------------------
    # Database
    # -------------------------
    db = get_db_connection()
    cursor = db.cursor()

    # Check place exists
    cursor.execute(
        "SELECT id FROM places WHERE id = %s",
        (place_id,)
    )

    place = cursor.fetchone()

    if not place:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Tourist place not found"
        }), 404

    # Insert hotel
    cursor.execute("""
        INSERT INTO hotels
        (
            place_id,
            name,
            location,
            category,
            rating,
            price_range,
            contact,
            description,
            image_url,
            image_url2,
            image_url3,
            image_url4
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        place_id,
        name.strip(),
        location.strip(),
        category.strip(),
        rating,
        price_range.strip(),
        contact.strip(),
        description.strip(),
        image_url.strip() if image_url else None,
        image_url2.strip() if image_url2 else None,
        image_url3.strip() if image_url3 else None,
        image_url4.strip() if image_url4 else None
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Hotel added successfully"
    }), 201


# =========================================================
# ADMIN SIDE - Update hotel
# =========================================================
@hotel.route("/hotels/<int:id>", methods=["PUT"])
def update_hotel(id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    place_id = data.get("place_id")
    name = data.get("name")
    location = data.get("location")
    category = data.get("category")
    rating = data.get("rating")
    price_range = data.get("price_range")
    contact = data.get("contact")
    description = data.get("description")

    image_url = data.get("image_url")
    image_url2 = data.get("image_url2")
    image_url3 = data.get("image_url3")
    image_url4 = data.get("image_url4")

    # -------------------------
    # Place ID
    # -------------------------
    if place_id is None:
        return jsonify({
            "message": "Place ID is required"
        }), 400

    try:
        place_id = int(place_id)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Place ID must be a number"
        }), 400

    if place_id <= 0:
        return jsonify({
            "message": "Place ID must be greater than 0"
        }), 400

    # -------------------------
    # Name
    # -------------------------
    if not name or not name.strip():
        return jsonify({
            "message": "Hotel name is required"
        }), 400

    if len(name.strip()) < 2:
        return jsonify({
            "message": "Hotel name must contain at least 2 characters"
        }), 400

    # -------------------------
    # Location
    # -------------------------
    if not location or not location.strip():
        return jsonify({
            "message": "Location is required"
        }), 400

    # -------------------------
    # Category
    # -------------------------
    if not category or not category.strip():
        return jsonify({
            "message": "Category is required"
        }), 400

    # -------------------------
    # Rating
    # -------------------------
    if rating is None or rating == "":
        return jsonify({
            "message": "Rating is required"
        }), 400

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
    # Price
    # -------------------------
    if not price_range or not price_range.strip():
        return jsonify({
            "message": "Price range is required"
        }), 400

    # -------------------------
    # Contact
    # -------------------------
    if not contact or not contact.strip():
        return jsonify({
            "message": "Contact is required"
        }), 400

    # -------------------------
    # Description
    # -------------------------
    if not description or not description.strip():
        return jsonify({
            "message": "Description is required"
        }), 400

    if len(description.strip()) < 10:
        return jsonify({
            "message": "Description must contain at least 10 characters"
        }), 400

    # -------------------------
    # Database
    # -------------------------
    db = get_db_connection()
    cursor = db.cursor()

    # Check place exists
    cursor.execute(
        "SELECT id FROM places WHERE id = %s",
        (place_id,)
    )

    place = cursor.fetchone()

    if not place:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Tourist place not found"
        }), 404

    # Update hotel
    cursor.execute("""
        UPDATE hotels
        SET
            place_id = %s,
            name = %s,
            location = %s,
            category = %s,
            rating = %s,
            price_range = %s,
            contact = %s,
            description = %s,
            image_url = %s,
            image_url2 = %s,
            image_url3 = %s,
            image_url4 = %s
        WHERE id = %s
    """, (
        place_id,
        name.strip(),
        location.strip(),
        category.strip(),
        rating,
        price_range.strip(),
        contact.strip(),
        description.strip(),
        image_url.strip() if image_url else None,
        image_url2.strip() if image_url2 else None,
        image_url3.strip() if image_url3 else None,
        image_url4.strip() if image_url4 else None,
        id
    ))

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Hotel not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Hotel updated successfully"
    }), 200


# =========================================================
# ADMIN SIDE - Delete hotel
# =========================================================
@hotel.route("/hotels/<int:id>", methods=["DELETE"])
def delete_hotel(id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM hotels WHERE id = %s",
        (id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Hotel not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Hotel deleted successfully"
    }), 200