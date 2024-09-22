import graphene
import traceback
from .models import AppConfig

class updateConfigFeature(graphene.Mutation):
    success: bool = graphene.Boolean()
    allow_introspection: bool = graphene.Boolean()
    message: str = graphene.String()
    
    class Arguments:
        allow_introspection = graphene.Boolean(required=True)
        
    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            config = AppConfig.objects.get(id=1)
            config.allow_introspection = kwargs['allow_introspection']
            config.save()
            return updateConfigFeature(success=True, message='success', allow_introspection=config.allow_introspection)
        except Exception as error:
            error = traceback.format_exc()
            return updateConfigFeature(success=False, message=error)

class Query(graphene.ObjectType):
    greeting = graphene.String()
    
    @staticmethod
    def resolve_greeting(root, info):
        return 'Hello World'

class Mutations(graphene.ObjectType):
    update_config = updateConfigFeature.Field()
    
schema  = graphene.Schema(query=Query, mutation=Mutations)


