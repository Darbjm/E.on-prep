import json

person = {'name': 'Claire', 'age': 28, "city": "New York", "hasChildren": False, "titles": ["engineer", "programmer"]}

# personJSON = json.dumps(person, indent=4, separators=('; ', '= '), sort_keys=True)
personJSON = json.dumps(person, indent=4)
# print(personJSON)

# Write Json to file
# with open('person.json', 'w') as file:
#     json.dump(person, file, indent=4)

# Convert json into dict
person = json.loads(personJSON)
# print(person)

class User:

    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User('Max', 27)

def encode_user(o):
    if isinstance(o, User):
        return {'name': o.name, 'age': o.age, o.__class__.__name__ : True}
    else:
        raise TypeError('Object of type User is not JSON serializable')

userJSON = json.dumps(user, default=encode_user)
# print(userJSON)

from json import JSONEncoder
class UserEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, User):
            return {'name': o.name, 'age': o.age, o.__class__.__name__: True}
        return JSONEncoder.default(self, o)


# userJSON2 = json.dumps(user, cls=UserEncoder)
userJSON2 = UserEncoder().encode(user)
print(userJSON2)

def decode_user(dct):
    if User.__name__ in dct:
        return User(name=dct['name'], age=dct['age'])
    return dct

user = json.loads(userJSON, object_hook=decode_user)
print(type(user))
print(user.name)