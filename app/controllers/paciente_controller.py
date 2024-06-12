from flask import Blueprint, request, jsonify # type: ignore
from app.models.paciente_model import Paciente
from app.views.paciente_view import render_paciente_list, render_paciente_detail
from app.utils.decorators import jwt_required, role_required

paciente_bp = Blueprint("paciente", __name__)

@paciente_bp.route("/patients", methods=["GET"])
@jwt_required
@role_required(roles=["admin", "user"])
def get_pacientes():
    pacientes = Paciente.get_all()
    return jsonify(render_paciente_list(pacientes))

@paciente_bp.route("/patients/<int:id>", methods=["GET"])
@jwt_required
@role_required(roles=["admin", "user"])
def get_paciente(id):
    paciente = Paciente.get_by_id(id)
    if paciente:
        return jsonify(render_paciente_detail(paciente))
    return jsonify({"error": "Paciente no encontrado"}), 404

@paciente_bp.route("/patients", methods=["POST"])
@jwt_required
@role_required(roles=["admin"])
def create_paciente():
    data = request.json
    name = data.get("name")
    lastname = data.get("lastname")
    ci = data.get("ci")
    birth_date = data.get("birth_date")

    if name is None or lastname is None or ci is None or birth_date is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    paciente = Paciente(name=name, lastname=lastname, ci=ci, birth_date=birth_date)
    paciente.save()

    return jsonify(render_paciente_detail(paciente)), 201


# Ruta para actualizar un animal existente
@paciente_bp.route("/patients/<int:id>", methods=["PUT"])
@jwt_required
@role_required(roles=["admin"])
def update_paciente(id):
    paciente = Paciente.get_by_id(id)

    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404

    data = request.json
    name = data.get("name")
    lastname = data.get("lastname")
    ci = data.get("ci")
    birth_date = data.get("birth_date")

    paciente.update(name=name, lastname=lastname, ci=ci, birth_date=birth_date)

    return jsonify(render_paciente_detail(paciente))

@paciente_bp.route("/patients/<int:id>", methods=["DELETE"])
@jwt_required
@role_required(roles=["admin"])
def delete_paciente(id):
    paciente = Paciente.get_by_id(id)

    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404
    
    paciente.delete()
    
    return "", 204
