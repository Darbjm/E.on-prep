# generators are functions that return an object that can be iterated over.
# they generate the items inside the object lazily. which means it generates the items one at a time and only when you ask for them.
# they are much more memory effcient when dealing with large data sets.
def mygenerator():
    yield 3
    yield 2
    yield 1

g = mygenerator()

# value = next(g)
# print(value)

# value = next(g)
# print(value)

# value = next(g)
# print(value)

# value = next(g)
# print(value) stopIteration

# print(sum(g))
# print(sorted(g))

def countdown(num):
    print('Starting')
    while num > 0:
        yield num
        num -= 1

# cd = countdown(4)

# value = next(cd)
# print(value)

# print(next(cd))
# print(next(cd))
# print(next(cd))
# print(next(cd)) stopIteration

import sys

def first(n):
    nums = []
    num = 0
    while num < n:
        nums.append(num)
        num += 1
    return nums
# print(sys.getsizeof(first(10000000)))

def first_generator(n):
    num = 0
    while num < n:
        yield num
        num += 1

# print(sys.getsizeof(first_generator(10000000)))

def fibonacci(limit):
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

# fib = fibonacci(30)
# print(fib)
# for i in fib:
#     print(i)

mygenerator = (i for i in range(10) if i % 2 == 0)
print(type(mygenerator))
print(mygenerator)
for i in mygenerator:
    print(i)
print(list(mygenerator))
mylist = [i for i in range(10) if i % 2 == 0]
print(mylist)