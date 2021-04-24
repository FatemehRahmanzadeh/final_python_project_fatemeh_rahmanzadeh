import user


def login():

    tries = 0
    while tries < 3:

        username = input('please enter your username:')
        password = input('please enter your password:')
        current_user = user.User.login(username, password)
        if not current_user:
            tries += 1
            print(f'username or password is wrong. you have {3-tries} tries')
        else:
            user.user_menu(current_user)
            break
        if tries >= 3:
            print('your account is locked for 20 minutes. try later')


def creat_account():
    try:
        user_data = input('enter requirement like: email, name, last_name, username, password').split(',')
        confirm_password = input('please enter your password again:')
        assert confirm_password == user_data[4]
        new_user = user.User.register(user_data)
        login()
        return new_user
    except AssertionError:
        print('password does not match to confirmation please try again')
        return 0


if __name__ == '__main__':
    login()
    print(creat_account())
