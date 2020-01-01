#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw, echo
from .collection import BitwardenCollection


@dataclass
class BitwardenItem(BitwardenCollection):
    item_name: str

    @staticmethod
    def _item_template():
        return json.loads(str(bw.get.template.item()))

    @staticmethod
    def _login_template():
        return json.loads(str(bw.get.template("item.login")))

    def _new(self, new_item_data):
        item_template = self._item_template()
        login_template = self._login_template()
        item_template["login"] = login_template
        item_template["login"]["totp"] = ""
        item_template["notes"] = ""
        item_template["name"] = self.item_name
        item_template.update(new_item_data)
        return item_template

    def _check_exists(self):
        for item in self.collection_items():
            if item["name"] == self.item_name:
                return True

    def _share(self, item):
        collection_ids = [self.collection_id()]
        item_id = item["id"]
        result = bw.share(
            item_id, self.org_id(), bw.encode(echo(json.dumps(collection_ids)))
        )
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def _create(self, item):
        result = bw.create.item(bw.encode(echo(json.dumps(item))))
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def _edit(self, new_item, existing_item_id):
        result = bw.edit.item(existing_item_id, bw.encode(echo(json.dumps(new_item))))
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def update(self, new_item_data):
        for item in self.collection_items():
            if item["name"] == self.item_name:
                result = self._edit(self._new(new_item_data), item["id"])
                return result
        raise KeyError(f"item not found: {self.item_name}")

    def insert(self, new_item_data):
        if self._check_exists():
            raise KeyError(f"item already exists: {self.item_name}")
        item = self._create(self._new(new_item_data))
        result = self._share(item)
        return result

    def upsert(self, new_item_data):
        if self._check_exists():
            result = self.update(new_item_data)
        else:
            result = self.insert(new_item_data)
        return result
