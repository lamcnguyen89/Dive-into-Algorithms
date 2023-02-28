"""
Chapter 05: Pure Math
"""

"""
Continued Fractions
"""
# An example of a continued fraction is the Golden Ratio of 1.618.
# Another is e used in logarithms.

# A continued fraction consists of sums and reciprocals nested in multiple layers. They can be finite and terminate after several layers or they can continue forever

"""
Page 82: Algorithm for Expressing Fractions as Continued Fractions
"""
import math
def continued_fraction(x,y,length_tolerance):
    output = []
    big = max(x,y)
    small = min(x,y)
    while small > 0 and len(output) < length_tolerance:
        quotient = math.floor(big/small)
        output.append(quotient)
        new_small = big % small
        big = small
        small = new_small
    return(output)

print(continued_fraction(105,33,10))


# Function to check that a continued fraction correctly express the number we're interested in by converting it to a decimal:

def get_number(continued_fraction):
    index = -1
    number = continued_fraction[index]

    while abs(index) < len(continued_fraction):
        next = continued_fraction[index - 1]
        number = 1/number + next
        index -= 1
    return(number)

"""
Page 86: From Decimals to Continued Fractions
"""

def continued_fraction_decimal(x,error_tolerance,length_tolerance):
    output = []
    first_term = int(x)
    leftover = x - int(x)
    output.append(first_term)
    error = leftover
    while error > error_tolerance and len(output) < length_tolerance:
        next_term = math.floor(1/leftover)
        leftover = 1/leftover - next_term
        output.append(next_term)
        error = abs(get_number(output) - x)
    return(output)

print(continued_fraction_decimal(1.4142135623730951,0.00001,100))

"""
Page 89: Square Roots
"""
# How are Square Roots calculated in electronic calculators?

"""
The Babylonian Algorithm
"""
# The Babulonian Algorithm is used to calculate the square root of a number.
    # 1. Make a guess, y, for the value of the square root of x.
    # 2. Calculate z = x/y
    # 3. Find the average of z and y. This average is your new value of y, or your new guess for the value of the square root of x.
    # 4. Repeat steps 2 and 3 until y^2 - x is sufficiently small.

# Python Code for the Babulonian Algorithm:
def square_root(x,y,error_tolerance):
    our_error = error_tolerance * 2
    while(our_error > error_tolerance):
        z = x/y
        y = (y + z)/2
        our_error = y**2 - x
    return(y)

print(square_root(5,1,.000000001))

""" Random Number Generators"""

"""
# There is a constant need for for random numbers:
    1. Video Games depend on them to keep gamers surprised by game characters' positions and movements.
    2. Several of the most powerful machine learning methods(including random forests and neural networks) rely on random selections to function properly.
    3. Powerful statistical methods like bootstrapping use randomness to make a static dataset better resemble the chaotic world.
    4. Corporations and research scientists perform A/B tests that rely heavily on randomly assigning subjects to conditions so that the conditions' effects can be properly compared.

"""

# Computers cannot be truly random, so through algorithms we create Pseudorandomness.


"""
Page 92: Linear Congruential Generators

In this algorithm we take 3 natural numbers n1,n2,n3 and use the formula:

    next = (previous * n1 + n2) mod n3
"""

# Code for the Linear Congruential Generator:
def next_random(previous, n1,n2,n3):
    the_next = (previous * n1 + n2) % n3
    return(the_next)

# Code for Creating a list of Pseudo random numbers:
def list_random(n1,n2,n3):
    output = [1]
    while len(output) <=n3:
        output.append(next_random(output[len(output) - 1],n1,n2,n3))
    return(output)

print(list_random(29,23,32))

""" Page 95: The Diehard Tests for Randomness"""

# The diehard tests are a collection of 12 tests that test for the randomness of a set of numbers in different ways

# One of these tests is the Overlapping Sums Test which takes the entire lists of random numbers and finds sums of sections of consecutive numbers on the list THe sums should follow a bell curve pattern:

def overlapping_sums(the_list,sum_length):
    length_of_list = len(the_list)
    the_list.extend(the_list)
    output = []
    for n in range(0, length_of_list):
        output.append(sum(the_list[n:(n + sum_length)]))
    return(output)

# We can run this test on a new random list with the code below:

import matplotlib.pyplot as plt
overlap = overlapping_sums(list_random(211111,111112,300007),12)
plt.hist(overlap, 20, facecolor = 'blue', alpha=0.5)
plt.title('Results of the Overlapping Sums Test')
plt.xlabel('Sum of Elements of OVerlapping Consecutive Sections of List')
plt.ylabel('Frequency of Sum')
plt.show()

"""Page 97: Linear Feedback Shift Registers"""
 # Linear Feedback Shift Registers are more random and less predictable then Pseudorandom Number Generators.

 # LFSRs were designed with computer architecture in mind unlike PNRGs. THey involve shifting bits or 1s and 0s.

 # Algorithm for LFSRs:
def feedback_shift(bits):
    xor_result = (bits[1] + bits[2] % 2)
    output = bits.pop()
    bits.insert(0,xor_result)
    return(bits,output)

# Code to use LSFR to generate a list of random numbers: 
def feedback_shift_list(bits_this):
    bits_output = [bits_this.copy()]
    random_output = []
    bits_next = bits_this.copy()
    while(len(bits_output) < 2**len(bits_this)):
        bits_next,next = feedback_shift(bits_next)
        bits_output.append(bits_next.copy())
        random_output.append(next)
    return(bits_output, random_output)

"""
LSFRs are used to generate pseudorandom numbers in a variety of applications, including white noise.

The most widely used PNRG in practice today is the Mersenne Twister, which is a modified, generalized feedback shift register- a much more convoluted form of a LSFR.
"""