from formats import parseFile
from formats import formats
import glob
import matplotlib.pyplot as plot

# for developing in VSCode
import importlib 
importlib.reload(formats)

# create datastructure
s_data = formats.create_datastr()

# specify directory and parse fit.gz files
files_dir = glob.glob("*.fit.gz")
for file in files_dir:
    parseFile.parse(s_data,file)

# write out to folder
out_dir = "new_dataset"    
formats.write_xlsx(s_data,out_dir)

# # load dateset from folder
# read_dir = "new_dataset"
# strava_data = format.read_xlsx(read_dir,activities=["4236163930"])
# print(strava_data['activities'].keys())
