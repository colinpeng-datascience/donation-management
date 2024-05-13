# Donation Management System API

This repository contains the backend API for a Donation Management System, providing endpoints to manage staff, donations, types of donations, and generate reports based on donation subtypes and donor activity.

## Features

- Staff registration/authentication and session management
- Create custom donation types and subtypes
- Registration and management of donors
- Recording and tracking of donations and distributions
- Report generation by type, donor, and subtype

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Installing

To get a local copy up and running follow these steps:

1. Clone the repository:
```sh
git clone https://github.com/colinpeng-datascience/donation-management.git
```
2. Navigate to the project directory:
```sh
cd donation-management
```
3. Install the project (editable mode recommended for development):
```sh
pip install -e .
```

4. Set the Flask app environment variable:
```sh
export FLASK_APP=donman
```

5. Initialize the database:
```sh
flask db init
```

6. Run the initial migration:
```sh
flask db migrate -m "Initial migration"
```

7. Create the `var` directory and touch the 
SQLite3 file:
```sh
mkdir var
touch var/donman.sqlite3
```

8. Perform the migration and upgrade the database:
```sh
flask db upgrade
```
9. Initialize the database with any necessary seed data:
```sh
flask init-db
```
10. Run the Flask app with:
 ```sh
 flask --app donman --debug run --host 0.0.0.0 --port 8000
 ```

### Testing the Endpoints

A separate test script is provided to test the API endpoints. In a new terminal window, proceed to make the `rest_test.sh` script executable and run the tests using the following commands:

```sh
chmod +x rest_test.sh
./rest_test.sh
```
(Make sure httpie is installed) 

This will test all of the available API endpoints, including success and error cases. 

## API Endpoints

### Auth Endpoints

- `POST /api/staff/login`: Authenticate a staff member and establish a session. Requires staff email and password.
- `DELETE /api/staff/logout`: Terminate the current staff session.

### Staff Endpoints

- `POST /api/staff`: Registers a new staff member. Requires staff name, email, and password.
- `GET /api/staff`: Retrieves a list of all staff members.
- `DELETE /api/staff/<staff_id>`: Deletes a staff by ID, removing them from the system.

### Donation Type Endpoints

- `POST /api/type`: Registers a new donation type, specified by the type name.
- `GET /api/type`: Retrieves a list of all donation types.

### Donation Subtype Endpoints

- `GET /api/type/sub`: Retrieves all donation subtypes associated with a specific type ID, passed as a query parameter.
- `POST /api/type/sub`: Registers a new donation subtype associated with an existing donation type. Requires type ID and subtype name.

### Donor Endpoints

- `GET /api/donor`: Retrieves a list of all registered donors.
- `POST /api/donor`: Registers a new donor. Requires donor name and email.

### Donation Endpoints

- `POST /api/donation`: Registers a new donation entry linked to a donor and subtype. Requires donor ID, donation quantity, and subtype ID.

### Distribution Endpoints

- `POST /api/distribution`: Registers a new distribution entry. Requires subtype ID and the amount distributed.

### Reporting Endpoints

- `GET /api/report/type/<type_id>`: Generates a report by type ID, showing totals of donated and distributed amounts, as well as the remaining amount.
- `GET /api/report/subtype/<subtype_id>`: Generates a report for a specific subtype ID, including the total amounts donated and distributed.
- `GET /api/report/donor/<donor_id>`: Generates a report summarizing donations made by a specific donor ID, broken down by type and subtype.

## Built With

- [Flask](http://flask.pocoo.org/) - The web framework used
- [Flask-RESTful](https://flask-restful.readthedocs.io/) - Extension for Flask that adds support for quickly building REST APIs.
- [Flask-SQLAlchemy](https://www.sqlalchemy.org/) - ORM and database management
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Database schema migrations
- [HTTPie](https://httpie.io/) - Command-line HTTP client

## Authors

**Colin Peng** [colinpeng-datascience](https://github.com/colinpeng-datascience)

## License

This project is licensed under the MIT License

## Acknowledgments
Special thanks to:
- [REST api tutorial](https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html#rest-api) by EECS 485 team at UMich 
- [Full Stack Flask + React tutorial](https://medium.com/@sandyjtech/building-a-full-stack-app-with-flask-react-mysql-a78fcc235ff0) by Sandyjtech