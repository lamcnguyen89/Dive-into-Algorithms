"""
Chapter 03: Maximizing and Minimizing
"""

# Maximizing and minimizing are very frequently used functions. They are used for maximizizing profit, minimizing expenses, minimizing errors, miinimum discomfort, minimum loss, etc...

"""
Page 36: Setting Tax Rates
"""

# If you set the tax rate too low, a government won't be able to get all the taxes it could extract from its citizens. If you set the tax rate too high, citizens will cheat taxes, leave the country or just not have the capital to start businesses which will shrink the economy and ultimately shrink the GDP that can be taxed... Decreasing the the tax revenue. 

# A bunch of theoretical economists have created this function for tax revenues:

import math
def revenue(tax):
    return(100 * (math.log(tax+1) - (tax - 0.2)**2 + 0.04))

# Generate a curve based off the above tax revenue formula. This plot shows the revenues (in billions of your countryy;s currenccy) that your team of economists expects for each tax rate between 0 and 1 (where 1 represents 100%).

import matplotlib.pyplot as plt
xs = [x/1000 for x in range(1001)]
ys = [revenue(x) for x in xs]
plt.plot(xs,ys)
plt.title('Tax Rates and Revenue')
plt.xlabel('Tax Rate')
plt.ylabel('Revenue')
plt.show()

# Add a point to show the 70% Tax Rate for a country.
import matplotlib.pyplot as plt
xs = [x/1000 for x in range(1001)]
ys = [revenue(x) for x in xs]
plt.plot(xs,ys)
current_rate = 0.7
plt.plot(current_rate,revenue(current_rate), 'ro')
plt.title('Tax Rates and Revenue')
plt.xlabel('Tax Rate')
plt.ylabel('Revenue')
plt.show()

# You will see from the above code that a 70 percent tax rate is not maximizing the tax revenue. The tax rate is too high so we have to decrease the rate. 

"""
Finding the Minima and Maxima involve taking the derivative of a curve. You want to find where the rate of change of the curve is equal to zero. To do this, you can use Calculus to solve for an equation. 

However you can use an algorithm where you take incremental steps through the curve and manually calculate the derivative 
"""

"""
Page 39: Algorithm for finding the Minima and Maxima:

1. Start with the current_rate and a step_size.
2. Calculate the derivative of the function you are trying to maximize at the current_rate.
3. Add step_size * revenue_derivative(current_rate) to the current rate, to get a new current_rate.
4. Repeat steps 2 and 3.
"""

# The step that is missing in the above algorithm is a stopping point. With each step you will never truly get to a derivative/rate-ofchange of zero. But we can set a threshold value of when to stop the algorithm. We can also set the maximum number of iterations:



def revenue_derivative(tax):
    return(100 * (1/(tax +1) - 2 * (tax - 0.2)))

current_rate = 0.7
step_size = 0.001
threshold = .0001
iterations = 0
maximum_iterations = 100000
keep_going = True
while(keep_going):
    rate_change = step_size * revenue_derivative(current_rate)
    current_rate = current_rate + rate_change

    if(abs(rate_change) < threshold):
        keep_going = False
        print("Optimal Tax Rate: " + str(100 * current_rate)+"%")

    if(iterations >=maximum_iterations):
        keep_going = False
        print("Optimal Tax Rate: " + str(100*current_rate)+"%")

    iterations = iterations + 1


"""
Page 42: The Problem of Local Extrema
"""

# There is a problem when finding the minima and maxima. That is that there is the possibility of multiple points along the curve where the rate of change is equal to zero or where a value reaches a maximum and drop multiple times along the curve. Or where a value reaches the minimum point and then rises again multiple times. 

# How does one account foe this fact that you can have multiple points of rises and falls and then falls and rises?

# How do you find the GLOBAL maxima and minima, not just the local ones?

# Consider the Education and Lifetime Income problem that is might be described with this formula below:

import math
def income(edu_years):
    return(math.sin((edu_years - 10.6) * (2 * math.pi/4)) + (edu_years -11)/2)

# Let's plot the Education and Life Income Curve:
import matplotlib.pyplot as plt
xs = [11 + x/100 for x in list(range(901))]
ys = [income(x) for x in xs]
plt.plot(xs,ys)
current_edu = 12.5
plt.plot(current_edu, income(current_edu), 'ro')
plt.title('Education and Life Income')
plt.xlabel('Years of Education')
plt.ylabel('Life Income')
plt.show()

# The code below is Using Gradient Ascent to find a Maxima for the optimal amount of education to maximumize income. The problem with this code is that it can only find local maxima. It can't take into the fact that if you keep getting more educated, overtime, even though your income will drop initially, you will eventually make more and more money over the long term.

def income_derivative(edu_years):
    return(math.cos((edu_years - 10.6) * (2 * math.pi/4)) + 1/2)

threshold = 0.0001
maximum_iterations = 100000

current_education = 12.5
step_size = 0.001

keep_going = True
iterations = 0
while(keep_going):
    education_change = step_size * income_derivative(current_education)
    current_education = current_education + education_change
    if(abs(education_change) < threshold):
        keep_going = False
        print("Optimal Education: " + str(current_education)+"%")
    if(iterations >= maximum_iterations):
        keep_going = False
        print("Optimal Education:" + str(current_education) + "%")
    iterations = iterations + 1

# One of the ways to combat the issue of local maxima is to randomly pick values along the curve to start Gradient Ascent. This randomness increases the chances that the code won't terminate prematurely at a local maxima.

"""
Page 45: Finding the Minima
"""

# Finding the minima is almost just like finding the maxima. 
# The difference is that we flip the equation we are working it by multiplying the equation by -1.

# Let's try this with the Revenue function from above:

def revenue_flipped(tax):
    return(-1 * revenue(tax))

# Let's plot the flipped revenue curve:
import matplotlib.pyplot as plt
xs = [x/1000 for  x in range(1001)]
ys = [revenue_flipped(x) for x in xs]
plt.plot(xs,ys)
plt.title('The Tax/Revenue Curve - Flipped')
plt.xlabel('Current Tax Rate')
plt.ylabel('Revenue - Flipped')
plt.show()

# Then you can do gradient ascent on the flipped function and get the minima.

# Another method is to do gradient descent algorithm. It's the same method but we move in the opposite direction.

def revenue_flipped_derivative(tax):
    return(-1*(100 * (1/(tax +1) - 2 * (tax - 0.2))))

current_rate = 0.7
step_size = 0.001
threshold = .0001
iterations = 0
maximum_iterations = 100000
keep_going = True
while(keep_going):
    rate_change = step_size * revenue_flipped_derivative(current_rate)
    current_rate = current_rate - rate_change

    if(abs(rate_change) < threshold):
        keep_going = False
        print("Minimum Tax Rate: " + str(100 * current_rate)+"%")

    if(iterations >=maximum_iterations):
        keep_going = False
        print("Minimum Tax Rate: " + str(100*current_rate)+"%")

    iterations = iterations + 1



"""
Page 48: When not to use an Algorithm:
"""

# Gradient Ascent/Descent works under certain conditions:
    # There is a mathematical function to work with.
    # Knowledge of where we currently are.
    # An unequivocal goal to maximize the function.
    # Ability to alter where we are.

# Alot of the time in real life, no mathematical functions exist
# Other times we are in situations that can't be reasonably changed.
# Other times it isn't appropriate to coldly seek to maximize or minimize things due to ethical reasons.
