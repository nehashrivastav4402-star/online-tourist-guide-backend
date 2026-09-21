import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NEHA@2004",          # agar MySQL password hai to yahan likho
    database="tourist_guide"
)

cursor = db.cursor()

# Transportation types
transport_types = [
    ("Train", "Nearest railway station"),
    ("Bus", "Local bus service available"),
    ("Taxi", "Taxi/cab service available"),
    ("Flight", "Nearest airport")
]

# Saare tourist places
cursor.execute("SELECT id, name FROM places")
places = cursor.fetchall()

print("Total places:", len(places))

added = 0

for place_id, place_name in places:

    # Check if transportation already exists
    cursor.execute(
        "SELECT COUNT(*) FROM transportation WHERE place_id = %s",
        (place_id,)
    )

    count = cursor.fetchone()[0]

    # Agar already transportation hai to skip
    if count > 0:
        print(f"Skipping {place_id} - {place_name} (already exists)")
        continue

    # 4 transportation records add karo
    for transport_type, detail in transport_types:

        if transport_type == "Train":
            name = f"Nearest Railway Station for {place_name}"
            fare = "₹50-₹500"
            travel_time = "15-60 minutes"

        elif transport_type == "Bus":
            name = f"Local Bus Stand near {place_name}"
            fare = "₹20-₹100"
            travel_time = "20-90 minutes"

        elif transport_type == "Taxi":
            name = f"Local Taxi to {place_name}"
            fare = "₹150-₹1000"
            travel_time = "15-60 minutes"

        else:
            name = f"Nearest Airport for {place_name}"
            fare = "₹2000-₹8000"
            travel_time = "30-120 minutes"

        cursor.execute("""
            INSERT INTO transportation
            (place_id, type, name, details, fare, travel_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            place_id,
            transport_type,
            name,
            detail,
            fare,
            travel_time
        ))

        added += 1

    print(f"Added transportation for {place_id} - {place_name}")

db.commit()

cursor.close()
db.close()

print("\n================================")
print("Transportation added:", added)
print("================================")