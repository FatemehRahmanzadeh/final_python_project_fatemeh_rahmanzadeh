import datetime
import time
from datetime import datetime as dt, timedelta as tdelta
from plyer import notification as ntftion


class Work:
    def __init__(self, work_name, work_datetime, category, status='in progress', importance=True, urgency=True,
                 location=None,
                 link=None, description=None, notification='time to do work'):
        """
        this class models the works that user adds to directory.all the lines in instance methods
        are sample and invalid. some attributes and method maybe add or remove in next phase of project.
        :param work_name: name of work in works list
        :param work_datetime: date and time of reminding work
        :param importance:work is important. True or False
        :param urgency: work is urgent. True or False
        :param location: place that work is going to be done.
        :param link: if work has a link
        :param description: some description about work
        """
        self.work_name = work_name
        self.work_datetime = dt.strptime(work_datetime, "%Y-%m-%d %H:%M:%S")
        self.category = category
        self.importance = importance
        self.urgency = urgency
        self.location = location
        self.link = link
        self.description = description
        self.status = status
        self.notification = notification

    def postpone(self, dlt_time, ky_word):
        """
        this function edits hour part of datetime object
        :param dlt_time: date-time object to edit
        :param dlt_time: delta-time of old and new time
        :param ky_word: represent type of dlt_time if
         it is hour, day, week or month
        """
        if ky_word == 'hour':
            self.work_datetime = self.work_datetime + tdelta(seconds=dlt_time * 3600)
        elif ky_word == 'day':
            self.work_datetime = self.work_datetime + tdelta(days=dlt_time)
        elif ky_word == 'week':
            self.work_datetime = self.work_datetime + tdelta(weeks=dlt_time)
        elif ky_word == 'month':
            self.work_datetime = self.work_datetime + tdelta(days=dlt_time * 30)
        return self.work_datetime

    def eisenhower_priority(self):
        """
        this method sets priority and time of notification based on importance attribute of work
        notification repeat:
        priority 1 -->  every 5 minutes during the day
        priority 2 --> just in time
        priority 3 --> at the end of the day (18:00:00)
        priority 4 --> at the end of the week (sunday)
            :return: a tuple of priority and notification time
        """
        if self.status != 'done':
            if self.importance and self.urgency:
                return 1, self.work_datetime
            elif not self.importance and self.urgency:
                return 2, self.work_datetime

            elif self.importance and not self.urgency:
                if self.work_datetime.hour < 18:
                    hours = (18 - self.work_datetime.hour)
                else:
                    hours = 0
                time_ntf = self.postpone(hours, 'hour')
                return 3, time_ntf

            elif not self.importance and not self.urgency:
                dys = (6 - self.work_datetime.weekday())
                time_ntf = self.postpone(dys, 'day')
                return 4, time_ntf
        else:
            return 0

    def notify(self):
        """
        this method shows notification based on self.priority of work
        :return:
        """

        def remind():
            """
            this function shows a pop-up using windows notification
            """
            ntftion.notify('reminder', f"{self.notification}:"
                                       f"\n{self.work_name}"
                                       f"\n{self.work_datetime.time()} ", app_icon='reminder.ico', timeout=10)
        if self.eisenhower_priority():
            priority, time_ntf = self.eisenhower_priority()

            while dt.now().day <= time_ntf.day:
                if priority == 1:
                    remind()
                    time.sleep(60*5)

                elif priority == 2 and dt.now().time() == self.work_datetime.time():
                    remind()
                    break
                elif priority == 3 and dt.now().time().hour == 18:
                    remind()
                    self.postpone(1, 'day')
                elif priority == 4 and dt.now().weekday() == 6:
                    remind()
                    self.postpone(1, 'week')
        else:
            pass

    def edit_work(self, new_values):
        """
        user can edit attributes of work using this method
        :return: a massage if editing is successful or not
        """

        for attr, new_val in new_values.items():
            self.__dict__[attr] = new_val
        return self.__dict__

    def change_status(self):
        """
        change status of work. done or in progress
        :return: a massage if changes are done and saved.
        """
        if self.status == 'in progress':
            self.status = 'done'
            return self.status
        elif self.status == 'done':
            self.status = 'in progress'
            return self.status

    def work_refresh(self):
        """
        this method updates datetime of undone works from last weeks
        """
        now = datetime.datetime.now()
        p_week = now.isocalendar()[1] - self.work_datetime.isocalendar()[1]
        if 1 <= p_week:
            self.work_datetime = now
        else:
            pass

    def __str__(self):
        return 'work_name: {}\nwork_datetime: {}\nimportance: {}\nurgency: {}\nstatus: {}\nlocation {}' \
               '  link: {}  description {}'.format(self.work_name, self.work_datetime, self.importance, self.urgency,
                                                   self.status, self.location, self.link, self.description)

    @classmethod
    def create_work(cls, work_dict):
        """
        this method makes instances from Work
        :param work_dict: attributes of work instance
        :return: an instance of Work class
        """
        return cls(*(work_dict.values()))


# w = Work('test',"2021-05-15 04:40:00", 'tests', importance=False)
# w.notify()
