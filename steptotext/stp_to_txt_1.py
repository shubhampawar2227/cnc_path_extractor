import os
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_RetError, IFSelect_RetFail
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_VERTEX
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.XCAFDoc import XCAFDoc_ColorType
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.TDF import TDF_LabelSequence
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XCAFApp import XCAFApp_Application
from OCC.Core.XCAFDoc import XCAFDoc_ColorTool, XCAFDoc_DocumentTool

# Function to extract all data from a STEP file
def extract_all_data(step_file, output_txt):
    # Check if the STEP file exists
    if not os.path.exists(step_file):
        print(f"Error: The file {step_file} does not exist.")
        return

    # Initialize XCAF application and document
    app = XCAFApp_Application.GetApplication()
    doc = TDocStd_Document("BinXCAF")
    app.NewDocument("BinXCAF", doc)

    # Load the STEP file
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file)

    # Check if the STEP file was read successfully
    if status != IFSelect_RetDone:
        if status == IFSelect_RetError:
            print("Error: Failed to read the STEP file. The file may be corrupted or invalid.")
        elif status == IFSelect_RetFail:
            print("Error: The STEP file is not supported or contains unsupported data.")
        else:
            print("Error: Unknown error occurred while reading the STEP file.")
        return

    # Transfer the STEP file data
    reader.TransferRoots()
    shape = reader.OneShape()

    # Open a text file to store extracted data
    with open(output_txt, "w") as file:
        file.write(f"STEP File: {os.path.basename(step_file)}\n\n")

        # Write the STEP file header and metadata
        file.write("--- STEP File Header and Metadata ---\n")
        try:
            file.write(f"File Description: {reader.FileDescription()}\n")
            file.write(f"File Name: {reader.FileName()}\n")
            file.write(f"File Schema: {reader.FileSchema()}\n\n")
        except Exception as e:
            file.write(f"Error extracting metadata: {str(e)}\n\n")

        # Write geometric entities (edges, faces, solids, vertices)
        file.write("--- Geometric Entities ---\n")

        # Define shape types to extract
        shape_types = {
            "Edges": (TopAbs_EDGE, "Edge"),
            "Faces": (TopAbs_FACE, "Face"),
            "Solids": (TopAbs_SOLID, "Solid"),
            "Vertices": (TopAbs_VERTEX, "Vertex"),
        }

        for shape_name, (shape_type, label) in shape_types.items():
            file.write(f"--- {shape_name} ---\n")

            explorer = TopExp_Explorer(shape, shape_type)
            count = 0
            while explorer.More():
                try:
                    item = explorer.Current()

                    # Get geometric properties
                    gprops = GProp_GProps()
                    if shape_type == TopAbs_EDGE:
                        brepgprop.LinearProperties(item, gprops)
                    elif shape_type == TopAbs_FACE:
                        brepgprop.SurfaceProperties(item, gprops)
                    elif shape_type == TopAbs_SOLID:
                        brepgprop.VolumeProperties(item, gprops)
                    elif shape_type == TopAbs_VERTEX:
                        brepgprop.LinearProperties(item, gprops)

                    center = gprops.CentreOfMass()
                    file.write(f"{label} {count}: Center (X={center.X()}, Y={center.Y()}, Z={center.Z()})\n")

                    # Get color information
                    color_tool = XCAFDoc_DocumentTool.ColorTool(doc.Main())
                    color_label_seq = TDF_LabelSequence()
                    color_tool.GetColors(color_label_seq)

                    color_found = False
                    for i in range(color_label_seq.Length()):
                        label = color_label_seq.Value(i + 1)
                        if color_tool.IsSet(label, XCAFDoc_ColorType.XCAFDoc_ColorGen):
                            color = Quantity_Color()
                            color_tool.GetColor(label, color)
                            file.write(f"  - Color: (R={color.Red()}, G={color.Green()}, B={color.Blue()})\n")
                            color_found = True

                    if not color_found:
                        file.write("  - Color: Not Found\n")

                    count += 1
                except Exception as e:
                    file.write(f"Error processing {label} {count}: {str(e)}\n")
                finally:
                    explorer.Next()

            file.write(f"Total {shape_name}: {count}\n\n")

        # Write additional STEP file data (raw content)
        file.write("--- Raw STEP File Data ---\n")
        try:
            with open(step_file, "r") as step_file_content:
                file.write(step_file_content.read())
        except Exception as e:
            file.write(f"Error reading raw STEP file data: {str(e)}\n")

    print(f"All STEP data saved to {output_txt}")

# Run the function with a sample STEP file
step_file_path = "/home/anaxturia/Anax_practice/steptotext/dataset/CORE HOUSING_IT0588-01.stp"  # Replace with actual file path
output_txt_path = "CoreHousingstp.txt"

extract_all_data(step_file_path, output_txt_path)