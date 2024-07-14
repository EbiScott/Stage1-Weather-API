from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, Organisation, User

organisation_bp = Blueprint('organisation_bp', __name__)


class Organisation(db.Model):
    __tablename__ = "organisation"
    orgId = db.column(db.string(100), nullable=False)
    name = db.column(db.string(100), nullable=False)
    description = db.column(db.string(500), nullable=False)



@organisation_bp.route("/api/organisations", methods=["GET", "POST"])
@jwt_required()
def organisations():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first_or_404()
    
    if request.method == "GET":
        user_organisations = Organisation.query.all()  # Simplified for example, should be filtered for user
        return jsonify({"status": "success", "data": [org.to_dict() for org in user_organisations]}), 200

    if request.method == "POST":
        data = request.json
        if not data.get('name'):
            return jsonify({"errors": [{"field": "name", "message": "Organisation name is required"}]}), 422
        
        new_org = Organisation(name=data['name'], description=data.get('description'))
        db.session.add(new_org)
        db.session.commit()
        return jsonify({"status": "success", "message": "Organisation created successfully", "data": new_org.to_dict()}), 201

@organisation_bp.route("/api/organisations/<int:id>", methods=["GET"])
@jwt_required()
def organisation_id(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first_or_404()
    organisation = Organisation.query.filter_by(id=id).first_or_404()  # Simplified for example, should be filtered for user
    return jsonify({"status": "success", "data": organisation.to_dict()}), 200

def register_organisation_blueprint(app):
    app.register_blueprint(organisation_bp)

# Add this method to Organisation model
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "description": self.description
    }
Organisation.to_dict = to_dict


