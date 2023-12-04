# Homework: Module 3 - Multithreading and processes in Python

# Task

### 1st Part: Threads

Write a Junk folder handler that sorts the files in the specified folder by extension using multiple threads. Speed up the processing of large directories with many subfolders and files by traversing all folders in parallel in separate threads. The most time-consuming will be transferring the file and getting the list of files in the folder (iterating through the contents of the directory). To speed up the file transfer, it can be done in a separate thread or in a thread pool. It is all the more convenient because you do not process the result of this operation in the application and you can not collect any results. To speed up traversal of the contents of a directory with multiple levels of nesting, you can process each subdirectory in a separate thread or pass the processing to a thread pool.

### 2nd Part: Processes

Write an implementation of the factorize function that takes a list of numbers and returns a list of numbers by which the numbers from the input list are divisible without a remainder.

Implement a synchronous version and measure execution time.

Then improve the performance of your function by implementing multiple CPU cores for parallel computation and measure the execution time again. To determine the number of cores on a machine, use the cpu_count() function from the multiprocessing package.

To check the correct operation of the algorithm of the function itself, use the test:

def factorize(*number):
    # YOUR CODE HERE
    raise NotImplementedError() # Remove after implementation


a, b, c, d  = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
