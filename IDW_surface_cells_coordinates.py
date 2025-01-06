import numpy as np

# Define the bounding box
latmin = 24.2961
latmax = 49.661
lonmin = -124.985
lonmax = -66.965

# Define the number of grid cells (resolution)
xcells = 300  # number of cells in the x (longitude) direction
ycells = 300  # number of cells in the y (latitude) direction

# Generate linearly spaced grid points
lats = np.linspace(latmin, latmax, ycells)
lons = np.linspace(lonmin, lonmax, xcells)

# Write the grid points to the IDW_surface_cells_coordinates.txt file
with open('IDW_surface_cells_coordinates.txt', 'w') as f:
    for lat in lats:
        for lon in lons:
            f.write(f"     {lon:.6f}       {lat:.6f}\n")

print("IDW_surface_cells_coordinates.txt file generated successfully.")
