import os
import subprocess
from setuptools import setup, find_packages

setup(
    name="mass_server",
    version="1.0a1",
    packages=find_packages(),
    install_requires=[
        'apispec==0.20.0',
        'APScheduler==3.3.1',
        'blinker==1.4',
        'cffi==1.10.0',
        'click==6.7',
        'docopt==0.6.2',
        'dominate==2.3.1',
        'Faker==0.7.10',
        'Flask==0.12',
        'Flask-APScheduler==1.7.0',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-Login==0.4.0',
        'flask-marshmallow==0.7.0',
        'flask-modular-auth==0.2',
        'flask-mongoengine==0.9.2',
        'Flask-WTF==0.14.2',
        'future==0.16.0',
        'itsdangerous==0.24',
        'Jinja2==2.9.5',
        'MarkupSafe==1.0',
        'marshmallow==2.13.4',
        'marshmallow-mongoengine==0.7.8',
        'mongoengine==0.11.0',
        'pefile==2016.3.28',
        'pycparser==2.17',
        'pymongo==3.4.0',
        'pyparsing==2.2.0',
        'python-dateutil==2.6.0',
        'python-magic==0.4.13',
        'pytz==2016.10',
        'PyYAML==3.12',
        'requests==2.13.0',
        'six==1.10.0',
        'ssdeep==3.2',
        'tzlocal==1.3',
        'uWSGI==2.0.14',
        'visitor==0.1.3',
        'Werkzeug==0.12.2',
        'WTForms==2.1'
    ],
    dependency_links=[
        'git+https://github.com/fabian-rump/flask_modular_auth.git#egg=flask_modular_auth-0.2',
        'git+https://github.com/erocarrera/pefile.git#egg=pefile-2016.3.28'
    ],
    entry_points={
        'console_scripts': ['mass_server=mass_server.bin.mass_server:main']
    }
)
