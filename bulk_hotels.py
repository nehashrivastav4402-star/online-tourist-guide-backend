import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NEHA@2004",
    database="tourist_guide"
)

cursor = db.cursor()

# Get all existing tourist places
cursor.execute("SELECT id, name FROM places")
places = cursor.fetchall()

hotel_templates = [
    {
        "name": "City View Hotel",
        "category": "3 Star",
        "price_range": "₹1000-₹2000",
        "contact": "Sample Contact",
        "description": "Sample hotel information for project demonstration."
    },
    {
        "name": "Grand Stay Hotel",
        "category": "4 Star",
        "price_range": "₹2000-₹4000",
        "contact": "Sample Contact",
        "description": "Sample comfortable hotel information for project demonstration."
    },
    {
        "name": "Royal Palace Hotel",
        "category": "5 Star",
        "price_range": "₹4000-₹8000",
        "contact": "Sample Contact",
        "description": "Sample premium hotel information for project demonstration."
    }
]

added = 0

for place_id, place_name in places:

    # Check existing hotels for this place
    cursor.execute(
        "SELECT COUNT(*) FROM hotels WHERE place_id = %s",
        (place_id,)
    )

    count = cursor.fetchone()[0]

    # Add hotels only until there are 3
    for i in range(count, 3):

        hotel = hotel_templates[i]

        cursor.execute("""
            INSERT INTO hotels
            (place_id, name, location, category,
             price_range, contact, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            place_id,
            f"{hotel['name']} - {place_name}",
            place_name,
            hotel["category"],
            hotel["price_range"],
            hotel["contact"],
            hotel["description"]
        ))

        added += 1

db.commit()

print(f"Hotels added: {added}")
print("Total hotels in database:", len(places) * 3)

cursor.close()
db.close()