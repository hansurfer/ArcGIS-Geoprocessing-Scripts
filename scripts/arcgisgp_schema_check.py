import arcpy

skipfieldtype = ["Geometry", "GlobalID", "Guid", "OID", "Date"]
skipfieldname = ['shape_length', 'shape_area', 'shape.len', 'shape.area', 'shape']


def compareIntersect(x, y):
    return frozenset(x).intersection(y)


def compareDifference(x, y):
    return frozenset(x).difference(y)


def makeFieldDict(input_layer):
    lFields=arcpy.ListFields(input_layer)

    fieldDict = dict()
    for lf in lFields:
        # fieldDict[lf.name] = [lf.type, lf.length]
        fieldDict[lf.name.lower()] = [lf.type, lf.length] # change filenames to lower case
    return fieldDict


def baseName(input_layer, target_layer):
    """
    return input and target data basename.

    Parameters:
    input_layer: string
        input data full path. ex) "C:\Works\GEODB\Data_Load.gdb\NotaryPublicPt"
    target_layer: string
        target data full path. ex) "Database Connections\Connection to dcgisprd.dc.gov.sde\DCGIS.NotaryPublicPt"
    """
    if ".sde" in input_layer:
        # remove schema from name
        in_name = arcpy.Describe(input_layer).baseName.split(".")[1]
    else:
        in_name = arcpy.Describe(input_layer).baseName
    if ".sde" in target_layer:
        tar_name = arcpy.Describe(target_layer).baseName.split(".")[1]
    else:
        tar_name = arcpy.Describe(target_layer).baseName
    return in_name, tar_name


def checkSchema(input_layer, target_layer):
    """
    check schema of input and target dataset
    """
    arcpy.AddMessage("****** Checking Schema ******")
    input_dict = makeFieldDict(input_layer)
    target_dict = makeFieldDict(target_layer)

    # fields in both dataset
    combinedfield_list = (compareIntersect(input_dict.keys(), target_dict.keys()))
    arcpy.AddMessage("** Checking Fields List")
    # fields not in input
    missingfieldInputlist = (compareDifference(target_dict.keys(), input_dict.keys()))
    # fields not in target
    missingfieldTargetlist = (compareDifference(input_dict.keys(), target_dict.keys()))

    if (len(missingfieldTargetlist) + len(missingfieldInputlist)) == 0:
        arcpy.AddMessage("* All fields are presented in input and target")
    else:
        arcpy.AddMessage("* Field not in input layer:")
        for i in missingfieldInputlist:
            if i.lower() not in skipfieldname:
                arcpy.AddMessage("  {}".format(i))
        arcpy.AddMessage(" ")

        arcpy.AddMessage("* Field not in target layer:")
        for i in missingfieldTargetlist:
            if i.lower() not in skipfieldname:
                arcpy.AddMessage("  {}".format(i))
    arcpy.AddMessage("\n")

    # check field type
    arcpy.AddMessage("** Checking Field Type")
    fieldtypeList = [i for i in combinedfield_list if input_dict[i][0] <> target_dict[i][0]]
    if fieldtypeList:
        arcpy.AddMessage("* Found type mismatch in common fields")
        for i in fieldtypeList:
            arcpy.AddMessage ("  Field:{}".format(i))
            arcpy.AddMessage ("  Input:{} - Len:{}, Target:{} - Len:{}".format(input_dict[i][0], input_dict[i][1], target_dict[i][0], target_dict[i][1]))
        arcpy.AddMessage("Total {} field(s) type mismatch found".format(len(fieldtypeList)))
    else:
        arcpy.AddMessage("* No field type mismatch in common fields")
    arcpy.AddMessage("\n")

    # check field length
    arcpy.AddMessage("** Checking Field Lenght")
    fieldlenList = [i for i in combinedfield_list if input_dict[i][1] <> target_dict[i][1]]
    if fieldlenList:
        arcpy.AddMessage("* Found length mismatch in common fields")
        for i in fieldlenList:
            arcpy.AddMessage ("  Field:{}".format(i))
            arcpy.AddMessage ("  Input:{}, Target:{}".format(input_dict[i][1], target_dict[i][1]))
        arcpy.AddMessage("Total {} field(s) lenght mismatch found".format(len(fieldlenList)))
    else:
        arcpy.AddMessage("* No field lenght mismatch in common fields")
    arcpy.AddMessage("\n\n")


def main():
    inputTable = arcpy.GetParameterAsText(0)
    targetTable= arcpy.GetParameterAsText(1)

    inputDesc = arcpy.Describe(inputTable)
    targetDesc = arcpy.Describe(targetTable)

    if (inputDesc.dataType in ("FeatureClass", "Table")) & (targetDesc.dataType in ("FeatureClass", "Table")):
        names = baseName(inputTable, targetTable)
        arcpy.AddMessage("****** Checking Data Name ******")
        if names[0] == names[1]:
            arcpy.AddMessage ("Input and Target have same name\n\n")
        else:
            arcpy.AddMessage ("Input and Target have different Name")
            arcpy.AddMessage("{} : {}\n\n".format(names[0], names[1]))

        checkSchema(inputTable, targetTable)
    else:
        arcpy.AddMessage("****** Input is not Feature Class or Table ******")

if __name__ == '__main__':
    main()