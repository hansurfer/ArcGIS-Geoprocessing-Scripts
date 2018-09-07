# https://gis.stackexchange.com/questions/138263/how-do-i-count-occurrences-of-unique-field-values
import arcpy

inputtable = arcpy.GetParameterAsText(0)
fields = arcpy.GetParameterAsText(1)

def uniquevalues(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        occurances = [row[0] for row in cursor]
    for i in sorted(set(occurances)):
        icount = occurances.count(i)
        if i is None:
            arcpy.AddMessage("    None: 0")
        else:
            arcpy.AddMessage("    {}: {}".format(i.encode('utf-8'), icount))


fieldList = fields.split(";")

for field in fieldList:
    arcpy.AddMessage("\nField: {}".format(field))
    arcpy.AddMessage("unique:")
    uniquevalues(inputtable, field)