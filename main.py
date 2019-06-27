# This module manages UI and parallelisation

from geometry import *
from render import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import time
from test import test_scene

# Initialize image data
width = 1920 # Image width
height = 1080 # Image height
cores = 1 # Segments in which the image is divided
pixelsPerBlock = int(np.ceil((width*height)/cores)) # Rough estimation of pixels per segment

# Debug output
print("--- Raytracing ---\n")
print("Initial Data:")
print("Width: "+str(width))
print("Height: "+str(height))
print("Segments: " + str(cores))
print("Pixels per segment: "+str(pixelsPerBlock))

# Prepare the scene

scene = test_scene

renderedImage = np.empty((height,width,3)) # Black background by default

imageRenderTime = 0

print("\n-- Started rendering --")

# Rendering - render every block into the image
for i in range(cores):
   block=i # Block index
   
   startIndex = block * pixelsPerBlock # The start index if the image would be a 1D matrix
   endIndex = np.minimum(width * height, block * pixelsPerBlock + pixelsPerBlock)-1 # The end index

   startRow = int(np.floor(startIndex/float(width))) # The start row index in the 2D image matrix
   startColumn = startIndex%width # The start column index
   
   endRow = int(np.floor(endIndex/float(width))) # The end row index
   endColumn = endIndex%width # The end column
   
   # Debug output
   print("Rendering block: "+str(block))
   print("Start index (1D): " + str(startIndex))
   print("End index (1D): " + str(endIndex))
   print("Start row index: "+str(startRow))
   print("Start column index: "+str(startColumn))
   print("End row index: "+str(endRow))
   print("End column index: "+str(endColumn))
   
   startTime = time.time()

   # Render the block. A 2D array in the exact size of the block is expected
   renderedBlock = render_scene(scene, width=width, height=height, block=block, cores=cores, pixelsPerBlock=pixelsPerBlock, startRow=startRow, endRow=endRow, startColumn=startColumn, endColumn=endColumn)
  
   blockRenderTime= time.time() - startTime
   imageRenderTime += blockRenderTime #Only count the time spent on rendering, not displaying 
   print("Rendered block within "+str(blockRenderTime) +"s")
   
   # Add the block to the rendered image
   for row in range(len(renderedBlock)):
       for column in range(len(renderedBlock[row])):
           color = renderedBlock[row][column]
           renderedImage[startRow+row][column if row != 0 else (column+startColumn)]=color
  
   # Display the image
   plt.imshow((renderedImage).astype(np.uint8))
   plt.show()
   
print("-- Finished rendering --")
print("Rendered image within "+str(imageRenderTime) +"s")

