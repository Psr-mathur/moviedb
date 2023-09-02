import mysql.connector
from mysql.connector import Error

dbConnect = mysql.connector.connect(
    host="localhost", user="root", passwd="744542", database="moviedb"
)

if dbConnect.is_connected():
    db_Info = dbConnect.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    db_cursor = dbConnect.cursor()
else:
    print("Error connecting to MySQL")
