from flask import Blueprint, jsonify

emergency = Blueprint("emergency", __name__)


@emergency.route("/emergency", methods=["GET"])
def get_emergency_contacts():

    contacts = [
        {
            "name": "Police",
            "number": "112"
        },
        {
            "name": "Ambulance",
            "number": "108"
        },
        {
            "name": "Fire Brigade",
            "number": "101"
        }
    ]

    return jsonify(contacts)