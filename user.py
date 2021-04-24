from hashlib import md5
import json

import work
from os import path


class User:
    def __init__(self, user_email, name, last_name, username, password, works=None):
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
        self.works = works
        self.aceept = False

    def new_work(self):
        """
        this method is going to make an instance from Work object
        :return: instance of Work
        """
        new_work = work.Work.create_work(self.username)
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
                    print(f'welcome {current_user.name}')
                    return current_user
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            return False


def user_menu(user):
    """
    this function runs when user log in successfully. methods
     of User class recall based on act variable as input.
    :param user: an instance from User class
    :return: output parameters of recalled method.
    """

    print(f'hello {user.name}')
    act = 0
    while act != 6:

        print('you are in main menu. what can I do for you?')
        print('\n 1. add a new work'
              '\n 2. show works list'
              '\n 3. go to work directory'
              '\n 4. share a work with a friend'
              '\n 5. accept or reject a work'
              '\n 6. log out')
        try:
            act = int(input('please choose a task from menu above:'))
            if act < 0 or act > 6:
                raise ValueError
        except ValueError:
            print('invalid input. Just 1-5 are allowed')
        if act == 1:
            print(user.new_work())
        elif act == 2:
            print(user.works)
        elif act == 3:
            if not user.works:
                print('no work defined yet')
            else:
                works_names = list(user.works.keys())
                for i, key in enumerate(works_names):
                    print(i+1, '. ', key)

                try:
                    select_work = int(input('enter the work number:'))
                    if 1 <= select_work <= len(works_names):
                        selected_work_name = works_names[select_work-1]          # execute work name from works of user
                        selected = work.Work(*(user.works[selected_work_name]))  # make work object to recall methods
                        work.work_menu(selected)
                    else:
                        raise ValueError
                except ValueError:
                    print(f'please enter a 1 <= number <= {len(user.works)}')

        elif act == 4:
            print(user.share_work())
        elif act == 5:
            print(user.accept_a_work())
        else:
            break


if __name__ == '__main__':
    test = User.register(['sareh@email.com', 'sareh', 'rahmanzadeh', 'srh', 'pass3'])
    login_tst = User.login('ftm', 'pass1')
