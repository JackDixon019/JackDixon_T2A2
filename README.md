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
e.g. `localhost:8080/register`
###### NB: All required data is to be in JSON format

#### Auth controller - 
**`/register`**
###### HTTP request verb - 
POST
###### Required data - 
- username: Minimum length of 2 characters. Can only contain letters and numbers.
- email: Must be in a valid email format (example@domain.com)
- password: Minimum length of 6 characters. Password is stored as a hash by bcrypt

###### Expected response data - 

###### Authentication methods where applicable - 


API endpoints must be documented in your readme
Endpoint documentation should include
    HTTP request verb
    Required data where applicable 
    Expected response data 
    Authentication methods where applicable


