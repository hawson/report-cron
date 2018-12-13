'''cron class'''

# [beckerje@bellona report-cron]$ atq
# 1	Thu Dec 13 12:00:00 2018 a beckerje
# 5	Fri Dec 14 00:03:00 2018 a beckerje
# 4	Fri Dec 14 00:01:00 2018 a beckerje
# 3	Fri Dec 14 00:00:00 2018 a beckerje


from job import Job

class At(Job):


    # command to call for dumping the queue
    ATQ = '/usr/bin/atq'

    def atd_installed():
        import os
        return os.path.exists(At.ATQ) and os.access(At.ATQ, os.X_OK)


    def parse_job(entry):
        '''Parse a single job entry from atq'''
        # Return an empty list on failure.
        # 4	Fri Dec 14 00:01:00 2018 a beckerje
        # jobid ^------timestamp-------^ Q user

        import re

        job_re = r'^\s*(\d+)\s+(\w{3}.+\d+) (\w) (\w+)'

        match = re.match(job_re, entry)
        if match:
            jobid, timestamp, queue, user = match.groups()
            src = 'atd queue {} job {}'.format(queue,jobid)
            cmd = 'execute this command: at -c %s' % jobid
            return At(src=src, user=user, when=timestamp, raw=entry, cmd=cmd)
        else:
            return []







    def find_jobs():
        '''Dump the atd queues, and return a list of jobs.'''

        import subprocess
        import re
        import sys

        if not At.atd_installed():
            return None

        jobs = []
        text = None

        try :
            text = subprocess.check_output(At.ATQ,  universal_newlines=True)

        except subprocess.CalledProcessError as e:
            print("Failed to run [%s]: [%s], [%s]" %(e.cmd, e.stdout, e.stderr))
            sys.exit(e.returncode)

        for line in text.strip().split('\n'):
            jobs.append(At.parse_job(line))

        return jobs



