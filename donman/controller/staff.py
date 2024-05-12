from flask import request, jsonify, session, abort, Blueprint
from donman.model import Staff
from flask_bcrypt import Bcrypt as bcrypt
from donman.controller import db

staff_bp = Blueprint('staff', __name__)
 
# Register new staff
@staff_bp.route('/staff', methods=['POST'])
def register_staff():
    """Register a new staff"""
    if 'staff_id' not in session:
        abort(401)

    data = request.json
    staff_email = data.get("staff_email")
    staff_password = data.get("staff_password")
    staff_name = data.get("staff_name")
    staff_created_by_staff_id = session['staff_id']

    if not all([staff_email, staff_password, staff_name, staff_created_by_staff_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    existing_staff = Staff.query.filter_by(staff_email=staff_email).first()
    if existing_staff:
        return jsonify({'error': 'Staff with this email already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(staff_password).decode('utf-8')
    new_staff = Staff(
        staff_email=staff_email,
        staff_password_hashed=hashed_password,
        staff_name=staff_name,
        staff_created_by_staff_id=staff_created_by_staff_id
    )

    db.session.add(new_staff)
    db.session.commit()

    return jsonify({'message': 'Staff registered successfully', 'staff_id': new_staff.staff_id}), 200

# Delete a staff (by id)
@staff_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    """Delete a staff by id"""
    if 'staff_id' not in session:
        abort(401)

    staff = Staff.query.get(staff_id)

    if staff:
        # Update the attributes of the staff object
        staff.staff_name = ""
        staff.staff_email = staff.staff_id
        staff.staff_deleted_by_staff_id = session['staff_id']
        staff.staff_password_hashed = ""
        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'Staff deleted successfully'}), 200
    else:
        return jsonify({'error': 'Staff not found'}), 404

# Show all staff
@staff_bp.route('/staff', methods=['GET'])
def get_all_staff():
    """Get all staff"""
    if 'staff_id' not in session:
        abort(401)

    staff = Staff.query.all()
    staff_data = [s.serialize() for s in staff]
    return jsonify(staff_data), 200

@staff_bp.route('/staff/login', methods=['POST'])
def login_staff():
    """Login a staff"""
    data = request.get_json()
    staff_email = data.get('staff_email')
    staff_password = data.get('staff_password')

    if not all([staff_email, staff_password]):
        return jsonify(message='Missing email or password'), 400

    staff = Staff.query.filter_by(staff_email=staff_email).first()
    if staff and bcrypt.check_password_hash(staff.staff_password_hashed, staff_password):
        session['staff_id'] = staff.staff_id
        return jsonify(message='Login successful'), 200
    else:
        return jsonify(message='Login failed'), 401

@staff_bp.route('/staff/login', methods=['DELETE'])
def logout_staff():
    """Logout a staff"""
    if 'staff_id' in session:
        session.pop('staff_id', None)
        return jsonify(message='Logged out'), 200
    else:
        return jsonify(message='No active session'), 401