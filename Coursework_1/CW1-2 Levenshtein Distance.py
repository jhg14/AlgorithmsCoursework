
# coding: utf-8

# # Algorithms 202: Coursework 1 Task 2: Levenshtein Distance

# Group-ID: 32

# Group members: Jonathan Muller, Louis de Beaumont, Jonny Goff-White

# # Objectives

# The aim of this coursework is to enhance your algorithmic skills by mastering the divide and conquer and dynamic programming strategies. You are asked to show that you can:
# 
# - implement a dynamic programming problem
# 
# This notebook *is* the coursework. It contains cells with function definitions that you will need to complete. You will submit this notebook as your coursework.
# 
# The comparisons of different algorithms involve textual descriptions and graphical plots. For graphing you will be using [matplotlib](http://matplotlib.org/index.html) to generate plots. [This tutorial](http://matplotlib.org/index.html) will be useful to go through to get you up to speed. For the textual descriptions you may wish to use [LaTeX](http://en.wikipedia.org/wiki/LaTeX) in-line like $\mathcal{O}(n\log{}n)$. Double click this cell to reveal the required markup - and [see here](http://texblog.org/2014/06/24/big-o-and-related-notations-in-latex/) for useful guidance on producing common symbols used in asymptotic run time analysis.

# # Preliminaries: helper functions

# Here we define a collection of functions that will be useful for the rest of the coursework. You'll need to run this cell to get started.

# In[3]:

# so our plots get drawn in the notebook
get_ipython().magic('matplotlib inline')
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path
from sys import maxsize
from time import clock
from urllib.request import urlretrieve

# a timer - runs the provided function and reports the
# run time in ms
def time_f(f):
    before = clock()
    f()
    after = clock()
    return after - before

# we can get a word list from here - we download it once
# to 'wordlist.txt' and then reuse this file.
url = 'http://www.doc.ic.ac.uk/~bglocker/teaching/wordlist.txt'
if not Path('wordlist.txt').exists():
    print("downloading word list...")
    urlretrieve(url, 'wordlist.txt')
    print('acquired word list.')
    
with open('wordlist.txt') as f:
    # here we use a *set* comprehension - just
    # like we've done with lists in the past but
    # the result is a set so each element is
    # guaranteed to be unique.
    # https://docs.python.org/3/tutorial/datastructures.html#sets
    # note that you can loop over a set just like you would a list
    wordlist = {l.strip() for l in f.readlines()}
    print("loaded set of words into 'wordlist' variable")


# ## Task 2: Levenshtein Distance

# ### 2a. Implement `levenshtein_distance`

# Complete the below definition for `levenshtein_distance`. Do not change the name of the function or it's arguments. 
# 
# 
# Hints:
# 
# - You are given access to numpy (`np`). Numpy is the crown jewel of the scientific Python community - it provides a multidimensional array (`np.array()`) which can be very convenient to solve problems involving matrices.

# In[5]:

def levenshtein_distance(x, y):
    m = len(x)
    n = len(y)
    
    # Initialise matrix of zeros with lengths of given words
    d = np.zeros(shape=[m+1,n+1])
    
    for i in range(1, m+1):
        d[i,0] = i
        
    for j in range(n+1):
        d[0,j] = j
        
    for j in range(1, n+1):
        for i in range(1, m+1):
            c = 0 if x[i-1] == y[j-1] else 1
            d[i,j] = min(d[i-1,j] + 1, d[i,j-1] + 1, d[i-1,j-1] + c)
            
    return d[m,n]


# Use this test to confirm your implementation is correct.

# In[4]:

print(levenshtein_distance('sunny', 'snowy') == 3)
print(levenshtein_distance('algorithm', 'altruistic') == 6)
print(levenshtein_distance('imperial', 'empirical') == 3)
print(levenshtein_distance('weird', 'wired') == 2)


# ### 2b. Find the minimum levenshtein distance

# Use your `levenshtein_distance` function to find the `closest_match` between a `candidate` word and an iterable of `words`. Note that if multiple words from `words` share the minimal edit distance to the `candidate`, you should return the word which would come first in a dictionary. 
# 
# As a concrete example, `zark` has an edit distance of 1 with both `ark` and `bark`, but you would return `ark` as it comes lexicographically before `bark`.
# 
# Your function should return a tuple of two values - first the closest word match, and secondly the edit distance between this word and the candidate.
# 
# ```python
# closest, distance = closest_match('zark', ['ark', 'bark', ...])
# assert closest == 'ark'
# assert distance == 1
# ```

# In[1]:

def closest_match(candidate, words):
    closest = ""
    
    # Set sentinel
    distance = float("inf")
    
    # Iterate through words list and check if distance is less than max value
    for word in words:
        d = levenshtein_distance(candidate, word)
        if d < distance:
            distance = d
            closest = word
            
    return closest, distance


# Run the below cell to test your implementation

# In[6]:

# A one liner that queries closest_match and then prints the result
print_closest = lambda w, wl: print('{}: {} ({})'.format(w, *closest_match(w, wl)))

print_closest('zilophone', wordlist)
print_closest('inconsidrable', wordlist)
print_closest('bisamfiguatd', wordlist)


# **Discuss in a few lines the running time of `closest_match`. Can you propose any ideas for making this faster? (Only discuss those in words, no need to do any implementations, unless you want to.)**

# The running time of `closest_match` is $\mathcal{O}(n)$ multiplied by the running time of `levenshtein_distance`, which is $\mathcal{O}(mn)$ - where $m$ and $n$ are the lengths of each of the words passed in. To make this faster, we could implement a divide and conquer approach for `levenshtein_distance` which would reduce the number of operations performed on the matrix and hence reduce the complexity of the `closest_match` function.
