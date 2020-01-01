#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw, echo
from .collection import BitwardenCollection


@dataclass
class BitwardenItem(BitwardenCollection):
    item_name: str

    @staticmethod
    def item_template():
        return json.loads(str(bw.get.template.item()))

    @staticmethod
    def login_template():
        return json.loads(str(bw.get.template("item.login")))

    def new(self, new_item_data):
        item_template = self.item_template()
        login_template = self.login_template()
        item_template["login"] = login_template
        item_template["login"]["totp"] = ""
        item_template["notes"] = ""
        item_template["name"] = self.item_name
        item_template.update(new_item_data)
        return item_template

    def check_exists(self):
        for item in self.collection_items():
            if item["name"] == self.item_name:
                return True

    def share(self, item):
        collection_ids = [self.collection_id()]
        item_id = item["id"]
        result = bw.share(
            item_id, self.org_id(), bw.encode(echo(json.dumps(collection_ids)))
        )

        return json.loads(str(result.stdout, "utf-8").rstrip())

    def create(self, item):
        result = bw.create.item(bw.encode(echo(json.dumps(item))))
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def edit(self, new_item, existing_item_id):
        result = bw.edit.item(existing_item_id, bw.encode(echo(json.dumps(new_item))))
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def insert(self, new_item_data):
        if self.check_exists():
            raise Exception(f"item already exists: {self.item_name}")
        item = self.create(self.new(new_item_data))
        result = self.share(item)
        print(
            f"created new item in {self.org_name}/{self.collection_name}:"
            + f" {self.item_name} ({result['id']})"
        )
        return result

    def update(self, new_item_data):
        for item in self.collection_items():
            if item["name"] == self.item_name:
                result = self.edit(self.new(new_item_data), item["id"])
                print(
                    f"updated existing item in {self.org_name}/{self.collection_name}: "
                    + f"{self.item_name} ({result['id']})"
                )
                return result
        return KeyError(f"item not found: {self.item_name}")

    def upsert(self, new_item_data):
        if self.check_exists():
            result = self.update(new_item_data)
        else:
            result = self.insert(new_item_data)
        return result
