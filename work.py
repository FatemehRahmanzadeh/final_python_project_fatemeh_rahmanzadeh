import json
class Work:
    def __init__(self, work_name, date, time, importance, location=None, link=None, description=None):
        """
        this class models the works that user adds to directory.all the lines in instance methods
        are sample and invalid. some attributes and method maybe add or remove in next phase of project.
        :param work_name: name of work in works list
        :param date: date of reminding work
        :param time: time of reminding work
        :param importance: level of urgent or importance of work. user can set it by numbers 1-4
        :param location:
        :param link:
        :param description: some description about work
        """

        self.work_name = work_name
        self.date = date
        self.time = time
        self.importance = importance
        self.location = location
        self.link = link
        self.description = description
        self.reminder_massage = f'time to do {self.work_name}'
        self.status = 'in progress'

    def categorize(self, importance=None):
        """
        assign a number to each work based on its priority and will save it in Corresponding csv or json file
        :param importance: sets the urgent_importance level for work (1-4)
        :return: category of work
        """
        importance_urgent = {1: 'important_urgent',
                             2: 'important_not_urgent',
                             3: 'not_important_urgent',
                             4: 'not_important_not_urgent'}

        return 'there are four categories for work based on Eisenhower matrix'

    def notification(self):
        """
        this method shows a notification based on importance attribute of work
            :return: a notification
        """
        return self.reminder_massage

    def edit_work(self, username, new_values, attributes):
        """
        user can edit attributes of work using this method
        :return: a massage if editing is successful or not
        """
        out_str = f'following items changed for {self.work_name}:'
        with open('users_data.json', 'r') as data:
            all_data = json.load(data)
            work_dict = all_data[username]['works']
            current_work = work_dict[self.work_name]

        for attr, new_val in zip(attributes, new_values):
            if 'work_name' in attributes:
                idx = attributes.index('work_name')
                work_dict[new_values[idx]] = current_work
                current_work = work_dict[new_values[idx]]
                work_dict.pop(self.work_name)

            self.__dict__[attr] = new_val
            current_work[attr] = new_val
            out_str += f'\n{attr} >>> {new_val}'

        with open('users_data.json', 'w') as data:
            json.dump(all_data, data, ensure_ascii=False)
        return out_str

    def postpone(self, postpone_time=None):
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

        print('please enter work attributes same as sample. location,link and description are optional')
        list_of_attributes = input('work_name,date,time,importance,location,link,description:').split(',')

        work_dict = {
            'work_name': list_of_attributes[0],
            'date': list_of_attributes[1],
            'time': list_of_attributes[2],
            'importance': list_of_attributes[3],
            'location': list_of_attributes[4],
            'link': list_of_attributes[5],
            'description': list_of_attributes[6],
        }
        works = {work_dict['work_name']: work_dict}
        with open('users_data.json', 'r') as all_data_file:
            user_data = json.load(all_data_file)
            if 'works' not in user_data[username].keys():
                user_data[username]['works'] = works
            else:
                user_data[username]['works'].update(works)

        with open('users_data.json', 'w') as all_data_file:
            json.dump(user_data, all_data_file)

        return cls(*list_of_attributes)
