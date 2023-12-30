import pyspark
from DatabaseHandler.MongoDBHandler import MongoDBHandler

sparkSession = pyspark.sql.SparkSession.builder.appName("todoist").getOrCreate()
mongodb = MongoDBHandler()

#connect to todoist database
mongodb.connect("todoist")

#load data from mongodb
comments = mongodb.read_data("comments", {})
opened_tasks = mongodb.read_data("opened_tasks", {})
completed_tasks = mongodb.read_data("completed_tasks", {})
projects = mongodb.read_data("projects", {})    
productivity_stats = mongodb.read_data("productivity_stats", {})


