# CSV 2 flare.json
# convert a csv file to flare.json for use with many D3.js viz's
# This script creates outputs a flare.json file with 2 levels of nesting.
# For additional nested layers, add them in lines 32 - 47
# sample: http://bl.ocks.org/mbostock/1283663

# author: Andrew Heekin
# MIT License

import pandas as pd
pd.set_option("display.max_columns", None)
import json


df = pd.read_csv('../538/data-college-majors/all-ages.csv')

# choose columns to keep, in the desired nested json hierarchical order
df = df[["Major_category", "Major", "Total","Employed","Unemployed","Unemployment_rate"]]


# order in the groupby here matters, it determines the json nesting
# the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
df1 = df.groupby(['Major_category', 'Major'])[["Total","Unemployed","Employed",'Unemployment_rate']].sum()
df1 = df1.reset_index()
# start a new flare.json document
flare = dict()
flare = {"name":"flare", "children": []}


for line in df1.values:
    the_parent = line[0]
    the_child = line[1]
    unemployed = line[3] 
    employed = line[4]#
    rate = line[5]
    keys_list = []
    # if the_parent == "Interdisciplinary":
    #     print("match")
    #     print(the_child)
    # for item in d['children']:
    for item in flare["children"]:
        keys_list.append(item['name'])
    # print(keys_list)
    # if 'the_parent' is NOT a key in the flare.json yet, append it
    if not the_parent in keys_list:
        #add parent class
        flare['children'].append({"name":the_parent, "children":[]})
        keys_list.append(the_parent)
        flare['children'][keys_list.index(the_parent)]['children'].append({"name":the_child, "value":rate, "total": unemployed + employed, 
            "unemployed":unemployed})   
    # if 'the_parent' IS a key in the flare.json, add a new child to it
    else:
        flare['children'][keys_list.index(the_parent)]['children'].append({"name":the_child, "value":rate, "total": unemployed + employed, 
            "unemployed":unemployed})   
for cat in flare["children"]:
    unemployed_ = 0
    total_ = 0
    if cat["name"] != "Interdisciplinary":
        for major in cat["children"]:
            unemployed_ += major["unemployed"]
            total_ += major["total"]
        if total_ != 0:
            overall = unemployed_ / total_
            cat["value"] = overall
        else:
            cat["value"] = None
    else:
        #print("match")
        for major in cat["children"]:
            #print(major)
            unemployed_ += major["unemployed"]
            total_ += major["total"]
        if total_ != 0:
            overall = unemployed_ / total_
            cat["value"] = overall
        else:
            cat["value"] = None


#print(flare)
# export the final result to a json file
with open('../538/flare.json', 'w') as outfile:
    json.dump(flare, outfile)
