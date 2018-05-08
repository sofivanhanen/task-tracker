# Architecture

## Overview

All data is user-specific, and there is only one type of user. The user has tasks and classes relevant to her account, and work sessions relevant to her tasks. There is a many to many -relationship between classes and tasks, as one task can belong to many classes.

Tasks know their name, current progress, original estimate of time required to complete, and status of completion. Work sessions know the date and time when they were initiated and length and quality of the session. Classes only know their own name, and accounts have a user name, a nickname, and a password.

## Database diagram

All tables except classtask also have an id (Integer) column as primary key, a date_created (DateTime) column, and a date_modified (DateTime) column.

![Diagram](database_diagram.png)

## Database schema

```sql
CREATE TABLE account (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	username VARCHAR(144) NOT NULL,
	password VARCHAR(144) NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE class (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(account_id) REFERENCES account (id)
)

CREATE TABLE task (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	done BOOLEAN NOT NULL,
	estimate INTEGER,
	progress FLOAT,
	account_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	CHECK (done IN (0, 1)),
	FOREIGN KEY(account_id) REFERENCES account (id)
)

CREATE TABLE working_period (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	time DATETIME NOT NULL,
	length INTEGER NOT NULL,
	quality FLOAT,
	task_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(task_id) REFERENCES task (id)
)

CREATE TABLE classtask (
	class_id INTEGER,
	task_id INTEGER,
	FOREIGN KEY(class_id) REFERENCES class (id),
	FOREIGN KEY(task_id) REFERENCES task (id)
)
```
