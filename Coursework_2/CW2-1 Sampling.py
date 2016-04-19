
# coding: utf-8

# # Algorithms 202: Coursework 2 Task 1: Random Sampling

# Group-ID: 32

# Group members: Jonathan Muller, Louis de Beaumont, Jonny Goff-White

# ## Objectives

# The aim of this coursework is to enhance your algorithmic skills by developing algorithms from textual, non-formal descriptions. You are asked to show that you can:
# 
# - implement three different random sampling algorithms
# - compare those algorithms using visual representations based on image sampling
# 
# This notebook *is* the coursework. It contains cells with function definitions that you will need to complete. You will submit this notebook as your coursework.

# ## Preliminaries: helper functions

# Here we define a collection of functions that will be useful for the rest of the coursework. You'll need to run this cell to get started.

# In[3]:

get_ipython().magic('matplotlib inline')
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.spatial import cKDTree as KDTree
from matplotlib import pyplot as plt
from PIL import Image

def load_image(path):
    return np.array(Image.open(str(path)))

def sample_colors(image, sample_points):
    r"""
    Sample RGB colour values from an image of shape (w, h, 3)
    at floating point (x, y) sample points.
    """
    r = map_coordinates(image[..., 0], sample_points.T)
    g = map_coordinates(image[..., 1], sample_points.T)
    b = map_coordinates(image[..., 2], sample_points.T)
    return np.vstack((r, g, b)).T

def indices_of_pixels(image):
    r"""(x, y) index values for each pixel in an image.
    """
    return np.indices(image.shape[:2]).reshape([2, -1]).T

def closest_index(sample_points, indices):
    r"""
    Find the nearest sample_point at a given index
    (along with the distance to the point). Input is
    an array of sample_points and an array of indicies to
    test at. Output is array of indices and distances.
    """
    kdtree = KDTree(sample_points)
    distance, index = kdtree.query(indices)
    return index, distance

def resample_image(image, sample_points):
    # for each (floating point) sample_point extract the
    # RGB colour value of the image at that location
    colors = sample_colors(image, sample_points)
    # get all (x, y) index values for each pixel in
    # the image
    indices = indices_of_pixels(image)
    # for every pixel (each index) find the nearest sample
    # point (and the distance, but we don't need it here)
    c_index,_ = closest_index(sample_points, indices)
    # map the closest indexes to colour values - reshape
    # the resulting RGB array back into the original image 
    # shape.
    return colors[c_index].reshape(image.shape)


# ## Task 1: Random Sampling

# In this task you are asked to implement `uniform_sampling`, `best_candidate_sampling` and `poison_disc_sampling`. Additionally, you will need to implement visualising techniques that can be used to compare the output of the three different random sampling algorithms.
# 
# Complete the below function definitions in the provided skeleton code. Do not change the names of the functions or their arguments.

# ### 1a. Implement `uniform_sampling`

# The `uniform_sampling` function should produce `n_samples` sample points randomly distributed over the sample domain. See lecture slides for details and pseudo-code. Hint: The sample domain defined by the width and the height of the image can be obtained by `image.shape[:2]`.

# In[7]:

import random

def uniform_sampling(image, n_samples):
    samples = []
    width = image.shape[0]
    height = image.shape[1]
    
    for i in range(n_samples):
        samples.append(uniform_sample(width, height))
        
    return np.array(samples)

def uniform_sample(width, height):
    x = random.random() * width
    y = random.random() * height
    
    return (x, y)


# ### 1b. Implement `best_candidate_sampling`

# The `best_candidate_sampling` function should produce `n_samples` sample points randomly distributed over the sample domain. See lecture slides for details and pseudo-code. Hint: The `best_candidate` function here corresponds to the BEST-CANDIDATE-SAMPLE function in the slides, which generates a single new sample.

# In[8]:

import math

def best_candidate_sampling(image, n_samples, n_candidates):
    samples = []
    for i in range(n_samples):
        samples.append(best_candidate(image, samples, n_candidates))
        
    return np.array(samples)

def distance(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    xsqrd = math.pow(x2-x1, 2)
    ysqrd = math.pow(y2-y1, 2)
    
    return math.sqrt(xsqrd+ysqrd)

def find_closest(samples, point):
    x = point[0]
    y = point[1]
    
    if not samples:
        return point
    
    closest = samples[0][0], samples[0][1]
    
    for sample in samples:
        if (distance(sample, (x,y)) < distance(closest, (x,y))):
            closest = sample
            
    return closest
        
def best_candidate(image, samples, n_candidates):
    width = image.shape[0]
    height = image.shape[1]
    best_candidate = (0,0)
    best_distance = 0
    
    for i in range(n_candidates):
        c = uniform_sample(width, height)
        d = distance(find_closest(samples, c), c)
        if (d > best_distance):
            best_distance = d
            best_candidate = c
            
    return best_candidate


# ### 1c. Implement `poison_disc_sampling`

# The `poison_disc_sampling` function should produce sample points randomly distributed over the sample domain with a minimum distance of `radius`. See lecture slides and [Bridson's original paper](https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf) for details.

# In[53]:

import math

# Find point is spherical annulus.
def point_in_annulus(point, radius):
    a = random.uniform(radius, 2*radius)
    b = random.uniform(0, 2*math.pi)
    
    return (point[0] + a*math.cos(b), point[1] + a*math.sin(b))

# Returns true iff the point is within the image.
def in_image(point, image):
    width = image.shape[0]
    height = image.shape[1]
    
    return (0 <= point[0] < width) and (0 <= point[1] < height)

# Returns true iff point is near existing samples.
def not_near(background_grid, point, radius):
    for p in background_grid:
        for i in p:
            if (i != -1 and distance(i, point) < radius):
                return False
    return True

def poison_disc_sampling(image, radius, n_candidates):
    samples = []
    active_list = []
    width = image.shape[0]
    height = image.shape[1]
    cell_size = radius / math.sqrt(2)
    grid_width = math.ceil(width / cell_size)
    grid_height = math.ceil(height / cell_size)
    
    background_grid = []
    
    for i in range(grid_height):
        background_grid.append([-1] * grid_width)
    
    initial_sample = uniform_sample(width, height)
    initial_index1 = int(initial_sample[0] / cell_size)
    initial_index2 = int(initial_sample[1] / cell_size)
    
    background_grid[initial_index1][initial_index2] = initial_sample
    samples.append(initial_sample)
    active_list.append(initial_sample)
    
    while active_list: # while active_list not empty
        random_index = random.randint(0, len(active_list) - 1)
        random_point = active_list[random_index]
        
        for i in range(n_candidates):
            point = point_in_annulus(random_point, radius)
            
            if in_image(point, image) and not_near(background_grid, point, radius):
                grid_index1 = int(point[0] / cell_size)
                grid_index2 = int(point[1] / cell_size)
                background_grid[grid_index1][grid_index2] = point
                samples.append(point)
                active_list.append(point)
                
        active_list.remove(random_point)
    
    return np.array(samples)


# ### Image sampling

# The following cells are for testing and visualisation of your sampling methods.

# #### Load test image

# In[5]:

# image= load_image('./brain.png')
# image = load_image('./face.png')
# image = load_image('./lighthouse.png')
image = load_image('./mandrill.png')
# image = load_image('./parrots.png')
# image = load_image('./starry-night.png')
# image = load_image('./synth.png')
plt.imshow(image)


# #### Generate random samples

# In[63]:

#less samples - good for debugging
# samples_uni = uniform_sampling(image, 685)
# samples_bc  = best_candidate_sampling(image, 685, 10)
# samples_pd  = poison_disc_sampling(image, 15, 30)

#more samples - looks better
samples_uni = uniform_sampling(image, 2000)
samples_bc = best_candidate_sampling(image, 2000, 10)
samples_pd = poison_disc_sampling(image, 10, 30)


# #### Plot samples

# In[64]:

fig, axs = plt.subplots(1, 3, figsize=(18,5))
axs[0].scatter(samples_uni[:,0], samples_uni[:,1], marker='x')
axs[0].set_title('Uniform Sampling')
axs[1].scatter(samples_bc[:,0], samples_bc[:,1], marker='x')
axs[1].set_title('Best-Candidate Sampling')
axs[2].scatter(samples_pd[:,0], samples_pd[:,1], marker='x')
axs[2].set_title('Poison-Disc Sampling')
plt.show()


# #### Resample images using random samples

# In[65]:

image_uni = resample_image(image, samples_uni)
image_bc = resample_image(image, samples_bc)
image_pd = resample_image(image, samples_pd)


# #### Plot images

# In[66]:

fig, axs = plt.subplots(1, 4, figsize=(15,3))
axs[0].imshow(image)
axs[0].set_title('Original')
axs[1].imshow(image_uni)
axs[1].set_title('Uniform Sampling')
axs[2].imshow(image_bc)
axs[2].set_title('Best-Candidate Sampling')
axs[3].imshow(image_pd)
axs[3].set_title('Poison-Disc Sampling')
plt.show()


# ### 1d. Implement `distance_map` for colouring image points according to their distance to sample points

# The `distance_map` function should generate an image where each pixel intensity is set to the distance to the closest sample point. Hint: You might want to check out the `resample_image` function provided above for guidance.

# In[70]:

def distance_map(image, sample_points):
    indices = indices_of_pixels(image)
    _, distance = closest_index(sample_points, indices)
    return distance.reshape(image.shape[:2])


# #### Generate distance maps using random samples

# In[71]:

distmap_uni = distance_map(image, samples_uni)
distmap_bc = distance_map(image, samples_bc)
distmap_pd = distance_map(image, samples_pd)


# #### Plot distance maps

# In[72]:

fig, axs = plt.subplots(1, 3, figsize=(18,5))
axs[0].imshow(distmap_uni)
axs[0].set_title('Uniform Sampling')
axs[1].imshow(distmap_bc)
axs[1].set_title('Best-Candidate Sampling')
axs[2].imshow(distmap_pd)
axs[2].set_title('Poison-Disc Sampling')
plt.show()


# In[ ]:



