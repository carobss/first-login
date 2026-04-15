import uuid
from app.repositories.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    def pre_register_user(self, name, email, birth_date):
        user_data = {
            "name": name,
            "email": email,
            "birth_date": birth_date,
            "first_login": "true"  # Marcador para sabermos que ele nunca logou
        }
        
        self.repository.save_user_pre_registration(email, user_data)
        return {"message": "Pré-cadastro realizado com sucesso!"}

    def login_check(self, email):
        user = self.repository.get_user_data(email)

        if not user:
            return {"error": "Usuário não encontrado. Por favor, cadastre-se."}, 404

        # Se for primeiro acesso, geramos o token de ativação
        if user.get("first_login") == "true":
            token = str(uuid.uuid4())
            self.repository.set_activation_token(token, email)
            
            return {
                "first_login": True,
                "activation_link": f"http://localhost:5000/auth/activate?token={token}",
                "message": "Este é seu primeiro acesso. Defina uma senha."
            }, 200

        return {"first_login": False, "message": "Prossiga com a senha."}, 200

    def finalize_activation(self, token, password):
        # Recupera o e-mail associado ao token no Redis
        email = self.repository.redis_client.get(f"token:{token}")

        if not email:
            return {"error": "Token inválido ou expirado."}, 400

        # Salva senha no banco

        # Atualiza o status do usuário
        user_data = self.repository.get_user_data(email)
        user_data["first_login"] = "false"
        user_data["password"] = password # Em produção, use hash de senha!
        
        self.repository.save_user_pre_registration(email, user_data)
        
        # Remove o token usado
        self.repository.redis_client.delete(f"token:{token}")

        return {"message": "Senha definida com sucesso! Agora você pode logar."}, 200