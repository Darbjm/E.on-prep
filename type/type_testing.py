from typing import NamedTuple, List, Optional, Dict

'''
Python 2 compatible

def power(x, k): # type: (float, float) -> float
    return x ** k
'''

# Python 3.x


def power(x: float, k: float) -> float:
    return x ** k

# Python 3.5


def log(s: str, *, filename: Optional[str] = None) -> None:
    print('log')

# Python 3.6


x: int = 10


class NT(NamedTuple):
    x: int = 5
    y: int = 1

# Python 3.9


# old way
def print_old(dct: Dict[str, str]) -> None: ...


newDict = {
    "test": "s",
    "test2": "t"
}


# new way no need to import Dict
def print_new(dct: dict[str, str]) -> None:
    print(dct["test"])


print_new(newDict)


def list_sum(l: List[int]) -> int:
    return l[0]


my_list = [1, 2, 3]

list_sum(my_list)


def list_sum2(l: List[object]) -> object:
    return l[0]


my_list2 = [1, 2, 3, "a"]

list_sum2(my_list2)
