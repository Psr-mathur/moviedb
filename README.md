# Moviedb

This is the documentation for the Moviedb API.

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Base URL
`http://localhost:4000`  || `https://moviedbserver-feey.onrender.com`

## Authentication
This API uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, you need to include a valid JWT token in the `Authorization` header of your requests.

### Obtaining a JWT Token
- To obtain a JWT token, send a `POST` request to the `/login` endpoint with valid credentials. Upon successful authentication, the server will respond with a JWT token.

  - **Endpoint:** `POST /api/auth/register`
    - **Request Body:**
      - **email** (string, required) - Your email.
      - **username** (string, required) - Your username.
      - **password** (string, required) - Your password.
    - **Response:**
      - **201:** Registration successful.
        - **Example:**
        ```json
        {
          "email":"test@google.com",
          "username":"Tester",
          "password":"testinger"
        }
        ```
      - **400 Bad Request:** Email cannot be empty , Password Cannot be empty , Username cannot be empty.
      - **409 Conflict:** email already in use, username already in use..


  - **Endpoint:** `POST /api/auth/login`
    - **Request Body:**
      - **username** (string, required) - Your username.
      - **password** (string, required) - Your password.
    - **Response:**
      - **200 OK:** Authentication successful. Token provided.
        - **Data Example:**
        ```json
        {
          "access_token": "your-access-token",
          "refresh_token":"your-refresh-token",
          "Time":"Current Date and Time",
        }
        ```
      - **401 Unauthorized:** Authentication failed. Invalid credentials.

  - **Endpoint:** `POST /api/auth/refresh`
    - **Description:** Get a new Access Token.
    - **Request Header:**
      - **Authorization**: `Bearer {refresh_token}`,
    - **Response:**
      - **200 OK:** Authentication successful. Token provided.
        - **Data Example:**
        ```json
        {
          "access_token": "your-access-token",
        }
        ```
      - **401 Unauthorized:** Authentication failed. Invalid credentials.

## Endpoints

### GET /api/movies
- **Description:** Retrieve all movie details.
- **Response:**
   - **200 OK:** Movie details retrieved successfully.
     - **Data Example:**
     ```json
     {
      "data":[
        {
          "director": "Victor Fleming",
          "genre": "Adventure, Family, Fantasy, Musical",
          "id": 1,
          "imdb_score": 8.3,
          "name": "The Wizard of Oz",
          "popularity": 83
        },
        .....
      ]
     }
     ```
   - **500:** Server Error.
   
### GET /api/movies?genre={movie_genre}
- **Description:** Retrieve all movie details with their genre.
- **Parameters:**
   - `{genre}` (string, required) - genre of the movie.
- **Response:**
   - **200 OK:** Movie details retrieved successfully.
     - **Data Example:** movie_genre = `Action`
     ```json
     {
      "data":[
        {
            "director": "George Lucas",
            "genre": "Action, Adventure, Fantasy, Sci-Fi",
            "id": 2,
            "imdb_score": 8.8,
            "name": "Star Wars",
            "popularity": 88
        },
        .....
      ]
     }
     ```
   - **500:** Server Error.
   
### GET /api/movies?rating={movie_imdb_score}
- **Description:** Retrieve all movie details whose imdb_score is >= `{movie_imdb_score}`.
- **Parameters:**
   - `{movie_imdb_score}` (double, required) - imdb_score of the movie. (Must be between 0 to 10.)
- **Response:**
   - **200 OK:** Movie details retrieved successfully.
     - **Data Example:** movie_imdb_score = `9.1`
     ```json
     {
      "data": [
        {
            "director": "Francis Ford Coppola",
            "genre": "Crime, Drama",
            "id": 11,
            "imdb_score": 9.2,
            "name": "The Godfather",
            "popularity": 92
        },
        {
            "director": "John Brahm",
            "genre": "Drama, Fantasy, Mystery, Sci-Fi, Thriller",
            "id": 51,
            "imdb_score": 9.5,
            "name": "The Twilight Zone",
            "popularity": 95
        }
      ]
     }
     ```
   - **500:** Server Error.
   
### GET /api/movies?director={movie_director}
- **Description:** Retrieve movies by thier director.
- **Parameters:**
   - `{movie_director}` (string, required) - director of the movie.
- **Response:**
   - **200 OK:** Movie details retrieved successfully.
     - **Data Example:** movie_director = `John Ford`
     ```json
     {
      "data":[
        {
            "director": "John Ford",
            "genre": "Adventure, Drama, Western",
            "id": 19,
            "imdb_score": 8.1,
            "name": "The Searchers",
            "popularity": 81
        },
        {
            "director": "John Ford",
            "genre": "Adventure, War",
            "id": 67,
            "imdb_score": 7.0,
            "name": "The Lost Patrol",
            "popularity": 70
        },
        .....
      ]
     }
     ```
   - **500:** Server Error.
   
### GET /api/movies/{movie_id}
- **Description:** Retrieve movie details by ID.
- **Parameters:**
   - `{movie_id}` (int, required) - The ID of the movie to retrieve.
- **Response:**
   - **200 OK:** Movie details retrieved successfully.
     - **Data Example:** movie_id = `1`
     ```json
     {
        "director": "Victor Fleming",
        "genre": "Adventure, Family, Fantasy, Musical",
        "id": 1,
        "imdb_score": 8.3,
        "name": "The Wizard of Oz",
        "popularity": 83
     }
     ```
   - **404 Not Found:** Movie not found.

### PUT /api/movies/update/{movie_id}
- **Description:** Update movie details by ID.
- **Parameters:**
   - `{movie_id}` (int, required) - The ID of the movie to update.
- **Request Body:**
   - **name** (string, required) - The new title or name of the movie.
   - **director** (string) - The  director of the movie.
   - **genre** (string) - The genre of the movie. (if there are more than one genre put a comma between them.)
   - **imdb_score** (string) - The imdb_score of the movie.
   - **popularity** (string) - The popularity of the movie.
- **Request Header:**
    - **Authorization**: `Bearer {access_token}`,
- **Response:**
   - **200 OK:** Movie updated successfully.
   - **400:** Movie name cannot be Empty.
   - **403:** IMDB_score should be between 0 to 10.
   - **409:** Movie already exist with this name. (If your new `name` of the movie already present in the database.)
   - **500:** Server Error.

### POST /api/movies/addmovie
- **Description:** Add a new movie.
- **Request Body:**
   - **name** (string, required) - The new title or name of the movie.
   - **director** (string) - The  director of the movie.
   - **genre** (string) - The genre of the movie. (if there are more than one genre put a comma between them.)
   - **imdb_score** (string) - The imdb_score of the movie.
   - **popularity** (string) - The popularity of the movie.
     - **Body Example:**
      ```json
      {
        "director": "Testing",
        "genre": "Adventure, Family, Fantasy",
        "imdb_score": 9.9,
        "name": "Test Wizard",
        "popularity": 83
      }
     ```
- **Request Header:**
    - **Authorization**: `Bearer {access_token}`,
- **Response:**
   - **201 Created:** Movie added successfully.
     - **Data Example:**
     ```json
      {
        "status": "Movie added Successfully",
        "id":"XX"
        "director": "Testing",
        "genre": "Adventure, Family, Fantasy",
        "imdb_score": 9.9,
        "name": "Test Wizard",
        "popularity": 83
      }
     ```
   - **400:** Movie name cannot be Empty.
   - **403:** IMDB_score should be between 0 to 10.
   - **409:** Movie already exist with this name. (If `name` of the movie already present in the database.)
   - **500:** Server Error.

### DELETE api/movies/delete/{movie_id}
- **Description:** Delete a movie by ID.
- **Parameters:**
   - `{movie_id}` (int, required) - The ID of the movie to delete.
- **Request Header:**
    - **Authorization**: `Bearer {access_token}`,
- **Response:**
   - **204 No Content:** Movie deleted successfully.
      ```json
      {
        "status": "Movie Deleted Successfully",
        "movie-id": "XX",
        "movie-name": "XXXXXXX",
      }
      ```
   - **404 Not Found:** Movie does not Exist with id = {`movie_id`}


## Example Requests

**POSTMAN** (*localhost*) : 
https://elements.getpostman.com/redirect?entityId=28087430-fdb9b748-dd50-4bc8-be42-81325683ef7e&entityType=collection

**POSTMAN** (*server*) : Will be Available soon.

### Scalability (*Beyondcc.club*):
- https://writeurl.com/3jrBlhYgnTJOcRuF