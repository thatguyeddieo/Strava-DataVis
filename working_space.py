from calcs import limits
from calcs import convert

import numpy as np 
from utils import googleAPI

import importlib
importlib.reload(googleAPI)
importlib.reload(convert)


zoom = 13
scale = 4 
center = [47.695239,-122.373471]
api_path = "/Users/eddiebunzo/Desktop/Python/google_api_key.txt"
with open(api_path) as a:
        api_key = a.readline()
img_name = "test"

googleAPI.get_map(zoom,scale,center,api_key,img_name,check=True)