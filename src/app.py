from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from routes import auth, movies

app = Flask(__name__)

app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_callback(error_string):
    return jsonify({"message": "Not LoggedIn"}), 401


@app.route("/")
def Home():
    return jsonify("Namaste! This API is developed by Prakash.")


app.register_blueprint(auth)
app.register_blueprint(movies)


@app.post("/show")
@jwt_required()
def Show():
    return jsonify({"msg": "Showing"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
