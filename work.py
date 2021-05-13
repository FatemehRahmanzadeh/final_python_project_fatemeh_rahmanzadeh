from datetime import datetime, timedelta as tdelta
from colorama import Fore


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
        self.work_datetime = datetime.strptime(work_datetime, "%Y-%m-%d %H:%M:%S")
        self.category = category
        self.importance = importance
        self.urgency = urgency
        self.location = location
        self.link = link
        self.description = description
        self.status = status
        self.notification = notification

    def eisenhower_priority(self):
        """
        this method shows a notification based on importance attribute of work
            :return: a notification
        """

        if self.importance and self.urgency:
            return 1
        elif not self.importance and self.urgency:
            return 2
        elif self.importance and not self.urgency:
            return 3
        elif not self.importance and not self.urgency:
            return 4

    def notify(self):
        """
        this method shows notification based on self.priority of work
        :return:
        """

        priority = self.eisenhower_priority()

    def edit_work(self, new_values):
        """
        user can edit attributes of work using this method
        :return: a massage if editing is successful or not
        """

        for attr, new_val in new_values.items():
            self.__dict__[attr] = new_val
        return self.__dict__

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

    def __str__(self):
        return 'work_name: {}  work_datetime: {}  importance: {}  urgency: {}   status: {}  location {}' \
               '  link: {}  description {}'.format(self.work_name, self.work_datetime, self.importance, self.urgency,
                                                   self.status, self.location, self.link, self.description)

    @classmethod
    def create_work(cls, work_dict):
        """
        this method makes instances from Work
        :param work_dict: attributes of work instans
        :return: an instance of Work class
        """
        return cls(*(work_dict.values()))
