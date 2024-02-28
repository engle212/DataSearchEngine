# DataSearchEngine

Python was used to relay data to and from a PostgreSQL database and upload data to a GeoServer. 
The frontend of this project is implemented solely using JavaScript and the OpenLayers library.
The frontend code gets the data from the GeoServer in the form of GeoJSON and displays it cartographically to the user using OpenLayers.
Under the map display, a table of the selected points is shown when the user selects points by clicking or box selection.
When a point is selected, it is enlarged and highlighted on the map.

## Instructions

To use this project, supply a CSV file named `imageProperties.csv` into the `my-app` folder. Then set up a PostgreSQL server and a corresponding `database.ini` file in the `my-app` folder formatted like so:
```
[postgresql]
host=
database=postgres
user=
password=
```
This `database.ini` file is likely already created. If it is present in the `my-app` folder, fill in the fields with the credentials used to set up the postgreSQL server.

Set up a GeoServer and change the `geoserverComm.py` file so its URL, username, and password match the GeoServer's.

If launching the website for the first time, you will need to run `create_and_populate_table.py` to load the data into PostgreSQL, and synchronize it with the GeoServer.

Whenever the data in imageProperties.csv is changed, run the `update.py` file before starting the website.

The site is ready to go after completing the all of the previous instructions.

To run the website, cd into the my-app directory in a terminal. Then run the `!npm run build` command. Lastly, run the `npm start` command. The website should now be up and running locally, follow the link to the website provided by the command line's output.

Below is a link to instructions on how to set up GeoServer.
https://docs.geoserver.org/main/en/user/installation/win_binary.html

To set up PostgreSQL, follow the instructions in the subsequent link.
https://www.postgresql.org/docs/current/install-binaries.html

This project is available as a GitHub repository at the following link. 
https://github.com/engle212/DataSearchEngine
