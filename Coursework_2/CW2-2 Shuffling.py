
# coding: utf-8

# # Algorithms 202: Coursework 2 Task 2: Random Shuffling

# Group-ID: 32

# Group members: Jonathan Muller, Louis de Beaumont, Jonny Goff-White

# ## Objectives

# The aim of this coursework is to enhance your algorithmic skills by developing algorithms from textual, non-formal descriptions. You are asked to show that you can:
# 
# - implement different random shuffling algorithms
# - compare those algorithms using visual representations
# 
# This notebook *is* the coursework. It contains cells with function definitions that you will need to complete. You will submit this notebook as your coursework.

# ## Preliminaries: helper functions

# Here we define a collection of functions that will be useful for the rest of the coursework. You'll need to run this cell to get started.

# In[2]:

get_ipython().magic('matplotlib inline')
from matplotlib import pyplot as plt
import random
import numpy as np


# ## Task 2: Random Shuffling

# In this task you are asked to implement `random_sort_shuffle` and `fisher_yates_shuffle`. Additionally, you will need to implement visualisation techniques that can be used to compare the output of the different random shuffling algorithms.
# 
# Complete the below function definitions in the provided skeleton code. Do not change the names of the functions or their arguments.

# ### 2a. Implement `random_sort_shuffle`

# The `random_sort_shuffle` function should follow the idea of using a random comparator for sorting the array `a`. See lecture slides for details. You might want to search the web for hints on how to use Python's sort function with a custom comparator. (`functools.cmp_to_key` will be very useful)

# In[3]:

from functools import cmp_to_key

def random_sort_shuffle(a):
    cmp_key = cmp_to_key(random_comparator)
    return sorted(a, key=cmp_key)

def random_comparator(x, y):
    return random.randint(-1, 1)


# ### 2b. Implement `fisher_yates_shuffle`

# The `fisher_yates_shuffle` function should implement one of the two versions of Fisher-Yates shuffle as outlined in the lecture slides.

# In[4]:

def fisher_yates_shuffle(a):
    n = len(a)
    for i in range(n):
        j = random.randint(i, n-1)
        # Swap a[i] and a[j]
        swap(a, i, j)
    return a

def swap(a, i, j):
    a[i], a[j] = a[j], a[i]
    return a


# ### 2c. Implement buggy `fisher_yates_shuffle`

# Check out the lecture slides for two common bugs that are found in Fisher-Yates shuffle implementations. Implement two buggy versions of `fisher_yates_shuffle` for later analysis.

# In[5]:

def fisher_yates_shuffle_buggy1(a):
    n = len(a)
    for i in range(n-1, 0, -1):
        j = random.randint(0, i-1)
        swap(a, i, j)
    return a

def fisher_yates_shuffle_buggy2(a):
    n = len(a)
    for i in range(n-1, 0, -1):
        j = random.randint(0, n-1)
        swap(a, i, j)
    return a


# ### 2d. Perform empirical analysis

# The empirical analysis is aiming to detect bias in the shuffle algorithms implemented above. You should build a swap matrix for each shuffle algorithm by executing them multiple times on suitable sequences with a fixed number of elements that allow you to track the random shuffles of elements.
# 
# You can visualise the swap matrices using the `plt.imshow(matrix)` function (see also the notebook on Random Sampling on the use of `plt.imshow`).
# 
# Plot the swap matrices and add a few lines of discussion about what you can conclude from the visualisations about possible bias in the different algorithms.

# In[13]:

def make_long_list(n):
    output = [0] * n
    for i in range(n):
        output[i] = i
    return output

test_list = make_long_list(20)

def swap_matrix_analysis(l, f, n):
    swap_matrix = np.zeros((len(l), len(l)))
    
    for i in range(n):
        list_a = list(f(list(l)))
        
        for j in range(len(l)):
            for k in range(len(l)):
                elem = list_a[j]
                index = l.index(elem)
                if list_a[j] == l[k]:
                    swap_matrix[j][k] += 1
    
    return swap_matrix

fig, axs = plt.subplots(1, 4, figsize=(18, 5))
axs[0].imshow(swap_matrix_analysis(test_list, random_sort_shuffle, 10000))
axs[0].set_title('Random sort shuffle')
axs[1].imshow(swap_matrix_analysis(test_list, fisher_yates_shuffle, 10000))
axs[1].set_title('Fisher-Yates shuffle')
axs[2].imshow(swap_matrix_analysis(test_list, fisher_yates_shuffle_buggy1, 10000))
axs[2].set_title('Buggy Fisher-Yates shuffle #1')
axs[3].imshow(swap_matrix_analysis(test_list, fisher_yates_shuffle_buggy2, 10000))
axs[3].set_title('Buggy Fisher-Yates shuffle #2')


# In the above graphs, dark blue represents no swaps have occured for the element, and red represents a high number of swaps have occured for the element.
# 
# The random shuffle sort shows a bias, since there is a concentrated number of swaps down the diagonal. This shows that elements are either swapped with themselves or with adjacent elements the most. Random shuffle rarely swaps the furthest two elements, and most frequently swaps the first (0th) element with itself (shown by the red mark in the top left corner).
# 
# The Fisher-Yates shuffle shows the least bias of all four algorithms. No patterns or symmetries in the visualisation stand out. On repeated and successive runs, the Fisher-Yates shuffle produces different outputs, further suggesting minimal bias.
# 
# The first bug containing Fisher-Yates shuffle shows a strong bias to not swapping elements with themselves, shown by the deep blue diagonal running across the visualisation.
# 
# The second bug containing Fisher-Yates shuffle shows that very few of the elements, except for (0,0), are ever swapped. There are few swaps between same elements, and far fewer between different elements. The vast majority of swaps that have occurred have occurred between (0,0) and itself, suggesting a very strong bias.

# In[ ]:



