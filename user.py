from hashlib import md5
import json
import work
from os import path


class User:
    def __init__(self, user_email, name, last_name, username, password,works = {}):
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
        self.works = work
        self.accept = False

    def new_work(self):
        """
        this method is going to make an instance from Work object
        :return: instance of Work
        """
        new_work = work.Work.create_work(self.username)
        self.works[new_work.work_name] = new_work
        return f'{new_work.work_name} added to your work list successfully.'

    def share_work(self, wrk=None, target_user=None):
        """
        this method is for send a work
        :param wrk: work that is going to be sent or receive
        :param target_user: user who is going to receive the work
        :return: a massage for sending or receiving or an error
        """
        return f'work_name has been sent to target_user'

    def accept_a_work(self):
        """
        this method accepts a work from a user and adds it to user's work list
        :return: a massage if accepted or rejected based on accept attribute
        """
        return 'work_name from sender username accepted or rejected '

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
        try:
            with open('users_data.json', 'r') as user_data:
                data = json.load(user_data)
                password = str(password).encode()
                hash_password = md5(password).hexdigest()
        except IOError:
            print('Error opening or loading file...')
        try:
            if username in data.keys():
                if hash_password == data[username]['password']:
                    current_user = User(*(data[username].values()))
                    print(f'welcome {current_user.name}. your registration was successful.')
                    return current_user
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            return False


if __name__ == '__main__':
    test = User.register(['sareh@email.com', 'sareh', 'rahmanzadeh', 'srh', 'pass3'])
    login_tst = User.login('ftm', 'pass1')
