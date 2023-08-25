"""
Chapter 10: Artificial Intelligence

The AI system that we will build will be able to play Dots and Boxes, a simple but nontrivial game.

1. First we will start by draeing the game board.
2. Next we'll build functions to keep score as games are in progress.
3. Next we'll generate game trees that represent all possible combinations of moves that can be played in a given game.
4. Finally we'll introduce a minmax algorithm.
"""

# Useless Comment

# PAGE 187: Drawing the Board

import matplotlib.pyplot as plt
from matplotlib import collections as mc
def drawlattice(n,name):
    for i in range(1,n+1):
        for j in range(1,n+1):
            plt.plot(i,j,'o',c = 'black')
    plt.savefig(name)

# We create a 5x5 Black Lattice
drawlattice(5, 'lattice.png')

"""
PAGE 188: Representing Games
"""

# Games can be represented by an ordered list of such lines:
games = [[(1,2),(1,1),(3,3),(4,3)],[(1,5),(2,5)],[(1,2),(2,2)],[(2,2),(2,1)],[(1,1),(2,1)],[(3,4),(3,3)],[(3,4),(4,4)]]


# Let's create a function to both draw the gameboard and to create all the lines on the game:


def drawgame(n,name,game):
    colors2 = []
    for k in range(0,len(game)):
        if k%2 == 0:
            colors2.append('red')
        else:
            colors2.append('blue')
    lc = mc.LineCollection(game,colors = colors2,linewidths = 2)
    fig, ax = plt.subplots()
    for i in range(1,n+1):
        for j in range(1,n+1):
            plt.plot(i,j,'o',c='black')
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.savefig(name)


# Call the function:
drawgame(5, 'game.png', games)

"""
PAGE 189: Scoring Games
"""

# Function to count the number of squares that appear on the gameboard:
def squarefinder(game):
    countofsquares = 0
    for line in game:
        parallel = False
        left = False
        right = False
        if line[0][1] ==line[1][1]:
            if [(line[0][0],line[0][1]-1),(line[1][0],line[1][1] - 1)] in game:
                parallel = True
            if [(line[0][0],line[0][1]),(line[1][0]-1,line[1][1] - 1)] in game:
                left = True
            if [(line[0][0]+1,line[0][1]),(line[1][0],line[1][1] - 1)] in game:
                right = True
            if parallel and left and right:
                countofsquares += 1
    return(countofsquares)

# Function that finds the score of an in-progress game:

def score(game):
    score = [0,0]
    progress = []
    squares = 0
    for line in game:
        progress.append(line)
        newsquares = squarefinder(progress)
        if newsquares > squares:
            if len(progress)%2 == 0:
                score[1] = score[1] + 1
            else:
                score[0] = score[0] + 1
        squares=newsquares
    return(score)

"""
Page 192: Building our Tree

Game trees are different from Decision Trees in that Game Trees describe every possible future whereas Decision Trees enable classifications and predictions based on characteristics
"""

# Create a Game Tree:
allpossible = []

gamesize = 5

for i in range(1,gamesize + 1):
   for j in range(2,gamesize + 1):
       allpossible.append([(i,j),(i,j-1)])

for i in range(1,gamesize):
    for j in range(1,gamesize + 1):
        allpossible.append([(i,j),(i+1,j)])
 
 # Remove moves that cannot be played anymore as the game progresses:
for move in allpossible:
    if move in games:
        allpossible.remove(move)


# Function to generate a game tree, record game score along with the moves, and secondly appends a blank list to keep a place for children:

def generate_tree(possible_moves,depth,maxdepth,game_so_far):
    tree = []
    for move in possible_moves:
        move_profile = [move]
        game2 = game_so_far.copy()
        game2.append(move)
        move_profile.append(score(game2))
        if depth < maxdepth:
            possible_moves2 = possible_moves.copy()
            possible_moves2.remove(move)
            move_profile.append(generate_tree(possible_moves2,depth + 1,maxdepth,game2))
        else:
            move_profile.append([])
        tree.append(move_profile)
    return(tree)

# Call the function:

allpossible = [[(4,4),(4,3)],[(4,1),(5,1)]]
thetree = generate_tree(allpossible,0,1,[])
print(thetree)

"""
PAGE 195: Winning a Game

    The algorithm that we will choose for a winning strategy is called Mini-Max. We are trying to maximize our score in the game and our opponent is trying to minimize it.

"""

# Function that uses minimax to find the best move in a game tree:
import numpy as np
def minimax(max_or_min,tree):
    allscores = []
    for move_profile in tree:
        if move_profile[2] == []:
            allscores.append(move_profile[1][0] - move_profile[1][1])
        else:
            move,score = minimax((-1) * max_or_min,move_profile[2])
            allscores.append(score)
    newlist = [score * max_or_min for score in allscores]
    bestscore = max(newlist)
    bestmove = np.argmax(newlist)
    return(bestmove,max_or_min * bestscore)


# Before calling the minimax function, let's define the game and get all the possible moves using the exact code as befor:

allpossible = []

games = [[(1,2),(1,1),(3,3),(4,3)],[(1,5),(2,5)],[(1,2),(2,2)],[(2,2),(2,1)],[(1,1),(2,1)],[(3,4),(3,3)],[(3,4),(4,4)]]

gamesize = 5

for i in range(1,gamesize + 1):
   for j in range(2,gamesize + 1):
       allpossible.append([(i,j),(i,j-1)])

for i in range(1,gamesize):
    for j in range(1,gamesize + 1):
        allpossible.append([(i,j),(i+1,j)])

for move in allpossible:
    if move in games:
        allpossible.remove(move)

# Next generate a complete game tree that extends to a depth of 3 levels:

thetree = generate_tree(allpossible,0,3,games)

# Now that we have the game tree, we can call the minimax function:
move,score = minimax(1,thetree)

# And finally, check the best moves as follows:
print(thetree[move][0])


"""
PAGE 199: Adding Enhancements

Our AI that we built is kind of slow. To improve speed, we can do something called Pruning which is to remove branches from a tree that are exceptionally poor.

Other ways to improve the AI is to allow it to work with different rules or games.

Other ways are:
    1. Reinforcement Learning: AI plays against itself to get better
    2. Monte Carlo Methods: Generate Random futures
    3. Neural Networks

Despite these advanced techniques of refinement, the core workhorses for strategic AI are tree search and minimax

"""
