import argparse
from mass_server import get_app


def run_development(args):
    app = get_app(debug=True, set_server_name=True)
    app.run(host=args.listen, port=args.port)


def run_uwsgi(args):
    import subprocess
    subprocess.run([
        'uwsgi',
        '--module',
        'mass_server.wsgi',
        '--callable',
        'app',
        '--http-socket',
        '{}:{}'.format(args.listen, args.port),
        '--master',
        '--workers',
        '{}'.format(args.workers),
        '--enable-threads',
        '--lazy-apps'
    ])


def run_tests(args):
    import subprocess
    result = subprocess.run('nosetests')
    exit(result.returncode)


def create_user(args):
    from getpass import getpass
    from mass_server.core.models import User, UserLevel
    app = get_app()
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
    if make_admin:
        user.user_level = UserLevel.USER_LEVEL_ADMIN
    else:
        user.user_level = UserLevel.USER_LEVEL_USER
    user.save()


def clear_db(args):
    from mongoengine import connection
    input_drop = input('Do you really want to clear your MASS database? ALL DATA WILL BE LOST! Type uppercase "yes" to continue. ')
    if input_drop != 'YES':
        print('Aborted.')
        return
    app = get_app()
    conn = connection.get_connection()
    db = connection.get_db()
    conn.drop_database(db)
    print('Database cleared.')


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_run_development = subparsers.add_parser(
        'run_development', help='Start the MASS server in development mode')
    parser_run_development.add_argument(
        '--port',
        default=8000,
        type=int,
        help='Specify the port which the server will listen on')
    parser_run_development.add_argument(
        '--listen',
        default='127.0.0.1',
        help=
        'Specify the listening address (e.g. 127.0.0.1 to listen only on localhost or 0.0.0.0 to allow external access to the server)'
    )
    parser_run_development.set_defaults(func=run_development)

    parser_run_uwsgi = subparsers.add_parser(
        'run_uwsgi', help='Start the MASS server production mode')
    parser_run_uwsgi.add_argument(
        '--port',
        default=8000,
        type=int,
        help='Specify the port which the server will listen on')
    parser_run_uwsgi.add_argument(
        '--listen',
        default='0.0.0.0',
        help=
        'Specify the listening address (e.g. 127.0.0.1 to listen only on localhost or 0.0.0.0 to allow external access to the server)'
    )
    parser_run_uwsgi.add_argument(
        '--workers',
        default=5,
        type=int,
        help='Specify the amount of worker processes')
    parser_run_uwsgi.set_defaults(func=run_uwsgi)

    parser_run_tests = subparsers.add_parser(
        'run_tests', help='Run unit tests')
    parser_run_tests.set_defaults(func=run_tests)

    parser_create_user = subparsers.add_parser(
        'create_user', help='Create a new user account')
    parser_create_user.set_defaults(func=create_user)

    parser_clear_db = subparsers.add_parser(
        'clear_db', help='Remove all contents from the MASS database')
    parser_clear_db.set_defaults(func=clear_db)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        print('No command specified. Exiting.')


if __name__ == '__main__':
    main()
