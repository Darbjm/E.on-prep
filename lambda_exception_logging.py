# LAMBDA
points2D = [(1,2), (15,1), (5,-1), (10,4)]

points2D_sorted = sorted(points2D, key=lambda x: x[0] + x[1])

# print(points2D)
# print(points2D_sorted)

a = [1, 2, 3, 4, 5, 6]
b = map(lambda x: x*2, a)
# print(list(b))
c = [x*2 for x in a]
# print(c)

d = filter(lambda x: x%2==0, a)
# print(list(d))

from functools import reduce

product_a = reduce(lambda x,y: x*y, a)
# print(product_a)

# EXCEPTIONS

# try:
#     a = 5/0
#     b = a+"10"
#     c = 10 + 5
# except ZeroDivisionError as e:
#     print(e)
# except TypeError as e:
#     print(e)
# else:
#     print('everything is fine')
# finally:
    # print('cleaning up...')

class ValueTooHighError(Exception):
    pass

class ValueTooSmallError(Exception):
    def __init__(self, message, value):
        self.message = message
        self.value = value

def test_value(x):
    if x > 100:
        raise ValueTooHighError('value is too high')
    if x < 5:
        raise ValueTooSmallError('value is too small', x)

# try:
#     test_value(2)
# except ValueTooHighError as e:
#     print(e)
# except ValueTooSmallError as e:
#     print(e.message, e.value)

# LOGGING
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
# logging.debug('debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('error')
# logging.critical('critical')

# gives the logger a name
# import helper


# include traceback
# try:
#     a = [1,2,3]
#     val = a[4]
# except IndexError as e:
#     logging.error(e, exc_info=True)

import traceback
# try:
#     a = [1,2,3]
#     val = a[4]
# except IndexError as e:
#     logging.error("The error is %s", traceback.format_exc())

from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# roll over after 2KB, and keep backip logs app.log.1, app.log.2, etc.
handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
logger.addHandler(handler)

for _ in range(100000):
    logger.info('Hello, world!')


