'''cron class'''

import re

from job import Job
from crontab import CronTab

'''cron_paths - Directories to look for to look for cronjobs.  This is very distro dependent.'''
default_crontab_paths = [
    '/var/spool/cron',
    '/usr/lib/cron/tabs/',
    '/var/cron/tabs/',
    '/var/spool/cron/crontabs/',
    '/var/spool/cron/',
    '/etc/crontab',
]

default_cron_script_paths = [
    '/etc/cron.d',
    '/etc/cron.daily',
    '/etc/cron.weekly',
    '/etc/cron.monthly',
    '/etc/cron.hourly',
]

def find_crontabs(cron_paths=default_crontab_paths):
    '''Look through a set of paths, and return all of the files (nominallly crontab files) found there.  This is pre-seeded with a set of defaults for many distributions.'''
    from pathlib import Path
    import os
    import re

    crontab_paths = []

    for pathname in filter(None, cron_paths):

        path = Path(pathname) 
        if os.access(pathname, os.R_OK) and os.path.isdir(pathname):
            for fname in path.iterdir():
                fullpath = re.sub(r'/{2,}', '/', str(pathname + '/' + fname.name))
                crontab_paths.append(fullpath)

    return list(filter(None, crontab_paths))

def find_cron_scripts(cron_paths = default_cron_script_paths):
    from pathlib import Path

    crontab_paths = []

    for pathname in filter(None, cron_paths):

        path = Path(pathname) 
        if path.is_dir():
            for fname in path.iterdir():
                fullpath = re.sub(r'/{2,}', '/', str(pathname + '/' + fname.name))
                crontab_paths.append(fullpath)

    return list(filter(None, crontab_paths))



def parse_crontab(path):
    '''returns a list of crontab objects'''

    import pathlib

    crontab = []

    # slurp in the file
    text = pathlib.Path(path).read_text()

    # for now, this assumes that there is 1 job per line.
    # Yes, this is a bad assumption, but do the simple case first.
    for line in text.split('\n'):
        line = re.sub('\s*#.*','', line)

        # Skip blank/all whitespace lines 
        if re.match('^\s*$', line):
            continue

        print(line)
        
        # Split into timefields, and "everything else"
        m = re.match(r'(@(?:reboot|yearly|annually|monthly|weekly|daily|hourly)|(?:\S+\s+){5})(.+)', line)
        if m:
            ts, remainder = m.groups()
            print(ts)
            print(remainder)

        # skip non-matching lines
        else:
            continue
        


    return text

class Cronjob(Job):
    pass
