from flask import request, jsonify, Blueprint
from donman.model import Distribution, Donation, Type, Subtype
from donman.controller import db

report_bp = Blueprint('report', __name__)

@report_bp.route('/report/type/<int:type_id>', methods=['GET'])
def report_by_type(type_id):
    """
    Generate a report by type with the total amounts donated and distributed.

    This endpoint calculates aggregate donation and distribution amounts for a specific type
    and returns the remaining quantity of resources for that type.

    URL parameter:
    - type_id (int): The identifier for the type whose report is being queried.

    Response format (JSON object):
    {
        "total_donated": total_donated,        // Sum of donations for the type
        "total_distributed": total_distributed,// Sum of distributions for the type
        "remaining_amount": remaining_amount   // Remaining amount (total_donated - total_distributed)
    }

    Example response:
    {
        "total_donated": 150,
        "total_distributed": 100,
        "remaining_amount": 50
    }

    On error:
    {
        "error": "Failed to generate report by type",
        "details": "Description of the error"
    }

    Status codes:
    - 200 OK: Successfully retrieved the report data.
    - 400 Bad Request: The type_id provided in the URL is invalid.
    - 500 Internal Server Error: A server-side error occurred during report generation.

    Raises:
    - HTTP 400: Raises an HTTP 400 if type_id is not a valid integer.
    - HTTP 500: Raises an HTTP 500 if there is a server-side error such as database connection issue.
    """
    try:
        # Aggregate the amount donated for the type
        total_donated = db.session.query(db.func.sum(Donation.donation_quantity))\
            .filter(Donation.subtype_id.in_(db.session.query(Subtype.subtype_id)\
            .filter_by(type_id=type_id))).scalar() or 0
        
        # Aggregate the amount distributed for the type
        total_distributed = db.session.query(db.func.sum(Distribution.distribution_amount))\
            .filter(Distribution.subtype_id.in_(db.session.query(Subtype.subtype_id)\
            .filter_by(type_id=type_id))).scalar() or 0
        
        # Calculate the remaining amount of the resource
        remaining_amount = total_donated - total_distributed

        return jsonify({
            'total_donated': total_donated,
            'total_distributed': total_distributed,
            'remaining_amount': remaining_amount
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate report by type',
            'details': str(e)
        }), 500

@report_bp.route('/report/subtype/<int:subtype_id>', methods=['GET'])
def report_by_subtype(subtype_id):
    """
    Generate a report for a specific subtype including the total amounts donated and distributed.

    This endpoint returns the aggregate quantities of donations and distributions for a given subtype,
    as well as the calculated remaining amount of resources for that subtype.

    URL parameter:
    - subtype_id (int): The identifier for the subtype being queried.

    Response format (JSON object):
    {
        "total_donated": total_donated,       // Sum of donations for the subtype
        "total_distributed": total_distributed, // Sum of distributions for the subtype
        "remaining_amount": remaining_amount  // Remaining amount (total_donated - total_distributed)
    }

    On error:
    {
        "error": "Failed to generate report by subtype",
        "details": "Description of the error"
    }

    Status codes:
    - 200 OK: Report data was retrieved successfully.
    - 400 Bad Request: The subtype_id provided in the URL is invalid.
    - 500 Internal Server Error: A server-side error occurred during report generation.

    Raises:
    - HTTP 400: Raised if subtype_id is not a valid integer or if no data exists for the subtype.
    - HTTP 500: Raised if there is a server-side error, such as a database connection issue or a failed query.
    """
    try:

        # Aggregate the amount donated for the subtype
        total_donated = db.session.query(db.func.sum(Donation.donation_quantity))\
            .filter_by(subtype_id=subtype_id).scalar() or 0
        
        # Aggregate the amount distributed for the subtype
        total_distributed = db.session.query(db.func.sum(Distribution.distribution_amount))\
            .filter_by(subtype_id=subtype_id).scalar() or 0
        
        # Calculate the remaining amount of the resource for the subtype
        remaining_amount = total_donated - total_distributed

        return jsonify({
            'total_donated': total_donated,
            'total_distributed': total_distributed,
            'remaining_amount': remaining_amount
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate report by subtype',
            'details': str(e)
        }), 500


@report_bp.route('/report/donor/<int:donor_id>', methods=['GET'])
def report_by_donor(donor_id):
    """
    Generate a report summarizing donations made by a specific donor.

    The report includes a breakdown of donations grouped by type and subtype.

    URL parameter:
    - donor_id (int): The identifier for the donor being queried.

    Response format (nested JSON object):
    {
        "type_name": {
            "subtype_name": donation_quantity,
            ...
        },
        ...
    }

    On error:
    {
        "error": "Failed to generate report by donor",
        "details": "Description of the error"
    }

    Status codes:
    - 200 OK: Report data was retrieved successfully.
    - 400 Bad Request: The donor_id provided in the URL is invalid or the donor does not exist.
    - 500 Internal Server Error: A server-side error occurred during report generation.

    Raises:
    - HTTP 400: Raised if donor_id is not a valid integer or no such donor exists.
    - HTTP 500: Raised if there is a server-side error such as a database connection issue.
    """
    try:
        # Get all donations by the donor
        donations = Donation.query.filter_by(donor_id=donor_id).all()

        # Initialize a dictionary to store the donation amounts by type and subtype
        report = {}

        for donation in donations:
            subtype = Subtype.query.get(donation.subtype_id)
            
            type_name = Type.query.filter_by(type_id=subtype.type_id).first().type_name
            subtype_name = subtype.subtype_name
            donation_quantity = donation.donation_quantity

            # Update the report dictionary with the donation amounts
            report.setdefault(type_name, {}).setdefault(subtype_name, 0)
            report[type_name][subtype_name] += donation_quantity

        return jsonify(report), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate report by donor',
            'details': str(e)
        }), 500

