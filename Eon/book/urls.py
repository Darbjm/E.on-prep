from django.urls import path
from graphene_django.views import GraphQLView
from .schema import sch

urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True, schema=sch))
]