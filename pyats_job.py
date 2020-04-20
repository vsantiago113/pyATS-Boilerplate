from pyats.easypy import Task
import argparse
import getpass


# https://docs.python.org/3/library/argparse.html#action
class PasswordPromptAction(argparse.Action):
    def __init__(self, nargs=0, **kwargs):
        super(PasswordPromptAction, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        values = getpass.getpass()
        setattr(namespace, self.dest, values)


# https://docs.python.org/3/library/argparse.html#action
class UsernamePromptAction(argparse.Action):
    def __init__(self, nargs=0, **kwargs):
        super(UsernamePromptAction, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        values = input('Username: ')
        setattr(namespace, self.dest, values)


# https://docs.python.org/3/library/argparse.html
parse = argparse.ArgumentParser(description='Pass arguments to the pyATS TestCase.')
parse.add_argument('--username', type=str, action=UsernamePromptAction, help='System Login Username.', required=True)
parse.add_argument('--password', type=str, action=PasswordPromptAction, help='System Login Password.', required=True)
args = parse.parse_args()


# https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html
def main(runtime):
    runtime.job.name = 'This is just a test.'
    task1 = Task('mytestcase.py', runtime=runtime, taskid='Testing', username=args.username, password=args.password)
    task1.start()
    task1.join()
