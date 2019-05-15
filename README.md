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





This text file was a YAML file, but due to the limitation of environment  parameters a more basic form was needed. Unfortunately, this means that editing this file may be more daunting for some. 

In order for the user to have flexibility in attribution, a text file is needed so that the user can define features to attribute. The config.txt file is used just for that purpose. In this config.txt file the user can edit names of fields and values which are representative of how the event table is structured and how attribution properties function in the application.

The config.txt file is a python dictionary, and in this dictionary there are three main pieces a 'polygonTable', 'displayTable', and 'eventTable'. Of these there are two objects the user can add to, and they are the "displayTable" and the "eventTable". The "polygonTable" should not be changed! To make changes to the config.txt file follow the example below.

This is what the config.txt file looks like:

------

```
{
'polygonTable': ['plotid', 'geo', 'json'], 
'displayTable': {
	'Comment': ['submit'], 
	'ChangeAgent': ['none', 'unknown', 'regrowth', 'fire', 'logging','flooding', 'pine bug', 'false reading'], 
	'YOD': ['year', 'false reading'], 
	'User': ['Peter', 'Katie'],
	'Confidance': ['low', 'med', 'high']}, 
'eventTable': ['plotId', 'obserId', 'LT_YOD', 'YOD', 'ChangeAgent', 'Confidance', 'User', 'Comment']
}
```

------

if we wanted to add a 'state' field to our table we would need to add " 'state', " to the 'eventTable' list. A list contain the values in the square brackets "[ ]". In the event table only add values after 'LT_YOD'. Once we add 'state' our event table line would look like this:

------

`'eventTable': ['plotId', 'obserId', 'LT_YOD', 'YOD', 'ChangeAgent', 'state', Confidance', 'User', 'Comment']`

------

you can add the " 'state', " value anywhere in the list aslong as it is after " 'LT_YOD', ". Next, if we want to be able to attribute our new feild we need to add a 'state' key to our display table object. The syntax is a key and value pair. The key stands alone in parenthesis with a colon after it followed by a list of values. In out case 'state' would be the key, and the state types would be our values as in the example below. 

------

 `'State': ['forest','urban','barren']`

------

you can add the key/value pair anywhere in the displaytables curly brackets '{ }'. Our new config.txt looks like this now.

```

{
'polygonTable': ['plotid', 'geo', 'json'], 
'displayTable': {
	'Comment': ['submit'], 
	'ChangeAgent': ['none', 'unknown', 'regrowth', 'fire', 'logging', 'flooding', 'pine bug', 'false reading'], 
	'YOD': ['year', 'false reading'], 
	'User': ['Peter', 'Katie'],\
	'State': ['forest','urban','barren']  <<<< new <<<<<
	'Confidance': ['low', 'med', 'high']}, 
'eventTable': ['plotId', 'obserId', 'LT_YOD', 'YOD', 'ChangeAgent', 'Confidance', 'state', 'User', 'Comment']
}
```

------

Be sure to save the config.txt file.

## Step 8: Start the App

The application location is in the TS-Plus folder in the base directory. In the TS-Plus folder there is a file named (ts name). Double click this file to open the TS-Plus application.



Once opened, a dialog box will appear and the user will need to locate the SQL database that was created in step 6. When the SQL file is found double click it and the dialog box will disappear. After a few moments the plot list will be populated with polygon or point identification values.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/01_DB_box.JPG' width="400">

Clicking on one of the plot list identification values, will render the spectral and spatial data for area the ID represents. This may take a few moments. Once loaded, the user will see that plot list ID value is highlighted, and spectral plot in the upper center is populated, and that there are several images chips with the same polygon geometry in the upper right bottom sections. 

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/02_plotlist.JPG' width="200"> 

The spectral plot shows the summary spectral values for the area represent by the point or polygon displayed. For visual purposes, the user can double click on two observation points to connect a line between them.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/03_specplot3.JPG' width="300">

More line segment can be added by continuing to double click on more observation points. To remove line segments double click on a already selected point.

The image chip in the upper right is different from the other images chips in that it show approximately current ariel imagery, topographical, and street base maps. 

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/04mainchip.JPG' width="200">

The user can change the base map by clicking the map icon in this image chip. The user can also remove the geometry in this image chip by unselecting the ROI option in the map icon.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/04mainchip3.JPG' width="200">

At the bottom of the application's display is a set of yearly spectral image maps with a geometry on top of them. This set of temporal images help the user get a feel for what the spectral plot is displaying and allow for more informed attribute selection.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/05imagechips.JPG' width="300">

The user can apply attributes to each plot ID by right clicking an observation in the spectral trajectory plot. This action will open a pop up box with several button that where defined by the user in the yaml file. When clicked these button open and show a selection of values that can be applied and saved to the event table in the SQL database. 

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/06savedata2.JPG' width="250">

If the comment/submit pair where applied in the yaml file the pop up box will have a comment button, and when clicked a comment box will expand in the pop up box. The user can add as much text as needed; however, when the user is done commenting the user need to click the submit button below the comment box. And once all associated values have been chosen the user will need to click the save button in order to record his or her attributes. 

All of the pop up button options need to have values selected in order to save them!

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/06savedata3.JPG' width="250">

To export the event table with saved attributes the user need to click on the Download CSV button in the header of the application. When clicked the user will be prompted with a dialog box asking where to save the CSV file. Once the user define a place the save the file a CSV file will appear there.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/07export.JPG' width="250">


