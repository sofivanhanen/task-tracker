# Task tracker

Web-based database app.
[App live on Heroku.](https://calm-plateau-92780.herokuapp.com/)
Done for the course TSOHAk2018.

## Features

User can log in to her account and add tasks that she needs to finish. After working on a task, she can log a new working period.
App displays trends in working times, efficiency, how long it takes to complete vs. how long it was estimated to take, etc.

## Directions for use

Go to the [site](https://calm-plateau-92780.herokuapp.com/) or clone the repo and start the app locally in a virtual environment with the command:
```bash
python3 run.py
```
Create an account by registering and then log in.
You have access only to data relevant to your account.

Add and edit tasks by selecting Tasks from the top bar, same for classes via the link Classes.
Delete tasks and classes by selecting the item from the list.
Add work sessions by clicking Add a work session in the top bar.
Delete work sessions by selecting the relevant task, and clicking Delete next to the relevant work session.
Click on Stats to see stats based on your work, but you'll have to have added tasks and work sessions to see any stats.
Remember to logout after you're done.

## Constraints

You only have access to data you've added for your own account. There is no way to view any other user's tasks, classes, work sessions, stats, or even if there are other users.

## Missing Features

Usability could be improved by adding a date picker.
Currently there is no way to modify selected classes for a task.
There's always room for more stats.
It would also be interesting to see stats on other users.

## Documentation

[User stories and SQL-queries](https://github.com/sofivanhanen/task-tracker/blob/master/documentation/User%20stories.md)

[Architecture - database diagram and database schema](https://github.com/sofivanhanen/task-tracker/blob/master/documentation/Architecture.md)
