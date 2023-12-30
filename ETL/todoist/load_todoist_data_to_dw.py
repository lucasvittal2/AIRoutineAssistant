import pyspark
from DatabaseHandler.MongoDBHandler import MongoDBHandler
from DatabaseHandler.PostgresHandler import PostgresHandler
from pandas import DataFrame as PandasDataFrame

postgresdb = PostgresHandler()
mongodb = MongoDBHandler()

#connect to todoist database
mongodb.connect("todoist")
postgresdb.connect("todoist")

#load data from mongodb
comments = mongodb.read_data("comments", {})
opened_tasks = mongodb.read_data("opened_tasks", {})
completed_tasks = mongodb.read_data("completed_tasks", {})
projects = mongodb.read_data("projects", {})    
productivity_stats = mongodb.read_data("productivity_stats", {})

#write data to postgres


#load projects
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

#load producitvity stats and items

raw_prod_stats_df = PandasDataFrame(productivity_stats)
prod_stats_df =raw_prod_stats_df[['date','total_completed','extraction_datetime','_id']]
prod_stats_df['id'] = raw_prod_stats_df['_id'].astype(str)
prod_stats_df.drop(['_id'], axis=1, inplace=True)



items_set = raw_prod_stats_df[['date','items']].to_dict('records')
items  = [{'date': items['date'], **item} for items in items_set for item in items['items']]
items_df= PandasDataFrame(items)
items_df = prod_stats_df[['date','id']].merge(items_df, on='date', how='inner').drop(['completed'], axis=1)
items_df.columns = ['date', 'prod_stats_id','project_id']


postgresdb.write_data('productivitystats', prod_stats_df)
postgresdb.write_data('items', items_df)



#opened_tasks, completed tasks  and tasks






#load attachments and comments

raw_comments_df = PandasDataFrame(comments)
raw_comments_df = raw_comments_df.drop_duplicates(subset='id', keep="first")

comments_df = raw_comments_df[['id', 'content','task_id', 'posted_at',  'extraction_datetime']]

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
attachments_df['id'] = raw_comments_df['_id'].astype(str)
comments_df['attachment_id'] = attachments_df['id']
postgresdb.write_data('attachments', attachments_df)
#postgresdb.write_data('comments', comments_df)
print("ok!")


# opened_tasks_df = PandasDataFrame(opened_tasks)
# completed_tasks_df = PandasDataFrame(completed_tasks)
# projects_df = PandasDataFrame(projects)
# productivity_stats_df = PandasDataFrame(productivity_stats)











