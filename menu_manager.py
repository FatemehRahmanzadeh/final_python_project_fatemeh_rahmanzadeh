import datetime
import logging
import re
from os import path
from colorama import Fore
import user
from work import Work
import file_manager
import threading
import calandar as c

threads = []

reminder_logger = logging.getLogger(__name__)
reminder_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('reminder_logger.log')
file_handler.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)
reminder_logger.addHandler(file_handler)


def create_work(usr):
    """
    this method gets information from user and makes instance of
    Work by calling creat work of class Work
    """
    work_names = [w.work_name for w in usr.works]
    time_format = "%Y-%m-%d %H:%M:%S"
    work_name = ''
    work_datetime = 0
    category = ''
    importance = True
    urgency = True

    while True:
        try:
            work_name = input('title of work:')
            assert work_name not in work_names
            break
        except AssertionError:
            print(f'{Fore.LIGHTRED_EX} work_name already exist in work list{Fore.RESET} ')
            continue

    while True:
        try:
            work_datetime = input('Enter date and time as :(year-month-day hour:min:sec): ')
            assert not re.match(time_format, work_datetime)
            break
        except AssertionError:
            print(f'{Fore.LIGHTRED_EX} wrong date or time format...{Fore.RESET}')
            continue
    while True:
        try:
            importance = input('is this work important? 1. Yes  2. No  ')
            urgency = input('is this work urgent? 1. Yes  2. No  ')
            if importance not in ['1', '2'] or urgency not in ['1', '2']:
                ValueError(importance, urgency)
            importance = True if importance == '1' else False
            urgency = True if urgency == '1' else False
            break

        except ValueError:
            print('invalid input... try again')
            reminder_logger.error(f'invalid input of importance or urgency of create work for {usr.username}')
            continue

    try:
        category = input('choose a category for your work: ')
        assert category in usr.categories.keys()
    except AssertionError:
        reminder_logger.info('new category adds to works list')
        pass

    location = input('location of work (optional): ')
    link = input('add a link related to your work (optional): ')
    description = input('enter a description for your work (optional): ')
    notification = input('enter a notification for your work(optional)')

    work_dict = {
        'work_name': work_name,
        'work_datetime': work_datetime,
        'category': category,
        'status': 'in progress',
        'importance': importance,
        'urgency': urgency,
        'location': location,
        'link': link,
        'description': description,
        'notification': notification
    }

    new_work = Work.create_work(work_dict)
    usr.works.append(new_work)
    new_thread = threading.Thread(name=new_work.work_name, target=new_work.notify, daemon=True)
    threads.append(new_thread)
    new_thread.start()

    print(file_manager.write_to_file('all_users_works.json', work_dict, usr.username, work_dict['work_name']))
    reminder_logger.info(f"'{usr.username}' created '{new_work.work_name}' work successfully", exc_info=True)
    return f'"{Fore.LIGHTGREEN_EX}{new_work.work_name}" were added to your to do list{Fore.RESET}'


def postpone_work(usr, wrk):
    """
    this function postpone a work by changing datetime attribute of work
    :param wrk: target work of user
    :param usr: logged in user to reminder
    :return: a massage about changing datetime of work
    """
    postpone = 0
    while postpone != 5:
        print(f'{Fore.CYAN}How much do you want to postpone "{wrk.work_name}"?'
              f'\n{Fore.LIGHTYELLOW_EX} 1. one hour'
              f'\n{Fore.LIGHTGREEN_EX} 2. one day'
              f'\n{Fore.LIGHTYELLOW_EX} 3. one week'
              f'\n{Fore.LIGHTGREEN_EX} 4. one month'
              f'\n{Fore.LIGHTYELLOW_EX}5. back {Fore.RESET}')

        try:
            p = int(input(f'pick a number for more changes enter >5>1 to edit{wrk.work_name}'))
            options = {1: 'hour', 2: 'day', 3: 'week', 4: 'month'}

            new_datetime = wrk.postpone(1, options[p])
            new_dt_file = new_datetime.strftime("%Y-%m-%d %H:%M:%S")
            update_work = {}
            try:
                assert path.isfile('all_users_works.json')
                update_work = file_manager.read_from_file('all_users_works.json', usr.username)
            except AssertionError:
                print('file not found')
            update_work[wrk.work_name]['work_datetime'] = new_dt_file
            print(file_manager.write_to_file('all_users_works.json', update_work, usr.username))
            reminder_logger.info(f'"{usr.username}" postponed "{wrk.work_name}"', exc_info=True)

            return f'{Fore.GREEN}{wrk.work_name} has been postponed to {new_datetime}{Fore.RESET}'
        except ValueError:
            print(f'{Fore.LIGHTRED_EX} invalid input try again..{Fore.RESET}')
        except IOError:
            print(f'{Fore.LIGHTRED_EX}file read and write error{Fore.RESET}')
            logging.error('error in reading or writing "all_users_works.json"')


def notify_on(usr):
    """
    this function enables notification for every tasks
    if its time has come notify of work object will recall
    first looks for today's user's tasks. Then makes thread for each task.
    start each thread after creation, finally join all of them in a thread list.
"""
    now = datetime.datetime.now()
    if usr.works:
        for _ in usr.works:
            _.work_refresh()
            if _.work_datetime.day == now.day and _.status != "done":
                th = threading.Thread(name=_.work_name, target=_.notify, daemon=True)
                th.start()
                threads.append(th)

        for notify in threads:
            notify.join(2)

    else:
        return f'{Fore.RED} task list is empty...{Fore.RESET}'


def delete_work(logged_in_user, target_work):
    """
    this function deletes a work from user work list and from file
    :param logged_in_user: current user
    :param target_work: selected work object to delete
    :return:
    """
    logged_in_user.delete_work(target_work.work_name)
    for th in threads:
        if th.name == target_work.work_name:
            threads.remove(th)

    user_works_file = file_manager.read_from_file('all_users_works.json', logged_in_user.username)

    user_works_file.pop(target_work.work_name)
    file_manager.write_to_file('all_users_works.json', user_works_file, logged_in_user.username)

    return f'"{target_work.work_name}" has been deleted successfully'


def change_status(usr, wrk):
    """
    this function changes status of work from in progress to done and vice versa
    :param wrk: target work of user
    :param usr: logged in user to reminder
    """
    change_sts = 0
    while change_sts != 3:
        print(f'{Fore.LIGHTGREEN_EX}current status of "{wrk.work_name}" is {wrk.status}{Fore.RESET}')

        try:
            change_sts = int(input(f'do you want to change it? 1. yes{Fore.CYAN}   '
                                   f'2. {Fore.LIGHTGREEN_EX}No{Fore.MAGENTA}3. back{Fore.RESET}:   '))
            if change_sts == 1:
                new_status = wrk.change_status()
                print(f'{Fore.LIGHTGREEN_EX} status of "{wrk.work_name}" changed to "{wrk.status}"{Fore.RESET}')

                all_usr_wrk = file_manager.read_from_file('all_users_works.json', usr.username)
                status_ch = all_usr_wrk[wrk.work_name]
                status_ch['status'] = new_status
                print(file_manager.write_to_file('all_users_works.json', status_ch, usr.username, wrk.work_name))
                reminder_logger.info(f'"{usr.username}" finished "{wrk.work_name}"', exc_info=True)
                break

            elif change_sts == 2:
                print(f'change status of "{wrk.work_name}" has been aborted')
                break
            else:
                ValueError(change_sts)
                continue
        except ValueError:
            print(f'invalid input, try again..')
        except IOError:
            print('something went wrong about "all_users_works.json" file')


def share(sender_user, target_work):
    """
    this function moves work from sender_user to receiver_user if receiver accepts it
    :param sender_user: logged in user
    :param target_work: selected work to be sent
    :return:
    """
    users_from_file = file_manager.read_from_file('users_data.json')
    users_from_file.pop(sender_user.username)
    all_usernames = {i + 1: username for i, username in enumerate(users_from_file.keys())}

    yes_or_no = int(input(f'\n{Fore.GREEN} do you know your friend username? 1. yes 2. no{Fore.RESET}'))

    receiver = ''
    if yes_or_no == 1:
        receiver = input(f'{Fore.BLUE} enter friend username:{Fore.RESET}')
    elif yes_or_no == 2:

        for num, username in all_usernames.items():
            print(f'{Fore.CYAN}{num}. "{username}"{Fore.RESET}')

        select = int(input(f'\n{Fore.MAGENTA} select a friend: '))
        receiver = all_usernames[select]

    receiver_usr = user.User(*(users_from_file[receiver].values()))
    receiver_usr.events[sender_user.username] = target_work
    to_event_file = target_work.__dict__
    to_event_file.pop("priority")
    to_event_file.pop("time_ntf")

    file_manager.write_to_file('events.json', to_event_file, receiver, sender_user.username)

    return f'{Fore.WHITE}"{target_work.work_name}" has been sent to "{receiver_usr.username}"{Fore.RESET}'


def check_events(logged_in_user):
    """
    this function checks event file of user just after log in.
    (work_select variable is a dict to assign number to every event
    work_select = {event_num:(sender, received work as Work obj)})
     User should decide what to do with received work.
    :param logged_in_user: current user in reminder
    :return: a massage about user decision
    """
    all_events = {}
    while True:
        try:
            all_events = file_manager.read_from_file('events.json')[logged_in_user.username]
            assert all_events
        except KeyError:
            print(f'{Fore.GREEN}You have no events...{Fore.RESET}')
            reminder_logger.info(f'"{logged_in_user.username}" has no event so far')
            back = input(f'{Fore.GREEN}enter "b" to back{Fore.RESET}')
            if back:
                break

        except AssertionError:
            print(f'{Fore.BLUE}no new event...{Fore.RESET}')
            reminder_logger.info(f'"{logged_in_user}" has no new event this time')
            back = input(f'{Fore.GREEN}enter "b" to back{Fore.RESET}')
            if back:
                break

        sender_work = {i + 1: event for i, event in enumerate(all_events.items())}
        work_select = {}
        for i, evnt in sender_work.items():
            work_select[i] = (evnt[0], (Work(*(evnt[1].values()))))

        options = len(work_select)

        while work_select:
            for i, evnt in work_select.items():
                print(f'{i}. {evnt[0]}: "{evnt[1].work_name}"')
            print('0. back to main menu')

            select = int(input('choose a work or enter 0 to back:'))

            if 0 < select <= options:
                temp = work_select.pop(select)
                slct_wrk = temp[1]
                all_events.pop(temp[0])
                print(file_manager.write_to_file('events.json', all_events, logged_in_user.username))

                print(f'{Fore.GREEN}information of "{slct_wrk.work_name}": {Fore.RESET}')
                print(f'{slct_wrk}')

                act = int(input(f'{Fore.GREEN}1. accept {Fore.RED}2. reject: {Fore.RESET}'))
                if act == 1:
                    print(logged_in_user.accept_a_work(slct_wrk))
                    wrk_to_file = slct_wrk.__dict__.copy()
                    wrk_to_file.pop("priority")
                    wrk_to_file.pop("time_ntf")
                    print(slct_wrk.__dict__)
                    print(file_manager.write_to_file('all_users_works.json', wrk_to_file,
                                                     logged_in_user.username, slct_wrk.work_name))

                elif act == 2:
                    print(f'\n{Fore.LIGHTYELLOW_EX}{slct_wrk.work_name} has been rejected{Fore.RESET}')
                    continue
            elif select == 0:
                print(f'\n{Fore.CYAN} event check has been aborted {Fore.RESET}')
                break

        if not work_select:
            all_events.clear()
            sender_work.clear()
            print(file_manager.write_to_file('events.json', {}, logged_in_user.username))
            break


def multi_threads(function_1, function_2, args1=None, args2=None):
    """
    switches between threads
    """
    th1 = threading.Thread(target=function_1, args=(args1,))
    th2 = threading.Thread(target=function_2, args=(args2,), daemon=True)
    try:
        th2.start()
        th1.start()
        th2.join(2)
        th1.join()
    except threading.ThreadError:
        print(f'{Fore.RED} Error in running thread{Fore.RESET}')
        logging.error("Error running threads")
        return 0
    if not th1.is_alive():
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

        print('\n', Fore.LIGHTMAGENTA_EX, f'"{usr.username}" > main menu.', Fore.RESET)
        print(Fore.CYAN, '\n 1. add a new work'
                         '\n 2. show all works'
                         '\n 3. go to work directory'
                         '\n 4. check events'
                         '\n 5. categorize works'
                         '\n 6. go to timespan work view'
                         '\n 7. log out', Fore.RESET)
        try:
            act = int(input(f'{Fore.GREEN}\nplease choose a task from menu above:{Fore.RESET}'))
            if act < 0 or act > 7:
                ValueError(act)
        except ValueError:
            print(Fore.RED, 'invalid input. Just 1-8 are allowed', Fore.RESET)
            continue
        if act == 1:
            print(f'{Fore.WHITE}"{usr.username}" > main menu > add a new work{Fore.RESET}')
            print(create_work(usr))
        elif act == 2:
            print(f'{Fore.WHITE}"{usr.username}" > main menu > {usr.username}`s works list{Fore.RESET}')
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
            print(Fore.LIGHTGREEN_EX, f'{usr.username} > main menu > check events{Fore.RESET}')
            check_events(usr)
        elif act == 5:
            work_categories_menu(usr)
        elif act == 6:
            print(Fore.LIGHTGREEN_EX, f'{usr.username} > main menu > timespan view', Fore.RESET)
            date_view(usr)
        else:
            print(usr.log_out())
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
    while action != 7:

        print(Fore.MAGENTA, f'\n1. edit "{wrk.work_name}"'
                            f'\n2. postpone "{wrk.work_name}" to another time'
                            f'\n3. change status of "{wrk.work_name}". (in progress or done)'
                            f'\n4. delete "{wrk.work_name}"'
                            f'\n5. show "{wrk.work_name}"'
                            f'\n6. share "{wrk.work_name}" with a friend'
                            f'\n7. back to previous page', Fore.RESET)

        try:
            action = int(input(f'{Fore.GREEN}\nplease select an option from list above:{Fore.RESET}'))
            if 0 >= action > 7:
                raise ValueError

        except ValueError:
            print(Fore.RED, 'invalid input. Just 1-7 are allowed...', Fore.RED)

        if action == 1:
            print(Fore.BLUE, f'\n{logged_in_user.username} main menu > work menu > {wrk.work_name} > edit ', Fore.RESET)
            print(edit_work_menu(logged_in_user, wrk))
        elif action == 2:
            print(f'{Fore.GREEN} "{logged_in_user.username}" > "{wrk.work_name}" > postpone:{Fore.RESET}')
            print(postpone_work(logged_in_user, wrk))

        elif action == 3:
            print(change_status(logged_in_user, wrk))
        elif action == 4:
            print(delete_work(logged_in_user, wrk))
            break
        elif action == 5:
            print(wrk)
        elif action == 6:
            print(share(logged_in_user, wrk))
        else:
            break


def edit_work_menu(usr, wrk):
    """
    this menu let users edit attributes of their works
    :param usr: user logged in to reminder
    :param wrk: selected work object to edit
    :return: an edited work object
    """

    items = []
    attributes_dict = {}
    attribute_lst = list(wrk.__dict__.keys())
    if ('priority' in attribute_lst) or ('time_ntf' in attribute_lst):
        attribute_lst.pop(attribute_lst.index('priority'))
        attribute_lst.pop(attribute_lst.index('time_ntf'))

    count = 0
    R = Fore.RESET
    for i in range(1, len(attribute_lst) + 1):
        if count % 2 == 0:
            C = Fore.LIGHTCYAN_EX
        else:
            C = Fore.LIGHTWHITE_EX
        attributes_dict[i] = attribute_lst[i - 1]
        print(f'{i}. {C}{attribute_lst[i - 1]} of {wrk.work_name}{R}')
        count += 1

    new_values = {}
    while True:
        try:
            items = list(map(lambda x: int(x), input('id of items fo editing:'
                                                     '(split items with comma): ').strip().split(',')))
            for itm in items:
                assert 1 <= itm <= 10
                if not isinstance(itm, int):
                    ValueError(itm)
            assert len(items) <= 10
            break
        except AssertionError:
            print(f"\n{Fore.RED} invalid input... just 1 - 10 are allowed."
                  f" you don't have more than 10 option{Fore.RESET}")
        except ValueError:
            print(f'\n{Fore.LIGHTRED_EX} invalid input. input must be integer')
            continue

    edit_items = [attributes_dict[num] for num in items]
    old_values = {_: wrk.__dict__[_] for _ in edit_items}
    out_str = ''
    work_dict = file_manager.read_from_file('all_users_works.json', usr.username)
    edit_work_file = work_dict[wrk.work_name]
    new_val = None
    cnt = 0
    R = Fore.RESET
    for itm in edit_items:
        if cnt % 2 == 0:
            C = Fore.BLUE
        else:
            C = Fore.LIGHTMAGENTA_EX

        if itm == 'importance' or itm == 'urgency':
            new_val = bool(int(input(f'{C} is {wrk.work_name} {itm}?,'
                                     f' current {itm} is {old_values[itm]} (1. yes 0. No){R}')))
            edit_work_file[itm] = new_val
            new_values[itm] = new_val

        elif itm == 'work_datetime':
            while True:
                try:
                    new_val = input(f'{C}new values of {itm}, current {itm} is {old_values[itm]}{R}')
                    if not re.match("%Y-%m-%d %H:%M:%S", new_val):
                        ValueError(new_val)
                        edit_work_file[itm] = new_val
                        new_values[itm] = new_val
                    new_values['work_datetime'] = datetime.datetime.strptime(new_values['work_datetime'],
                                                                             "%Y-%m-%d %H:%M:%S")
                    break
                except ValueError:
                    print(Fore.LIGHTRED_EX, f'invalid datetime format. try this: year-month-day hour:minutes:second', R)
                    continue
        else:
            new_val = input(f'{C}new values of {itm}, current {itm} is {old_values[itm]}{R}')
            edit_work_file[itm] = new_val
            new_values[itm] = new_val
        out_str += f'{C}{itm} changed from >> {old_values[itm]} to >> {new_val}\n{R}'
        cnt += 1

    if 'work_name' in new_values.keys():
        new_work_name = edit_work_file['work_name']
        work_dict[new_work_name] = edit_work_file
        work_dict.pop(wrk.work_name)

    file_manager.write_to_file('all_users_works.json', work_dict, usr.username)
    wrk.edit_work(new_values)
    print(wrk.__dict__)

    th_names = [th.name for th in threads]
    if wrk.work_name in th_names:
        for th in threads:
            if wrk.work_name == th.name:
                th.join(1)
    else:
        th = threading.Thread(name=wrk.work_name, target=wrk.notify, daemon=True)
        threads.append(th)
        th.start()
        th.join(1)

    reminder_logger.info(f'{usr.username} edited {wrk.work_name}:\n{out_str}')
    return out_str


def work_categories_menu(logged_in_user):
    """
    this menu shows works of user in organized categories
    :param logged_in_user: current user who logged in
    :return: a massage of successful categorising or an error if something goes wrong
    """
    all_categories = logged_in_user.categorize_works()

    while True:
        print(Fore.BLUE, '\n', '-.' * 30, 'list of categories:', '-.' * 30, Fore.RESET)

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
                print(Fore.BLUE, '\n', '×' * 50, f'list of works in {selected_cat}:', '×' * 50, Fore.RESET)

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


def date_view(usr):
    """
    this method shows works in specific month, week or day that user selects
    :param usr:
    :return: a table of works name and dates if found
    """
    timespan = 0
    while True:

        date = datetime.datetime.now()
        print(Fore.LIGHTMAGENTA_EX, '\nyou can see current works here in selected timespan\n', Fore.RESET)

        print(f'{Fore.GREEN}select a timespan:{Fore.RESET}'
              f'{Fore.CYAN}\n1. month {Fore.RESET}'
              f'{Fore.MAGENTA}   2. week {Fore.RESET}'
              f'{Fore.LIGHTGREEN_EX}   3. day{Fore.RESET}'
              f'{Fore.BLUE}   4. back{Fore.RESET}')
        try:
            timespan = int(input(f'{Fore.LIGHTWHITE_EX} enter your number here: {Fore.RESET}'))
            assert 1 <= timespan <= 4
        except AssertionError:
            print(f'{Fore.LIGHTRED_EX} invalid input enter number between 1 to 4{Fore.RESET}')
            reminder_logger.error(f'input error for {usr.username}')

        choice = {1: lambda u, d: c.show_month_works(u, d),
                  2: lambda u, d: c.show_week_works(u, d),
                  3: lambda u, d: c.show_day_works(u, d)}
        if timespan == 4:
            break
        else:
            try:
                print("\n", Fore.BLUE, choice[timespan](usr, date), Fore.RESET, "\n")
            except IOError:
                print(Fore.LIGHTRED_EX, '\nsomething went wrong in calandar module', Fore.RESET)
                reminder_logger.error(f'error in {usr.username} app, in calendar module..')
