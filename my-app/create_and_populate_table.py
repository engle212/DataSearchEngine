#!/usr/bin/python

import psycopg2
from config import config
import pandas as pd


def create_and_populate(conn):
    columnList = ['data_id', 'file_path_year', 'remarks', 'date', 'farm_name', 'sensor_name', 'ground_control_points', 'spatial_resolution', 'fly_altitude', 'raw_images', 'bands', 'lat', 'lon', 'geom', 'file_path']
    """ create table in the PostgreSQL database"""
    #CREATE EXTENSION postgis;
    command = (
        """
        CREATE EXTENSION postgis;
        CREATE TABLE data_sets (
                data_id INTEGER PRIMARY KEY,
                file_path_year INTEGER NOT NULL,
                remarks VARCHAR(10000) NOT NULL,
                date DATE NOT NULL,
                farm_name VARCHAR(255) NOT NULL,
                sensor_name VARCHAR(255) NOT NULL,
                ground_control_points VARCHAR(3) NOT NULL,
                spatial_resolution FLOAT,
                fly_altitude FLOAT NOT NULL,
				raw_images VARCHAR(255),
                bands VARCHAR(255) NOT NULL,
                lat FLOAT(9) NOT NULL,
                lon FLOAT(9) NOT NULL,
                geom geometry,
				file_path VARCHAR(10000)
                )
        """     )
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        # create table
        cur.execute(command)

        # populate table with csv inFileDF     
        inFileDF = pd.read_csv('imageProperties.csv', skiprows=1, names=columnList, index_col=False).fillna(-1)

        insertStatement = '\nINSERT INTO data_sets ('
        
        insertStatement += ', '.join(columnList)
        insertStatement += ')\nVALUES'
        

        for i, row in inFileDF.iterrows():
            # add newline and ( to insertStatement
            insertStatement += '\n('
            # data_id and file_path_year
            insertStatement += str(row[0]) + ', ' + str(row[1]) + ', '
            insertStatement.join(str(row[0]) + ', ' + str(row[1]) + ', ')
            # remarks
            insertStatement += '\'' + str(row[2]) + '\', '
            # date "YYYY-MM-DD"
            date = row[3].split('.')
            insertStatement += '\'' + str(date[2]) + '-' + str(date[0]) + '-' + str(date[1]) + '\', '
            # farm_name
            insertStatement += '\'' + str(row[4]) + '\', '
            # sensor_name
            insertStatement += '\'' + str(row[5]) + '\', '
            # ground_control_points
            insertStatement += '\'' + str(row[6]) + '\', '
            # spatial_resolution and fly_altitude
            insertStatement += str(row[7]) + ', ' + str(row[8]) + ', '
            # raw_images
            insertStatement += '\'' + str(row[9]) + '\', '
            # bands
            insertStatement += '\'' + str(row[10]) + '\', '
            # lat and lon
            insertStatement += str(row[11]) + ', ' + str(row[12]) + ', '
            # geometry
            insertStatement += 'ST_GeomFromText(\'POINT(' + str(row[12]) + ' ' + str(row[11]) + ')\', 4326), '
            # file_path
            insertStatement += '\'' + str(row[14]) + '\')'
            if i + 1 < len(inFileDF.index):
                insertStatement += ', '
        insertStatement += ';'

        cur.execute(insertStatement)

        # commit the changes
        conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    params = config()
    conn = psycopg2.connect(**params)
    create_and_populate(conn)

