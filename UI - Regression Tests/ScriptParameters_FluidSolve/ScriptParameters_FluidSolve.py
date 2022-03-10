# Python Script, API Version = V22 Beta

# Clear geometry, physics, and monitors
def clear():
    Results.Streamline().Visible = False
    Results.Particles().Visible = False
    Results.Vectors().Visible = False

    for monitor in Results.Monitor.GetAll():
        monitor.Delete()
        
    for condition in Conditions.Flow.GetAll():
        condition.Delete()
        
    if not Selection.SelectAll().Count == 0:
        Delete.Execute(Selection.SelectAll())

# Return updated script parameters
def updateParameters():
    return [
        Parameters.MainPipe_Diameter, # Main pipe diameter in mm
        Parameters.MainPipe_Length, # Main pipe length in mm
        Parameters.Inlet_Diameter, # Inlet pipe diameter in mm
        int(Parameters.Inlet_Quantity), # Number of inlet pipes
        Parameters.Inlet_Velocity, # Inlet velocity in m/s
        Parameters.Outlet_Pressure # Outlet pressure in Pa
        ]

# Create pipe geometry and return DesignFaces for Inlet and Outlet BC creation
def createGeometry():
    from math import sin
    from math import cos
    from math import radians

    # Create the main section of the pipe geometry and return DesignFace for Outlet BC creation
    def createMainPipe(mainPipe_diameter, mainPipe_length):
        
        # Set Sketch Plane
        sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(0), MM(0), MM(0)), 
            -Direction.DirX, 
            Direction.DirY))
        result = ViewHelper.SetSketchPlane(sectionPlane, None)
        # End Block
    
        # Sketch Circle
        plane = Plane.PlaneXY
        result = ViewHelper.SetSketchPlane(plane)
        origin = Point2D.Create(MM(0), MM(0))
        result = SketchCircle.Create(origin, MM(mainPipe_diameter / 2))
        # EndBlock
        
        # Solidify Sketch
        mode = InteractionMode.Solid
        result = ViewHelper.SetViewMode(mode, None)
        # EndBlock
        
        circle = result.CreatedBodies[0].Faces[0]
        
        # Set Sketch Plane
        sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(0), MM(0), MM(mainPipe_length)), 
            -Direction.DirX, 
            Direction.DirY))
        result = ViewHelper.SetSketchPlane(sectionPlane, None)
        # End Block
        
        # Sketch Circle
        origin = Point2D.Create(MM(0), MM(0))
        result = SketchCircle.Create(origin, MM(mainPipe_diameter / 2))
        # EndBlock
        
        # Solidify Sketch
        mode = InteractionMode.Solid
        result = ViewHelper.SetViewMode(mode, None)
        # EndBlock
        
        endPlane = result.CreatedBodies[0].Faces[0]
        
        # Extrude Up To Body
        selection = FaceSelection.Create(circle)
        upToSelection = Selection.Create(endPlane)
        options = ExtrudeFaceOptions()
        result = ExtrudeFaces.UpTo(selection, Direction.DirZ, upToSelection, Point.Create(MM(0.0), MM(0.0), MM(mainPipe_length)), options)
        # EndBlock
        
        return result.CreatedBodies[0].Faces[1]
    
    # Create inlet pipes that feed into the main pipe and return DesignFaces collection for Inlet BC Creation
    def createInletPipes(inlet_diameter, inlet_N, mainPipe_diameter):
        
        # Create a curved pipe that branches off from the z axis
        # startZ = Z axis position to start drawing the pipe from
        # Return DesignFace that links to the end face of the created pipe
        def createPipe(startZ, straightLength, curveRadius, curveAngle, pipeDiameter):
            
            # Set Sketch Plane
            sectionPlane = Plane.PlaneZX
            result = ViewHelper.SetSketchPlane(sectionPlane, None)
            # EndBlock
            
            # Set New Sketch
            result = SketchHelper.StartConstraintSketching()
            # EndBlock
            
            # Sketch Line
            start = Point2D.Create(MM(startZ), MM(0))
            end = Point2D.Create(MM(startZ), MM(straightLength))
            result = SketchLine.Create(start, end)
            # EndBlock
            
            line = result.CreatedCurves[0]
            
            # Create Tangent Arc
            startSelPoint = SelectionPoint.Create(line.GetChildren[ICurvePoint]()[1])
            end = Point2D.Create(MM(startZ + curveRadius * (cos(radians(curveAngle)) -1)), MM(straightLength + curveRadius * sin(radians(curveAngle))))
            result = SketchArc.CreateTangentArc(startSelPoint, end)
            # EndBlock
            
            arc = result.CreatedCurves[0]
            
            # Solidify Sketch
            mode = InteractionMode.Solid
            result = ViewHelper.SetViewMode(mode, None)
            # EndBlock
            
            # Set Sketch Plane
            sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(straightLength + curveRadius * sin(radians(curveAngle))), MM(0), MM(startZ + curveRadius * (cos(radians(curveAngle)) -1))), 
                -Direction.DirX, 
                Direction.DirY))
            result = ViewHelper.SetSketchPlane(sectionPlane, None)
            # EndBlock
            
            # Set New Sketch
            result = SketchHelper.StartConstraintSketching()
            # EndBlock
            
            # Sketch Circle
            origin = Point2D.Create(MM(0), MM(0))
            result = SketchCircle.Create(origin, MM(inlet_diameter / 2))
            # EndBlock
            
            # Solidify Sketch
            mode = InteractionMode.Solid
            result = ViewHelper.SetViewMode(mode, None)
            # EndBlock
            
            circle = result.CreatedBodies[0].Faces[0]
            
            # Sweep 1 Face
            selection = FaceSelection.Create(circle)
            trajectories = Selection.Create([line, arc])
            options = SweepCommandOptions()
            options.ExtrudeType = ExtrudeType.Add
            options.Select = True
            result = Sweep.Execute(selection, trajectories, options, None)
            # EndBlock
            
            return result.CreatedFaces[0]
        
        padding = 2 * inlet_diameter # distance between inlet pipe connections
            
        inletFaces = [createPipe(padding * (i + 1), mainPipe_diameter/2+15, padding * (i + 1), 90, inlet_diameter) for i in range(0, inlet_N)]
        
        return inletFaces
    
    outletFace = createMainPipe(mainPipe_diameter, mainPipe_length)
    inletFaces = createInletPipes(inlet_diameter, inlet_N, mainPipe_diameter)
    
    ViewHelper.ZoomToEntity(Selection.SelectAll())

    return inletFaces, outletFace

# Create Inlet and Outlet conditions
# Create Avg. Static Pressure monitors at Inlet faces and an Avg. Velocity monitor at the Outlet face
def createSimulation(inletFaces, inletVelocity, outletFace, outletPressure):
    # Apply Flow Inlets
    for i, inletFace in enumerate(inletFaces):
        selection = FaceSelection.Create(inletFace)
        speed = SpeedQuantity.Create(inletVelocity, SpeedUnit.MeterPerSecond)
        result = Conditions.Flow.Create(selection, speed, FlowDirection.In)
        result.Temperature = TemperatureQuantity.Create(22, TemperatureUnit.DegreeCelsius)
        result.Label = "Flow Inlet {}".format(i+1)
        # EndBlock
    
    # Apply Flow Outlet
    selection = FaceSelection.Create(outletFace)
    pressure = PressureQuantity.Create(outletPressure, PressureUnit.Pascal)
    result = Conditions.Flow.Create(selection, pressure, FlowDirection.Out)
    result.Label = "Flow Outlet"
    # EndBlock
    
    # Add Avg. Static Pressure monitors at Inlets
    for i, inletFace in enumerate(inletFaces):
        # Add monitor
        resultVariable = Results.ResultVariable.Pressure
        resultFunction = Results.ResultFunction.Average
        selection = FaceSelection.Create(inletFace)
        result = Results.Monitor.Create(selection, resultVariable, resultFunction)
        result.Rename("Inlet {} - Avg. Static Pressure".format(i+1))
        # EndBlock
        
    # Create Avg. Velocity Monitor at Outlet
    resultVariable = Results.ResultVariable.Velocity
    resultFunction = Results.ResultFunction.Average
    selection = FaceSelection.Create(outletFace)
    result = Results.Monitor.Create(selection, resultVariable, resultFunction)
    result.Rename("Outlet - Avg. Velocity")
    # EndBlock

# Set Solver fidelity to 0.0 and solve in Refine Stage
# Configure results display to show Particles
def solve():
    Solution.Solver.SetTestingFidelity(4e6)
    Solution.Solver.StartExplore()
    Results.Streamline().Visible = False
    Results.Particles().Visible = True
    Results.Vectors().Visible = True

# Clear geometry, physics, and monitors
clear()

# Retrieve updated script parameters
mainPipe_diameter, mainPipe_length, inlet_diameter, inlet_N, inlet_velocity, outlet_pressure = updateParameters()

# Create pipe geometry
inletFaces, outletFace = createGeometry()

# Set up simulation
createSimulation(inletFaces, inlet_velocity, outletFace, outlet_pressure)

# Solve
solve()