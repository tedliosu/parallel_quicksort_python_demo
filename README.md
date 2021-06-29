
# Instructions

1. `sudo -H pip install numpy`

2. Git clone this repository

3. Change working directory to cloned repository
 
4. `./parallel_vs_serial_sort.py` to pit my personal implementations of serial and parallel
   quicksort (of lists) against each other, and report the total time taken to run each of
   those two sorting algorithms/functions. A message of congratulations also appears for
   each of my personal implementations of quicksort if the implementation sorted a list
   correctly. Python's built-in "sorted" function is used to check the correctness of
   each implementation.

5. You may tweak the `LENGTH_OF_STRING` and `LENGTH_OF_STRING_LIST` global variables within
   the main "parallel_vs_serial_sort.py" file to see how each sorting algorithm/function
   operates under various different parameters. The ONLY stipulations on each of those global
   variables' value is that each of them must be a non-negative integer.

# Sample Performance Metrics #

- NOTE: I only picked the best results of multiple runs of the program for showing
  the **maximum (and NOT the average) possible performance gain** from parallelizing
  quicksort in the way that I have implemented it within "parallel_quicksort.py".

## Main Program Output on Machine with Ryzen 5 2600 ##

### Sorting A List Of Length 2 Million ###

<pre>

Initializing list copies to be sorted (this may take some time)...

Generating reference sorted list using Python's "sorted" built-in function for
    validating correctness of serial version and parallel version of quicksort... Done!

Time to sort list of 2000000 strings where each string is 20 characters long...

...using serial version of quicksort: 10.430464 seconds.

...using parallel version of quicksort
    (parallelized over a target of 12 processes): 6.511897 seconds.

Validating result of serial version of quicksort...
    Congratulations, expected and actual lists are equal!

Validating result of parallel version of quicksort...
    Congratulations, expected and actual lists are equal!

</pre>

### Sorting A List Of Length 10 Million

<pre>

Initializing list copies to be sorted (this may take some time)...

Generating reference sorted list using Python's "sorted" built-in function for
    validating correctness of serial version and parallel version of quicksort... Done!

Time to sort list of 10000000 strings where each string is 20 characters long...

...using serial version of quicksort: 62.619475 seconds.

...using parallel version of quicksort
    (parallelized over a target of 12 processes): 34.282575 seconds.

Validating result of serial version of quicksort...
    Congratulations, expected and actual lists are equal!

Validating result of parallel version of quicksort...
    Congratulations, expected and actual lists are equal!

</pre>

# Comments About Code in General

- Please refer to the file descriptions written at the top of each file within
  "serial_quicksort.py" and "parallel_quicksort.py" for where I got my implementations
  of serial and parallel quicksort from.

- I tried speeding up how fast the code ran first by compiling as much as possible
  into C using Cython.  Unfortunately, the code failed to run faster after being
  compiled into C (and then compiled into an executable using `gcc`), as the compiled
  serial version of quicksort took 80+ seconds to run instead of 60+ seconds to run
  when sorting 10 million numbers. So I then tried using Numba's JIT compilation feature
  to speed up the code, which also failed to make the code run faster (i.e. JIT
  compiled serial quicksort took 80+ seconds to run again instead of 60+ seconds).
  Numba also failed to JIT compile the parallel version of quicksort because Numba
  didn't know how to compile the types such as `multiprocessing.connection.Connection`
  under the `multiprocessing` module. Therefore, as far as I'm aware, I have no
  choice but to leave the code as it is in native Python for demonstrating
  serial and parallel quicksort performance.

# Comments About Program Performance In General

- For some reason that I've not been able to completely figure out yet, there
  is sometimes up to a ~60%+ discrepancy in how fast the parallel quicksort portion
  of the program runs from each run to each run of the main program. This is also
  without changing ANYTHING about how my machine runs or changing anything about
  how the overall program runs.  I suspect that it has something to do with inter-
  process communication overhead, as I've noticed in my 'Task Manager' how processes
  are spawned quickly when the parallel quicksort function executes, but it takes a
  while for each spawned process to transition from the zombie state (where each
  spawned process's parent process is presumably finishing receiving the sorted
  partitions of the array) to being terminated.  Unfortunately, due to my general
  lack of knowledge (as of right now) on how inter-process communication is
  implemented with the `Connection` class under Python3's `multiprocessing` module,
  I cannot confirm or deny my current speculations about the performance
  discrepancies.  


