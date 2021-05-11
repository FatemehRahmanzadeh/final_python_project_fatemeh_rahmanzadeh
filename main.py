import menu_manager
from user import User
from colorama import Fore

def login():
    """
    this method takes username and and password from user and pass them to login method of user.
    it also manage number of times user enters password wrong
    :return:
    """
    tries = 0
    while tries < 3:

        username = input(f'{Fore.YELLOW}please enter your username:')
        password = input(f'please enter your password:{Fore.RESET}')
        current_user = User.login(username, password)
        if not current_user:
            tries += 1
            print(f'{Fore.RED}username or password is wrong. you have {3 - tries} tries{Fore.RESET}')
        else:
            menu_manager.user_menu(current_user)
            break
        if tries >= 3:
            print(f'{Fore.RED}your account is locked for 20 minutes. try later{Fore.RESET}')


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
    print('>' * 20, 'welcome to reminder', '<' * 20)

    action = input('you should have an account to enter:'
                   '\n  1. I have an account.    2. I am new to reminder   3. exit reminder \n\n'
                   'enter a number from menu above -->>>:')

    if action == '1':
        login()
    elif action == '2':
        creat_account()
    elif action == '3':
        break
    else:
        print('invalid choice please try again')
