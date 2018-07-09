import os
import re
import subprocess
from setuptools import setup, find_packages

version_file = os.path.join(
    os.path.dirname(__file__),
    'mass_server',
    '__version__.py'
)


with open(version_file, 'r') as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.MULTILINE
    )
    version = m.groups(1)[0]

requirements = [
    'apispec==0.22.1',
    'APScheduler==3.3.1',
    'blinker==1.4',
    'cffi==1.10.0',
    'click==6.7',
    'codecov==2.0.9',
    'coverage==4.4.1',
    'docopt==0.6.2',
    'dominate==2.3.1',
    'Faker==0.7.3',
    'Flask==0.12.2',
    'Flask-APScheduler==1.7.0',
    'Flask-Bootstrap==3.3.7.1',
    'Flask-Login==0.4.0',
    'flask-marshmallow==0.8.0',
    'flask-modular-auth==0.2',
    'flask-mongoengine==0.9.3',
    'flask-slimrest==0.1.2',
    'Flask-WTF==0.14.2',
    'future==0.16.0',
    'itsdangerous==0.24',
    'Jinja2==2.9.6',
    'MarkupSafe==1.0',
    'marshmallow==2.13.5',
    'marshmallow-mongoengine==0.7.8',
    'mixer==5.6.6',
    'mongoengine==0.13.0',
    'nose==1.3.7',
    'nose-exclude==0.5.0',
    'pefile==2017.9.3',
    'pika==0.12.0',
    'pycparser==2.17',
    'pymongo==3.4.0',
    'pyparsing==2.2.0',
    'python-dateutil==2.6.0',
    'python-magic==0.4.13',
    'pytz==2017.2',
    'PyYAML==3.12',
    'requests==2.18.1',
    'six==1.10.0',
    'ssdeep==3.2',
    'tzlocal==1.4',
    'uWSGI==2.0.15',
    'visitor==0.1.3',
    'Werkzeug==0.12.2',
    'WTForms==2.1',
    'raven==6.6.0'
]

setup(
    name='mass-server',
    version=version,
    license='MIT',
    url='https://github.com/mass-project/mass_server/',
    author='Fabian Marquardt',
    author_email='marquard@cs.uni-bonn.de',
    description='Malware Analysis and Storage System server',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    platforms='any',
    test_suite='nose.collector',
    install_requires=requirements,
    tests_require=['nose', 'coverage'],
    entry_points={
        'console_scripts': [
            'mass_server=mass_server.bin.mass_server:main',
            'mass_scheduler=mass_server.bin.mass_scheduler:main',
            'mass_worker=mass_server.bin.mass_worker:main'
        ]
    }
)
