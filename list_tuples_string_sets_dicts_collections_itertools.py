# Five steps of TDD
# 1. write the test
# 2. make the test compile
# 3. watch the test fail
# 4. do just enough to make all the tests pass
# 5. refactor and generalize

#  Arrange-Act-Assert is a pattern for writing unit tests:
#  - Arrange - Set up preconditions
#  - Act - Call the code under test
#  - Assert - Check that expected results have occurred 


list_org = ["banana", "cherry", "apple"]
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Make a copy
list_cpy = list_org[:]
# print(list_cpy)

# Reverse list
a = nums[::-1]
# print(a)

# Create step
b = nums[::2]
# print(b)

# To make a single tuple you must place a comma at the end
my_tuple = ("Max")
real_tuple = ("Max",)
# print(type(my_tuple))
# print(type(real_tuple))

# Without brackets
next_tuple = "Max", 28, "Boston"
name, age, city = next_tuple
# print(name, age, city)

# Split tuple
num_tuple = (0, 1, 2, 3, 4)
i1, *i2, i3 = num_tuple
# print(i1)
# print(i3)
# print(i2)

# Tuple is more efficient
import sys, timeit
my_list = [0, 1, 2, "hello", True]
my_tup = (0, 1, 2, "hello", True)
# print(sys.getsizeof(my_list), "bytes")
# print(sys.getsizeof(my_tup), "bytes")
# print(timeit.timeit(stmt="[0, 1, 2, 3, 4, 5]", number=1000000))
# print(timeit.timeit(stmt="(0, 1, 2, 3, 4, 5)", number=1000000))

# Tuple can be used as key in dict
my_tple = (8, 7)
my_dict = {my_tple : 15}
new_dict = {my_tple : 12, "q" : 10}
my_dict.update(new_dict)
# print(my_dict)

# Sets remove duplicates
my_set = set("hello")
# print(my_set)

# Join sets and intersections
odds = {1, 3, 5, 7}
evens = {0, 2, 4, 6}
primes = {2, 3, 5, 7}
u = odds.union(evens)
# print(u)
i = odds.intersection(primes)
# print(i)

# Find difference and update in differ
setA = {1, 2, 3, 4, 5, 6, 7, 8, 9}
setB = {1, 2, 3, 10, 11, 12}

diff = setA.difference(setB)
diffS = setA.symmetric_difference(setB)
setA.intersection_update(setB)
setA.difference_update(setB)
setA.update(setB)
# print(diff)

# itertools to reduce for loops

from itertools import product, permutations, combinations, combinations_with_replacement, accumulate, groupby
import operator
a = [1, 2]
b = [3, 4]
prod = product(a,b, repeat=1)
# print(list(prod))

c = [1, 2, 3]
perm = permutations(c, 3)
# print(list(perm))

d = [1, 2, 5, 3, 4]
comb = combinations(d, 2)
# print(list(comb))

comb_wr = combinations_with_replacement(d, 2)
# print(list(comb_wr))

acc = accumulate(d)
acc2 = accumulate(d, func=operator.mul)
acc3 = accumulate(d, func=max)
# print(list(acc3))

def smaller_than_3(x):
    return x < 3

group_obj = groupby(d, key=smaller_than_3)
# for key, value in group_obj:
    # print(key, list(value))

persons = [{'name': 'Tim', 'age': 25}, {'name': 'Dan', 'age': 25}, {'name': 'Lisa', 'age': 27}, {'name': 'Claire', 'age': 28}]
group_per = groupby(persons, key=lambda x: x['age'])
# for key, value in group_per:
#     print(key, list(value))
