from flask import Flask
from flask_cors import CORS

from routes.auth import auth
from routes.places import places
from routes.reviews import reviews
from routes.profile import profile
from routes.feedback import feedback
from routes.admin import admin
from routes.budget import budget
from routes.emergency import emergency
from routes.chatbot import chatbot
from routes.weather import weather
from routes.transportation import transportation
from routes.hotel import hotel
from routes.restaurant import restaurant_bp
from routes.contact import contact
from routes.compare_routes import compare_routes
from routes.saved_places import saved_places
from routes.map import map_bp

app = Flask(__name__)

# Allow Flutter Web to access Flask APIs
CORS(app
     , resources={r"/api/*": {"origins": "*"}}
     , methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      allow_headers=["Content-Type", "Authorization"]
     )

app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(places, url_prefix="/api")
app.register_blueprint(reviews, url_prefix="/api")
app.register_blueprint(profile, url_prefix="/api")
app.register_blueprint(feedback, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api")
app.register_blueprint(budget, url_prefix="/api")
app.register_blueprint(emergency, url_prefix="/api")
app.register_blueprint(chatbot, url_prefix="/api")
app.register_blueprint(weather, url_prefix="/api")
app.register_blueprint(transportation, url_prefix="/api")
app.register_blueprint(hotel, url_prefix="/api")
app.register_blueprint(restaurant_bp, url_prefix="/api")
app.register_blueprint(contact, url_prefix="/api")
app.register_blueprint(compare_routes, url_prefix="/api")
app.register_blueprint(saved_places, url_prefix="/api")
app.register_blueprint(map_bp, url_prefix="/api")


@app.route("/")
def home():
    return "Online Tourist Guide System Backend is Running!"


print(app.url_map)


if __name__ == "__main__":
    app.run(debug=False)