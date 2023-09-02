from flask import Blueprint, jsonify, request, make_response
from database import db_cursor, dbConnect
from mysql.connector import Error
from flask_jwt_extended import jwt_required

movies = Blueprint("movies", __name__, url_prefix="/api/movies")


@movies.get("/")
def Get_movies():
    genre = request.args.get("genre")
    if genre is not None:
        try:
            db_cursor.execute(
                "SELECT movies.* FROM movies JOIN genres ON movies.id = genres.movie_id WHERE genres.genre = %s",
                (genre,),
            )
            rows = db_cursor.fetchall()
            column_names = [desc[0] for desc in db_cursor.description]
            movies = [dict(zip(column_names, row)) for row in rows]
            resp = make_response(jsonify({"data": movies}), 200)
            return resp
        except Error:
            return make_response(jsonify({"error": "Server Error"}), 500)

    rating = request.args.get("rating")
    if rating is not None:
        try:
            db_cursor.execute(
                "SELECT movies.* FROM movies WHERE imdb_score >= %s", (rating,)
            )
            rows = db_cursor.fetchall()
            column_names = [desc[0] for desc in db_cursor.description]
            movies = [dict(zip(column_names, row)) for row in rows]
            resp = make_response(jsonify({"data": movies}), 200)
            return resp
        except Error:
            return make_response(jsonify({"error": "Server Error"}), 500)

    director = request.args.get("director", "")
    if director is not None:
        try:
            db_cursor.execute(
                "SELECT movies.* FROM movies WHERE director = %s", (director,)
            )
            rows = db_cursor.fetchall()
            column_names = [desc[0] for desc in db_cursor.description]
            movies = [dict(zip(column_names, row)) for row in rows]
            resp = make_response(jsonify({"data": movies}), 200)
            return resp
        except Error:
            return make_response(jsonify({"error": "Server Error"}), 500)

    try:
        db_cursor.execute("Select * from movies")
        rows = db_cursor.fetchall()
        column_names = [desc[0] for desc in db_cursor.description]
        movies = [dict(zip(column_names, row)) for row in rows]
        resp = make_response(jsonify({"data": movies}), 200)

        return resp
    except Error as e:
        return make_response(jsonify({"error": e}), 500)


@movies.post("/addmovie")
@jwt_required()
def Add_movie():
    name = request.json.get("name")
    director = request.json.get("director")
    genre = request.json.get("genre")
    imdb_score = request.json.get("imdb_score")
    popularity = request.json.get("popularity")
    if name is None:
        return make_response(jsonify({"error": "Name cannot be Empty"}), 400)
    if imdb_score > 10:
        return make_response(jsonify({"error": "IMDB_score must not exceed 10."}), 403)
    try:
        db_cursor.execute("Select name from movies where name = %s", (name,))
        result_email = db_cursor.fetchall()

        if len(result_email):
            return jsonify({"error": "Movie already exist."}), 409

        q = "INSERT INTO movies(name,director,genre,imdb_score,popularity) VALUES (%s,%s,%s,%s,%s)"
        db_cursor.execute(
            q,
            (
                name,
                director,
                genre,
                imdb_score,
                popularity,
            ),
        )
        dbConnect.commit()

        return make_response(
            jsonify({"status": "Movie added Successfully", "name": name}), 201
        )
    except Error as e:
        return make_response(jsonify({"error": "Server Error", "e": e}), 500)


@movies.put("/update/<id>")
@jwt_required()
def Update_movie(id):
    name = request.json.get("name")
    director = request.json.get("director")
    genre = request.json.get("genre")
    imdb_score = request.json.get("imdb_score")
    popularity = request.json.get("popularity")

    if name is None:
        return make_response(jsonify({"error": "Name cannot be Empty"}), 400)
    if imdb_score > 10:
        return make_response(jsonify({"error": "IMDB_score must not exceed 10."}), 403)

    try:
        db_cursor.execute(
            "Select name from movies where id != %s and name = %s", (id, name)
        )
        result_movie = db_cursor.fetchall()
        # print(result_movie)
        if len(result_movie):
            return jsonify({"error": "Movie already exist with this name."}), 409

        q = "UPDATE movies SET director = %s,genre = %s, imdb_score = %s,name = %s, popularity = %s WHERE id = %s"
        db_cursor.execute(q, (director, genre, imdb_score, name, popularity, id))
        dbConnect.commit()

        return make_response(
            jsonify(
                {
                    "status": "Movie Updated Successfully",
                    "name": name,
                    "director": director,
                    "genre": genre,
                    "imdb_score": imdb_score,
                    "popularity": popularity,
                    "id": id,
                }
            ),
            201,
        )
    except Error as e:
        return make_response(jsonify({"error": "Server Error"}), 500)


@movies.delete("/delete/<int:id>")
@jwt_required()
def Delete_movie(id):
    try:
        db_cursor.execute("Select name from movies where id = %s", (id,))
        result_movie = db_cursor.fetchall()
        # print(result_movie)
        if not len(result_movie):
            return jsonify({"error": f"Movie does not Exist with id = {id}."}), 400

        db_cursor.execute("DELETE FROM movies WHERE id = %s", (id,))
        dbConnect.commit()
        return make_response(
            jsonify(
                {
                    "status": "Movie Deleted Successfully",
                    "movie-id": id,
                    "movie-name": result_movie[0][0],
                }
            )
        )
    except Error:
        return make_response(jsonify({"error": "Server Error", "e": Error}), 500)
