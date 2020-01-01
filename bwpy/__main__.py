#!/usr/bin/env python

import sys
from .cli import parse_args


def main():
    try:
        args = parse_args()
        args.func(args)

    except Exception as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
