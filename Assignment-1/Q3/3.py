#Imports
import numpy as np
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as img
from math import sqrt, log
from scipy.ndimage import gaussian_filter, generic_laplace
from skimage.feature import peak_local_max
from skimage.feature.blob import _prune_blobs
import time

#Functions
def gaussian_laplace(input, sigma):
    
    input = np.asarray(input)

    def derivative2(input, axis, output, mode, cval, *extra_arguments, **extra_keywords):
        order = [0] * input.ndim
        order[axis] = 2
        return gaussian_filter(input, sigma, order)

    return generic_laplace(input, derivative2, extra_arguments=(sigma,))

def laplacian_of_gaussian(image, min_sigma=1, max_sigma=15, num_sigma=10, k=2):
    
    image = image.astype(np.float64)

    sigma_values = np.linspace(min_sigma, max_sigma, num_sigma)
    #sigma_values = np.array([2 ** i for i in range(0,10)])

    gaussian_laplace_images = [-gaussian_laplace(image, s) * s ** 2 for s in sigma_values]
    image_cube = np.dstack(gaussian_laplace_images)

    local_maxima = peak_local_max(image_cube, threshold_abs=.2, footprint=np.ones((3, 3, 3)), threshold_rel=0.0, exclude_border=False)

    if local_maxima.size == 0:
        return np.empty((0,3))

    lm = local_maxima.astype(np.float64)
    lm[:, 2] = sigma_values[local_maxima[:, 2]]

    return _prune_blobs(lm, .5)

def difference_of_gaussian(image, min_sigma=1, max_sigma=15, sigma_ratio=1.6):

    image = image.astype(np.float64)

    # k such that min_sigma*(sigma_ratio**k) > max_sigma
    k = int(log(float(max_sigma) / min_sigma, sigma_ratio)) + 1

    # a geometric progression of standard deviations for gaussian kernels
    sigma_values = np.array([min_sigma * (sigma_ratio ** i) for i in range(k + 1)])

    gaussian_images = [gaussian_filter(image, s) for s in sigma_values]

    dog_images = [(gaussian_images[i] - gaussian_images[i + 1]) for i in range(k)]
    image_cube = np.dstack(dog_images)

    local_maxima = peak_local_max(image_cube, threshold_abs=0.1, footprint=np.ones((3, 3, 3)), threshold_rel=0.0, exclude_border=False)
   
    if local_maxima.size == 0:
        return np.empty((0,3))
   
    lm = local_maxima.astype(np.float64)
    lm[:, 2] = sigma_values[local_maxima[:, 2]]
  
    return _prune_blobs(lm, .5)

#Code
image = cv2.imread('/Users/yashsrivastava/Documents/Files/CV-Assignments/Assignment-1/Images/Input/HW1_Q3/butterfly.jpg',0)

start = time.time()
blobs_log = laplacian_of_gaussian(image)
end_log = str(time.time() - start)
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

start = time.time()
blobs_dog = difference_of_gaussian(image, max_sigma=30)
end_dog = str(time.time() - start)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_list = [np.empty((0,3)),blobs_log, blobs_dog]
colors = ['blue','red', 'yellow']
titles = ['Original Image','Laplacian of Gaussian' + '\n Time Taken: ' + end_log , 'Difference of Gaussian' + '\n Time Taken: ' + end_dog]
sequence = zip(blobs_list, colors, titles)

fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True, subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

for idx, (blobs, color, title) in enumerate(sequence):
    ax[idx].set_title(title)
    ax[idx].imshow(image, interpolation='nearest', cmap = 'gray')
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax[idx].add_patch(c)
    ax[idx].set_axis_off()

plt.tight_layout()
plt.show()
