import django_filters
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


class HealthStat(graphene.ObjectType):
    status = graphene.String()


class Query(graphene.ObjectType):
    health_stat = graphene.Field(HealthStat)

    def resolve_health_stat(self, info):
        return HealthStat("ok")
