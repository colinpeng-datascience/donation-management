from flask import request, jsonify, Blueprint
from donman.model import Distribution, Donation, Type, Subtype
from donman.controller import db

report_bp = Blueprint('report', __name__)

# Report by type
@report_bp.route('/report/type/<int:type_id>', methods=['GET'])
def report_by_type(type_id):
    """Generate a report by type"""
    # Aggregate the amount donated
    total_donated = db.session.query(db.func.sum(Donation.donation_quantity)).filter(Donation.subtype_id.in_(db.session.query(Subtype.subtype_id).filter_by(type_id=type_id))).scalar() or 0
    
    # Aggregate the amount distributed
    total_distributed = db.session.query(db.func.sum(Distribution.distribution_amount)).filter(Distribution.subtype_id.in_(db.session.query(Subtype.subtype_id).filter_by(type_id=type_id))).scalar() or 0
    
    # Calculate the remaining amount
    remaining_amount = total_donated - total_distributed

    return jsonify({
        'total_donated': total_donated,
        'total_distributed': total_distributed,
        'remaining_amount': remaining_amount
    }), 200

# Report by subtype
@report_bp.route('/report/subtype/<int:subtype_id>', methods=['GET'])
def report_by_subtype(subtype_id):
    """Generate a report by subtype"""
    # Aggregate the amount donated
    total_donated = db.session.query(db.func.sum(Donation.donation_quantity)).filter_by(subtype_id=subtype_id).scalar() or 0
    
    # Aggregate the amount distributed
    total_distributed = db.session.query(db.func.sum(Distribution.distribution_amount)).filter_by(subtype_id=subtype_id).scalar() or 0
    
    # Calculate the remaining amount
    remaining_amount = total_donated - total_distributed

    return jsonify({
        'total_donated': total_donated,
        'total_distributed': total_distributed,
        'remaining_amount': remaining_amount
    }), 200

@report_bp.route('/report/donor/<int:donor_id>', methods=['GET'])
def report_by_donor(donor_id):
    """Generate a report by donor"""
    # Get all donations by the donor
    donations = Donation.query.filter_by(donor_id=donor_id).all()

    # Initialize a dictionary to store the donation amounts by type and subtype
    report = {}

    for donation in donations:
        subtype = Subtype.query.get(donation.subtype_id)
        type_name = subtype.type.type_name
        subtype_name = subtype.subtype_name
        donation_quantity = donation.donation_quantity

        # Update the report dictionary with the donation amount for each type and subtype
        if type_name not in report:
            report[type_name] = {}
        if subtype_name not in report[type_name]:
            report[type_name][subtype_name] = donation_quantity
        else:
            report[type_name][subtype_name] += donation_quantity

    return jsonify(report), 200


