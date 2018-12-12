#!/usr/bin/env python3

import time
import re
import sys
import os

import cron


'''cron_files - List of crontabs to parse.  This includes both user crontab (including "root"), and files /etc/cron* directories and files.'''
cron_files = []


'''systemd_timers - List of systemd timers for the system and all users.'''
systemd_timers = []

''' atd_jobs - List of atd jobs for all users.'''
atd_jobs = []


atd_paths = [
    '/var/spool/cron/atjobs',
    '/var/spool/at',
]



jobs = {}

if '__main__' == __name__:

    cron_files = cron.find_crontabs()
    #cron_files = list(map(lambda p: p.name, cron._find_cron_tabs()))

    #print(cron_files)

    cron.parse_crontab('/var/spool/cron/beckerje')



