from getpass import getpass
from mass_flask_core.models import User
from mass_flask_config.app import app

if __name__ == '__main__':
    print('mass-server-flask version' + app.version)
    username = input('Please enter username to create: ')
    password = getpass(prompt='Please enter the password for the new user: ')
    password_verify = getpass(prompt='Enter password again to verify: ')
    if password != password_verify:
        print('Passwords do not match. Exiting.')
        exit(1)
    make_admin = False
    while True:
        input_admin = input('Should the new user have admin privileges? [y/n] ')
        if input_admin == 'y':
            make_admin = True
            break
        elif input_admin == 'n':
            make_admin = False
            break
    user = User()
    user.username = username
    user.set_password(password)
    user._is_admin = make_admin
    user.save()
    print('New user has been created!')
    exit(0)
