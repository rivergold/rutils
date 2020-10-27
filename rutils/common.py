from pathlib import Path


def str2path(in_str):
    if isinstance(in_str, str):
        return Path(in_str).resolve()
    else:
        raise TypeError('Need input str type')
