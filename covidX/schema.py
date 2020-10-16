import graphene
from graphene_django.debug import DjangoDebug

import apps.apihealth.schema as schema


class Query(schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutations(graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    # TODO(codecakes): Enable when Mutations ready.
    # mutation=Mutations
)
