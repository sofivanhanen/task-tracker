# User stories

As a user, I want to...

- log in to have access to a personalized account
- add tasks so I can keep track of my tasks
- add working periods to keep tracks of my work habits
- attach working periods to tasks to see which tasks are progressing
- evaluate the quality of my working periods to see trends in my work
- attach dates and lengths to working periods to see trends in my work
- mark a task as finished so I can see what I no longer need to work on
- estimate how long a task will take so I can see how good I am at estimating
- estimate my progress while working on a task so I can see how long it will take to finish
- attach tasks to self-defined classes so I can sort my tasks by type
- see automatically made stats to see trends in my work

Everything is implemented.

## SQL-queries

Most queries the app uses are automated using SQLAlchemy. Here I've written some examples to demonstrate what it does.

### Inserting
Example of creating a new account. SQLAlchemy automatically calculates adds in the id, date_created and date_modified values.
```sql
INSERT INTO account (id, date_created, date_modified, name, username, password)
VALUES ([ID], CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, "Helena", "helluuu", "koira1")
```

### Querying

Example of fetching all of the user's tasks for listing of tasks.
```sql
SELECT *
FROM task
WHERE task.account_id = [USERID]
ORDER BY task.progress ASC, task.name COLLATE NOCASE ASC
```

### Stats
The most complicated queries, used for stats, found in application/stats/models.py. These are the only queries actually hardcoded into the app.

Get total minutes worked for one account:
```sql
SELECT SUM(working_period.length)
FROM working_period
INNER JOIN task ON working_period.task_id = task.id
INNER JOIN account ON task.account_id = account.id
WHERE account.id = [USERID]
```
Get the date and length of each work session for one account:
```sql
SELECT working_period.time, working_period.length
FROM working_period
INNER JOIN task ON working_period.task_id = task.id
INNER JOIN account ON task.account_id = account.id
WHERE account.id = [USERID]
```
Get the class with most minutes worked for one account:
```sql
SELECT class.name AS name, SUM(working_period.length) AS minutes
FROM class
INNER JOIN classtask ON classtask.class_id = class.id
INNER JOIN task ON task.id = classtask.task_id
INNER JOIN account ON account.id = task.account_id
INNER JOIN working_period ON working_period.task_id = task.id
WHERE account.id = [USERID]
GROUP BY name
ORDER BY minutes DESC
LIMIT 1
```
