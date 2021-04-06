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

