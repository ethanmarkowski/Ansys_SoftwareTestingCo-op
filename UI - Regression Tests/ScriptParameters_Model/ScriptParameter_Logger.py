# Python Script, API Version = V22 Beta

import os

filename = "ScriptParameters_Log.txt"

# Log all accessible script parameters and associated values to the given file path
def logParameters(logPath):
    parameters = [attribute for attribute in dir(Parameters) if not callable(getattr(Parameters, attribute)) and not attribute.startswith('__')]
    
    with open(logPath, 'a') as fileObj:
        for parameter in parameters:
            fileObj.write("{} = {}\n".format(parameter, getattr(Parameters, parameter)))
        fileObj.write('\n')

logParameters(os.getenv("TEMP") + '\\Discovery\\' + filename)