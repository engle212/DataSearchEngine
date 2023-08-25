from geo.Geoserver import Geoserver

def uploadShapeFileToGeoserver(file_path='C:\ShapeFiles\dataframe'):
    # Initialize
    geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')

    # Upload file
    geo.create_shp_datastore(path=file_path, store_name='data_sets', workspace='searchengine')

