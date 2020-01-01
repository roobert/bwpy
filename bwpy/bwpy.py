#!/usr/bin/env python

import sys
from .cli import parse_args
from sh import bw


def main():
    try:
        bw.sync()
        args = parse_args()
        args.func(args)
        bw.sync()

    except Exception as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
