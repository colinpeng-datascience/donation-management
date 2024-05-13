from flask import request, jsonify, session, abort, Blueprint
from donman.model import Staff
from werkzeug.security import generate_password_hash, check_password_hash
from donman.controller import db

staff_bp = Blueprint('staff', __name__)
 
@staff_bp.route('/staff', methods=['POST'])
def register_staff():
    """
    Register a new staff member.

    This endpoint will create a new staff member's account, provided their information
    including email, password, and full name. The staff member will be created by the
    already authenticated staff (indicated in session).

    Requires an authenticated staff member (indicated by 'staff_id' in session).

    Request format (JSON object):
    Content-Type: application/json
    {
        "staff_email": string,  // Staff's email address
        "staff_password": string,             // Staff's password
        "staff_name": string       // Staff's full name
    }

    Response format:
    On success (JSON object):
    {
        "message": "Staff registered successfully",
        "staff_id": new_staff.staff_id           // The newly created staff's identifier
    }
    On failure due to missing data (JSON object):
    {
        "error": "Missing required fields"
    }
    On failure due to existing staff (JSON object):
    {
        "error": "Staff with this email already exists"
    }

    Status codes:
    - 200 OK: Staff was registered successfully.
    - 400 Bad Request: Required data is missing or staff with provided email already exists.
    - 401 Unauthorized: User attempting to register staff is not authenticated.
    - 500 Internal Server Error: A server-side error occurred while registering the staff member.

    Raises:
    - HTTP 401: Raises an HTTP 401 if the user is not authenticated (no 'staff_id' in session).
    - HTTP 500: Raises an HTTP 500 if there is a server-side error during registration process.
    """
    try:
        if 'staff_id' not in session:
            abort(401, description='Unauthorized: An authenticated staff user is required.')

        data = request.json
        staff_email = data.get("staff_email")
        staff_password = data.get("staff_password")
        staff_name = data.get("staff_name")
        staff_created_by_staff_id = session['staff_id']  # Assumed to be in session if authenticated

        if not all([staff_email, staff_password, staff_name]):
            return jsonify({'error': 'Missing required fields'}), 400

        existing_staff = Staff.query.filter_by(staff_email=staff_email).first()
        if existing_staff:
            return jsonify({'error': 'Staff with this email already exists'}), 400

        hashed_password = generate_password_hash(staff_password)
        new_staff = Staff(
            staff_email=staff_email,
            staff_password_hashed=hashed_password,
            staff_name=staff_name,
            staff_created_by_staff_id=staff_created_by_staff_id
        )

        db.session.add(new_staff)
        db.session.commit()

        return jsonify({'message': 'Staff registered successfully', 'staff_id': new_staff.staff_id}), 201
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@staff_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    """
    Delete an existing staff member by their unique staff identifier.

    This endpoint soft-deletes a staff member by clearing their identifiable information.
    It requires an authenticated staff member for the operation.
    
    URL parameter:
    - staff_id (int): The identifier for the staff member to be deleted.

    Response format:
    
    Status codes:
    - 200 OK: Staff member was deleted successfully.
    - 401 Unauthorized: User attempting to delete staff is not authenticated.
    - 404 Not Found: The staff member with the provided ID was not found.
    - 500 Internal Server Error: A server-side error occurred while deleting the staff member.

    Raises:
    - HTTP 401: Raised if no authenticated staff is in session.
    - HTTP 404: Raised if the staff member with the given staff_id does not exist.
    - HTTP 500: Raised if there is a server error, such as a database connection issue or failed update.
    """
    try:
        if 'staff_id' not in session:
            abort(401, description='Unauthorized: An authenticated staff user is required.')

        staff = Staff.query.get_or_404(staff_id)
        
        # Soft-delete the staff member by clearing their information
        staff.staff_name = ""
        staff.staff_email = f"deleted_{staff.staff_id}"
        staff.staff_deleted_by_staff_id = session['staff_id']
        staff.staff_password_hashed = ""

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Staff deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@staff_bp.route('/staff/login', methods=['POST'])
def login_staff():
    """
    Authenticate a staff member and establish a session.

    This endpoint allows a staff member to log in by providing their email address
    and password. Upon successful authentication, the staff_id is stored in the session.

    Request format (JSON object):
    Content-Type: application/json
    {
        "staff_email": "staffmember@example.com",  // Staff's email address
        "staff_password": "password"              // Staff's password
    }

    Response format:
    Status codes:
    - 200 OK: Logged in successfully.
    - 400 Bad Request: Required data is missing.
    - 401 Unauthorized: Email or password is incorrect, or the staff member does not exist.

    Raises:
    - HTTP 400: Raised if either staff_email or staff_password is missing.
    - HTTP 401: Raised if the provided credentials are incorrect or the staff member does not exist.
    - HTTP 500: Raised if there is a server error, such as a database connection issue.
    """

    try:
        data = request.get_json(force=True)
        staff_email = data.get('staff_email')
        staff_password = data.get('staff_password')

        if not all([staff_email, staff_password]):
            return jsonify(message='Missing email or password'), 400

        staff = Staff.query.filter_by(staff_email=staff_email).first()
        if staff and check_password_hash(staff.staff_password_hashed, staff_password):
            session['staff_id'] = staff.staff_id
            return jsonify(message='Login successful'), 200
        else:
            return jsonify(message='Login failed'), 401
    except Exception as e:
        return jsonify(message='An unexpected error occurred', details=str(e)), 500

@staff_bp.route('/staff/login', methods=['DELETE'])
def logout_staff():
    """
    Terminate the current staff session.

    This endpoint allows a logged-in staff member to log out, ending
    their current session. The 'staff_id' is removed from the session storage.

    No request payload is required.

    Response format:
    On successful logout (JSON object):
    {
        "message": "Logged out successfully"
    }

    On failure due to no active session (JSON object):
    {
        "message": "No active session"
    }

    Status codes:
    - 200 OK: Session ended successfully.
    - 401 Unauthorized: There is no active session to end.

    Raises:
    - HTTP 401: Raised if no active session exists or if the user is not logged in.
    """
    # Attempt to terminate the session if a staff_id is present
    staff_id = session.pop('staff_id', None)

    # Determine the appropriate response based on whether a staff_id was present in the session
    if staff_id:
        return jsonify(message='Logged out successfully'), 200
    else:
        return jsonify(message='No active session'), 401

@staff_bp.route('/staff', methods=['GET'])
def get_all_staff():
    """
    Retrieve a list of all staff members.

    This endpoint returns an array of staff member objects with details like name, 
    email, and other relevant staff information.

    Response format (JSON array):
    A JSON array of staff member objects containing information for each staff.
    
    [
        {
            'id': staff_id,
            'name': staff_name,
            'email': staff_email
        }
        ...
    ]

    On error (JSON object):
    {
        "error": "Failed to retrieve staff members",
        "details": "Error message string here"
    }

    Status codes:
    - 200 OK: Successfully retrieved the list of staff members.
    - 500 Internal Server Error: A server-side error occurred while attempting to retrieve staff information.
    
    Raises:
    - HTTP 500: Raised if there is a server error such as database connection issues 
      or problems with the query execution.
    """
    try:
        if 'staff_id' not in session:
            abort(401, description='Unauthorized: An authenticated staff user is required.')
        staff_members = Staff.query.all()
        # Ensure that each Staff model instance has a method to serialize its information.
        staff_data = [staff.serialize() for staff in staff_members]
        return jsonify(staff_data), 200
    except Exception as e:
        # Catch all other unexpected errors
        return jsonify({'error': 'An unexpected error occurred while retrieving staff members', 'details': str(e)}), 500
