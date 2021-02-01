from pathlib import Path
import subprocess, traceback
from datetime import datetime
from rlogger import RLogger


def str2path(in_str):
    if isinstance(in_str, str):
        return Path(in_str).resolve()
    else:
        raise TypeError('Need input str type')


def run_command(command):
    RLogger.log('Run command: {}'.format(command))
    try:
        subprocess.check_call(command, shell=True, executable='/bin/bash')
    except Exception as e:
        log_info = f'Run command failed, exception={type(e).__name__},\n{e},\n{"".join(traceback.format_tb(e.__traceback__))}'
        RLogger.log(log_info, RLogger.ERROR)
        raise ValueError(f'Run subcommand error: {log_info}')


def get_current_strtime() -> str:
    return datetime.now().strftime('%Y%m%d-%H%M%S-%f')
