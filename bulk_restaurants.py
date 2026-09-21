import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NEHA@2004",
    database="tourist_guide"
)

cursor = db.cursor()

# Get all tourist places
cursor.execute("SELECT id, name FROM places")
places = cursor.fetchall()

restaurant_templates = [
    {
        "name": "Local Food Restaurant",
        "cuisine": "Indian",
        "rating": 4.0,
        "price_range": "₹200-₹500",
        "contact": "Sample Contact",
        "description": "Sample restaurant information for project demonstration."
    },
    {
        "name": "Family Restaurant",
        "cuisine": "North Indian",
        "rating": 4.2,
        "price_range": "₹500-₹1000",
        "contact": "Sample Contact",
        "description": "Sample family restaurant information for project demonstration."
    },
    {
        "name": "Traditional Food Restaurant",
        "cuisine": "Multi Cuisine",
        "rating": 4.1,
        "price_range": "₹300-₹800",
        "contact": "Sample Contact",
        "description": "Sample traditional restaurant information for project demonstration."
    }
]

added = 0

for place_id, place_name in places:

    # Check how many restaurants already exist for this place
    cursor.execute(
        "SELECT COUNT(*) FROM restaurants WHERE place_id = %s",
        (place_id,)
    )

    count = cursor.fetchone()[0]

    # Add only until there are 3 restaurants
    for i in range(count, 3):

        restaurant = restaurant_templates[i]

        cursor.execute("""
            INSERT INTO restaurants
            (place_id, name, location, cuisine, rating,
             price_range, contact, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            place_id,
            f"{restaurant['name']} - {place_name}",
            place_name,
            restaurant["cuisine"],
            restaurant["rating"],
            restaurant["price_range"],
            restaurant["contact"],
            restaurant["description"]
        ))

        added += 1

db.commit()

print(f"Restaurants added: {added}")

cursor.close()
db.close()