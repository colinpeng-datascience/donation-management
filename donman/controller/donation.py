from flask import request, jsonify, session, abort, Blueprint
from donman.model import Donation
from donman.controller import db

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/donation', methods=['POST'])
def register_donation():
    """
    Register a new donation entry.

    This endpoint is responsible for creating a new donation record in the database
    associated with a staff member and a donor.

    Request format:
    Content-Type: application/json
    {
        "donor_id": "integer",       // Identifier for the donor
        "donation_quantity": "integer",         // The quantity of the donation
        "subtype_id": "integer"      // Identifier for the donation subtype
    }

    Response format:
    Status codes:
    - 200 OK: Donation entry registered successfully.
    - 400 Bad Request: Missing required fields or incorrect data formats.
    - 401 Unauthorized: User is not authenticated.

    Returns a JSON object with a success or error message and suitable HTTP status code.
    """
    try:
        if 'staff_id' not in session:
            abort(401, description='Unauthorized: User must be logged in.')

        data = request.json

        # Validate required fields
        donor_id = data.get("donor_id")
        donation_quantity = data.get("donation_quantity")
        subtype_id = data.get("subtype_id")
        if not all([donor_id, donation_quantity, subtype_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create a new donation record
        new_donation = Donation(
            donor_id=donor_id,
            staff_id=session['staff_id'],  # Extract staff_id from session
            donation_quantity=donation_quantity,
            subtype_id=subtype_id
        )
        db.session.add(new_donation)
        db.session.commit()

        # Return successful response
        return jsonify({
            'message': 'Donation entry registered successfully',
            'donation_id': new_donation.donation_id
        }), 200

    except Exception as e:
        # Perform a rollback in case of any exception
        db.session.rollback()
        # You would likely want to log the exception to your server's log
        print(e)

        # Return a generic error message to the client
        return jsonify({'error': 'An unexpected error occurred'}), 500
