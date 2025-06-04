import redis
r = redis.Redis(host='localhost', port=8001, db=0, password='your_strong_password')
try:
    print(r.ping())
except Exception as e:
    print(f"Ошибка подключения к Redis: {e}")