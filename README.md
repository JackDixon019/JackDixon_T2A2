# T2A2 - API Webserver Project

## Links - 
#### [Github Repository](https://github.com/JackDixon019/JackDixon_T2A2)

#### [Trello Board](https://trello.com/invite/b/dKlcYBQh/ATTIadd08f5f7b90e8a717572101ac6a867b5130947C/jackdixont2a2)

## Installation and Setup - 

<u>Requirements - </u>

- [Python 3](https://www.python.org/downloads/)

- [PostgreSQL](https://www.postgresql.org/download/)

- [Project's Github Repo](https://github.com/JackDixon019/JackDixon_T2A2)

<u>Initial Setup - </u>

When first setting up this app, you must use PSQL to create the database that will be used, as well as a user which can manage the database. The specifics will vary by the user, however the information must be included under the `DATABASE_URL` of the `.env` file. This file is not included, but an example can be found in the `.env.sample` file included in this repo.

After the database as been established, a virtual environment should be created, and the addons and libraries specified in the `requirements.txt` file should be installed using `$ pip3 install -r requirements.txt`

To initialise the database's tables, in a CLI, enter the following commands:
`$ flask db create`
`$ flask db seed`
The tables can be dropped with the command:
`$ flask db yeet`

The database can also be reset by entering the command:
`$ flask db reset`
Which will drop all tables, then re-create and re-seed them.

After creating and seeding the tables, the app is ready to be launched. This can be done by the CLI command:
`$ flask run`

At this point, the app will run on localhost:8080, where it can be accessed either directly via url, or via an API Platform such as Postman.


## Endpoints - 

###### NB: All endpoints are preceded by "localhost:8080" 
e.g. `localhost:8080/auth/register`
###### NB: All required data is to be in JSON format

#### Auth controller - 
###### NB: All auth controller endpoints are preceded by "/auth"

**`/register`**
###### HTTP request verb - 
POST
###### Required data - 
- username: Minimum length of 2 characters. Can only contain letters and numbers.
- email: Must be unique and in a valid email format (example@domain.com)
- password: Minimum length of 6 characters. Password is hashed by bcrypt
- location_id: Must be included, must be an integer.

e.g. - 
```
{
    "username":"user1",
    "email":"user@email.com",
    "password":"password",
    "location_id":1
}
```

###### Expected response data - 
The response data should include the user's id, their username, whether they are an admin, their email, their location id, and location name

e.g. - 
```
{
    "id": 5,
    "username": "user1",
    "is_admin": false,
    "email": "user@email.com",
    "location_id": 1,
    "location": {
        "name": "Melbourne"
    }
}
```
**`/login`**
###### HTTP request verb - 
POST
###### Required data - 
- email: Must match the email of a user in the database
- password: Must match the password of the user whose email was provided
###### Expected response data - 
The user's email, their access token, and whether they are an admin or not
e.g.
```
{
    "email": "user1@email.com",
    "token": "token_goes_here",
    "is_admin": false
}
```


**`/<int:id>`**
###### HTTP request verb - 
DELETE
###### Required data - 
None in the body. Only the id of the user to be deleted in the URL.
###### Expected response data - 
A message in JSON format saying that the user has been deleted
###### Authentication methods where applicable - 
This action can only be performed by either a user where `is_admin == True` or by the user being deleted themselves. 


**`/location/<int:id>`**
###### HTTP request verb - 
PUT
###### Required data - 
None in the body. Only the id of the location desired to be included in the URL
###### Expected response data - 
The user's email, their access token, and whether they are an admin or not
e.g.
```
{
    "id": 1,
    "username": "user1",
    "is_admin": false,
    "email": "user1@email.com",
    "location_id": 1,
    "location": {
        "name": "Melbourne"
    }
}
```
###### Authentication methods where applicable - 
The user must be logged in with a JWT token accessible to change their location



#### Bird controller - 
###### NB: All bird controller endpoints are preceded by "/birds"

**`/`**
###### HTTP request verb - 
POST
###### Required data - 
- name: String containing the name of the bird. Minimum length of 2 characters
- description: String describing the bird. Minimum length of 2 characters

###### Expected response data - 
The bird's id, name, description, whether it is approved or not, and the submitting user's id.
e.g.
```
{
    "id": 8,
    "name": "Galah",
    "description": "Gooby",
    "is_approved": false,
    "submitting_user_id": 1
}
```

###### Authentication methods where applicable - 
User must be logged in to submit a bird


**`/<int:id>`**
###### HTTP request verb - 
DELETE
###### Required data - 
None in the body, only the id of the bird to be included in the URL
###### Expected response data - 
JSON format message informing that that bird has been deleted successfully
###### Authentication methods where applicable - 
User must be logged in to delete a bird. Only either an admin or the user who created the bird may delete it.


**`/<int:id>`**
###### HTTP request verb - 
PUT or PATCH
###### Required data - 
None technically required, but can include the name and/or description of the bird
###### Expected response data - 
The bird's id, name, description, whether it is approved or not, and the submitting user's id.
e.g.
```
{
    "id": 8,
    "name": "Galah",
    "description": "Gooby",
    "is_approved": false,
    "submitting_user_id": 1
}
```
###### Authentication methods where applicable - 
User must be logged in to update a bird's details


**`/<int:id>/approve`**
###### HTTP request verb - 
PUT or PATCH
###### Required data - 
None in the body, only the bird's id included in the URL
###### Expected response data - 
The bird's id, name, description, whether it is approved or not, and the submitting user's id.
e.g.
```
{
    "id": 8,
    "name": "Galah",
    "description": "Gooby",
    "is_approved": false,
    "submitting_user_id": 1
}
```
###### Authentication methods where applicable - 
Only an admin may approve a bird



#### Location controller - 
###### NB: All location controller endpoints are preceded by "/locations"
**`/`**
###### HTTP request verb - 
POST
###### Required data - 
- name: the name of the location must be included. Minimum length of 2 characters
###### Expected response data - 
The id, and name of the location
e.g.
```
{
    "id": 7,
    "name": "Birdsville"
}
```
###### Authentication methods where applicable - 
User must be logged in to post a location

**`/<int:id>`**
###### HTTP request verb - 
DELETE
###### Required data - 
None in the body, just the id of the location as given in the URL
###### Expected response data - 
JSON format message informing that that location has been deleted successfully
###### Authentication methods where applicable - 
User must be an admin to delete the location

#### Session controller - 
###### NB: All session controller endpoints are preceded by "/sessions"

**`/`**
###### HTTP request verb - 
POST
###### Required data - 
- date: Must be given in appropriate date format aka MM/DD/YYYY or YYYY-MM-DD. If none is provided, the current date is used instead
- location_id: The id of a location in the database. If non is provided, the user's current location will be used instead.
###### Expected response data - 
The session's id, date, user_id, location_id, and session_counts will be returned. 
e.g.
```
{
    "id": 5,
    "date": "2023-07-30",
    "user_id": 1,
    "location_id": 3,
    "session_counts": []
}
```

###### Authentication methods where applicable - 
User must be logged in to create a session


**`/<int:id>`**
###### HTTP request verb - 
DELETE
###### Required data - 
None in the body, only the session id provided in the URL
###### Expected response data - 
JSON format message informing that that bird has been deleted successfully

###### Authentication methods where applicable - 
Only an admin or the original creator of a session can delete it


**`/<int:id>`**
###### HTTP request verb - 
PUT or PATCH
###### Required data - 
- date: Must be given in appropriate date format aka MM/DD/YYYY or YYYY-MM-DD. If none is provided, the existing date is maintained
- location_id: The id of a location in the database. If non is provided, the existing location_id is used instead

###### Expected response data - 
The session's id, date, user_id, location_id, and session_counts will be returned. 
e.g.
```
{
    "id": 5,
    "date": "2023-07-30",
    "user_id": 1,
    "location_id": 3,
    "session_counts": []
}
```

###### Authentication methods where applicable - 
Only the creator of a session, or an admin may edit a session's details.



#### Session Count controller - 
###### NB: All session count controller endpoints are preceded by "/sessions/\<int:session_id>/count"

**`/`**
###### HTTP request verb - 
POST
###### Required data - 
- bird_id: Integer value that aligns with bird's id
- count: Integer value 
- session: Not required in body, provided as session_id in the URL

###### Expected response data - 
Session data, including session counts.
e.g.
```
{
    "id": 4,
    "date": "2023-07-23",
    "user_id": 2,
    "location_id": 1,
    "session_counts": [
        {
            "bird_id": 6,
            "count": 5
        },
        {
            "bird_id": 7,
            "count": 14
        },
        {
            "bird_id": 2,
            "count": 50
        }
    ]
}
```

###### Authentication methods where applicable - 
Only the user who created the session can post session counts to it.


**`/<int:id>`**
###### HTTP request verb - 
PUT or PATCH
###### Required data - 
- bird_id: Integer value that aligns with bird's id. If none provided, will use existing value
- count: Integer value. If none provided, will use existing value
- session_id and session_count_id: Not required in body, provided as session_id and id respectively in the URL

###### Expected response data - 
Session data, including session counts. As above
###### Authentication methods where applicable - 
Only user who created the session or an admin may edit the session counts. 



#### Search controller - 
###### NB: All search controller endpoints are preceded by "/search"
###### All search controller endpoints use the HTTP request verb - 
GET
###### All search controller endpoints require no data in the body - 
Necessary id's are provided in the URL


**`/users/<int:id>`**
###### Expected response data - 
User details including: id, username, is_admin, email, location_id, location name, submitted birds (and their details), user's sessions (and their counts), and, if the user is an admin, a list of birds they have approved


###### Authentication methods where applicable - 
User must be logged in to search for user details.


**`/birds`**

###### Expected response data - 
A list of all birds and their details.


**`/birds/<int:id>`**

###### Expected response data - 
The details of the bird whose id is provided


**`/birds_by_user/<int:user_id>`**

###### Expected response data - 
A list of all birds, and their details, submitted by the user whose id is provided.

###### Authentication methods where applicable - 
User must be logged in

**`/birds_by_location/<int:location_id>`**

###### Expected response data - 
A list of all birds, which have been counted in a session at the given location.

**`/locations`**

###### Expected response data - 
A list of all locations and their details.


**`/locations<int:id>`**

###### Expected response data - 
The details of the location whose id has been provided


**`/locations_by_bird/<int:bird_id>`**

###### Expected response data - 
A list of all locations which a given bird has been counted at


**`/sessions`**

###### Expected response data - 
A list of all sessions and their details.


**`/sessions/<int:id>`**

###### Expected response data - 
The details of the session whose id has been provided


**`/sessions/<int:session_id>/counts`**

###### Expected response data - 
A list of all session counts associated with the session whose id has been provided

