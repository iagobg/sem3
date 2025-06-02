people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 35},
    {"name": "Charlie", "age": 30},
    {"name": "Diana", "age": 40}
]
string = 'aaa'
test = [person['name'].upper() for person in people if person['age'] > 30]


print(test)