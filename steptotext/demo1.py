import pandas as pd
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopoDS import topods
from OCC.Core.BRep import BRep_Tool
from OCC.Core.gp import gp_Pnt

def extract_step_data(step_file):
    # Load STEP file
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(step_file)
    if status != IFSelect_RetDone:
        raise Exception("Error reading STEP file")

    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    # Initialize lists for structured data
    data = []

    # Extract Faces
    exp_face = TopExp_Explorer(shape, TopAbs_FACE)
    face_id = 1
    while exp_face.More():
        face = topods.Face(exp_face.Current())  # Updated method
        surface_info = BRep_Tool.Surface(face)

        if surface_info:  # Check if the surface exists
            bounds = surface_info.Bounds()
            if len(bounds) == 4:
                umin, umax, vmin, vmax = bounds
                data.append(["Face", face_id, "", "", "", str(surface_info), umin, umax, vmin, vmax])
            else:
                data.append(["Face", face_id, "", "", "", str(surface_info), "", "", "", ""])
        face_id += 1
        exp_face.Next()

    # Extract Edges
    exp_edge = TopExp_Explorer(shape, TopAbs_EDGE)
    edge_id = 1
    while exp_edge.More():
        edge = topods.Edge(exp_edge.Current())  # Updated method
        curve_info = BRep_Tool.Curve(edge)

        if curve_info:  # Check if curve exists
            if len(curve_info) == 3:
                curve, first, last = curve_info
            elif len(curve_info) == 2:  # Handle missing last parameter
                curve, first = curve_info
                last = "N/A"  # Assign a default value

            data.append(["Edge", edge_id, "", "", "", str(curve), first, last, "", ""])
        edge_id += 1
        exp_edge.Next()

    # Extract Vertices
    exp_vertex = TopExp_Explorer(shape, TopAbs_VERTEX)
    vertex_id = 1
    while exp_vertex.More():
        vertex = topods.Vertex(exp_vertex.Current())  # Updated method
        point = BRep_Tool.Pnt(vertex)
        data.append(["Vertex", vertex_id, point.X(), point.Y(), point.Z(), "", "", "", "", ""])
        vertex_id += 1
        exp_vertex.Next()

    # Save to CSV
    columns = ["Type", "ID", "X", "Y", "Z", "Surface/Curve", "Umin", "Umax", "Vmin", "Vmax"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("step_data.csv", index=False)
    print("STEP data successfully extracted and saved to step_data.csv")

# Replace with your actual STEP file path
extract_step_data("/home/anaxturia/Anax_practice/steptotext/dataset/CORE HOUSING_IT0588-01.stp")
