-- Drop if exist table for reason of update schemas

DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Attachments;
DROP TABLE IF EXISTS CompletedTasks;
DROP TABLE IF EXISTS OpenedTasks;
DROP TABLE IF EXISTS Tasks;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS productivitystats;
DROP TABLE IF EXISTS Projects;

CREATE TABLE Projects(
    id CHAR(10) PRIMARY KEY NOT NULL,
    name VARCHAR(255),
    color VARCHAR(100),
    comment_count INT,
    is_favorite INT,
    is_inbox_project INT,
    is_shared INT,
    is_team_inbox INT,
    "order" INT,
    parent_id INT,
    url VARCHAR(255),
    view_style VARCHAR(50),
    extraction_datetime TIMESTAMP NOT NULL
);



CREATE TABLE ProductivityStats(
    id CHAR(24) PRIMARY KEY NOT NULL,
    date TIMESTAMP,
    total_completed INT,
    extraction_datetime TIMESTAMP NOT NULL
    
);

CREATE TABLE Items(
    date TIMESTAMP,
    prod_stats_id CHAR(24) NOT NULL,
    project_id CHAR(10) NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(id),
    FOREIGN KEY (prod_stats_id) REFERENCES ProductivityStats(id)
);


CREATE TABLE Tasks (
    id CHAR(10) PRIMARY KEY NOT NULL,
    project_id CHAR(10),
    section_id CHAR(9),
    content VARCHAR(500),
    extraction_datetime TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(id)
);

CREATE TABLE CompletedTasks(
    id CHAR(10) PRIMARY KEY NOT NULL,
    user_id CHAR(8) NOT NULL,
    FOREIGN KEY (id) REFERENCES Tasks(id)
);

CREATE TABLE OpenedTasks(
    id CHAR(10) PRIMARY KEY NOT NULL,
    assignee_id CHAR(8) NOT NULL,
    assigner_id CHAR(8) NOT NULL,
    comment_count INT,
    created_at TIMESTAMP,    
    creator_id CHAR(8) NOT NULL,
    description VARCHAR(500),
    due TIMESTAMP,
    labels VARCHAR(255),
    "order" INT,
    parent_id CHAR(10),
    priority INT,
    url VARCHAR(255),
    FOREIGN KEY (id) REFERENCES Tasks(id)
);
CREATE TABLE Attachments(
    id CHAR(24) PRIMARY KEY NOT NULL,
    title VARCHAR(255),
    resource_type VARCHAR(50),
    file_size INT,
    file_type VARCHAR(50),
    file_url VARCHAR(255),
    file_duration FLOAT,
    file_name VARCHAR(100),
    upload_state VARCHAR(50),
    image VARCHAR(255),
    image_width INT,
    image_height INT,
    url VARCHAR(255)
);

CREATE TABLE comments (
     id CHAR(10)  PRIMARY KEY NOT NULL,
    attachment_id CHAR(24) NOT NULL,
    content VARCHAR(4000),
    posted_at TIMESTAMP NOT NULL,
    task_id CHAR(10) NOT NULL,
    extraction_datetime TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES Tasks(id),
    FOREIGN KEY (attachment_id) REFERENCES Attachments(id)
);

