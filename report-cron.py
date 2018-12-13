#!/usr/bin/env python3
'''Reports on periodic jobs run on this host.  Needs elevated privileges
to funtion.'''

#import time
#import re
#import sys
#import os
#import json

from cron import Cron
from at import At


#cron_files - List of crontabs to parse.  This includes both user
#crontab (including "root"), and files /etc/cron* directories and files.
cron_files = []


#systemd_timers - List of systemd timers for the system and all users.
systemd_timers = []

#atd_jobs - List of atd jobs for all users.
atd_jobs = []

atd_paths = [
    '/var/spool/cron/atjobs',
    '/var/spool/at',
]



if __name__ == '__main__':

    jobs = []
    crontab_files = Cron.find_crontabs()
    cron_script_files = Cron.find_cron_scripts()
    #cron_files = list(map(lambda p: p.name, cron._find_cron_tabs()))

    #print("Found crontab files:")
    #print(crontab_files)

    for f in crontab_files:
        newjobs = Cron.parse_crontab(f)
        if newjobs:
            jobs.extend(newjobs)

    #print("Found cron script files:")
    #print(cron_script_files)
    for f in cron_script_files:
        jobs.extend([Cron.parse_cron_script(f)])

    jobs.extend(At.find_jobs())

    for j in jobs:
        print(j)

    #for j in jobs:
    #    print(j.as_json())
