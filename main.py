import json
from datetime import datetime, timedelta
import file_manager
import menu_manager
from user import User
from colorama import Fore


def check_lock(username):
    """
    this function checks if user's account is lock
    :param username: input username to check
    """
    try:
        users = file_manager.read_from_file('users_data.json')
        user = users[username]
    except KeyError:
        return 2
    if user["status"]:
        return 1

    else:
        lock_time = datetime.strptime(user["lock_time"], "%Y-%m-%d %H:%M:%S")

        if lock_time + timedelta(seconds=60 * 2) < datetime.now():
            user["status"] = True
            file_manager.write_to_file('users_data.json', user, username)
            return 1
        return 0


def lock_user(username):
    """
    if user enters password wrong 3 times, this function will recall and changes status attribute of user to False.
    :param username: target username for locking
    """
    users = file_manager.read_from_file('users_data.json')
    user = users[username]
    print(user)

    if username in users.keys():
        menu_manager.reminder_logger.info(f"one account locked")
        lock_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        user.update({'status': False})
        user.update({'lock_time': lock_time})
        print(user)
        file_manager.write_to_file('users_data.json', user, username)
        print(f'{Fore.RED}your account is locked for 2 minutes. try later{Fore.RESET}')
    else:
        print('pass')


def login():
    """
    this method takes username and and password from user and pass them to login method of user.
    it also manage number of times user enters password wrong
    :return:
    """
    tries = 0
    username = ''
    while True:
        try:
            username = input(f'{Fore.YELLOW}please enter your username:{Fore.RESET}')
            check = check_lock(username)
            if not check:
                print(Fore.LIGHTRED_EX, 'your account is lock try later', Fore.RESET)
                break
            elif check == 2:
                raise ValueError

            password = input(f'{Fore.YELLOW}please enter your password:{Fore.RESET}')

            current_user = User.login(username, password)
            if not current_user:
                tries += 1
                print(f'{Fore.RED}password is wrong. you have {3 - tries} tries{Fore.RESET}')
                menu_manager.reminder_logger.error('password or username is wrong..')
            else:
                menu_manager.reminder_logger.info(f"a user logged in")
                print(f'welcome {current_user.name}. your log in was successful.')
                out = menu_manager.multi_threads(menu_manager.user_menu, menu_manager.notify_on,
                                                 args1=current_user, args2=current_user)
                if not out:
                    break
            if tries >= 3:
                lock_user(username)
                break

        except ValueError:
            print(f'{Fore.LIGHTMAGENTA_EX}no user named "{username}"...! {Fore.RESET}')
            reg_ques = int(input(f'would you like to register?\n{Fore.LIGHTGREEN_EX}1.Yes\n{Fore.RED}0.No{Fore.RESET}'))
            if reg_ques:
                creat_account()
                break
            continue


def creat_account():
    user_data = [input(f'{Fore.GREEN}email: '),
                 input('your name: '),
                 input('your last name: '),
                 input('define an username: '),
                 input(f'enter a secure password: {Fore.RESET}')]

    confirm_password = input('please enter your password again:')
    while True:
        if confirm_password != user_data[4]:
            confirm_password = input('please enter your password again:')
            print('password does not match confirmation..')
            menu_manager.reminder_logger.error('password does not match confirmation..registration failed')
        else:
            new_user = User.register(user_data)
            check = int(input('would you like to log in? 1. yes   2. no '))
            if check == 1:
                login()
                return new_user
            elif check == 2:
                print('Thanks for registration, see you later')
                return new_user
            break


while True:
    try:
        print(Fore.LIGHTCYAN_EX, '\n', '>' * 20, 'welcome to reminder', '<' * 20, '\n', Fore.RESET)

        action = int(input(f'{Fore.LIGHTYELLOW_EX}you should have an account to enter:'
                           f'\n{Fore.BLUE}  1. I have an account. '
                           f'   {Fore.MAGENTA}2. I am new to reminder'
                           f'   {Fore.GREEN}3. exit reminder \n\n{Fore.RESET}'
                           'enter a number from menu above -->>>:'))

        if action == 1:
            login()

        elif action == 2:
            creat_account()
        elif action == 3:
            break
        assert 0 < action < 4

    except AssertionError:
        print(Fore.RED, 'invalid choice please try again', Fore.RESET)
        menu_manager.reminder_logger.error(f'invalid input')

    except ValueError:
        print(Fore.RED, 'invalid choice please enter number..', Fore.RESET)
        menu_manager.reminder_logger.error(f'invalid input. not digit')
