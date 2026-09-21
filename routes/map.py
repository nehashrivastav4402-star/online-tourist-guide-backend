from flask import Blueprint, jsonify
import mysql.connector

map_bp = Blueprint("map_bp", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# =========================
# GET PLACES FOR MAP
# =========================

@map_bp.route("/map/places", methods=["GET"])
def get_map_places():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            name,
            state,
            location,
            rating,
            image_url,
            latitude,
            longitude
        FROM places
        WHERE latitude IS NOT NULL
        AND longitude IS NOT NULL
        ORDER BY id ASC
        """
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data), 200