#!/usr/bin/env python

DESCRIPTION = "bitwarden bwcli(1) wrapper to upsert items for organization collections"

import sys
import json
from dataclasses import dataclass
from argparse import ArgumentParser, ArgumentError
from sh import bw, echo


@dataclass
class BitwardenOrg:
    org_name: str

    def org_id(self):
        # FIXME: check for exit status and print out stderr/stdout
        orgs = json.loads(str(bw.list.organizations()))
        for org in orgs:
            if org["name"] == self.org_name:
                return org["id"]
        return None

    def org_collections(self):
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(
            str(bw.list("org-collections", "--organizationid", self.org_id()))
        )


@dataclass
class BitwardenCollection(BitwardenOrg):
    collection_name: str

    def collection_id(self):
        for collection in self.org_collections():
            if collection["externalId"] == self.collection_name:
                return collection["id"]
        return None

    def collection_items(self):
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(bw.list.items("--collectionid", self.collection_id())))

    def __str__(self):
        lines = ""
        for item in self.collection_items():
            if not item["login"]["username"]:
                raise KeyError(f"missing 'username' key for item: {item['name']}")

            if not item["login"]["password"]:
                raise KeyError(f"missing 'password' key for item: {item['name']}")

            lines += f"{item['login']['username']} = \"{item['login']['password']}\"\n"
        return lines.rstrip()


@dataclass
class BitwardenItem(BitwardenCollection):
    item_name: str

    @staticmethod
    def item_template():
        return json.loads(str(bw.get.template.item()))

    @staticmethod
    def login_template():
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(bw.get.template("item.login")))

    def new(self, item_key, item_value):
        login_template = self.login_template()
        login_template["username"] = self.item_name
        login_template[item_key] = item_value
        login_template["totp"] = ""

        item_template = self.item_template()
        item_template["login"] = login_template
        item_template["name"] = self.item_name
        item_template["notes"] = ""

        return item_template

    def create(self, item):
        result = bw.create.item(bw.encode(echo(json.dumps(item))))
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def edit(self, new_item, existing_item_id):
        result = bw.edit.item(existing_item_id, bw.encode(echo(json.dumps(new_item))))
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def share(self, item):
        collection_ids = [self.collection_id()]
        item_id = item["id"]
        # FIXME: check for exit status and print out stderr/stdout
        result = bw.share(
            item_id, self.org_id(), bw.encode(echo(json.dumps(collection_ids)))
        )
        return json.loads(str(result.stdout, "utf-8").rstrip())

    # FIXME: use this
    def check_for_multiple(self):
        item_names = [
            item for item in self.collection_items() if item["name"] == self.item_name
        ]

        if item_names.count() > 1:
            raise Exception(
                f"error: multiple existing entries found for name: {self.item_name}"
            )

    def upsert(self, item_key, item_value):
        # FIXME: split out into update / insert
        for item in self.collection_items():
            if item["name"] == self.item_name:
                new_item = self.new(item_key, item_value)
                new_item["login"] = item["login"]
                new_item["login"][item_key] = item_value
                result = self.edit(new_item, item["id"])
                print(f"updated existing item in organization collection: {item['id']}")
                return json.loads(str(result.stdout, "utf-8").rstrip())

        item = self.create(self.new(item_key, item_value))
        result = self.share(item)
        print(f"created new item in organization collection: {result['id']}")
        return item


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

    return parser, args


def main():
    try:
        parser, args = parse_args()
    except Exception as error:
        print(error)
        sys.exit(1)

    bw.sync()

    if args.output:
        print(BitwardenCollection(org_name=args.org, collection_name=args.collection))
        sys.exit()

    if args.password:
        item = BitwardenItem(
            org_name=args.org, collection_name=args.collection, item_name=args.item
        )
        item.upsert("password", args.password)
        sys.exit()

    if args.item and args.set:
        item = BitwardenItem(
            org_name=args.org, collection_name=args.collection, item_name=args.item
        )
        key, value = args.set.split(":")
        item.upsert(key, value)
        sys.exit()

    parser.print_help()


if __name__ == "__main__":
    main()
