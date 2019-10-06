
# TimeSync-Plus
TimeSync+ is an application for gathering point and polygon spectral temporal information from Landsat time series data into a database.

## About 

TimeSync+ is a desktop application modeled after the original [TimeSync application](http:example.com) that was originally developed as a validation tool for the [LandTrendr](http:example.com) spectral-temporal segmentation algorimth. Since its inception, its utility has grown beyond a segmentation validation tool. It is also useful for exploring know or predicted change events on the landscape and for collecting information about individual observations in time. TimeSync-Plus better handles these two significant use cases (event and observations information collection) more explicilty and greatly expands flexibity for user to define what tpyes of information should be recorded.

### Improvements:
- Slippy map zoom and pan image chips
- Four RGB image chip display option
- Total user-control over what information can be collected
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
- In the upper center panel edit line 16 to your file path string of your shapefile asset.
- Once your happy with your parameter adjustments (if needed) click "Run" in the upper right portion of the upper center panel
- After a few moments the "Tasks" Tab will flash yellow
- Click the "Tasks" Tab.
- In the "Tasks" there will be 7 tasks: 4 images (rgb654 rgb543 rgbTC rbg432) and 3 files (observationsInfo, Observations-KML, Observations_GeoJSON).
- Click on each of the "RUN" Tabs.
- A Tasks dialog box will appear
- Double check Drive folder (the folder where it will be saved on your Google Drive)
- Click the "Run" Tab.
- A rotating gear will appear next to the task.
- repeat for each task, keeping the Drive folder the same for each task.
## Step 4: Setting up a project directory locally

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
|              gdal2tiles.py
|              geojsonToSqlDB.py
|              make_rgb_tms.py
|              splitJsonByFe.py
|              splitJsonByYear.py
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

## Step 5: Download data from Google Drive
- Go to your Google Drive .
- Find the location of your Drive folder from step 3.
- Right click folder.
- Select Download from the dropdown box.
- A download process box will appear in the lower right.
- Once downloading is complete. Unzip the file and name the folder "TimeSync".
- Place the "TimeSync" folder in the "tiles" folder of the "project" directory so it looks like the structure above.

## Step 6: Make annual image tile sets
- Open a terminal or command prompt.
- Navigate to script folder in the project directory with your terminal.
- In the terminal enter as follows and pertains to your operating system:
```
python make_rgb_tms.py ../tiles/TimeSync/ 13
NOTE: The 13 represent the highest zoomlevel of tiles that will be created. A value between 
12 to 15 is suggested.   
```
- Once complete a "tms" folder will be in the TimeSync folder as in the file structure.




## Step 7: (Optional but suggested for large areas) Split Geojson by year or number of features PYTHON 2.7:

- Split By Feature:
  - Open a terminal or command prompt.
  - Navigate to script folder in the project directory with your terminal.
  - In the terminal enter as follows and pertains to your operating system:
```
"python splitJsonByFe.py ../tiles/TimeSync/observations.geojson ../geojsons/" 
NOTE For Below: 6 , will output 6 geojson files with about 893 features per split geojson file
>>>There are 5362 features in your GEE geojson file. How many split geojson files, which will become databases, would you like? 6
```

  - Split By Year of Detection.
    - Open a terminal or command prompt.
    - Navigate to script folder in the project directory with your terminal.
    - In the terminal enter as follows and pertains to your operating system:
```
"python splitJsonByYear.py ../tiles/TimeSync/observations.geojson ../geojsons/"
NOTE for below :: 1986 to 2018 will make a geojson file for that range of years. 1992 to 1992 would return one geojson file for 1992
Reading geojson file.
Out directory is real.
What is the starting year? :1986
What is the ending year? :2018
```
## Step 8: Edit App options text file

The config.txt file in the database folder is used to define names for attribution.  

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
    'Valid_name': ['Smith','Happ','Row','Johnson','Bolstad'],
    'Confidence': ['3', '2', '1'], 
    'Alt_type': ['Development', 'Fire', 'Mass Movement', 'Progressive Defoliation','Riparian', 'Tree Toppling', 'Unknown']},
'eventTable': ['plotId', 'Valid_Date', 'LT_YOD', 'Event_Year', 'Event_Name', 'ChangeType', 'Confidence', 'Alt_type', 'Comment']
}
```

The keys in the "displayTable" are names that will correspond to a field name in a CSV file and the values will be the selectable values for that field. When 'displayTable' keys match 'eventTable' values they will be display in the application as  attribution buttons.  There are some special key value pairs that allow a text box to be available as an attribution style.  Those pairs are "'Comment': [''],  Event_Year': [''], and 'Event_Name': ['']" . These key pairs can be removed from the config.txt file if a text box is not need.


## Step 9: Create Database(s) from geojson(s) PYTHON 2.7
- Open a terminal or command prompt.
- Navigate to script folder in the project directory with your terminal.
- In the terminal enter as follows:
```
python geojsonToSqlDB.py
```
  - A dialog box will appear asking for the location of the config.txt file.
- Click OK
- A file path dialog box will appear.
- Find the location of your "config.txt" file.
- Double click the file.
- A dialog box will appear asking for the location of the geojsons file(s).
- Click OK.
- A file path dialog box will appear.
- Find the location of a geojson file.
- Double click the file.
- The databases will be written to the same directory as the config.txt file.

## Step 10: Start the App

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


