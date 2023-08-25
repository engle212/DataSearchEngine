import psycopg2
import shapely
import shapely.wkt
import geopandas as gpd
from config import config

def query_data(conn, uri, columns=['*'], buffer=[]):
    """ Connect to the PostgreSQL database server """
    try:
        # create a cursor
        cur = conn.cursor()
        
        queryStatement = 'SELECT ' + str(', '.join(columns)) + ' FROM data_sets'

        # check if buffer info has been passed in
        if (len(buffer) > 0):
            queryStatement += ' WHERE ST_DWithin(geom, \'SRID=4326;POINT(' + str(buffer[1]) + ' ' + str(buffer[0]) + ')\', ' + str(buffer[2]) + ')'

        queryStatement += ' ORDER BY data_id ASC;\n'
            
    	# execute query statement
        cur.execute(queryStatement)
        geoDF = gpd.GeoDataFrame.from_postgis(queryStatement, conn, index_col=None)
        geoDF.to_crs(4326, inplace=True)
        print(geoDF.to_string())

        geoDF['date']=geoDF['date'].astype(str)

        #geoDF.to_file('dataframe.json', driver='GeoJSON')
        geoDF.to_file('C:\\ShapeFiles\\dataframe', mode='w')

        return geoDF
       
       # 1 degree = 111km
    	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    params = config()
    conn = psycopg2.connect(**params)
    #query_data(conn)