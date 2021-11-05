from IPython.display import display
import arcgis, getpass
from arcgis.gis import GIS
from arcgis.mapping import WebMap

##Refer to the article below if wanting to modify search item types
##https://support.esri.com/en/technical-article/000024383

##administrator username
username = ""
##password for administrative user
password = ""
##site you are querying, for example: https://domain/portal/home
site = ""


##Populate Services list
services = []

try:

    gis = GIS(site, username, password)
    ##item_type can be either: Web Mapping Application, Web Map, Map(returns results for Web Maps and Web Apps) or Feature Service
    items = gis.content.search(query="",item_type="Web Map", max_items=1000)

    item_list = []
    for i in items:
        if i is not None:
            webmap_json = i.get_data()
            for layer in webmap_json['operationalLayers']:
                for service in services:
                    if layer.get('url') is not None and service in layer.get('url'):
                        if not i in item_list:
                            item_list.append(i)
    for item in item_list:
        print(item)

except Exception as e:
    import traceback, sys
    tb = sys.exc_info()[2]
    print(e)
    print("Line %i" % tb.tb_lineno)
