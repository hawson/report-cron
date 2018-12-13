'''cron class'''

import re
from job import Job

class Cron:

    #cron_paths - Directories to look for to look for cronjobs.
    #This is very distro dependent.'''
    DEFAULT_CRONTAB_PATHS = [
        '/etc/crontab',
        '/usr/lib/cron/tabs/',
        '/var/cron/tabs/',
        '/var/spool/cron/',
        '/var/spool/cron/crontabs/',
        '/etc/cron.d',
    ]

    #cron_paths - Directories to look for to look for scripts
    # automagically called by crond.  This is a bit more standard.
    DEFAULT_CRON_SCRIPT_PATHS = [
        '/etc/cron.daily',
        '/etc/cron.weekly',
        '/etc/cron.monthly',
        '/etc/cron.hourly',
    ]


    def find_crontabs(cron_paths=DEFAULT_CRONTAB_PATHS):
        '''Look through a set of paths, and return all of the files
        (nominallly crontab files) found there.  This is pre-seeded with
        a set of defaults for many distributions.'''
        from pathlib import Path
        import os

        crontab_paths = []

        for pathname in filter(None, cron_paths):

            path = Path(pathname)
            if os.access(pathname, os.R_OK) and os.path.isdir(pathname):
                for fname in path.iterdir():
                    fullpath = re.sub(r'/{2,}', '/', str(pathname + '/' + fname.name))
                    crontab_paths.append(fullpath)

        return list(filter(None, crontab_paths))


    def find_cron_scripts(cron_paths=DEFAULT_CRON_SCRIPT_PATHS):
        '''Look through a set of paths, and return all of the scripts
        found.  These are exectuted directly, at times based on their paths
        (e.g. "hourly" if found in "/etc/cron.hourly")'''
        from pathlib import Path

        crontab_paths = []

        for pathname in filter(None, cron_paths):

            path = Path(pathname)
            if path.is_dir():
                for fname in path.iterdir():
                    fullpath = re.sub(r'/{2,}', '/', str(pathname + '/' + fname.name))
                    crontab_paths.append(fullpath)

        return list(filter(None, crontab_paths))


    def parse_cron_script(path):
        '''returns a single job entry based on a script file'''

        #print("Parsing [%s]"  % path)

        when = "now"
        if   re.match(r'.+cron.hourly', path):
            when = '@hourly'
        elif re.match(r'.+cron.daily', path):
            when = '@daily'
        elif re.match(r'.+cron.weekly', path):
            when = '@weekly'
        elif re.match(r'.+cron.monthly', path):
            when = '@monthly'
        else:
            pass

        return Cronjob(src=path, raw=path, user='root', when=when, cmd=path)


    def parse_crontab(path):
        '''returns a list of cronjob objects based on parsing crontab files'''

        #print("Parsing [%s]"  % path)
        import pathlib
        import os

        jobs = []

        # slurp in the file

        if os.path.isfile(path) and os.access(path, os.R_OK):
            text = pathlib.Path(path).read_text()
        else:
            return None

        # for now, this assumes that there is 1 job per line.
        # Yes, this is a bad assumption, but do the simple case first.
        lineno = 1
        for line in text.split('\n'):
            lineno += 1
            line = re.sub(r'\s*#.*', '', line.strip())

            # Skip blank/all whitespace lines
            if re.match(r'^\s*$', line):
                continue

            #print('>>> '+ line)

            # Split into timefields, and "everything else"
            crontab_re = r'(@(?:reboot|yearly|annually|monthly|weekly|daily|hourly)\s+|(?:[0-9\*,\/-]+\s+){5})(.+)'
            match = re.match(crontab_re, line)
            if match:
                when, remainder = match.groups()
                when = when.strip()
                remainder = remainder.strip()
                #print(when + "|" + remainder)

                job = Cronjob(src=path+':'+str(lineno), raw=line)

                # Kinda of hacky, but search for paths known to use the "cron.d" format
                # of crontab:  the 6th field is a username
                job.cmd = remainder
                job.user = 'root'
                job.when = when

                if re.match(r'^(/etc/cron\.d|/etc/crontab)', path):
                    job.user, job.cmd = remainder.split(maxsplit=1)

                elif re.match(r'^/var', path):
                    job.user = pathlib.PurePath(path).name


                jobs.append(job)

            # skip non-matching lines
            else:
                #print("Bad line: [{}".format(line))
                continue

        return jobs



class Cronjob(Job):
    '''Cron-specific job class'''

    NICKNAMES = {
        '@yearly':  '0 0 1 1 *',
        '@annually':'0 0 1 1 *',
        '@monthly': '0 0 1 * *',
        '@weekly':  '0 0 * * 0',
        '@daily':   '0 0 * * *',
        '@hourly':  '0 * * * *',
    }



    def __str__(self):
        return super(Cronjob, self).__str__()

