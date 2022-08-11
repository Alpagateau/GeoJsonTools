import json as js
import geoJ
from zipfile import ZipFile

#opens the json file
f = open("file.json", "r")
#decodes it as an object
obj = js.loads(f.read())

#some debug
print(obj.keys())
print(obj["_id"])
print(obj["datasets"][0]["results"][0]["situacao"])

#select only the results
results = obj["datasets"][0]["results"]
ATfiles = []

#create a list of all AT files
for i in range(len(results)):
    print(i / len(results))
    if (results[i]["situacao"] == "AT"):
        ATfiles += [results[i]]

poligons = [ATfiles[i]["poligono"] for i in range(len(ATfiles))]

#convert multipolygon into one polygone only
for i in range(len(poligons)):
    a = js.loads(poligons[i])
    if len(a["coordinates"]) == 1:
        a["type"] = "Polygon"
        a["coordinates"] = a["coordinates"][0]
    poligons[i] = a

print(len(poligons))
#creates a normal form of a feature list
featureList = {"type": "FeatureCollection", "features": []}

for i in range(len(poligons)):
    featureList["features"] += [{
        "id": str(i),
        "type": "Feature",
        "properties": {
            "col1": "name2"
        },
        "geometry": poligons[i],
    }]

a = geoJ.GeoJ(str(js.dumps(featureList)), True)

g = open("demofile2.json", "a")
g.write(str(js.dumps(featureList)))
g.close()

a.toShp("shape")

# create a ZipFile object
zipObj = ZipFile('shape.zip', 'w')
# Add multiple files to the zip
zipObj.write('shape.shx')
zipObj.write('shape.shp')
zipObj.write('shape.prj')
zipObj.write('shape.dbf')
# close the Zip File
zipObj.close()
