# Chapter 02: Algorithms in History
# Algorithms have been around for thousands of years.

"""
Page 14: Russian Peasant Multiplication
"""

# Implementing RPM in python:

#First Define the Variables:
n1 = 89
n2 = 18

# Create the halving column, which begins with one of the numbers we want to multiply:
halving = [n1]

# The following code is to halve n1:
import math
print(math.floor(halving[0]/2))
# You'll see the answer is 44

# We can create a loop to progressively halve an entry and use that entry as the next input to halve until the ending point requirements are met. This loop will create the halving column:

while(min(halving) > 1):
    halving.append(math.floor(min(halving)/2))


print('Halving Column:' + str(halving))

# Now we can create a loop for the doubling column:

doubling = [n2]
while(len(doubling) < len(halving)):
    doubling.append(max(doubling)*2)


print('Doubling Column:' + str(doubling))

# Page 18: Finally let's put the two columns together in a dataframe called half_double:
import pandas as pd
half_double = pd.DataFrame(zip(halving,doubling)) # Creates a table from the two Arrays in something called a dataframe that can then be manipulated.

# Page 19: Now we need to remove the rows whose entries in the halving column are even:

half_double = half_double.loc[half_double[0]%2 == 1, :] # The Colon (:) specifies that we want to select every row.

# loc is a function in pandas that allows us to select only the rows that we want.
    # In the square brackets we specify which rows and columns we want in order,seperated by a comma using the [row, column] syntax.

# Finally we take the sum of the remaining doubling entries:
answer = sum(half_double.loc[:,1])
print('Answer of ' +str(n1) + ' multiplied by ' + str(n2) + ' is equal to ' + str(answer))

"""
Page 20: Euclid's Theorem
"""

# Euclid's Algorithm is a method of finding the greatest common divisor of two numbers.

# Implementation of Euclid's Algorithm in python:

def gcd(x,y):
    larger = max(x,y)
    smaller = min(x,y)

    remainder = larger % smaller

    if(remainder == 0):
        return(smaller)
    
    if(remainder != 0):
        return(gcd(smaller,remainder))
    
"""
Page 22 Japanese Magic Square
"""

# A magic square  is an array of unique, consecutive natural numbers such that all rows, all the columns, and both the main diagonals have the same sum.


