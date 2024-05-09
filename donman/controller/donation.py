"""REST API for donation."""
from flask import Blueprint, request, jsonify

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/donation', methods=['POST'])
def register_donation():
    """Register the donation as specified in request
    """
    data = request.json
    # TODO: finish this function
    context = {
        "id": 0
    }
    return jsonify(**context), 200