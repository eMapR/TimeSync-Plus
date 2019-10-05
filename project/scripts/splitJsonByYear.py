#================================================================================
# This script splits a multi year geojson in smaller single year geojson files. 
# the multi year geojson needs a uniqID value with a syntax where 14 and 18 characters
# are a year value (1995) or results will be unfavorable. 
#---------example--------
# python [path to jsonsplit.py] [file path to geojsonfile] [file path to a empty output directory]
#
# python ./jsonsplit.py ./observation.geojson
#
#       What is the start year? (this is the first year of your dataset )
#
#       What is the end year ? (this is the last year in your dataset)
#
#===========================================================================
import json
import sys
import operator
import os

def geoJsonSplit(geojson,outdir):

    # open the geojson and reads the contents
    with open(geojson, 'r+') as f:
        data = json.load(f)

    #get start year and end year
    startYear = int(raw_input("What is the starting year? :"))
    if len(str(startYear)) != 4:
        print("try again")
        startYear = int(raw_input("What is the starting year? :"))
 
    endYear = int(raw_input("What is the ending year? :"))+1
    if len(str(endYear)) != 4:
        print("try again")
        endYear = int(raw_input("What is the ending year? :"))+1

    #sort
    sorted_obj = dict(data) 
    #sorted_obj['features'] = sorted(data['features'], key=lambda x : x['properties']['uniqID'][14:18], reverse=False)
    sorted_obj['features'] = sorted(data['features'], key=lambda x : x['properties']['yod'], reverse=False)

    #loop over the range lenght from the start to the end year.
    for Year in range(int(startYear),int(endYear)):

        #filters and list indexs of a matching year   
        #output_list = [x for x in sorted_obj['features'] if str(Year) == x['properties']['uniqID'][14:18]]
        output_list = [x for x in sorted_obj['features'] if Year == x['properties']['yod']]
        if len(output_list) < 1:
            print("geojson ID issues")
            sys.exit()


        # dictionary of year
        data['features'] = output_list

        print("writing geojson file here: "+outdir+'/observation_'+str(Year)+'.geojson')

        with open(outdir+'/observation_'+str(Year)+'.geojson', "w") as g:
            json.dump(data,g,indent=4,sort_keys=True)

        output_index = []

def main():

    script = sys.argv[0]

    geojson = sys.argv[1]
    if os.path.isfile(geojson):
        print("Reading geojson file.")
    else:
        sys.exit('Check your geojson filepath.')
    outdir = sys.argv[2]
    if os.path.isdir(outdir): 
        print("Out directory is real.")
    else:
        sys.exit('Check your output directory pathway.')

    geoJsonSplit(geojson,outdir)

if __name__ == '__main__':
    main()

