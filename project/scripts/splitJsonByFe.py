#================================================================================
# This script splits geojson files that are create by the TS_Plus_GetData.js on Google Earth Engine. The geojson file will be split by groups 
# of features (polygons). When the script starts it will ask the user how many split geojson file they would like. An example would be:
# 
#---------example--------
# python [path to jsonsplit.py] [file path to geojsonfile] [file path to a empty output directory]
#
# python ./jsonsplit.py ./observation.geojson
#
#	There are 27639 features in your GEE geojson file. How many split geojson files would you like?
#
#	(if you wanted 1000 feature (polygons) per file the user would divide 27639 by 1000 (27639/1000 = 27.6 ~ 28 ), and then enter 28. )
#===========================================================================

import json
import sys
import operator
#geojson = "/vol/v1/proj/TimeSyncPlus/TimeSyncAssets/observations.geojson"

#============================================================================

def geoJsonSplit(geojson,outdir):

    # open the geojson and reads the contents
    with open(geojson, 'r+') as f:
        data = json.load(f)
    #data.sort(key=operator.itemgetter("")) #
    numberOfFeatures = len(data['features'])
    # number of databases wanted by user
    #chuckSize = 3
    chuckSize = int(raw_input("There are "+str(numberOfFeatures)+" features in your GEE geojson file. How many split geojson files, which will become databaseas, would you like? "))
    # number of features per database
    div = numberOfFeatures/chuckSize
	
    counter = 0 
    # loops over the number of databases wanted.
    for i in range(chuckSize):
	
        if counter < 1:
            start = 0  
            end = div
            if chuckSize == 1:
                start = 0
                end = numberOfFeatures  
        elif counter >= 1 and counter != chuckSize-1:
            start = div*counter+1 
            end =  div*counter+div
            if chuckSize == 2:
                start = div*counter+1
                end = numberOfFeatures 
        elif counter == chuckSize-1:
            start = div*counter+1 
            end = numberOfFeatures
        print (start, end)
	
        geojson2 = {"type": data['type'],"features":data['features'][start:end]}
        	
        with open(outdir+"ObservationSplit"+str(counter)+".geojson", "w") as f:
            	json.dump(geojson2,f,indent=4,sort_keys=True)
        counter += 1

	print("done")
	

def main():          
                
    script = sys.argv[0]  
    geojson = sys.argv[1] 
    outdir = sys.argv[2]
    geoJsonSplit(geojson,outdir)
                                              
if __name__ == '__main__':
    main()
