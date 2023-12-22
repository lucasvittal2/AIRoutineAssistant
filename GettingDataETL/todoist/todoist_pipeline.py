from TodoIstExtractor import TodoIstExtractor
from Env.paths import *
extractor = TodoIstExtractor()

print ('Extracting data from Todoist...')
data = extractor.extract_data()

extractor.load_on_database(data['opened_tasks'], 'opened_tasks.csv')
extractor.load_on_database(data['completed_tasks'], 'completed_tasks.csv')
extractor.load_on_database(data['projects'], 'projects.csv')
extractor.load_on_database(data['comments'], 'comments.csv')
extractor.load_on_database(data['productivity_stats'], 'productivity_stats.csv')

