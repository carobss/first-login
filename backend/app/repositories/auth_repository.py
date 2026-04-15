from app.infra.redis_client import redis_client

class AuthRepository:
    
    def __init__(self):
            self.redis_client = redis_client
    
    def save_user_pre_registration(self, email: str, user_data: dict):
        key = f"user:pre:{email}"
        # hset armazena o dicionário completo no Redis
        redis_client.hset(key, mapping=user_data)
        # O cadastro expira em 24h se não for ativado (86400 segundos)
        redis_client.expire(key, 86400)

    def get_user_data(self, email: str):
        """Busca todos os dados do usuário no Redis."""
        return redis_client.hgetall(f"user:pre:{email}")

    def set_activation_token(self, token: str, email: str):
        """Salva o token de ativação com tempo de expiração (15 min)."""
        redis_client.setex(f"token:{token}", 900, email)