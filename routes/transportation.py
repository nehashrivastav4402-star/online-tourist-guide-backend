from flask import Blueprint, request, jsonify
import mysql.connector

transportation = Blueprint("transportation", __name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NEHA@2004",
        database="tourist_guide"
    )


# =====================================================
# USER - GET TRANSPORTATION FOR A PLACE
# =====================================================
@transportation.route("/transportation/<int:place_id>", methods=["GET"])
def get_transportation(place_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            place_id,
            type,
            name,
            details,
            fare,
            travel_time
        FROM transportation
        WHERE place_id = %s
        ORDER BY id ASC
    """, (place_id,))

    transport = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(transport), 200


# =====================================================
# ADMIN - GET ALL TRANSPORTATION
# =====================================================
@transportation.route("/admin/transportation", methods=["GET"])
def get_all_transportation():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            transportation.id,
            transportation.place_id,
            places.name AS place_name,
            transportation.type,
            transportation.name,
            transportation.details,
            transportation.fare,
            transportation.travel_time
        FROM transportation
        JOIN places
            ON transportation.place_id = places.id
        ORDER BY transportation.id ASC
    """)

    transport = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(transport), 200


# =====================================================
# ADMIN - ADD TRANSPORTATION
# =====================================================
@transportation.route("/admin/transportation", methods=["POST"])
def add_transportation():

    data = request.get_json()

    place_id = data.get("place_id")
    transport_type = data.get("type")
    name = data.get("name")
    details = data.get("details")
    fare = data.get("fare")
    travel_time = data.get("travel_time")

    if not place_id or not transport_type or not name:
        return jsonify({
            "message": "Place ID, type and name are required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor()

    # Check whether place exists
    cursor.execute(
        "SELECT id FROM places WHERE id = %s",
        (place_id,)
    )

    place = cursor.fetchone()

    if not place:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Place not found"
        }), 404

    cursor.execute("""
        INSERT INTO transportation
        (place_id, type, name, details, fare, travel_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        place_id,
        transport_type,
        name,
        details,
        fare,
        travel_time
    ))

    db.commit()

    new_id = cursor.lastrowid

    cursor.close()
    db.close()

    return jsonify({
        "message": "Transportation added successfully",
        "id": new_id
    }), 201


# =====================================================
# ADMIN - EDIT TRANSPORTATION
# =====================================================
@transportation.route(
    "/admin/transportation/<int:transportation_id>",
    methods=["PUT"]
)
def edit_transportation(transportation_id):

    data = request.get_json()

    place_id = data.get("place_id")
    transport_type = data.get("type")
    name = data.get("name")
    details = data.get("details")
    fare = data.get("fare")
    travel_time = data.get("travel_time")

    if not place_id or not transport_type or not name:
        return jsonify({
            "message": "Place ID, type and name are required"
        }), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check transportation exists
    cursor.execute("""
        SELECT id
        FROM transportation
        WHERE id = %s
    """, (transportation_id,))

    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Transportation not found"
        }), 404

    # Check place exists
    cursor.execute("""
        SELECT id
        FROM places
        WHERE id = %s
    """, (place_id,))

    place = cursor.fetchone()

    if not place:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Place not found"
        }), 404

    cursor.execute("""
        UPDATE transportation
        SET
            place_id = %s,
            type = %s,
            name = %s,
            details = %s,
            fare = %s,
            travel_time = %s
        WHERE id = %s
    """, (
        place_id,
        transport_type,
        name,
        details,
        fare,
        travel_time,
        transportation_id
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Transportation updated successfully"
    }), 200


# =====================================================
# ADMIN - DELETE TRANSPORTATION
# =====================================================
@transportation.route(
    "/admin/transportation/<int:transportation_id>",
    methods=["DELETE"]
)
def delete_transportation(transportation_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check transportation exists
    cursor.execute("""
        SELECT id
        FROM transportation
        WHERE id = %s
    """, (transportation_id,))

    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        db.close()

        return jsonify({
            "message": "Transportation not found"
        }), 404

    cursor.execute("""
        DELETE FROM transportation
        WHERE id = %s
    """, (transportation_id,))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Transportation deleted successfully"
    }), 200

