from flask import request, jsonify, session, abort, Blueprint
from donman.model import Donation
from donman.controller import db

donation_bp = Blueprint('donation', __name__)

# Register a new donation entry
@donation_bp.route('/donation/register', methods=['POST'])
def register_donation():
    """Register a new donation entry"""
    if 'staff_id' not in session:
        abort(401)

    data = request.json
    donor_id = data.get("donor_id")
    donation_quantity = data.get("donation_quantity")
    subtype_id = data.get("subtype_id")

    if not all([donor_id, donation_quantity, subtype_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_donation = Donation(
        donor_id=donor_id,
        staff_id=session['staff_id'],  # Get staff_id from session
        donation_quantity=donation_quantity,
        subtype_id=subtype_id
    )

    db.session.add(new_donation)
    db.session.commit()

    return jsonify({'message': 'Donation entry registered successfully', 'donation_id': new_donation.donation_id}), 200