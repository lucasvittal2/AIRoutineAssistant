from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pandas import DataFrame as PandasDataFrame
import findspark
from Interfaces.DatabaseHandler import DatabaseHandler
from Env.paths import DRIVERS_PATH,CONFIG_PATH
from Utils.file_handler import read_yaml
from Env.project_types import *

class PostgresHandler(DatabaseHandler):
    def __init__(self):
        findspark.init()
        self.sparkSession = SparkSession.builder \
                            .appName("Postgres Datawarehouse Connection with PySpark") \
                            .config("spark.jars", DRIVERS_PATH + "postgresql-42.7.1.jar") \
                            .getOrCreate()
        
        self.postgres_configs  = read_yaml(CONFIG_PATH + 'app_config.yaml')['databases']['postgres']
        
        #set disconnect statte
        self.url = None
        self.properties= None

    def connect(self, db_name: str) -> None:
        
        host = self.postgres_configs['host']
        port =self.postgres_configs['port']
        user = self.postgres_configs['user']
        password = self.postgres_configs['password']
        driver = self.postgres_configs['driver']
        
        self.properties = {
            "user": user,
            "password": password,
            "driver": driver
        }
        self.url = f"jdbc:postgresql://{host}:{port}/{db_name}"

    def disconnect(self):
        #set disconnect statte
        self.url = None
        self.properties= None
        
    def __filter_duplicates(self, table_name: str, data: SparkDataFrame) -> SparkDataFrame:
        df = self.sparkSession.jdbc(self.url, table_name, properties=self.properties)
        last_update = df.agg({"extraction_date": "max"}).collect()[0][0]
        filtered_df = data.filter(f"extraction_date > '{last_update}'")
        return filtered_df

    def write_data(self, table_name: str, data: PandasDataFrame) -> None:
        spark_df = SparkDataFrame(data)
        filtered_df = self.__filter_duplicates(table_name, spark_df)
        filtered_df.write.jdbc(self.url, table_name, properties=self.properties, mode='overwrite')

    def read_data(self, table_name: str) -> PandasDataFrame:
        df = self.sparkSession.jdbc(self.url, table_name, properties=self.properties)
        return df.toPandas()