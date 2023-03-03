
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
    pl.savefig(str(thename)+'.png')
    pl.show()
    pl.close()

# Show the plot:
plot_triangle_simple(points_to_triangle((0.2,0.8),(0.5,0.2),(0.8,0.7)),'triangle1')


# It will also come in handy to to have a function that calculates the distance between any two points:
import math
def get_distance(point1,point2):
    distance = math.sqrt((point1[0]-point2[0])**2+(point1[1[1] - point2[1]])**2)
    return(distance)