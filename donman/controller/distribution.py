from flask import request, jsonify, session, abort, Blueprint
from donman.model import Distribution
from donman.controller import db

distribution_bp = Blueprint('distribution', __name__)

@distribution_bp.route('/distribution', methods=['POST'])
def register_distribution():
    """
    Register a new distribution entry.

    This endpoint creates a new distribution record in the database associated with a staff member.
    A distribution entry consists of a subtype and the distribution amount.

    The user must be authenticated (a 'staff_id' must be present in the session).

    Request format:
    Content-Type: application/json
    {
        "subtype_id": "int",  // Identifier for the distribution subtype
        "distribution_amount": "int"     // The amount of distribution
    }

    Response format:
    Status codes:
    - 200 OK: Distribution entry registered successfully.
    - 400 Bad Request: Missing required fields or incorrect data formats.
    - 401 Unauthorized: User is not authenticated.

    Returns a JSON object with a success or error message and suitable HTTP status code.
    """
    try:
        if 'staff_id' not in session:
            abort(401, description='Unauthorized: User must be logged in.')

        data = request.json

        # Validate required fields
        subtype_id = data.get("subtype_id")
        distribution_amount = data.get("distribution_amount")
        if not all([subtype_id, distribution_amount]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create a new distribution record
        new_distribution = Distribution(
            staff_id=session['staff_id'],
            subtype_id=subtype_id,
            distribution_amount=distribution_amount
        )
        db.session.add(new_distribution)
        db.session.commit()

        # Return successful response
        return jsonify({'message': 'Distribution entry registered successfully', 'distribution_id': new_distribution.distribution_id}), 200

    except Exception as e:
        # Log the exception internally
        db.session.rollback()
        # You can also log to some logging service or file
        print(e)
        
        # Return a generic error message to the client
        return jsonify({'error': 'An unexpected error occurred'}), 500
