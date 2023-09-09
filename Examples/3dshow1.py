import pyvista as pv
import numpy as np

# Define the dimensions of the tube
outer_radius = 0.15
inner_radius = 0.1
tube_length = 1.0
tube_resolution = 100

# Create the outer cylinder
outer_cylinder = pv.Cylinder(radius=outer_radius, height=tube_length, resolution=tube_resolution).triangulate()

# Create the inner cylinder
inner_cylinder = pv.Cylinder(radius=inner_radius, height=tube_length, resolution=tube_resolution).triangulate()

# Set the transparency of the inner cylinder
inner_opacity = 0.0  # Fully transparent inner cylinder
inner_color = np.array([1.0, 0.0, 0.0, inner_opacity])  # Red color with specified opacity (alpha value)
inner_cylinder.cell_arrays["colors"] = np.tile(inner_color, (inner_cylinder.n_cells, 1))

# Create the material-filled tube by merging the inner and outer cylinders
tube = outer_cylinder.copy()
tube.merge(inner_cylinder)

# Plot the tube
tube.plot(scalars="colors", show_scalar_bar=False)