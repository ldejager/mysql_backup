#!/usr/bin/env python
#
# MySQL Database Backup

import argparse
import ConfigParser
import subprocess
import sys
import os
import tarfile
from datetime import datetime


class MySQLDBBackup(object):
    """ MySQL Backup Class """

    def __init__(self):
        """ Initializing """

        self._config = 'config.cfg'
        self._destination = argument.destination

    def __check_config__(self):
        """ Check that config file exists """

        try:
            with open(self._config) as f:
                pass
        except IOError as e:
            print "Unable to open file", e
            exit(1)

    def __dblist__(self):
        """ Obtain list of databases from a running MySQL instance """

        skipdbs = ['Database', 'information_schema', 'performance_schema', 'test']

        try:
            mysql = ['mysql', '--defaults-extra-file='+self._config, '-e', 'show databases']
            p = subprocess.Popen(mysql, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            if p.returncode > 0:
                print "MySQL Error:"
                print stderr
                exit(1)
            dblist = stdout.strip().split('\n')
            for item in skipdbs:
                try:
                    dblist.remove(item)
                except ValueError:
                    continue
            if len(dblist) == 1:
                print "No user databases found"
            return dblist
        except:
            print "Error occurred"

    def __backup__(self):
        """ Backup """

        for db in self.__dblist__():
            print db
            return db

    def __main__(self):
        """ Main """

        self.__check_config__()
        self.__dblist__()
        self.__backup__()


if __name__ == '__main__':

    args_parse = argparse.ArgumentParser(prog='backup.py', usage='%(prog)s [destination]')
    args_parse.add_argument('destination', help='Destination of backup files, defaults to working directory')
    argument = args_parse.parse_args()

    backup = MySQLDBBackup()

    backup.__main__()





