# fakeredis para teste
import fakeredis

def get_redis_connection():
    print("Utilizando Fakeredis (Simulador em memória)")
    return fakeredis.FakeRedis(decode_responses=True)

redis_client = get_redis_connection()

# Redis real
#import redis
#from app.core.config import settings
#
#def get_redis_connection():
#    """
#    Cria e retorna uma conexão com o Redis. 
#    Usamos decode_responses=True para receber strings em vez de bytes.
#    """
#    try:
#        client = redis.StrictRedis(
#            host=settings.REDIS_HOST,
#            port=settings.REDIS_PORT,
#           decode_responses=True
#       )
#        client.ping()
#        return client
#    except redis.ConnectionError:
#        import fakeredis
#        return fakeredis.FakeRedis(decode_responses=True)
#
#redis_client = get_redis_connection()