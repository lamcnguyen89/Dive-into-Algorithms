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


