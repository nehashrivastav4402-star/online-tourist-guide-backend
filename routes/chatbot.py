from flask import Blueprint, jsonify, request

chatbot = Blueprint("chatbot", __name__)


@chatbot.route("/chatbot", methods=["POST"])
def chatbot_response():

    data = request.get_json()
    message = data.get("message", "").lower().strip()

    if not message:
        return jsonify({
            "message": "Please enter your question"
        }), 400

    if "goa" in message:
        reply = "Goa is famous for beaches, forts, churches and beautiful tourist places."

    elif "mumbai" in message:
        reply = "Popular places in Mumbai include Gateway of India, Marine Drive and Elephanta Caves."

    elif "delhi" in message:
        reply = "Popular places in Delhi include India Gate, Red Fort and Qutub Minar."

    elif "taj mahal" in message:
        reply = "Taj Mahal is a famous historical monument located in Agra, Uttar Pradesh."

    elif "weather" in message:
        reply = "You can use the Weather feature in the app to check current weather."

    else:
        reply = "I can help you find tourist places, destinations and travel information."

    return jsonify({
        "user_message": message,
        "reply": reply
    })