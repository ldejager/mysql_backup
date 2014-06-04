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
        self._backup_date = datetime.now().strftime('%d%m%Y')


    def __check_config__(self):
        """ Check that config file exists """

        try:
            with open(self._config) as f:
                pass
        except IOError as e:
            print 'Unable to open file', e
            exit(1)

    def __dblist__(self):
        """ Obtain list of databases from a running MySQL instance """

        skipdbs = ['Database', 'information_schema', 'performance_schema', 'test']

        try:
            mysql = ['mysql', '--defaults-extra-file='+self._config, '-e', 'show databases']
            p = subprocess.Popen(mysql, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            if p.returncode > 0:
                print 'MySQL Error:'
                print stderr
                exit(1)
            dblist = stdout.strip().split('\n')
            for item in skipdbs:
                try:
                    dblist.remove(item)
                except ValueError:
                    continue
            if len(dblist) == 1:
                print 'No user databases found'
            return dblist
        except:
            print 'Error occurred'

    def __backup__(self, destination):
        """ Backup """

        for db in self.__dblist__():
            backup_file = db+'_'+self._backup_date+'.sql'
            backup_dump = open(os.path.join(destination,backup_file), 'w')
            if db == 'mysql':
                backup_cmd = ['mysqldump', '--defaults-extra-file='+self._config, '--events', db]
            else:
                backup_cmd = ['mysqldump', '--defaults-extra-file='+self._config,  db]
            p = subprocess.Popen(backup_cmd, stdout=backup_dump)
            return_code = p.wait()
            backup_dump.close()
            if return_code > 0:
                print 'Error: There was an error backing up', db
            self.__compress__(destination,backup_file)

    def __compress__(self, destination, backup_file):
        """ Compress """

        tar = tarfile.open(os.path.join(self._destination, backup_file)+'.tar.gz', 'w:gz')
        tar.add(os.path.join(destination, backup_file), arcname=backup_file)
        tar.close()
        os.remove(os.path.join(destination, backup_file))

    def __main__(self):
        """ Main """

        self.__check_config__()
        self.__dblist__()
        self.__backup__(self._destination)


if __name__ == '__main__':

    args_parse = argparse.ArgumentParser(prog='backup.py', usage='%(prog)s [destination]')
    args_parse.add_argument('destination', help='Destination of backup files, defaults to working directory')
    argument = args_parse.parse_args()

    backup = MySQLDBBackup()

    backup.__main__()





