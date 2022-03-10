# Test Name:    ForceCreation_Looping
# Author:       Ethan Markowski
#
# Objective:    Validate use of for loops to create 100 force conditions with different values on different faces
#
# Steps:        Create a 20 x 5 grid of rectangular faces
#               Assign a Distributed Force to each face with scaled magnitudes ranging between 10 N and 1000 N

# Python Script, API Version = V22 Beta

modelTolerance = 1E-5

# Create numX by numY grid of faces with overall dimensions of x by y
def createFaces(x, y, numX, numY):
    SpaceClaimTesting.Scenario("Create {} x {} Grid of Rectangular Faces".format(numX, numY))

    # Set New Sketch
    result = SketchHelper.StartConstraintSketching()
    # EndBlock

    # Sketch Rectangle
    plane = Plane.PlaneXY
    result = ViewHelper.SetSketchPlane(plane)
    point1 = Point2D.Create(MM(0),MM(y))
    point2 = Point2D.Create(MM(x),MM(y))
    point3 = Point2D.Create(MM(x),MM(0))
    result = SketchRectangle.Create(point1, point2, point3)
    # EndBlock

    for i in range(numX - 1):
        # Sketch Line
        start = Point2D.Create(MM(x / numX * (i + 1)), MM(0))
        end = Point2D.Create(MM(x / numX * (i + 1)), MM(y))
        result = SketchLine.Create(start, end)
        # EndBlock
        
    for i in range(numY - 1):
        # Sketch Line
        start = Point2D.Create(MM(0), MM(y / numY * (i + 1)))
        end = Point2D.Create(MM(x), MM(y / numY * (i + 1)))
        result = SketchLine.Create(start, end)
        # EndBlock
    
    # Solidify Sketch
    mode = InteractionMode.Solid
    result = ViewHelper.SetViewMode(mode, None)
    # EndBlock
    
    body = result.CreatedBodies[0]
    
    ViewHelper.ActivateNamedView("Trimetric")
    ViewHelper.ZoomToEntity(Selection.SelectAll())

    # Validate Geometry
    SpaceClaimTesting.ValidateAll(1.0, 0, numX * numY, 0, numX + numY + 2 * numX * numY, 0, 0.0, 0.0 * modelTolerance, MM(x) * MM(y), MM(x) * MM(y) * modelTolerance, "Model Geometry")

    return body

# Iterate through the faces of the specified DesignBody assigning a Distributed Force to each face with magnitudes that vary linearly between lowerMag and UpperMag
def createForces(body, lowerMag, upperMag):
    SpaceClaimTesting.Scenario("Apply Distributed Forces To Faces")

    # Create Distributed Forces
    forces = []
    for i, face in enumerate(body.Faces):
        # Apply Distributed Force
        magnitude = (upperMag - lowerMag) * i / (body.Faces.Count - 1) + lowerMag
        force = ForceQuantity.Create(magnitude, ForceUnit.Newton)
        result = Conditions.Force.Create(FaceSelection.Create(face), force)
        forces.append(result)
        # EndBlock

    # Validate Distributed Forces
    for i, (face, force) in enumerate(zip(body.Faces, forces)):
        label = "Distributed Force {}".format(i + 1)
        targetScope = FaceSelection.Create(face)
        targetMagnitude = (upperMag - lowerMag) * i / (body.Faces.Count - 1) + lowerMag

        SpaceClaimTesting.ValidateString(label, force.Label, "Label", label)
        SpaceClaimTesting.ValidateDouble(1.0, Selection.Create(force.Location).Evaluations == targetScope.Evaluations, "Correct Scope", label, 0)
        SpaceClaimTesting.ValidateDouble(1.0, force.Location.Count, "Location.Count", label, 0)
        SpaceClaimTesting.ValidateDouble(0.0, force.IsDeleted, "IsDeleted", label, 0)
        SpaceClaimTesting.ValidateDouble(targetMagnitude, force.TotalForce.Magnitude.Value, "TotalForce.Magnitude.Value", label, 0)
        SpaceClaimTesting.ValidateString("Newton", force.TotalForce.Magnitude.Unit.ToString(), "TotalForce.Magnitude.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.TotalForce.X.Value, "TotalForce.X.Value", label, 0)
        SpaceClaimTesting.ValidateString("Newton", force.TotalForce.X.Unit.ToString(), "TotalForce.X.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.TotalForce.Y.Value, "TotalForce.Y.Value", label, 0)
        SpaceClaimTesting.ValidateString("Newton", force.TotalForce.Y.Unit.ToString(), "TotalForce.Y.Unit", label)
        SpaceClaimTesting.ValidateDouble(-targetMagnitude, force.TotalForce.Z.Value, "TotalForce.Z.Value", label, 0)
        SpaceClaimTesting.ValidateString("Newton", force.TotalForce.Z.Unit.ToString(), "TotalForce.Z.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.Magnitude.Value, "Torque.Magnitude.Value", label, 0)
        SpaceClaimTesting.ValidateString("NewtonMeter", force.Torque.Magnitude.Unit.ToString(), "Torque.Magnitude.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.X.Value, "Torque.X.Value", label, 0)
        SpaceClaimTesting.ValidateString("NewtonMeter", force.Torque.X.Unit.ToString(), "Torque.X.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.Y.Value, "Torque.Y.Value", label, 0)
        SpaceClaimTesting.ValidateString("NewtonMeter", force.Torque.Y.Unit.ToString(), "Torque.Y.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.Z.Value, "Torque.Z.Value", label, 0)
        SpaceClaimTesting.ValidateString("NewtonMeter", force.Torque.Z.Unit.ToString(), "Torque.Z.Unit", label)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.Direction.X, "Torque.Direction.X", label, 0)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.Direction.Y, "Torque.Direction.Y", label, 0)
        SpaceClaimTesting.ValidateDouble(0.0, force.Torque.Direction.Z, "Torque.Direction.Z", label, 0)

body = createFaces(100, 40, 20, 5)
createForces(body, 10, 1000)
