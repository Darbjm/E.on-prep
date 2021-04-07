# Process: An instance of a program (e.g a Python interpreter)
# + Takes advantage of miltiple CPUs and cores
# + Separate memory space -> Memoory is not shared between processes
# + Great for CPU-bound processing
# + New process is stated independently from other processes

# - Heavyweight
# - Starting a process is slower than starting a thread
# - More memory
# - IPC (inter-process communication) is more complicated

# Threads: An entity within a process that can be scheduled (also known as leightweight process)
# A process can spawn multiple threads.

# + All threads within a process share the same memory
# + Leightweight
# + Starting a thread is faster than starting a process
# + Great for I/O-BOUND TASKS

# - Threading is limited by GIL: Only one thread at a time
# - No effect for CPU-bound tasks
# - Not interruptable/killable
# - Careful with race conditions

# GIL: Global interpreter lock
# - A lock that allows only one thread at a time to execute in Python

# - Needed in CPython because memory management is not thread-safe
# - References to objects are kept count and when the count reaches 0 the memory is released.
# - When using threads these my interfer with the counts in other threads causing leaks

#  - Avoid:
# - Use multiprocessing
# - Use a different, free-threaded Python implementation (Jython, IronPython)
# - User Python as a wrapper for third-party lbraries (C/C++) -> numpy, scipy

from threading import Thread, Lock, current_thread
from queue import Queue
import time

############# NOT THREAD SAFE

# def square_numbers():
#     for i in range(100):
#         i + i
#         time.sleep(0.1)

# threads = []
# num_threads = 10

# # create threads
# for i in range(num_threads):
#     t = Thread(target=square_numbers)
#     threads.append(t)

# # start
# for t in threads:
#     t.start()

# #join
# for t in threads:
#     t.join()

# print('end main')

############# THREAD SAFE

# database_value = 0

# def increase(lock):
#     global database_value

#     # can use context manager with locks
#     with lock:
#         local_copy = database_value
#         local_copy += 1
#         time.sleep(0.1)
#         database_value = local_copy
#     # could use lock.acquire() then finish with lock.release()

# if __name__ == '__main__':

#     lock = Lock()
#     print('start value', database_value)

#     thread1 = Thread(target=increase, args=(lock,))
#     thread2 = Thread(target=increase, args=(lock,))

#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     print('end value', database_value)

#     print('end main')

############# QUEING AND BACKGROUND

# def worker(q, lock):
#     # this would normally be infinate but as its a background thread it stops when the main thread stops
#     while True:
#         value = q.get()

#         # processing...
#         with lock:
#             print(f'in {current_thread().name} got {value}')
#             q.task_done()

# if __name__ == '__main__':
#     # A queue creates a first in first out list
#     q = Queue()
#     lock = Lock()
#     num_threads = 10

#     for i in range(num_threads):
#         thread = Thread(target=worker, args=(q, lock))
#         # daemon puts the process in the background
#         Thread.daemon=True
#         thread.start()

#     for i in range(1, 21):
#         q.put(i)
    
#     q.join()

#     print('end main')

############################# PROCESSING

from multiprocessing import Process, Value, Array, Lock, Pool
from multiprocessing import Queue
import time
import os

########## DOES NOT WORK

# def process():
#     def square_numbers():
#         for i in range(100):
#             i + i
#             time.sleep(0.1)

#     processes = []
#     num_processes = os.cpu_count()

#     # create threads
#     for i in range(num_processes):
#         p = Process(target=square_numbers)
#         processes.append(p)

#     # start
#     for p in processes:
#         p.start()

#     join
#     for p in processes:
#         p.join()

#     print('end main')

# if __name__ == '__main__':
    # freeze_support()
    # process()

########## NOT SURE HOW THIS WORKS - FOUND ON INTERNET

# import multiprocessing as mp  
# import time  

# def test_function(i):   
#     print("function starts" + " " + str(i))  
#     time.sleep(1)  
#     print("function ends" + str(i))  

# if __name__ == '__main__':  
#     pool = mp.Pool(mp.cpu_count())  
#     pool.map(test_function, [i for i in range(4)])  
#     pool.close()  
#     pool.join()  

########## LOCKING

# def add_100(numbers, lock):
#     for i in range(100):
#         time.sleep(0.01)
#         # Lock allows only one process or thread to change it at a time
#         for i in range(len(numbers)):
#             with lock:
#                 numbers[i] += 1


# if __name__ == '__main__':

#         lock = Lock()
#         shared_array = Array('d', [0.0, 100.0, 200.0])
#         print('Number at beginning is', shared_array[:])

#         p1 = Process(target=add_100, args=(shared_array, lock))
#         p2 = Process(target=add_100, args=(shared_array, lock))

#         p1.start()
#         p2.start()

#         p1.join()
#         p2.join()

#         print('array at end is', shared_array[:])

########## QUEING
# If it matters what order processes begin

# def square(numbers, queue):
#     for i in numbers:
#         queue.put(i * i)

# def make_negative(numbers, queue):
#     for i in numbers:
#         queue.put(-1 * i)

# if __name__ == '__main__':

#     numbers = range(1, 6)
#     q = Queue()

#     p1 = Process(target=square, args=(numbers, q))
#     p2 = Process(target=make_negative, args=(numbers, q))

#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()

#     while not q.empty():
#         print(q.get())

########## POOL

def cube(number):
    return number * number * number

if __name__ == '__main__':

    numbers = range(10)
    pool = Pool()

    # pool creates as many processes as possible to run the function on paralell processes
    result = pool.map(cube, numbers)

    pool.close()
    pool.join()
    print(result)