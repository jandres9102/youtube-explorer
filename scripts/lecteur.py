import pandas as pd
import numpy as np
from database import *
from pathlib import Path
import datetime

col = connect('db','id')
#os.path.abspath('2021_10_08_video_ids.csv')
csv_read = pd.read_csv(Path('scripts/2021_10_08_video_ids.csv').absolute(), sep =';')

col.drop()


for idx in csv_read['video_id'][:3]:
     store_data(col,{"id":idx,"status_video":"0","status_commentaire":"0","label":0}) # status will be used to know if we download data 

if __name__ == "__main__":
     print(list(col.find()))


"""
csv_read['last_inspection_date'] = np.NaN
csv_read['debug_msg'] = np.NaN
csv_read['warning_msg'] = np.NaN
csv_read['error_msg'] = np.NaN
csv_read.to_csv('logger_'+datetime.datetime.today().strftime('%Y-%m-%d'), index=False)
"""