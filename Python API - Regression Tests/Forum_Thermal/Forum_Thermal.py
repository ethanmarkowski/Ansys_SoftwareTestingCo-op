# Test Name:    Forum_Thermal
# Author:       Ethan Markowski
#
# Objective:    Validate the workflow of the Getting Started - Thermal tutorial from the Discovery Forum
#
# Steps:        Open "IGBT Cooling_2021R1.scdoc"
#               Toggle the Base Plate to transparent and then back to opaque
#               Switch to Refine Stage
#               Perform a Volume Extract on the interior of the Base Plate
#               Generate Curve Imprints at the connections between the IGBT's and the Base Plate for the CHT Mesh Connections
#               Add a 1 m/s Flow Inlet to the extracted Volume
#               Enable Thermal Conditions and set the Inlet Temperature to 30 degrees C
#               Add a 0 Pa Flow Outlet to the Volume
#               Add 100 Watt Heat conditions to each IGT body
#               Set Default Convection condition to 5 W/(m^2*C) at 35 degrees
#               Apply an Insulated Condition to the bottom of the Base Plate
#               Set Fidelity to 0
#               Solve in Refine Stage and validate Max. Temperature, Pressure Drop, and Max. Velocity
#               Set each IGBT body material to Pure Silicon
#               Increase Flow Inlet Velocity to 2 m/s
#               Solve again in Refine Stage and validate Max. Temperature, Pressure Drop, and Max. Velocity
#
#               Open "Router_2021R1.scdoc"
#               Suppress and Hide the Case and Antennas
#               Apply a 25 Watt Heat Condition to the Chip body
#               Set the Default Convection condition to 5 W/(m^2*C)
#               Assign the following Material Conditions:
#                   Chip: Pure Silicon
#                   PCB: PCB laminate, Epoxy/Glass fiber, FR-4
#                   Conduct Layer: Copper, C10100, hard
#                   Heatsink: Aluminum alloy, wrought, 6061, T6
#               Add an Average Temperature Monitor to the Heatsink body and rename to Avg. Temperature Ribs
#               Set Testing Fidelity to 1,000,000
#               Solve in Explore Stage and validate Avg. Temperature Ribs, Max. Von Mises Stress, and Factor of Safety
#               Use the Move Tool to shorten the Heatsink ribs by 10 mm while the Solver is still running, validate Avg. Temperature Ribs
#               Show the Case and Antennas and set the Case to transparent
#               Pause the Solver
#               Hide the Case and Antennas
#               Apply Fixed Supports to the interior faces of the mounting holes in the PCB
#               Solve in Explore, validate Avg. Temperature Ribs and Factor of Safety

# Python Script, API Version = V22 Beta

import os

def ValidateMonitor(targetValue, targetUnit, testValue, propertyName, id, tolerance):
    if testValue is None:
        SpaceClaimTesting.ValidateString(str(targetValue), str(testValue), propertyName, id)
    else:
        SpaceClaimTesting.ValidateDouble(targetValue, testValue.Value, propertyName, id, targetValue*tolerance)
        SpaceClaimTesting.ValidateString(targetUnit, str(testValue.Unit), propertyName, id)

modelTolerance = 1e-5
simulationResultTolerance = 0.05

SpaceClaimTesting.Scenario("Open \"IGBT Cooling_2021R1.scdoc\"")

# Open Document
path = os.path.join(os.getenv("DISCO_TESTING_RESOURCES"), r"Unified\Geometry", "IGBT Cooling_2021R1.scdoc")
File.Open(path)
# EndBlock

# Validate Geometry
SpaceClaimTesting.ValidateAll(4.0, 0, 171.0, 0, 468.0, 0, 0.00111362, 0.00111362*modelTolerance, 0.1639108, 0.1639108*modelTolerance, "Model Geometry 1 - After Loading")

# Validate Stage
SpaceClaimTesting.ValidateString("ExploreStage", Solution.Solver.GetCurrentStageIdentifier(), "CurrentStageIdentifier", "Solution.Solver - After Loading 1")

SpaceClaimTesting.Scenario("Toggle Body Transparency")

# Set Style
selection = FaceSelection.Create(GetRootPart().Components[3].Content.Bodies[0].Faces[5])
ColorHelper.SetFillStyle(selection, FillStyle.Transparent)
# EndBlock

# Set Style
selection = FaceSelection.Create(GetRootPart().Components[3].Content.Bodies[0].Faces[5])
ColorHelper.SetFillStyle(selection, FillStyle.Opaque)
# EndBlock

SpaceClaimTesting.Scenario("Navigate To Refine Stage")

# Change Stage
Solution.Solver.SetStage("RefineStage")
# EndBlock

# Validate Stage
SpaceClaimTesting.ValidateString("RefineStage", Solution.Solver.GetCurrentStageIdentifier(), "CurrentStageIdentifier", "Solution.Solver - After Stage Switch")

SpaceClaimTesting.Scenario("Create Volume Extract")

# Create Volume
options = VolumeExtractOptions()
options.SeedPoint = GetRootPart().Components[3].Content.Bodies[0].Faces[12].EvalProportion(0.107641360586498, 0.499942292649546)
selection = FaceSelection.Create(GetRootPart().Components[3].Content.Bodies[0].Faces[9])
secondarySelection = FaceSelection.Create(GetRootPart().Components[3].Content.Bodies[0].Faces[12])
result = VolumeExtract.Create(selection, secondarySelection, options)
# EndBlock

SpaceClaimTesting.Scenario("Imprint Curves")

# Imprint Curves
options = FixImprintOptions()
options.Tolerance = MM(0.15707963267949)
result = FixImprint.FindAndFix(options)
# EndBlock

# Validate Geometry
SpaceClaimTesting.ValidateAll(5.0, 0, 178.0, 0, 484.0, 0, 0.001223995, 0.001223995*modelTolerance, 0.1930948, 0.1930948*modelTolerance, "Model Geometry 1 - After Modifying")

SpaceClaimTesting.Scenario("Enable Thermal Effects And Add Fluid-thermal Conditions")

# Regenerate Volume Body
selection = FaceSelection.Create(GetRootPart().Components[4].Content.Bodies[0].Faces[6])
speed = SpeedQuantity.Create(1, SpeedUnit.MeterPerSecond)
result = Conditions.Flow.Create(selection, speed, FlowDirection.In)
result.Temperature = TemperatureQuantity.Create(22, TemperatureUnit.DegreeCelsius)
# EndBlock

# Change Simulation Thermal Effects
simulation = Solution.Simulation.GetByLabel("Simulation 1")
simulation.IncludeThermalEffects = True
# EndBlock

# Set flow temperature
condition = Conditions.Flow.GetByLabel("Flow Inlet 1")
temperature = TemperatureQuantity.Create(30, TemperatureUnit.DegreeCelsius)
condition.Temperature = temperature
# EndBlock

# Apply Flow Outlet 2
selection = FaceSelection.Create(GetRootPart().Components[4].Content.Bodies[0].Faces[5])
pressure = PressureQuantity.Create(0, PressureUnit.Pascal)
result = Conditions.Flow.Create(selection, pressure, FlowDirection.Out)
# EndBlock

SpaceClaimTesting.Scenario("Apply Solid-Thermal Conditions")

# Apply Heat 1
selection = BodySelection.Create(GetRootPart().Components[0].Content.Bodies[0])
heat = PowerQuantity.Create(100, PowerUnit.Watt)
result = Conditions.Heat.Create(selection, heat)
# EndBlock

# Apply Heat 2
selection = BodySelection.Create(GetRootPart().Components[1].Content.Bodies[0])
heat = PowerQuantity.Create(100, PowerUnit.Watt)
result = Conditions.Heat.Create(selection, heat)
# EndBlock

# Apply Heat 3
selection = BodySelection.Create(GetRootPart().Components[2].Content.Bodies[0])
heat = PowerQuantity.Create(100, PowerUnit.Watt)
result = Conditions.Heat.Create(selection, heat)
# EndBlock

# Change Convection Coefficient
condition = Conditions.Convection.GetByLabel("Convection (default)")
coefficient = HeatTransferCoefficientQuantity.Create(5, HeatTransferCoefficientUnit.WattPerSquareMeterCelsius)
condition.ConvectionCoefficient = coefficient
# EndBlock

# Change Convection External Temperature
condition = Conditions.Convection.GetByLabel("Convection (default)")
temperature = TemperatureQuantity.Create(35, TemperatureUnit.DegreeCelsius)
condition.ExternalTemperature = temperature
# EndBlock

# Apply Insulated 1
selection = FaceSelection.Create(GetRootPart().Components[3].Content.Bodies[0].Faces[2])
result = Conditions.InsulatedCondition.Create(selection)
# EndBlock

# Set Fidelity Value
Solution.Solver.SetFidelity(0)
# EndBlock

# Validate Solver Fidelity
SpaceClaimTesting.ValidateDouble(0.0, Solution.Solver.GetFidelity(), "GetFidelity", "Solver - Refine 1", 0.0)

# Validate Material Assignments
componentLabels = [
        "IGBT1",
        "IGBT2",
        "IGBT3",
        "Base Plate"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Structural steel, S275N", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Volume"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Water", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

SpaceClaimTesting.Scenario("Solve CHT In Refine Stage")

# Start Solver in Refine Mode
Solution.Solver.StartRefine()
# EndBlock

# Validate Max. Temperature Results 1
maxTemperature = Results.Monitor.GetByLabel("Max. Temperature")
SpaceClaimTesting.ValidateString("Max. Temperature", maxTemperature.Label, "Label", "Max. Temperature - Refine Stage 1")
SpaceClaimTesting.ValidateString("None", maxTemperature.ResultComponent.ToString(), "ResultComponent", "Max. Temperature - Refine Stage 1")
SpaceClaimTesting.ValidateString("Maximum", maxTemperature.ResultFunction.ToString(), "ResultFunction", "Max. Temperature - Refine Stage 1")
SpaceClaimTesting.ValidateDouble(2.0, maxTemperature.Location.Count, "Location.Count", "Max. Temperature - Refine Stage 1", 0)
ValidateMonitor(319.54535, "Kelvin", maxTemperature.GetValue(ResultSource.Refine), "Temperature", "Max. Temperature - Refine Stage 1", simulationResultTolerance)

# Validate Pressure Drop Results 1
pressureDrop = Results.Monitor.GetByLabel("Pressure Drop")
SpaceClaimTesting.ValidateString("Pressure Drop", pressureDrop.Label, "Label", "Pressure Drop - Refine Stage 1")
SpaceClaimTesting.ValidateDouble(1.0, pressureDrop.Location.Count, "Location.Count", "Pressure Drop - Refine Stage 1", 0)
SpaceClaimTesting.ValidateString("None", pressureDrop.ResultComponent.ToString(), "ResultComponent", "Pressure Drop - Refine Stage 1")
SpaceClaimTesting.ValidateString("Average", pressureDrop.ResultFunction.ToString(), "ResultFunction", "Pressure Drop - Refine Stage 1")
SpaceClaimTesting.ValidateString("PressureDrop", pressureDrop.ResultVariable.ToString(), "ResultVariable", "Pressure Drop - Refine Stage 1")
ValidateMonitor(699.06934, "Pascal", pressureDrop.GetValue(Results.ResultSource.Refine), "Pressure", "Pressure Drop - Refine Stage 1", simulationResultTolerance)

# Validate Max. Velocity Results 1
maxVelocity = Results.Monitor.GetByLabel("Max. Velocity")
SpaceClaimTesting.ValidateString("Max. Velocity", maxVelocity.Label, "Label", "Max. Velocity - Refine Stage 1")
SpaceClaimTesting.ValidateDouble(1.0, maxVelocity.Location.Count, "Location.Count", "Max. Velocity - Refine Stage 1", 0)
SpaceClaimTesting.ValidateString("Mag", maxVelocity.ResultComponent.ToString(), "ResultComponent", "Max. Velocity - Refine Stage 1")
SpaceClaimTesting.ValidateString("Maximum", maxVelocity.ResultFunction.ToString(), "ResultFunction", "Max. Velocity - Refine Stage 1")
SpaceClaimTesting.ValidateString("Velocity", maxVelocity.ResultVariable.ToString(), "ResultVariable", "Max. Velocity - Refine Stage 1")
ValidateMonitor(1.3125601, "MeterPerSecond", maxVelocity.GetValue(Results.ResultSource.Refine), "Velocity", "Max. Velocity - Refine Stage 1", simulationResultTolerance)

SpaceClaimTesting.Scenario("Modify Material Assignments")

# Assign Silicon, pure
simulation = Solution.Simulation.GetByLabel("Simulation 1")
bodies = [GetRootPart().Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Content.Bodies[0],
    GetRootPart().Components[2].Content.Bodies[0]]
material = Materials.Material.GetLibraryMaterial("Silicon, pure")

for body in bodies:
    materialAssignment = Materials.MaterialAssignment.Create(simulation, body, material)
# EndBlock

# Validate Material Assignments
componentLabels = [
        "IGBT1",
        "IGBT2",
        "IGBT3",
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Silicon, pure", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Base Plate"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Structural steel, S275N", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Volume"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Water", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

SpaceClaimTesting.Scenario("Modify Flow Inlet 1")

# Set flow inlet velocity
condition = Conditions.Flow.GetByLabel("Flow Inlet 1")
speed = SpeedQuantity.Create(2, SpeedUnit.MeterPerSecond)
condition.Velocity = speed
# EndBlock

SpaceClaimTesting.Scenario("Solve CHT In Refine Stage")

# Start Solver in Refine Mode
Solution.Solver.StartRefine()
# EndBlock

# Validate Max. Temperature Results 2
maxTemperature = Results.Monitor.GetByLabel("Max. Temperature")
SpaceClaimTesting.ValidateString("Max. Temperature", maxTemperature.Label, "Label", "Max. Temperature - Refine Stage 2")
SpaceClaimTesting.ValidateString("None", maxTemperature.ResultComponent.ToString(), "ResultComponent", "Max. Temperature - Refine Stage 2")
SpaceClaimTesting.ValidateString("Maximum", maxTemperature.ResultFunction.ToString(), "ResultFunction", "Max. Temperature - Refine Stage 2")
SpaceClaimTesting.ValidateDouble(2.0, maxTemperature.Location.Count, "Location.Count", "Max. Temperature - Refine Stage 2", 0)
ValidateMonitor(314.00128, "Kelvin", maxTemperature.GetValue(ResultSource.Refine), "Temperature", "Max. Temperature - Refine Stage 2", simulationResultTolerance)

# Validate Pressure Drop Results 2
pressureDrop = Results.Monitor.GetByLabel("Pressure Drop")
SpaceClaimTesting.ValidateString("Pressure Drop", pressureDrop.Label, "Label", "Pressure Drop - Refine Stage 2")
SpaceClaimTesting.ValidateDouble(1.0, pressureDrop.Location.Count, "Location.Count", "Pressure Drop - Refine Stage 2", 0)
SpaceClaimTesting.ValidateString("None", pressureDrop.ResultComponent.ToString(), "ResultComponent", "Pressure Drop - Refine Stage 2")
SpaceClaimTesting.ValidateString("Average", pressureDrop.ResultFunction.ToString(), "ResultFunction", "Pressure Drop - Refine Stage 2")
SpaceClaimTesting.ValidateString("PressureDrop", pressureDrop.ResultVariable.ToString(), "ResultVariable", "Pressure Drop - Refine Stage 2")
ValidateMonitor(2590.9144, "Pascal", pressureDrop.GetValue(Results.ResultSource.Refine), "Velocity", "Pressure Drop - Refine Stage 2", simulationResultTolerance)

# Validate Max. Velocity Results 2
maxVelocity = Results.Monitor.GetByLabel("Max. Velocity")
SpaceClaimTesting.ValidateString("Max. Velocity", maxVelocity.Label, "Label", "Max. Velocity - Refine Stage 2")
SpaceClaimTesting.ValidateDouble(1.0, maxVelocity.Location.Count, "Location.Count", "Max. Velocity - Refine Stage 2", 0)
SpaceClaimTesting.ValidateString("Mag", maxVelocity.ResultComponent.ToString(), "ResultComponent", "Max. Velocity - Refine Stage 2")
SpaceClaimTesting.ValidateString("Maximum", maxVelocity.ResultFunction.ToString(), "ResultFunction", "Max. Velocity - Refine Stage 2")
SpaceClaimTesting.ValidateString("Velocity", maxVelocity.ResultVariable.ToString(), "ResultVariable", "Max. Velocity - Refine Stage 2")
ValidateMonitor(2.625830, "MeterPerSecond", maxVelocity.GetValue(Results.ResultSource.Refine), "Velocity", "Max. Velocity - Refine Stage 2", simulationResultTolerance)

SpaceClaimTesting.Scenario("Navigate To Explore Stage")

# Start Solver in Explore Mode
Solution.Solver.SetStage("ExploreStage")
# EndBlock

SpaceClaimTesting.Scenario("Open Router_2021R1.scdoc")

# Open Document
path = os.path.join(os.getenv("DISCO_TESTING_RESOURCES"), r"Unified\Geometry", "Router_2021R1.scdoc")
File.Open(path)
# EndBlock

# Validate Geometry
SpaceClaimTesting.ValidateAll(25.0, 0, 4563.0, 0, 11489.0, 0, 0.0006503473, 0.0006503473*modelTolerance, 0.4966698, 0.4966698*modelTolerance, "Model Geometry 2")

# Validate Stage
SpaceClaimTesting.ValidateString("ExploreStage", Solution.Solver.GetCurrentStageIdentifier(), "CurrentStageIdentifier", "Solution.Solver - After Loading 2")

# Validate Material Assignments
componentLabels = [
        "Case",
        "Electronics",
        "Antennas"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Structural steel, S275N", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Suppress Physics
simulation = Solution.Simulation.GetByLabel("Simulation 1")
selection = BodySelection.Create([GetRootPart().Components[0].Components[0].Content.Bodies[0],
    GetRootPart().Components[0].Components[1].Content.Bodies[0],
    GetRootPart().Components[0].Components[2].Content.Bodies[0],
    GetRootPart().Components[0].Components[3].Content.Bodies[0],
    GetRootPart().Components[0].Components[4].Content.Bodies[0],
    GetRootPart().Components[0].Components[5].Content.Bodies[0]])
simulation.SuppressBodies(selection,True)
# EndBlock

SpaceClaimTesting.Scenario("Set Suppression And Visibility States")

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[0].Content,
    GetRootPart().Components[0].Components[0].Content,
    GetRootPart().Components[0].Components[0].Content.Bodies[0],
    GetRootPart().Components[0].Components[1].Content,
    GetRootPart().Components[0].Components[1].Content.Bodies[0],
    GetRootPart().Components[0].Components[2].Content,
    GetRootPart().Components[0].Components[2].Content.Bodies[0],
    GetRootPart().Components[0].Components[3].Content,
    GetRootPart().Components[0].Components[3].Content.Bodies[0],
    GetRootPart().Components[0].Components[4].Content,
    GetRootPart().Components[0].Components[4].Content.Bodies[0],
    GetRootPart().Components[0].Components[5].Content,
    GetRootPart().Components[0].Components[5].Content.Bodies[0]])
visibility = VisibilityType.Hide
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

# Suppress Physics
simulation = Solution.Simulation.GetByLabel("Simulation 1")
selection = BodySelection.Create([GetRootPart().Components[2].Components[0].Content.Bodies[0],
    GetRootPart().Components[2].Components[0].Content.Bodies[1],
    GetRootPart().Components[2].Components[1].Content.Bodies[0],
    GetRootPart().Components[2].Components[2].Content.Bodies[0],
    GetRootPart().Components[2].Components[3].Content.Bodies[0],
    GetRootPart().Components[2].Components[4].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content.Bodies[1],
    GetRootPart().Components[2].Components[6].Content.Bodies[0],
    GetRootPart().Components[2].Components[6].Content.Bodies[1],
    GetRootPart().Components[2].Components[7].Content.Bodies[0],
    GetRootPart().Components[2].Components[8].Content.Bodies[0],
    GetRootPart().Components[2].Components[9].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content.Bodies[1]])
simulation.SuppressBodies(selection,True)
# EndBlock

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[2].Content,
    GetRootPart().Components[2].Components[0].Content,
    GetRootPart().Components[2].Components[0].Content.Bodies[0],
    GetRootPart().Components[2].Components[0].Content.Bodies[1],
    GetRootPart().Components[2].Components[1].Content,
    GetRootPart().Components[2].Components[1].Content.Bodies[0],
    GetRootPart().Components[2].Components[2].Content,
    GetRootPart().Components[2].Components[2].Content.Bodies[0],
    GetRootPart().Components[2].Components[3].Content,
    GetRootPart().Components[2].Components[3].Content.Bodies[0],
    GetRootPart().Components[2].Components[4].Content,
    GetRootPart().Components[2].Components[4].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content,
    GetRootPart().Components[2].Components[5].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content.Bodies[1],
    GetRootPart().Components[2].Components[6].Content,
    GetRootPart().Components[2].Components[6].Content.Bodies[0],
    GetRootPart().Components[2].Components[6].Content.Bodies[1],
    GetRootPart().Components[2].Components[7].Content,
    GetRootPart().Components[2].Components[7].Content.Bodies[0],
    GetRootPart().Components[2].Components[8].Content,
    GetRootPart().Components[2].Components[8].Content.Bodies[0],
    GetRootPart().Components[2].Components[9].Content,
    GetRootPart().Components[2].Components[9].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content,
    GetRootPart().Components[2].Components[10].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content.Bodies[1]])
visibility = VisibilityType.Hide
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

SpaceClaimTesting.Scenario("Apply Thermal Boundary Conditions")

# Apply Heat 1
selection = BodySelection.Create(GetRootPart().Components[1].Components[2].Content.Bodies[0])
heat = PowerQuantity.Create(25, PowerUnit.Watt)
result = Conditions.Heat.Create(selection, heat)
# EndBlock

# Change Convection Coefficient
condition = Conditions.Convection.GetByLabel("Convection (default)")
coefficient = HeatTransferCoefficientQuantity.Create(5, HeatTransferCoefficientUnit.WattPerSquareMeterCelsius)
condition.ConvectionCoefficient = coefficient
# EndBlock

SpaceClaimTesting.Scenario("Modify Material Assignments")

# Assign Silicon, pure
simulation = Solution.Simulation.GetByLabel("Simulation 1")
body = GetRootPart().Components[1].Components[2].Content.Bodies[0]
material = Materials.Material.GetLibraryMaterial("Silicon, pure")
materialAssignment = Materials.MaterialAssignment.Create(simulation, body, material)
# EndBlock

# Assign PCB laminate, Epoxy/Glass fiber, FR-4
simulation = Solution.Simulation.GetByLabel("Simulation 1")
body = GetRootPart().Components[1].Components[1].Content.Bodies[0]
material = Materials.Material.GetLibraryMaterial("PCB laminate, Epoxy/Glass fiber, FR-4")
materialAssignment = Materials.MaterialAssignment.Create(simulation, body, material)
# EndBlock

# Assign Copper, C10100, hard
simulation = Solution.Simulation.GetByLabel("Simulation 1")
body = GetRootPart().Components[1].Components[3].Content.Bodies[0]
material = Materials.Material.GetLibraryMaterial("Copper, C10100, hard")
materialAssignment = Materials.MaterialAssignment.Create(simulation, body, material)
# EndBlock

# Assign Aluminum alloy, wrought, 6061, T6
simulation = Solution.Simulation.GetByLabel("Simulation 1")
body = GetRootPart().Components[1].Components[0].Content.Bodies[0]
material = Materials.Material.GetLibraryMaterial("Aluminum alloy, wrought, 6061, T6")
materialAssignment = Materials.MaterialAssignment.Create(simulation, body, material)
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Case",
        "Antennas"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Structural steel, S275N", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Heatsink"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Aluminum alloy, wrought, 6061, T6", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "PCB"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("PCB laminate, Epoxy/Glass fiber, FR-4", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Chip"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Silicon, pure", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

# Validate Material Assignments
componentLabels = [
        "Conduct Layer"
        ]

for label in componentLabels:
    for i, body in enumerate(ComponentSelection.CreateByNames(label).ConvertToBodies().Items):
        SpaceClaimTesting.ValidateString("Copper, C10100, hard", body.GetMaterial().Label, "Material.Label", "{} - Body {}".format(body.Parent.GetName(), i))
# EndBlock

SpaceClaimTesting.Scenario("Add Avg. Temperature Ribs Monitor")

# Add monitor
resultVariable = Results.ResultVariable.Temperature
resultFunction = Results.ResultFunction.Average
selection = BodySelection.Create(GetRootPart().Components[1].Components[0].Content.Bodies[0])
result = Results.Monitor.Create(selection, resultVariable, resultFunction)
# EndBlock

# Set Label
monitor = Results.Monitor.GetByLabel("Avg. Temperature 1")
monitor.Rename("Avg. Temperature Ribs")
# EndBlock

# Set Fidelity Value
Solution.Solver.SetTestingFidelity(2e6)
# EndBlock

SpaceClaimTesting.Scenario("Solve In Explore Stage")

# Start Solver in Explore Mode
Solution.Solver.StartExplore()
Solution.Solver.PauseExplore()
# EndBlock

# Validate Avg. Temperature Ribs Results 1
avgTempRibs = Results.Monitor.GetByLabel("Avg. Temperature Ribs")
SpaceClaimTesting.ValidateString("Avg. Temperature Ribs", avgTempRibs.Label, "Label", "Avg. Temperature Ribs - Explore Stage 1")
SpaceClaimTesting.ValidateDouble(1.0, avgTempRibs.Location.Count, "Location.Count", "Avg. Temperature Ribs - Explore Stage 1", 0)
SpaceClaimTesting.ValidateString("None", str(avgTempRibs.ResultComponent), "ResultComponent", "Avg. Temperature Ribs - Explore Stage 1")
SpaceClaimTesting.ValidateString("Average", avgTempRibs.ResultFunction.ToString(), "ResultFunction", "Avg. Temperature Ribs - Explore Stage 1")
SpaceClaimTesting.ValidateString("Temperature", avgTempRibs.ResultVariable.ToString(), "ResultVariable", "Avg. Temperature Ribs - Explore Stage 1")
ValidateMonitor(65.2891998291016, "DegreeCelsius", avgTempRibs.GetValue(ResultSource.Explore), "Temperature", "Avg. Temperature Ribs - Explore Stage 1", simulationResultTolerance)

SpaceClaimTesting.Scenario("Modify Heatsink Height")

# Translate Along Z Handle
selection = FaceSelection.Create([GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[27],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[28],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[29],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[30],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[149],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[150],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[151],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[152],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[153],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[154],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[155],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[156],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[157],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[158],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[159],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[160],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[161],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[162],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[163],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[164],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[165],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[166],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[167],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[168],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[169],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[170],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[171],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[172],
    GetRootPart().Components[1].Components[0].Content.Bodies[0].Faces[173]])
direction = Move.GetDirection(selection)
options = MoveOptions()
result = Move.Translate(selection, direction, MM(-10), options)
# EndBlock

# Validate Geometry
SpaceClaimTesting.ValidateAll(25.0, 0, 4563.0, 0, 11489.0, 0, 0.0006225473, 0.0006225473*modelTolerance, 0.4677098, 0.4677098*modelTolerance, "Model Geometry 2 - After Modifying")

SpaceClaimTesting.Scenario("Solve In Explore Stage")

# Start Solver in Explore Mode
Solution.Solver.StartExplore()
Solution.Solver.PauseExplore()
# EndBlock

# Validate Avg. Temperature Ribs Results 2
avgTempRibs = Results.Monitor.GetByLabel("Avg. Temperature Ribs")
SpaceClaimTesting.ValidateString("Avg. Temperature Ribs", avgTempRibs.Label, "Label", "Avg. Temperature Ribs - Explore Stage 2")
SpaceClaimTesting.ValidateDouble(1.0, avgTempRibs.Location.Count, "Location.Count", "Avg. Temperature Ribs - Explore Stage 2", 0)
SpaceClaimTesting.ValidateString("None", str(avgTempRibs.ResultComponent), "ResultComponent", "Avg. Temperature Ribs - Explore Stage 2")
SpaceClaimTesting.ValidateString("Average", avgTempRibs.ResultFunction.ToString(), "ResultFunction", "Avg. Temperature Ribs - Explore Stage 2")
SpaceClaimTesting.ValidateString("Temperature", avgTempRibs.ResultVariable.ToString(), "ResultVariable", "Avg. Temperature Ribs - Explore Stage 2")
ValidateMonitor(71.5075759887695, "DegreeCelsius", avgTempRibs.GetValue(ResultSource.Explore), "Temperature", "Avg. Temperature Ribs - Explore Stage 2", simulationResultTolerance)

SpaceClaimTesting.Scenario("Modify Visibility States")

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[0].Content,
    GetRootPart().Components[0].Components[0].Content,
    GetRootPart().Components[0].Components[0].Content.Bodies[0],
    GetRootPart().Components[0].Components[1].Content,
    GetRootPart().Components[0].Components[1].Content.Bodies[0],
    GetRootPart().Components[0].Components[2].Content,
    GetRootPart().Components[0].Components[2].Content.Bodies[0],
    GetRootPart().Components[0].Components[3].Content,
    GetRootPart().Components[0].Components[3].Content.Bodies[0],
    GetRootPart().Components[0].Components[4].Content,
    GetRootPart().Components[0].Components[4].Content.Bodies[0],
    GetRootPart().Components[0].Components[5].Content,
    GetRootPart().Components[0].Components[5].Content.Bodies[0]])
visibility = VisibilityType.Show
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[2].Content,
    GetRootPart().Components[2].Components[0].Content,
    GetRootPart().Components[2].Components[0].Content.Bodies[0],
    GetRootPart().Components[2].Components[0].Content.Bodies[1],
    GetRootPart().Components[2].Components[1].Content,
    GetRootPart().Components[2].Components[1].Content.Bodies[0],
    GetRootPart().Components[2].Components[2].Content,
    GetRootPart().Components[2].Components[2].Content.Bodies[0],
    GetRootPart().Components[2].Components[3].Content,
    GetRootPart().Components[2].Components[3].Content.Bodies[0],
    GetRootPart().Components[2].Components[4].Content,
    GetRootPart().Components[2].Components[4].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content,
    GetRootPart().Components[2].Components[5].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content.Bodies[1],
    GetRootPart().Components[2].Components[6].Content,
    GetRootPart().Components[2].Components[6].Content.Bodies[0],
    GetRootPart().Components[2].Components[6].Content.Bodies[1],
    GetRootPart().Components[2].Components[7].Content,
    GetRootPart().Components[2].Components[7].Content.Bodies[0],
    GetRootPart().Components[2].Components[8].Content,
    GetRootPart().Components[2].Components[8].Content.Bodies[0],
    GetRootPart().Components[2].Components[9].Content,
    GetRootPart().Components[2].Components[9].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content,
    GetRootPart().Components[2].Components[10].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content.Bodies[1]])
visibility = VisibilityType.Show
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

# Set Style
selection = BodySelection.Create(GetRootPart().Components[0].Components[2].Content.Bodies[0])
ColorHelper.SetFillStyle(selection, FillStyle.Transparent)
# EndBlock

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[0].Content,
    GetRootPart().Components[0].Components[0].Content,
    GetRootPart().Components[0].Components[0].Content.Bodies[0],
    GetRootPart().Components[0].Components[1].Content,
    GetRootPart().Components[0].Components[1].Content.Bodies[0],
    GetRootPart().Components[0].Components[2].Content,
    GetRootPart().Components[0].Components[2].Content.Bodies[0],
    GetRootPart().Components[0].Components[3].Content,
    GetRootPart().Components[0].Components[3].Content.Bodies[0],
    GetRootPart().Components[0].Components[4].Content,
    GetRootPart().Components[0].Components[4].Content.Bodies[0],
    GetRootPart().Components[0].Components[5].Content,
    GetRootPart().Components[0].Components[5].Content.Bodies[0]])
visibility = VisibilityType.Hide
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[2].Content,
    GetRootPart().Components[2].Components[0].Content,
    GetRootPart().Components[2].Components[0].Content.Bodies[0],
    GetRootPart().Components[2].Components[0].Content.Bodies[1],
    GetRootPart().Components[2].Components[1].Content,
    GetRootPart().Components[2].Components[1].Content.Bodies[0],
    GetRootPart().Components[2].Components[2].Content,
    GetRootPart().Components[2].Components[2].Content.Bodies[0],
    GetRootPart().Components[2].Components[3].Content,
    GetRootPart().Components[2].Components[3].Content.Bodies[0],
    GetRootPart().Components[2].Components[4].Content,
    GetRootPart().Components[2].Components[4].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content,
    GetRootPart().Components[2].Components[5].Content.Bodies[0],
    GetRootPart().Components[2].Components[5].Content.Bodies[1],
    GetRootPart().Components[2].Components[6].Content,
    GetRootPart().Components[2].Components[6].Content.Bodies[0],
    GetRootPart().Components[2].Components[6].Content.Bodies[1],
    GetRootPart().Components[2].Components[7].Content,
    GetRootPart().Components[2].Components[7].Content.Bodies[0],
    GetRootPart().Components[2].Components[8].Content,
    GetRootPart().Components[2].Components[8].Content.Bodies[0],
    GetRootPart().Components[2].Components[9].Content,
    GetRootPart().Components[2].Components[9].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content,
    GetRootPart().Components[2].Components[10].Content.Bodies[0],
    GetRootPart().Components[2].Components[10].Content.Bodies[1]])
visibility = VisibilityType.Hide
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

SpaceClaimTesting.Scenario("Apply Fixed Support 1")

# Apply Fixed Support 1
selection = FaceSelection.Create([GetRootPart().Components[1].Components[1].Content.Bodies[0].Faces[39],
    GetRootPart().Components[1].Components[1].Content.Bodies[0].Faces[38],
    GetRootPart().Components[1].Components[1].Content.Bodies[0].Faces[40],
    GetRootPart().Components[1].Components[1].Content.Bodies[0].Faces[41]])
result = Conditions.Support.Create(selection, SupportType.Fixed)
# EndBlock

SpaceClaimTesting.Scenario("Solve Static Structural Simulation With Thermal Stress In Explore Stage")

# Start Solver in Explore Mode
Solution.Solver.StartExplore()
Solution.Solver.PauseExplore()
# EndBlock

# Validate Avg. Temperature Ribs Results 3
avgTempRibs = Results.Monitor.GetByLabel("Avg. Temperature Ribs")
SpaceClaimTesting.ValidateString("Avg. Temperature Ribs", avgTempRibs.Label, "Label", "Avg. Temperature Ribs - Explore Stage 3")
SpaceClaimTesting.ValidateDouble(1.0, avgTempRibs.Location.Count, "Location.Count", "Avg. Temperature Ribs - Explore Stage 3", 0)
SpaceClaimTesting.ValidateString("None", str(avgTempRibs.ResultComponent), "ResultComponent", "Avg. Temperature Ribs - Explore Stage 3")
SpaceClaimTesting.ValidateString("Average", avgTempRibs.ResultFunction.ToString(), "ResultFunction", "Avg. Temperature Ribs - Explore Stage 3")
SpaceClaimTesting.ValidateString("Temperature", avgTempRibs.ResultVariable.ToString(), "ResultVariable", "Avg. Temperature Ribs - Explore Stage 3")
ValidateMonitor(71.5075759887695, "DegreeCelsius", avgTempRibs.GetValue(ResultSource.Explore), "Temperature", "Avg. Temperature Ribs - Explore Stage 3", simulationResultTolerance)

# Validate Factor of Safety Results 3
factorOfSafety = Results.Monitor.GetByLabel("Factor of Safety")
SpaceClaimTesting.ValidateString("Factor of Safety", factorOfSafety.Label, "Label", "Factor of Safety - Explore Stage 3")
SpaceClaimTesting.ValidateDouble(1.0, factorOfSafety.Location.Count, "Location.Count", "Factor of Safety - Explore Stage 3", 0)
SpaceClaimTesting.ValidateString("None", factorOfSafety.ResultComponent.ToString(), "ResultComponent", "Factor of Safety - Explore Stage 3")
SpaceClaimTesting.ValidateString("Minimum", factorOfSafety.ResultFunction.ToString(), "ResultFunction", "Factor of Safety - Explore Stage 3")
SpaceClaimTesting.ValidateString("FactorOfSafety", factorOfSafety.ResultVariable.ToString(), "ResultVariable", "Factor of Safety - Explore Stage 3")
ValidateMonitor(0.169925492522671, "DecimalFraction", factorOfSafety.GetValue(Results.ResultSource.Explore), "Displacement", "Factor of Safety - Explore Stage 3", simulationResultTolerance)
