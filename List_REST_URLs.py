import urllib, urllib2, json

##This is a quick throw together that returns the REST URL for published services using string concatenation
##as there was a question regarding this process during the 2021 SWOGIS GIS Day presentation


# Variables
username = ""
password = ""

##Just use the server name not the full computer name
server = ""

#Update token from server admin
token = ""

##Update protocol and domain appropriately
baseUrl = ""

try:
    
    catalog = json.load(urllib2.urlopen(baseUrl + "/" + "?token=" + token + "&f=json"))
    print("ROOT")
    services = catalog['services']
    for service in services:
        if service['type']!= 'StreamServer':
            print('\t Service Name: ' + str(service['serviceName']))
            manifestUrl = baseUrl + "/" + service['serviceName'] + '.' + service['type'] + "/iteminfo/manifest/manifest.json" + "?token=" + token + "&f=json"
            dataSource = json.load(urllib2.urlopen(manifestUrl))
            print('\t\t Rest URL: ' + baseUrl.replace('admin','rest') + "/" + str(service['serviceName']) + '/MapServer')
            print('\t\t Original Document: ' + dataSource['resources'][0]['onPremisePath'])

    folders = catalog['folders']
    for folderName in folders:
        if str(folderName) not in ('System', 'Utilities', 'DataStoreCatalogs', 'Hosted', 'GeoEvent'):
            print(str(folderName))
            catalog = json.load(urllib2.urlopen(baseUrl + "/" + folderName + "/" + "?token=" + token + "&f=json"))
            services = catalog['services']
            for service in services:
                print('\t Service Name: ' + str(service['serviceName']))
                manifestUrl = baseUrl + "/" + str(folderName) + '/' + service['serviceName'] + '.' + service['type'] + "/iteminfo/manifest/manifest.json" + "?token=" + token + "&f=json"
                dataSource = json.load(urllib2.urlopen(manifestUrl))
                print('\t\t Rest URL: ' + baseUrl.replace('admin','rest') + "/" + str(folderName) + '/' + str(service['serviceName']) + "/MapServer")
                print('\t\t Original Document: ' + dataSource['resources'][0]['onPremisePath'])
                
except Exception as e:
    import traceback, sys
    tb = sys.exc_info()[2]
    print "Line %i" % tb.tb_lineno 
    print e.message
