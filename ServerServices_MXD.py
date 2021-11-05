import urllib, urllib2, json, arcpy, getpass

##UPDATE VARIABLES

##Username
username = ""
##Password
password = ""
##Server name which is the Full Computer Name as found in Control Panel>System and Security>System
server = ""
##Update to use name of feature class or name of feature dataset
searchString = ""

##END UPDATE VARIABLES

##Get new token from server admin and paste below:
token = ""

baseUrl = "https://{}:6443/arcgis/admin/services".format(server)

def parseServices(searchName):
    dataSource = json.load(urllib2.urlopen(manifestUrl))
    try:
        current_map = dataSource['resources'][0]['onPremisePath']
        try:  
            if current_map.endswith('.mxd'):
                current_mxd = arcpy.mapping.MapDocument(current_map)
                for lyr in arcpy.mapping.ListLayers(current_mxd):
                    if lyr.supports("DATASOURCE"):
                        if searchName in lyr.dataSource:
                            print("\t" + str(service['serviceName']) + "|" + dataSource['resources'][0]['onPremisePath'] + "|" + lyr.dataSource)

                        
        except Exception as e:
            print("\nFailed on: " + current_map)
            print(e)
            
    except KeyError:
        print("Key Error\n")

        
##Root folder
catalog = json.load(urllib2.urlopen(baseUrl + "/" + "?token=" + token + "&f=json"))
print("ROOT")
services = catalog['services']
for service in services:
    if service['type']!= 'StreamServer':
        manifestUrl = baseUrl + "/" + service['serviceName'] + '.' + service['type'] + "/iteminfo/manifest/manifest.json" + "?token=" + token + "&f=json"
        parseServices(searchString)

##All other folders
folders = catalog['folders']
for folderName in folders:
    if str(folderName) not in ('System', 'Utilities', 'DataStoreCatalogs'):
        print(str(folderName))
        catalog = json.load(urllib2.urlopen(baseUrl + "/" + folderName + "/" + "?token=" + token + "&f=json"))
        services = catalog['services']
        parseServices(searchString)
        for service in services:
            if service['type']!= 'StreamServer':
                manifestUrl = baseUrl + "/" + str(folderName) + '/' + service['serviceName'] + '.' + service['type'] + "/iteminfo/manifest/manifest.json" + "?token=" + token + "&f=json"
                parseServices(searchString)


