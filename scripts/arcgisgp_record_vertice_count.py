import arcpy


def getVertCount(featureclass):
    """
    return total record and vertice count

    Parameters
    ----------
    featureclass: Feature Class;
        feature class must be a polygon or point
    Returns
    -------
        int; number of records and vertices
    """
    desc = arcpy.Describe(featureclass)
    if desc.shapeType == "Polygon" or desc.shapeType == "Line":
        numberrecords = int(arcpy.GetCount_management(featureclass).getOutput(0))
        with arcpy.da.SearchCursor(featureclass, "SHAPE@") as cursor:
            totVert = 0
            for row in cursor:
                totVert += row[0].pointCount
        return numberrecords, totVert


input_fc = arcpy.GetParameterAsText(0)
counts = getVertCount(input_fc)

if counts is not None:
    arcpy.AddMessage('\n# Total number of records: {}'.format('{0:,}'.format(counts[0])))
    arcpy.AddMessage('\n# Total number of vertices: {}\n'.format('{0:,}'.format(counts[1])))
else:
    arcpy.AddMessage('\n# Not a polygon or line\n')