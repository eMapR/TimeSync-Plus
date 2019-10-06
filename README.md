
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

Make a point or polygon shapefile of disturbance areas. You will need to add a uniq id field to your shapefile called "uniqID" where each feature has a uniq ID. You can either generate your own shapefiles or use the [LT-ChangeDB](http:example.com) process to make distubance polygons for you. This shapefile will need to zipped in order to upload it to GEE.

## Step 2: How to Upload the shapefile to Google Earth Engine
- Do you have a GEE (Google Earth Engine) account?
  - [Make a GEE account](https://code.earthengine.google.com/)
- How to upload a zipped shapefile to GEE.
  - From the main GEE page click "Assets" in the upper left panel.
  - Click the "NEW" button under the "Assets" Tab. 
  - A dropdown box will appear.
  - Click the shapefile button. 
  - A dialog box will appear.
  - Click "SELECT".
  - A file path way dialog box will appear.
  - Find the location of your zipped shapefile.
  - Double click your file.
  - Define the directory, in Assets, where you would like to save your shapefile asset
  - How to make a new directory in GEE.
    - From the assets tab click "NEW".
	- In the dropdown box click "Folder".
	-  A "New Folder" dialog box will appear.
	-  Enter the new folder's name.
	-  Click Ok.
	-  A folder with your defined name will appear in Assets. 
  - Click upload.
  - Under the "Tasks" in the upper right panel you can check the process of your uploading asset.
  - Once the task is complete you will be able to locate the shapefile asset in your Assets Tab.

## Step 3: Setting up a project directory locally

- download the TimeSync-Plus GitHub repository.
- Go to https://github.com/eMapR/TimeSync-Plus.
- Click the green button "Clone or Download".
- A dropdown box will appear.
- Click download "ZIP".
- Find and unzipped download file.
-Find the project directory in the unzipped TimeSync-Plus folder.
***Note: This directory is where all your pre-project processing will take place ***
File Structure:
```
project
|              
|---------|databases 
|              config.txt
|              
|---------|scripts
              gdal2tiles.py
              geojsonToSqlDB.py
              make_rgb_tms.py
              splitJsonByFe.py
              splitJsonByYear.py
|
|----------|geojsons
|               *** export location for split geojson files ***
|
|----------|tiles
           |
           |-------|TimeSync
                   |      observationsInfo.geojson
                   |      observations.geojson
                   |      observations.kml
                   | 
                   |-------|tms
                           |
                           |rgb543  ***years>>>zoomlevels>>>location>>>images.png***
                           |rgb654  ***years>>>zoomlevels>>>location>>>images.png***
                           |rgbTC   ***years>>>zoomlevels>>>location>>>image.png***
                           |rgb432  ***years>>>zoomlevels>>>location>>>image.png***
```

## Step 3: How to Run Google Earth Engine Script to generate data

- Go to [GEE](https://code.earthengine.google.com/).
  - If don't have repository access go to the links below.
    - [Support Module](https://code.earthengine.google.com/?accept_repo=users/jstnbraaten/modules)
    - [TS Plus GetData](https://code.earthengine.google.com/691d2d6e525772f97f1d6e74d271fcaf)
- Click on the "Scripts" Tab in the upper left panel.
- Open "Reader" the the "Scripts" Tab
- Open "TS_Plus_GetData.js"
- In the upper center panel verify that line 6 points to  
	 `users/jstnbraaten/modules:ee-lcb.js`
- There are a variety of parameters that can be changed and there is a brief description of each on the same line as the parameters value. 
- In the upper center panel edit line 16 to your file path string to your shapefile asset.
-the code line label can be seen in the left position of the upper center panel.
- Once happy with your parameter adjustments (if needed)

-Click "Run" in the upper right portion of the upper center panel

- After a few moments the "Tasks" Tab will flash yellow

- Click the "Tasks" Tab.

- In the "Tasks" there will be 7 tasks: 4 images (rgb654 rgb543 rgbTC rbg432) and 3 files (observationsInfo, Observations-KML, Observations_GeoJSON)

*** describe each file ***.............................................................................More

- Click on each of the "RUN" Tabs.

- A Tasks dialog box will appear

- Double check Drive folder (the folder where it will be saved on your Google Drive)

- Click the "Run" Tab.

- A rotating gear will appear next to the task.

- repeat for each task, keeping the Drive folder the same for each task.



## Step 4: Download data from Google Drive

Once all the tasks are completed there will be a folder in your Google Drive called TimeSync. To download the folder right click it and select download. This will create a zip folder and it will be downloaded to your computer, and there may be multiple zipped folder depending of the size of your region of interest. Next, make a new folder on your computer and name it 'tiles'. Then extract all the contents of the zip folder or folders to the 'tiles' directory. If there was more than one zipped folders you may get a warning about there already being a TimeSync folder and concerns about merging them. This is fine go ahead and merge them.

Next, you'll need to download the python files in our python folder on GitHub, but it easier to just download the whole Time Sync Plus directory that way you have the files ready to go. You can do this by clicking the green button near the top of the page. Anyway, download them and then place 'gdal2tiles.py' and 'make_rgb_tms.py' in the 'tiles' folder so it looks like this:

<img src ='https://github.com/eMapR/TimeSync-Plus/blob/master/images/folder.JPG' width = 300>


## Step 5: Make annual image tile sets

Annual image data downloaded from Google Drive needs to be arranged for use in the TimeSync+ app.
In this step you'll run a Python script to generate the required image tiles. The script is called
`make_rgb_tms.py` and can be found in the "PythonScripts" directory in the folder of code you downloaded
in a previous step. Here is the definition

`python make_rgb_tms.py [downloadedImgDir] [maxZoomLevel]`

Where: 

- `downloadedImgDir` is full path to the folder where all of the image data dowloaded from Google Drive
lives
- `maxZoomLevel` is the maximum tile zoom level to produce. Between 13 and 16 are good. Depending on your latitude these zoom
levels will appoximate full 30m resolution. Note that beyond level 13, the process can take a long time and create millions
of files, depending on the size of the study area. We suggest trying 13 to start and if find you'd like more resolution, then
rerun the process and increase the value by 1.


To Run:

​            `python /full/file/path/to/tiles/make_rgb_tms.py /full/file/path/to/tiles/TimeSyncfolder 14`

 

This process will create a “tms” folder that will house the tile images.

------
Once your done with the above process you'll need to make a new folder called 'TS-Plus' and place the 'tiles' directory in it. The TS-Plus folder will be the base of the directory and this where the config.txt file should be place along with 'create_sql_db.py' file and the 'TimeSyncPlus' application folder. The base directory should look like this:

<img src ='https://github.com/eMapR/TimeSync-Plus/blob/master/images/folder1.JPG' width = 200>


------


## Step 6: Edit App options text file

the config.txt file in the database folder is used to define names for attribution.  

The config.txt file is a python dictionary, and in this dictionary there are three main pieces a 'polygonTable', 'displayTable', and 'eventTable'. Only "displayTable" and the "eventTable" should be edited by the user. To make changes to the config.txt file follow the example below.

This is what the config.txt file looks like:

------

```
{
'polygonTable': ['plotid', 'geo', 'json'], 
'displayTable': {
    'Comment': [''],
    'ChangeType': ['Annual Variability', 'Agricultural', 'Agricultural Clearing', 'Development', 'Fire', 'Mass Movement', 'Progressive Defoliation','Riparian', 'Tree Toppling', 'Unknown'], 
    'Event_Year': [''],
    'Event_Name': [''],
    'Valid_name': ['APlatel','CBarsch','CCopass','GStonecipher','NAntonova'],
    'Confidence': ['3', '2', '1'], 
    'Alt_type': ['Development', 'Fire', 'Mass Movement', 'Progressive Defoliation','Riparian', 'Tree Toppling', 'Unknown']},
'eventTable': ['plotId', 'Valid_Date', 'LT_YOD', 'Event_Year', 'Event_Name', 'ChangeType', 'Confidence', 'Alt_type', 'Comment']
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
	'Comment': [''], 
	'ChangeAgent': ['none', 'unknown', 'regrowth', 'fire', 'logging', 'flooding', 'pine bug', 'false reading'], 
	'YOD': [''], 
	'User': ['Peter', 'Katie'],
	'State': ['forest','urban','barren'], 
	'Confidance': ['low', 'med', 'high']}, 
'eventTable': ['plotId', 'obserId', 'LT_YOD', 'YOD', 'ChangeAgent', 'Confidance', 'State', 'User', 'Comment']
}
```

------
Make sure the names between the display table and the event table are the same for it is case sensitive.
Be sure to save the config.txt file.

## Step 7: Opitional: Split Geojson file 

Depending on the size of your study area you may want to split your geojson into small sections. If you decide to split your geojson first you need to make a folder called geojson in base directory. Then run "jsonsplit.py". This python script can be run from the command line with.

```sh
python [path to python script] [path to your GEE geojson file] [path to your new geojson directory]
```
Once the script is running, it will tell how many features (polygons) are in your geojson file, and will ask how many split files you want. An example would be if my geojson file had 5362 features, and if I wanted each geojson to have about 500 features I would divide 5362 by 500 and round up from 10.724 to 11 and use this value. This would give me 11 geojson files with each file have ~487 feautures per file in the geojson directory. Next, we will make databases for our geojson file or files.  


## Step 8: Create Database(s) from geojson(s)
Now, we will make SQL Databases from our geojoson files. This is done by running the geojsonToSqlDB.py script. The script will ask for the location of two files. The config text file and a geojson directory (just click on the a geojson file in the directory). This will create an equal number of databases to the number of geojson files. The databases will be placed in directory with the tiles folder.

## Step 9: Start the App

The application location is in your zipped TSP+4 file. Decompresses or unzipped the zipped file, then open the unpackaged folder. Continue opening folder until you come to a folder with a variety files. Here, there will be a TSP+4.2.exe file. Double click that file.   

Once opened, a dialog box will appear and the user will need to locate the SQL database they created. When the SQL file is found double click it, and the dialog box will disappear. After a few moments the plot list will be populated with polygon or point identification values.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/01_DB_box.JPG' width="400">

Clicking on one of the plot list identification values, will render the spectral and spatial data. This may take a few moments. Once loaded, the user will see that plot list ID value is highlighted, and spectral plot in the upper center is populated, and that there are several images chips with the same polygon geometry in the upper right and bottom sections. If no images appear in the bottom section make sure your selected database is in the same directory as your tiles folder. 

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


