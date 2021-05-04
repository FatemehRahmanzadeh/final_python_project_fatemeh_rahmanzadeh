import json
class Work:
    def __init__(self, work_name, date, time, category, importance=True, urgency=True, location=None,
                 link=None, description=None):
        """
        this class models the works that user adds to directory.all the lines in instance methods
        are sample and invalid. some attributes and method maybe add or remove in next phase of project.
        :param work_name: name of work in works list
        :param date: date of reminding work
        :param time: time of reminding work
        :param importance:work is important. True or False
        :param urgency: work is urgent. True or False
        :param location: place that work is going to be done.
        :param link: if work has a link
        :param description: some description about work
        """

        self.work_name = work_name
        self.date = date
        self.time = time
        self.category = category
        self.importance = importance
        self.urgency = urgency
        self.location = location
        self.link = link
        self.description = description
        self.reminder_massage = f'time to do {self.work_name}'
        self.status = 'in progress'

    def notification(self):
        """
        this method shows a notification based on importance attribute of work
            :return: a notification
        """

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

    def postpone(self, postpone_time):
        """
        this method changes the time of work.
        :param postpone_time:
        :return:
        """

        return 'you can edit time of your work'

    def change_status(self, status):
        """
        change status of work. done or in progress
        :return: a massage if changes are done and saved.
        """
        self.status = status
        return f'status of {self.work_name} changed to {self.status}'

    def __str__(self):
        return f'work id: {self.work_name}\n date: {self.date}\n' \
               f'time: {self.time}\n importance: {self.importance}\n' \
               f'location: {self.location}\n link: {self.link}\n description: {self.description}'

    @classmethod
    def create_work(cls, username):
        """
        this method makes instances from Work
        :return: an instance of Work class
        """

        work_name = input('title of work:')
        date = input('enter date of work(Y/M/D):')
        time = input('enter time of work (h:min):')
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
            'date': date,
            'time': time,
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
