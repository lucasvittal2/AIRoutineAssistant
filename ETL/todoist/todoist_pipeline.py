import os
from TodoIstExtractor import TodoIstExtractor
from ETL.transformations import *
from Env.paths import *
extractor = TodoIstExtractor()
print('*'*150)
print ('Extracting data from Todoist...')

#extract data
data = extractor.extract_data()
print('data extracted succefully !!')
print('*'*150)

# transform data

print('-'*150)
print('Transforming data...')
data['opened_tasks'] = change_tz(data['opened_tasks'], 'created_at', 'America/Sao_Paulo') 
data['completed_tasks'] = change_tz(data['completed_tasks'], 'completed_at', 'America/Sao_Paulo')
data['comments'] = change_tz(data['comments'], 'posted_at', 'America/Sao_Paulo')
data['productivity_stats'] = change_tz(data['productivity_stats'], 'date', 'America/Sao_Paulo')

print(
        """
    data['opened_tasks'] = change_tz(data['opened_tasks'], 'created_at', 'America/Sao_Paulo') 
    data['completed_tasks'] = change_tz(data['completed_tasks'], 'completed_at', 'America/Sao_Paulo')
    data['comments'] = change_tz(data['comments'], 'posted_at', 'America/Sao_Paulo')
    data['productivity_stats'] = change_tz(data['productivity_stats'], 'date', 'America/Sao_Paulo')
    """
)

print('data transformed succefully !!')
print('-'*150)

# track save and save locally
print('-'*150)
print('tracking data....')
extractor.track_data_and_save_locally(data['opened_tasks'], 'opened_tasks.pkl')
extractor.track_data_and_save_locally(data['completed_tasks'], 'completed_tasks.pkl')
extractor.track_data_and_save_locally(data['projects'], 'projects.pkl')
extractor.track_data_and_save_locally(data['comments'], 'comments.pkl')
extractor.track_data_and_save_locally(data['productivity_stats'], 'productivity_stats.pkl')

print(f"""
    Data tracked and saved locally succefully !!\n
    The data was saved on  {EXTRACTED_DATA_PATH + 'Todoist/'} \n
    {  os.listdir(EXTRACTED_DATA_PATH + 'Todoist/')}
    
    """)

print('Data tracking finished !!')
print('-'*150)
print('Job \'todoist_pipeline\' finished !!')
