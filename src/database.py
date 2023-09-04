import mysql.connector
from mysql.connector import Error

# dbConnect = mysql.connector.connect(
#     host="localhost", user="root", passwd="744542", database="moviedb"
# )
dbConnect = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12644167",
    passwd="T7PVr3i5GD",
    database="sql12644167",
)

if dbConnect.is_connected():
    db_Info = dbConnect.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    db_cursor = dbConnect.cursor()
else:
    print("Error connecting to MySQL")
