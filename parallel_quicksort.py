

#######################################################
#
# Description - Parallel implementation of Quicksort for
#               sorting a list.  Implementation inspired
#               by python parallel quicksort example from
#               http://eg.bucknell.edu/~jvs008/SC13/codes/parallelQuicksort.py
#               Documentation under https://docs.python.org/3/library/multiprocessing.html
#               was also helpful.
#
# Author - Ted Li
#
########################################################


## IMPORTS SECTION ##

# For parallelizing quicksort
import multiprocessing
# Personal implementation of serial partitioning and quicksort
from serial_quicksort import serial_quicksort, partition

## END IMPORTS SECTION ##


## BEGIN FUNCTIONS DECLARATIONS SECTION ##

# Parameter details:
# - a_list: list to be sorted using parallel quicksort
# - sending_socket: the end of the inter-processes communication pipe
#                   used to send part of the sorted list over to the
#                   parent process, so that the parent process may
#                   combine in the proper order the sorted parts of
#                   the list it recieved from each of the child
#                   processes, after the child processes have each
#                   sorted their assigned portion of the overall
#                   list.
# - current_processes_count: current number of processes that this
#                            function has been parallelized over
# - MAX_PROCESSES_COUNT: maximum number of processes this function
#                        will spawn to sort list in parallel
#
def parallel_quicksort(a_list, sending_socket, current_processes_count,
                                                    MAX_PROCESSES_COUNT):
    # Assert that no parameter can be "None"
    assert a_list is not None
    assert sending_socket is not None
    assert current_processes_count is not None
    assert MAX_PROCESSES_COUNT is not None

    # Recursively partition the list and sort each partition until each
    #     partition is a list of length zero (i.e. the base case has been
    #     reached). Then unwind the recursion and combine the now sorted
    #     partitions into a overall sorted list.
    if (len(a_list) > 0):
        # If we've spawned enough processes recursively for
        #    sorting in parallel, switch over to sorting each
        #    partition of the list via the serial version of
        #    quicksort.
        if (current_processes_count >= MAX_PROCESSES_COUNT):
            serial_quicksort(a_list=a_list)
            # send sorted result to parent process
            sending_socket.send(a_list)
            # close socket as we're done with inter-process communication
            sending_socket.close()
        # Otherwise, partition list using a middle partition element
        #     as in the serial version of quicksort, but here we
        #     send each resulting partition of the list to a process
        #     we spawn that calls this function recursively to
        #     sorting each resulting partition.
        else:
            # Use middle element for partitioning to avoid O(n^2)
            #    runtime especially in cases where the list may
            #    already be sorted
            partitioning_element = a_list.pop((len(a_list) - 1) // 2)
            # List containing all elements no larger than "partitioning_element"
            #    from "a_list".
            no_larger_than_list = []
            # List containing all elements larger than "partitioning_element"
            #    from "a_list".
            larger_than_list = []
            # partition "a_list" using "partitioning_element"
            partition(a_list=a_list, no_larger_than_list=no_larger_than_list,
                           larger_than_list=larger_than_list, partitioner=partitioning_element)
            # Create Pipes for child processes recursively calling
            #     this function to send their sorted results over to
            #     the parent process 
            receive_sock_no_larger_than_proc, send_sock_no_larger_than_proc = \
                                                    multiprocessing.Pipe(duplex=False)
            receive_sock_larger_than_proc, send_sock_larger_than_proc = \
                                                    multiprocessing.Pipe(duplex=False)
            # If each process spawns 2 processes, then at any given level of recursion
            #     we're spawning 2^i processes, where "i" equals how many times
            #     we've called this function recursively. So given n levels of
            #     recursion we have a total of 2^(n+1)-1 processes (including
            #     the root processes) at any given point, which is equivalent to
            #     saying p = 2p + 1 where "p" equals the total number of processes
            #     we've spawned thus far (not that the "=" is assignment and NOT equality!).
            new_process_count = 2 * current_processes_count + 1
            # Create processes which each recursively calls this function for sorting
            #     a partition of "a_list".
            no_larger_than_proc = multiprocessing.Process(target=parallel_quicksort,             \
                                                            args=(no_larger_than_list,           \
                                                                  send_sock_no_larger_than_proc, \
                                                                  new_process_count,             \
                                                                  MAX_PROCESSES_COUNT))
            larger_than_proc = multiprocessing.Process(target=parallel_quicksort,             \
                                                            args=(larger_than_list,           \
                                                                  send_sock_larger_than_proc, \
                                                                  new_process_count,          \
                                                                  MAX_PROCESSES_COUNT))
            # Launch processes spawned to have each process recursively sort a partition
            #     of the list and send the sorted result back over to this parent process.
            no_larger_than_proc.start()
            larger_than_proc.start()
            # Fetch the sorted list partitions from the child processes
            no_larger_than_list = receive_sock_no_larger_than_proc.recv()
            larger_than_list = receive_sock_larger_than_proc.recv()
            # Combine the sorted partitions along with the middle partitioning element
            #     and send the combined result (i.e. the final sorted list/partition)
            #     over to the parent process.
            a_list.extend(no_larger_than_list)
            a_list.append(partitioning_element)
            a_list.extend(larger_than_list)
            sending_socket.send(a_list)
            # Inter-processes communication finished; close the socket used
            #     to send the sorted partition over to the parent process.
            #     Because each child process spawned above recieved a sending
            #     socket and recursively called this function using that
            #     sending socket, the following "close()" method also closes
            #     the inter-process communication pipes used to retrieve the
            #     sorted partitions from each child process.
            sending_socket.close()
            # Wait for each process to finish transmitting the partition it
            #     has sorted to the parent process and make sure each process
            #     has released its resources before exiting this function.
            no_larger_than_proc.join()
            larger_than_proc.join()
            no_larger_than_proc.close()
            larger_than_proc.close()
    # To avoid a deadlock on the base case when number of
    #    processes spawned recursively is less than MAX_PROCESSES_COUNT,
    #    send over the empty list to the parent process and
    #    then close the inter-process communication pipe.
    else:
        sending_socket.send(a_list)
        sending_socket.close()

## END FUNCTIONS DECLARATIONS SECTION ##


