import json

import user
from datetime import datetime


def login():
    """
    this method takes username and and password from user and pass them to login method of user.
    it also manage number of times user enters password wrong
    :return:
    """
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
    user_data = []
    try:
        user_data.append(input('email: '))
        user_data.append(input('your name: '))
        user_data.append(input('your last name: '))
        user_data.append(input('define an username: '))
        user_data.append(input('enter a secure password: '))
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
    act = 0
    while act != 7:

        print('you are in main menu. what can I do for you?')
        print('\n 1. add a new work'
              '\n 2. show works list'
              '\n 3. go to work directory'
              '\n 4. share a work with a friend'
              '\n 5. accept or reject a work'
              '\n 6. categorize your works'
              '\n 7. log out')
        try:
            act = int(input('please choose a task from menu above:'))
            if act < 0 or act > 7:
                raise ValueError
        except ValueError:
            print('invalid input. Just 1-7 are allowed')
        if act == 1:
            print(usr.new_work())
        elif act == 2:
            usr.show_works()
        elif act == 3:
            if not usr.works:
                print('no work defined yet')
            else:
                for i, obj in enumerate(usr.works):
                    print(i + 1, ".", obj.work_name)

                try:
                    select_work = int(input('enter the work number:'))
                    if 1 <= select_work <= len(usr.works):
                        selected = usr.works[select_work - 1]
                        work_menu(usr, selected)
                    else:
                        raise ValueError
                except ValueError:
                    print(f'please enter a 1 <= number <= {len(usr.works)}')

        elif act == 4:
            share(usr)
        elif act == 5:
            print(usr.accept_a_work())
        elif act == 6:
            work_categories_menu(usr)
        else:
            break


def work_menu(logged_in_user, wrk):
    """
    this function runs if user selects a work. methods
     of work class recall based on action variable as input.
     :param logged_in_user: user who logged in to reminder
    :param wrk: chosen work instance by user
    :return: output parameters of recalled method (for now just a string that describes methods).
    """

    action = 0
    while action != 5:

        print(f'{logged_in_user.username} > {wrk.work_name} option menu:')

        print(f'\n1. edit {wrk.work_name}'
              f'\n2. postpone {wrk.work_name} to another time'
              f'\n3. change status of {wrk.work_name}. (in progress or done)'
              f'\n4. delete {wrk.work_name}'
              f'\n5. back to previous page')

        while ValueError:
            try:
                action = int(input('please select an option from list above:'))
                if action < 0 or action > 5:
                    raise ValueError
                else:
                    break
            except ValueError:
                print('invalid input. Just 1-4 are allowed...')
        if action == 1:
            edit_work_menu(logged_in_user.username, wrk)
        elif action == 2:
            postpone = datetime.strptime(input('enter New date and time as ((01-31-2020 14:45:37)): '),
                                         "%m-%d-%Y %H:%M:%S")
            print(wrk.postpone(logged_in_user.username, postpone))
        elif action == 3:
            status = input(f'current status: {wrk.status}. please enter new status: ')
            print(wrk.change_status(logged_in_user.username, status))
        elif action == 4:
            print(logged_in_user.delete_work(wrk.work_name))
            logged_in_user.categorize_works()
            break
        else:
            break


def edit_work_menu(username, wrk):
    """
    this menu let users edit attributes of their works
    :param username: user logged in to reminder
    :param wrk: selected work object to edit
    :return: an edited work object
    """
    format_string = {'datetime': "%m-%d-%Y %H:%M:%S", 'date': "%m-%d-%Y", 'time': "%H:%M:%S"}
    attributes_dict = {}
    print(f'{username} > {wrk.work_name} > edit {wrk.work_name}')
    attribute_lst = list(wrk.__dict__.keys())

    for i in range(1, len(attribute_lst) + 1):
        attributes_dict[i] = attribute_lst[i - 1]
        print(f'{i}. {attribute_lst[i - 1]} of {wrk.work_name}')

    new_values = []
    items = list(map(lambda x: int(x), input('id of items fo editing:(split items with comma)').split(',')))

    edit_items = [attributes_dict[num] for num in items]

    for i, itm in enumerate(edit_items):
        new_val = input(f'new values of {itm}')

        if type(new_val) == "<class 'datetime.datetime'>":
            new_val = datetime.strptime(new_val, format_string[itm])
            new_values.append(new_val)

        elif new_val.isdigit():
            new_val = int(new_val)
            new_values.append(new_val)
        else:
            new_values.append(new_val)
    print(wrk.edit_work(username, new_values, edit_items))
    return wrk


def work_categories_menu(logged_in_user):
    """
    this menu shows works of user in organized categories
    :param logged_in_user: current user who logged in
    :return: a massage of successful categorising or an error if something goes wrong
    """
    all_categories = logged_in_user.categorize_works()

    while True:
        print('\n', '-.' * 30, 'list of categories:', '-.' * 30)

        cat_select_dict = {_ + 1: cat for _, cat in enumerate(all_categories.keys())}
        cat_select_dict[0] = 'back to main menu'

        for num, cat in cat_select_dict.items():
            print(num, '.', cat)

        select_cat = int(input('enter a category number from list above: '))
        if select_cat != 0:
            selected_cat = cat_select_dict[select_cat]
            work_dict = {i + 1: w for i, w in enumerate(all_categories[selected_cat])}
            work_dict[0] = 'back to categories'
            while True:
                print('\n', '×' * 30, f'list of works in {selected_cat}:', '×' * 30)

                for num, work in work_dict.items():
                    if num != 0:
                        print(num, '.', work.work_name)
                    else:
                        print(num, '.', work)

                select_work = int(input('choose a work to enter work menu: '))
                if select_work != 0:
                    work_menu(logged_in_user, work_dict[select_work])
                else:
                    break
        else:
            break


def share(sender_user):
    """
    this function moves work from sender_user to receiver_user if receiver accepts it
    :param sender_user:
    :return:
    """
    while True:
        select_work_dict = {i+1: w for i, w in enumerate(sender_user.works)}
        select_work_dict[0] = "back"

        print('**************** list of works *****************')
        for i, w in select_work_dict.items():
            if i > 0:
                print(i, ".", w.work_name)
            else:
                print(i, '.', w)

        select = int(input("enter a work number from list above:"))

        if select > 0:
            target_work = select_work_dict[select]

            receiver_user_username = input("please enter receiver's username: ")

            with open('all_users_works.json') as user_data:
                receiver_user = user.User(json.load(user_data)[receiver_user_username])
            receiver_user.events['receive'] = {'user': sender_user.username, 'work': target_work}

            with open('users_events.json' 'r+') as event_file:
                events = json.load(event_file)
                events[receiver_user]['events'].append(receiver_user.events)
                json.dump(events, event_file, ensure_ascii=False)

            if receiver_user.accept:
                receiver_user.works.append(target_work)

                target_work_dict = {'work_name': target_work.work_name,
                                    'date and time': target_work.work_datetime,
                                    'importance': target_work.importance,
                                    'urgency': target_work.urgency,
                                    'category': target_work.category,
                                    'location': target_work.location,
                                    'link': target_work.link,
                                    'description': target_work.description,
                                    }

                with open('all_users_works.json', 'r') as edit:
                    all_works = json.load(edit)
                all_works[receiver_user.username].update({target_work.work_name: target_work_dict})

                with open('all_users_works.json', 'w') as write_file:
                    json.dump(all_works, write_file, ensure_ascii=False)

            else:
                break
