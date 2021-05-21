import time
import file_manager
import menu_manager
from user import User
from colorama import Fore


def login():
    """
    this method takes username and and password from user and pass them to login method of user.
    it also manage number of times user enters password wrong
    :return:
    """
    users = file_manager.read_from_file('users_data.json')
    tries = 0
    while True:

        username = input(f'{Fore.YELLOW}please enter your username:')
        password = input(f'please enter your password:{Fore.RESET}')
        current_user = User.login(username, password)
        if not current_user:
            tries += 1
            print(f'{Fore.RED}username or password is wrong. you have {3 - tries} tries{Fore.RESET}')
        else:
            menu_manager.reminder_logger.info(f"{current_user} logged in")
            out = menu_manager.multi_threads(menu_manager.user_menu, menu_manager.notify_on,
                                             args1=current_user, args2=current_user)
            if not out:
                break
        if tries >= 3:
            print(f'{Fore.RED}your account is locked for 20 minutes. try later{Fore.RESET}')
            if username in users:
                menu_manager.reminder_logger.info(f"{username}'s account locked")
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

        action = input(f'{Fore.LIGHTYELLOW_EX}you should have an account to enter:'
                       f'\n{Fore.BLUE}  1. I have an account. '
                       f'   {Fore.MAGENTA}2. I am new to reminder'
                       f'   {Fore.GREEN}3. exit reminder \n\n{Fore.RESET}'
                       'enter a number from menu above -->>>:')

        if action == '1':
            login()

        elif action == '2':
            creat_account()
        elif action == '3':
            break
        else:
            ValueError(action)
    except ValueError:
        print('invalid choice please try again')
