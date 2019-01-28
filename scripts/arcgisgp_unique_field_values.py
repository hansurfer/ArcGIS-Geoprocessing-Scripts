# https://gis.stackexchange.com/questions/138263/how-do-i-count-occurrences-of-unique-field-values
import arcpy

def constructDict(table, fields):
    """
    construct a dictionary with table name and field values

    Args:
        table (str): table full path.
        fields (str): field names, separated by ';'

    Returns:
        vDict (dict): a dictionary with table name key and field values
    """
    vDict = dict((fname, []) for fname in fields)
    with arcpy.da.SearchCursor(table, fields) as cursor:
        for row in cursor:
            for i in range(len(row)):
                vDict[fields[i]].append(row[i])
    return vDict


def uniquevalues(valueDict):
    """
    print unique value count

    Args:
        valueDict (dict): a dictionary with table name key and field values
    """
    for fname in valueDict:
        arcpy.AddMessage("\nField: {}".format(fname))
        arcpy.AddMessage("unique:")
        occurances = valueDict[fname]
        for i in sorted(set(occurances)):
            icount = occurances.count(i)
            if i is None:
                arcpy.AddMessage("    None: 0")
            elif isinstance(i, str):
                arcpy.AddMessage("    {}: {}".format(i.encode('utf-8'), icount))
            else:
                arcpy.AddMessage("    {}: {}".format(i, icount))


inputtable = arcpy.GetParameterAsText(0)
fields = arcpy.GetParameterAsText(1)

fieldList = fields.split(";")

numberrecords = int(arcpy.GetCount_management(inputtable).getOutput(0))
uniquevalues(constructDict(inputtable, fieldList))

arcpy.AddMessage("    ")