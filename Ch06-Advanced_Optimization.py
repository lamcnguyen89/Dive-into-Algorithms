"""
Chapter 06: Advanced Optimization

"""

# The Gradient Ascent Algorithm is used for optimization.
# The problem with it is that it gets caught in local minima and maxima.
# We need a more advance algorithm that can optimize for GLOBAL maxima and minima.


"""
Page 102: The Traveling Salesman Problem

The traveling salesman problem  involves a salesman having to travel around to many cities trying to sell his stuff. But he has to find the most optimal route to save on time, gas, etc... in order to maximize profit.

"""

# First we randomly generate a map for our salesman to traverse.

import numpy as np
random_seed = 1729
np.random.seed(random_seed) # a module that takes in any number as a seed and plugs it into the pseudo-random number generator.
N = 40 # Represents the number of cities in the map.
x = np.random.rand(N)
y = np.random.rand(N)

# Next we'll zip the x values and y values together to create cities, a list containing coordinate pairs for each of our 40 randomly generated cities.
points = zip(x,y)
cities = list(points)

# Our first try at the solution is to simply visit all the cities in the order they appear on the list:
itinerary = list(range(0,N))

# In order to test out the itinerary, we first need a function will generate a collection of lines that connect all our points. After that we need to sum up the distances represented by those lines.
lines = []

# Iterate over ever city in the itinerary, adding a new line to our lines collection that connects the current city to the the city after it.
for j in range(0,len(itinerary) - 1):
    lines.append([cities[itinerary[j]], cities[itinerary[j + 1]]])