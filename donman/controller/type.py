"""REST API for type."""
from flask import Blueprint, request, jsonify, session, abort
from donman.controller import db
from donman.model import Type, Subtype

type_bp = Blueprint('type', __name__)

@type_bp.route('/type', methods=['GET'])
def get_types():
    """
    Retrieve all donation types from the database.

    This endpoint returns a list of all the donation types that have been registered.

    No parameters required.

    Response format (JSON array):
    A JSON array of serialized type objects each containing type details.

    Example response:
    [
        {
            "id": 1,
            "name": "Food",
        },
        {
            "id": 2,
            "name": "Clothing",
        },
        ...
    ]

    On error (JSON object):
    {
        "error": "Failed to retrieve types",
        "details": "Error message string here"
    }

    Status codes:
    - 200 OK: Donation types information retrieved successfully.
    - 500 Internal Server Error: A server-side error occurred during the data retrieval process.

    Raises:
    - HTTP 500: Raised if there is a server error, such as database connection issues or issues with the query execution.
    """
    try:
        types = Type.query.all()
        # Ensure that the 'serialize' method is defined in the Type model and serializes data correctly.
        type_data = [type.serialize() for type in types]
        return jsonify(type_data), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@type_bp.route('/type', methods=['POST'])
def register_type():
    """
    Register a new donation type provided by type_name in the request payload.

    Only authenticated staff members can create new donation types.

    Request format (JSON object):
    Content-Type: application/json
    {
        "type_name": "string"  // The name of the new donation type
    }

    Response format:
    On success (JSON object):
    {
        "message": "Type registered successfully",
        "type_id": new_type.id  // The identifier of the newly created donation type
    }
    Status codes:
    - 200 OK: New donation type registered successfully.
    - 400 Bad Request: Required data is missing or data format is incorrect.
    - 401 Unauthorized: The user attempting to create the donation type is not authenticated.
    - 500 Internal Server Error: A server-side error occurred during the registration process.

    Raises:
    - HTTP 400: Raised if the 'type_name' key is missing from the payload.
    - HTTP 401: Raised if the user attempting to register the type is not authenticated.
    - HTTP 500: Raised if there is a server error during the process of registration, including issues while committing to the database or issues with registering the default subtype.
    """
    try:
        if 'staff_id' not in session:
            abort(401, description='Unauthorized: An authenticated staff user is required.')

        data = request.json
        type_name = data.get("type_name")
        
        if not type_name:
            return jsonify({'error': 'Invalid data provided'}), 400
        
        new_type = Type(type_name=type_name)
        db.session.add(new_type)
        db.session.commit()
        new_subtype = Subtype(type_id=new_type.type_id, subtype_name="other")
        db.session.add(new_subtype)
                
        db.session.commit()
        return jsonify({'message': 'Type registered successfully', 'type_id': new_type.type_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@type_bp.route('/type/sub', methods=['GET'])
def get_subtypes():
    """
    Retrieve all donation subtypes associated with a specific type id.

    The type id is provided as a query parameter and is used to fetch the subtypes.

    Query parameter:
    - type_id (int): The identifier for the donation type.

    Response format (JSON array):
    A JSON array of serialized subtype objects containing subtype details.

    [
        {
            'id': subtype_id,
            'name': subtype_name,
        }
    ]

    Status codes:
    - 200 OK: Subtype information retrieved successfully.
    - 400 Bad Request: Type id is not provided or is invalid.
    - 500 Internal Server Error: A server-side error occurred during the retrieval process.

    Raises:
    - HTTP 400: Raised if the 'type_id' is missing or invalid.
    - HTTP 500: Raised if there is a server error, such as a database connection issue or a failed query execution.
    """
    type_id = request.args.get('type_id')
    if not type_id:
        return jsonify({'error': 'Invalid data provided'}), 400

    try:
        subtypes = Subtype.query.filter(Subtype.type_id == type_id).all()
        subtypes_data = [subtype.serialize() for subtype in subtypes]
        return jsonify(subtypes_data), 200
    except Exception as e:
        # Handle any other unexpected exceptions
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@type_bp.route('/type/sub', methods=['POST'])
def register_subtype():
    """
    Register a new donation subtype associated with an existing donation type.

    Requires an authenticated staff member.

    Request format (JSON object):
    Content-Type: application/json
    {
        "type_id": int,         // The identifier of the existing donation type
        "subtype_name": "string"    // The name of the new donation subtype
    }

    Response format:
    On success:
    A JSON object with the message and the id of the newly registered donation subtype.
    
    Status codes:
    - 200 OK: The new donation subtype was registered successfully.
    - 400 Bad Request: The request is missing the 'type_id' or 'subtype_name', or the provided data format is incorrect.
    - 401 Unauthorized: The user attempting to register the donation subtype is not authenticated.

    Raises:
    - HTTP 401: Raised if the user attempting to register the subtype is not authenticated.
    - HTTP 400: Raised if the 'type_id' or 'subtype_name' keys are missing from the payload.
    """
    if 'staff_id' not in session:
        abort(401)
    
    data = request.json
    type_id = data.get("type_id")
    subtype_name = data.get("subtype_name")
    
    if not type_id or not subtype_name:
        return jsonify({'error': 'Invalid data provided'}), 400
    
    try:
        new_subtype = Subtype(type_id=type_id, subtype_name=subtype_name)
        db.session.add(new_subtype)
        db.session.commit()
    except Exception as e:
        # Handle any  unexpected exceptions here
        return jsonify({'error': 'An unexpected error occurred while registering subtype', 'details': str(e)}), 500
