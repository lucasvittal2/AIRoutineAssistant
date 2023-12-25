from TodoIstExtractor import TodoIstExtractor
from GettingDataETL.transformations import *
from Env.paths import *
extractor = TodoIstExtractor()

print ('Extracting data from Todoist...')

#extract data
data = extractor.extract_data()

# transform data

data['opened_tasks'] = change_tz(data['opened_tasks'], 'created_at', 'America/Sao_Paulo') 
data['completed_tasks'] = change_tz(data['completed_tasks'], 'completed_at', 'America/Sao_Paulo')
data['comments'] = change_tz(data['comments'], 'posted_at', 'America/Sao_Paulo')
data['productivity_stats'] = change_tz(data['productivity_stats'], 'date', 'America/Sao_Paulo')

# load data
extractor.load_on_database(data['opened_tasks'], 'opened_tasks.pkl')
extractor.load_on_database(data['completed_tasks'], 'completed_tasks.pkl')
extractor.load_on_database(data['projects'], 'projects.pkl')
extractor.load_on_database(data['comments'], 'comments.pkl')
extractor.load_on_database(data['productivity_stats'], 'productivity_stats.pkl')



