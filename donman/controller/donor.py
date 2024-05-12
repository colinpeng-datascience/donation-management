"""REST API for donor."""
from flask import Blueprint, request, jsonify
from donman.controller import db
from donman.model import Donor

donor_bp = Blueprint('donor', __name__)


@donor_bp.route('/donor', methods=['GET'])
def get_donors():
    """Get all donor"""
    try:
        donors = Donor.query.all()
        donor_data = [donor.serialize() for donor in donors]
        return jsonify(donor_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve donors', 'details': str(e)}), 500


@donor_bp.route('/donor', methods=['POST'])
def register_donor():
    """Register a new donor as specified by the donor_name and donor_email in request"""
    data = request.json
    if not data or 'donor_name' not in data or "donor_email" not in data:
        return jsonify({'error': 'Invalid data provided'}), 400
    
    new_donor = Donor(donor_name=data["donor_name"], donor_email=data["donor_email"])
    db.session.add(new_donor)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Type registered successfully', 'type_id': new_donor.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register type', 'details': str(e)}), 500
    