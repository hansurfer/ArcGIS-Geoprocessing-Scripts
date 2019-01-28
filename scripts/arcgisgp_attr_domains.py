import arcpy


def codeddomainDict(ws):
    """
    construct a dictionary with attribute domain code value and code desc

    Args:
        ws (str): workspace

    Returns:
        coded_dict (dict): a dictionary with code value and code desc
    """
    arcpy.env.workspace = ws
    # dictionary - {domain name lowercase: {code value: code desc}}
    coded_dict = {}
    domains = arcpy.da.ListDomains(ws)
    for domain in domains:
        if domain.domainType == 'CodedValue':
            coded_values = domain.codedValues
            temp_dict = {}
            for val, desc in coded_values.items():
                temp_dict[val] = desc
            coded_dict[domain.name.lower()] = temp_dict
        elif domain.domainType == 'Range':
            temp_dict = {}
            temp_dict['min'] = domain.range[0]
            temp_dict['max'] = domain.range[1]
            coded_dict[domain.name.lower()] = temp_dict

    return coded_dict


inputdatasets = arcpy.GetParameterAsText(0)
input_datasets = inputdatasets.split(";")
ws = arcpy.GetParameterAsText(1)

if arcpy.Describe(ws).workspaceType in ['LocalDatabase', 'RemoteDatabase'] :
    domaindicts = codeddomainDict(ws)

    for counter, dataset in enumerate(input_datasets, start=1):
        dataset = dataset.replace("'", "")
        desc = arcpy.Describe(dataset)
        arcpy.AddMessage(("\n# {} of {} : {}".format(counter, len(input_datasets), desc.baseName)))
        if desc.dataType == 'FeatureClass' or desc.dataType == 'Table':
            fields = arcpy.ListFields(dataset)
            # dictionary - {field name lowercase: domain name lowercase}
            fieldswithdomain = {field.name.lower():field.domain.lower() for field in fields if field.domain != ""}
            # all attribute elements
            for counter1, field in enumerate(fieldswithdomain):
                if counter1 > 0:
                    arcpy.AddMessage("  ")
                arcpy.AddMessage("    field name : {}".format(field))
                arcpy.AddMessage("    domain name: {}".format(fieldswithdomain[field]))
                domaincodelist = domaindicts[fieldswithdomain[field]]
                for ecodeddomain in domaincodelist.keys():
                    arcpy.AddMessage("                 {} : {}".format(ecodeddomain, domaincodelist[ecodeddomain]))
        else:
            arcpy.AddMessage("    !Not Feature Class or Table!")
    arcpy.AddMessage("  ")

else:
    arcpy.AddMessage("\n *---- Select file geodb or enterprise geodb ----* \n")
    exit()