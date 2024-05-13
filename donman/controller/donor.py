"""REST API for donor."""
from flask import Blueprint, request, jsonify
from donman.controller import db
from donman.model import Donor

donor_bp = Blueprint('donor', __name__)


@donor_bp.route('/donor', methods=['GET'])
def get_donors():
    """
    Retrieve a list of all registered donors in the system.

    No request parameters are required.

    Response format:
    A JSON array of donor objects, where each object contains the donor details.
        {
            'id': donor_id,
            'email': donor_email,
            'name': donor_name,
        }
    
    On error:
    - If there is an issue retrieving donor data from the database:
        {
            "error": "Failed to retrieve donors",
            "details": "Error message string here"
        }
    Status codes:
    - 200 OK: Donor data retrieved successfully.
    - 500 Internal Server Error: An error occurred during retrieval of donor data.

    Returns a JSON array with the donor data and an HTTP status code.
    """
    try:
        donors = Donor.query.all()
        donor_data = [donor.serialize() for donor in donors]  # Ensure serialize method is well-defined
        return jsonify(donor_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve donors', 'details': str(e)}), 500


@donor_bp.route('/donor', methods=['POST'])
def register_donor():
    """
    Register a new donor.

    Request format:
    Content-Type: application/json
    {
        "donor_name": "string",   // The name of the donor
        "donor_email": "string"   // The email of the donor
    }

    Response format:
    On success:
    {
        "message": "Donor registered successfully",
        "donor_id": "new donor's id value"
    }
    On failure:
    - If data is missing or invalid:
        {
            "error": "Invalid data provided"
        }
    - If there is a failure in saving the donor to the database:
        {
            "error": "Failed to register donor",
            "details": "Error message string here"
        }
    Status codes:
    - 200 OK: Donor registered successfully.
    - 400 Bad Request: Missing or invalid data provided.
    - 500 Internal Server Error: An error occurred during donor registration.

    Returns a JSON object with a success or error message and a suitable HTTP status code.
    """
    try:
        data = request.json
        if not data or 'donor_name' not in data or 'donor_email' not in data:
            return jsonify({'error': 'Invalid data provided'}), 400
        
        new_donor = Donor(donor_name=data["donor_name"], donor_email=data["donor_email"])
        db.session.add(new_donor)
        db.session.commit()
        
        return jsonify({'message': 'Donor registered successfully', 'donor_id': new_donor.donor_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register donor', 'details': str(e)}), 500
