import logging

# strawberry
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

# Import Schema Types
from ...schemas.claims import ClaimMutation,ClaimQuery


# Get context
from .context import get_context

# Get Logger
log = logging.getLogger("uvicorn")

Query = merge_types("Query", (
    ClaimQuery,
))

Mutation = merge_types("Mutation", (
    ClaimMutation,
))

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema, context_getter=get_context)