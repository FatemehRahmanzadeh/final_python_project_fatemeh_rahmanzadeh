import user
import work
import json


def login():
    tries = 0
    while tries < 3:

        username = input('please enter your username:')
        password = input('please enter your password:')
        current_user = user.User.login(username, password)
        if not current_user:
            tries += 1
            print(f'username or password is wrong. you have {3 - tries} tries')
        else:
            user_menu(current_user)
            break
        if tries >= 3:
            print('your account is locked for 20 minutes. try later')


def creat_account():
    try:
        user_data = input('enter requirement like: email, name, last_name, username, password').split(',')
        confirm_password = input('please enter your password again:')
        assert confirm_password == user_data[4]
        new_user = user.User.register(user_data)
        check = int(input('would you like to log in? 1. yes   2. no '))
        if check == 1:
            login()
            return new_user
        elif check == 2:
            print('Thanks for registration, see you later')
            return new_user
        else:
            raise ValueError
    except ValueError:
        print('invalid input.. please enter a number 1-2')

    except AssertionError:
        print('password does not match to confirmation please try again')
        return 0


def user_menu(usr):
    """
    this function runs when user log in successfully. methods
     of User class recall based on act variable as input.
    :param usr: an instance from User class
    :return: output parameters of recalled method.
    """

    print(f'hello {usr.name}')
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
            print(usr.new_work())
        elif act == 2:
            print(usr.works)
        elif act == 3:
            if not usr.works:
                print('no work defined yet')
            else:
                with open('users_data.json', 'r') as works_data:
                    works_from_file = json.load(works_data)[usr.username]['works']
                works_names = list(works_from_file.keys())
                for i, key in enumerate(works_names):
                    print(i + 1, '. ', key)

                try:
                    select_work = int(input('enter the work number:'))
                    if 1 <= select_work <= len(works_names):
                        selected_work_name = works_names[select_work - 1]  # execute work name from works of user
                        selected = work.Work(*(works_from_file[selected_work_name]))  # make work object
                        work_menu(selected)
                    else:
                        raise ValueError
                except ValueError:
                    print(f'please enter a 1 <= number <= {len(usr.works)}')

        elif act == 4:
            print(usr.share_work())
        elif act == 5:
            print(usr.accept_a_work())
        else:
            break


def work_menu(wrk):
    """
    this function runs if user selects a work. methods
     of work class recall based on action variable as input.
    :param wrk: chosen work instance by user
    :return: output parameters of recalled method (for now just a string that describes methods).
    """
    print(f'this is {wrk.work_name} option menu:')

    print(f'\n1. edit {wrk.work_name}'
          f'\n2. postpone {wrk.work_name} to another time'
          f'\n3. change status of {wrk.work_name}. (in progress or done)'
          f'\n4. categorize {wrk.work_name}'
          f'\n5. back to the main menu')

    action = 0
    while action != 5:
        while ValueError:
            try:
                action = int(input('please select an option from list above:'))
                if action < 0 or action > 5:
                    raise ValueError
                else:
                    break
            except ValueError:
                print('invalid input. Just 1-5 are allowed...')
        if action == 1:
            print(wrk.edit_work())
        elif action == 2:
            print(wrk.postpone())
        elif action == 3:
            print(wrk.change_status())
        elif action == 4:
            print(wrk.categorize())
        else:
            break


if __name__ == '__main__':
    login()
    print(creat_account())
