import arcpy

# Script arguments
inputtable = arcpy.GetParameterAsText(0)
TargetField = arcpy.GetParameterAsText(1)
Field_Type = arcpy.GetParameterAsText(2)
Field_Length = arcpy.GetParameterAsText(3)

inputDesc = arcpy.Describe(inputtable)

if inputDesc.dataType in ("FeatureClass", "Table"):
    # set list of OID and target field
    replace_fields = ['OID@', TargetField]
    # dictionary of OID and target field value
    valueDict = {r[0]: r[1] for r in arcpy.da.SearchCursor(inputtable, replace_fields)}
    # update cursor
    with arcpy.da.UpdateCursor(inputtable, replace_fields) as cursor:
        arcpy.AddMessage("delete {} field".format(TargetField))
        arcpy.DeleteField_management(inputtable, TargetField)
        arcpy.AddMessage("add {} field".format(TargetField))
        arcpy.AddField_management(inputtable, TargetField, field_type=Field_Type, field_length=Field_Length)
        arcpy.AddMessage("update field value")
        for row in cursor:
            # set value to the new field
            row[1] = valueDict[row[0]]
            cursor.updateRow(row)
    arcpy.AddMessage("Finished")

else:
    arcpy.AddMessage("****** Input is not Feature Class or Table ******")


