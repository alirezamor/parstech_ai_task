import requests
import redis
from parstech_ai_task.constants import RedisSettings, OpenMapSettings


r = redis.Redis(host=RedisSettings.redis_host, password=RedisSettings.redis_password,
                port=RedisSettings.redis_port, db=9)


def get_weather_from_open_map(city):
    try:
        weather_info = requests.get(
            f'{OpenMapSettings.base_url}/data/2.5/weather?q={city}&cnt=1&appid={OpenMapSettings.app_id}').json()
        feels_like = weather_info['main']['feels_like']
        temp = weather_info['main']['temp']
        max_temp = weather_info['main']['temp']
        min_temp = weather_info['main']['temp']
        weather_description = ''
        for w in weather_info['weather']:
            weather_description += w['main'] + ', ' + w['description'] + '.'
        return {'feels_like': feels_like, 'temp': temp, 'max_temp': max_temp, 'min_temp': min_temp,
                'description': weather_description}
    except Exception as ex:
        raise ex


def save_weather_redis(city, weather):
    r.setex(city, RedisSettings.key_expiration_time, weather)


def get_city_weather(city):
    return r.get(city)
