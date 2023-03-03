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

def findnearest(cities,idx,nnitinerary):
    point = cities[idx]
    mindistance = float('inf')
    minidx = -1
    for j in range(0,len(cities)):
        distance = math.sqrt((point[0] - cities[j][0])**2 + (point[1] - cities[j][1])**2)
        if distance < mindistance and distance > 0 and j not in nnitinerary:
            mindistance = distance
            minidx = j
    return(minidx)

# Function that successively finds the nearest neighbor to each city and returns a complete itinerary.

def donn(cities, N):
    nnitinerary = [0]
    for j in range(0,N-1):
        next = findnearest(cities,nnitinerary[len(nnitinerary)-1],nnitinerary)
        nnitinerary.append(next)
    return(nnitinerary)

# Plot the nearest neighbor itinerary:
plotitinerary(cities,donn(cities,N),'TSP - Nearest Neighbor', 'figures')

# Check how far the salesman had to travel using this new itinerary:
print(howfar(genlines(cities,donn(cities,N))))

# Page 111: A function that makes a small change to an itinerary, compares it to the original itinerary, and returns whichever itinary is shorter.
def perturb(cities, itinerary):
    neighborids1 = math.floor(np.random.rand() * (len(itinerary)))
    neighborids2 = math.floor(np.random.rand() * (len(itinerary)))

    itinerary2 = itinerary.copy()

    itinerary2[neighborids1] = itinerary[neighborids2]
    itinerary2[neighborids2] = itinerary[neighborids1]

    distance1 = howfar(genlines(cities,itinerary))
    distance2 = howfar(genlines(cities,itinerary2))

    itinerarytoreturn = itinerary.copy()

    if(distance1 > distance2):
        itinerarytoreturn = itinerary2.copy()
    
    return(itinerarytoreturn.copy())

# Let's call the perturb function multiple times in order to get the lowest traveling distance possible:

itinerary = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]

np.random.seed(random_seed)
itinerary_ps = itinerary.copy()
for n in range(0,len(itinerary) * 50000):
    itinerary_ps = perturb(cities, itinerary_ps)

print(howfar(genlines(cities,itinerary_ps)))

"""
Simulated Annealing

It's an optimization algorithm where you take alot of risk and are willing to deviate and go down from optimal performance at the beginning of the algorithm's execution, but as you near the end of the algorithm, you become less willing to tolerate downward performance.

This is a systematic way of breaking past local maxima/minima to make it more likely to reach the global maxima/minima.
"""

# Modified version of the perturb() function to take into account the temperature and a random draw:

def perturb_sa1(cities, itinerary, time):
    neighborids1 = math.floor(np.random.rand() * (len(itinerary)))
    neighborids2 = math.floor(np.random.rand() * (len(itinerary)))

    itinerary2 = itinerary.copy()

    itinerary2[neighborids1] = itinerary[neighborids2]
    itinerary2[neighborids2] = itinerary[neighborids1]

    distance1 = howfar(genlines(cities,itinerary))
    distance2 = howfar(genlines(cities,itinerary2))

    itinerarytoreturn = itinerary.copy()

    randomdraw = np.random.rand()
    temperature = 1/((time/1000) + 1)

    if((distance2 > distance1 and (randomdraw) < (temperature)) or (distance1 > distance2)):
        itinerarytoreturn = itinerary2.copy()
    
    return(itinerarytoreturn.copy())

# We can compare the performance of simulated annealing with the perturb search algorithm and nearest neighbor algorithm as follows:
itinerary = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
np.random.seed(random_seed)

itinerary_sa = itinerary.copy()
for n in range(0, len(itinerary) * 50000):
    itinerary_sa = perturb_sa1(cities, itinerary_sa,n)

print(howfar(genlines(cities,itinerary))) #random itinerary
print(howfar(genlines(cities,itinerary_sa))) #simulated annealing
print(howfar(genlines(cities,itinerary_ps))) #perturb search
print(howfar(genlines(cities,donn(cities,N)))) #nearest neighbor

"""
Page 118: Tuning Simulated Annealing

    Simulated Annealing is a sensitive process and needs to be tuned in order to perform the best. If it isn't tuned, it can do worse than a nearest neighbor search.
"""

# One way to add some randomness that can help the algorithm move to a global optima is to reverse the order of some of the items on the list/itinerary:
small = 10
big = 20
itinerary = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
itinerary[small:big] = itinerary[small:big][::-1]
print("Reversed Items Perturbed Itinerary: " + str(itinerary))

# Another way to perturb or add randomness is to lift one part of the data set and place it in another part of the data set:
small = 1
big = 5
itinerary = [0,1,2,3,4,5,6,7,8,9]
tempitin = itinerary[small:big]
del(itinerary[small:big])
np.random.seed(random_seed + 1)
neighborids3 = math.floor(np.random.rand() * (len(itinerary)))
for j in range(0, len(tempitin)):
    itinerary.insert(neighborids3 + j,tempitin[j])


# Page 119: We can update the perturn function to alternate between the two perturb methods discussed above.

def perturb_sa2(cities, itinerary,time):
    neighborids1 = math.floor(np.random.rand() * (len(itinerary)))
    neighborids2 = math.floor(np.random.rand() * (len(itinerary)))

    itinerary2 = itinerary.copy()

    randomdraw2 = np.random.rand()
    small = min(neighborids1,neighborids2)
    big = max(neighborids1,neighborids2)
    if(randomdraw2 >= 0.55):
        itinerary2[small:big] = itinerary2[small:big][::-1]
    elif(randomdraw2 < 0.45):
        tempitin = itinerary[small:big]
        del(itinerary2[small:big])
        neighborids3 = math.floor(np.random.rand() * (len(itinerary)))
        for j in range(0, len(tempitin)):
            itinerary2.insert(neighborids3 + j,tempitin[j])
    else:
        itinerary2[neighborids1] = itinerary[neighborids2]
        itinerary2[neighborids2] = itinerary[neighborids1]

    distance1 = howfar(genlines(cities,itinerary))
    distance2 = howfar(genlines(cities,itinerary2))

    itinerarytoreturn = itinerary.copy()

    randomdraw = np.random.rand()
    temperature = 1/((time/1000) + 1)

    if((distance2 > distance1 and (randomdraw) < (temperature)) or (distance1 > distance2)):
        itinerarytoreturn = itinerary2.copy()
    
    return(itinerarytoreturn.copy())

"""
# Page 120: Avoiding Major Setbacks

The whoel point of simulated annealing is that we need to do worse in order to do better.
However we want to avoid doing much worse off. So we change the code in the perturb function so that the code is less likely to accept an itinerary as the error increases

"""

def perturb_sa2(cities, itinerary,time):
    neighborids1 = math.floor(np.random.rand() * (len(itinerary)))
    neighborids2 = math.floor(np.random.rand() * (len(itinerary)))

    itinerary2 = itinerary.copy()

    randomdraw2 = np.random.rand()
    small = min(neighborids1,neighborids2)
    big = max(neighborids1,neighborids2)
    if(randomdraw2 >= 0.55):
        itinerary2[small:big] = itinerary2[small:big][::-1]
    elif(randomdraw2 < 0.45):
        tempitin = itinerary[small:big]
        del(itinerary2[small:big])
        neighborids3 = math.floor(np.random.rand() * (len(itinerary)))
        for j in range(0, len(tempitin)):
            itinerary2.insert(neighborids3 + j,tempitin[j])
    else:
        itinerary2[neighborids1] = itinerary[neighborids2]
        itinerary2[neighborids2] = itinerary[neighborids1]

    distance1 = howfar(genlines(cities,itinerary))
    distance2 = howfar(genlines(cities,itinerary2))

    itinerarytoreturn = itinerary.copy()

    randomdraw = np.random.rand()
    temperature = 1/((time/1000) + 1)
    
    scale = 3.5
    if((distance2 > distance1 and (randomdraw) < (math.exp(scale *(distance1-distance2)) * temperature)) or (distance1 > distance2)):
        itinerarytoreturn = itinerary2.copy()

    return(itinerarytoreturn.copy())


"""
Page 121: Allowing Resets

During the simulated annealing process, we may accidentally accept a change in our itinerary that is unequivocally bad. In this case, we need to keep track of the best itinerary we've encountered so far and allow our algorithm to reset to that best itinerary under certain conditions:
"""

def perturb_sa3(cities, itinerary,time,maxitin):
    neighborids1 = math.floor(np.random.rand() * (len(itinerary)))
    neighborids2 = math.floor(np.random.rand() * (len(itinerary)))
    global mindistance
    global minitinerary
    global minidx
    itinerary2 = itinerary.copy()

    randomdraw2 = np.random.rand()
    small = min(neighborids1,neighborids2)
    big = max(neighborids1,neighborids2)
    if(randomdraw2 >= 0.55):
        itinerary2[small:big] = itinerary2[small:big][::-1]
    elif(randomdraw2 < 0.45):
        tempitin = itinerary[small:big]
        del(itinerary2[small:big])
        neighborids3 = math.floor(np.random.rand() * (len(itinerary)))
        for j in range(0, len(tempitin)):
            itinerary2.insert(neighborids3 + j,tempitin[j])
    else:
        itinerary2[neighborids1] = itinerary[neighborids2]
        itinerary2[neighborids2] = itinerary[neighborids1]

    distance1 = howfar(genlines(cities,itinerary))
    distance2 = howfar(genlines(cities,itinerary2))

    itinerarytoreturn = itinerary.copy()

    randomdraw = np.random.rand()
    temperature = 1/((time/1000) + 1)
    
    scale = 3.5
    if((distance2 > distance1 and (randomdraw) < (math.exp(scale *(distance1-distance2)) * temperature)) or (distance1 > distance2)):
        itinerarytoreturn = itinerary2.copy()

    reset = True
    resetthresh = 0.04
    if(reset and (time - minidx) > (maxitin * resetthresh)):
        itinerarytoreturn = minitinerary
        minidx = time
    
    if(howfar(genlines(cities,itinerarytoreturn)) < mindistance):
        mindistance = howfar(genlines(cities,itinerary2))
        minitinerary = itinerarytoreturn
        minidx = time

    return(itinerarytoreturn.copy())


# Page 122: Testing Our Performance- Now we can create a function cto create global variables and then call our newest perturb() function repeatedly, eventually arriving at an itinerary with a very low traveling distance:

def siman(itinerary,cities):
    newitinerary = itinerary.copy()
    global mindistance
    global minitinerary
    global minidx
    mindistance = howfar(genlines(cities,itinerary))
    minitinerary = itinerary
    minidx = 0

    maxitin = len(itinerary) * 50000
    for t in range(0,maxitin):
        newitinerary = perturb_sa3(cities,newitinerary,t,maxitin)
    
    return(newitinerary.copy())

# Next we call our siman() function and compare its results to the results of our nearest neighbor algorithm:

np.random.seed(random_seed)
itinerary = list(range(N))
nnitin = donn(cities,N)
nnresult = howfar(genlines(cities,nnitin))
simanitinerary = siman(itinerary,cities)
simanresult = howfar(genlines(cities,simanitinerary))
print(nnresult)
print(simanresult)
print(simanresult/nnresult)
