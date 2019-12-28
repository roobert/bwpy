#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw, echo
from .bitwarden_collection import BitwardenCollection


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
                f"error: multiple existing entries found for item name in {self.org_name}/{self.collection_name}: {self.item_name}"
            )

    def upsert(self, item_key, item_value):
        # FIXME: split out into update / insert
        for item in self.collection_items():
            if item["name"] == self.item_name:
                print(f"found existing item: {item}")
                new_item = self.new(item_key, item_value)
                new_item["login"] = item["login"]
                new_item["login"][item_key] = item_value
                result = self.edit(new_item, item["id"])
                print(
                    f"updated existing item in {self.org_name}/{self.collection_name}: {self.item_name} ({result['id']})"
                )
                return result

        item = self.create(self.new(item_key, item_value))
        result = self.share(item)
        print(
            f"created new item in {self.org_name}/{self.collection_name}: {self.item_name} ({result['id']})"
        )
        return item
