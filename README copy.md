### Identification of the problem you are trying to solve by building this particular app.
This app is designed to facilitate tracking of birds when birdwatching. It allows for birdwatchers to collaborate in building a library of birds, while also allowing for people to also record their own personal birdwatching records. 

### Why is it a problem that needs solving?
It's much more convenient to have the ability to track and record information from a phone than in a paper records like a book. It also allows for much easier collaboration. Having access to a community's resources also allows for novices to identify birds with greater ease.

### Why have you chosen this database system. What are the drawbacks compared to others?
I have chosen PostgreSQL. I have chosen it because I am more familiar with it than other DBMS's, it is used to manage relational databases which I am building, and it is compatible with ORMs which I am also using. for these reasons, PostgreSQL is a suitable database for my project.

PostgreSQL does have some drawbacks when compared to competitors such as MySQL. Such as less support, more difficult setup, and slower performance. The consequences of these disadvantages, however, will be extremely minimal for a project the scale of this one, and the advantage of my familiarity with the system will be a much greater advantage by comparison.

### Identify and discuss the key functionalities and benefits of an ORM
An ORM allows for the ability to create and control relations between tables in a database by treating them as objects in an object-oriented language. 

This allows for much more intuitive control of data structures and dataflow for a developer who is used to object-oriented languages. It also allows for the ability to manipulate a SQL database without having to write in SQL, making development easier since only one language needs to be used for most processes. 

They facilitate DRY principles of programming by abbreviating extended SQL queries into much shorter and simpler to understand functions which can be used flexibly with variable inputs. 

ORMs can also be used in conjunction with data serialisers and deserialisers to validate data and protect data integrity. 

### Document all endpoints for your API
Endpoints are documented at the end. [Here](#endpoints)

### An ERD for your app
![ERD](./docs/ERD.png)

### Detail any third party services that your app will use
- <b>Flask</b>
Flask is a lightweight and flexible web framework built for Python. Flask depends on the Werkzeug WSGI toolkit to process HTTP requests and responses, the Jinja template engine for rendering of webpages, and the Click CLI toolkit for CLI interactions. 
Flask is a simple and highly "pythonic" framework that makes it ideal for beginner developers such as myself. Its flexibility allows it to manage a wide variety of potential tasks. 
- <b>Psycopg2</b>
Psycopg2 is a database adaptor to allow Python-based apps to directly control PostgreSQL databases. It is designed for multi-threaded apps which allows it to perform many actions simultaneously within the database. It can adapt the majority of Python datatypes to their SQL equivalents, and features the ability to adapt more through the creation of custom datatypes.

- <b>SQLAlchemy</b>
SQLAlchemy is used in this project primarily as an ORM, although the ORM is only one component of SQLAlchemy alongside the "Core": an SQL abstraction toolkit. It features function-based query construction, utilising the flexibility of functions to create intuitive and flexible SQL queries. As an ORM, it is also very useful for constructing tables.
SQLAlchemy is also "non-opinionated", meaning that it doesn't create any schemas of its own, allowing it to be used with any appropriate serialiser.
SQLAlchemy is used in this app to create and manipulate tables within the database.

- <b>Marshmallow</b>
Marshmallow is a serialiser. It converts complex datatypes, such as objects, into basic Python datatypes and vice-versa through the use of Schemas. Marshmallow is used in this app to convert data from JSON to python objects which are defined by SQLAlchemy, and back again, as well as to validate the data each contains. 

- <b>Bcrypt</b>
Bcrypt is a library used to hash, salt, and secure data into an unreadable string. It is designed to perform (relatively) slowly, to reduce the ability to brute-force decryption. 
In this app, it is used to securely store user passwords

- <b>JSON Web Token</b>
JSON Web Tokens (JWTs) are a compact and secure way of transmitting information as a JSON object. JWTs verify the integrity of the data contained within them. They are comprised of the Header, containing the datatype and the signing algorithm, the Payload, containing the data being transmitted, and the signature, which is comprised of the encoded header, the encoded payload, and a "secret" which is used as a key for algorithmic hashing. In this way, the data can be protected from tampering. In this app, JWTs are used for user authorisation. 


### Describe your projects models in terms of the relationships they have with each other

#### Models
##### User - 
```python
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), default=False)

    submitted_birds = db.relationship("Bird", back_populates="submitting_user")

    approved_birds = db.relationship("ApprovedBird", back_populates="admin")

    user_sessions = db.relationship(
        "Session", back_populates="user", cascade="all, delete"
    )

    location_id = db.Column(db.Integer(), db.ForeignKey("locations.id"))
    location = db.relationship("Location", back_populates="users")
```
The user model contains information on the user. It has several relations with other models. 
- Users and Birds share a relationship, connecting the "submitted_birds" attribute and the "submitting_user" attribute, with the Birds model also having the "submitting_user_id" Foreign Key. 

- Users and Birds share a second, indirect, relationship. Users are related to the ApprovedBird model, which acts as a join table between Users and Birds. 

- Users and Sessions are also related by the "user_sessions" attribute. This relationship cascades deletions from the user-side 

- Finally, Users and Locations are related via the "location" and "users" attributes. The Users model also has the "location_id" foreign key
##### Bird - 
```py
class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)
    # relates birds and users
    submitting_user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    submitting_user = db.relationship("User", back_populates="submitted_birds")
    # relation with admin via ApprovedBird join table.
    # While I don"t think a join table is strictly necessary for a 1-to-many relationship,
    # I couldn't make two connections directly from Bird to User without issues
    approving_admin = db.relationship(
        "ApprovedBird", back_populates="bird", uselist=False, cascade="all, delete"
    )
    # relates birds with session_counts
    session_counts = db.relationship(
        "SessionCount", back_populates="bird", cascade="all, delete"
    )

```

Birds have several relationships with other tables:
- Birds and Users are related, as discussed above
- Birds and ApprovedBirds are related via the "bird" and "approving_admin" attributes. The ApprovedBirds entities cascade deletion from the bird-side. 
- Birds and Sessions are related via the SessionCounts join table, with the attributes "session_counts" and "bird". 

#### Session - 
```py
class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False, default=datetime.today().date())

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="user_sessions")

    session_counts = db.relationship(
        "SessionCount", back_populates="session", cascade="all, delete"
    )

    location_id = db.Column(db.Integer(), db.ForeignKey("locations.id"), nullable=False)
    session_location = db.relationship("Location", back_populates="sessions")

```

Sessions are related to Location, SessionCount, and User models:
- Sessions are related to users as discussed above, including the user_id Foreign Key
- Sessions are related to SessionCount via the "session_counts" and "session" attributes.
- Sessions and Locations are related via the "session_location" and "sessions" attributes, with the "location_id" Foreign Key

#### Location - 
```py
class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    sessions = db.relationship(
        "Session", back_populates="session_location", cascade="all, delete"
    )

    users = db.relationship("User", back_populates="location")

```
Locations are related to users and sessions:
- Locations and users are related via  the "users" and "locations" attributes, as discussed above
- Locations and Sessions are related via the "sessions" and "session_location" attributes as discussed above. This relation cascades deletions from the location-side

#### ApprovedBird - 
```py
class ApprovedBird(db.Model):
    __tablename__ = "approved_birds"

    admin_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    bird_id = db.Column(db.ForeignKey("birds.id"), primary_key=True)

    admin = db.relationship("User", back_populates="approved_birds")
    bird = db.relationship("Bird", back_populates="approving_admin")

    date = db.Column(db.Date(), nullable=False, default=datetime.today().date())

```
ApprovedBird model acts as a join table between users and birds

#### SessionCount - 
```py
class SessionCount(db.Model):
    __tablename__ = "session_counts"

    id = db.Column(db.Integer(), primary_key=True)
    count = db.Column(db.Integer(), nullable=False)

    session_id = db.Column(db.Integer(), db.ForeignKey("sessions.id"), nullable=False)
    session = db.relationship("Session", back_populates="session_counts")

    bird_id = db.Column(db.Integer(), db.ForeignKey("birds.id"), nullable=False)
    bird = db.relationship("Bird", back_populates="session_counts")

```
SessionCount model acts as a join table between birds and sessions.
### Discuss the database relations to be implemented in your application

- Users and birds have a \[one-and-only-one]-to-\[zero-or-many] relationship. A single user can create zero or many bird entities, but each bird must only have one submitting_user. The birds table contains the "submitting_user_id" FK to represent this.

- Users and ApprovedBirds have a \[one-and-only-one]-to-\[zero-or-many] relationship as well, since each ApprovedBird entity can only have one approving user, while each user can have zero or many approved birds.

- Users and Sessions have a \[one-and-only-one]-to-\[zero-or-many] relationship. Each user can have zero or many sessions, while each session can only have one user.

- Users and Locations are related in a \[zero-or-many]-to-\[one-and-only-one] relationship. Each User can only have one Location, while each Location can have zero or many Users



- Birds and ApprovedBirds have a \[zero-or-one]-to-\[one-and-only-one] relationship. This is because each bird can either be approved or not approved, hence zero or one relations to ApprovedBirds model, while each ApprovedBirds model can only have one and only one relation to Birds

- Birds and SessionCounts are related via a \[one-and-only-one]-to-\[zero-or-many] relationship. Each bird can be associated with many SessionCounts, while each SessionCount can only be associated with a single bird. SessionCount acts as a join table here, connecting Birds and Sessions in what is ultimately a \[zero-or-many]-to-\[zero-or-many] relationship.

- Sessions and Locations have a \[zero-or-many]-to-\[one-and-only-one] relationship. Each Session can only have one Location, while each Location can have zero or many Sessions

- Sessions and SessionCounts have a  \[one-and-only-one]-to-\[zero-or-many] relationship. Each Session can have many SessionCounts, while each SessionCount must have only one Session. 


### Describe the way tasks are allocated and tracked in your project
Tasks are allocated and tracked using the Trello project management system. You may note that some of the dates in my Trello project initially went beyond the due date of the assignment. This is because I mixed up the "Available Until: August 4th" and "Due Date: July 30" and thought I had until the 4th of August. My apologies for any discrepancies in that regard.

![Trello1](./docs/Trello1.png)
![Trello2](./docs/Trello2.png)
![Trello3](./docs/Trello3.png)
![Trello4](./docs/Trello4.png)
![Trello5](./docs/Trello5.png)
![Trello6](./docs/Trello6.png)
![Trello7](./docs/Trello7.png)
![Trello8](./docs/Trello8.png)



### Document all endpoints for your API
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

