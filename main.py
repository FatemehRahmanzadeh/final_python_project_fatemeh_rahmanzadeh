import menu_manager

while True:
    print('>'*20, 'welcome to reminder', '<'*20)

    action = input('you should have ac account to enter:'
                   '\n  1. I have an account.    2. I am new to reminder   3. exit reminder \n\n'
                   'enter a number from menu above -->>>:')
    try:
        if action == '1':
            menu_manager.login()
        elif action == '2':
            menu_manager.creat_account()
        elif action == '3':
            break
        else:
            raise ValueError
    except ValueError:
        print('invalid choice please try again')
