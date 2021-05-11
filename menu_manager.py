import json
from colorama import Fore
import calandar
import user
from work import Work
from datetime import datetime
from os import path
import re
import file_manager
from tabulate import tabulate





def delete_work(logged_in_user, target_work):
    """
    this function deletes a work from user work list and from file
    :param logged_in_user: current user
    :param target_work: selected work object to delete
    :return:
    """
    user_works = logged_in_user.delete_work(target_work)
    user_works_file = file_manager.read_from_file('all_users_works.json', logged_in_user.username)

    user_works_file.pop(target_work.work_name)
    file_manager.write_to_file('all_users_works.json', user_works_file, logged_in_user.username)

    return f'{target_work.work_name} has been deleted successfully'


def share(sender_user, target_work):
    """
    this function moves work from sender_user to receiver_user if receiver accepts it
    :param sender_user:
    :return:
    """

    data_from_file = file_manager.read_from_file('all_users_works.json', sender_user.username)

    yes_or_no = int(input(f'\n{Fore.GREEN} do you know your friend username? 1. yes 2. no{Fore.RESET}'))

    if yes_or_no == 1:
        reciver = input(f'{Fore.BLUE} enter friend username:{Fore.RESET}')
    elif yes_or_no == 2:
        users_from_file = file_manager.read_from_file('users_data.json')
        users_from_file.pop(sender_user.username)
        all_usernames = {i + 1: username for i, username in enumerate(users_from_file.keys())}

        for num, username in all_usernames.items():
            print(f'{Fore.CYAN}{num}. {username}{Fore.RESET}')

        select = int(input(f'\n{Fore.MAGENTA} select a friend: '))
        reciver = all_usernames[select]
        reciver_usr = user.User(*(users_from_file[reciver].values()))
        reciver_usr.events[sender_user.username] = target_work

        file_manager.write_to_file('events.json', (target_work.__dict__),reciver, sender_user.username)

        return f'{Fore.WHITE}{target_work.work_name} has been sent to {reciver_usr.username}{Fore.RESET}'


def check_events(logged_in_user):
    """
    this function checkes event file of user just after log in.
     User should decide what to do with recieved work.
    :param logged_in_user: current user in reminder
    :return: a massage about user decision
    """
    all_events = file_manager.read_from_file('events.json')[logged_in_user.username]
    choice = None

    while choice != 0:
        if all_events == {}:
            print('no new event...')
            break
        sender_work = {sender:Work(*(w.values())) for sender, w in all_events.items()}
        work_select = {}
        choice = 0
        while choice !=3:
            i=1
            for sender, wrk in sender_work.items():
                work_select[i] = wrk
                print(f'{i}. {sender}: {wrk.work_name} ')
                i+=1
            choice = int(input(f'{Fore.YELLOW} select a work from list above or enter 3 to back: {Fore.RESET}'))

            selected_work = sender_work[choice]
            print(selected_work)

            act = int(input(f'what are you going to do?'f'\n'
                                f'1. accept the work and add it to work list\n2. reject it: '))
            if act == 2:
                work_select.pop(choice)
                continue
            elif act == 1:
                logged_in_user.accept_a_work(selected_work)
                file_manager.write_to_file('all_users_works.json', selected_work.__dict__,
                                                 logged_in_user.username, selected_work.work_name)
                work_select.pop(choice)
        all_events.clear()
        file_manager.write_to_file('events.json', {}, logged_in_user.username)


def user_menu(usr):
    """
    this function runs when user log in successfully. methods
     of User class recall based on act variable as input.
    :param usr: an instance from User class
    :return: output parameters of recalled method.
    """
    act = 0
    while act != 8:

        print('\n', Fore.LIGHTMAGENTA_EX, f'{usr.username} > main menu. what can I do for you?', Fore.RESET)
        print(Fore.CYAN, '\n 1. add a new work'
                         '\n 2. show works list'
                         '\n 3. go to work directory'
                         '\n 4. check events'
                         '\n 5. accept or reject a work'
                         '\n 6. categorize your works'
                         '\n 7. go to calendar'
                         '\n 8. log out', Fore.RESET)
        try:
            act = int(input(f'{Fore.GREEN}\nplease choose a task from menu above:{Fore.RESET}'))
            if act < 0 or act > 8:
                raise ValueError
        except ValueError:
            print(Fore.RED, 'invalid input. Just 1-8 are allowed', Fore.RESET)
        if act == 1:
            print(usr.new_work())
        elif act == 2:
            print(usr.show_works())
        elif act == 3:
            if not usr.works:
                print('no work defined yet')
            else:
                for i, obj in enumerate(usr.works):
                    print(i + 1, ".", obj.work_name)

                try:
                    select_work = int(input(f'{Fore.GREEN}enter the work number:{Fore.RESET}'))
                    if 1 <= select_work <= len(usr.works):
                        selected = usr.works[select_work - 1]
                        print(Fore.LIGHTGREEN_EX, f'\n{usr.username} > main menu > {selected.work_name}'
                                                  f' option menu:', Fore.RESET)
                        work_menu(usr, selected)
                    else:
                        raise ValueError
                except ValueError:
                    print(f'please enter a 1 <= number <= {len(usr.works)}')

        elif act == 4:
            check_events(usr)
        elif act == 5:
            print(usr.accept_a_work())
        elif act == 6:
            work_categories_menu(usr)
        elif act == 7:
            print(Fore.LIGHTGREEN_EX, f'{usr.username} > main menu > calendar', Fore.RESET)
            calandar_menu(usr)
        else:
            break


def calendar_menu(current_user):
    """
    this function is for showing works in calendar
    :param current_user: logged in user
    :return:
    """
    select = 0
    while select != 4:
        calandar.show_calandar()


def work_menu(logged_in_user, wrk):
    """
    this function runs if user selects a work. methods
     of work class recall based on action variable as input.
     :param logged_in_user: user who logged in to reminder
    :param wrk: chosen work instance by user
    :return: output parameters of recalled method (for now just a string that describes methods).
    """

    action = 0
    while action != 7:

        print(Fore.MAGENTA, f'\n1. edit {wrk.work_name}'
                            f'\n2. postpone "{wrk.work_name}" to another time'
                            f'\n3. change status of "{wrk.work_name}". (in progress or done)'
                            f'\n4. delete "{wrk.work_name}"'
                            f'\n5. show "{wrk.work_name}"'
                            f'\n6. share "{wrk.work_name}" with a friend'
                            f'\n7. back to previous page', Fore.RESET)

        while ValueError:
            try:
                action = int(input(f'{Fore.GREEN}\nplease select an option from list above:{Fore.RESET}'))
                if action < 0 or action > 7:
                    raise ValueError
                else:
                    break
            except ValueError:
                print(Fore.RED, 'invalid input. Just 1-7 are allowed...', Fore.RED)
        if action == 1:
            print(Fore.BLUE, f'\n{logged_in_user.username} main menu > work menu > {wrk.work_name} > edit ', Fore.RESET)
            print(edit_work_menu(logged_in_user, wrk))
        elif action == 2:
            postpone = datetime.strptime(input('enter New date and time as ((01-31-2020 14:45:37)): '),
                                         "%m-%d-%Y %H:%M:%S")
            print(wrk.postpone(logged_in_user.username, postpone))
        elif action == 3:
            status = input(Fore.CYAN, f'current status: {wrk.status}. please enter new status: ', Fore.RESET)
            print(wrk.change_status(logged_in_user.username, status))
        elif action == 4:
            print(delete_work(logged_in_user, wrk))
            logged_in_user.categorize_works()
            break
        elif action == 5:
            print(wrk)
        elif action == 6:
            print(share(logged_in_user, wrk))
        else:
            break


def edit_work_menu(user, wrk):
    """
    this menu let users edit attributes of their works
    :param user: user logged in to reminder
    :param wrk: selected work object to edit
    :return: an edited work object
    """

    format_string = "%Y-%m-%d %H:%M:%S"
    attributes_dict = {}
    print(f'{user.username} > work: {wrk.work_name} > edit {wrk.work_name}')
    attribute_lst = list(wrk.__dict__.keys())

    for i in range(1, len(attribute_lst) + 1):
        attributes_dict[i] = attribute_lst[i - 1]
        print(f'{i}. {attribute_lst[i - 1]} of {wrk.work_name}')

    new_values = {}
    items = list(map(lambda x: int(x), input('id of items fo editing:(split items with comma)').split(',')))

    edit_items = [attributes_dict[num] for num in items]
    old_values = {_: wrk.__dict__[_] for _ in edit_items}
    out_str = ''
    with open('all_users_works.json', 'r') as data:
        all_work_dict = json.load(data)
        work_dict = all_work_dict[user.username]
        edit_work_file = work_dict[wrk.work_name]

    for itm in edit_items:
        if itm == 'importance' or itm == 'urgency':
            new_val = bool(int(input(f' is {wrk.work_name} {itm}?, current {itm} is {old_values[itm]} (1. yes 0. No)')))
            edit_work_file[itm] = new_val
            new_values[itm] = new_val
        else:
            new_val = input(f'new values of {itm}, current {itm} is {old_values[itm]}')
            edit_work_file[itm] = new_val
            new_values[itm] = new_val
        out_str += f'{itm} changed from >> {old_values[itm]} to >> {new_val}\n'

    if 'work_datetime' in new_values.keys():
        new_values['work_datetime'] = datetime.strptime(new_values['work_datetime'], format_string)

    if 'work_name' in new_values.keys():
        new_work_name = edit_work_file['work_name']
        all_work_dict[user.username][new_work_name] = edit_work_file
        all_work_dict[user.username].pop(wrk.work_name)
        with open('all_users_works.json', 'w') as data:
            json.dump(all_work_dict, data, ensure_ascii=False)

    wrk.edit_work(new_values)
    return out_str


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

