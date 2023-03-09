"""
Chapter 09: Machine Learning

    Machine learning refers to a broad range of methods. But the common goal is to find patterns in data and using them to make predictions. 

    We will discuss a method called decision trees to predict a person's level of happiness based on some of their personal characteristics.

"""

# Decision Trees are diagrams that have a branching structure resembling a tree. They are like flowcharts with yes/no questions. Let's design a decision tree for happiness.

# First Download the dataset:
    # https://bradfordtuckfield.com/ess.csv

# Read the dataset:
import pandas as pd
ess = pd.read_csv('ess.csv')

# See how many rows and columns in the dataset:
print(ess.shape)


# Use Pandas's slicing functions to look at the first five answers to the happy question.
print(ess.loc[:,'happy'].head())

# We can do the sme with the sclmeet variable:
print(ess.loc[:,'sclmeet'].head())

# For our analysis we can restrict the responses to only full responses; no missing answers. Responses are from a 1-10. So a number way outside the range means that no answer was given.

ess = ess.loc[ess['sclmeet'] <= 10,:].copy()
ess = ess.loc[ess['rlgdgr'] <= 10,:].copy()
ess = ess.loc[ess['hhmmb'] <= 50,:].copy()
ess = ess.loc[ess['netusoft'] <= 5,:].copy()
ess = ess.loc[ess['agea'] <= 200,:].copy()
ess = ess.loc[ess['health'] <= 5,:].copy()
ess = ess.loc[ess['happy'] <= 10,:].copy()
ess = ess.loc[ess['eduyrs'] <= 100,:].copy().reset_index(drop=True)


"""
PAGE 169: Splitting Our Data

"""

# Binary Splitting: Compare happiness of people with active vs inactive social lives
import numpy as np
social = list(ess.loc[:,'sclmeet'])
happy = list(ess.loc[:,'happy'])
low_social_happiness = [hap for soc,hap in zip(social,happy) if soc <= 5]
high_social_happiness = [hap for soc,hap in zip(social,happy) if soc > 5]

meanlower = np.mean(low_social_happiness)
meanhigher = np.mean(high_social_happiness)

print("Unsocial People Happiness Score: ", str(meanlower))
print("Social People Happiness Score: ", str(meanhigher))

# We see from the data that increased sociability correlates to higher social happiness of about .6/10. So now we have the first part of our decision tree which is split based on sociability levels. 

"""
Page 171: Smarter Splitting

We split high vs low sociability levels at 5/10. However this split might not be accurate. In order to measure the accuracy of this split, we can use the Sum of Errors. The sum of errors is basically the difference between the model's prediction and the actual value. The lower the sum of errors, the better the model's prediction.
"""

# Simple way for Sum of Errors:
lowerrors = [abs(lowhappy - meanlower) for lowhappy in low_social_happiness]
higherrors = [abs(highhappy - meanhigher) for highhappy in high_social_happiness]

total_error = sum(lowerrors) + sum(higherrors)

# Code to test out different splits and their sum of errors:

def get_splitpoint(allvalues,predictedvalues):
    lowest_error = float('inf')
    best_split = None
    best_lowermean = np.mean(predictedvalues)
    best_highermean = np.mean(predictedvalues)
    for pctl in range(0,100):
        split_candidate = np.percentile(allvalues, pctl)
        loweroutcomes = [outcome for value,outcome in zip(allvalues,predictedvalues) if value <= split_candidate]
        higheroutcomes = [outcome for value,outcome in zip(allvalues,predictedvalues) if value > split_candidate]

        if np.min([len(loweroutcomes),len(higheroutcomes)]) > 0:
            meanlower = np.mean(loweroutcomes)
            meanhigher = np.mean(higheroutcomes)

            lowerrors = [abs(outcome - meanlower) for outcome in loweroutcomes]
            highererrors = [abs(outcome - meanhigher) for outcome in higheroutcomes]

            total_error = sum(lowerrors) + sum(highererrors)

            if total_error < lowest_error:
                best_split = split_candidate
                lowest_error = total_error
                best_lowermean = meanlower
                best_highermean = meanhigher
    return(best_split,lowest_error,best_lowermean,best_highermean)

# Let's test it for hhmb, or the number of household members:
allvalues = list(ess.loc[:,'hhmmb'])
predictedvalues = list(ess.loc[:,'happy'])
print(get_splitpoint(allvalues,predictedvalues))


"""
Page 173: Choosing Splitting Variables

How do we determine which variables to split at each branching node? It'd the one that leads to the smallest error.
"""
def get_split(data,variables,outcome_variable):
    best_var = ''
    lowest_error = float('inf')
    best_split = None
    predictedvalues = list(data.loc[:,outcome_variable])
    best_lowermean = -1
    best_highermean = -1
    for var in variables:
        allvalues = list(data.loc[:,var])
        splitted = get_splitpoint(allvalues,predictedvalues)

        if(splitted[1] < lowest_error):
            best_split = splitted[0]
            lowest_error = splitted[1]
            best_var = var
            best_lowermean = splitted[2]
            best_highermean = splitted[3]
    generated_tree = [[best_var,float('-inf'),best_split,best_lowermean],[best_var,best_split,float('inf'),best_highermean]]

    return(generated_tree)

# Let's run the get_split function on the data:
variables = ['rlgdgr','hhmmb','netusoft','agea','eduyrs']
outcome_variable = 'happy'
print(get_split(ess,variables,outcome_variable))
# Running this code we get some output. The first list tells us we are looking at a branch based on a respondent's value of netusoft(frequency of internet usage). The last element of each list shows an estimated happiness rating.

"""
Page 175: Adding Depth

We need to add some depth to the tree or more variables to make a decision on at a branch. To do that we have to specify the depth we want to reach in the tree.

To do this, we make additions to our getsplit() function 
"""
maxdepth = 3
def get_split_with_depth(depth,data,variables,outcome_variable):
    best_var = ''
    lowest_error = float('inf')
    best_split = None
    predictedvalues = list(data.loc[:,outcome_variable])
    best_lowermean = -1
    best_highermean = -1
    for var in variables:
        allvalues = list(data.loc[:,var])
        splitted = get_splitpoint(allvalues,predictedvalues)

        if(splitted[1] < lowest_error):
            best_split = splitted[0]
            lowest_error = splitted[1]
            best_var = var
            best_lowermean = splitted[2]
            best_highermean = splitted[3]
    generated_tree = [[best_var,float('-inf'),best_split,[]],[best_var,best_split,float('inf'),[]]]

    if depth < maxdepth:
        splitdata1=data.loc[data[best_var] <= best_split, :]
        splitdata2=data.loc[data[best_var] > best_split, :]
        if len(splitdata1.index) > 10 and len(splitdata2.index) > 10:
            generated_tree[0][3] = get_split_with_depth(depth + 1,splitdata1,variables,outcome_variable)
            generated_tree[1][3] = get_split_with_depth(depth + 1,splitdata2,variables,outcome_variable)
        else:
            depth = maxdepth + 1
            generated_tree[0][3] = best_lowermean
            generated_tree[1][3] = best_highermean
    else:
        generated_tree[0][3] = best_lowermean
        generated_tree[1][3] = best_highermean

    return(generated_tree)


# Let's run this code:
variables = ['rlgdgr','hhmmb','netusoft','agea','eduyrs']
outcome_variable = 'happy'
maxdepth = 2
print(get_split_with_depth(0,ess,variables,outcome_variable))


# Code to predict a person's level of happiness based on certain factors:
def get_prediction(observation,tree):
    j = 0
    keepgoing = True
    prediction = -1
    while(keepgoing):
        j = j + 1
        variable_tocheck = tree[0][0]
        bound1 = tree[0][1]
        bound2 = tree[0][2]
        bound3 = tree[1][2]
        if observation.loc[variable_tocheck] < bound2:
            tree = tree[0][3]
        else:
            tree = tree[1][3]
        if isinstance(tree,float):
            keepgoing = False
            prediction = tree
    return(prediction)


# Next we create a loop that goes through any portion of our dataset and gets any tree's happiness prediction for that portion.
predictions = []
outcome_variable = 'happy'
maxdepth = 4
thetree = get_split_with_depth(0,ess,variables,outcome_variable)
for k in range(0,30):
    observation = ess.loc[k,:]
    predictions.append(get_prediction(observation,thetree))

print(predictions)

# Finally we can check how these predictions compare to the actual happiness ratings to see what the total error rate is:
predictions = []

for k in range(0,len(ess.index)):
    observation = ess.loc[k,:]
    predictions.append(get_prediction(observation,thetree))
    
ess.loc[:,'predicted'] = predictions
errors = abs(ess.loc[:,'predicted'] - ess.loc[:,'happy'])
print(np.mean(errors))


"""
PAGE 179: The Problem of Overfitting

You can get a problem with overfitting your test data. This means that you get very low error rates when testing on your preexisting data. But on a different set of data, you do very poorly.
This tends to happen when we seek error rates that are too low that the machine learning algorithm will create relationships that shouldn't exist in real life.

To address this issue, we can split our data into training and testing sets. We create our decision tree on the training data and then test with the test data.
"""

# Code to define training and testing sets:
import numpy as np
np.random.seed(518)
ess_shuffled = ess.reindex(np.random.permutation(ess.index)).reset_index(drop=True)
training_data = ess_shuffled.loc[0:37000, :]
test_data = ess_shuffled.loc[37000:,:].reset_index(drop=True)

# Let's generate a decision tree with only the training data:
thetree = get_split_with_depth(0,training_data,variables,outcome_variable)

# Finally, we check the average error rate on the test data which wasn't used to train the model:
predictions = []

for k in range(0,len(test_data.index)):
    observation = test_data.loc[k,:]
    predictions.append(get_prediction(observation,thetree))
    
test_data.loc[:,'predicted'] = predictions
errors = abs(test_data.loc[:,'predicted'] - test_data.loc[:,'happy'])
print(np.mean(errors))


"""
PAGE 181: Improvements and Refinements

There might be a problem with overfitting data if you make your decision tree with too much depth. Vice versa you can underfit data with not enough depth.

"""

"""
PAGE 182: Random Forest

Random Forests are better then Decision Trees. Decision trees have a tendency to overfit and have high error rates.

The Random Forest Model is a collection of decision tree models. Each decision tree was created with some randomness incorporated in its creation.

THe randomization occurs in two places: Training dataset is randomized. Next variables used to build a tree are randomized.

We take all the predictions of the decision trees and average them together.

"""