# tracking/schema.py
import graphene
import json
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Shipment, Article
from .utils import *


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article


class WeatherType(ObjectType):
    description = graphene.String()
    feels_like = graphene.Float()
    temp = graphene.Float()
    max_temp = graphene.Float()
    min_temp = graphene.Float()


class ShipmentType(DjangoObjectType):
    class Meta:
        model = Shipment

    articles = graphene.List(lambda: ArticleType)
    weather = graphene.Field(lambda: WeatherType)

    def resolve_articles(self, info):
        return self.get_articles()

    def resolve_weather(self, info):
        city = self.get_destination_city()
        if r.exists(city):
            weather_str = get_city_weather(city)
            return json.loads(weather_str)
        else:
            weather = get_weather_from_open_map(city)
            save_weather_redis(city, json.dumps(weather))
            return weather


class Query(graphene.ObjectType):
    shipment = graphene.Field(ShipmentType, tracking_number=graphene.String(required=True),
                              carrier=graphene.String(required=True))

    def resolve_shipment(self, info, tracking_number, carrier):
        return Shipment.objects.get(tracking_number=tracking_number, carrier=carrier)


schema = graphene.Schema(query=Query)
