from fastkml import kml
from pykml import parser

with open('test.kml', 'rt', encoding="utf-8") as myfile:
    doc = myfile.readline()
    doc2 = myfile.readline()
print(doc)
print(doc2)
# print(len(doc))

# k = kml.KML()

# k.from_string(doc)

# features = list(k.features())
# features[0].features()
# f2 = list(features[0].features())
