// load the functions library - you may need to add the repo to your account - visit: 
//   https://code.earthengine.google.com/?accept_repo=users/jstnbraaten/modules
// See for more info on the functions module: https://jdbcode.github.io/EE-LCB/ 
var lcb = require('users/jstnbraaten/modules:ee-lcb.js'); 

//###############################################################################
// INPUTS
//###############################################################################

lcb.props['crs'] = 'EPSG:5070'                                        // what CRS should the polygons be summarized for - set to the same projection as the uploaded asset
lcb.props['scale'] = 120                                              // what scale should pixels be summarized at (meters) if using 30, program could run out of memory for large polygons - in that case increase the scale - increasing the scale a little will also remove some noise
lcb.props['reducer'] = ee.Reducer.mean()                              // what reducer to summarize polygons by
lcb.props['gDriveFolder'] = 'TimeSync'                                // what GDrive folder to write to
lcb.props['featureCollection'] = 'users/emaprlab/NCCN/change_1993_id' // this comes from asset upload
lcb.props['featureID'] = 'uniqID'                                     // this is a field name in the uploaded asset for unique polygons
lcb.setProps({                                                        
  startYear: 1984,                                                    // what year should the time series start
  endYear: 2018,                                                      // what year should the time series end                                               
  startDate: '06-20',                                                 // what date should should annual image composites start (mm-dd)
  endDate: '09-20',                                                   // what date should should annual image composites end (mm-dd)
  sensors: ['LT05', 'LE07', 'LC08'],                                  // what sensor images should be inlcuded in annual image composites - options: 'LT05', 'LE07', 'LC08'
  cfmask: ['cloud', 'shadow'],                                        // what image features should be masked out - options: cloud, shadow, snow, water
  harmonizeTo: 'LC08',                                                // what sensor should images be harmonized to - options: 'LE07', 'LC08'
});

//###############################################################################

lcb.setProps({ 
  aoi: ee.FeatureCollection(lcb.props.featureCollection).geometry().bounds() 
});

var plan = function(year){
  var col = lcb.sr.gather(year)
    .map(lcb.sr.harmonize)
    .map(lcb.sr.maskCFmask);
  return lcb.sr.mosaicMedoid(col).select(['B2','B3','B4','B5','B6','B7']);
};

var years = ee.List.sequence(lcb.props.startYear, lcb.props.endYear);
var annualSR = ee.ImageCollection.fromImages(years.map(plan));

var summary = annualSR.toBands()
  .reduceRegions({
    collection:lcb.props.featureCollection, 
    reducer:lcb.props.reducer, 
    scale:lcb.props.scale, 
    crs:lcb.props.crs, 
    tileScale: 4
  }).map(function(ft){
    return ft.set('id', ft.get(lcb.props.featureID));
  });

Export.table.toDrive({
  collection:summary, 
  description:'Observations-GeoJSON', 
  folder:lcb.props.gDriveFolder, 
  fileNamePrefix:'observations', 
  fileFormat:'GeoJSON',
});

Export.table.toDrive({
  collection:summary, 
  description:'Observations-KML', 
  folder:lcb.props.gDriveFolder, 
  fileNamePrefix:'observations', 
  fileFormat:'KML',
});

var rgbTC = annualSR.map(lcb.sr.addBandTC).map(lcb.sr.visualizeTC).toBands();
var rgb654 = annualSR.map(lcb.sr.visualize654).toBands();
var rgb543 = annualSR.map(lcb.sr.visualize543).toBands();
var rgb432 = annualSR.map(lcb.sr.visualize432).toBands();

Export.image.toDrive({
  image:rgbTC,
  region:lcb.props.aoi, 
  scale:30,
  description:'rgbTC',
  folder:lcb.props.gDriveFolder,
  fileNamePrefix:'rgbTC',
  crs:'EPSG:4326',
  maxPixels:1e13
});

Export.image.toDrive({
  image:rgb654,
  region:lcb.props.aoi, 
  scale:30,
  description:'rgb654',
  folder:lcb.props.gDriveFolder,
  fileNamePrefix:'rgb654',
  crs:'EPSG:4326',
  maxPixels:1e13
});

Export.image.toDrive({
  image:rgb543,
  region:lcb.props.aoi, 
  scale:30,
  description:'rgb543',
  folder:lcb.props.gDriveFolder,
  fileNamePrefix:'rgb543',
  crs:'EPSG:4326',
  maxPixels:1e13
});

Export.image.toDrive({
  image:rgb432,
  region:lcb.props.aoi, 
  scale:30,
  description:'rgb432',
  folder:lcb.props.gDriveFolder,
  fileNamePrefix:'rgb432',
  crs:'EPSG:4326',
  maxPixels:1e13
});

var runInfo = ee.Dictionary({
  'featureCollection': lcb.props.featureCollection, 
  'featureID': lcb.props.featureID,
  'gDriveFolder': lcb.props.gDriveFolder,
  'startYear': lcb.props.startYear,
  'endYear': lcb.props.endYear,
  'startDay': lcb.props.startDate,
  'endDay': lcb.props.endDate,
  'maskThese': lcb.props.cfmask,
  //'noData': -9999,                        ???
  //'srCollectionList': srCollectionList,   ???
  'sensors': lcb.props.sensors,
  'harmonizeTo': lcb.props.harmonizeTo,
  'summaryScale': lcb.props.scale,
  'summaryCRS': lcb.props.crs,
  'summaryStat': lcb.props.reducer.getInfo().type
});

var runInfo = ee.FeatureCollection(ee.Feature(null, runInfo));
Export.table.toDrive({
  collection: runInfo,
  description: 'observationsInfo',
  folder: lcb.props.gDriveFolder,
  fileNamePrefix: 'observationsInfo',
  fileFormat: 'GeoJSON'
});
