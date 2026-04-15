from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

auth_service = AuthService()

@auth_bp.route('/pre-register', methods=['POST'])
def pre_register():
    """Rota para o pré-cadastro (Nome, Email, Nascimento)."""
    data = request.json
    
    if not all(k in data for k in ("name", "email", "birth_date")):
        return jsonify({"error": "Dados incompletos"}), 400

    result = auth_service.pre_register_user(
        name=data['name'], 
        email=data['email'], 
        birth_date=data['birth_date']
    )
    return jsonify(result), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Rota de login que identifica se é o primeiro acesso."""
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400
    
    result, status_code = auth_service.login_check(email)
    return jsonify(result), status_code

@auth_bp.route('/activate', methods=['POST'])
def activate():
    """Rota para definir a senha no primeiro acesso."""
    data = request.json
    token = data.get('token')
    password = data.get('password')

    if not token or not password:
        return jsonify({"error": "Token e senha são obrigatórios"}), 400

    result, status_code = auth_service.finalize_activation(token, password)
    return jsonify(result), status_code