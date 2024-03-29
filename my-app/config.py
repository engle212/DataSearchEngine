#!/usr/bin/python
from configparser import SafeConfigParser
import os

def config(filename='database.ini', section='postgresql'):
    filename = os.path.abspath(os.pardir) + '\\PythonPostgres\\my-app\\' + filename
    print(filename)
    # Create a parser
    parser = SafeConfigParser()
    # Read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if os.path.isfile(filename):
      if parser.has_section(section):
          params = parser.items(section)
          for param in params:
              db[param[0]] = param[1]
      else:
          raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    else:
      raise Exception(filename + ' file not found')
    return db