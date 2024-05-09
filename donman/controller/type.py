"""REST API for type."""
from flask import Blueprint, request, jsonify
from donman.controller import db
from donman.model import Type

type_bp = Blueprint('type', __name__)

@type_bp.route('/type', methods=['GET'])
def get_types():
    """get all donation type
    """
    types = Type.query.all()
    return jsonify([type.serialize() for type in types]), 200

@type_bp.route('/type', methods=['POST'])
def register_type():
    """Register a new donation type as specified in request
    """
    data = request.json
    print(data)
    new_type = Type(type_name = data["type_name"])
    db.session.add(new_type)
    db.session.commit()
    return "successful", 200