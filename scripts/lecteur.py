import pandas as pd
from database import *
from pathlib import Path

db,col = connect('db','id')
#os.path.abspath('2021_10_08_video_ids.csv')
csv_read = pd.read_csv(Path('scripts/2021_10_08_video_ids.csv').absolute(), sep =';')



for idx in csv_read['video_id'] :
     store_data(col,{"id":idx})

if __name__ == "__main__":
     print(list(col.find()))
# col.drop()