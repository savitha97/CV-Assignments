#Imports
import matplotlib
matplotlib.use('TkAgg')
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import math

#Functions
def gaussian_filter(rows,columns,sigma):

    if rows%2==0:
        center_x = rows/2
    else:
        center_x = rows/2 + 1

    if columns%2==0:
        center_y = columns/2
    else:
        center_y = columns/2 + 1
 
    def gaussian(i,j):
        
        value = math.exp(-1.0 * ((i - center_x)**2 + (j - center_y)**2) / (2 * sigma**2))
        return value
 
    gaussian_array = np.zeros((rows,columns))

    for i in range(0,rows):
        for j in range(0,columns):
            gaussian_array[i][j] = gaussian(i,j)

    return gaussian_array
    
def LowPassFilter(image,sd):
    
    n,m = image.shape
    gaussian_matrix = gaussian_filter(n,m,sd)

    dft = np.fft.fft2(image)
    dftshift = np.fft.fftshift(dft)
    filterImage = dftshift * gaussian_matrix

    ifftshift = np.fft.ifftshift(filterImage)
    ifftImage = np.fft.ifft2(ifftshift)

    return ifftImage

def HighPassFilter(image,sd):
    
    n,m = image.shape
    gaussian_matrix = (1 - gaussian_filter(n,m,sd))

    dft = np.fft.fft2(image)
    dftshift = np.fft.fftshift(dft)
    filterImage = dftshift * gaussian_matrix

    ifftshift = np.fft.ifftshift(filterImage)
    ifftImage = np.fft.ifft2(ifftshift)

    return ifftImage

#Code
image1 = cv2.imread('/Users/yashsrivastava/Documents/Files/CV-Assignments/Assignment-1/Images/Input/HW1_Q1/cat.bmp',0) #Low Pass
image2 = cv2.imread('/Users/yashsrivastava/Documents/Files/CV-Assignments/Assignment-1/Images/Input/HW1_Q1/dog.bmp',0) #High Pass

alpha = 50
beta = .5

img1_low = LowPassFilter(image1,alpha)
img2_high = HighPassFilter(image2,beta)

plt.imshow(np.real(img1_low), cmap = 'gray')
plt.show()

plt.imshow(np.real(img2_high), cmap = 'gray')
plt.show()

image_hybrid = np.real(img1_low + img2_high)

plt.subplot(131),plt.imshow(image1, cmap = 'gray')
plt.title('Input Image (Low)'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(image2, cmap = 'gray')
plt.title('Input Image (High)'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(image_hybrid, cmap = 'gray')
plt.title('Hybrid Result'), plt.xticks([]), plt.yticks([])

plt.show()