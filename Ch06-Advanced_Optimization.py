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


print(lines)

# The complete function takes cities and itinerary as arguments and returns a collection of lines connecting each city on our list of cities in the order specified in the itinerary:

def genlines(cities, itinerary):
    lines = []
    for j in range(0,len(itinerary) - 1):
        lines.append([cities[itinerary[j]],cities[itinerary[j + 1]]])
    return(lines)


""" Page 105: Now that we have a way to generate a collction of lines between two cities, we can create a function that measures the distances along those lines.
"""

# The function below takes a list of lines as its input and outputs the sum of the lengths of every line:
import math
def howfar(lines):
    distance = 0
    for j in range(0,len(lines)):
        distance = 0
        for j in range(0,len(lines)):
            distance += math.sqrt(abs(lines[j][1][0] - lines[j][0][0])**2 + abs(lines[j][1][1] -lines[j][0][1]**2))
        return(distance)

# Now we can call both the functions; one to genertate the cities that are connected by lines and the other to measure the distance between them.
totaldistance = howfar(genlines(cities, itinerary))
print(totaldistance)

# To get a sense of what this result means, let's plot our itinerary.
import matplotlib.collections as mc
import matplotlib.pylab as pl
def plotitinerary(cities, itin,plottitle,thename):
    lc = mc.LineCollection(genlines(cities,itin),linewidths=2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.01)
    pl.scatter(x,y)
    pl.title(plottitle)
    pl.xlabel('X Coordinate')
    pl.ylabel('Y Coordinate')
    pl.savefig(str(thename) + '.png')
    pl.close()


"""Page 107: Determining the Shortest Path"""

# There are a few ways to determine the shortest path amongst the cities in the itinerary.

# The first is a brute force method where you list out all the itineraries and measure the distances. But this becomes very unfeasible due to something called combinatorial explosion. So we  have to use an algorithmic technique.


"""The Nearest Neighbor Algorithm
1. Start with the first city on the list. 
2. Choose the closest city from the first city and go to that city.
3. Then chose the closest city from the second city you have just arrived at.
4. Keep repeating until all the cities have been visited.

"""

