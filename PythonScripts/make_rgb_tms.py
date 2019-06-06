# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:57:30 2019

@author: braatenj
"""

import gdal     #  changed Peter os:ubuntu
from glob import glob
import os
import subprocess
import sys
import json
import gdal2tiles # this is a sibling file module

def mosaicFiles(files, bands, vrtFile):
  listFile = vrtFile.replace('.vrt', '_filelist.txt')
  tileList = open(listFile, 'w')
  for fn in files:
    tileList.write(fn+'\n')
  tileList.close()
  bands = ' '.join(['-b '+str(b) for b in bands])
  cmd = 'gdalbuildvrt -q -input_file_list '+listFile+' '+bands+' '+vrtFile
  print (cmd)
  subprocess.call(cmd, shell = True)  #  changed Peter os:ubuntu

def makesTiles(fn, folder, maxZoom):
  fn = fn.replace('\\', '/')
  folder = folder.replace('\\', '/')
  cmd = 'gdal2tiles.py -q -z 5-'+maxZoom+' "'+fn+'" "'+folder+'"' # 13
  args = [i.replace('"','') for i in cmd.split(' ')]
  gdalArgs = gdal.GeneralCmdLineProcessor( args )
  gdal2tiles.runit(gdalArgs)

def getBandList(fn):
  src = gdal.Open(fn, gdal.GA_ReadOnly)
  return([range(i,(i+3)) for i in range(1,src.RasterCount,3)])

def makeDir(folder):
  if not os.path.exists(folder):
    os.makedirs(folder)

def getYearEnds(prepDir):
  print(prepDir)
  infoFile = glob(os.path.join(prepDir,'observationsInfo.geojson*'))[0]
  # TODO: check if this file exisits
  with open(infoFile) as f:
    info = json.load(f)
  startYear = info['features'][0]['properties']['startYear']
  endYear = info['features'][0]['properties']['endYear']
  return([int(startYear), int(endYear)])
  
def main(prepDir, maxZoom):
  names = ['rgbTC','rgb654','rgb543','rgb432']
  startYear, endYear = getYearEnds(prepDir)
  years = range(startYear, endYear+1)  
  for name in names:
    print(name)
    rgbFiles = glob(os.path.join(prepDir,name+'*.tif'))
    if len(rgbFiles) == 0:
      print('  No files found, skipping')
    else:
      bandsList = getBandList(rgbFiles[0])
      baseDir = os.path.dirname(rgbFiles[0])
      for year, bands in zip(years, bandsList):
        print('   '+str(year))
        thisDir = os.path.normpath(os.path.join(baseDir,'tms',name,str(year)))
        thisVRT = os.path.normpath(os.path.join(thisDir,'rgbIMG.vrt'))
        makeDir(thisDir)
        mosaicFiles(rgbFiles, bands, thisVRT)
        makesTiles(thisVRT, thisDir, maxZoom)

      
if __name__ == '__main__':
  prepDir = sys.argv[1]
  maxZoom = sys.argv[2]
  main(prepDir, maxZoom) 

  



