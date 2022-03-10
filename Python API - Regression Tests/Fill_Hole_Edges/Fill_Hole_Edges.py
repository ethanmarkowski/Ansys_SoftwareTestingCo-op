# Test Name:        Fill_Hole_Edges
# Author:           Ethan Markowski
# Editor:
# Bug(s):
# User Story(s):
#
# Objective:        Validate functionality of Fill tool from Design tab
#
# Steps:            Sketch a rectangle and extrude to solid, validate
#                   Create a circular hole, validate
#                   Make all four edges round, validate
#                   Apply Fill tool to each rounded edge and validate after application of the tool
#                   Apply Fill tool to the hole and validate

# Python Script, API Version = V20

modelTolerance = 1E-5

SpaceClaimTesting.Scenario("Navigate To Model Stage")

# Change Stage
Solution.Solver.SetStage("ModelStage")
# EndBlock

# Repeated Validation Block To Confirm Existence of Round Features and Area If Feature Exists
def validateRounds():
    for [reference, isValid, area, id] in surfaces:
        SpaceClaimTesting.ValidateDouble(isValid, reference.IsValid(), "Exists", id+message, 0)
        if reference.IsValid():
            SpaceClaimTesting.ValidateArea(reference, area, area*modelTolerance, id+message)

SpaceClaimTesting.Scenario("Create Geometry")

# Sketch Rectangle
plane = Plane.PlaneXY
result = ViewHelper.SetSketchPlane(plane)
point1 = Point2D.Create(MM(-19),MM(14))
point2 = Point2D.Create(MM(29),MM(14))
point3 = Point2D.Create(MM(29),MM(-11))
result = SketchRectangle.Create(point1, point2, point3)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# Extrude 1 Face
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[0])
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.Add
result = ExtrudeFaces.Execute(selection, MM(8.42), options)
# EndBlock

# Validate Model Geometry
message = " - after extruding sketch"
SpaceClaimTesting.ValidateAll(1.0, 0, 6.0, 0, 12.0, 0, 1.0104e-05, 1.0104e-05*modelTolerance, 0.00362932, 0.00362932*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Create 4 Rounds")

# Create Round 1
selection = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[3])
options = ConstantRoundOptions()
result = ConstantRound.Execute(selection, MM(9.87), options, None)
# EndBlock

# Create Round 2
selection = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[1])
options = ConstantRoundOptions()
result = ConstantRound.Execute(selection, MM(7.05), options, None)
# EndBlock

# Create Round 3
selection = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[3])
options = ConstantRoundOptions()
result = ConstantRound.Execute(selection, MM(6.58), options, None)
# EndBlock

# Create Round 4
selection = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[4])
options = ConstantRoundOptions()
result = ConstantRound.Execute(selection, MM(7.8), options, None)
# EndBlock

# Creating List Of References To Round Surfaces, Corresponding IsValid States, Surface Areas, And Validation ID's
surfaces = [
        [FaceSelection.Create(GetRootPart().Bodies[0].Faces[6]), True, MM2(130.542), "Round: 1"],
        [FaceSelection.Create(GetRootPart().Bodies[0].Faces[7]), True, MM2(93.2440), "Round: 2"],
        [FaceSelection.Create(GetRootPart().Bodies[0].Faces[8]), True, MM2(87.0278), "Round: 3"],
        [FaceSelection.Create(GetRootPart().Bodies[0].Faces[9]), True, MM2(103.164), "Round: 4"]
        ]

# Validate Model Geometry
message = " - after creating Rounds"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 10.0, 0, 24.0, 0, 9.649994e-06, 9.649994e-06*modelTolerance, 0.003408365, 0.003408365*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Extrude Hole")

# Set Sketch Plane
sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(5), MM(1.5), MM(8.42)),
	Direction.DirX,
	Direction.DirY))
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Sketch Circle
origin = Point2D.Create(MM(-14), MM(7))
result = SketchCircle.Create(origin, MM(2.82842712474619))
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# Extrude 1 Face
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[10])
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.Cut
result = ExtrudeFaces.Execute(selection, MM(-79.38), options)
# EndBlock

# Append Interior Surface Of Hole to List Of Surfaces
surfaces.append([FaceSelection.Create(GetRootPart().Bodies[0].Faces[10]), True, MM2(149.636), "Hole Interior"])

# Validate Model Geometry
message = " - after creating hole"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 11.0, 0, 26.0, 0, 9.438376e-06, 9.438376e-06*modelTolerance, 0.003507736, 0.003507736*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Fill Round 1")

# Fill
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[5])
secondarySelection = Selection.Empty()
options = FillOptions()
result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)
# EndBlock

# Updating Expected IsValid State for Round: 1
surfaces[0][1] = False

# Validate Model Geometry
message = " - after Fill tool 1"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 10.0, 0, 23.0, 0, 9.614404e-06, 9.614404e-06*modelTolerance, 0.003585217, 0.003585217*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Fill Round 2")

# Fill
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[5])
secondarySelection = Selection.Empty()
options = FillOptions()
result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)
# EndBlock

# Updating Expected IsValid State for Round: 2
surfaces[1][1] = False

# Validate Model Geometry
message = " - after Fill tool 2"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 9.0, 0, 20.0, 0, 9.704213e-06, 9.704213e-06*modelTolerance, 0.003632027, 0.003632027*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Fill Round 3")

# Fill
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[5])
secondarySelection = Selection.Empty()
options = FillOptions()
result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)
# EndBlock

# Updating Expected IsValid State for Round: 3
surfaces[2][1] = False

# Validate Model Geometry
message = " - after Fill tool 3"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 8.0, 0, 17.0, 0, 9.782448e-06, 9.782448e-06*modelTolerance, 0.00367439, 0.00367439*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Fill Round 4")

# Fill
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[5])
secondarySelection = Selection.Empty()
options = FillOptions()
result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)
# EndBlock

# Updating Expected IsValid State for Round: 4
surfaces[3][1] = False

# Validate Model Geometry
message = " - after Fill tool 4"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 7.0, 0, 14.0, 0, 9.892382e-06, 9.892382e-06*modelTolerance, 0.003728691, 0.003728691*modelTolerance, "Model Geometry"+message)

SpaceClaimTesting.Scenario("Fill Hole")

# Fill
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[6])
secondarySelection = Selection.Empty()
options = FillOptions()
result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)
# EndBlock

# Updating Expected IsValid State for Hole Interior
surfaces[4][1] = False

# Validate Model Geometry
message = " - after Fill tool 5"
validateRounds()
SpaceClaimTesting.ValidateAll(1.0, 0, 6.0, 0, 12.0, 0, 1.0104e-05, 1.0104e-05*modelTolerance, 0.00362932, 0.00362932*modelTolerance, "Model Geometry"+message)
