
from DatabaseHandler.MongoDBHandler import MongoDBHandler
from DatabaseHandler.PostgresHandler import PostgresHandler
from pandas import DataFrame as PandasDataFrame, concat
from datetime import datetime

print('setup postgres and mongodb connections...')
postgresdb = PostgresHandler()
mongodb = MongoDBHandler()

print('-'*180)
print('')
#connect to todoist database
mongodb.connect("todoist")
postgresdb.connect("todoist")
print('App connected to databases successfully!')

#load data from mongodb
print('*'*180)
print('')
print('loading data from stagging on mongo...')
comments = mongodb.read_data("comments", {})
opened_tasks = mongodb.read_data("opened_tasks", {})
completed_tasks = mongodb.read_data("completed_tasks", {})
projects = mongodb.read_data("projects", {})    
productivity_stats = mongodb.read_data("productivity_stats", {})
print('data loaded successfully!')
print('')
print('*'*180)


#write data to postgres


#load projects
print('*'*180)
print('')
print('loading projects data on Postgres Datawarehouse...')

raw_projects_df = PandasDataFrame(projects)
raw_projects_df = raw_projects_df.drop_duplicates(subset='id', keep="first")

projects_df = raw_projects_df[['id', 'name', 'color', 'comment_count', 
                               'is_favorite', 'is_inbox_project', 'is_shared', 'is_team_inbox',
                               'order', 'parent_id', 'url', 'view_style', 
                               'extraction_datetime'
                            ]]
projects_df['is_favorite'] = projects_df['is_favorite'].replace({True: 1, False: 0})
projects_df['is_inbox_project'] = projects_df['is_inbox_project'].replace({True: 1, False: 0})
projects_df['is_shared'] = projects_df['is_shared'].replace({True: 1, False: 0})
projects_df['is_team_inbox'] = projects_df['is_team_inbox'].replace({True: 1, False: 0})
postgresdb.write_data('projects', projects_df)

print('Projects data loaded successfully on Postgres Datawarehouse!')
print('')
print('*'*180)


#load producitvity stats and items
print('loading producitvity data on Postgres Datawarehouse...')
raw_prod_stats_df = PandasDataFrame(productivity_stats)
prod_stats_df =raw_prod_stats_df[['date','total_completed','extraction_datetime','_id']]
prod_stats_df['id'] = raw_prod_stats_df['_id'].astype(str)
prod_stats_df.drop(['_id'], axis=1, inplace=True)


items_set = raw_prod_stats_df[['date','items']].to_dict('records')
items  = [{'date': items['date'], **item} for items in items_set for item in items['items']]
items_df= PandasDataFrame(items)
items_df = prod_stats_df[['date','id','extraction_datetime']].merge(items_df, on='date', how='inner').drop(['completed'], axis=1)
items_df.columns = ['date', 'prod_stats_id','extraction_datetime','project_id']


postgresdb.write_data('productivitystats', prod_stats_df)
postgresdb.write_data('items', items_df)
print('Producitvity data loaded successfully on Postgres Datawarehouse!')
print('')
print('*'*180)



#opened_tasks, completed tasks  and tasks
print('*'*180)
print('')
print('loading tasks data on Postgres Datawarehouse...')
raw_opened_tasks_df = PandasDataFrame(opened_tasks)
raw_completed_tasks_df = PandasDataFrame(completed_tasks) 
raw_completed_tasks_df = raw_completed_tasks_df.drop_duplicates(subset='id', keep="first")

tasks_cols=['id','project_id','section_id','content','extraction_datetime']
tasks_df =  concat([raw_opened_tasks_df[tasks_cols], raw_completed_tasks_df[tasks_cols]], axis=0)
tasks_df = tasks_df.drop_duplicates(subset='id', keep="first")
tasks_df.columns = ['id','project_id','section_id','content','extraction_datetime']


completed_tasks_df = raw_completed_tasks_df[['id','completed_at','user_id','extraction_datetime']]
completed_tasks_df.columns = ['id','completed_at','user_id','extraction_datetime']
completed_tasks_df = completed_tasks_df.drop_duplicates(subset='id', keep="first")

opened_tasks_df = raw_opened_tasks_df[[
                        'id','assignee_id','comment_count','created_at',
                        'creator_id','description','due','labels','order',
                        'parent_id','priority','url','extraction_datetime'
                        ]]

opened_tasks_df.columns =[
                        'id','assignee_id','comment_count','created_at',
                        'creator_id','description','due','labels','order',
                        'parent_id','priority','url','extraction_datetime']


opened_tasks_df['due'] = opened_tasks_df['due'].apply(lambda x: datetime.strptime(x['date'], '%Y-%m-%d') if x is not None else None)
opened_tasks_df = opened_tasks_df.drop_duplicates(subset='id', keep="first")

postgresdb.write_data('tasks', tasks_df)
postgresdb.write_data('completedtasks', completed_tasks_df)
postgresdb.write_data('openedtasks', opened_tasks_df)
print('Tasks data loaded successfully on Postgres Datawarehouse!')
print('')
print('*'*180)


#load attachments and comments
print('*'*180)
print('')
print('loading comnments data on Postgres Datawarehouse...')

raw_comments_df = PandasDataFrame(comments)
raw_comments_df = raw_comments_df.drop_duplicates(subset='id', keep="first")

comments_df = raw_comments_df[['id', 'content','task_id', 'posted_at',  'extraction_datetime']]
comments_df = comments_df[ comments_df['task_id'].isin(tasks_df['id'].to_list())] #filter comments that are not related to tasks

attchement_none_row = {
    'resource_type': None,
    'file_name': None,
    'file_size': None,
    'file_type': None,
    'file_url': None,
    'file_duration': None,
    'upload_state': None,
    'image': None,
    'image_width': None,
    'image_height': None,
    'url': None,
    'title': None
  }
attachments = [el if el != None else attchement_none_row  for el in raw_comments_df['attachment'].to_list() ]
attachments_df = PandasDataFrame(attachments)
attachments_df['attachment_id'] = raw_comments_df['_id'].astype(str)
comments_df['attachment_id'] = attachments_df['attachment_id']
attachments_df = attachments_df.merge(comments_df[['attachment_id','extraction_datetime']], on='attachment_id', how='inner')
attachments_df.columns = ['resource_type', 'file_name', 'file_size', 'file_type', 'file_url',
       'file_duration', 'upload_state', 'image', 'image_width', 'image_height',
       'url', 'title', 'id','extraction_datetime']

postgresdb.write_data('attachments', attachments_df)
postgresdb.write_data('comments', comments_df)

print('Tasks data loaded successfully on Postgres Datawarehouse!')
print('')
print('*'*180)
print('-'*180)

print("Todoist data loaded on Postgres Datawarehouse succefully!")
print('Job terminated successfully!')












