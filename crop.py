##########################################################
##########################################################
#
#   crop.py
#   crops and exports slide image
#   
#   USAGE
#   1. python crop.py [filename] [extension]
#   2. drag to select area for export
#   3. press ENTER(RETURN) to export image
#   4. press ESC to close application
#
#   [[ THIS IS A PROJECT OF DEVDOCTORS ]]
#   [[    https://bit.ly/devdoctors    ]]
#
#   Created by JoonNyung Heo (github @jnheo-md)
#   jnheo@jnheo.com
#   https://jnheo.com
#
##########################################################
##########################################################

from openslide import OpenSlide 
import cv2
import numpy as np
import sys

################################
#  Draws rectangle on the image
################################
def draw_rectangle(x,y):
    global small_img, image 
    image = small_img.copy()    # start from original image
    image -= 50                 # decrease brightness of image

    dragged = np.zeros_like(image)
    cv2.rectangle(dragged, pt1=(ix,iy), pt2=(x, y),color=(255,255,255),thickness=-1)    # create white box
    alpha = 0.8
    mask = dragged.astype(bool)
    image[mask] = cv2.addWeighted(image, alpha, dragged, 1-alpha,0)[mask]               # merge rectangle onto image

def onClick(event, x, y, flags, param):
    global ix, iy, drawing, finalX, finalY
    if event == cv2.EVENT_LBUTTONDOWN:  #when mousedown, set initial values
        drawing = True
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:  #when moving, redraw rectangle
        if drawing == True:
            draw_rectangle(x,y)
            


    elif event == cv2.EVENT_LBUTTONUP:  #when dragging end, set drawing to false and save the final coordinates
        drawing = False
        finalX = x
        finalY = y
        if abs(x-ix)<10 and abs(y-iy)<10 :  # if dragged are is too small, ignore
            return
        draw_rectangle(x,y)


###### START ######
if len(sys.argv) == 1:
    # no argument so error
    print("")
    print("=====================================================")
    print("!!!!! ERROR : Please provide the slide file !!!!!!!!!")
    print("-----------------------------------------------------")
    print("                       USAGE")
    print("-----------------------------------------------------")
    print("python crop.py [filename] [extension, default to tif]")
    print("ex) python crop.py filename.svs png")
    print("=====================================================")
    print("")

    exit()

if len(sys.argv) > 2: #receives second argument as output image extension (ex .tif)
    FILE_EXT = sys.argv[2] 
else : # Default extension to tif
    FILE_EXT = "tif"

FILE_NAME = sys.argv[1] #receives first argument as input file

slide_img = OpenSlide(FILE_NAME)
small_level = 2                     #use small image for setting croppable area
if slide_img.level_count <= 2: small_level = slide_img.level_count-1 # if there is less than or equal to 2 levels, set level to last level

small_img_size = slide_img.level_dimensions[small_level]

small_img = np.array(slide_img.read_region((0,0), small_level, size=small_img_size)) 
small_img = cv2.cvtColor(small_img, cv2.COLOR_RGB2BGR)  #finally, the image is presentable with cv2.imshow

#variables for dragging, initial values
ix = -1
iy = -1
finalX = -1
finalY = -1
drawing = False

image = small_img.copy()        #image for displaying

WINDOW_NAME = "DRAG to set crop area, then press ENTER"
cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, onClick)

while True:
    cv2.imshow(WINDOW_NAME, image)
    ret = cv2.waitKey(10)
    if ret == 27:   #esc, exit
        
        exit()
    elif ret==13 :  #return, so continue!
        cv2.destroyAllWindows()
        print("Cropping and exporting image...")
        break
        

if abs(ix-finalX) < 10 and abs(iy-finalY) < 10 :    # no area or too small area was selected. so export whole image 
    ix = 0
    iy =0
    finalX = small_img_size[0]
    finalY = small_img_size[1]

del small_img           #will not use again



# we got the coordinates
# so crop then save to tiff

#convert coordinates to level 0



orig_img_size = slide_img.level_dimensions[0]           #get full resolution image size

resize_ratio = orig_img_size[0]/small_img_size[0]       # get the ratio of larger image compared to thumbnail

newX1 = int(resize_ratio*ix)                            #start X of new image
newY1 = int(resize_ratio*iy)                            #start Y of new image
newX2 = int(resize_ratio*finalX)                        #end X of new image
newY2 = int(resize_ratio*finalY)                        #end Y of new image

image = np.array(slide_img.read_region((newX1,newY1), 0,size = (newX2-newX1, newY2-newY1)))
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

cv2.imwrite(FILE_NAME+"."+FILE_EXT,image)               #finally, right to file with extension