import os
from dotenv import load_dotenv


load_dotenv()


class OpenMapSettings:
    base_url = "http://api.openweathermap.org"
    app_id = os.getenv("OPEN_WEATHER_MAP_API_KEY")


class RedisSettings:
    redis_host = os.getenv("REDIS_HOST")
    redis_password = os.getenv("REDIS_PASSWORD")
    redis_port = os.getenv("REDIS_PORT")
    key_expiration_time = 7200
