#!/usr/bin/env python

import sys
import json
from argparse import ArgumentParser
from .bitwarden.item import BitwardenItem
from .bitwarden.collection import BitwardenCollection
from .bwpy import pull, push


class ExtendedHelpArgumentParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n\n" % message)
        self.print_help()
        sys.exit(2)


def add_sub_command_push(subparsers):
    parser_push = subparsers.add_parser("push", help="push item to remote server")

    parser_push.add_argument(
        "-i", "--item", help="item name to push to", type=str, required=True
    )
    parser_push.add_argument(
        "-j",
        "--json",
        help="json to into item template when creating or updating an item",
        type=str,
        required=True,
    )
    parser_push.add_argument(
        "-f",
        "--force",
        help="overwrite remote item if it already exists",
        action="store_true",
        required=False,
    )
    parser_push.add_argument(
        "-s",
        "--silent",
        help="do not output success message(s)",
        action="store_true",
        required=False,
    )

    parser_push.set_defaults(func=push)


def add_sub_command_pull(subparsers):
    parser_pull = subparsers.add_parser(
        "pull",
        help="fetch remote item(s) from server, defaults to password field",
        description="fetch items from organization collection - by default fetch all items",
    )

    parser_pull.add_argument(
        "-i",
        "--item",
        help="fetch specific item, by item name",
        type=str,
        required=False,
    )

    parser_pull.set_defaults(func=pull)


def add_root_command_args(parser):
    parser.add_argument(
        "-o", "--org", help="organization name", required=True, type=str
    )
    parser.add_argument(
        "-c", "--collection", help="collection name", required=True, type=str
    )


def parse_args():
    parser = ExtendedHelpArgumentParser(
        description="bitwarden bwcli(1) wrapper to upsert items in organization collections"
    )

    add_root_command_args(parser)

    subparsers = parser.add_subparsers(help="sub_command help", dest="sub_command")
    subparsers.required = True

    add_sub_command_pull(subparsers)
    add_sub_command_push(subparsers)

    return parser.parse_args()
