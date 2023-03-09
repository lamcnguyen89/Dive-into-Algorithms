"""
Chapter 10: Artificial Intelligence

The AI system that we will build will be able to play Dots and Boxes, a simple but nontrivial game.

1. First we will start by draeing the game board.
2. Next we'll build functions to keep score as games are in progress.
3. Next we'll generate game trees that represent all possible combinations of moves that can be played in a given game.
4. Finally we'll introduce a minmax algorithm.
"""

# PAGE 187: Drawing the Board

import matplotlib.pyplot as plt
from matplotlib import collections as mc
def drawlattice(n,name):
    for i in range(1,n+1):
        for j in range(1,n+1):
            plt.plot(i,j,'o',c = 'black')
    plt.savefig(name)