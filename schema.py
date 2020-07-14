import graphene
import json
from datetime import datetime

class User(graphene.ObjectType):
    last_login = graphene.DateTime()
    username = graphene.String()
    id = graphene.ID()

class Query(graphene.ObjectType):
    users = graphene.List(User, first=graphene.Int())

    def resolve_users(self, info, first):
        return [
            User(username='Foo', last_login=datetime.now()),
            User(username='Bar', last_login=datetime.now()),
            User(username='Baz', last_login=datetime.now()),
        ][:first]

schema = graphene.Schema(query=Query, auto_camelcase=False)

result = schema.execute(
    '''
    {
        users(first: 1) {
             username
             last_login
        }
    }
    '''
)

print(result)
items = dict(result.data.items())

print(json.dumps(items, indent=4))
