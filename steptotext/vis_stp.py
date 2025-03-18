import cadquery as cq
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh

# Function to load STEP file, convert to STL, and visualize
def step_to_stl_visualize(step_file, stl_output):
    # Load STEP file
    shape = cq.importers.importStep(step_file)
    
    # Export as STL
    cq.exporters.export(shape, stl_output)
    print(f"Conversion complete: {stl_output}")

    # Load the generated STL file
    your_mesh = mesh.Mesh.from_file(stl_output)

    # Plot the STL file
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection(your_mesh.vectors, alpha=0.5, edgecolor="k"))

    # Auto-scaling
    scale = your_mesh.points.flatten()
    ax.auto_scale_xyz(scale, scale, scale)

    plt.show()

step_file = "/home/anaxturia/Anax_practice/DRFN (1Nm to 20Nm).STEP"
stl_output = "output.stl"
step_to_stl_visualize(step_file, stl_output)
