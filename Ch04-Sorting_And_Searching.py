"""Chapter 04: Sorting and Searching"""

# Sorting and Searching are so fundamental to software processes that Computer Scientists have striven to get them as efficient as possible.


"""Insertion Sort"""
# This method relies on looking at each item individually in a list  and inserting it into a seprate list that is correctly sorted
# This algorithm will have two parts:
    # An insertion section which inserts an entry into a list
    # A sort section which performs insertion repeatedly until we have completed our sorting task.

# Algorithm for sorting a filing cabinet:
    # First select the highest file in the filing cabinet. (We'll start at the back of the cabinet and work our way to the front).
    # Next compare the file you have selected with the file to insert.
    # If the file you have selected is lower then the filr to insert, place the file to insert one position behind that file.
    # If the file you have selected is higher than the file to insert, select the net highest file in the filing cabinet.
    # Repeat steps 2 to 4 until you have inserted your file or compared it with every existing file. If you have not yet inserted your file after comparing it with every existing file, insert it at the beginning of the filing cabinet.

# Here os the code for that algorithm:

cabinet = [1,2,3,3,4,6,8,12]
to_insert = 5

# We proceed through every number on the list . This variable called check_location will store the location of the cabinet we want to check. We start at the back:
check_location = len(cabinet) - 1 

# We define a value called insert_location. The goal of the algorithm is to determine the proper value of insert_location, and then it's a matter of inserting the file at insert_location.
insert_location = 0


if to_insert > cabinet[check_location]:
    insert_location = check_location + 1

# After we know the right insert_location, we can use a built-in Python method for list manipulation called insert to put the file into the cabinet:
cabinet.insert(insert_location, to_insert)

# The code for insertion algorithm:
def insert_cabinet(cabinet,to_insert):
    check_location = len(cabinet) - 1
    insert_location = 0
    while(check_location >=0):
        if to_insert > cabinet[check_location]:
            insert_location = check_location + 1
            check_location = -1
        check_location = check_location - 1
    cabinet.insert(insert_location,to_insert)
    return(cabinet)

cabinet = [1,2,3,3,4,6,8,12]
newcabinet = insert_cabinet(cabinet, 5)
print(newcabinet)

"""
Page 54: Sorting via Insertion
"""

# Now that we know how to insert and have the code for it, we can perform insertion sort.

# Insertion Sort is where we take each element of an unsorted list at a time and use the insertion algorithm to insert it correctly into a new sorted list:

cabinet = [8,4,6,1,2,5,3,7]
newcabinet = []

# Implement insert sort  by repeatedly calling insert_cabinet(). In order to call it, we need to have a file in our hand by popping the item out of the unsorted array:

to_insert = cabinet.pop(0) # pop() removes a list element at a specified index. After we use pop(), the array no longer contains the item that we popped. Instead that item is stored in a separate variable.
newcabinet = insert_cabinet(newcabinet, to_insert)

# Below is a fully fleshed out function for the Insertion Sort Algorithm:

cabinet = [8,4,6,1,2,5,3,7]

def insertion_sort(cabinet):

    # Insertion Algorithm
    def insert_cabinet(cabinet,to_insert):
        check_location = len(cabinet) - 1
        insert_location = 0
        while(check_location >=0):
            if to_insert > cabinet[check_location]:
                insert_location = check_location + 1
                check_location = -1
            check_location = check_location - 1
        cabinet.insert(insert_location,to_insert)
        return(cabinet)
    
    # Sorting Algorithm
    newcabinet = []
    while len(cabinet) > 0:
        to_insert = cabinet.pop(0)
        newcabinet = insert_cabinet(newcabinet, to_insert)
    return(newcabinet)

sortedcabinet = insertion_sort(cabinet)
print(sortedcabinet)



# The above algorithm can sort any list. However it might not be the most efficient algorithm.


"""
Page 55: Measuring Algorithm Efficiency
"""

# Algorithm efficiency is measured by speed and the amount of memory used. If you can save a tenth of a second on a 100 item sort... That is extremely significant when sorting and dealing with data sets that are billions and trillions of items long as is seen in search engines, machine learning models, banking information, etc...

# Python has a module called timeit that is used to measure the time it takes to sort a list of items.

from timeit import default_timer as timer
start = timer()
cabinet = [8,4,6,1,2,5,3,7]
sortedcabinet = insertion_sort(cabinet)
end = timer()
print("Insertion_Sort Algorthim Timespan: " + str(end-start) + "seconds")

# However time isn't very precise as a measure of algorithm efficiency. Differences in hardware speed, hardware architecture, version of Python, randomness, phases of the moon, solar flares, etc... can effect the speed of an algorithm and change it from moment to moment. At such speeds we are working with, these subtle energetic factors matter.

# Instead, we can measure the steps required to execute an algorithm.

# For the insertion_sort algorithm, we can modify the code to add a step counter to increasr the step count each time we:
    #  pick a new file to insert from the old cabinet
    #  everytime we compare that file to another file in the new cabinet
    # Everytime we insert the file into the new cabinet

def insertion_sort_with_counter(cabinet):
    

    # Insertion Algorithm
    def insert_cabinet(cabinet,to_insert):
        global step_counter
        check_location = len(cabinet) - 1
        insert_location = 0
        while(check_location >=0):
            step_counter += 1
            if to_insert > cabinet[check_location]:
                insert_location = check_location + 1
                check_location = -1
            check_location = check_location - 1
        step_counter += 1
        cabinet.insert(insert_location,to_insert)
        return(cabinet)
    
    # Sorting Algorithm
    newcabinet = []
    global step_counter
    while len(cabinet) > 0:
        step_counter += 1
        to_insert = cabinet.pop(0)
        newcabinet = insert_cabinet(newcabinet, to_insert)
    return(newcabinet)

cabinet = [8,4,6,1,2,5,3,7]
step_counter = 0
sortedcabinet = insertion_sort_with_counter(cabinet)
print(sortedcabinet)
print("Number of steps in Algorithm: " + str(step_counter))


# We can test the insertion algorithm with lists of different lengths.
# Instead of writing out the list manually, we can do it with a module:

import random
size_of_cabinet = 10
cabinet = [int(1000 * random.random()) for i in range(size_of_cabinet)]

def check_steps(size_of_cabinet):
    cabinet = [int(1000 * random.random()) for i in range(size_of_cabinet)]
    global step_counter
    step_counter = 0
    sortedcabinet = insertion_sort_with_counter(cabinet)
    return(step_counter)

# Page 59: Let's create a list of all numbers between 1 and 100 and check the number of steps required to sort each length
random.seed(5040)
xs = list(range(1,100))
ys = [check_steps(x) for x in xs]
print("Number of Steps: " + str(ys))

# We can plot the relationship between list length and sorting steps as follows:

import matplotlib.pyplot as plt
plt.plot(xs,ys)
plt.title("Steps Required for Insertion Sort for Random Cabinets")
plt.xlabel("Number of Files in Random Cabinet")
plt.ylabel("Steps Required to Sort Cabinet by Insertion Sort")
plt.show()

# Compare Insertion Sort to Exponential Function:
import math
import numpy as np
random.seed(5040)
xs = list(range(1,100))
ys = [check_steps(x) for x in xs]
ys_exp = [math.exp(x) for x in xs]
plt.plot(xs,ys)
axes = plt.gca()
axes.set_ylim([np.min(ys),np.max(ys) + 140])
plt.plot(xs,ys_exp)
plt.title('Comparing Insertion Sort to the Exponential Function')
plt.xlabel('Number of Files in Random Cabinet')
plt.ylabel('Steps Required to Sort Cabinet')
plt.show()

# Compare Insertion Sort to other Functions:
random.seed(5040)
xs = list(range(1,100))
ys = [check_steps(x) for x in xs]
xs_exp = [math.exp(x) for x in xs]
xs_squared = [x**2 for x in xs]
xs_threehalves = [x**1.5 for x in xs]
xs_cubed = [x**3 for x in xs]
plt.plot(xs,ys)
axes = plt.gca()
axes.set_ylim([np.min(ys),np.max(ys) + 140])
plt.plot(xs,xs_exp)
plt.plot(xs, xs)
plt.plot(xs,xs_squared)
plt.plot(xs,xs_threehalves)
plt.plot(xs,xs_cubed)
plt.title('Comparing Insertion Sort to Other Growth Rates')
plt.xlabel('Number of Files in Random Cabinet')
plt.ylabel('Steps Required to Sort Cabinet')
plt.show()

# From the graphs created in the code above we can see that the Insertion Sort Algorithm will take between n^1.5 to n^2 steps to complete.


"""
Page 64: Using Big O Notation
"""

"""
Page 65: Merge Sort
"""

# Merge Sort is an algorithm that is much quicker than insertion sort.
def merging(left,right):
    newcabinet = []
    while(min(len(left),len(right)) > 0):
        if left[0] > right[0]:
            to_insert = right.pop(0)
            newcabinet.append(to_insert)
        elif left[0] <= right[0]:
            to_insert = left.pop(0)
            newcabinet.append(to_insert)
    if(len(left) > 0):
        for i in left:
            newcabinet.append(i)
    if(len(right) > 0):
        for i in right:
            newcabinet.append(i)
    return(newcabinet)

left = [1,3,4,4,5,7,8,9]
right = [2,4,6,7,8,8,10,12,13,14]
newcab = merging(left,right)
print("Merge-Sort Filing Cabinet: " + str(newcab))

"""
Sorting a Single List into Multiple Lists
"""

# The code below relies on Python's list indexing syntax to split whatever cabinet we want to sirt into a left cabinet and right cabinet.
import math

def merge_sort_two_elements(cabinet):
    newcabinet = []
    if(len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = cabinet[:math.floor(len(cabinet)/2)]
        right = cabinet[math.floor(len(cabinet)/2):]
        newcabinet = merging(left,right)
    return(newcabinet)

# Next  let's write a function that can sort a list that has four elements into two sublists, call our merge sort function that works on two-element lists on each of those two sublists, and then merge the two sorted lists together to get a sorted result with four elements:

def mergesort_four_elements(cabinet):
    newcabinet = []
    if(len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = merge_sort_two_elements(cabinet[:math.floor(len(cabinet)/2)])
        right = merge_sort_two_elements(cabinet[math.floor(len(cabinet)/2):])
        newcabinet = merging(left,right)
    return(newcabinet)

cabinet = [2,6,4,1]
newcabinet = mergesort_four_elements(cabinet)

# THe above code is not efficient because you have to rewrite the code every time the list size changes. But we can use recursion to make scalable code:

def mergesort(cabinet):
    newcabinet = []
    if(len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = mergesort(cabinet[:math.floor(len(cabinet)/2)])
        right = mergesort(cabinet[math.floor(len(cabinet)/2):])
        newcabinet = merging(left,right)
    return(newcabinet)

cabinet = [4,1,3,2,6,3,18,2,9,7,3,1,2.5,-9]
newcabinet = mergesort(cabinet)
print(newcabinet)

# We can put our Merge Sort code together:

"""Completed Merge Sort Algorithm"""
def merging(left,right):
    newcabinet = []
    while(min(len(left),len(right)) > 0):
        if left[0] > right[0]:
            to_insert = right.pop(0)
            newcabinet.append(to_insert)
        elif left[0] <= right[0]:
            to_insert = left.pop(0)
            newcabinet.append(to_insert)
    if(len(left) > 0):
        for i in left:
            newcabinet.append(i)
    if(len(right) > 0):
        for i in right:
            newcabinet.append(i)
    return(newcabinet)

def mergesort(cabinet):
    newcabinet = []
    if(len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = mergesort(cabinet[:math.floor(len(cabinet)/2)])
        right = mergesort(cabinet[math.floor(len(cabinet)/2):])
        newcabinet = merging(left,right)
    return(newcabinet)

cabinet = [4,1,3,2,6,3,18,2,9,7,3,1,2.5,-9]
newcabinet = mergesort(cabinet)
print(newcabinet)


"""
Page 70: Sleep Sort
"""

# Sleep sort is where each element to insert itself directly into the Array, but only after a pause in proportion to the metric its being sorted on. From a programming perspective, these pauses are called "Sleeps".

import threading
from time import sleep

def sleep_sort(i):
    sleep(i)
    global sortedlist
    sortedlist.append(i)
    return(i)

items = [2,4,5,2,1,7]
sortedlist = []
# ignore_result = [threading.Thread(target = sleep_sort, args = (i,)).start() \for i in items] 

"""
From Sorting to Searching
"""

# Binary Search is a quick and effective method for searching for an element in a sorted list.
# You guess the midpoint of a sorted list, if it is too high, you eliminate the lower half and vice versa. Then you guess the midpoint of what is left and so on. It's recursive.

import math
sortedcabinet = [1,2,3,4,5,6,7,8,9,10]

def binarysearch(sorted_cabinet,looking_for):
    guess = math.floor(len(sorted_cabinet)/2)
    upperbound = len(sorted_cabinet)
    lowerbound = 0
    while(abs(sorted_cabinet[guess] - looking_for) > 0.0001):
        if(sorted_cabinet[guess] > looking_for):
            upperbound = guess
            guess = math.floor((guess + lowerbound)/2)
        if(sorted_cabinet[guess] < looking_for):
            lowerbound = guess
            guess = math.floor((guess + upperbound)/2)
    return(guess)

print(binarysearch(sortedcabinet,8))

"""
Applications of Binary Search
"""

# Binary Search can be used to debug code, search through databases for information, etc...
# They can also be used to invert functions:
def inverse_sin(number):
    domain = [x * math.pi/10000 - math.pi/2 for x in list(range(0,10000))]
    the_range = [math.sin(x) for x in domain]
    result = domain[binarysearch(the_range,number)]
    return(result)

print(inverse_sin(0.9))
