from TodoIstExtractor import TodoIstExtractor
from Env.paths import *
extractor = TodoIstExtractor()

print ('Extracting data from Todoist...')
data = extractor.extract_data()

extractor.load_on_database(data['opened_tasks'], 'opened_tasks.pkl')
extractor.load_on_database(data['completed_tasks'], 'completed_tasks.pkl')
extractor.load_on_database(data['projects'], 'projects.pkl')
extractor.load_on_database(data['comments'], 'comments.pkl')
extractor.load_on_database(data['productivity_stats'], 'productivity_stats.pkl')

