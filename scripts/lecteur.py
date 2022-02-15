import pandas as pd
from database import *
from pathlib import Path

print("Avant le connect ")
db,col = connect('db','id')
#os.path.abspath('2021_10_08_video_ids.csv')
csv_read = pd.read_csv(Path('scripts/2021_10_08_video_ids.csv').absolute(), sep =';')



for idx in csv_read['video_id'][:10] :
     store_data(col,{"id":idx})


print(list(col.find()))
print("On est après le connect")
# col.drop()