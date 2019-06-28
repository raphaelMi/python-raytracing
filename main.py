# This module manages UI and parallel programming
import time

import numpy as np

from render import *
import test
import PIL
from PIL import Image

ULD = [160, 90]         # Ultra Low Definition; resolution mostly for quick testing
VLD = [320, 180]        # Very Low Definition
LD = [720, 360]         # Low Definition
SD = [1024, 576]        # Standard Definition
HD = [1280, 720]        # High Definition
FHD = [1920, 1080]      # Full HD
UHD = [2560, 1440]      # Ultra High Definition
UHD_4K = [3840, 2160]   # as a meme

# Initialize image data
width = ULD[0]  # Image width
height = ULD[1]  # Image height
cores = 1  # Segments in which the image is divided
pixels_per_block = int(np.ceil((width * height) / cores))  # Rough estimation of pixels per segment

# Debug output
print("--- Raytracing ---\n")
print("Initial Data:")
print("Width: " + str(width))
print("Height: " + str(height))
print("Segments: " + str(cores))
print("Pixels per segment: " + str(pixels_per_block))

# Prepare the scene

scene = test.test_scene_0

image_render_time = 0

# Rendering - render every block into the image
for i in range(cores):
    block = i  # Block index

    start_index = block * pixels_per_block  # The start index if the image would be a 1D matrix
    end_index = np.minimum(width * height, (block + 1) * pixels_per_block) - 1  # The end index

    start_row = int(np.floor(start_index / float(width)))  # The start row index in the 2D image matrix
    start_column = start_index % width  # The start column index

    end_row = int(np.floor(end_index / float(width)))  # The end row index
    end_column = end_index % width  # The end column

    # Debug output
    print("\nRendering block: " + str(block))
    print("Start index (1D): " + str(start_index))
    print("End index (1D): " + str(end_index))
    print("Start row index: " + str(start_row))
    print("Start column index: " + str(start_column))
    print("End row index: " + str(end_row))
    print("End column index: " + str(end_column))

    start_time = time.time()

    # Render the block. A 2D array in the exact size of the block is expected
    rendered_block = render_scene(scene, width=width, height=height, block=block, cores=cores,
                                  pixels_per_block=pixels_per_block, start_row=start_row, end_row=end_row,
                                  start_column=start_column, end_column=end_column)

    block_render_time = time.time() - start_time
    image_render_time += block_render_time  # Only count the time spent on rendering, not displaying
    print("Rendered block within", str(block_render_time) + "s")

    # Display the image

    im = PIL.Image.fromarray(rendered_block, mode="RGB")
    im = im.resize([width//2, height//2], Image.LANCZOS)
    im.save("render.bmp")
    im.show(title="render")


print("-- Finished rendering --")
print("Rendered image within " + str(image_render_time) + "s")
