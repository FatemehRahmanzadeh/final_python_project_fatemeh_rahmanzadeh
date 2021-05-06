import json
from _datetime import datetime
from win10toast import ToastNotifier
from time import sleep


class Work:
    def __init__(self, work_name, work_datetime, category, importance=True, urgency=True, location=None,
                 link=None, status=None, description=None):
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
        self.work_datetime = datetime.strptime(work_datetime, "%m-%d-%Y %H:%M:%S")
        self.category = category
        self.importance = importance
        self.urgency = urgency
        self.location = location
        self.link = link
        self.description = description
        self.status = status
        self.priority = 0
        self.notification = f"time to do {self.work_name}"

    def eisenhower_priority(self):
        """
        this method shows a notification based on importance attribute of work
            :return: a notification
        """

        if self.importance and self.urgency:
            self.priority = 1
        elif not self.importance and self.urgency:
            self.priority = 2
        elif self.importance and not self.urgency:
            self.priority = 3
        elif not self.importance and not self.urgency:
            self.priority = 4

    def notify(self):
        """
        this method shows notification based on self.priority of work
        :return:
        """
        toast = ToastNotifier()
        if self.work_datetime <= datetime.now():
            while True:
                if self.priority == 1:
                    sleep(5)
                    toast.show_toast("Reminder ;)", f"{self.notification}", duration=10)
                elif self.priority == 2:
                    toast.show_toast("Reminder ;)", f"{self.notification}", duration=20)
                elif self.priority == 3:
                    sleep(86400)
                    toast.show_toast("Reminder ;)", f"{self.notification}", duration=20)
                elif self.priority == 4:
                    sleep(604800)
                    toast.show_toast("Reminder ;)", f"{self.notification}", duration=20)

    def edit_work(self, username, new_values, attributes):
        """
        user can edit attributes of work using this method
        :return: a massage if editing is successful or not
        """
        out_str = ''
        with open('all_users_works.json', 'r') as data:
            work_dict = json.load(data)
            current_work = work_dict[username][self.work_name]

            if 'work_name' in attributes:
                idx = attributes.index('work_name')
                work_dict[username][new_values[idx]] = current_work
                current_work = work_dict[username][new_values[idx]]
                work_dict[username].pop(self.work_name)

        old_values = {_: self.__dict__[_] for _ in attributes}

        for attr, new_val in zip(attributes, new_values):
            self.__dict__[attr] = new_val
            current_work[attr] = new_val

            out_str += f'\n{attr}: {old_values[attr]} > changed to > {new_val}'

        with open('all_users_works.json', 'w') as data:
            json.dump(work_dict, data, ensure_ascii=False)
        return out_str

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
        return f'work id: {self.work_name}\n date: {self.work_datetime}\n' \
               f'importance: {self.importance}\n' \
               f'location: {self.location}\n link: {self.link}\n description: {self.description}'

    @classmethod
    def create_work(cls, username):
        """
        this method makes instances from Work
        :return: an instance of Work class
        """
        format_string = "%m-%d-%Y %H:%M:%S"

        work_name = input('title of work:')
        datetime_in = input('Enter date and time as :(01-31-2020 14:45:37): ')
        work_datetime = datetime.strptime(datetime_in, format_string)
        importance = input('is tis work important? 1. Yes  2. No  ')
        importance = True if importance == '1' else False
        urgency = input('is your work urgent? 1. Yes  2. No  ')
        urgency = True if urgency == '1' else False
        category = input('choose a category for your work: ')
        location = input('location of work (optional): ')
        link = input('add a link related to your work (optional): ')
        description = input('enter a description for your work (optional): ')

        work_dict = {
            'work_name': work_name,
            'date and time': f"{work_datetime.month}-"
                             f"{work_datetime.day}-"
                             f"{work_datetime.year} "
                             f"{work_datetime.time()}",
            'importance': importance,
            'urgency': urgency,
            'category': category,
            'location': location,
            'link': link,
            'description': description,
        }

        with open('all_users_works.json', 'r') as all_users_work:
            user_work = json.load(all_users_work)
            if username not in user_work.keys():
                user_work.update({username: {work_name: work_dict}})
            else:
                user_work[username].update({work_name: work_dict})

        with open('all_users_works.json', 'w') as all_users_work:
            json.dump(user_work, all_users_work)

        return cls(*list(work_dict.values()))
