from flask import Blueprint, request, jsonify
import mysql.connector

reviews = Blueprint("reviews", __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# Add review
@reviews.route("/reviews", methods=["POST"])
def add_review():
    data = request.get_json()

    user_id = data.get("user_id")
    place_id = data.get("place_id")
    rating = data.get("rating")
    comment = data.get("comment")

    if not user_id or not place_id or not rating:
        return jsonify({"message": "User, place and rating are required"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO reviews
        (user_id, place_id, rating, comment)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, place_id, rating, comment)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Review added successfully"}), 201


# Get reviews for a place
@reviews.route("/places/<int:place_id>/reviews", methods=["GET"])
def get_reviews(place_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT reviews.id, users.name, reviews.rating,
               reviews.comment, reviews.created_at
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.place_id = %s
        ORDER BY reviews.created_at DESC
        """,
        (place_id,)
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)