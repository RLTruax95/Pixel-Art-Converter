import numpy as np
from PIL import Image
import colorsys
from math import sqrt
from PIL import ImageDraw

def main():
    path =  "C:/Users/Truax/OneDrive/Pictures/KCat2.png" #temporarily load the image
    image_array : np.array  #all the colors for the 1x1 round tile from lego website
    availableColors = [[180, 0, 0], [187, 128, 90], [145, 80, 28],       #Bright Red, Nougat, Dark Orange
                      [225, 190, 161], [95, 49, 9], [170, 125, 85],      #Light Nougat, Reddish Brown, Medium Nougat
                      [214, 121, 35], [55, 33, 0], #[252, 172, 0],        #Bright Orange, Dark Brown, Flame Yellowish Orange
                      [137, 125, 98], [204, 185, 141], [185, 149, 59],   #Sand Yellow, Brick Yellow, Warm Gold
                      [250, 200, 10], [255, 236, 108], #[245, 243, 215],  #Bright Yellow, Cool Yellow, White Glow
                      [119, 119, 78], [225, 255, 0], [165, 202, 24],     #Olive Green, Vibrant Yellow, Bright Yellowish Green
                      [226, 249, 154], [88, 171, 65], [0, 133, 43],      #Spring Yellowish Green, Bright Green, Dark Green
                      [211, 242, 234], [0, 152, 148], [104, 195, 226],   #Aqua, Bright, Bluish Green, Medium Azur
                      [70, 155, 195], [30, 90, 168], [112, 129, 154],    #Dark Azur, Bright Blue, Sand Blue
                      [25, 50, 90], [0, 0, 0], [68, 26, 145],            #Earth Blue, Black, Medium Lilac
                      [160, 110, 185], [205, 164, 222], [144, 31, 118],  #Medium Lavender, Lavender, Bright Reddish Violet
                      [200, 80, 155], [255, 158, 205], [114, 0, 18],     #Bright Purple, Light Purple, New Dark Red
                      [240, 109, 120], [245, 245, 245], [150, 150, 150], #Vibrant Coral, White, Medium Stone Grey
                      [140, 140, 140], [100, 100, 100]]                  #Silver Metallic, Dark Stone Gray
    
    colorNames = ["Bright Red", "Nougat", "Dark Orange",
                  "Light Nougat", "Reddish Brown", "Medium Nougat",
                  "Bright Orange", "Dark Brown", #"Flame Yellowish Orange",
                  "Sand Yellow", "Brick Yellow", "Warm Gold",
                  "Bright Yellow", "Cool Yellow", #"White Glow",
                  "Olive Green", "Vibrant Yellow", "Bright Yellowish Green",
                  "Spring Yellowish Green", "Bright Green", "Dark Green",
                  "Aqua, Bright", "Bluish Green", "Medium Azur",
                  "Dark Azur", "Bright Blue", "Sand Blue",
                  "Earth Blue", "Black", "Medium Lilac",
                  "Medium Lavender", "Lavender", "Bright Reddish Violet",
                  "Bright Purple", "Light Purple", "New Dark Red",
                  "Vibrant Coral", "White", "Medium Stone Grey",
                  "Silver Metallic", "Dark Stone Gray"]
    
    color_counts = {tuple(c): 0 for c in availableColors}

    try:
        image = Image.open(path)        #opens the image and prints the size in terms of pixels
    except Exception as e:
        print("Error loading image")
        exit

    image_array = np.array(image)       #convert the image to a numpy array

    print("Image is ", image_array.shape[0], " pixels tall.")       #display dimensions and obtain target dimensions
    xVal = int(input("How many Legos tall?: "))
    print("Image is ", image_array.shape[1], " pixels wide.")
    yVal = int(input("How many Legos wide?: "))

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

            chosen  = compare_color(avg_rgb, availableColors)
            color_counts[tuple(chosen)] += 1
            colored_image[i,j] = chosen

    print("\nColor usage: ")
    for (color, name) in zip(availableColors, colorNames):
        count = color_counts[tuple(color)]
        if count > 0:
            print(f"{name} : {count}")

    circle_img = circles_from_pixels(colored_image, circle_diameter=20, bg_color=(0,0,0))       #convert the colored_image to a image drawn with circles instead of pixels
    circle_img.show()

def compare_color(current_color, color_options):        #function to find the pixels nearest color amongst the available colors
    best_distance = None
    color_choice = None

    for color in color_options:     #finds the distance from the current color and the available color by finding the difference
        distance = (                #between the red, green, and blue factors of the pixel
            (color[0] - current_color[0]) ** 2 +
            (color[1] - current_color[1]) ** 2 +
            (color[2] - current_color[2]) ** 2)

        if best_distance is None or distance < best_distance:       #saves the closest color
            best_distance = distance
            color_choice = color
    return color_choice     

def circles_from_pixels(pixel_array, circle_diameter=20, bg_color=(255, 255, 255)):     #converts the pixels to a series of dots
    
    h, w, _ = pixel_array.shape         #gets the dimensions of the image
    r = circle_diameter // 2            #sets the circle size

    # Size of the new image: one circle cell per pixel
    out_width = w * circle_diameter     #calculates the new image size
    out_height = h * circle_diameter

    out_img = Image.new("RGB", (out_width, out_height), bg_color)   #generate a new image
    draw = ImageDraw.Draw(out_img)      #draws the background onto the image

    for y in range(h):      #loop to draw the pixels in as cirlces
        for x in range(w):
            color = tuple(pixel_array[y, x].tolist())

            cx = x * circle_diameter + r   # circle center x
            cy = y * circle_diameter + r   # circle center y

            bbox = [cx - r, cy - r, cx + r, cy + r]     #defines the box that the cirlce will be drawn in
            draw.ellipse(bbox, fill=color, outline=None)        #draw circle

    return out_img
    
if __name__ == '__main__':
    main()