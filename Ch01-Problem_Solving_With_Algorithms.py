# Chapter 01: Problem Solving with Algorithms

# Problems can be solved Analytically or Algorithmically with a Computer.

"""
In the following examples we will be using first an Analytic Method and then an Algorithmic Method for solving the problem of catching a ball that's flying through the air.
"""

"""The Analytic Approach to catching a ball: """

# Function for calculating the Trajectory of a ball:
def ball_trajectory(x):
    location = 10*x - 5*(x**2)
    return(location)

# Plot a hypothetical ball trajectory between the moment it is thrown (at x=0) and when it hits the ground again (at x=2)
import matplotlib.pyplot as plt
xs = [x/100 for x in list(range(201))]
ys = [ball_trajectory(x) for x in xs]
plt.plot(xs, ys)
plt.title("Trajectory of Thrown Ball")
plt.xlabel('Horizontal Position of Ball')
plt.ylabel('Vetical Position of Ball')
plt.axhline(y=0)
plt.show()

"""The Algorithmic Approach to catching a ball: (Page 05)"""

""" The algorithmic approach to catching a ball involves thinking with your neck. If you have to tilt your neck downward at negative acceleration, then you run towards the ball. If you have to tilt your neck upward at positive acceleration, then you run away from the ball. If you can tilt your neck at a constant speed with zero acceleration while watching the ball, then you are in the right position to catch the ball and you stand still.
"""

# Code plotting the trajectory of a hypothetical thrown ball, with line segments representing the outfielder looking at the ball as it travels. Some
xs2 = [0.1, 2]
ys2 = [ball_trajectory(0.1), 0]
xs3 = [0.2, 2]
ys3 = [ball_trajectory(0.2), 0]
xs4 = [0.3, 2]
ys4 = [ball_trajectory(0.3), 0]
plt.title('The Trajectory of a Thrown Ball - with Lines of Sight')
plt.xlabel('Horizontal Position of Ball')
plt.ylabel('Vertical Position of Ball')
plt.plot(xs,ys,xs2,ys2,xs3,ys3,xs4,ys4)
plt.show()
