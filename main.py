# This module manages UI and parallel programming
import time

from multiprocessing import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from render import *
import test
import PIL
from PIL import Image

ULD = [160, 90]  # Ultra Low Definition; resolution mostly for quick testing
VLD = [320, 180]  # Very Low Definition
LD = [720, 360]  # Low Definition
SD = [1024, 576]  # Standard Definition
HD = [1280, 720]  # High Definition
FHD = [1920, 1080]  # Full HD
UHD = [2560, 1440]  # Ultra High Definition
UHD_4K = [3840, 2160]  # as a meme

if __name__ == "__main__":  # Make sure the threads don't execute this
    # Initialize image data
    width = int(input("Horizontal resolution: "))  # Image width
    height = int(input("Vertical resolution: "))  # Image height
    cores = max(int(input("Threads: "))-1, 1)  # Segments in which the image is divided
    antialiasing = bool(int(input("Antialiasing (0/1): ")))  # Render in double resolution and scale later down with a special algorithm
    debug_mode = False  # Set to true to print additional debug information
    save_images = True  # Set to true to save the rendered image

    scene_number = int(input("Scene (1/2/3):"))
    if scene_number == 3:
        scene = test.test_scene_2
    elif scene_number == 2:
        scene = test.test_scene_1
    else:
        scene = test.test_scene_0

    # Rendering image with double width and scaling it down later
    if antialiasing:
        width *= 2
        height *= 2

    pixels_per_block = int(np.ceil((width * height) / cores))  # Rough estimation of pixels per segment

    # Debug output
    print("--- Raytracing ---\n")
    print("Initial Data:")
    print("Width: " + str(width))
    print("Height: " + str(height))
    print("Segments: " + str(cores))
    print("Pixels per segment: " + str(pixels_per_block))
    print("Antialiasing: " + str(antialiasing) + (
        " (Rendering in double resolution and scaling down later)" if antialiasing else ""))
    print("Rendering scene",scene_number)

    rendered_image = np.zeros((height, width, 3), dtype=np.uint8)

image_render_time = time.time()


def block_render_thread(queue, scene, width, height, cores, block, pixels_per_block, start_index, end_index, start_row,
                        end_row, start_column, end_column):
    # Debug output

    start_time = time.time()

    # Render the block. A 2D array in the exact size of the block is expected
    rendered_block = render_scene(scene, width=width, height=height, block=block, cores=cores,
                                  pixels_per_block=pixels_per_block, start_row=start_row, end_row=end_row,
                                  start_column=start_column, end_column=end_column)

    queue.put((rendered_block, start_row, start_column))

    block_render_time = time.time() - start_time

    print("Rendered block " + str(block) + " within", str(block_render_time) + "s")


if __name__ == "__main__":  # Make sure the threads don't execute this

    queue = Queue()
    threads = []

    print("\nRendering " + str(cores) + " blocks...")

    # Rendering - render every block into the image
    for i in range(cores):
        block = i  # Block index

        start_index = block * pixels_per_block  # The start index if the image would be a 1D matrix
        end_index = np.minimum(width * height, (block + 1) * pixels_per_block) - 1  # The end index

        start_row = int(np.floor(start_index / float(width)))  # The start row index in the 2D image matrix
        start_column = start_index % width  # The start column index

        end_row = int(np.floor(end_index / float(width)))  # The end row index
        end_column = end_index % width  # The end column

        if debug_mode:
            print("\nRendering block: " + str(block))
            print("Start index (1D): " + str(start_index))
            print("End index (1D): " + str(end_index))
            print("Start row index: " + str(start_row))
            print("Start column index: " + str(start_column))
            print("End row index: " + str(end_row))
            print("End column index: " + str(end_column))

        thread = Process(target=block_render_thread, args=(
            queue, scene, width, height, cores, block, pixels_per_block, start_index, end_index, start_row, end_row,
            start_column, end_column))
        threads.append(thread)
        thread.start()

    rendered_blocks = 0  # Counter for rendered blocks

    plt.ion()  # Turn interactive mode on

    plt.figure().canvas.set_window_title(
        "Scene (" + str(width) + " x " + str(height) + (" , Antialiasing" if antialiasing else "") + ")")
    plt.title("Progress: 0.0 %")
    render_container = plt.imshow(rendered_image.astype(np.uint8))
    plt.pause(0.001)  # Pause shortly so the scene can be rendered
    im = PIL.Image.fromarray(rendered_image, mode="RGB")

    while rendered_blocks != cores:  # Wait for the threads to complete
        while not queue.empty():
            data = queue.get()
            rendered_block = data[0]

            for row in range(len(rendered_block)):
                for column in range(len(rendered_block[row])):
                    color = rendered_block[row][column]
                    rendered_image[data[1] + row][column if row != 0 else (column + data[2])] = color

            # Display the image
            im = PIL.Image.fromarray(rendered_image, mode="RGB")

            # Scale the image down to the original size if antialiasing is enabled
            if antialiasing:
                im = im.resize([width // 2, height // 2], Image.LANCZOS)

            rendered_blocks += 1

            plt.title("Progress: " + str(float(rendered_blocks / cores) * 100) + " %")
            plt.imshow(im)
            plt.draw()
            plt.pause(0.001)  # Pause shortly so the scene can be rendered

    plt.pause(0.2)

    render_time = str(time.time() - image_render_time)
    print("Rendered the scene within " + render_time + " s")

    plt.title("Rendered in " + render_time + " s")

    if save_images:
        im.save("render.bmp")

    plt.ioff()  # Turn interactive mode off
    plt.show()  # The window stays open
