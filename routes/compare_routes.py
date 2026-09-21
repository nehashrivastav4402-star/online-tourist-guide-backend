from flask import Blueprint, request, jsonify

compare_routes = Blueprint("compare_routes", __name__)


@compare_routes.route("/compare-routes", methods=["POST"])
def compare_route_options():

    data = request.get_json()

    origin = data.get("origin")
    destination = data.get("destination")

    if not origin or not destination:
        return jsonify({
            "error": "Origin and destination are required"
        }), 400

    # Demo/local route data
    routes = [
        {
            "route": "Route 1",
            "distance": "150 km",
            "duration": "3 hours 10 mins",
            "type": "Balanced Route"
        },
        {
            "route": "Route 2",
            "distance": "160 km",
            "duration": "2 hours 50 mins",
            "type": "Fastest Route"
        },
        {
            "route": "Route 3",
            "distance": "145 km",
            "duration": "3 hours 30 mins",
            "type": "Shortest Route"
        }
    ]

    return jsonify({
        "origin": origin,
        "destination": destination,
        "routes": routes
    }), 200