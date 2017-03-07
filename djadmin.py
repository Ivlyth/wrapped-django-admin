# -*- coding:utf8 -*-
"""
Author : Myth
Date   : 17/3/7S
Email  : belongmyth at 163.com

Wrapped django-admin tool for modify project and app template to add encoding, author, date and so on
"""

import commands
import os
import re
import sys
from ConfigParser import ConfigParser
from datetime import datetime


def ask_info():
    AUTHOR = None
    EMAIL = None

    # interactively to ask user name and user email

    print 'Hi, this is your first time use `djadmin`'

    author = raw_input(u'What\'s your name: ')
    if author:
        AUTHOR = author

    email = raw_input(u'What\'s your email address: ')
    if email:
        EMAIL = email

    if AUTHOR and EMAIL:

        if '@' in EMAIL:
            name, at, suffix = EMAIL.partition('@')
            EMAIL = '%s at %s' % (name, suffix)

        c = ConfigParser()
        c.add_section('djadmin')
        c.set('djadmin', 'author', AUTHOR)
        c.set('djadmin', 'email', EMAIL)
        c.write(open(os.path.expanduser('~/.djadmin.conf'), 'w'))


def get_config_parser():
    config_file = '~/.djadmin.conf'
    if not os.path.isfile(os.path.expanduser(config_file)):
        ask_info()

    if not os.path.isfile(os.path.expanduser(config_file)):
        print 'You must provide user name and user email before you use this tool.'
        print 'Re execute the command to provide information.'
        sys.exit(-1)

    c = ConfigParser()
    c.read(os.path.expanduser(config_file))
    return c


def get_author():
    c = get_config_parser()
    return c.get('djadmin', 'author')


def get_email():
    c = get_config_parser()
    return c.get('djadmin', 'email')


TEMPLATE_BANNER_WITHOUT_ENCODING = '''\
"""
Author : %(author)s
Date   : %(now)s
Email  : %(email)s
"""''' % {
    'author': get_author(),
    'email': get_email(),
    'now': datetime.now().strftime('%Y/%m/%d')
}

TEMPLATE_BANNER_WITH_ENCODING = '''\
# -*- coding:utf8 -*-
%(template)s''' % {
    'template': TEMPLATE_BANNER_WITHOUT_ENCODING,
}


def is_hashbang(line):
    return line.startswith('#!')


def is_encoding(line):
    p = re.compile('coding:')
    return p.search(line) is not None


def insert_banner(param):
    directory = os.path.abspath(param)
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for file_ in files:
                abs_file = os.path.join(root, file_)
                rf = open(abs_file, 'rb')
                first_line = rf.readline()  # may be hashbang(#!) or encoding declare statement( coding: **** )
                second_line = rf.readline()  # may be encoding declare statement( coding: **** )
                remain_old_content = rf.read()

                first_line_write_back = False
                second_line_write_back = False
                encoding_declared = False
                wf = open(abs_file, 'wb')

                if is_hashbang(first_line):
                    wf.write(first_line)
                    first_line_write_back = True
                elif is_encoding(first_line):
                    wf.write(first_line)
                    encoding_declared = True
                    first_line_write_back = True

                if is_encoding(second_line):
                    wf.write(second_line)
                    second_line_write_back = True

                if encoding_declared:
                    wf.write('%s%s' % (TEMPLATE_BANNER_WITHOUT_ENCODING, os.linesep))
                else:
                    wf.write('%s%s' % (TEMPLATE_BANNER_WITH_ENCODING, os.linesep))

                if not first_line_write_back:
                    wf.write(first_line)
                if not second_line_write_back:
                    wf.write(second_line)
                wf.write(remain_old_content)
                wf.close()


def main():
    ret, output = commands.getstatusoutput('django-admin %s' % ' '.join(sys.argv[1:]))
    if output:
        print output

    if ret == 0:  # when command is successfully executed
        if len(sys.argv) > 2:
            command = sys.argv[1]
            param = sys.argv[2]
            if command in ('startproject', 'startapp'):  # if command is either `startproject` or `startapp`
                insert_banner(param)  # insert banner at the beginning of the file


if __name__ == '__main__':
    main()
