# Python Script, API Version = V22 Beta

# Return updated script parameters
def updateParameters():
    return Parameters.Height, Parameters.Width, Parameters.Depth

# Create a box and return dictionary of FaceSelections
def createGeometry():
    # Create Box
    result = BlockBody.Create(Point.Create(-10, -10, 0), Point.Create(10, 10, 20), ExtrudeType.ForceAdd)
    # EndBlock
    
    selections = {
            "height" : [
                    FaceSelection.Create(GetRootPart().Bodies[0].Faces[1]),
                    FaceSelection.Create(GetRootPart().Bodies[0].Faces[0])
                    ],
            "width" : [
                    FaceSelection.Create(GetRootPart().Bodies[0].Faces[3]),
                    FaceSelection.Create(GetRootPart().Bodies[0].Faces[5])
                    ],
            "depth" : [
                    FaceSelection.Create(GetRootPart().Bodies[0].Faces[4]),
                    FaceSelection.Create(GetRootPart().Bodies[0].Faces[2])
                    ]
            }
    return selections

# Modify height, width, and depth of the box
def updateGeometry(selections, height, width, depth):
    # Extrude 1 Face
    selection = selections["height"][0]
    reference = selections["height"][1]
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.Add
    result = ExtrudeFaces.SetDimension(selection, reference, height, options)
    # EndBlock
    
    # Extrude 1 Face
    selection = selections["width"][0]
    reference = selections["width"][1]
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.Add
    result = ExtrudeFaces.SetDimension(selection, reference, width, options)
    # EndBlock
    
    # Extrude 1 Face
    selection = selections["depth"][0]
    reference =  selections["depth"][1]
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.Add
    result = ExtrudeFaces.SetDimension(selection, reference, depth, options)
    # EndBlock

# Retrieve updated script parameters
height, width, depth = updateParameters()

# Create a box and generate "selections" dictionary if "selections" does not exist
if not "selections" in globals():
    selections = createGeometry()
    
# Update height, width, and depth of the box based on script parameters
updateGeometry(selections, height, width, depth)