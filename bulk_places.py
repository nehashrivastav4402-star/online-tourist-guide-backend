import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NEHA@2004",
    database="tourist_guide"
)

cursor = db.cursor()

places = [
    ("Gateway of India", "Famous historical monument and tourist attraction.", "Mumbai, Maharashtra", "Historical"),
    ("Ajanta Caves", "Ancient Buddhist rock-cut caves.", "Aurangabad, Maharashtra", "Historical"),
    ("Ellora Caves", "Famous rock-cut cave complex.", "Aurangabad, Maharashtra", "Historical"),
    ("Mahabaleshwar", "Popular hill station known for scenic views.", "Maharashtra", "Hill Station"),
    ("Lonavala", "Popular hill station near Mumbai and Pune.", "Maharashtra", "Hill Station"),
    ("Shirdi", "Famous pilgrimage destination.", "Maharashtra", "Religious"),
    ("Elephanta Caves", "Ancient cave temples on Elephanta Island.", "Mumbai, Maharashtra", "Historical"),

    ("Taj Mahal", "World-famous white marble monument.", "Agra, Uttar Pradesh", "Historical"),
    ("Agra Fort", "Historic Mughal fort.", "Agra, Uttar Pradesh", "Historical"),
    ("Varanasi Ghats", "Famous ghats along the River Ganga.", "Varanasi, Uttar Pradesh", "Religious"),
    ("Ayodhya", "Important religious and cultural destination.", "Uttar Pradesh", "Religious"),
    ("Sarnath", "Important Buddhist pilgrimage site.", "Uttar Pradesh", "Religious"),
    ("Lucknow Bara Imambara", "Historic monument and architectural attraction.", "Lucknow, Uttar Pradesh", "Historical"),

    ("Jaipur City Palace", "Historic royal palace complex.", "Jaipur, Rajasthan", "Historical"),
    ("Amber Fort", "Historic hill fort and palace.", "Jaipur, Rajasthan", "Historical"),
    ("Hawa Mahal", "Iconic palace known for its unique windows.", "Jaipur, Rajasthan", "Historical"),
    ("Jaisalmer Fort", "Famous golden sandstone fort.", "Jaisalmer, Rajasthan", "Historical"),
    ("Udaipur City Palace", "Large palace complex overlooking Lake Pichola.", "Udaipur, Rajasthan", "Historical"),
    ("Lake Pichola", "Beautiful lake surrounded by palaces.", "Udaipur, Rajasthan", "Nature"),
    ("Mehrangarh Fort", "Massive historic fort.", "Jodhpur, Rajasthan", "Historical"),
    ("Pushkar", "Famous religious and cultural destination.", "Rajasthan", "Religious"),

    ("Goa Beaches", "Popular beaches and coastal tourist destination.", "Goa", "Beach"),
    ("Baga Beach", "Popular beach destination.", "Goa", "Beach"),
    ("Calangute Beach", "One of Goa's popular beaches.", "Goa", "Beach"),
    ("Basilica of Bom Jesus", "Historic church and UNESCO World Heritage site.", "Goa", "Religious"),

    ("Mysore Palace", "Famous royal palace.", "Mysore, Karnataka", "Historical"),
    ("Coorg", "Scenic hill station known for coffee plantations.", "Karnataka", "Hill Station"),
    ("Hampi", "Ancient ruins and UNESCO World Heritage site.", "Karnataka", "Historical"),
    ("Gokarna", "Coastal town known for beaches and temples.", "Karnataka", "Beach"),
    ("Bengaluru Palace", "Historic palace and tourist attraction.", "Bengaluru, Karnataka", "Historical"),

    ("Munnar", "Beautiful hill station surrounded by tea plantations.", "Kerala", "Hill Station"),
    ("Alleppey", "Famous for backwaters and houseboats.", "Kerala", "Nature"),
    ("Kochi Fort", "Historic coastal area with cultural attractions.", "Kochi, Kerala", "Historical"),
    ("Wayanad", "Scenic destination with forests and waterfalls.", "Kerala", "Nature"),
    ("Kovalam Beach", "Popular coastal tourist destination.", "Kerala", "Beach"),

    ("Ooty", "Popular hill station in the Nilgiri Hills.", "Tamil Nadu", "Hill Station"),
    ("Kodaikanal", "Scenic hill station known for its lake and forests.", "Tamil Nadu", "Hill Station"),
    ("Meenakshi Amman Temple", "Famous historic temple.", "Madurai, Tamil Nadu", "Religious"),
    ("Marina Beach", "One of India's famous urban beaches.", "Chennai, Tamil Nadu", "Beach"),
    ("Mahabalipuram", "Historic monuments and Shore Temple.", "Tamil Nadu", "Historical"),

    ("Red Fort", "Historic Mughal fort.", "Delhi", "Historical"),
    ("India Gate", "War memorial and major landmark.", "Delhi", "Historical"),
    ("Qutub Minar", "Historic minaret and UNESCO World Heritage site.", "Delhi", "Historical"),
    ("Lotus Temple", "Famous modern architectural landmark.", "Delhi", "Architecture"),

    ("Dal Lake", "Famous lake surrounded by mountains.", "Srinagar, Jammu and Kashmir", "Nature"),
    ("Gulmarg", "Popular mountain and winter tourism destination.", "Jammu and Kashmir", "Hill Station"),
    ("Pahalgam", "Scenic valley surrounded by mountains.", "Jammu and Kashmir", "Nature"),
    ("Vaishno Devi", "Important pilgrimage destination.", "Jammu and Kashmir", "Religious"),

    ("Manali", "Popular Himalayan hill station.", "Himachal Pradesh", "Hill Station"),
    ("Shimla", "Historic hill station and former summer capital.", "Himachal Pradesh", "Hill Station"),
    ("Dharamshala", "Mountain destination with Tibetan cultural attractions.", "Himachal Pradesh", "Hill Station"),
    ("Kasol", "Scenic mountain destination.", "Himachal Pradesh", "Nature"),

    ("Nainital", "Popular lake town and hill station.", "Uttarakhand", "Hill Station"),
    ("Mussoorie", "Popular Himalayan hill station.", "Uttarakhand", "Hill Station"),
    ("Rishikesh", "Famous spiritual and adventure destination.", "Uttarakhand", "Adventure"),
    ("Haridwar", "Important pilgrimage destination on the Ganga.", "Uttarakhand", "Religious"),
    ("Kedarnath", "Important Himalayan pilgrimage destination.", "Uttarakhand", "Religious"),
    ("Badrinath", "Major Hindu pilgrimage destination.", "Uttarakhand", "Religious"),

    ("Khajuraho Temples", "Famous historic temple complex.", "Madhya Pradesh", "Historical"),
    ("Sanchi Stupa", "Ancient Buddhist monument.", "Madhya Pradesh", "Historical"),
    ("Kanha National Park", "Famous wildlife destination.", "Madhya Pradesh", "Wildlife"),
    ("Bandhavgarh National Park", "Popular wildlife and tiger destination.", "Madhya Pradesh", "Wildlife"),

    ("Rann of Kutch", "Unique salt desert landscape.", "Gujarat", "Nature"),
    ("Somnath Temple", "Famous coastal temple.", "Gujarat", "Religious"),
    ("Statue of Unity", "Major modern landmark and tourist attraction.", "Gujarat", "Monument"),
    ("Dwarkadhish Temple", "Important pilgrimage destination.", "Gujarat", "Religious"),

    ("Darjeeling", "Famous hill station known for tea gardens.", "West Bengal", "Hill Station"),
    ("Victoria Memorial", "Historic monument and museum.", "Kolkata, West Bengal", "Historical"),
    ("Sundarbans", "Famous mangrove forest and wildlife destination.", "West Bengal", "Wildlife"),

    ("Konark Sun Temple", "Historic temple and UNESCO World Heritage site.", "Odisha", "Historical"),
    ("Jagannath Temple", "Major pilgrimage destination.", "Puri, Odisha", "Religious"),
    ("Chilika Lake", "Large coastal lagoon and wildlife destination.", "Odisha", "Nature"),

    ("Kaziranga National Park", "Famous wildlife destination.", "Assam", "Wildlife"),
    ("Majuli Island", "Large river island known for culture and nature.", "Assam", "Nature"),
    ("Kamakhya Temple", "Important pilgrimage destination.", "Guwahati, Assam", "Religious"),

    ("Shillong", "Popular hill destination known for scenic landscapes.", "Meghalaya", "Hill Station"),
    ("Cherrapunji", "Famous for rainfall, waterfalls and landscapes.", "Meghalaya", "Nature"),
    ("Living Root Bridges", "Unique natural and cultural attraction.", "Meghalaya", "Nature"),

    ("Gangtok", "Popular Himalayan destination.", "Sikkim", "Hill Station"),
    ("Tsomgo Lake", "Beautiful high-altitude lake.", "Sikkim", "Nature"),
    ("Nathula Pass", "Mountain pass near the India-China border.", "Sikkim", "Adventure"),

    ("Charminar", "Historic monument and landmark.", "Hyderabad, Telangana", "Historical"),
    ("Golconda Fort", "Historic fort and architectural attraction.", "Hyderabad, Telangana", "Historical"),
    ("Hussain Sagar Lake", "Popular lake and city landmark.", "Hyderabad, Telangana", "Nature"),

    ("Araku Valley", "Scenic valley and hill destination.", "Andhra Pradesh", "Hill Station"),
    ("Tirupati Temple", "Major pilgrimage destination.", "Andhra Pradesh", "Religious"),
    ("Visakhapatnam Beach", "Popular coastal destination.", "Andhra Pradesh", "Beach"),

    ("Nalanda", "Ancient center of learning and archaeological site.", "Bihar", "Historical"),
    ("Bodh Gaya", "Important Buddhist pilgrimage destination.", "Bihar", "Religious"),
    ("Patna Sahib", "Important Sikh pilgrimage site.", "Bihar", "Religious"),

    ("Golden Temple", "Famous Sikh pilgrimage and cultural site.", "Amritsar, Punjab", "Religious"),
    ("Jallianwala Bagh", "Historic memorial and tourist attraction.", "Amritsar, Punjab", "Historical"),
    ("Wagah Border", "Popular border ceremony attraction.", "Punjab", "Cultural"),

    ("Daman Beach", "Popular coastal destination.", "Daman and Diu", "Beach"),
    ("Port Blair", "Gateway to the Andaman Islands.", "Andaman and Nicobar Islands", "Beach"),
    ("Radhanagar Beach", "Famous tropical beach destination.", "Andaman and Nicobar Islands", "Beach"),
]

for place in places:
    cursor.execute(
        """
        SELECT id FROM places
        WHERE name = %s
        """,
        (place[0],)
    )

    if cursor.fetchone() is None:
        cursor.execute(
            """
            INSERT INTO places
            (name, description, location, category, image_url)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (place[0], place[1], place[2], place[3], "")
        )

db.commit()

print(f"{len(places)} places processed successfully!")

cursor.close()
db.close()