from argparse import ArgumentParser
from rutils.common import str2path

if __name__ == '__main__':
    opt_parser = ArgumentParser()
    opt_parser.add_argument('--in_path', type=str2path)
    opt = opt_parser.parse_args()
    print(opt.in_path)
