<h1 align="center"> Coffee Shop App Documentation </h1>

===============================================================================
- <span style='color:brown;'>Contributor:</span> **Adedoyin Simeon Adeyemi** <br />
- <span style='color:brown;'>Version:</span> **v1.0**

===============================================================================


# Coffee Shop App
A simple APP built around Flask (backend) and Ionic/Angular (frontend) for allowing Udacity students to access a digitally enabled cafe to order drinks, socialize, and study hard. The app helps students setup their menu experience.

## The Backend
A simple API built around the REST principles for accessing and providing services for performing CRUD operations on "drinks" resource. The api uses the standard HTTP request codes and provides responses, as well as, errors using `json` format. 

## Setting up the Backend - Coffee Shop App

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is highly recommeded you setup a virtual environment where you can install your dependencies, specific to the project. To setup a virtual environment, visit [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Set up the Database

This project uses the `SQLite DBMS`. 

The database used is named "database.db" stored (to be stored) in `./backend/src/database` directory.

Running the app the first time, creates the database if not already existing and, stores a single instance of a drink (stores one dring record) in the `database.db`.


### Run the Server

From within the `./backend/src` directory first ensure you are working using your created virtual environment.

To run the server, execute the following commands:

On Mac
```bash
export FLASK_APP=api.py
export FLASK_DEBUG=true
flask run
```

On Windows:
```bash
set FLASK_APP=api.py
set FLASK_DEBUG=true
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.



## THE API ENDPOINTS
This api provides access to a single resource `drinks`. 

-----
### Base URL
- `http://127.0.0.1:5000` 
 *OR*
- `http://localhost:5000`
-----

### Endpoints
-----
#### Resource: `drinks`
-----

1. **`GET /drinks`**
-----
Fetches a list of drinks in json format.
- *Request Arguments:* None
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `drinks`, holding list of the fetched drinks
- *HTTP Response Status Codes:* 
    - `200`, 'ok', 'successful fetch'
    - `422`, 'unprocessable', required `title` and `recipe` body properties yet.
    - `401`, 'unauthorized', authentication token invalid or problem authenticating user.
    - `403`, 'forbidden', user does not have the permission to access the resource or perform the operation requested.

Example:
```bash
curl -X GET http://localhost:5000/drinks
```

Sample Response
```json
{
    "success": true,
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "brown",
                    "name": "coffee",
                    "parts": 2
                }
            ],
            "title": "coffee"
        },
    ],
}
```

-----
2. **`POST /drinks`**
-----
Saves a new drink in the request body, in json format, to the database.
- *Request Arguments:* None
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the post request, and `drinks` a list holding a single json object containing the details of the newly created drink.
- *Sample Request Body:*
```json
{   
    "title": "coffee",
    "recipe": [
        {
            "color": "brown",
            "name": "coffee",
            "parts": 2
        }
    ]
}
```

- *HTTP Response Status Codes:* 
    - `201`, 'created', created successfully
    - `409`, 'conflict', 'cannot create an already existing drink'
    - `422`, 'unprocessable', required body property `title` and `recipe` not present in request body'


Example:
```bash
curl -X POST http://localhost:5000/drinks
-H 'application/json' 
-d '{ "title": "coffee", "recipe": [{"color": "brown","name": "coffee",
    "parts": 2}]}'
```

Sample Response
```json
{
    "success": true,
    "drinks": [
        {   
            "id": 1,
            "title": "coffee",
            "recipe": [
                {
                    "color": "brown",
                    "name": "coffee",
                    "parts": 2
                }
            ]
        }
    ]
}
```


-----
4. **`PATCH /drinks/:id`**
-----
Performs partial update of record of drink with id of `id` specified in the parameter using the object specified in the request body (in json format).
- *Request Arguments:* `id`, the id of the drink to update
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `drinks` a list holding a single json object containing the details of the newly updated drink.
- *Sample Request Body:*
```json
{   
    "title": "updated_title",
    "recipe": [
        {
            "color": "new_color",
            "name": "new_name",
            "parts": 1
        }
    ]
}
```

- *HTTP Response Status Codes:* 
    - `200`, 'ok', updated successfully
    - `400`, 'bad request', body data not present.
    - `404`, 'not found', drink with the specified id not found in database.
    - `422`, 'unprocessable', required body property `title` or `recipe` not present in request body'


Example:
```bash
curl -X PATCH http://localhost:5000/drinks/2
-H 'application/json' 
-d '{ "title": "updated_title", "recipe": [{"color": "new_color","name": "new_name", "parts": 2}]}'
```

Sample Response
```json
{
    "success": true,
    "drinks": [
        {   
            "id": 2,
            "title": "new_title",
            "recipe": [
                {
                    "color": "new_color",
                    "name": "new_name",
                    "parts": 2
                }
            ]
        }
    ]
}
```


-----
5. **`DELETE /drinks/:id`**
-----
Deletes record of a drink with the id of `id`.
- *Request Arguments:* `id`, the id of the drink to delete
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `delete`, holding the id of the deleted drink.
- *HTTP Response Codes:* 
    - `200`, 'ok', deleted successfully
    - `404`, 'not found', category with the specified id not found in database.

Example:
```bash
curl -X DELETE http://localhost:5000/drinks/2
```

Sample Response
```json
{
    "success": true,
    "delete": 2
}
```


## Setting up the Frontend - Coffee Shop APP
The frontend code was written using Ionic/Angular. 

### Install Dependencies
1. **Nodejs**: Make sure that you already have `Nodejs` installed, from their official website
2. **NPM**: Also, make sure `npm`, Node Packege Manager, is also installed. This comes with latest versions of Nodejs installation.
3. **Ionic**: Also, make sure `ionic`, is also installed. To install, visit [Ionic Documentation] (https://ionicframework.com/docs/intro/cli).

To test whether you already have `Nodejs`, `npm` and `Ionic` installed, Open command prompt (for Windows users) or Terminal (For Mac users) and run the commands shown below, if the versions are shown, then you already have them installed.

```bash
node --version
npm --version
ionic --version
```

3. **Project Dependencies**: Once `Nodejs`, `npm` and `Ionic` are confirmed installed, to install the frontend project dependencies, from within the `./frontend` directory of this project, execute the following commands:

```bash
npm install
```

*NOTE:*
- To resolve the dependency issue due to deprecated `node-sass` package, install `sass` as a development dependency package for compiling the `.scss` files into reqular css files by executing the command below:

```bash
npm install --save-dev sass
```

### Run the Local Ionic Server

*NOTE:*
`Before starting the frontend server, ensure the backend server is live.`

To start the local Ionic/Angular frontend Server, from within the `./frontend` directory, execute the following commands:

```bash
ionic serve
```