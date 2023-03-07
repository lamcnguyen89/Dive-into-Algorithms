
# Chapter 07: Geometry

# In this chapter we'll use a geometric algorithm to solve the postmaster problem.

"""
Page 126: The Postmaster Problem

The postmaster problem is how to decide which houses in an area should be served by a particular post office in an area. There are multiple post offices located in a city, so you want to figure out the most efficient routes that the mail delivery trucks operating out of a particular post office should take in order to most efficiently serve the citizens in the city.

There are many factors that might be considered for deciding which houses are served by a particular post office. But the one factor we will use in this chapter is proximity to a particular PO. Each PO will serve the houses closest to it.

To computionally solve this problem, we can add straight lines through a map of the city to divide it up into regions that each PO will then serve. This sort of map that is divided into triangles is called a Voronoi Diagram.

"""

# Page 128: Triangles 101

# The triangles can be thought of as a series of 3 points. Each point will be described by an X and Y coordinate on a 2D Graph:

triangle = [[0.2,0.8],[0.5,0.2],[0.8,0.7]]


# Helper function to bring together 3 disparate points into a list that describes a triangle:

def points_to_triangle(point1,point2,point3):
    triangle = [list(point1),list(point2),list(point3)]
    return(triangle)

# Function to turn points into a series of lines that can later be used to plot a triangle:

def gen_lines(listpoints,itinerary):
    lines = []
    for j in range(len(itinerary)-1):
        lines.append([listpoints[itinerary[j]],listpoints[itinerary[j+1]]])
    return(lines)

# Code to plot the lines on a graph:

import pylab as pl
from matplotlib import collections as mc

def plot_triangle_simple(triangle, thename):
    fig, ax = pl.subplots()

    xs = [triangle[0][0],triangle[1][0],triangle[2][0]]
    ys = [triangle[0][1],triangle[1][1],triangle[2][1]]

    itin = [0,1,2,0]

    thelines = gen_lines(triangle, itin)

    lc = mc.LineCollection(gen_lines(triangle,itin),linewidths=2)

    ax.add_collection(lc)

    ax.margins(0.1)
    pl.scatter(xs,ys)
    pl.title(str(thename))
    pl.savefig(str(thename)+'.png')
    pl.show()
    pl.close()

# Show the plot:
plot_triangle_simple(points_to_triangle((0.2,0.8),(0.5,0.2),(0.8,0.7)),'Triangle 1')


# It will also come in handy to to have a function that calculates the distance between any two points:
import math
def get_distance(point1,point2):
    distance = math.sqrt((point1[0]-point2[0])**2+(point1[1] - point2[1])**2)
    return(distance)


"""
PAGE 132: Finding the Circumcenter of a Triangle

The Circumcenter: Where the center of each line on a triangle has a line that passes perpendicular through it.
These perpendicular lines meet inside of the triangle. And that point where those three perpendicular lines meet is the circumcenter.
"""

# Function to find circumcenter and circumradius(The radius around of the circumcircle. The circumcircle has the circumcenter at it's center point and the vertexes of the triangle are on this circumcircle.)

def triangle_to_circumcenter(triangle):
    x,y,z = complex(triangle[0][0],triangle[0][1]), complex(triangle[1][0],triangle[1][1]), complex(triangle[2][0],triangle[2][1])
    w = z - x
    w /= y - x
    c = (x-y) * (w-abs(w)**2)/2j/w.imag - x
    radius = abs(c + x)
    return((0 - c.real,0 - c.imag),radius)

# The code above is complex and in this book, the deep technical details aren't discussed.


# Now let's update the plot_triangle function to also incorporate the circumcenter:
def plot_triangle(triangles, centers, radii, thename):
    fig, ax = pl.subplots()
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    for i in range(0,len(triangles)):
        triangle = triangles[i]
        center = centers[i]
        radius = radii[i]
        itin = [0,1,2,0]
        thelines = gen_lines(triangle, itin)
        xs = [triangle[0][0],triangle[1][0],triangle[2][0]]
        ys = [triangle[0][1],triangle[1][1],triangle[2][1]]

        lc = mc.LineCollection(gen_lines(triangle,itin),linewidths=2)

        ax.add_collection(lc)
        ax.margins(0.1)
        pl.scatter(xs,ys)
        pl.scatter(center[0],center[1])

        circle = pl.Circle(center, radius, color = 'b', fill = False)

        ax.add_artist(circle)

    pl.title(str(thename))
    pl.savefig(str(thename)+'.png')
    pl.show()
    pl.close()


# Let's call the function with a list of triangels that we define:
triangle1 = points_to_triangle((0.1,0.1),(0.3,0.6),(0.5,0.2))
center1,radius1 = triangle_to_circumcenter(triangle1)
triangle2 = points_to_triangle((0.8,0.1),(0.7,0.5),(0.8,0.9))
center2,radius2 = triangle_to_circumcenter(triangle2)
plot_triangle([triangle1,triangle2],[center1,center2],[radius1,radius2],'Two Triangles One Graph')


"""
PAGE 134: Delaunay Triangulation

This algorithm takes a set of points as its input and returns a set of triangles as its output. This process is called triangulation. Again, triangulation is a process where you take a bunch of points and connect them together in such a way that triangle shapes are formed in a network. For example a square can be divided into 2 triangles. An Octagon can be turned into triangles and so on...

The previous points_to_triangle function is the most simple triangulation algorithm, but it is limited in that it only works if we give it exactly 3 input points.

But what if we have 7 points or 10 points or more? We need a more complex algorithm.

Also note that a collection of points can be triangulated in many ways. And as the number of points increase, the number of different ways of triangulating these points can be staggering.

There are a few different triangulation algorithms. We will be using the Bowyer-Watson Algorithm to take a set of inputs and output a Delauney Triangulation.

"""


"""
A Delauney Triangulation (DT) aims to avoid narrow, sliver triangles. It tends to output triangles that are somewhat close to equilateral.

Equilateral triangles have relatively small circumcircles while sliver triangles have large circumcircles. So in this algorithm, we can use a filter to remove triangles with circumcircles above a certain size.

# For example, we can have rule stating that no point can be inside the circumcircle of any other triangle.

"""


def gen_delaunay(points):
    delaunay = [points_to_triangle([-5,-5],[-5,10],[10,-5])]
    number_of_points = 0

    while number_of_points < len(points): # For every point, it creates a list of invalid triangles: Every triangle that's in the DT whose circumcircle  includes the point we're currently looking at.
        point_to_add = points[number_of_points]
        
        delaunay_index = 0

        invalid_triangles = [] # Removes those invalid triangles from the DT and creates a collectionof poinrs using each point that was in those invalid triangles.
        while delaunay_index < len(delaunay):
            circumcenter,radius = triangle_to_circumcenter(delaunay[delaunay_index])
            new_distance = get_distance(circumcenter, point_to_add)
            if(new_distance < radius):
                invalid_triangles.append(delaunay[delaunay_index])
            delaunay_index += 1

        points_in_invalid = [] # Then, using those points, it adds new triangles that follow the rules of Delaunay triangulations.
        for i in range(0,len(invalid_triangles)):
            delaunay.remove(invalid_triangles[i])
            for j in range(0,len(invalid_triangles[i])):
                points_in_invalid.append(invalid_triangles[i][j])
        points_in_invalid = [list(x) for x in set(tuple(x) for x in points_in_invalid)]

        for i in range(0, len(points_in_invalid)): # It accomplishes this incrementally, using exactly the code that we have already introduced. Finally it returns a delaunay, a list containing the collection of trianglesthat constitutes our DT.
            for j in range(i+1,len(points_in_invalid)):
                # Count the number of times both of these are in the bad triangles
                count_occurences = 0
                for k in range(0, len(invalid_triangles)):
                    count_occurences += 1 * (points_in_invalid[i] in invalid_triangles[k]) * (points_in_invalid[j] in invalid_triangles[k])
                if(count_occurences == 1):
                    delaunay.append(points_to_triangle(points_in_invalid[i],points_in_invalid[j], point_to_add))

        number_of_points += 1

    return(delaunay)
        


# In the following code, we specify a number for N and this generates random points (x and y values). Then we zip the x and y values, put them together in a list, pass them to our gen_delaunay() function and get back a full DT:

N = 15
import numpy as np
np.random.seed(5201314)
xs = np.random.rand(N)
ys = np.random.rand(N)
points = zip(xs,ys)
listpoints = list(points)
the_delaunay = gen_delaunay(listpoints) # We can use this delaunay to generate a Voronoi diagram.


"""
PAGE 143: From Delaunay to Voronoi

We can generate a Voronoi Diagram by following this Algorithm:

1. Find the DT of a set of points.
2. Take the circumcenter of every triangle in the DT.
3. Draw lines connecting the circumcenters of all triangles in the DT that share an edge.

"""

# Before Creating the Voronoi Diagram, let's add some extra functionality to the plotting function:

def plot_triangle_circum(triangles, centers,plotcircles,plotpoints,plottriangles,plotvoronoi,plotvpoints, thename):
    fig, ax = pl.subplots()
    ax.set_xlim([-0.1,1.1])
    ax.set_ylim([-0.1,1.1])

    lines = []
    for i in range(0,len(triangles)):
        triangle = triangles[i]
        center = centers[i][0]
        radius = centers[i][1]
        itin = [0,1,2,0]
        thelines = gen_lines(triangle, itin)
        xs = [triangle[0][0],triangle[1][0],triangle[2][0]]
        ys = [triangle[0][1],triangle[1][1],triangle[2][1]]

        lc = mc.LineCollection(gen_lines(triangle,itin),linewidths=2)
        if(plottriangles):
            ax.add_collection(lc)
        if(plotpoints):
            pl.scatter(xs,ys)

        ax.margins(0.1)

        if(plotvpoints):
            pl.scatter(center[0],center[1])
        
        circle = pl.Circle(center, radius, color = 'b', fill = False)
        if(plotcircles):
            ax.add_artist(circle)

        if(plotvoronoi):
            for j in range(0, len(triangles)):
                commonpoints = 0
                for k in range(0, len(triangles[i])):
                    for n in range(0,len(triangles[j])):
                        if triangles[i][k] == triangles[j][n]:
                            commonpoints += 1
                if commonpoints == 2:
                    lines.append([list(centers[i][0]),list(centers[j][0])])

        
        lc = mc.LineCollection(lines,linewidths = 1)

        ax.add_collection(lc)

    pl.title(str(thename))
    pl.savefig(str(thename)+'.png')
    pl.show()
    pl.close()



# We're almost ready to call this plotting function and see our final Voronoi Diagram. However we first need to get the circumcenters of every triangle in our DT. We can create an empty list called circumceters and append the circumcenter of every triangle in our DT:

circumcenters = []
for i in range(0,len(the_delaunay)):
    circumcenters.append(triangle_to_circumcenter(the_delaunay[i]))



# Finally we call the plotting function, specifying that we want to draw the Voronoi Boundaries:
plot_triangle_circum(the_delaunay,circumcenters,False,True,False,True,False, 'Final Voronoi Diagram')


# Graph with all the parameters set to True:
plot_triangle_circum(the_delaunay,circumcenters,True,True,True,True,True, 'Everything and Voronoi Diagram')


"""
PAGE 144: Summary

Voronoi Diagrams can be used for many purposes such as Water pumps, post office placement, crystal structures, bomb blast radius planning, etc...

"""
