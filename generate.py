import random
import numpy as np

def generate_random_array(x,spread=590):
    """Generates an array with x random numbers from 1 to 1000."""
    return [random.randint(1, spread) for _ in range(x)]

def generate_random_colors(x):
    """Generates a list of x random colors."""
    return [np.random.rand(3,) for _ in range(x)]

def generate_num_to_color(x,spread=590):
    # Initial data and colors
    data = generate_random_array(x)
    colors = generate_random_colors(x)

    # Create a mapping from number to color
    number_to_color = {number: color for number, color in zip(data, colors)}
    return data, colors, number_to_color