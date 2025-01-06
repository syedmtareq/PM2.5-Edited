import numpy as np

# Define the bounding box and grid resolution
latmin, latmax = 24.2961, 49.661
lonmin, lonmax = -124.985, -66.965
# Calculate the necessary grid size
num_lines = 82499  # Derived from the character count requirement
grid_size = int(np.sqrt(num_lines))  # Assuming a square grid

# Generate the grid points
lats = np.linspace(latmin, latmax, grid_size)
lons = np.linspace(lonmin, lonmax, grid_size)

# Create the file and write the coordinates
with open('Bspline_Pixels_Corners.txt', 'w') as f:
    for lat in lats:
        for lon in lons:
            f.write(f"{lon:.6f}\t{lat:.6f}\n")

