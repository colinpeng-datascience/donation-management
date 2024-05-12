from flask import request, jsonify, session, abort, Blueprint
from donman.model import Distribution
from donman.controller import db

distribution_bp = Blueprint('distribution', __name__)

# Register a new distribution entry
@distribution_bp.route('/distribution/register', methods=['POST'])
def register_distribution():
    """Register a new distribution entry"""
    if 'staff_id' not in session:
        abort(401)

    data = request.json
    subtype_id = data.get("subtype_id")
    distribution_amount = data.get("distribution_amount")

    if not all([subtype_id, distribution_amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_distribution = Distribution(
        staff_id=session['staff_id'],  # Get staff_id from session
        subtype_id=subtype_id,
        distribution_amount=distribution_amount
    )

    db.session.add(new_distribution)
    db.session.commit()

    return jsonify({'message': 'Distribution entry registered successfully', 'distribution_id': new_distribution.distribution_id}), 200