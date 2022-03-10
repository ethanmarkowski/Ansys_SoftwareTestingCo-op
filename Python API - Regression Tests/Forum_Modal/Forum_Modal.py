# Test Name:    Forum_Modal
# Author:       Ethan Markowski
#
# Objective:    Validate the workflow of the Getting Started - Modal tutorial from the Discovery Forum
#
# Steps:        Open "Modal with Contact in Explore Mode.scdoc"
#               Hide and Suppress the Truck and Hardware
#               Enable Natural Frequency
#               Add a Fixed Support to the mounting holes of the Mounting Bracket
#               Convert each Contact Pair from the Bonded Contact (default) Condition to Permanently Bonded
#               ** The tutorial workflow goes on to modify the scopes of the Contact Conditions and set the default Contact type to Prevented. 
#                   These steps are not included in the test because scripting does not currently support modifying the Default Classification of the default Contact Condition and Bug 542557 is preventing the permanent Contact scopes from being modified as is done in the tutorial.
#               Add a Mode 1 Frequency Monitor
#               Set Testing Fidelity to 1,000,000, solve in Explore, validate Mode 1 Frequency Monitor
#               ** This first Explore Stage solve's results are currently being validated with a 20% tolerance due to result variance seen on some machines
#
#               Open "Tube Assembly Simplified.scdoc"
#               Apply a Fixed Support to each set of mounting holes
#               Apply a Remote Mass to the holes in the coupler near the origin of the global coordinate system. Mass = 2 kg, Origin = 0 m, 0 m, 0.2 m
#               Enable Natural Frequency
#               Add a Mode 1 Frequency Monitor
#               Set Testing Fidelity to 1,000,000, solve in Explore, validate Mode 1 Frequency Monitor
#               Switch to Refine Stage
#               Convert each Contact Pair between the mounting plates, brackets, and pipes in Bonded Contact (default) to Permanently Prevented
#               Create Fixed Joint Conditions at the mounting holes between the brackets and mounting plates
#               Set Fidelity to 0, solve in Refine, validate Mode 1 Frequency Monitor

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

SpaceClaimTesting.Scenario("Open \"Modal with Contact In Explore Mode.scdoc\"")

# Open Document
path = os.path.join(os.getenv("DISCO_TESTING_RESOURCES"), r"Unified\Geometry", "Modal with Contact in Explore Mode.scdoc")
File.Open(path)
# EndBlock

# Validate Geometry
SpaceClaimTesting.ValidateAll(42.0, 0, 1565.0, 0, 3371.0, 0, 0.1836992, 0.1836992*modelTolerance, 35.68066, 35.68066*modelTolerance, "Model Geometry 1 - After Loading")

# Validate Stage
SpaceClaimTesting.ValidateString("ExploreStage", Solution.Solver.GetCurrentStageIdentifier(), "CurrentStageIdentifier", "Solution.Solver - After Loading 1")

SpaceClaimTesting.Scenario("Modify Suppression And Visibility States")

# Suppress Physics
simulation = Solution.Simulation.GetByLabel("Simulation 1")
selection = BodySelection.Create(GetRootPart().Components[0].Content.Bodies[0])
simulation.SuppressBodies(selection,True)
# EndBlock

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[0].Content,
    GetRootPart().Components[0].Content.Bodies[0]])
visibility = VisibilityType.Hide
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

# Suppress Physics
simulation = Solution.Simulation.GetByLabel("Simulation 1")
selection = BodySelection.Create([GetRootPart().Components[1].Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Components[1].Content.Bodies[0],
    GetRootPart().Components[1].Components[2].Content.Bodies[0],
    GetRootPart().Components[1].Components[3].Content.Bodies[0],
    GetRootPart().Components[1].Components[4].Content.Bodies[0],
    GetRootPart().Components[1].Components[5].Content.Bodies[0],
    GetRootPart().Components[1].Components[6].Content.Bodies[0],
    GetRootPart().Components[1].Components[7].Content.Bodies[0],
    GetRootPart().Components[1].Components[8].Content.Bodies[0],
    GetRootPart().Components[1].Components[9].Content.Bodies[0],
    GetRootPart().Components[1].Components[10].Content.Bodies[0],
    GetRootPart().Components[1].Components[11].Content.Bodies[0],
    GetRootPart().Components[1].Components[12].Content.Bodies[0],
    GetRootPart().Components[1].Components[13].Content.Bodies[0],
    GetRootPart().Components[1].Components[14].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[1].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[2].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[3].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[4].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[5].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[6].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[1].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[2].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[3].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[4].Content.Bodies[0],
    GetRootPart().Components[1].Components[17].Content.Bodies[0],
    GetRootPart().Components[1].Components[18].Content.Bodies[0],
    GetRootPart().Components[1].Components[19].Content.Bodies[0],
    GetRootPart().Components[1].Components[20].Content.Bodies[0],
    GetRootPart().Components[1].Components[21].Content.Bodies[0],
    GetRootPart().Components[1].Components[22].Content.Bodies[0],
    GetRootPart().Components[1].Components[23].Content.Bodies[0],
    GetRootPart().Components[1].Components[24].Content.Bodies[0]])
simulation.SuppressBodies(selection,True)
# EndBlock

# Change Object Visibility
selection = Selection.Create([GetRootPart().Components[1].Content,
    GetRootPart().Components[1].Components[0].Content,
    GetRootPart().Components[1].Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Components[1].Content,
    GetRootPart().Components[1].Components[1].Content.Bodies[0],
    GetRootPart().Components[1].Components[2].Content,
    GetRootPart().Components[1].Components[2].Content.Bodies[0],
    GetRootPart().Components[1].Components[3].Content,
    GetRootPart().Components[1].Components[3].Content.Bodies[0],
    GetRootPart().Components[1].Components[4].Content,
    GetRootPart().Components[1].Components[4].Content.Bodies[0],
    GetRootPart().Components[1].Components[5].Content,
    GetRootPart().Components[1].Components[5].Content.Bodies[0],
    GetRootPart().Components[1].Components[6].Content,
    GetRootPart().Components[1].Components[6].Content.Bodies[0],
    GetRootPart().Components[1].Components[7].Content,
    GetRootPart().Components[1].Components[7].Content.Bodies[0],
    GetRootPart().Components[1].Components[8].Content,
    GetRootPart().Components[1].Components[8].Content.Bodies[0],
    GetRootPart().Components[1].Components[9].Content,
    GetRootPart().Components[1].Components[9].Content.Bodies[0],
    GetRootPart().Components[1].Components[10].Content,
    GetRootPart().Components[1].Components[10].Content.Bodies[0],
    GetRootPart().Components[1].Components[11].Content,
    GetRootPart().Components[1].Components[11].Content.Bodies[0],
    GetRootPart().Components[1].Components[12].Content,
    GetRootPart().Components[1].Components[12].Content.Bodies[0],
    GetRootPart().Components[1].Components[13].Content,
    GetRootPart().Components[1].Components[13].Content.Bodies[0],
    GetRootPart().Components[1].Components[14].Content,
    GetRootPart().Components[1].Components[14].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Content,
    GetRootPart().Components[1].Components[15].Components[0].Content,
    GetRootPart().Components[1].Components[15].Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[1].Content,
    GetRootPart().Components[1].Components[15].Components[1].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[2].Content,
    GetRootPart().Components[1].Components[15].Components[2].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[3].Content,
    GetRootPart().Components[1].Components[15].Components[3].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[4].Content,
    GetRootPart().Components[1].Components[15].Components[4].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[5].Content,
    GetRootPart().Components[1].Components[15].Components[5].Content.Bodies[0],
    GetRootPart().Components[1].Components[15].Components[6].Content,
    GetRootPart().Components[1].Components[15].Components[6].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Content,
    GetRootPart().Components[1].Components[16].Components[0].Content,
    GetRootPart().Components[1].Components[16].Components[0].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[1].Content,
    GetRootPart().Components[1].Components[16].Components[1].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[2].Content,
    GetRootPart().Components[1].Components[16].Components[2].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[3].Content,
    GetRootPart().Components[1].Components[16].Components[3].Content.Bodies[0],
    GetRootPart().Components[1].Components[16].Components[4].Content,
    GetRootPart().Components[1].Components[16].Components[4].Content.Bodies[0],
    GetRootPart().Components[1].Components[17].Content,
    GetRootPart().Components[1].Components[17].Content.Bodies[0],
    GetRootPart().Components[1].Components[18].Content,
    GetRootPart().Components[1].Components[18].Content.Bodies[0],
    GetRootPart().Components[1].Components[19].Content,
    GetRootPart().Components[1].Components[19].Content.Bodies[0],
    GetRootPart().Components[1].Components[20].Content,
    GetRootPart().Components[1].Components[20].Content.Bodies[0],
    GetRootPart().Components[1].Components[21].Content,
    GetRootPart().Components[1].Components[21].Content.Bodies[0],
    GetRootPart().Components[1].Components[22].Content,
    GetRootPart().Components[1].Components[22].Content.Bodies[0],
    GetRootPart().Components[1].Components[23].Content,
    GetRootPart().Components[1].Components[23].Content.Bodies[0],
    GetRootPart().Components[1].Components[24].Content,
    GetRootPart().Components[1].Components[24].Content.Bodies[0]])
visibility = VisibilityType.Hide
inSelectedView = False
faceLevel = False
ViewHelper.SetObjectVisibility(selection, visibility, inSelectedView, faceLevel)
# EndBlock

ViewHelper.ZoomToEntity(Selection.SelectAll())

SpaceClaimTesting.Scenario("Enable Natural Frequency")

# Natural Frequency on
simulation = Solution.Simulation.GetByLabel("Simulation 1")
simulation.EnableNaturalFrequency = True
# EndBlock

SpaceClaimTesting.Scenario("Apply Fixed Support 1")

# Apply Fixed Support 1
selection = FaceSelection.Create([GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[1],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[0],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[3],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[2]])
result = Conditions.Support.Create(selection, SupportType.Fixed)
# EndBlock

SpaceClaimTesting.Scenario("Convert Contact Groups")

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Bond
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create([GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[21],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[20],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[22],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[25],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[23],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[48],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[49],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[50],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[51]]), FaceSelection.Create([GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[1],
    GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[18],
    GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[94],
    GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[93],
    GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[0],
    GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[95],
    GetRootPart().Components[3].Components[0].Content.Bodies[0].Faces[92]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Bond
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create([GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[21],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[20],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[22],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[25],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[23],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[43],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[49],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[42],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[50]]), FaceSelection.Create([GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[21],
    GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[86],
    GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[95],
    GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[96],
    GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[89],
    GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[94],
    GetRootPart().Components[3].Components[1].Content.Bodies[0].Faces[97]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Bond
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create([GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[42],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[104],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[41],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[103],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[102]]), FaceSelection.Create([GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[21],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[20],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[24],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[25],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[45],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[44],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[49],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[46],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[47]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Bond
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create([GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[106],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[107],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[105],
    GetRootPart().Components[2].Components[1].Content.Bodies[0].Faces[108]]), FaceSelection.Create([GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[50],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[49],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[51],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[46],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[47],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[48]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Bond
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create([GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[59],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[57],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[58],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[60],
    GetRootPart().Components[2].Components[2].Content.Bodies[0].Faces[61]]), FaceSelection.Create([GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[396],
    GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[398],
    GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[395],
    GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[397],
    GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[399]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Bond
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create([GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[41],
    GetRootPart().Components[2].Components[0].Content.Bodies[0].Faces[40]]), FaceSelection.Create([GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[400],
    GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[401],
    GetRootPart().Components[3].Components[2].Content.Bodies[0].Faces[402]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

SpaceClaimTesting.Scenario("Add Mode 1 Frequency Monitor")

# Create Monitor
resultVariable = Results.ResultVariable.Frequency
resultFunction = Results.ResultFunction.Average
simulation=Solution.Simulation.GetCurrentSimulation()
result = Results.Monitor.Create(simulation, resultVariable, resultFunction)
# EndBlock

mode1 = result

# Set Fidelity Value
Solution.Solver.SetTestingFidelity(3e6)
# EndBlock

SpaceClaimTesting.Scenario("Solve In Explore Stage")

# Start Solver in Explore Mode
Solution.Solver.StartExplore()
Solution.Solver.PauseExplore()
# EndBlock

# Validate Mode 1 Frequency Results 1
SpaceClaimTesting.ValidateString("Mode 1 Frequency", mode1.Label, "Label", "Mode 1 Frequency - Geometry 1 - Explore Stage")
SpaceClaimTesting.ValidateDouble(1.0, mode1.Location.Count, "Location.Count", "Mode 1 Frequency - Geometry 1 - Explore Stage", 0)
SpaceClaimTesting.ValidateString("None", str(mode1.ResultComponent), "ResultComponent", "Mode 1 Frequency - Geometry 1 - Explore Stage")
SpaceClaimTesting.ValidateString("Average", mode1.ResultFunction.ToString(), "ResultFunction", "Mode 1 Frequency - Geometry 1 - Explore Stage")
SpaceClaimTesting.ValidateString("Frequency", mode1.ResultVariable.ToString(), "ResultVariable", "Mode 1 Frequency - Geometry 1 - Explore Stage")
SpaceClaimTesting.ValidateDouble(1.0, mode1.ModeNumber, "ModeNumber", "Mode 1 Frequency - Geometry 1 - Explore Stage", 0)
ValidateMonitor(9.69632720947266, "Hertz", mode1.GetValue(ResultSource.Explore), "Frequency", "Mode 1 Frequency - Geometry 1 - Explore Stage", 0.20)

SpaceClaimTesting.Scenario("Open \"Tube Assembly Simplified.scdoc\"")

# Open Document
path = os.path.join(os.getenv("DISCO_TESTING_RESOURCES"), r"Unified\Geometry", "Tube Assembly Simplified.scdoc")
File.Open(path)
# EndBlock

# Validate Geometry
SpaceClaimTesting.ValidateAll(9.0, 0, 152.0, 0, 370.0, 0, 0.0021073, 0.0021073*modelTolerance, 0.7696313, 0.7696313*modelTolerance, "Model Geometry 2 - After Loading")

# Validate Stage
SpaceClaimTesting.ValidateString("ExploreStage", Solution.Solver.GetCurrentStageIdentifier(), "CurrentStageIdentifier", "Solution.Solver - After Loading 2")

SpaceClaimTesting.Scenario("Apply Fixed Supports and Remote Mass")

# Apply Fixed Support 1
selection = PowerSelection.Faces.BySurfaceHoleRadius(FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[4]), 
	PowerSelectOptions(False), 
	SearchCriteria.SizeComparison.Equal)
result = Conditions.Support.Create(selection, SupportType.Fixed)
# EndBlock

# Apply Fixed Support 2
selection = PowerSelection.Faces.BySurfaceHoleRadius(FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[0]), 
	PowerSelectOptions(False), 
	SearchCriteria.SizeComparison.Equal)
result = Conditions.Support.Create(selection, SupportType.Fixed)
# EndBlock

# Apply Remote Mass 1
selection = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[7].Content.Bodies[0].Faces[2],
	GetRootPart().Components[0].Components[0].Components[0].Components[7].Content.Bodies[0].Faces[1]])
mass = MassQuantity.Create(2, MassUnit.Kilogram)
origin = Units.PointQuantity.Create(LengthQuantity.Create(0, LengthUnit.Meter), LengthQuantity.Create(0, LengthUnit.Meter), LengthQuantity.Create(200, LengthUnit.Millimeter))
result = Conditions.Mass.Create(selection, mass, origin)
# EndBlock

SpaceClaimTesting.Scenario("Enable Natural Frequency")

# Natural Frequency on
simulation = Solution.Simulation.GetByLabel("Simulation 1")
simulation.EnableNaturalFrequency = True
# EndBlock

SpaceClaimTesting.Scenario("Add Mode 1 Frequency Monitor")

# Create Monitor
resultVariable = Results.ResultVariable.Frequency
resultFunction = Results.ResultFunction.Average
simulation=Solution.Simulation.GetCurrentSimulation()
result = Results.Monitor.Create(simulation, resultVariable, resultFunction)
# EndBlock

mode1 = result

# Set Fidelity Value
Solution.Solver.SetTestingFidelity(3e6)
# EndBlock

SpaceClaimTesting.Scenario("Solve In Explore Stage")

# Start Solver in Explore Mode
Solution.Solver.StartExplore()
Solution.Solver.PauseExplore()
# EndBlock

# Validate Mode 1 Frequency Results 1
SpaceClaimTesting.ValidateString("Mode 1 Frequency", mode1.Label, "Label", "Mode 1 Frequency - Geometry 2 - Explore Stage")
SpaceClaimTesting.ValidateDouble(1.0, mode1.Location.Count, "Location.Count", "Mode 1 Frequency - Geometry 2 - Explore Stage", 0)
SpaceClaimTesting.ValidateString("None", str(mode1.ResultComponent), "ResultComponent", "Mode 1 Frequency - Geometry 2 - Explore Stage")
SpaceClaimTesting.ValidateString("Average", mode1.ResultFunction.ToString(), "ResultFunction", "Mode 1 Frequency - Geometry 2 - Explore Stage")
SpaceClaimTesting.ValidateString("Frequency", mode1.ResultVariable.ToString(), "ResultVariable", "Mode 1 Frequency - Geometry 2 - Explore Stage")
SpaceClaimTesting.ValidateDouble(1.0, mode1.ModeNumber, "ModeNumber", "Mode 1 Frequency - Geometry 2 - Explore Stage", 0)
ValidateMonitor(49.5433082580566, "Hertz", mode1.GetValue(ResultSource.Explore), "Frequency", "Mode 1 Frequency - Geometry 2 - Explore Stage", simulationResultTolerance)

SpaceClaimTesting.Scenario("Navigate To Refine Stage")

# Change Stage
Solution.Solver.SetStage("RefineStage")
# EndBlock

# Validate Stage
SpaceClaimTesting.ValidateString("RefineStage", Solution.Solver.GetCurrentStageIdentifier(), "CurrentStageIdentifier", "Solution.Solver - After Stage Switch")

SpaceClaimTesting.Scenario("Convert Contact Groups")

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Exclude
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[18]), FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[9],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[24],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[25],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[20]]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

# Convert Contact Group
contactGroup = Solution.Simulation.GetByLabel("Simulation 1").DefaultContactGroup
contactType = ContactGroupConversionType.Exclude
contactPairs = List[Connections.ContactPair]()
contactPair = Connections.ContactPair.Create(FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[5]), FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[11]))
contactPairs.Add(contactPair)
contactPair = Connections.ContactPair.Create(FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[5]), FaceSelection.Create(GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[10]))
contactPairs.Add(contactPair)
contactGroup.ChangeType(contactType, contactPairs, 0, False)
# EndBlock

SpaceClaimTesting.Scenario("Apply Fixed Joints")

# Apply Fixed Joint 1
selection1 = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[11],
	GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[0],
	GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[2],
	GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[13]])
selection2 = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[1],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[21],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[18],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[0]])
jointType = Connections.JointType.Fixed
result = Connections.Joint.Create(selection1,selection2,jointType)
# EndBlock

# Apply Fixed Joint 2
selection1 = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[1],
	GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[12],
	GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[10],
	GetRootPart().Components[0].Components[0].Components[0].Components[2].Content.Bodies[0].Faces[3]])
selection2 = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[5],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[7],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[6],
	GetRootPart().Components[0].Components[0].Components[0].Components[5].Content.Bodies[0].Faces[4]])
jointType = Connections.JointType.Fixed
result = Connections.Joint.Create(selection1,selection2,jointType)
# EndBlock

# Apply Fixed Joint 3
selection1 = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[19],
	GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[18],
	GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[20],
	GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[21]])
selection2 = FaceSelection.Create([GetRootPart().Components[0].Content.Bodies[0].Faces[18],
	GetRootPart().Components[0].Content.Bodies[0].Faces[2],
	GetRootPart().Components[0].Content.Bodies[0].Faces[1],
	GetRootPart().Components[0].Content.Bodies[0].Faces[21]])
jointType = Connections.JointType.Fixed
result = Connections.Joint.Create(selection1,selection2,jointType)
# EndBlock

# Apply Fixed Joint 4
selection1 = FaceSelection.Create([GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[23],
	GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[22],
	GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[24],
	GetRootPart().Components[0].Components[0].Components[0].Components[0].Components[1].Content.Bodies[0].Faces[25]])
selection2 = FaceSelection.Create([GetRootPart().Components[0].Content.Bodies[0].Faces[7],
	GetRootPart().Components[0].Content.Bodies[0].Faces[5],
	GetRootPart().Components[0].Content.Bodies[0].Faces[6],
	GetRootPart().Components[0].Content.Bodies[0].Faces[8]])
jointType = Connections.JointType.Fixed
result = Connections.Joint.Create(selection1,selection2,jointType)
# EndBlock

# Set Fidelity Value
Solution.Solver.SetFidelity(0)
# EndBlock

# Validate Solver Fidelity
SpaceClaimTesting.ValidateDouble(0.0, Solution.Solver.GetFidelity(), "GetFidelity", "Solution.Solver - Refine", 0.0)

SpaceClaimTesting.Scenario("Solve In Refine Stage")

# Start Solver in Refine Mode
Solution.Solver.StartRefine()
# EndBlock

# Validate Mode 1 Frequency Results 2
SpaceClaimTesting.ValidateString("Mode 1 Frequency", mode1.Label, "Label", "Mode 1 Frequency - Geometry 2 - Refine Stage")
SpaceClaimTesting.ValidateDouble(1.0, mode1.Location.Count, "Location.Count", "Mode 1 Frequency - Geometry 2 - Refine Stage", 0)
SpaceClaimTesting.ValidateString("None", str(mode1.ResultComponent), "ResultComponent", "Mode 1 Frequency - Geometry 2 - Refine Stage")
SpaceClaimTesting.ValidateString("Average", mode1.ResultFunction.ToString(), "ResultFunction", "Mode 1 Frequency - Geometry 2 - Refine Stage")
SpaceClaimTesting.ValidateString("Frequency", mode1.ResultVariable.ToString(), "ResultVariable", "Mode 1 Frequency - Geometry 2 - Refine Stage")
SpaceClaimTesting.ValidateDouble(1.0, mode1.ModeNumber, "ModeNumber", "Mode 1 Frequency - Geometry 2 - Refine Stage", 0)
ValidateMonitor(42.244329, "Hertz", mode1.GetValue(ResultSource.Refine), "Frequency", "Mode 1 Frequency - Geometry 2 - Refine Stage", simulationResultTolerance)