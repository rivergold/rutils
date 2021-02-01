import sys
sys.path.append('.')
from rutils.common import run_command


def test_run_command():
    command = 'echo "test_run_command"'
    run_command(command)
