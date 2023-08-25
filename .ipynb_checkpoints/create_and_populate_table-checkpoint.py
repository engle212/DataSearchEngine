#!/usr/bin/python

import psycopg2
from config import config
import pandas as pd

columnList = ['index', 'file_path_year', 'comments', 'date', 'farm_name', 'sensor_name', 'ground_control_points', 'spatial_resolution(m)', 'raw_images', 'bands', 'lat', 'lon', 'geometry', 'file_path']


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE data_sets (
                data_id INTEGER PRIMARY KEY,
                file_path_year INTEGER NOT NULL,
                remarks VARCHAR(10000) NOT NULL,
                date DATE NOT NULL,
                farm_name VARCHAR(255) NOT NULL,
                sensor_name VARCHAR(255) NOT NULL,
                ground_control_points VARCHAR(3) NOT NULL,
                spatial_resolution FLOAT(5),
                fly_altitude FLOAT NOT NULL,
				raw_images VARCHAR(255),
                bands VARCHAR(255) NOT NULL,
                lat FLOAT(9) NOT NULL,
                lon FLOAT(9) NOT NULL,
				file_path VARCHAR(10000),
                geom geometry
        """     )
       

    insertStatement =
    """
    INSERT INTO """
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        
        # populate table with csv inFileDF     
        dataFrame = pd.read_csv('imageProperties.csv', skiprows=1, names=columnList)
        
        medStr = 
        """)
        
        """
        
        insertStatement += ','.join(columnList)
        insertStatement += medStr
        vals = inFileDF.index.values
        
     vals in inFileDF:
            # add newline and ( to insertStatement
            insertStatement += '\n('
            # data_id and file_path_year
            insertStatement += row[0] + ', ' + row[1] + ', '
            # remarks
            insertStatement += '\"' + row[2] + '\", '
            # date "YYYY-MM-DD"
            date = row[3].split('.')
            insertStatement += '\"' + date[2] + '-' + date[0] + '-' + date[1] + '\", '
            # farm_name
            insertStatement += '\"' + row[4] + '\", '
            # sensor_name
            insertStatement += '\"' + row[5] + '\", '
            # ground_control_points
            insertStatement += '\"' + row[6] + '\", '
            # spatial_resolution and fly_altitude
            insertStatement += row[7] + ', ' + row[8] + ', '
            # raw_images
            insertStatement += '\"' + row[9] + '\", '
            # bands
            insertStatement += '\"' + row[10] + '\", '
            # lat and lon
            insertStatement += row[11] + ', ' + row[12] + ', '
            # geometry
            insertStatement += 'ST_GeomFromText(\"POINT(' + lon + ' ' + lat + ')\", 4326)), '
            # file_path
            insertStatement += '\"' + row[14] + '\")'
            if !next(vals, None):
                insertStatement += ', '
        insertStatement += ';'
        
        cur.execute(insertStatement)
            

        # commit the changes
        conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()