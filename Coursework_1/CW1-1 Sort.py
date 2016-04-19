
# coding: utf-8

# # Algorithms 202: Coursework 1 Task 1: Sorting

# Group-ID: 32

# Group members: Jonathan Muller, Louis de Beaumont, Jonny Goff-White

# # Objectives

# The aim of this coursework is to enhance your algorithmic skills by mastering the divide and conquer and dynamic programming strategies. You are asked to show that you can:
# 
# - implement divide and conquer solutions for given problems
# - compare naive and advanced implementations of algorithms solving the same problem
# 
# This notebook *is* the coursework. It contains cells with function definitions that you will need to complete. You will submit this notebook as your coursework.
# 
# The comparisons of different algorithms involve textual descriptions and graphical plots. For graphing you will be using [matplotlib](http://matplotlib.org/index.html) to generate plots. [This tutorial](http://matplotlib.org/index.html) will be useful to go through to get you up to speed. For the textual descriptions you may wish to use [LaTeX](http://en.wikipedia.org/wiki/LaTeX) inline like $\mathcal{O}(n\log{}n)$. Double click this cell to reveal the required markup - and [see here](http://texblog.org/2014/06/24/big-o-and-related-notations-in-latex/) for useful guidance on producing common symbols used in asymptotic run time analysis.

# # Preliminaries: helper functions

# Here we define a collection of functions that will be useful for the rest of the coursework. You'll need to run this cell to get started.

# In[66]:

# so our plots get drawn in the notebook
get_ipython().magic('matplotlib inline')
from matplotlib import pyplot as plt
import numpy as np
from random import randint
from time import clock

# a timer - runs the provided function and reports the
# run time in ms
def time_f(f):
    before = clock()
    f()
    after = clock()
    return after - before

# remember - lambdas are just one line functions

# make us a random list length (between 1 - 2000)
rand_len = lambda max_len=2e3: randint(1, max_len)

# choose a random value for a list element (between 0 1e6)
rand_int = lambda: randint(0, 1e6)

# generate a random list of random length -
# here we use a list comprehension, a very tidy
# way of transforming lists of data
rand_list = lambda max_len=2e3: [rand_int() 
                                 for i in range(rand_len(max_len=max_len))]


# ## Task 1: Sorting

# In this task you are asked to implement `insertion_sort` and `merge_sort`. You need to perform an experimental analysis of their running time. Based on your analysis, you should implement a third sorting algorithm, `hybrid_sort`, which is similar to `merge_sort` but uses `insertion_sort` for the base case. The problem size for which the base case is invoked has to be inferred from the running time analysis.

# ### 1a. Implement `insertion_sort`

# Complete the below definition for `insertion_sort`. Do not change the name of the function or it's arguments. 
# 
# 
# Hints:
# 
# - Your sort should be in-place (i.e. it changes the input list for the caller) but you should also return the list so the function can be called as indicated below.

# In[2]:

def insertion_sort(a):
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        
        while ((i >= 0) & (a[i] > key)):
            a[i+1] = a[i]
            i = i - 1
            
        a[i+1] = key
        
    return a


# Use this test to confirm your implementation is correct.

# In[3]:

x = [2, 4, 1, 3]
print(insertion_sort(x) == [1, 2, 3, 4])


# ### 1b. Implement `merge_sort`

# Complete the below definition for `merge_sort`. Do not change the name of the function or it's arguments.
# 
# Hints:
# 
# - Your implementation should leave the input list unmodified for the caller
# - You are free to define other functions in this cell

# In[8]:

import math

def merge_sort(a):
    sortedList = list(a)
    merge_sort_helper(sortedList, sortedList)
    return sortedList
    
def merge_sort_helper(A, a):
    if len(a) > 1:
        mid = int(math.floor(len(a)/2))
        l = a[:mid]
        r = a[mid:]
        merge_sort_helper(A, l)
        merge_sort_helper(A, r)
        merge(a, l, r)

def merge(A, l, r):
    l.append(float("inf"))
    r.append(float("inf"))
    i = 0
    j = 0
    for k in range(len(A)):
        if l[i] <= r[j]:
            A[k] = l[i]
            i = i + 1
        else:
            A[k] = r[j]
            j = j + 1


# Use this test to confirm your implementation is correct.

# In[9]:

x = [2, 4, 1, 3]
print(merge_sort(x) == [1, 2, 3, 4])


# ### 1c. Analyse the running time performance of `insertion_sort` and `merge_sort`

# Draw a graph showing the run time performance of your `insertion_sort` and `merge_sort` for different lengths of random integers. Analyse the performance at the large scale ($n \approx 10^3$) and small scale ($n \approx 10$). To remove noisy measurements, you might want to repeat the analysis several times and estimate average performance for different $n$.

# In[74]:

random_lists = [rand_list() for i in range(100)]

t_avg_insertion = []
t_avg_merge = []

for i in range(0,3):
    t_insertion = []
    t_merge = []
    n = []

    for r_list in random_lists:
        t_merge.append(time_f(lambda: merge_sort(list(r_list))))
        t_insertion.append(time_f(lambda: insertion_sort(list(r_list))))
        n.append(len(r_list))
    
    if i == 0:
        t_avg_insertion = list(t_insertion)
        t_avg_merge = list(t_merge)
    else:
        for j in range(0, len(t_insertion)):
            t_avg_insertion[j] += t_insertion[j]
            t_avg_merge[j] += t_merge[j]
    
# Get average values for both sorts
for j in range(0, len(t_avg_insertion)):
    t_avg_insertion[j] /= 3
    t_avg_merge[j] /= 3
    
t_avg_insertion = merge_sort(t_avg_insertion)
t_avg_merge = merge_sort(t_avg_merge)
n = merge_sort(n)
    
plt.xlabel('n')
plt.ylabel('t/s')
plt.scatter(n, t_avg_insertion, color='red')
plt.scatter(n, t_avg_merge, color='blue')
plt.legend(['insertion_sort', 'merge_sort'], loc='upper left')


# **Now discuss your findings in a few lines in the below cell:**

# At a small scale ($n \approx 10$), the performance of `insertion_sort` is more efficient than `merge_sort`, however because the list size is so small the difference is minor. Once $n > 100$, the perfomance of `insertion_sort` can be seen to be $\mathcal{O}(n^2)$, whereas the performance of `merge_sort` is $\mathcal{O}(n\log{}n)$. Therefore the problem size for which the base case is invoked for `hybrid_sort` is when $n < 100$.

# ### 1d. Implement `hybrid_sort()`

# Implement `hybrid_sort()`, a `merge_sort()` variant which uses `insertion_sort()` for the base case. The problem size for which the base case is invoked has to be inferred from your above running time analysis.

# In[39]:

def hybrid_sort(a):
    if (len(a) < 100):
        return insertion_sort(a)
    else:
        return merge_sort(a)


# Use this test to confirm your implementation is correct.

# In[40]:

x = [2, 4, 1, 3]
print(hybrid_sort(x) == [1, 2, 3, 4])


# ### 1e. Analyse all three sorting implementations together

# Draw a graph showing the running time performance of your `insertion_sort()`, `merge_sort()` and `hybrid_sort()` for different lengths of random integers.

# In[73]:

random_lists = [rand_list() for i in range(100)]
t_insertion = []
t_merge = []
t_hybrid = []
n = []

for r_list in random_lists:
    t_insertion.append(time_f(lambda: insertion_sort(r_list)))
    t_merge.append(time_f(lambda: merge_sort(r_list)))
    t_hybrid.append(time_f(lambda: hybrid_sort(r_list)))
    n.append(len(r_list))

plt.xlabel('n')
plt.ylabel('t/s')
plt.scatter(n, t_insertion, color='red')
plt.scatter(n, t_merge, color='blue')
plt.scatter(n, t_hybrid, color='green')
plt.legend(['insertion_sort', 'merge_sort', 'hybrid_sort'], loc='upper left')


# **Now discuss your findings in a few lines in the below cell:**

# The graph with `hybrid_sort` looks extremely similar to the graph of `merge_sort`. This is expected when viewing the graph with $0 < n \leq 2000$ since the only difference is that for $n < 100$, `hybrid_sort` will have the same efficiency as `insertion_sort`. The graph shows that `hybrid_sort` is the most efficient algorithm of the three since it uses the best sorting algorithm for each $n$.
# 
# There may be some inefficiences in `hybrid_sort` because we cannot be sure around $n \approx 100$ whether `insertion_sort` or `merge_sort` is the more efficient algorithm.
