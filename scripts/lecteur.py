import pandas as pd
from database import *


db,col = connect('db','id')

csv_read = pd.read_csv('2021_10_08_video_ids.csv', sep =';')



for idx in csv_read['video_id'][:10] :
     store_data(col,{"id":idx})


print(list(col.find()))

# col.drop()