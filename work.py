import json
from _datetime import datetime
from time import sleep

import file_manager


class Work:
    def __init__(self, work_name, work_datetime, category, importance=True, urgency=True, location=None,
                 link=None, description=None, status=None, notification=None):
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

    def postpone(self, username, postpone_time):
        """
        this method changes the time of work.

        :param username: user who logged in reminder
        :param postpone_time:
        :return:
        """
        old_time = self.work_datetime
        self.work_datetime = postpone_time
        with open('all_users_works.json', 'r') as edit:
            all_works = json.load(edit)
            all_works[username][self.work_name]['work_datetime'] = f"{self.work_datetime.month}-" \
                                                                   f"{self.work_datetime.day}-" \
                                                                   f"{self.work_datetime.year} " \
                                                                   f"{self.work_datetime.time()}"
        with open('all_users_works.json', 'w') as write_file:
            json.dump(all_works, write_file, ensure_ascii=False)

        return f'{self.work_name} has been postponed from {old_time} to {self.work_datetime}'

    def change_status(self, username, status):
        """
        change status of work. done or in progress
        :return: a massage if changes are done and saved.
        """
        self.status = status
        with open('all_users_works.json', 'r') as edit:
            all_works = json.load(edit)
            all_works[username][self.work_name]['status'] = self.status

        with open('all_users_works.json', 'w') as write_file:
            json.dump(all_works, write_file, ensure_ascii=False)

        return f'status of {self.work_name} changed to {self.status}'

    def __str__(self):
        return 'work_name: {}  work_datetime: {}  importance: {}  urgency: {}' \
               '  status: {}  location {}  link: {}  description {}'.format(
            self.work_name, self.work_datetime, self.importance, self.urgency,
            self.status, self.location, self.link, self.description)

    @classmethod
    def create_work(cls, username):
        """
        this method makes instances from Work
        :return: an instance of Work class
        """

        work_name = input('title of work:')
        work_datetime = input('Enter date and time as :(year-month-day hour:min:sec): ')
        importance = input('is this work important? 1. Yes  2. No  ')
        importance = True if importance == '1' else False
        urgency = input('is this work urgent? 1. Yes  2. No  ')
        urgency = True if urgency == '1' else False
        category = input('choose a category for your work: ')
        location = input('location of work (optional): ')
        link = input('add a link related to your work (optional): ')
        description = input('enter a description for your work (optional): ')

        work_dict = {
            'work_name': work_name,
            'work_datetime': work_datetime,
            'category': category,
            'importance': importance,
            'urgency': urgency,
            'location': location,
            'link': link,
            'description': description,
        }
        file_manager.write_to_file('all_users_works.json', work_dict, username, work_dict['work_name'])

        return cls(*list(work_dict.values()))
