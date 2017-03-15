from setuptools import setup

setup(
    name='djadmin_template',
    version='0.1.0',
    url='https://github.com/MythRen/wrapped-django-admin',
    license='None',
    author='Myth',
    author_email='email4myth@gmail.com',
    description='Wrapped django-admin tool for modify project and app template to add encoding, author, date and so on',
    scripts=['djadmin.py'],
    entry_points={
        'console_scripts': [
            'djadmin = djadmin:main'
        ]
    }
)
