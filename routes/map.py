from flask import Blueprint, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

map_bp = Blueprint("map_bp", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tourist_guide"),
        ssl_disabled=False
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