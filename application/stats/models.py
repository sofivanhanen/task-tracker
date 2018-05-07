from application import db, current_user
from application.tasks.models import Task
from application.workingperiods.models import WorkingPeriod
from application.classes.models import Class
from datetime import *
from sqlalchemy.sql import text


class Stats():

    @staticmethod
    def get_total_worked_minutes_string():

        stmt = text(
            "SELECT SUM(working_period.length) FROM working_period INNER JOIN task ON working_period.task_id = task.id INNER JOIN account ON task.account_id = account.id WHERE account.id = " + str(current_user.id))
        res = db.engine.execute(stmt)

        for row in res:
            # res contains only one row
            if str(row[0]) == None or row[0] == 0 or row[0] == None:
                return "You haven't logged any work sessions yet."
            return "You have worked a total of " + str(row[0]) + " minutes."

    @staticmethod
    def get_most_worked_day_of_week_string():

        stmt = text(
            "SELECT working_period.time, working_period.length FROM working_period INNER JOIN task ON working_period.task_id = task.id INNER JOIN account ON task.account_id = account.id WHERE account.id = " + str(current_user.id))
        res = db.engine.execute(stmt)

        return_string = ""
        # Save total minutes for each day in a list
        minutes = [0, 0, 0, 0, 0, 0, 0]

        for row in res:
            if type(row[0]) is str:
                # Because with SQLite returned object is a String, not DateTime
                return "Unfortunately the stats concerning dates can only be seen on the online version of the app."
            # Day of week is 0-7, starting from Monday. Add number of minutes to the sum of that day in the list
            minutes[row[0].weekday()] += row[1]

        return_string += "You have worked most on "

        # Get index of max value = the day on which most minutes have been worked
        # TODO Is there a smarter way to do this?
        day = minutes.index(max(minutes))
        if day is 0:
            return_string += "Mondays"
        if day is 1:
            return_string += "Tuesdays"
        if day is 2:
            return_string += "Wednesdays"
        if day is 3:
            return_string += "Thursdays"
        if day is 4:
            return_string += "Fridays"
        if day is 5:
            return_string += "Saturdays"
        if day is 6:
            return_string += "Sundays"

        return_string += ", a total of " + str(minutes[day]) + " minutes."

        if str(minutes[day]) == None or minutes[day] == 0:
            return "Add work sessions to see your favourite work day!"

        return return_string

    @staticmethod
    def get_most_worked_class_string():

        stmt = text("SELECT class.name AS name, SUM(working_period.length) AS minutes FROM class INNER JOIN classtask ON classtask.class_id = class.id INNER JOIN task ON task.id = classtask.task_id INNER JOIN account ON account.id = task.account_id INNER JOIN working_period ON working_period.task_id = task.id WHERE account.id = " +
                    str(current_user.id) + " GROUP BY class.name ORDER BY minutes DESC LIMIT 1")
        res = db.engine.execute(stmt)

        for row in res:
            # res contains only one row
            if row[1] == 0:
                break
            return "Your most used class is " + str(row[0]) + " with a total of " + str(row[1]) + " minutes worked."

        # if res was empty / no classes

        return "Add classes to see your most used class!"
