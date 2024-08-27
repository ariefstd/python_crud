import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

print("Connected to MySQL successfully!")
connection.close()
