import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    last_login = graphene.DateTime(required=False)
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


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        if info.context.get('is_vip'):
            username = username.upper()
        user = User(username=username)
        return CreateUser(user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)

get_user_query = '''
    {
        users(first: 1) {
             username
             last_login
        }
    }
    '''
create_user_query = '''
    mutation create_user($username: String) {
        create_user(username: $username) {
            user {
                username
            }
        }
    }
'''
# result = schema.execute(get_user_query)
result = schema.execute(create_user_query, variables={'username': 'Ban'}, context={'is_vip': False})
try:
    items = dict(result.data.items())
    print(json.dumps(items, indent=4))
except AttributeError as e:
    print(result)
