from flask import Blueprint, request, jsonify
import mysql.connector

saved_places = Blueprint("saved_places", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# ============================================================
# SAVE PLACE
# ============================================================

@saved_places.route("/saved-places", methods=["POST"])
def save_place():

    data = request.get_json()

    user_id = data.get("user_id")
    place_id = data.get("place_id")

    if not user_id or not place_id:
        return jsonify({
            "error": "user_id and place_id are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Check whether place is already saved
        cursor.execute(
            """
            SELECT id
            FROM saved_places
            WHERE user_id = %s AND place_id = %s
            """,
            (user_id, place_id)
        )

        existing = cursor.fetchone()

        if existing:
            return jsonify({
                "message": "Place already saved",
                "saved": True
            }), 200

        # Save place
        cursor.execute(
            """
            INSERT INTO saved_places (user_id, place_id)
            VALUES (%s, %s)
            """,
            (user_id, place_id)
        )

        conn.commit()

        return jsonify({
            "message": "Place saved successfully",
            "saved": True
        }), 201

    except mysql.connector.Error as e:

        conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()


# ============================================================
# GET SAVED PLACES
# ============================================================

@saved_places.route(
    "/saved-places/<int:user_id>",
    methods=["GET"]
)
def get_saved_places(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                p.id,
                p.name,
                p.state,
                p.description,
                p.location,
                p.rating,
                p.image_url,
                s.created_at
            FROM saved_places s
            JOIN places p
                ON s.place_id = p.id
            WHERE s.user_id = %s
            ORDER BY s.created_at DESC
            """,
            (user_id,)
        )

        places = cursor.fetchall()

        return jsonify(places), 200

    except mysql.connector.Error as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()


# ============================================================
# CHECK WHETHER PLACE IS SAVED
# ============================================================

@saved_places.route(
    "/saved-places/<int:user_id>/<int:place_id>",
    methods=["GET"]
)
def check_saved_place(user_id, place_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT id
            FROM saved_places
            WHERE user_id = %s AND place_id = %s
            """,
            (user_id, place_id)
        )

        saved = cursor.fetchone()

        return jsonify({
            "saved": saved is not None
        }), 200

    except mysql.connector.Error as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()


# ============================================================
# REMOVE SAVED PLACE
# ============================================================

@saved_places.route(
    "/saved-places/<int:user_id>/<int:place_id>",
    methods=["DELETE"]
)
def remove_saved_place(user_id, place_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM saved_places
            WHERE user_id = %s AND place_id = %s
            """,
            (user_id, place_id)
        )

        conn.commit()

        deleted = cursor.rowcount

        if deleted == 0:
            return jsonify({
                "message": "Place was not saved",
                "saved": False
            }), 404

        return jsonify({
            "message": "Place removed from saved places",
            "saved": False
        }), 200

    except mysql.connector.Error as e:

        conn.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

