# This script parses a SQL file based in the evolution template
# from Play! Framework (!Ups and !Downs), and apply the given
# action.

from os import listdir, path, stat
from sys import argv
from time import asctime
from enum import Enum, auto

import re


class Token(Enum):
    SHARP = '#'
    SINGLE_COMMENT = '---'
    UPS = '!Ups'
    DOWNS = '!Downs'


class State(Enum):
    UNKNOWN = 0
    UPS = 1
    DOWNS = 2


def parse(filename: str) -> tuple:
    ups = [f'\n\n-- {filename}\n']
    downs = [f'\n\n-- {filename}\n']
    current_state = State.UNKNOWN
    with open(filename) as fp:
        for line in fp:
            splitted_line = line.replace('\n', '').split()
            if splitted_line != [] and splitted_line[0] == Token.SHARP.value:
                if Token.UPS.value in splitted_line:
                    current_state = State.UPS
                elif Token.DOWNS.value in splitted_line:
                    current_state = State.DOWNS
                else:
                    return None
            else:
                if current_state == State.UPS:
                    ups.append(line)
                elif current_state == State.DOWNS:
                    downs.append(line)
    return (
        ''.join(ups),
        ''.join(downs),
    )


def get_timestamp() -> str:
    return '_'.join(asctime().replace(':', '_').split())


def main(dirname: str) -> None:
    timestamp = get_timestamp()
    ups = []
    downs = []

    for file in sorted(listdir(dirname), key=lambda x: int(re.findall(r'\d+.sql', x)[0].replace('.sql', ''))):
        up, down = parse(path.join(dirname, file))
        ups.append(up)
        downs.append(down)

    with open(f'ups-{timestamp}.sql', 'w') as fp:
        fp.writelines(ups)

    with open(f'downs-{timestamp}.sql', 'w') as fp:
        fp.writelines(downs)


if __name__ == '__main__':
    main(argv[1])
