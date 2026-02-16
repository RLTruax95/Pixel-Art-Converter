import numpy as np
from PIL import Image
import colorsys

def main():
    path = "c:/Users/Truax/OneDrive/Pictures/yp8h4s0tr7p21.jpg"  #temporarily load the image
    image_array : np.array
    #desired_colors = [[0,0,0], [255,255,255]]       #array for holding the potential colors
    try:
        image = Image.open(path)        #opens the image and prints the size in terms of pixels
        print("Loaded image of size: ", image.size)     #--------------------Remove-------------------
    except Exception as e:
        print("Error loading image")

    image_array = np.array(image)       #convert the image to a numpy array

    print("Image is ", image_array.shape[1], " pixels wide.")       #display dimensions and obtain target dimensions
    xVal = int(input("How many Legos wide?: "))
    print("Image is ", image_array.shape[0], " pixels tall.")
    yVal = int(input("How many Legos tall?: "))

    lego_image = np.zeros((xVal, yVal, 3), dtype=np.uint8)      #create a new array of the target size full of zeros

    xRatio = int((image_array.shape[1]/xVal)+1)     #Gets the amount of pixels that will make up 1 target pixel
    yRatio = int((image_array.shape[0]/yVal)+1)

    image_temp = image.resize((yRatio*yVal, xRatio*xVal), Image.BILINEAR)   #resize the image to the next value divisible by the target size
    image_array = np.array(image_temp)

    for i in range(xVal):
        for j in range(yVal):
            xStart = i*xRatio       #get the location of the current x block position based on the target size
            xEnd = ((i+1)*xRatio)
            yStart = j*yRatio       #get the location of the current y block position based on the target size
            yEnd = ((j+1)*yRatio)
            block = image_array[xStart:xEnd, yStart:yEnd, :3]       #get a block of pixels
            avg_rgb = block.mean(axis=(0,1))        #average the RGB values for the new pixel
            lego_image[i, j] = avg_rgb.astype(np.uint8)     #save the new pixel to the finished image

    image.show()        #show the original and edited image
    lego_image = Image.fromarray(lego_image, mode="RGB")
    lego_image.show()
    
if __name__ == '__main__':
    main()