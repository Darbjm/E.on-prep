import functools

def my_decorator(func):
# functools helps python know what the func name is
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # do something then excute the function
        result = func(*args, **kwargs)
        # do something then return result
        print('hello')
        print(result)
        return result
    return wrapper

# @start_end_decorator
# def print_name():
#     print('James')

# print_name = start_end_decorator(print_name)

# print_name()

@my_decorator
def add5(x):
    return x + 5

# result = add5(10)
# print(help(add5))
# print(add5.__name__)

def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=4)
def greet(name):
    print(f'Hello {name}')

# greet('James')

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(signature, kwargs_repr, args_repr)
        print(f'Calling {func.__name__}({signature})')
        result = func(*args, **kwargs)
        print(f'{func.__name__!r} returned {result!r}')
        return result
    return wrapper

def start_end_decorator(func):
# functools helps python know what the func name is
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # do something then excute the function
        print('Start')
        result = func(*args, **kwargs)
        # do something then return result
        print('End')
        return result
    return wrapper

@debug
@start_end_decorator
def say_hello(name):
    greeting = f'Hello {name}'
    print(greeting)
    return greeting

# say_hello('James')


class CountCalls:

    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f'This is executed {self.num_calls} times')
        return self.func(*args, **kwargs)

cc = CountCalls(None)
# cc()

@CountCalls
def say_goodbye():
    print("Goodbye")

say_goodbye()
say_goodbye()