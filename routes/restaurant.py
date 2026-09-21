from flask import Blueprint, request, jsonify
import mysql.connector

restaurant_bp = Blueprint("restaurant", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# ---------------------------------------------------------
# USER SIDE - Get restaurants of a particular tourist place
# ---------------------------------------------------------
@restaurant_bp.route("/restaurants/<int:place_id>", methods=["GET"])
def get_restaurants(place_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            place_id,
            name,
            location,
            cuisine,
            rating,
            price_range,
            contact,
            description,
            image_url,
            image_url2,
            image_url3,
            image_url4
        FROM restaurants
        WHERE place_id = %s
        ORDER BY id
    """, (place_id,))

    restaurants = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(restaurants), 200


# ---------------------------------------------------------
# ADMIN SIDE - Get all restaurants
# ---------------------------------------------------------
@restaurant_bp.route("/restaurants", methods=["GET"])
def get_all_restaurants():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            place_id,
            name,
            location,
            cuisine,
            rating,
            price_range,
            contact,
            description,
            image_url,
            image_url2,
            image_url3,
            image_url4
        FROM restaurants
        ORDER BY id
    """)

    restaurants = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(restaurants), 200


# ---------------------------------------------------------
# ADMIN SIDE - Add restaurant
# ---------------------------------------------------------
@restaurant_bp.route("/restaurants", methods=["POST"])
def add_restaurant():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    place_id = data.get("place_id")
    name = data.get("name")
    location = data.get("location")
    cuisine = data.get("cuisine")
    rating = data.get("rating")
    price_range = data.get("price_range")
    contact = data.get("contact")
    description = data.get("description")

    image_url = data.get("image_url")
    image_url2 = data.get("image_url2")
    image_url3 = data.get("image_url3")
    image_url4 = data.get("image_url4")

    # -----------------------------------------------------
    # Place ID validation
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # Name validation
    # -----------------------------------------------------
    if not name or not name.strip():
        return jsonify({
            "message": "Restaurant name is required"
        }), 400

    if len(name.strip()) < 2:
        return jsonify({
            "message": "Restaurant name must contain at least 2 characters"
        }), 400

    # -----------------------------------------------------
    # Location validation
    # -----------------------------------------------------
    if not location or not location.strip():
        return jsonify({
            "message": "Location is required"
        }), 400

    # -----------------------------------------------------
    # Cuisine validation
    # -----------------------------------------------------
    if not cuisine or not cuisine.strip():
        return jsonify({
            "message": "Cuisine is required"
        }), 400

    # -----------------------------------------------------
    # Rating validation
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # Price validation
    # -----------------------------------------------------
    if not price_range or not price_range.strip():
        return jsonify({
            "message": "Price range is required"
        }), 400

    # -----------------------------------------------------
    # Contact validation
    # -----------------------------------------------------
    if not contact or not contact.strip():
        return jsonify({
            "message": "Contact is required"
        }), 400

    if len(contact.strip()) < 10:
        return jsonify({
            "message": "Contact must contain at least 10 characters"
        }), 400

    # -----------------------------------------------------
    # Description validation
    # -----------------------------------------------------
    if not description or not description.strip():
        return jsonify({
            "message": "Description is required"
        }), 400

    if len(description.strip()) < 10:
        return jsonify({
            "message": "Description must contain at least 10 characters"
        }), 400

    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------
    db = get_db_connection()
    cursor = db.cursor()

    # Check tourist place
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

    # -----------------------------------------------------
    # Insert restaurant
    # -----------------------------------------------------
    cursor.execute("""
        INSERT INTO restaurants
        (
            place_id,
            name,
            location,
            cuisine,
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
        cuisine.strip(),
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
        "message": "Restaurant added successfully"
    }), 201


# ---------------------------------------------------------
# ADMIN SIDE - Update restaurant
# ---------------------------------------------------------
@restaurant_bp.route("/restaurants/<int:id>", methods=["PUT"])
def update_restaurant(id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request data is required"
        }), 400

    place_id = data.get("place_id")
    name = data.get("name")
    location = data.get("location")
    cuisine = data.get("cuisine")
    rating = data.get("rating")
    price_range = data.get("price_range")
    contact = data.get("contact")
    description = data.get("description")

    image_url = data.get("image_url")
    image_url2 = data.get("image_url2")
    image_url3 = data.get("image_url3")
    image_url4 = data.get("image_url4")

    # -----------------------------------------------------
    # Place ID validation
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # Name validation
    # -----------------------------------------------------
    if not name or not name.strip():
        return jsonify({
            "message": "Restaurant name is required"
        }), 400

    if len(name.strip()) < 2:
        return jsonify({
            "message": "Restaurant name must contain at least 2 characters"
        }), 400

    # -----------------------------------------------------
    # Location validation
    # -----------------------------------------------------
    if not location or not location.strip():
        return jsonify({
            "message": "Location is required"
        }), 400

    # -----------------------------------------------------
    # Cuisine validation
    # -----------------------------------------------------
    if not cuisine or not cuisine.strip():
        return jsonify({
            "message": "Cuisine is required"
        }), 400

    # -----------------------------------------------------
    # Rating validation
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # Price validation
    # -----------------------------------------------------
    if not price_range or not price_range.strip():
        return jsonify({
            "message": "Price range is required"
        }), 400

    # -----------------------------------------------------
    # Contact validation
    # -----------------------------------------------------
    if not contact or not contact.strip():
        return jsonify({
            "message": "Contact is required"
        }), 400

    if len(contact.strip()) < 10:
        return jsonify({
            "message": "Contact must contain at least 10 characters"
        }), 400

    # -----------------------------------------------------
    # Description validation
    # -----------------------------------------------------
    if not description or not description.strip():
        return jsonify({
            "message": "Description is required"
        }), 400

    if len(description.strip()) < 10:
        return jsonify({
            "message": "Description must contain at least 10 characters"
        }), 400

    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------
    db = get_db_connection()
    cursor = db.cursor()

    # Check tourist place
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

    # -----------------------------------------------------
    # Update restaurant
    # -----------------------------------------------------
    cursor.execute("""
        UPDATE restaurants
        SET
            place_id = %s,
            name = %s,
            location = %s,
            cuisine = %s,
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
        cuisine.strip(),
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
            "message": "Restaurant not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Restaurant updated successfully"
    }), 200


# ---------------------------------------------------------
# ADMIN SIDE - Delete restaurant
# ---------------------------------------------------------
@restaurant_bp.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM restaurants WHERE id = %s",
        (id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Restaurant not found"
        }), 404

    cursor.close()
    db.close()

    return jsonify({
        "message": "Restaurant deleted successfully"
    }), 200