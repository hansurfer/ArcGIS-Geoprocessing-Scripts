import arcpy

# Script arguments
inputtable = arcpy.GetParameterAsText(0)
target_field = arcpy.GetParameterAsText(1)
fld_length = arcpy.GetParameterAsText(2)

inputDesc = arcpy.Describe(inputtable)

if inputDesc.dataType in ("FeatureClass", "Table"):
    # set list of OID and target field
    replace_fields = ['OID@', target_field]
    # dictionary of OID and target field value
    valueDict = {r[0]: r[1] for r in arcpy.da.SearchCursor(inputtable, replace_fields)}
    # update cursor
    with arcpy.da.UpdateCursor(inputtable, replace_fields) as cursor:
        arcpy.AddMessage("delete {} field".format(target_field))
        arcpy.DeleteField_management(inputtable, target_field)
        arcpy.AddMessage("add {} field".format(target_field))
        arcpy.AddField_management(inputtable, target_field, field_type = 'TEXT', field_length = int(fld_length))
        arcpy.AddMessage("update field value")
        for row in cursor:
            # set value to the new field
            row[1] = valueDict[row[0]]
            cursor.updateRow(row)
    arcpy.AddMessage("Finished")

else:
    arcpy.AddMessage("****** Input is not Feature Class or Table ******")