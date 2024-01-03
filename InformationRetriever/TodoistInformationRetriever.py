from DatabaseHandler.PostgresHandler import PostgresHandler


class TodoistInformationRetriever:
    def __init__(self):
        self.postgres_handler = PostgresHandler()
        self.postgres_handler.connect('todoist')
        

    def get_opened_tasks_amount(self):
        query = "SELECT COUNT(*) FROM openedtasks;"
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_opened_tasks(self):
        query = """
            SELECT t.content  FROM openedtasks ot 
            INNER JOIN  tasks t on ot.id = t.id 
            WHERE ot.parent_id IS NULL;
        """
        response = self.postgres_handler.read_data(query)
        return response['content'].tolist()
    
    def get_subtasks_amount(self, task:str = None):
        if task:
            query = f"""
                SELECT COUNT(ot.id)
                FROM openedtasks ot 
                INNER JOIN  tasks t 
                ON ot.parent_id = t.id 
                WHERE ot.parent_id IS NOT NULL
                AND t.content='{task}';
            """
        else:
            query = """
                SELECT COUNT(parent_id)  
                FROM openedtasks
                WHERE parent_id IS NOT NULL;
            """
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_completed_taks_amount(self, date:str = None):
        if date:
            query = f"""
                SELECT COUNT(*) FROM completedtasks
                WHERE DATE(completed_at)=DATE('{date}');
            """
        else:
            query = """
                SELECT COUNT(*) FROM completedtasks;
            """
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_completed_taks_avg_amount(self):

        query = """
            SELECT 
            COUNT(*)/COUNT(DISTINCT(DATE(completed_at))) as count
            FROM completedtasks;
        """
        response = self.postgres_handler.read_data(query)
        return response['count'][0]
    
    def get_completed_taks(self, date:str = None):
        if date:
            query = f"""
                    SELECT t.content  
                    FROM completedtasks ct 
                    INNER JOIN tasks t
                    ON t.id=ct.id
                    WHERE DATE(completed_at)=DATE('{date}') ;

                """
        else:
            return None
        response = self.postgres_handler.read_data(query)
        return[] if response.empty else response['content'].tolist()
    
    def get_projects_completed_tasks(self, date:str = None):
        if date:
            query = f"""
                SELECT p.name, COUNT(*) as count
                FROM completedtasks ct 
                INNER JOIN tasks t
                ON t.id=ct.id
                INNER JOIN projects p
                ON t.project_id=p.id
                WHERE DATE(completed_at)=DATE('{date}')
                GROUP BY p.name
                ORDER BY count DESC;
            """
        else:
            query = f"""
                SELECT p.name, COUNT(*) as count
                FROM completedtasks ct 
                INNER JOIN tasks t
                ON t.id=ct.id
                INNER JOIN projects p
                ON t.project_id=p.id
                GROUP BY p.name
                ORDER BY count DESC;
            """
        response = self.postgres_handler.read_data(query)
        return response.to_dict('records')
    
    
    
    def get_comments(self, task: str, date:str = None):
        
        if date:
            query = f"""
            SELECT t.id, c.posted_at, c.content, a.file_url 
            FROM comments c INNER JOIN  tasks t 
            ON t.id=c.task_id
            INNER JOIN  attachments a
            ON c.attachment_id=a.id 
            WHERE t.content='{task}'
            AND DATE(c.posted_at)=DATE('{date}');
            """
        else:
            query = f"""
            SELECT t.id, c.posted_at, c.content, a.file_url  
            FROM comments c INNER JOIN  tasks t 
            ON t.id=c.task_id
            INNER JOIN  attachments a
            ON c.attachment_id=a.id 
            WHERE t.content='{task}';
            """
        response = self.postgres_handler.read_data(query)
        
        if response.empty:
            return []

        contents = [content + '\n\n' if content != "" else content for content in response['content'].tolist()]
        attachmets = response['file_url'].tolist()
        return [f'{contents[i]} você anexou o arquivo: {attachmets[i]}' for i in range(len(contents))]
    
    def get_comments_by_word(self, key_word:str):
        query= f"""
            SELECT t.id, c.posted_at, c.content, a.file_url 
            FROM comments c INNER JOIN  tasks t 
            ON t.id=c.task_id
            INNER JOIN  attachments a
            ON c.attachment_id=a.id 
            WHERE LOWER(c.content) LIKE LOWER('%{key_word}%');
        """
        
        response = self.postgres_handler.read_data(query)
        contents = [content + '\n\n' if content != "" else content for content in response['content'].tolist()]
        attachmets = response['file_url'].tolist()
        
        return [f'{contents[i]} você anexou o arquivo: {attachmets[i]}' for i in range(len(contents))]
    