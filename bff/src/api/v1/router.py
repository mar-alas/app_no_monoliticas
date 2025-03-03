from strawberry.fastapi import GraphQLRouter
from src.api.v1.consultas import Query
from src.api.v1.mutaciones import Mutation
import strawberry

schema = strawberry.Schema(query=Query, mutation=Mutation)
router = GraphQLRouter(schema)