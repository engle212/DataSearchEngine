# DataSearchEngine

This project was created as part of my work as Research Assistant. It gave me valuable experience in web development and data handling.
I used Python to relay data to and from a PostgreSQL database and upload data to a GeoServer. 
The frontend of this project is implemented solely using JavaScript and the OpenLayers library.
The frontend code gets the data from the GeoServer in the form of GeoJSON and displays it cartographically to the user using OpenLayers.
Under the map display, a table of the selected points is shown when the user selects points by clicking or box selection.
When a point is selected, it is enlarged and highlighted on the map.

To use this project, supply a CSV file named ```imageProperties.csv``` into the ```my-app``` folder. Then set up a PostgreSQL server and a corresponding ```database.ini``` file in the ```my-app``` folder formatted like so:
```
[postgresql]
host=
database=postgres
user=
password=
```

Lastly, set up a GeoServer and change the ```geoserverComm.py``` file so its URL, username, and password match the GeoServer's.
