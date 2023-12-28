CREATE DATABASE IF NOT EXISTS 'todo_ist_db';
USE 'todo_ist_db';


-- Drop if exist table for reason of update schemas

DROP TABLE IF EXISTS Attachments;
DROP TABLE IF EXISTS CompletedTasks;
DROP TABLE IF EXISTS OpenedTasks;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Tasks;
DROP TABLE IF EXISTS ProductivityStats;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Projects;


-- create new database tables
CREATE IF NOT EXISTS Projects(
    id CHAR(10) PRIMARY KEY NOT NULL,
    name VARCHAR(255),
    color VARCHAR(100),
    comment_count INT,
    is_favorite INT,
    is_inbox_project INT,
    is_shared INT,
    is_team_inbox INT,
    order INT,
    parent_id CHAR(10),
    url VARCHAR(255),
    view_style VARCHAR(50),
    extraction_datetime DATETIME NOT NULL

);

CREATE TABLE IF EXISTS Items(
    date DATETIME,
    project_id CHAR(10),
    project_id refrences Projects(id)
);

CREATE TABLE IF EXISTS ProductivityStats(
    date DATETIME,
    total_completed INT,
    extraction_datetime DATETIME NOT NULL
    date refrences Items(date)
);


CREATE TABLE IF NOT EXISTS Tasks (
    id CHAR(10) PRIMARY KEY NOT NULL,
    project_id CHAR(10),
    section_id CHAR(9),
    content VARCHAR(500),
    extraction_datetime DATETIME NOT NULL,
    project_id refrences Projects(id)
);


CREATE TABLE  IF NOT EXISTS CompletedTasks(
    id CHAR(10) PRIMARY KEY NOT NULL,
    user_id CHAR(8) NOT NULL,
    id refrences Tasks(id)
);


CREATE TABLE IF NOT EXISTS OpenedTasks(
    id CHAR(10) PRIMARY KEY NOT NULL,
    assignee_id CHAR(8) NOT NULL,
    assigner_id CHAR(8) NOT NULL,
    comment_count INT,
    created_at DATETIME,    
    creator_id CHAR(8) NOT NULL,
    description VARCHAR(500),
    due DATETIME
    labels VARCHAR(255),
    order INT,
    parent_id CHAR(10),
    priority INT,
    url VARCHAR(255),
    id refrences Tasks(id)
);


CREATE TABLE IF NOT EXISTS comments (
    id CHAR(10)  PRIMARY KEY NOT NULL,
    attachment_id CHAR(10) NOT NULL,
    content VARCHAR(500),
    posted_at DATETIME NOT NULL,
    task_id CHAR(10) NOT NULL,
    extraction_datetime DATETIME NOT NULL,
    task_id refrences Tasks(id),
    attachment_id refrences Attachments(id)

);

CREATE TABLE IF NOT EXISTS Attachments(
    id CHAR(10) PRIMARY KEY NOT NULL,
    title VARCHAR(255),
    resource_type VARCHAR(50),
    file_size INT,
    file_type VARCHAR(50),
    file_url VARCHAR(255),
    file_duration FLOAT,
    upload_state VARCHAR(50),
    image VARCHAR(255),
    image_width INT,
    image_height INT,
    url VARCHAR(255),
    extraction_datetime DTETIME NOT NULL
);
