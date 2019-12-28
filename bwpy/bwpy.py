#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from sh import bw, ErrorReturnCode
from .bitwarden_item import BitwardenItem
from .bitwarden_collection import BitwardenCollection

DESCRIPTION = "bitwarden bwcli(1) wrapper to upsert items in organization collections"


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION)

    parser.add_argument("-o", "--org", help="organization name", type=str)
    parser.add_argument("-c", "--collection", help="collection name", type=str)
    parser.add_argument("-i", "--item", help="item name", type=str, required=False)
    parser.add_argument(
        "--output",
        help="output collection in format: login = password",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--set",
        help="set an item key/value using format: key:value (valid keys: username, password, totp)",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-p",
        "--password",
        help="update an item username to item name, and password to password",
        type=str,
        required=False,
    )

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(1)

    if not args.org:
        raise Exception("error: org not specified")

    if not args.collection:
        raise Exception("error: collection not specified")

    if not args.set and not args.password and not args.output:
        raise Exception("error: missing argument: --set, --password, or --output")

    if args.password and args.set:
        raise Exception("error: conflicting arguments: --set, --password")

    if args.set and args.output:
        raise Exception("error: conflicting arguments: --set, --output")

    if args.password and args.output:
        raise Exception("error: conflicting arguments: --password, --output")

    if args.item and args.output:
        raise Exception("error: conflicting arguments: --item, --output")

    bw.sync()

    if args.output:
        print(BitwardenCollection(org_name=args.org, collection_name=args.collection))
        bw.sync()
        sys.exit()

    if args.password:
        item = BitwardenItem(
            org_name=args.org, collection_name=args.collection, item_name=args.item
        )
        item.upsert("password", args.password)
        bw.sync()
        sys.exit()

    if args.item and args.set:
        item = BitwardenItem(
            org_name=args.org, collection_name=args.collection, item_name=args.item
        )
        key, value = args.set.split(":")
        item.upsert(key, value)
        bw.sync()
        sys.exit()

    parser.print_help()


def main():
    try:
        parse_args()
    except ErrorReturnCode as error:
        print(f"error: {error}")
    except Exception as error:
        print(error)
    finally:
        sys.exit(1)


if __name__ == "__main__":
    main()
