# Test Name:        ForLoop_MultiBodyValidation
# Author:           Ethan Markowski
# Editor:
# Bug(s):
# User Story(s):

# Objective:        Utilize python programming concepts to create and validate a model with an extremely large number of bodies

# Steps:            Sketch a series of 150 rectangles in a grid formation (timed)
#                   Pull each face a different distance to ensure that each body has a unique Volume (timed)
#                   Validate the existence and volume of each body using index style references

# Python Script, API Version = V21

# Import And Configure Script Performance Tools
import Ansys.Discovery.Api.V21.Internal.DiscoveryTesting as DiscoveryTesting
DiscoveryTesting.Performance.SetTestName("ForLoop_MultiBodyValidation")

# Relative Tolerance Value For Modeling Accuracy
modelTolerance = 1E-5

# Number Of Rectangles In X And Y Directions
num_x=10
num_y=15

# X And Y Dimensions Of Cube Bases
x=20
y=15

# Padding
padding=5

# Height Multiplier
height_multiplier=5

# Create Performance Objects
perfSketch = DiscoveryTesting.Performance("Script - Sketch {} Rectangles".format(num_x*num_y), 0.75)
perfPull = DiscoveryTesting.Performance("Script - Extrude {} Rectangles".format(num_x*num_y), 12.5)

SpaceClaimTesting.Scenario("Navigate To Model Stage")

# Change Stage
Solution.Solver.SetStage("ModelStage")
# EndBlock

SpaceClaimTesting.Scenario("Sketch {} Rectangles In A Grid Pattern".format(num_x * num_y))

# Sketch (num_x*num_y) Number Of Rectangles In A Grid Pattern And Time With Performance Object
perfSketch.StartPerformance()
for i in range(0, num_x):
    for j in range(0, num_y):
        # Sketch Rectangle
        plane = Plane.PlaneXY
        result = ViewHelper.SetSketchPlane(plane)
        point1 = Point2D.Create(MM(i*(x+padding)),MM(j*(y+padding)))
        point2 = Point2D.Create(MM((i+1)*x+i*padding),MM(j*(y+padding)))
        point3 = Point2D.Create(MM(i*(x+padding)),MM((j+1)*y+j*padding))
        result = SketchRectangle.Create(point1, point2, point3)
        # EndBlock
perfSketch.EndPerformance()

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

SpaceClaimTesting.Scenario("Extrude Each Rectangle To A Different Height")

# Use Pull Tool To Extrude Each Rectangle To A Different Height And Time With Performance Object
perfPull.StartPerformance()
for num in range(0, num_x*num_y):
    # This Conditional Statement Is Required Because The Face Indices Of The Rectangle Sketches Are Not All Assigned In Order
    if num == 0:
        selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[num_x*num_y-1])
    else:
        selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[0])
    # Extrude 1 Face
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.Add
    result = ExtrudeFaces.Execute(selection, MM((num+1)*height_multiplier), options)
    # EndBlock
perfPull.EndPerformance()

# Validate Existence And Volume Of Each Body
for num in range(0, num_x*num_y):
    SpaceClaimTesting.ValidateBodies(BodySelection.Create(GetRootPart().Bodies[num]), 1, 0, "Body: " + str(num))
    SpaceClaimTesting.ValidateVolume(BodySelection.Create(GetRootPart().Bodies[num]), MM3(x*y*height_multiplier*(num+1)), MM3(x*y*height_multiplier*(num+1))*modelTolerance, "Body: " + str(num))
