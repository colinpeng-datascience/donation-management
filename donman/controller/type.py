"""REST API for type."""
from flask import Blueprint, request, jsonify, session, abort
from donman.controller import db
from donman.model import Type, Subtype

type_bp = Blueprint('type', __name__)

from flask import jsonify

@type_bp.route('/type', methods=['GET'])
def get_types():
    """Get all donation types"""

    try:
        types = Type.query.all()
        type_data = [type.serialize() for type in types]
        return jsonify(type_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve types', 'details': str(e)}), 500


@type_bp.route('/type', methods=['POST'])
def register_type():
    """Register a new donation type as specified by the type_name in request"""
    if 'staff_id' not in session:
        abort(401)
    data = request.json
    if not data or 'type_name' not in data:
        return jsonify({'error': 'Invalid data provided'}), 400
    
    new_type = Type(type_name=data["type_name"])
    db.session.add(new_type)
    
    try:
        db.session.commit()
        register_subtype_response = _register_subtype(new_type.type_id, "other")
        if register_subtype_response[1] != 200:
            raise RuntimeError('Failed to register default subtype')
        return jsonify({'message': 'Type registered successfully', 'type_id': new_type.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register type', 'details': str(e)}), 500
    
@type_bp.route('/type/sub', methods=['GET'])
def get_subtypes():
    """Get all donation subtype by type id"""
    data = request.json
    if not data or 'type_id' not in data:
        return jsonify({'error': 'Invalid data provided'}), 400
    
    try:
        subtypes = Subtype.query.filter(Subtype.type_id == data["type_id"])
        subtypes_data = [sub_type.serialize() for sub_type in subtypes]
        return jsonify(subtypes_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve types', 'details': str(e)}), 500

@type_bp.route('/type/sub', methods=['POST'])
def register_subtype():
    """Register a new donation subtype as specified by the subtype_name and type_id in request"""
    if 'staff_id' not in session:
        abort(401)
    data = request.json
    if not data or 'type_id' not in data or "subtype_name" not in data:
        return jsonify({'error': 'Invalid data provided'}), 400
    
    return _register_subtype(data["type_id"], data["subtype_name"])

def _register_subtype(type_id, subtype_name):
    new_subtype = Subtype(type_id=type_id, subtype_name=subtype_name)
    db.session.add(new_subtype)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Type registered successfully', 'type_id': new_subtype.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register type', 'details': str(e)}), 500
