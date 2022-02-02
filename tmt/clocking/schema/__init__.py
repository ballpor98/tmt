import graphene

from tmt.clocking.schema.mutation import Mutation
from tmt.clocking.schema.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
