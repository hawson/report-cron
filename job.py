'''base class for a "job".  This can be cron, systemd, atd, etc'''

class Job:

    def __init__(self, source, definition, name=None):
        '''name - the name given to the job, if any...
        source - from whence the job came
        definition - raw or original definition of the job'''
        self.name = name
        self.source = source
        self.definition = definition


    def Name(self):
        if self.name is not None:
            return self.name
        else:
            return ""
