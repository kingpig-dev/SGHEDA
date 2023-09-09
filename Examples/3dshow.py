import pyvista as pv
import numpy as np

# Define the dimensions of the tube
outer_radius = 0.15
inner_radius = 0.1
tube_length = 1.0
tube_resolution = 100
inner_color = (255, 0, 0)  # Red color for the inner cylinder
outer_color = (0, 0, 255)  # Blue color for the outer cylinder

# Create the outer cylinder
outer_cylinder = pv.Cylinder(radius=outer_radius, height=tube_length, resolution=tube_resolution).triangulate()
outer_cylinder.opacity = 0.2
# outer_cylinder.cell_arrays["colors"] = outer_color

# Create the inner cylinder
inner_cylinder = pv.Cylinder(radius=inner_radius, height=tube_length, resolution=tube_resolution).triangulate()
# inner_cylinder.cell_arrays["colors"] = inner_color

# Create the material-filled tube by subtracting the inner cylinder from the outer cylinder
tube = outer_cylinder - inner_cylinder

# Set the color of the inner and outer cylinders
n_points = tube.n_points
colors = np.zeros((n_points, 3))
inner_color = np.array([255, 0, 0])  # Red color for the inner part
outer_color = np.array([0, 0, 255])  # Blue color for the outer part
colors[:n_points//2] = inner_color
colors[n_points//2:] = outer_color

# Assign the colors as a scalar field to the tube
tube["colors"] = colors

# Plot the tube
tube.plot(scalars="colors", show_scalar_bar=False)
