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

    director = request.args.get("director")
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


@movies.get("/<int:id>")
def GetMoviebyID(id):
    try:
        db_cursor.execute("Select * from movies where id = %s", (id,))
        rows = db_cursor.fetchall()
        column_names = [desc[0] for desc in db_cursor.description]
        movies = [dict(zip(column_names, row)) for row in rows]
        if not len(movies):
            return jsonify({"error": f"Movie does not Exist with id = {id}."}), 404

        resp = make_response(jsonify({"data": movies[0]}), 200)

        return resp
    except Error as e:
        return make_response(jsonify({"error": str(e)}), 500)


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
    if imdb_score > 10 or imdb_score < 0:
        return make_response(
            jsonify({"error": "IMDB_score should be between 0 to 10."}), 403
        )
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
        movie_id = db_cursor.lastrowid
        gen_list = [str(gen) for gen in genre.split(",")]
        genre_values = [
            (
                movie_id,
                g,
            )
            for g in gen_list
        ]
        genre_query = "INSERT INTO genres (movie_id, genre) VALUES (%s, %s)"
        db_cursor.executemany(genre_query, genre_values)
        dbConnect.commit()
        return make_response(
            jsonify(
                {
                    "status": "Movie added Successfully",
                    "details": {"name": name, "id": movie_id},
                }
            ),
            201,
        )
    except Error as e:
        return make_response(jsonify({"error": "Server Error", "e": str(e)}), 500)


@movies.put("/update/<id>")
@jwt_required()
def Update_movie(id):
    name = request.json.get("name")
    director = request.json.get("director")
    genre = request.json.get("genre")
    imdb_score = request.json.get("imdb_score")
    popularity = request.json.get("popularity")

    if name is None:
        return make_response(jsonify({"error": "Movie name cannot be Empty"}), 400)
    if imdb_score > 10 or imdb_score < 0:
        return make_response(
            jsonify({"error": "IMDB_score should be between 0 to 10."}), 403
        )

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

        db_cursor.execute("DELETE FROM genres WHERE movie_id = %s", (id,))

        gen_list = [str(gen) for gen in genre.split(",")]
        genre_values = [
            (
                id,
                g,
            )
            for g in gen_list
        ]
        genre_query = "INSERT INTO genres (movie_id, genre) VALUES (%s, %s)"
        db_cursor.executemany(genre_query, genre_values)
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
        return make_response(jsonify({"error": "Server Error", "e": str(e)}), 500)


@movies.delete("/delete/<int:id>")
@jwt_required()
def Delete_movie(id):
    try:
        db_cursor.execute("Select name from movies where id = %s", (id,))
        result_movie = db_cursor.fetchall()
        print(result_movie)
        if not len(result_movie):
            return jsonify({"error": f"Movie does not Exist with id = {id}."}), 400

        db_cursor.execute(
            "DELETE FROM movies WHERE id = %s",
            (id,),
        )
        # db_cursor.execute("DELETE FROM genres WHERE movie_id = %s", (id,))
        # added cascading with fkeys
        dbConnect.commit()
        print("Here")
        return make_response(
            jsonify(
                {
                    "status": "Movie Deleted Successfully",
                    "movie-id": id,
                }
            ),
            200,
        )
    except Error as e:
        return make_response(jsonify({"error": "Server Error", "e": str(e)}), 500)
