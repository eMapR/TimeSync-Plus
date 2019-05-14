# TimeSync-Plus
TimeSync+ is an application for gathering point and polygon spectral temporal information from Landsat time series data into a database.

## About 

TimeSync+ is a desktop application modeled after the original [TimeSync application](http:example.com) that was originally developed as a validation tool for the [LandTrendr](http:example.com) spectral-temporal segmentation algorimth. Since its inception, its utility has grown beyond a segmentation validation tool. It is also useful for exploring know or predicted change events on the landscape and for collecting information about individual observations in time. TimeSync-Plus better handles these two significant use cases (event and observations information collection) more explicilty and greatly expands flexibity for user to define what tpyes of information should be recorded.

### Improvements:
- Slippy map zoom and pan image chips
- Four RGB image chip display option
- Total user-control over what information can be collected
- Two new data collection modes: event and observation (original segmentation as well)
- a context map
- Modern web-like interface
- Uses Google Earth Engine to process data


## Step 1: Make a shapefile

Make a point or polygon shapefile. Either generate your own or use the [LT-ChangeDB](http:example.com) process.

Needs to have a unique ID field - needs to be noted and entered into following Earth Engine script


## Step 2: Upload the shapefile to Google Earth Engine

1. Get an EE account
2. Upload Asset 
3. 

## Step 3: Run Google Earth Engine Script to generate data

## Step 4: Run Google Earth Engine Script to generate data

## Step 5: Download data from Google Drive

directory structure

- TS-Event-py27
  - create_sql_DB.py
  - config.yaml
  - TS_DB.db
  - TS-Event.exe
  - tiles
    - gdal2tiles.py
    - make_rgb_tms.py
    - TimeSync
      - observatios.geojson
      - observationsInfo.geojson
      - rgb432
      - rgb543
      - rgb654
      - rgbTC
      - tms



## Step 6: Run Python data prep script
There are three python scripts one that creates a SQL data-base (`create_sql_db.py`), and others parcel up the time series images into tiles (`make_rgb_tms.py`). There are located in two different folders in the directory structure. `create_sql_db.py`is located at the base of the directory and `make_rgb_tms.py` and its dependent script is located in the “tiles” folder, which is located in the base directory.

 

`make_rgb_tms.py` only needs to know the location of the “TimeSync” folder , which contains the downloaded images and the geojson files.



`create_sql_db.py` has two inputs, first,  a yaml or text file and a geojson file. The yaml file is located in the base directory. The geojson file is outputted with the Google Earth Engine images that where downloaded in step 5 and should be in “TimeSync” folder which is in the “tiles” directory.  

------

To Run `make_rgb_tms.py`: open your LT-Change-DB command prompt and go to tiles folder then add and run:

​            `python make_rgb_tms.py ./TimeSync`

 

This process will create a “tms” folder that will house the tile images.

------

To Run the “create_sql_db.py”: in your LT-Change-DB command prompt add and run:

 

​            `python create_sql_db.py`

 

Once running it will prompt you to find the locations of the yaml file and the location of the observations.geojson with file path dialog boxes. Once completed a sql database will be located in the base directory.

------

 

 

   



## Step 7: Edit App options YAML file

The YAML file is how the user will customize the application for the editing needs. This is done by defining field names for the created event table and the corresponding buttons and drop down values. 

1. Polygon section:
   - This section should **not** be edited by the users.
   - The polygon section is contains information for the Time Sync application (spectral values, geometries, etc.)
2. Display section :
   - The user will edit this section.
   - This section is where the user will define what editable fields they will have in the Time Sync application and the values that can be attributed to them.  
   - Special keywords: 
     - Comment :
       - If the user wants to add text comments the value submit is needed as the value like in the example below.
     - YOD
       - If the user needs a dynamic way to add year values to the yaml file the 'year' value dynamic add year values to the drop down when an observation is selected. 
   - Structure:
     -  Image example of the display section:

![](\display_example.JPG)

1. Event Section:

   - The user will edit this section.
   - In the event section the user added the editable fields. This field names need to match the ones the user added in the display section. 

2. Format Notes:

   - Uses 4 spaces for one indentation. 


   - No spaces between words for field values.
   - Fields names need a colon at the end of them.
   - values can have spaces between words.
   - Number values need parentheses.
 
## Step 8: Start the App








