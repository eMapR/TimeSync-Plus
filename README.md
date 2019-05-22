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

Needs to have a unique ID field called "uniqID" - needs to be noted and entered into following Earth Engine script


## Step 2: Upload the shapefile to Google Earth Engine

1. Get an EE account
2. Upload shapefile Asset as table 

## Step 3: Run Google Earth Engine Script to generate data
Once you have made it to the [Google Earth Engine IDE](https://code.earthengine.google.com/) copy and paste the javascript file "TS_Plus_GetData.js" into the Google Earth Engine console. "TS_Plus_GetData.js" can be found in the GEE_JS directory here on Github.

Before running the GEE script to generate images and observation data you need to make sure the feature collection file path points to your uploaded asset, and that the feature ID string is "uniqID". The feature collection path looks like:

`lcb.props['featureCollection'] = 'your/asset/location'`

and the feature ID looks like:

`lcb.props['featureID'] = 'uniqID'`

Next click "Run" at the top of the console.


After a few moments the console tab should turn yellow and object will be appear under the tasks tab.

<img src ='https://github.com/eMapR/TimeSync-Plus/blob/master/images/gee3.JPG' width = 300>

These tasks represent the images and geometries/data files that will be used in Time Sync Plus. You will see that there are four different 'rgb' images and three 'observation' files.   Click the 'Run' button for which ever images you like, but you'll need to run the tasks for all the observation files. After Clicking the 'Run' button you will be prompted with a dialog 
box that looks like this:

<img src ='https://github.com/eMapR/TimeSync-Plus/blob/master/images/gee4.JPG' width = 300>

Here, you can define where the files and images get saved. Please, keep the default file names.




## Step 4: Download data from Google Drive

Once all the tasks are completed there will be a folder in your Google Drive called TimeSync. To download the folder right click it and select download. This will create a zip folder and it will be downloaded to your computer. Make a new folder on your computer and name it 'tiles'. Then extract all the contents of the zip folder to 'tiles'.

Next, you'll need to download the python files in our python folder, but it easier to just download the whole Time Sync Plus directory that way you have the files ready to go. You can do this by clicking the green button near the top of the page. Anyway, download them and then place 'gdal2tiles.py' and 'make_rgb_tms.py' in the 'tiles' folder so it looks like this:

<img src ='https://github.com/eMapR/TimeSync-Plus/blob/master/images/folder.JPG' width = 300>


## Step 5: Run Python data prep script

To Run `make_rgb_tms.py`: open your LT-Change-DB command prompt and go to tiles folder using the change directory command 'cd', and then add and run:

​            `python /full/file/path/to/tiles/make_rgb_tms.py /full/file/path/to/tiles/TimeSyncfolder`

 

This process will create a “tms” folder that will house the tile images.

------
Once your done with the above process you'll need to make a new folder called 'TS-Plus' and place the 'tiles' directroy in it. TS-Plus will be the base of the directory and this where the config.txt file should be place along with 'create_sql_db.py' file and the 'TimeSyncPlus' application folder. the base directory should look like this:

<img src ='https://github.com/eMapR/TimeSync-Plus/blob/master/images/folder1.JPG' width = 200>


To Run the “create_sql_db.py”: in your LT-Change-DB command prompt add and run:

 

​            `python \full\path\to\create_sql_db.py`

 

Once running it will prompt you to find the locations of the config text file ()and the location of the observations.geojson with file path dialog boxes. Once completed a sql database will be located in the base directory.

------

 

 

   



## Step 6: Edit App options text file





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

If we wanted to add a 'State' field to our table we would need to add " 'State', " to the 'eventTable' list. A list contain the values in the square brackets "[ ]". In the event table only add values after 'LT_YOD'. Once we add 'State' our event table line would look like this:

------

`'eventTable': ['plotId', 'obserId', 'LT_YOD', 'YOD', 'ChangeAgent', 'State', Confidance', 'User', 'Comment']`

------

You can add the " 'State', " value anywhere in the list aslong as it is after " 'LT_YOD', ". Next, if we want to be able to attribute our new feild we need to add a 'State' key to our display table object. The syntax is a key and value pair. The key stands alone in parenthesis with a colon after it followed by a list of values. In out case 'State' would be the key, and the state types would be our values as in the example below. 

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
	'User': ['Peter', 'Katie'],
	'State': ['forest','urban','barren'], 
	'Confidance': ['low', 'med', 'high']}, 
'eventTable': ['plotId', 'obserId', 'LT_YOD', 'YOD', 'ChangeAgent', 'Confidance', 'State', 'User', 'Comment']
}
```

------
Make sure the names between the display table and the event table are the same for it is case sensitive.
Be sure to save the config.txt file.

## Step 7: Start the App

The application location is in the TS-Plus folder in the base directory. In the TS-Plus folder there is a file named 'Plus'. Double click this file to open the TS-Plus application.



Once opened, a dialog box will appear and the user will need to locate the SQL database that was created in step 5. When the SQL file is found double click it and the dialog box will disappear. After a few moments the plot list will be populated with polygon or point identification values.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/01_DB_box.JPG' width="400">

Clicking on one of the plot list identification values, will render the spectral and spatial data. This may take a few moments. Once loaded, the user will see that plot list ID value is highlighted, and spectral plot in the upper center is populated, and that there are several images chips with the same polygon geometry in the upper right bottom sections. 

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

The user can apply attributes to the plot ID by right clicking an observation in the spectral trajectory plot. This action will open a pop up box with several button that where defined by the user in the text file. When clicked these button open and show a selection of values that need to be applied in order to save them to the event table in the SQL database. 

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/06savedata2.JPG' width="250">

If the comment/submit pair where applied in the text file the pop up box will have a comment button, and when clicked a comment box will expand in the pop up box. The user can add as much text as needed; however, when the user is done commenting the user must click the submit button below the comment box. And once all associated values have been chosen the user will need to click the save button in order to record his or her attributes. 

All of the pop up button options need to have values selected in order for them to be save them!

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/06savedata3.JPG' width="250">

To export the event table with saved attributes the user need to click on the Download CSV button in the header of the application. When clicked the user will be prompted with a dialog box asking where to save the CSV file. Once the user define a place the save the file a CSV file will appear there.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/07export.JPG' width="250">


