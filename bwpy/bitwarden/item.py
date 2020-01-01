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

    def __new(self, new_item_data):
        item_template = self.item_template()
        login_template = self.login_template()
        item_template["login"] = login_template
        item_template["login"]["totp"] = ""
        item_template["notes"] = ""
        item_template["name"] = self.item_name
        item_template.update(new_item_data)
        return item_template

    def __check_exists(self):
        for item in self.collection_items():
            if item["name"] == self.item_name:
                return True

    def __share(self, item):
        collection_ids = [self.__collection_id()]
        item_id = item["id"]
        result = bw.share(
            item_id, self.__org_id(), bw.encode(echo(json.dumps(collection_ids)))
        )
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def __create(self, item):
        result = bw.create.item(bw.encode(echo(json.dumps(item))))
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def __edit(self, new_item, existing_item_id):
        result = bw.edit.item(existing_item_id, bw.encode(echo(json.dumps(new_item))))
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def update(self, new_item_data):
        for item in self.collection_items():
            if item["name"] == self.item_name:
                result = self.__edit(self.__new(new_item_data), item["id"])
                return result
        raise KeyError(f"item not found: {self.item_name}")

    def insert(self, new_item_data):
        if self.__check_exists():
            raise KeyError(f"item already exists: {self.item_name}")
        item = self.__create(self.__new(new_item_data))
        result = self.__share(item)
        return result

    def upsert(self, new_item_data):
        if self.__check_exists():
            result = self.update(new_item_data)
        else:
            result = self.insert(new_item_data)
        return result
