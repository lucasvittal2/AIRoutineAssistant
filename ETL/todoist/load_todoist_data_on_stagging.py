from DatabaseHandler.MongoDBHandler import MongoDBHandler
import pandas as pd
from Env.project_types import *
from Env.paths import EXTRACTED_DATA_PATH
import os

print('-'*150)
print("reading todoist data saved locally...")

file_lst = os.listdir(EXTRACTED_DATA_PATH + 'Todoist/')
comments_df = pd.read_pickle(EXTRACTED_DATA_PATH + 'Todoist/comments.pkl')
print(f'read {file_lst[0]}')
projects_df = pd.read_pickle(EXTRACTED_DATA_PATH + 'Todoist/projects.pkl')
print(f'read {file_lst[1]}')
opened_tasks_df = pd.read_pickle(EXTRACTED_DATA_PATH + 'Todoist/opened_tasks.pkl')
print(f'read {file_lst[2]}')
completed_tasks_df = pd.read_pickle(EXTRACTED_DATA_PATH + 'Todoist/completed_tasks.pkl')
print(f'read {file_lst[3]}')
productivity_stats_df = pd.read_pickle(EXTRACTED_DATA_PATH + 'Todoist/productivity_stats.pkl')
print(f'read {file_lst[4]}')
print('data read succefully !!')
print('-'*150)
print('')
#connect to database
try:
    print('connecting to database...')
    mongodb = MongoDBHandler()
    mongodb.connect('todoist')
    print('connection were succefully !!')
except:
    print('connection failed !!')
    raise Exception('Mongodb connection failed !!')

print("writing todoist data on database...")

mongodb.write_data('comments', comments_df.to_dict('records'))
print("Comments data written !!")
mongodb.write_data('projects', projects_df.to_dict('records'))
print("Projects data written !!")
mongodb.write_data('opened_tasks', opened_tasks_df.to_dict('records'))
print("OpenedTasks data written !!")
mongodb.write_data('completed_tasks', completed_tasks_df.to_dict('records'))
print("CompletedTasks data written !!")
mongodb.write_data('productivity_stats', productivity_stats_df.to_dict('records'))
print("ProductivityStats data written !!")
print('-'*150)
print('')

print('Data loaded to stagging succefully !!')

