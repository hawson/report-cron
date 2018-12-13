'''base class for a "job".  This can be cron, systemd, atd, etc'''

class Job:
    '''base class for a "job".  This can be cron, systemd, atd, etc'''


    def __init__(self, src, raw, name=None, user=None, cmd=None, when=None):
        '''name - the name given to the job, if any...
        src  - from whence the job came
        raw  - raw or original definition of the job
        user - user for whom this runs
        cmd  - command that is run
        when - "when" the job runs'''

        self.name = name
        self.src = src
        self.raw = raw
        self.user = user
        self.cmd = cmd
        self.when = when

    def __str__(self):
        '''Pretty print the job'''
        return "+---\n|user: {}\n|when: {}\n| cmd: {}\n| src: {}\n| raw: {}".format(
            self.user, self.when, self.cmd, self.src, self.raw)


    def as_json(self):
        """Convert to JSON, and return it"""
        import json
        return json.dumps(vars(self))

