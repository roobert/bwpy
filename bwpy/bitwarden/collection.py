#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw
from .org import BitwardenOrg


@dataclass
class BitwardenCollection(BitwardenOrg):
    collection_name: str

    def collection_id(self):
        for collection in self.__org_collections():
            if collection["externalId"] == self.collection_name:
                return collection["id"]
        raise KeyError(f"collection not found: {self.collection_name}")

    def __collection_items(self):
        return json.loads(str(bw.list.items("--collectionid", self.__collection_id())))

    def json(self, filter=None):
        items = []
        for item in self.collection_items():
            if not item["login"]["username"]:
                raise KeyError(f"missing 'username' key for item: {item['name']}")
            if not item["login"]["password"]:
                raise KeyError(f"missing 'password' key for item: {item['name']}")
            if (not filter) or (filter and filter == item["name"]):
                items.append(item)
        if not items:
            raise KeyError(
                f"no items found for collection: {self.collection_name}, filter: {filter}"
            )
        return json.dumps(items)
