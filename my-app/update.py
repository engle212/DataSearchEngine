import psycopg2
import geopandas as gpd
from config import config
from create_and_populate_table import create_and_populate
from query import query_data
from geoserverComm import uploadShapeFileToGeoserver

columnList = ['data_id', 'file_path_year', 'remarks', 'date', 'farm_name', 'sensor_name', 'ground_control_points', 'spatial_resolution', 'fly_altitude', 'raw_images', 'bands', 'lat', 'lon', 'geom', 'file_path']

#             latitude  longitude  radius
queryBuffer = [39.9612, -82.9988, 5]

def update():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        strURI = 'postgres://' + params['user'] + ':' + params['password'] + '@' + params['host'] + '/' + params['database']

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        #create_and_populate(conn)
        
        result = query_data(conn, strURI, columnList, queryBuffer)

        # Upload and publish data to GeoServer
        uploadShapeFileToGeoserver()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    update()
