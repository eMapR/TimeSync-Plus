
# TimeSync-Plus 
TimeSync+ is an application for gathering point and polygon spectral temporal information from Landsat time series data into a database.

## About 

TimeSyncPlus is a desktop application modeled after the original [TimeSync application](https://timesync.forestry.oregonstate.edu/) that was originally developed as a validation tool for the [LandTrendr](https://emapr.github.io/LT-GEE/landtrendr.html) spectral-temporal segmentation algorimth. Since its inception, its utility has grown beyond a segmentation validation tool. It is also useful for exploring know or predicted change events on the landscape and for collecting information about observations in time. TimeSync-Plus better handles these two significant use cases (event and observations information collection) more explicilty and greatly expands flexibity for user to define what types of information should be recorded.

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
- If don't have repository access go to the links below. They should add file paths in your GEE "Reader" directory under "scripts".
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
- A Tasks dialog box will appear.
- Double check the drive folder value (The folder where it will be saved on your Google Drive).
- Click the "Run" Tab.
- A rotating gear will appear next to the task.
- repeat for each task, keeping the Drive folder the same for each task.
## Step 4: Setting up a project directory locally

- download the TimeSync-Plus GitHub repository.
- Go to https://github.com/eMapR/TimeSync-Plus.
- Click the green button "Clone or Download".
- A dropdown box will appear.
- Click download "ZIP".
- Find and unzip downloaded file.
- Find the project directory in the unzipped TimeSync-Plus folder.
***Note: This directory is where all your pre-project processing will take place ***
File Structure:
```
project
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
           |      config.txt
	   |      *** Database files will appear in step 9 ***
	   |      TSdatabase.db 
           |
           |-------|TimeSync
                   |      observationsInfo.geojson
                   |      observations.geojson
                   |      observations.kml
		   |      rgb543.tif
		   |	  rgb654.tif
		   |	  rbg432.tif
                   |	  rbgTC.tif 
		   |
                   |-------|tms *** This folder and the ones below will appear in step 6 ***
                   |       |
                   |       |rgb543  ***years>>>zoomlevels>>>location>>>images.png***
                   |       |rgb654  ***years>>>zoomlevels>>>location>>>images.png***
                   |       |rgbTC   ***years>>>zoomlevels>>>location>>>image.png***
                   |       |rgb432  ***years>>>zoomlevels>>>location>>>image.png***
                   |

		   

```

## Step 5: Download data from Google Drive
- Go to your Google Drive .
- Find the location of your drive folder from step 3.
- Right click folder.
- Select Download from the dropdown box.
- A download process box will appear in the lower right.
- Once downloading is complete. Unzip the file and name the folder "TimeSync".
- Be sure that all file were downloaded by matching files with the ones in your Google Drive.
- Place the "TimeSync" folder in the "tiles" folder of the "project" directory so it looks like the structure above.

## Step 6: Make annual image tile sets
- Open a terminal or command prompt. I suggest using an anaconda command prompt with gdal installed. (not powershell)
- Navigate to script folder in the project directory with your terminal.
- In the terminal enter as follows and pertains to your operating system:
```
python make_rgb_tms.py ../tiles/TimeSync/ 13
NOTE: The 13 represent the highest zoomlevel of tiles that will be created. A value between 
12 to 15 is suggested.   
```
- Once complete a "tms" folder will be in the TimeSync folder as in the file structure.




## Step 7: (Optional but suggested for large areas) Split Geojson by year or number of features (Python 2.7 required):

- Split By Feature:
  - Open a terminal or command prompt.
  - Navigate to script folder in the project directory with your terminal.
  - In the terminal enter as follows and pertains to your operating system:
```
python splitJsonByFe.py \full\file\path\tiles\TimeSync\observations.geojson \full\file\path\tiles\TimeSync\geojsons\
NOTE For Below: 6 , will output 6 geojson files with about 893 features per split geojson file
>>>There are 5362 features in your GEE geojson file. How many split geojson files, which will become databases, would you like? 6
```

  - Split By Year of Detection.
    - Open a terminal or command prompt.
    - Navigate to script folder in the project directory with your terminal.
    - In the terminal enter as follows and pertains to your operating system:
```
python splitJsonByYear_v2.py \full\file\path\tiles\TimeSync\observations.geojson \full\folder\path\geojsons\
``` 

## Step 8: Edit App attribution text file

The config.txt file in the project folder is used to define categories and values for attribution in the application.  

This is what the config text file looks like:

------

```
{
'polygonTable': ['plotid', 'geo', 'json'], 
'displayTable': {
    'Comment': [''],
    'ChangeType': ['Annual Variability', 'Agricultural', 'Agricultural Clearing', 'Development', 'Fire', 'Mass Movement', 'Progressive   Defoliation','Riparian', 'Tree Toppling', 'Unknown'], 
    'Event_Year': [''],
    'Event_Name': [''],
    'Valid_name': ['Smith','Happ','Row','Johnson','Bolstad'],
    'Confidence': ['3', '2', '1'], 
    'Alt_type': ['Development', 'Fire', 'Mass Movement', 'Progressive Defoliation','Riparian', 'Tree Toppling', 'Unknown']},
'eventTable': ['plotId', 'Valid_Date', 'LT_YOD', 'Event_Year', 'Event_Name', 'ChangeType', 'Confidence', 'Alt_type', 'Comment']
}
```


There are keys and values in the config file. Keys are the elements in front of the colon ":" and values are the elements in brackets. For example, "Valid_name" is a key and 'Smith' is one of the value assocatied with that key. 

The key "displaytable" holds the user's specific attribution categories and values. A key value that is defined in both the "displayTable" and "eventTable" will be display in the application as a button with its values as choices for attribution. Some of the values in the "displayTable" above are only brackets and quotation marks. Thess are unique key value pairs and will only work in there current form as in the above example, meaning if you want a text box you have three key/value options avaiable to you: "'Event_Year': ['']" , "'Event_Name': ['']" or "'commment': ['']" .  These allow a commment box to be used insted of having hard coded values. This is helpful when a wide range of choices are needed for attribution.

**All values must be in matching quotation marks.**

You'll notice that there are some keys in the eventTable that are not in the displayTable of the config text file. These keys are "plotID", "Vaild_Date",and "LT_YOD". They are important to the exportable CSV file avaiable in the application. they are field names for the plot ID, a time stamp for when data is saved and landTrendr impiled year of change. These value should not be changed. 

**Config Text Editing Example**

If you wanted to add a new category and values you would do as follows:

- Make a key value pair
`'State': ['no change', 'postive change', 'negative change']`
- Add the the key value pair anywhere in the displayTable dictionary (in the "'displayTable':{add here}")
- If a value is added anywhere but the end of the displayTable dictionary be sure to add a "," at the end.
- Add the key in this case "State" to the end list of values of the eventTable.

The new config file would then look like this:

```diff
{
'polygonTable': ['plotid', 'geo', 'json'], 
'displayTable': {
    'Comment': [''],
    'ChangeType': ['Annual Variability', 'Agricultural', 'Agricultural Clearing', 'Development', 'Fire', 'Mass Movement', 'Progressive Defoliation','Riparian', 'Tree Toppling', 'Unknown'], 
    'Event_Year': [''],
+   'State': ['no change', 'postive change', 'negative change'], <<<<< NEW
    'Event_Name': [''],
    'Valid_name': ['Smith','Happ','Row','Johnson','Bolstad'],
    'Confidence': ['3', '2', '1'], 
    'Alt_type': ['Development', 'Fire', 'Mass Movement', 'Progressive Defoliation','Riparian', 'Tree Toppling', 'Unknown']},+
+ 'eventTable': ['plotId', 'Valid_Date', 'LT_YOD', 'Event_Year', 'Event_Name', 'ChangeType', 'Confidence', 'Alt_type', 'Comment', 'State']           <<<<  NEW
}
```


## Step 9: Create Database(s) from geojson(s) (Python 2.7 required)
- NOTE: The Databases created in this step will be written in the same location of the config text file.
- Open a terminal or command prompt that supports python version 2.7.1 .
- Navigate to script folder in the project directory with your terminal.
- In the terminal enter as follows:
```
python geojsonToSqlDB_v2.py
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
- The databases will be written to the same directory location as the config.txt file used.




## Step 10: Start the App

- Make sure that the Database you want to attributed is in the same directory as the tiles folder.

The application is avaible at ftp://islay.ceoas.oregonstate.edu/TimeSyncPlus/ .

- Decompresses or unzipped the zipped file.
- Open the unpackaged folder. 
- Locate the "TSP_v*.*" file.
- Double click that file.
- If you see a warning message like the one below. If so click "more info" and then a new message will appear and then click "Run anyway".   
<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/winWarning1.JPG' width="400">

Once opened, a dialog box will appear and the user will need to locate the database you moved to be with the tiles folder. When the DB file is found double click it, and the dialog box will disappear. 

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/01_DB_box.JPG' width="400">

After a few moments the plots list will be populated with polygon or point identification values. Clicking on one of the plot list identification values will show the plot's spectral and temporal data.This may take a few moments. If no images appear in the bottom section make sure your selected database is in the same directory as your tiles folder. If you see a "no data" value in the plots list, that good. It just means the exportable CSV is writable. Also, you'll notice that the plot you selected will have a green background color. This marks the plot you are currently viewing, and when you move on to another plot the green will turn to a light gray. Furthermore, a check mark means plot attribution was saved. 

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/02_plotlist.JPG' width="200"> 

Your display should look similar to the image below.  

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/full2.JPG' width="800">

The spectral plot shows the summary spectral values for the area represent by the point or polygon displayed. For visual purposes, the user can double click on two observation points to connect a line between them.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/03_specplot3.JPG' width="800">

More line segment can be added by continuing to double click on more observation points. To remove line segments double click on a already selected point.

The image chip in the upper right is different from the other images chips in that it show approximately current ariel imagery, topographical, and street base maps. 

The user can change the base map by clicking the map icon in this image chip. The user can also remove the geometry in this image chip by unselecting the ROI option in the map icon.

At the bottom of the application's display is a set of yearly spectral image maps with a geometry on top of them. This set of temporal images help the user get a feel for what the spectral plot is displaying and allows for a more informed attribution.


## Applying Attribution 

You will notice a two separate tab bar selection at the bottom of either of the Spectral Trajectory Plot. 

The one on the left contains five tabs, Index/Bands, Chip Set, show line, Global stretch, and local stretch. 

​	Index/Bands : Changes the Spectral Trajectory Plot values to various bands and indices 

​	Chip Set: Changes the image chips color scheme 

​	Show line : either adds or removes the trend line of the plot

​	Global Stretch: Extends the y-axis 

​	Local Stretch: Reduces the y-axis to the max and min values. 

The tab bar on the right should look familiar to you as these are your keys and values, and if you hover over a tab the values for the key will appear. Click a value and its name will populate the tab. If you used comment boxes and would like to add text to them, click the expand box and begin to type, once completed a "text submitted" value will populate the tab. Once you are finished attributing a plot be sure to click the save button to the right of the attribution bar. If saved correctly a check mark will appear next to the plot name. 

To export the event table with saved attributes the user need to click on the Download CSV button in the header of the application. When clicked the user will be prompted with a dialog box asking where to save the CSV file. Once the user define a place the save the file a CSV file will appear there.

<img src = 'https://github.com/eMapR/TimeSync-Plus/blob/master/images/07export.JPG' width="250">
