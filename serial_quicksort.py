

#######################################################
#
# Description - Serial implementation of Quicksort for
#               sorting a list; based on personal implementation
#               of quicksorting a queue used for a class project
#               at Ohio State.
#
# Author - Ted Li
#
########################################################


## BEGIN FUNCTIONS DECLARATIONS SECTION ##

# Parameter details:
# - a_list: list to be sorted in ascending order
#           via serial quicksort; this function
#           DOES modify directly the contents of
#           "a_list"
def serial_quicksort(a_list):
    # Assert that no parameter can be "None"
    assert a_list is not None
    # Recursively partition array into halves and sort
    #    each half until we're sorting lists each of
    #    length 0, then unwind the recursion and merge
    #    the sorted halves together while including in
    #    the middle the partitioning element used to
    #    partition the array recursively.    
    if (len(a_list) > 0):
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
        partition(a_list=a_list,
                     no_larger_than_list=no_larger_than_list,
                     larger_than_list=larger_than_list,
                                partitioner=partitioning_element)
        # Recursively sort the two lists
        serial_quicksort(no_larger_than_list)
        serial_quicksort(larger_than_list)
        # Combine the two recursively sorted lists with
        #   the partitioning element in the proper order
        a_list.extend(no_larger_than_list)
        a_list.append(partitioning_element)
        a_list.extend(larger_than_list)

# Parameter details:
# - a_list: list to be partitioned into two parts: entries greater
#           than "partitioner" and entries less than "partitioner";
#           note that "a_list" WILL BE EMPTY when this function
#           returns
# - no_larger_than_list: When this function returns, will contain all
#                        elements from "a_list" no larger than "partitioner"
# - larger_than_list:  When this function returns, will contain all
#                      elements from "a_list" larger than "partitioner"
# - partitioner: The value used to partition the list
def partition(a_list, no_larger_than_list, larger_than_list, partitioner):
    # Assert that no parameter can be "None"
    assert a_list is not None
    assert no_larger_than_list is not None
    assert larger_than_list is not None
    assert partitioner is not None

    # Make sure "no_larger_than_list" and "larger_than_list" are empty lists
    no_larger_than_list.clear()
    larger_than_list.clear()

    # Remove each element from "a_list", and add the element to either
    # "no_larger_than_list" or "larger_than_list" depending on whether
    # element is larger than, equal to, or smaller than "partitioner"
    while (len(a_list) > 0):
        element = a_list.pop()
        if (element > partitioner):
            larger_than_list.append(element)
        else:
            no_larger_than_list.append(element)

## END FUNCTIONS DECLARATIONS SECTION ##


