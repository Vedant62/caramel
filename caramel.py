#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
import subprocess
import os
from scipy import signal

#utils
def open_finder_and_select_image():
    script = """
    set file_path to POSIX path of (choose file of type {"public.image"} with prompt "Select an image:")
    return file_path
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    
    if result.returncode == 0:
        image_path = result.stdout.strip()
        print("Selected image:", image_path)
        return image_path
    else:
        print("No file selected.")
        return None
    
def open_finder_for_save():

    applescript = '''
    tell application "Finder"
        activate
        set theFolder to choose folder with prompt "Choose a destination to save the image"
    end tell
    return POSIX path of theFolder
    '''
    result = subprocess.run(["osascript", "-e", applescript], text=True, capture_output=True)
    return result.stdout.strip()

def preview_and_save(image_array):

    if len(image_array.shape)==2:
        plt.imshow(image_array, cmap='gray')
    elif len(image_array.shape)>2:
        plt.imshow(image_array) 

    plt.title("Image Preview (close to continue)")
    plt.show()


    save_image = input("Do you want to save this image? (y/n): ").strip().lower()
    if save_image == 'y':

        save_path = open_finder_for_save()
        if save_path:

            file_name = input("Enter a name for your file (without extensions): ")
            image_save_path = os.path.join(save_path, f"{file_name}.png")
            if len(image.shape)==2:
                plt.imsave(image_save_path, image_array, cmap='gray')
            else:
                plt.imsave(image_save_path, image_array)
            print(f"Image saved to: {image_save_path}")
        else:
            print("Save canceled.")
    else:
        print("Image save canceled.")

def create_gaussian_kernel(radius, sigma):
    size =  2 * radius + 1; #odd sized kernel for symmetric blur
    x,y = np.mgrid[-radius:radius+1, -radius:radius+1]

    gaussian = np.exp(-(x**2 + y**2)/( 2* sigma**2 )) #the gaussian formula 

    return gaussian/gaussian.sum()

#main functions

def invert(image):
    inverted_img = 255 - image
    return np.clip(inverted_img, 0, 255).astype(np.uint8)


def brightness(image, value):
    tempArr = np.clip(image + value, 0, 255)
    return tempArr.astype(np.uint8)

def grayscale(image):
    nrows, ncols, nchannels = image.shape
    new_img = np.zeros((nrows,ncols))
    
    for i in range(nrows):
        for j in range(ncols):
            form = 0.299*img[i][j][0] + 0.587*img[i][j][1] + 0.114*img[i][j][2] # adjusted to match human eye perception
            new_img[i][j] = form
    return new_img

def blur(image, radius, sigma):
    kernel = create_gaussian_kernel(radius, sigma)

    if len(image.shape) == 3: #if colored
        blurred = np.zeros_like(image, dtype=np.float32) #our image, initially zeores
        for i in range(3):
            blurred[:,:,i] = signal.convolve2d(
                image[:,:,i],
                kernel,
                mode='same',
                boundary='symm'
            )
    else: # if grayscale
        blurred = signal.convolve2d(
            image, 
            kernel,
            mode='same',
            boundary='symm'
        )

    return np.clip(blurred, 0, 255).astype(np.uint8)

def sharpen(img, intensity):
    sharpening_kernel = np.array([[0, -1, 0],
                                [-1, 4 * intensity + 1, -1],
                                [0, -1, 0]])

    sharpened_image = signal.convolve2d(img, sharpening_kernel, mode='reflect')
    return sharpened_image

def flip(image, axis='horizontal'):

    new_img = np.zeros_like(image)
    if axis=='horizontal':
        new_img = np.fliplr(image)
    elif axis=='vertical':
        new_img = np.flipud(image)
    else:
        new_img = image
    
    return new_img

def rotate(image, degrees):
    new_img = np.zeros_like(image)
    if(degrees==90):
        new_img = np.rot90(image, k=1)
    elif(degrees==180):
        new_img = np.rot90(image, k=2)
    elif(degrees==270):
        new_img = np.rot90(image, k=3)
    else:
        new_img = image
    return new_img


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-i","--invert",help='invert an image', action='store_true')
group.add_argument("--brightness", help='increase(+) or decrease(-) brightness', metavar='VAL', type=int)
group.add_argument("--grayscale", help='convert an image to grayscale', action='store_true')
group.add_argument("--blur", help="radius:controls area, sigma:controls strength", metavar=('RADIUS', 'SIGMA'), nargs=2, type=float)
group.add_argument("--sharpen", help="sharpen an image", metavar='INTENSITY', type=float)
group.add_argument("--flip", help="horizontal: left to right, vertical: upside down", choices=['horizontal', 'vertical'], metavar='AXIS', type=str)
group.add_argument("--rotate", help="rotate anti-clockwise 90, 180, 270 degrees", choices=[90,180,270], metavar='DEG', type=int)



args = parser.parse_args()
if args.invert:
    img = open_finder_and_select_image()
    image = plt.imread(img)
    new_img = invert(image)
    preview_and_save(new_img)
elif args.brightness:
    image = open_finder_and_select_image()
    img = plt.imread(image)
    new_img = brightness(img, args.brightness)
    preview_and_save(new_img)
elif args.grayscale:
    image = open_finder_and_select_image()
    img = plt.imread(image)
    new_img = grayscale(img)
    preview_and_save(new_img)
elif args.blur:
    image = open_finder_and_select_image()
    img = plt.imread(image)
    new_img = blur(img, args.blur[0], args.blur[1])
    preview_and_save(new_img)
elif args.sharpen:
    image = open_finder_and_select_image()
    img = plt.imread(image)
    new_img = sharpen(img, args.sharpen)
    preview_and_save(new_img)
elif args.flip:
    image = open_finder_and_select_image()
    img = plt.imread(image)
    new_img = flip(img, axis=args.flip)
    preview_and_save(new_img)
elif args.rotate:
    image = open_finder_and_select_image()
    img = plt.imread(image)
    new_img = rotate(img, args.rotate)
    preview_and_save(new_img)


