from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from datetime import datetime as dt
import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)
from database import db_cursor, dbConnect

auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.post("/register")
def Register():
    body_data = request.json
    email = body_data.get("email")
    password = body_data.get("password")
    username = body_data.get("username")
    if email is None:
        return jsonify({"error": "Email cannot be empty"}), 400
    elif not validators.email(email):
        return jsonify({"error": "Invalid email"}), 400

    if password is None:
        return jsonify({"error": "Password Cannot be empty"}), 400
    elif len(password) < 6:
        return jsonify({"error": "Password is too short."}), 400

    if username is None:
        return jsonify({"error": "Username cannot be empty"}), 400
    elif len(username) < 3:
        return jsonify({"error": "Username is too short."}), 400
    elif not username.isalnum() or " " in username:
        return (
            jsonify({"error": "Username should be alphanumeric, also no spaces."}),
            400,
        )

    db_cursor.execute("Select email from users where email = %s", (email,))
    result_email = db_cursor.fetchall()

    if len(result_email):
        return jsonify({"error": "email already in use."}), 409

    db_cursor.execute("Select username from users where username = %s", (username,))
    result_username = db_cursor.fetchall()

    if len(result_username):
        return jsonify({"error": "Username already in use."}), 409

    pwd_hash = generate_password_hash(password)

    db_cursor.execute(
        "INSERT INTO users (email, username, password) VALUES (%s ,%s,%s)",
        (email, username, pwd_hash),
    )
    dbConnect.commit()

    return jsonify({"status": "Registeration Successfull", "username": username}), 201


@auth.post("/login")
def Login():
    body_data = request.json
    password = body_data.get("password")
    username = body_data.get("username")

    db_cursor.execute("Select password from users where username = %s", (username,))
    result_username = db_cursor.fetchall()

    if len(result_username) == 0:
        return jsonify({"error": "User not Found"}), 404
    str_password = result_username[0][0]
    if not check_password_hash(str_password, password):
        return jsonify({"error": "Incorrect Password"}), 501

    refresh = create_refresh_token(identity=username)
    access = create_access_token(
        identity=username, expires_delta=datetime.timedelta(minutes=60)
    )

    content = jsonify(
        {
            "status": "Login Successful",
            "Time": dt.now(),
            "access_token": access,
            "refresh_token": refresh,
        }
    )
    resp = make_response(content, 200)

    return resp


@auth.post("logout")
def Logout():
    resp = make_response(jsonify("Logout successful"), 200)
    unset_jwt_cookies(resp)
    return resp


@auth.post("/refresh")
@jwt_required(refresh=True)  # Requires a valid refresh token
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return {"access_token": new_access_token}
