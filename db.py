import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NEHA@2004",
    database="tourist_guide"
)

print("MySQL Database Connected Successfully!")

db.close()