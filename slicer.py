from stl import Mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from pygcode import GCodeRapidMove, GCodeLinearMove


# Load STL model
stl_filename = 'test.stl'
mesh_data = Mesh.from_file(stl_filename)

print("STL model loaded.")

# Create a new plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D model facets as polygons
for facet in mesh_data.vectors:
    vertices = facet[:, :3]  # Extract the first 3 columns (x, y, z)
    poly = Poly3DCollection([vertices], edgecolor='black', alpha=0.2)
    ax.add_collection3d(poly)

# Set plot labels
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Adjust plot limits based on model dimensions
ax.auto_scale_xyz(mesh_data.x.flatten(), mesh_data.y.flatten(), mesh_data.z.flatten())

# Show the plot
plt.show()




# Set slicing parameters
layer_height = 0.2  # Layer height in mm
tool_diameter = 6.0  # Diameter of your cutting tool in mm
tool_height = 20.0  # Height of your cutting tool in mm

# Calculate adjusted maximum Z value
max_z = np.max(mesh_data.vectors[:, :, 2]) + tool_height

print("Calculations completed.")

# Open G-code output file
output_filename = 'carving_toolpath.gcode'
with open(output_filename, 'w') as output_file:
    # Iterate through layers and generate G-code
    for z in np.arange(layer_height, max_z + layer_height, layer_height):
        gcode = []
        
        for triangle in mesh_data.vectors:
            for vertex in triangle:
                # Calculate adjusted starting point based on tool diameter
                adjusted_x = vertex[0] - (tool_diameter / 2)
                adjusted_y = vertex[1] - (tool_diameter / 2)
                
                # Move to adjusted starting point (rapid move)
                gcode.append(GCodeRapidMove(x=adjusted_x, y=adjusted_y))
                
                # Move down to current layer (linear move)
                gcode.append(GCodeLinearMove(z=z))
                
                # Carve (add your carving G-code command here, e.g., M3/M5 for spindle control)
                gcode.append("M3")  # Start rotary tool
                
                # Rapid retract after carving (optional, adjust as needed)
                gcode.append(GCodeRapidMove(z=z + 2.0))
                gcode.append("M5")  # Stop rotary tool
        
        # Combine G-code instructions for this layer
        layer_gcode = '\n'.join(map(str, gcode))
        
        # Write layer G-code to the output file
        output_file.write(layer_gcode + '\n')
        
        print(f"Layer G-code generated and written for z = {z:.2f}")

print(f"G-code generation completed. Saved to {output_filename}")
