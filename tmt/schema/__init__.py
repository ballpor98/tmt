import graphene

from tmt.schema.mutation import Mutation
from tmt.schema.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
