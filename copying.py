import copy

# make a shallow copy
org = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
cpy = copy.copy(org)
cpy[0][1] = -10
print(cpy)
print(org)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person('Millie', 24)
p2 = copy.copy(p1)

p2.age = 28
print(p2.age)
print(p1.age)

# make deep copy 
org = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
cpy = copy.deepcopy(org)
cpy[0][1] = -10
print(cpy)
print(org)

class Company:
    def __init__(self, boss, employee):
        self.boss = boss
        self.employee = employee

p3 = Person('Jim', 25)
p4 = Person('Max', 34)

# Create company
company = Company(p3, p4)
# Create a deep copy of the company
company_clone = copy.deepcopy(company)
# Change variable in copy
company_clone.boss.age = 26
# Variables are now different
print(company_clone.boss.age)
print(company.boss.age)