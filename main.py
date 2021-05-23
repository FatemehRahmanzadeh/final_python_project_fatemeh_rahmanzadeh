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
    locked_usrs = file_manager.user_lock_r('lock_user.json')
    if username not in locked_usrs.keys():
        return True

    elif username in locked_usrs.keys():
        lock_time = datetime.strptime(locked_usrs[username], "%Y-%m-%d %H:%M:%S")

        if lock_time + timedelta(seconds=60*2) < datetime.now():
            locked_usrs.pop(username)
            with open('lock_user.json', 'w') as file:
                json.dump(locked_usrs, file, indent=4, ensure_ascii=False)
            return True
        return False


def login():
    """
    this method takes username and and password from user and pass them to login method of user.
    it also manage number of times user enters password wrong
    :return:
    """
    users = file_manager.read_from_file('users_data.json')
    tries = 0
    username = ''
    while True:
        while True:
            try:
                username = input(f'{Fore.YELLOW}please enter your username:{Fore.RESET}')
                check = check_lock(username)
                assert not check
                print(Fore.LIGHTRED_EX, 'your account is lock try later', Fore.RESET)
                continue
            except AssertionError:
                break

        password = input(f'{Fore.YELLOW}please enter your password:{Fore.RESET}')

        current_user = User.login(username, password)
        if not current_user:
            tries += 1
            print(f'{Fore.RED}username or password is wrong. you have {3 - tries} tries{Fore.RESET}')
        else:
            menu_manager.reminder_logger.info(f"{current_user.username} logged in")
            out = menu_manager.multi_threads(menu_manager.user_menu, menu_manager.notify_on,
                                             args1=current_user, args2=current_user)
            if not out:
                break

        if tries >= 3:
            print(f'{Fore.RED}your account is locked for 2 minutes. try later{Fore.RESET}')
            if username in users:
                menu_manager.reminder_logger.info(f"{username}'s account locked")
                locked_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                file_manager.user_lock_w('lock_user.json', username, locked_time)
            break


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
