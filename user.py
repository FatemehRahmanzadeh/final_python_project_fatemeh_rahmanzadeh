from hashlib import md5
import json
import work
from os import path
import pprint


class User:
    def __init__(self, user_email, name, last_name, username, password):
        """

        :param user_email: an unique email address for each user
        :param name: first name of user
        :param last_name: last name of user
        :param username: a freewill name chosen by user
        :param password: a safe password chosen by user
        """
        self.user_email = user_email
        self.name = name
        self.last_name = last_name
        self.username = username
        self.__password = password
        self.fullname = name + last_name
        self.works = []
        self.categories = {}
        self.accept = False
        self.events = {}

    def new_work(self):
        """
        this method is going to make an instance from Work object
        :return: instance of Work
        """
        new_work = work.Work.create_work(self.username)
        self.works.append(new_work)
        return f'{new_work.work_name} added to your work list successfully.'

    def categorize_works(self):
        """
        this method takes works from self.works attribute and categorise them
         based on self.category attribute of work
        :return: a massage about categorise succeed or failed
        """
        for task in self.works:
            if task.category not in self.categories.keys():
                self.categories[task.category] = [task]
            else:
                self.categories[task.category].append(task)

        return self.categories

    def delete_work(self, work_name):
        """
        this method remove a work from work list of user and from akk_users_works.jason
        :param work_name: name of work which user is going to delete
        :return: a massage about successful delete of fail.
        """

        for w in self.works:
            if w.work_name == work_name:
                self.works.remove(w)
                with open('all_users_works.json', 'r') as all_works:
                    work_dict = json.load(all_works)
                    user_works = work_dict[self.username]
                    user_works.pop(w.work_name)

                with open('all_users_works.json', 'w') as all_works:
                    json.dump(work_dict, all_works, ensure_ascii=False)
                return self.works

    def share_work(self, work_name):
        """
        this method is for send a work
        :param work_name: work that is going to be sent or receive
        :return: a work and a True flag for sending or an error if work does not exist in user work list
        """
        work_names = [w.work_name for w in self.works]
        if work_name in work_names:
            for w in self.works:
                if w.work_name == work_name:
                    return w
        else:
            return f'no such file exist in {self.name} work list'

    def accept_a_work(self, accept, received_work):
        """
        this method accepts a work from a user and adds it to user's work list
        :return: a massage if accepted or rejected based on accept attribute
        """
        # if accept:
        #     self.accept = True
        #     self.works[received_work.work_name] = received_work
        #     with open('users_data.json', 'r+') as add_new_work:
        #         all_works = json.load(add_new_work)[self.username]['works']
        #     all_works[received_work.work_name] = received_work

        return 'work_name from sender username accepted or rejected '

    def show_works(self):
        """
        this method prints json file of works pretty
        :return:
        """
        with open('all_users_works.json', 'r') as user_works:
            works = json.load(user_works)[self.username]
            print('*'*30, f'list of {self.username} works: ', '*'*30)
            pprint.pprint(works)

    def __str__(self):
        return f'name: {self.name}\n last name: {self.last_name}\nusername: {self.username}\n' \
               f'Email: {self.user_email}\n list of works: {self.works}'

    @classmethod
    def register(cls, user_data):
        """
        this method takes information of a User class and makes an instance from it
        :return: an instance of User class or an error about wrong inputs
        """

        file_exist = path.isfile('users_data.json')

        new_user_data = {'email': user_data[0],
                         'name': user_data[1],
                         'last_name': user_data[2],
                         'username': user_data[3],
                         'password': user_data[4]}
        password = str(new_user_data['password']).encode()
        hashed_password = md5(password).hexdigest()
        new_user_data['password'] = hashed_password
        new_user = cls(*(new_user_data.values()))

        if file_exist:
            with open('users_data.json', 'r') as exist_file:
                all_users_data = json.load(exist_file)
                if user_data[3] in all_users_data.keys():
                    print(f'{user_data[3]} already exists')

                else:
                    all_users_data[new_user.username] = new_user_data

                    with open('users_data.json', 'w') as new_file:
                        json.dump(all_users_data, new_file, ensure_ascii=False)
        else:
            all_users_data = {new_user.username: new_user_data}
            with open('users_data.json', 'w') as new_file:
                json.dump(all_users_data, new_file, ensure_ascii=False)
        return new_user

    @classmethod
    def login(cls, username, password):
        """
        this method takes two argument and checks if there is a match user with this information
        :param username: unchecked username
        :param password: unchecked password
        :return: True if username and password are match, or False otherwise
        """

        with open('users_data.json', 'r') as user_data, open('all_users_works.json', 'r') as wrks:
            data = json.load(user_data)
            works = json.load(wrks)

            user_has_work = True if username in works.keys() else False
            my_works = works[username] if user_has_work else {}

            password = str(password).encode()
            hash_password = md5(password).hexdigest()

            if username in data.keys():
                if hash_password == data[username]['password']:
                    current_user = User(*(data[username].values()))
                    if user_has_work:
                        for _ in my_works.values():
                            wrk_obj = work.Work(*(_.values()))
                            current_user.works.append(wrk_obj)

                    print(f'welcome {current_user.name}. your log in was successful.')
                    return current_user
                else:
                    print('password is wrong...')
                    return False
            else:
                print(f'No user named {username}...')
                return False
