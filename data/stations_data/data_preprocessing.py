import xml.etree.ElementTree as ET
import pandas as pd

root = ET.parse("cycle_hire-stations_2023-03-29_04-30.xml").getroot()

data = []
for child in root:
    data.append( [ subchild.text for subchild in child ] )

cols = []
for subchild in root[0]:
    cols.append( subchild.tag )

df = pd.DataFrame( data=data, columns=cols )

df.to_csv("cycle_hire-stations_2023-03-29_04-30.csv")
