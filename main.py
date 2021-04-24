import menu_manager

print('>'*20, 'welcome to reminder', '<'*20)

action = input('you should have ac account to enter:'
               '\n  1. I have an account.    2. I am new to reminder \n\ntype a number here -->>>:')
try:
    if action == '1':
        menu_manager.login()
    elif action == '2':
        menu_manager.creat_account()
    else:
        raise ValueError
except ValueError:
    print('invalid choice please try again')
