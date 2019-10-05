import json
import re
import sqlite3
from sqlite3 import Error
from sys import platform
from collections import OrderedDict
#import yaml
# dialog box for paths
import Tkinter,tkFileDialog
#from Tkinter.filedialog import askopenfilename
import tkMessageBox
import os
import glob
import sys

#=============================================================================
yam = ''
jsonPath = ''
inputs_paths = [yam,jsonPath]
inpho = ["Please, find the location of the config.txt file. Click ok to continue to file path dialog box.", "Please, find the location of your geojson directory. Click ok to continue to file path dialog box."]

manSwitch = 1

if manSwitch == 1:
    for f in range(len(inputs_paths)):
       root = Tkinter.Tk()
       root.withdraw()
       tkMessageBox.showinfo("File Location", inpho[f])
       inputs_paths[f] = tkFileDialog.askopenfilename()

    yam = inputs_paths[0]
    database = os.path.dirname(inputs_paths[0])
    #print(database)
    #database = database+ "/"
    jsonPathDir = os.path.dirname(inputs_paths[1])
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        geojsons = glob.glob(jsonPathDir+"/"+"**.geojson")   #linux
    elif platform == "win32":
        geojsons = glob.glob(jsonPathDir+"\\"+"**.geojson") #windows
    #print(geojsons)

else:
#"""this the manual run option that does not use the Tkinter module."""
    yam = "/home/alpha/Desktop/TSP/tsp_projects/watershed/config.txt"
    jsonPath = "/home/alpha/Desktop/TSP/tsp_projects/watershed/geojsons2/"
    geojsons = glob.glob(jsonPath+"**.geojson")
    #jsonPath = "/vol/v1/proj/TimeSyncPlus/TimeSync/observations.geojson"
    database = "/home/alpha/Desktop/TSP/tsp_projects/watershed/"


#============================================================================
def openJson(jsonPath):
    with open(jsonPath, 'r+') as f:
        data = json.load(f)
    return data
#=============================================================================
def get_yaml(yam):
    a=''
    with open (yam,'r') as f:
        for line in f:
            line = line.strip()
            a+=line
    dataMap = eval(a)    
    return (dataMap)
#=============================================================================   
def create_connection(db_file):
    """ create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)

    return None
#=============================================================================
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
#=============================================================================
def input_values_table(conn, main):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    cur = conn.cursor()
    cur.execute(main)
    return cur.lastrowid
#=============================================================================
def sql_input_list(yam):

    # gets yaml data in the form of a dictionary
    dataMap = get_yaml(yam)
    
    # gets the keys and values as lists from the yaml dictionary
    tablenames =  list(dataMap.keys())
    fieldnames = list(dataMap.values())
    # since the display table has nest key/values they need to be removed and added later. 
    for q in fieldnames:
        
        if type(q) == dict:
            indexOut = fieldnames.index(q)
            fieldnames.remove(q)
            tablenames.append(tablenames[indexOut])
            del tablenames[indexOut]
            
    # blank list yaml dictionary values 
    templ = []
    addtext = []
    dropdown = []
    dropdownstrings = []
    # loops through the display table to get dropdown names and values. Remember they were removed above.
    for i in dataMap.keys():
        if i =='displayTable':
            for key,val in dataMap[i].items(): # keys are will be field names (state, change, etc) the values will be dropdown values (fire, flood, etc)
                dropdown.append(key)
                dropdownstrings.append(str(val).strip('[]'))	
    fieldnames.append(dropdown)
    
    # loops through yaml file dictionary and adds sql data type to column name
    for p in fieldnames:
        for q in p:
            add = q + ' text'
            templ.append(add)
        addtext.append(templ)
        templ = []
    
    # changes lists of lists of stringS into lists of lists of a string 
    fieldNamesWithText = [','.join(x) for x in addtext]

    # list of lists of column names
    fieldNames = [','.join(x) for x in fieldnames]
   
   
    return tablenames, fieldNamesWithText, fieldNames, tuple(dropdownstrings)
#=============================================================================

# makes a list of lists of yearly spectral observation for each polygon (needs to be called into a loop
# for each year) one loop for year 1985 will give spectral values for each polygon for that year.
def observation_value_list(data,year):
    year = str(year)
    templist = []
    templist2 = []
    #print(len(data['features']))# ---------------------maybe here to split in many databases-----nope
    counter = 1 
    for values in data['features']:
        if 1 == 2:
            break
        else:
     
            for key, value in sorted(values['properties'].iteritems()):
                if year in key:
                    templist.append(value)
                    #print (templist)
                    if len(templist) == 6:
                
                        templist.append(year)
                        #templist.append(values['id'])
                        try:
                            templist.append(str(values['properties']['uniqID']))
                        except KeyError:
                            templist.append(values['id'])
                        try:
                            templist.append(values['properties']['yod'])
                        except (KeyError, IndexError):
                            templist.append('none')
                            #print(templist)
                        
                        templist2.append(templist)
                        templist = []
        counter += 1
    
    return templist2
#print (observation_value_list(data, 2001)) # 1985 to 2017
#==========================================================================================
def observation_value_dict(startYear, end, data):

    """  here we rearange our input GEE json file. So, we start by looping a loop. the first
    loop (outter loop) iterates over our time series (1985 to 2017). the loop varible is used 
    in a function that returns a list of lists that are our yearly spectral infromation for each
    polygon. So, in start of the first loop we have a list of lists of spectral infromation for
    all polygons for 1985. In the next loop (inner loop) we iterate over the number of polygons
    in the json file. In this loop we are rearanging the spectral information to a structure 
    TimeSync and the tables want .  """

    sql_list = sql_input_list(yam)
    fieldnames = sql_list[2]
    
    mainlist = []
    obserlist = []

    while startYear <= 2018:  #  loops to the number of years 33
        templistB = observation_value_list(data,startYear)# list of lists of spectral information for all polygons for one year pre loop. 
        for i in range(end): # loops to the number of polygons 170 
            keys = ['b1', 'b2', 'b3', 'b4', 'b5', 'b7', 'cloud_cover', 'image_julday', 'image_year', 'plotid', 'project_id', 'selected', 'sensor', 'spectral_scaler', 'target_day','tcb', 'tcg','tcw', 'tsa', 'url', 'yod']
            values = [templistB[i][0], templistB[i][1], templistB[i][2], templistB[i][3], templistB[i][4], templistB[i][5], 0, '217', int(templistB[i][6]), templistB[i][7].encode("utf-8"), 1100, 'null', 'LT5', 10000, templistB[i][8], 0, 0, 0, 999999, 'another.png', templistB[i][8]]	
            q = dict(OrderedDict(zip(keys,values)))
            mainlist.append(q)           
        startYear += 1
        
    polyTab = []
    evenTab =[]
    obserTab = []
    
    for i in  range(end):
        """ make return tuple lists here for each table. maybe combine the function above
       	with this one to to make a master list of values for each table. """
        #-----------------------------------------------------------------
        try:
            coordinates = str(data['features'][i]['geometry']['coordinates'])
            featureType = str(data['features'][i]['geometry']['type'])
            geometry = "{'type':'"+featureType+"', 'coordinates':"+coordinates+"}"
            # project is a big tuple of the rearanged data
            project = (templistB[i][7].encode("utf-8"),geometry , re.sub(r'(?<!: )"(\S*?)"', '\\1',json.dumps(mainlist[i::end], sort_keys=True)).rstrip());
            #print('project', project)
            #print('project', type(project))
            polyTab.append(project)
        except KeyError:
            continue
    polygonData = str(polyTab).strip('[]')

    return polygonData, 'obserData', templistB
#==========================================================================================

def main():

    

    counter = 0
    for i in geojsons:
        data = openJson(i)
        # lists of table names, column names, and column names with datatypes 
        sql_list = sql_input_list(yam)
        tablenames = sql_list[0]
        fieldNamesWithText = sql_list[1]
        fieldNames = sql_list[2]
        dropdownstrings = str(sql_list[3]).replace("'", "")

        #startYear = 1986 # make this dynamic
        startYear = int(sorted(data['features'][0]['properties'])[0][0:4])
        #print (type(data))
        end = len(data['features'])

        defaultFeilds = 'id int PRIMARY KEY'

        # create a database connection
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            conn = create_connection(database+"/TSPdatabase"+str(counter+startYear)+".db")
        elif platform == "win32":
            conn = create_connection(database+"\TSPdatabase"+str(counter+startYear)+".db")
        counter += 1
        obser_val_dict = observation_value_dict(startYear, end, data) 
        polygonData = obser_val_dict[0]
        #obserData = obser_val_dict[1]
        templistB = obser_val_dict[2]
    
        # values to be inputted into table
        #print(polygonData[0])
        polygonTable = polygonData
        #print(type(polygonTable))
        #print(len(polygonTable))
        eventTable = ""
        #segTable = ""
        #obserTable = obserData
        displayTable = dropdownstrings
        print ('writing database from ' + i)
    
        # alot of stuff going on here, making sql commands, tables, and inputing values into tables
        for i, v  in zip(tablenames, fieldNamesWithText):
                create_table_sql = "CREATE TABLE IF NOT EXISTS  "+i+" ("+defaultFeilds+", "+v+");"
            
                if conn is not None:
                    # creates table
                    create_table(conn, create_table_sql)
                else:
                    print("Error! cannot create the database connection.")

        for i, e in zip(tablenames, fieldNames):
        
        
            if len(eval(i)) >= 2:
            
                main = 'INSERT INTO '+i+ '('+e+')  VALUES'+eval(i)+'; '
                #print(i)
                #print (main)
                if conn is not None:
                    with conn:
                        # inputs values into a table
                        input_values_table(conn, main)
                else:
                    print("Error! cannot create the database connection.")
            else:
                print (' ')
            #finds the number of columns
            lengt = (len(e.split(',')))
            tup = ()
            for t in range(lengt):
                tup = tup + ('no data',) 
            
            main = 'INSERT INTO '+i+ '('+e+')  VALUES'+str(tup)+'; '
            #print (main)
            if conn is not None:
                with conn:
                    # inputs values into a table
                    input_values_table(conn, main)
            else:
                print("Error! cannot create the database connection.")
    print('done')
if __name__ == '__main__':
    main()
