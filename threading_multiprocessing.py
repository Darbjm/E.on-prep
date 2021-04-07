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

from threading import Thread, Lock
import time

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

database_value = 0

def increase(lock):
    global database_value

    lock.acquire()
    local_copy = database_value
    local_copy += 1
    time.sleep(0.1)
    database_value = local_copy
    lock.release()

if __name__ == '__main__':

    lock = Lock()
    print('start value', database_value)

    thread1 = Thread(target=increase, args=(lock,))
    thread2 = Thread(target=increase, args=(lock,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print('end value', database_value)

    print('end main')

############################# PROCESSING

# from multiprocessing import Process
# import time
# import os

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

    #join
    # for p in processes:
        # p.join()

    # print('end main')

# if __name__ == '__main__':
    # freeze_support()
    # process()


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