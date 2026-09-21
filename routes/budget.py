from flask import Blueprint, jsonify, request

budget = Blueprint("budget", __name__)


@budget.route("/budget/plan", methods=["POST"])
def create_budget_plan():

    data = request.get_json()

    destination = data.get("destination")
    days = data.get("days")
    people = data.get("people")
    total_budget = data.get("budget")

    if not destination or not days or not people or not total_budget:
        return jsonify({
            "message": "All fields are required"
        }), 400

    days = int(days)
    people = int(people)
    total_budget = float(total_budget)

    # Basic estimated expenses
    stay = total_budget * 0.30
    food = total_budget * 0.20
    transport = total_budget * 0.20
    activities = total_budget * 0.15
    other = total_budget * 0.05

    estimated_total = stay + food + transport + activities + other
    remaining = total_budget - estimated_total

    return jsonify({
        "destination": destination,
        "days": days,
        "people": people,
        "budget": total_budget,
        "estimated_expenses": {
            "stay": round(stay, 2),
            "food": round(food, 2),
            "transport": round(transport, 2),
            "activities": round(activities, 2),
            "other": round(other, 2)
        },
        "estimated_total": round(estimated_total, 2),
        "remaining_budget": round(remaining, 2)
    })