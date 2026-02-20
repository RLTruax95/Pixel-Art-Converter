import numpy as np
from PIL import Image
import colorsys
from math import sqrt
from PIL import ImageDraw

def main():
    path = "C:/Users/Truax/OneDrive/Pictures/1abf3cbc-37a8-4690-9c7b-fd410bd4264c.jpg" #temporarily load the image
    image_array : np.array
    desired_colors = [[180, 0, 0], [187, 128, 90], [145, 80, 28],       #all the colors for the 1x1 round tile from lego website
                      [225, 190, 161], [95, 49, 9], [170, 125, 85],
                      [214, 121, 35], [55, 33, 0], [252, 172, 0],
                      [137, 125, 98], [204, 185, 141], [185, 149, 59],
                      [250, 200, 10], [255, 236, 108], [245, 243, 215],
                      [119, 119, 78], [225, 255, 0], [165, 202, 24],
                      [226, 249, 154], [88, 171, 65], [0, 133, 43],
                      [211, 242, 234], [0, 152, 148], [104, 195, 226],
                      [70, 155, 195], [30, 90, 168], [112, 129, 154],
                      [25, 50, 90], [0, 0, 0], [68, 26, 145],
                      [160, 110, 185], [205, 164, 222], [144, 31, 118],
                      [200, 80, 155], [255, 158, 205], [114, 0, 18],
                      [240, 109, 120], [245, 245, 245], [150, 150, 150],
                      [140, 140, 140], [100, 100, 100]]  
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

    print("\nWhite and black are always included")
    colorCount = int(input("How many other colors would you like to use?: "))
    for i in range(colorCount):
        red = int(input("\nRed Value: "))
        green = int(input("Green Value: "))
        blue = int(input("Blue Value: "))
        desired_colors.append([red, green, blue])
        print("Color added")

    lego_image = np.zeros((xVal, yVal, 3), dtype=np.uint8)      #create a new array of the target size full of zeros
    colored_image = np.zeros((xVal, yVal, 3), dtype=np.uint8)      #create a new array of the target size full of zeros

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
            colored_image[i,j]  = compare_color(avg_rgb, desired_colors)

    circle_img = circles_from_pixels(colored_image, circle_diameter=20, bg_color=(0,0,0))
    circle_img.show()
    colored_image = Image.fromarray(colored_image, mode="RGB")
    colored_image.show()

def compare_color(current_color, color_options):
    best_distance = None
    color_choice = None

    for color in color_options:
        distance = (
            (color[0] - current_color[0]) ** 2 +
            (color[1] - current_color[1]) ** 2 +
            (color[2] - current_color[2]) ** 2)

        if best_distance is None or distance < best_distance:
            best_distance = distance
            color_choice = color
    return color_choice

def circles_from_pixels(pixel_array, circle_diameter=20, bg_color=(255, 255, 255)):
    """
    pixel_array: numpy array (H, W, 3) of uint8 RGB values
    circle_diameter: diameter in pixels for each circle
    bg_color: background color of the new image
    """
    h, w, _ = pixel_array.shape
    r = circle_diameter // 2

    # Size of the new image: one circle cell per pixel
    out_width = w * circle_diameter
    out_height = h * circle_diameter

    out_img = Image.new("RGB", (out_width, out_height), bg_color)
    draw = ImageDraw.Draw(out_img)

    for y in range(h):
        for x in range(w):
            color = tuple(pixel_array[y, x].tolist())

            cx = x * circle_diameter + r   # circle center x
            cy = y * circle_diameter + r   # circle center y

            bbox = [cx - r, cy - r, cx + r, cy + r]
            draw.ellipse(bbox, fill=color, outline=None)

    return out_img
    
if __name__ == '__main__':
    main()