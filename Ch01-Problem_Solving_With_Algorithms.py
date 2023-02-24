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

# The trajectory of a hypothetical thrown ball, with a line segment representing the outfielder looking at the ball as it travels and line segments A an B showing the lengths whose ratio constitutes the tangent we are interested in

xs5 = [0.3, 0.3]
ys5 = [0, ball_trajectory(0.3)]
xs6 = [0.3,2]
ys6 = [0,0]
plt.title('The Trajectory of a Thrown Ball - Tangent Calculator')
plt.xlabel('Horizontal Position of the Ball')
plt.ylabel('Vertical Position of the Ball')
plt.plot(xs,ys,xs4,ys4,xs5,ys5,xs6,ys6)
plt.text(0.31,ball_trajectory(0.3)/2, 'A',fontsize=16)
plt.text((0.3 + 2)/2,0.05, 'B', fontsize=16)
plt.show()

# Page 09: Chapman's Solution to Algorithmically catching a ball is that when the catcher is standing in the correct location to catch the ball, the angle of the head tilt of the catcher as he watches the ball grows at a simple and constant rate

"""
Chapman's Algorithm for Catching a Ball:

    1. Observe the acceleration of the  tangent of the angle between the ground and your line of sight with the ball.
    2. If the acceleration is positive, step backward.
    3. If the acceleration is negative, step forward.
    4. Repeat step 1 and 2 until the catcher is standing in the correct location to catch.
    5. Catch it.
"""
"""
Algorithm: A set of instructions to produce a predefined outcome
"""