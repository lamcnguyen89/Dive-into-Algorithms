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

