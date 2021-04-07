numbers = (1,2,3,4,5,6)

beginning, *middle, secondlast, last = numbers
print(beginning)
print(middle)
print(secondlast)
print(last)

def foo(a,b,c):
    print(a,b,c)

my_list = [0,1,2]
foo(*my_list)

def dct(a,b,c):
    print(a,b,c)

my_dict = {'a': 1, 'b': 2, 'c': 3}
dct(*my_dict)
dct(**my_dict)

def bar(a, b, *, c):
    print(a,b,c)

bar(1, 2, c=3)

def kwargs(a, *args, **kwargs):
    print(a)
    for arg in args:
        print(arg)
    for key in kwargs:
        print(key, kwargs[key])

kwargs(1, 2, 3, four=4, five=5, six=6)

############# SPREAD SETS, TUPLES, LISTS OR DICTS

my_tuple = (1,2,3)
my_set = {4,5,6}

new_list = [*my_tuple, *my_set]
print(new_list)

dict_a = {'a': 1, 'b': 2}
dict_b = {'c': 3, 'd': 4}

dict_c = {**dict_a, **dict_b}
print(dict_c)